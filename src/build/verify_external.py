#!/usr/bin/env python3
"""驗證非 YouTube 來源的連結是否真的存在（YouTube 的部分交給 verify_links.py）。

醫學教育資源多半在學會、期刊、醫院教學站與病例圖譜，沒有 oEmbed 可查。
這裡實際發出請求，記錄：HTTP 狀態、重導向鏈、最終網址、網域、content-type、
頁面標題、是否疑似需要登入。**不信任策展 agent 說「我查過了」**。

用法：
    python3 verify_external.py               # 驗證並列出問題
    python3 verify_external.py --json        # 機器可讀報告
    python3 verify_external.py --stamp       # 把通過的連結 last_verified 更新為今天（改 course/data/）
"""

from __future__ import annotations

import datetime
import gzip
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sources as SRC  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
COURSE = Path(os.environ.get("COURSE") or ROOT / "course").resolve()
DATA = COURSE / "data"
DIST = Path(os.environ.get("DIST") or ROOT / "dist").resolve()
COURSE_JSON = DIST / "course.json"
REPORT = DATA / "external-verify.json"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0 Safari/537.36"
)
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
CANON = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', re.I)
LOGIN_HINTS = re.compile(
    r"sign in to continue|please log ?in|subscription required|purchase access|"
    r"institutional login|member login|create an account to", re.I
)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """自己跟重導向，才記得住整條鏈。"""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D102
        return None


def fetch(url: str, hops: int = 0) -> dict:
    out = {"url": url, "ok": False, "status": None, "redirects": [], "final_url": url}
    opener = urllib.request.build_opener(NoRedirect)
    seen = []
    cur = url
    for _ in range(6):
        req = urllib.request.Request(
            cur,
            headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml,application/pdf,*/*",
                "Accept-Language": "en,zh-TW;q=0.8",
                "Accept-Encoding": "gzip",
            },
        )
        try:
            res = opener.open(req, timeout=25)
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308) and e.headers.get("Location"):
                nxt = urllib.parse.urljoin(cur, e.headers["Location"])
                seen.append(nxt)
                cur = nxt
                continue
            out["status"] = e.code
            out["note"] = {403: "被擋（可能是 bot 防護，需人工確認）",
                           404: "頁面不存在",
                           410: "已移除"}.get(e.code, f"HTTP {e.code}")
            # 403 常常只是 WAF 擋 bot，網頁對真人是活的——標為待人工確認而非死連結
            out["manual"] = e.code in (403, 429)
            out["redirects"] = seen
            out["final_url"] = cur
            return out
        except Exception as e:
            out["note"] = f"連線失敗：{type(e).__name__}"
            out["redirects"] = seen
            return out

        body = res.read(400_000)
        if res.headers.get("Content-Encoding") == "gzip":
            try:
                body = gzip.decompress(body)
            except OSError:
                pass
        text = body.decode("utf-8", "replace")
        out.update(
            ok=True,
            status=res.status,
            redirects=seen,
            final_url=res.geturl(),
            domain=urllib.parse.urlparse(res.geturl()).netloc,
            content_type=(res.headers.get("Content-Type") or "").split(";")[0].strip(),
        )
        if m := TITLE.search(text):
            out["title"] = html.unescape(re.sub(r"\s+", " ", m.group(1))).strip()[:160]
        if m := CANON.search(text):
            out["canonical"] = html.unescape(m.group(1))
        out["login_wall"] = bool(LOGIN_HINTS.search(text))
        return out
    out["note"] = "重導向次數過多"
    out["redirects"] = seen
    return out


def walk(course: dict):
    for ch in course["chapters"]:
        for u in ch["units"]:
            for les in u.get("lessons") or ([u["lesson"]] if u.get("lesson") else []):
                yield ch["code"], u["id"], "主課", les
            for d in u.get("drills") or []:
                yield ch["code"], u["id"], d.get("name", "?"), d


def stamp(passed: set[str]) -> int:
    """把驗證通過的連結在 course/data/*.json 裡的 last_verified 更新為今天。"""
    today = datetime.date.today().isoformat()
    touched = 0
    for path in sorted(DATA.glob("*.json")):
        if path.name in ("video-meta.json", "external-verify.json"):
            continue
        try:
            blob = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        changed = [0]

        def walk_node(node):
            if isinstance(node, dict):
                if node.get("url") in passed and node.get("last_verified") != today:
                    node["last_verified"] = today
                    changed[0] += 1
                for v in node.values():
                    walk_node(v)
            elif isinstance(node, list):
                for v in node:
                    walk_node(v)

        walk_node(blob)
        if changed[0]:
            path.write_text(json.dumps(blob, ensure_ascii=False, indent=1) + "\n")
            touched += changed[0]
    return touched


def main() -> int:
    as_json = "--json" in sys.argv
    do_stamp = "--stamp" in sys.argv

    if not COURSE_JSON.exists():
        print("找不到 dist/course.json，先跑 make build", file=sys.stderr)
        return 1
    course = json.loads(COURSE_JSON.read_text())

    nodes = [(c, u, lbl, v) for c, u, lbl, v in walk(course) if v.get("url")]
    urls = sorted({v["url"] for *_, v in nodes if not SRC.is_youtube(v)})
    if not urls:
        print("沒有非 YouTube 來源，不用驗。")
        return 0

    if not as_json:
        print(f"檢查 {len(urls)} 個外部連結…\n")

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = {r["url"]: r for r in pool.map(fetch, urls)}

    dead = {u: r for u, r in results.items() if not r["ok"] and not r.get("manual")}
    manual = {u: r for u, r in results.items() if r.get("manual")}
    walled = {u: r for u, r in results.items() if r.get("ok") and r.get("login_wall")}
    passed = {u for u, r in results.items() if r["ok"]}

    REPORT.write_text(
        json.dumps(
            {"checked": datetime.date.today().isoformat(), "results": results},
            ensure_ascii=False,
            indent=1,
        )
        + "\n"
    )

    if as_json:
        print(json.dumps(
            {"ok": not dead, "total": len(urls), "dead": list(dead), "manual": list(manual),
             "login_wall": list(walled)}, ensure_ascii=False, indent=1))
        return 1 if dead else 0

    for label, group, mark in (
        ("失效", dead, "✗"),
        ("被 bot 防護擋下，需人工開一次確認", manual, "⚠"),
        ("疑似需要登入或訂閱（課程頁面必須標示 access）", walled, "⚠"),
    ):
        if not group:
            continue
        print(f"{mark} {len(group)} 個連結{label}：")
        for code, uid, lbl, v in nodes:
            if v["url"] in group:
                r = group[v["url"]]
                print(f"   {code} {uid} · {lbl}")
                print(f"      {v['url']} — {r.get('note') or r.get('title') or ''}")
        print()

    ok = len(passed)
    print(f"通過 {ok} / {len(urls)}（{ok / len(urls) * 100:.1f}%）· 報告寫入 {REPORT.relative_to(ROOT)}")

    if do_stamp:
        n = stamp(passed)
        print(f"→ 已更新 {n} 個欄位的 last_verified 為今天")

    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
