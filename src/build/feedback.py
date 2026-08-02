#!/usr/bin/env python3
"""把使用者回饋整理成摘要，並可直接開成 GitHub Issue（GitHub 會寄信通知你）。

為什麼不做「每則寄一封信」：單則通知很快變成噪音，看幾天就開始忽略，
而忽略掉的通知等於沒有通知。這支改成產出**一份摘要**，只在有新回饋時發。

為什麼用 GitHub Issue 當送信管道：
不必接第三方寄信服務、不必再存一組金鑰。repo 已經開了 Issues，
而 GitHub 本來就會把新 Issue 寄到你的信箱——順便留下公開可討論的紀錄，
其他人也看得到、可以回覆。

用法：
    make feedback                       # 印出摘要
    make feedback ARGS="--since 7d"     # 只看最近七天
    make feedback ARGS="--post"         # 另外開一個 GitHub Issue（會寄信給你）
    make feedback ARGS="--json"
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COURSE = Path(os.environ.get("COURSE") or ROOT / "course").resolve()
DATA = COURSE / "data"
CFG = json.loads((COURSE / "course.config.json").read_text())
SITE = CFG["site"]["url"]
REPO = (CFG.get("discussions") or {}).get("repo") or ""
REASONS = {r["id"]: r["label"] for r in (CFG.get("ratings") or {}).get("reasons", [])}
STATE = DATA / "feedback-state.json"


def env_token() -> str | None:
    """FEEDBACK_TOKEN 從環境或 .env 讀，絕不印出來。"""
    if tok := os.environ.get("FEEDBACK_TOKEN"):
        return tok
    envf = ROOT / ".env"
    if envf.exists():
        for line in envf.read_text().splitlines():
            if line.startswith("FEEDBACK_TOKEN="):
                return line.split("=", 1)[1].strip()
    return None


def parse_since(s: str | None) -> int:
    """'7d' / '24h' / epoch / None(=上次跑到哪)。"""
    if not s:
        try:
            return int(json.loads(STATE.read_text()).get("latest_ts", 0))
        except (OSError, json.JSONDecodeError, ValueError):
            return 0
    if m := re.fullmatch(r"(\d+)([dh])", s.strip()):
        n, unit = int(m.group(1)), m.group(2)
        return int(time.time()) - n * (86400 if unit == "d" else 3600)
    return int(s)


def video_index() -> dict[str, list[dict]]:
    """video id -> 掛在哪些單元。回饋要能直接對到課程位置才有用。"""
    idx: dict[str, list[dict]] = defaultdict(list)
    for path in sorted(DATA.glob("ch*.json")):
        try:
            blob = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        for node in blob.get("chapters") or [blob]:
            code = node.get("chapter") or "?"
            for u in node.get("units") or []:
                for role, v in [("核心教材", u.get("lesson"))] + [
                    ("資源", d) for d in (u.get("drills") or [])
                ]:
                    if not v or not v.get("url"):
                        continue
                    if m := re.search(r"(?:v=|youtu\.be/)([\w-]{11})", v["url"]):
                        idx[m.group(1)].append(
                            {
                                "chapter": code,
                                "unit": u.get("id"),
                                "role": role,
                                "name": v.get("name") or v.get("title"),
                            }
                        )
    return idx


def fetch(since: int, token: str) -> dict:
    url = f"{SITE.rstrip('/')}/api/feedback?since={since}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "User-Agent": "thyroid-course/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return json.loads(res.read())
    except urllib.error.HTTPError as e:
        hint = {
            401: "token 不對——Cloudflare 的 FEEDBACK_TOKEN 與本機 .env 要一致",
            503: "後端沒設 FEEDBACK_TOKEN 或沒綁 D1",
        }.get(e.code, f"HTTP {e.code}")
        print(f"✗ 讀不到回饋：{hint}", file=sys.stderr)
        return {}


def digest(data: dict, idx: dict) -> tuple[str, dict]:
    items = data.get("items") or []
    if not items:
        return "", {}

    by_video: dict[str, list[dict]] = defaultdict(list)
    for r in items:
        by_video[r["video"]].append(r)

    lines: list[str] = []
    scores = Counter()
    comments = [r for r in items if r.get("comment")]

    for r in items:
        scores[r["score"]] += 1

    lines.append(f"共 {len(items)} 則回饋，其中 {len(comments)} 則有文字說明。")
    lines.append("")
    lines.append(
        "分數分布："
        + "、".join(f"{s} 分 {n}" for s, n in sorted(scores.items(), reverse=True))
    )
    lines.append("")

    # 先講最需要處理的：有文字的、低分的
    ranked = sorted(
        by_video.items(),
        key=lambda kv: (
            -sum(1 for r in kv[1] if r.get("comment")),
            sum(r["score"] for r in kv[1]) / len(kv[1]),
        ),
    )

    for vid, rows in ranked:
        where = idx.get(vid) or []
        head = (
            f"{where[0]['chapter']} {where[0]['unit']} · {where[0]['name']}"
            if where
            else "（已不在課程裡）"
        )
        avg = sum(r["score"] for r in rows) / len(rows)
        lines.append(f"### {head}")
        lines.append("")
        lines.append(f"平均 {avg:.1f}／5（{len(rows)} 則） · https://youtu.be/{vid}")
        tags = Counter(r["reason"] for r in rows if r.get("reason"))
        if tags:
            lines.append("")
            for t, n in tags.most_common():
                lines.append(f"- {REASONS.get(t, t)}：{n}")
        for r in rows:
            if r.get("comment"):
                lines.append("")
                lines.append(f"> {r['comment']}")
                lines.append(">")
                lines.append(f"> — {r['score']} 分")
        lines.append("")

    return "\n".join(lines), {"count": len(items), "comments": len(comments)}


def post_issue(body: str, meta: dict) -> int:
    if not REPO:
        print("✗ course.config.json 沒有 discussions.repo，不知道要開在哪個 repo", file=sys.stderr)
        return 1
    title = f"使用者回饋摘要：{meta['count']} 則（{meta['comments']} 則有文字）"
    note = (
        "\n\n---\n\n"
        "由 `make feedback ARGS=\"--post\"` 產生。文字回饋是匿名的、未經驗證，"
        "當成待查線索而不是結論；要換片前請自己打開影片確認。\n"
        "完整換片清單見 `make ratings`。"
    )
    proc = subprocess.run(
        ["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", body + note],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0:
        print(f"✗ 開 Issue 失敗：{(proc.stderr or '').strip()[:200]}", file=sys.stderr)
        return 1
    print(f"→ {proc.stdout.strip()}")
    print("   GitHub 會把這則 Issue 寄到你的信箱，其他人也看得到、可以回覆。")
    return 0


def main() -> int:
    args = sys.argv[1:]
    as_json = "--json" in args
    do_post = "--post" in args
    since_arg = None
    if "--since" in args:
        since_arg = args[args.index("--since") + 1]

    token = env_token()
    if not token:
        print(
            "略過回饋摘要：沒有 FEEDBACK_TOKEN。\n"
            "  1) 產生一組：openssl rand -hex 24\n"
            "  2) 存進本機 .env：FEEDBACK_TOKEN=<值>\n"
            "  3) 設進 Cloudflare：npx wrangler pages secret put FEEDBACK_TOKEN --project-name "
            f"{CFG['site']['project']}"
        )
        return 0

    since = parse_since(since_arg)
    data = fetch(since, token)
    if not data:
        return 1

    body, meta = digest(data, video_index())

    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=1))
        return 0

    if not body:
        print(f"沒有新回饋（since={since}）。")
        return 0

    print(body)

    rc = post_issue(body, meta) if do_post else 0
    # 記住這次讀到哪，下次預設只看更新的
    if data.get("latest_ts"):
        STATE.write_text(json.dumps({"latest_ts": data["latest_ts"]}, indent=1) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
