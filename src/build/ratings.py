#!/usr/bin/env python3
"""把使用者評價變成**換片工作清單**。

評價的目的不是給影片打人氣，是找出該換掉的片子。所以這支腳本回答的是
「哪一支要換、換的理由是什麼、它掛在哪個單元」，不是「平均幾分」。

低分而**沒有原因標籤**的不列入必換清單——只知道有人不喜歡，
不知道哪裡不合格，換片時等於重猜一次。這種只列在「待觀察」。

用法：
    make ratings                    # 讀線上 API，印出換片清單
    python3 src/build/ratings.py --json
    python3 src/build/ratings.py --url https://thyroid-us.pages.dev
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COURSE = Path(os.environ.get("COURSE") or ROOT / "course").resolve()
DATA = COURSE / "data"
CFG = json.loads((COURSE / "course.config.json").read_text())

RATINGS_CFG = CFG.get("ratings") or {}
LOW = RATINGS_CFG.get("lowThreshold", 2)
REASON_LABEL = {r["id"]: r["label"] for r in RATINGS_CFG.get("reasons", [])}
# 幾票以上才算數。一個人給一分就換片，等於把策展決定權交給單一使用者
MIN_VOTES = int(os.environ.get("MIN_VOTES", "3"))


def video_id(url: str | None) -> str | None:
    import re

    m = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", url or "")
    return m.group(1) if m else None


def course_index() -> dict[str, list[dict]]:
    """video id -> 掛在哪些單元的哪些欄位。一支片可能被多個單元共用。"""
    idx: dict[str, list[dict]] = {}
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
                    vid = video_id(v["url"])
                    if not vid:
                        continue
                    idx.setdefault(vid, []).append(
                        {
                            "chapter": code,
                            "unit": u.get("id"),
                            "role": role,
                            "name": v.get("name") or v.get("title"),
                            "title": v.get("title"),
                            "url": v["url"],
                        }
                    )
    return idx


def fetch(base: str) -> list[dict]:
    req = urllib.request.Request(
        f"{base.rstrip('/')}/api/rate", headers={"User-Agent": "thyroid-course/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return json.loads(res.read()).get("videos", [])
    except urllib.error.HTTPError as e:
        if e.code == 503:
            print("後端沒有綁 D1（或還沒部署），沒有評價可讀。跑 make counter 建資料庫。", file=sys.stderr)
            return []
        raise


def main() -> int:
    as_json = "--json" in sys.argv
    base = CFG["site"]["url"]
    if "--url" in sys.argv:
        base = sys.argv[sys.argv.index("--url") + 1]

    videos = fetch(base)
    idx = course_index()

    replace, watch = [], []
    for v in videos:
        n, avg = v.get("n", 0), v.get("avg")
        if avg is None or n < MIN_VOTES or avg > LOW:
            continue
        row = {
            "video": v["video"],
            "avg": avg,
            "n": n,
            "reasons": [
                {"id": r["reason"], "label": REASON_LABEL.get(r["reason"], r["reason"]), "n": r["n"]}
                for r in v.get("reasons", [])
            ],
            "slots": idx.get(v["video"], []),
        }
        (replace if row["reasons"] else watch).append(row)

    if as_json:
        print(json.dumps({"replace": replace, "watch": watch}, ensure_ascii=False, indent=1))
        return 0

    print(f"評價來源：{base}/api/rate · 門檻：平均 ≤ {LOW} 且至少 {MIN_VOTES} 票\n")

    if not videos:
        print("目前沒有任何評價。")
        return 0

    if replace:
        print(f"■ 建議換片 {len(replace)} 支（低分且有具體原因）\n")
        for r in replace:
            print(f"  {r['avg']}／5（{r['n']} 票）  https://www.youtube.com/watch?v={r['video']}")
            for s in r["slots"]:
                print(f"      掛在 {s['chapter']} {s['unit']} · {s['role']}：{s['name']}")
            if not r["slots"]:
                print("      ⚠ 這支已經不在課程裡（可能已被換掉）")
            for rs in r["reasons"]:
                print(f"      → {rs['label']}（{rs['n']} 人）")
            print()
    else:
        print("■ 沒有需要換片的影片。\n")

    if watch:
        print(f"□ 待觀察 {len(watch)} 支（分數低但沒人說明原因，不足以決定換成什麼）\n")
        for r in watch:
            slot = r["slots"][0] if r["slots"] else None
            where = f"{slot['chapter']} {slot['unit']}" if slot else "（已不在課程裡）"
            print(f"  {r['avg']}／5（{r['n']} 票）{where} https://youtu.be/{r['video']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
