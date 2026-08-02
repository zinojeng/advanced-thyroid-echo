#!/usr/bin/env python3
"""把 CH12 擴充 workflow 的產出合併進 ch12.json。

平行 agent 各寫各的檔（`course/data/_ch12-*.json`），避免互相覆蓋；
合併這件事由單一流程做，才控制得住順序與去重。

用法：
    python3 src/build/merge_ch12.py --dry-run
    python3 src/build/merge_ch12.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(os.environ.get("COURSE") or ROOT / "course").resolve() / "data"
TARGET = DATA / "ch12.json"

NEW_UNIT_ORDER = ["ch12-u6", "ch12-u7", "ch12-u8", "ch12-u9", "ch12-u10"]


def load(p: Path):
    try:
        return json.loads(p.read_text())
    except (OSError, json.JSONDecodeError) as e:
        print(f"  ✗ {p.name}：{e}", file=sys.stderr)
        return None


def existing_urls(blob: dict) -> set[str]:
    out = set()
    for u in blob.get("units", []):
        for v in [u.get("lesson"), *(u.get("drills") or [])]:
            if v and v.get("url"):
                out.add(v["url"])
    return out


def course_urls() -> set[str]:
    """全課已用的 URL，用來擋跨章重複。"""
    out = set()
    for p in sorted(DATA.glob("ch*.json")):
        blob = load(p)
        if blob:
            out |= existing_urls(blob)
    return out


def main() -> int:
    dry = "--dry-run" in sys.argv
    ch12 = load(TARGET)
    if not ch12:
        return 1

    before_units = len(ch12["units"])
    before_drills = sum(len(u.get("drills") or []) for u in ch12["units"])

    used = course_urls()
    added_units, added_drills, skipped = [], 0, []

    # 1) 既有單元補資源
    topup = load(DATA / "_ch12-topup.json")
    if topup:
        by_id = {u["id"]: u for u in ch12["units"]}
        for add in topup.get("additions", []):
            uid, drill = add.get("unit"), add.get("drill")
            if not uid or not drill or uid not in by_id:
                skipped.append(f"topup 指向不存在的單元 {uid}")
                continue
            url = drill.get("url")
            if url and url in used:
                skipped.append(f"{uid} 補的資源與課程既有影片重複：{url}")
                continue
            by_id[uid].setdefault("drills", []).append(drill)
            if url:
                used.add(url)
            added_drills += 1

    # 2) 新單元，照固定順序接在後面
    for uid in NEW_UNIT_ORDER:
        blob = load(DATA / f"_{uid}.json")
        if not blob:
            skipped.append(f"找不到 _{uid}.json")
            continue
        if any(u["id"] == uid for u in ch12["units"]):
            skipped.append(f"{uid} 已存在，跳過")
            continue

        # 單元內部去重 + 跨章去重
        kept = []
        for d in blob.get("drills") or []:
            url = d.get("url")
            if url and url in used:
                skipped.append(f"{uid} 的資源重複，已移除：{url}")
                continue
            if url:
                used.add(url)
            kept.append(d)
        blob["drills"] = kept

        les = blob.get("lesson") or {}
        if les.get("url") and les["url"] in used:
            skipped.append(f"{uid} 的核心教材與既有影片重複：{les['url']}")
        elif les.get("url"):
            used.add(les["url"])

        ch12["units"].append(blob)
        added_units.append(uid)
        added_drills += len(kept)

    after_units = len(ch12["units"])
    after_drills = sum(len(u.get("drills") or []) for u in ch12["units"])

    print(f"單元 {before_units} → {after_units}（新增 {', '.join(added_units) or '無'}）")
    print(f"資源 {before_drills} → {after_drills}（新增 {added_drills}）")
    if skipped:
        print(f"\n⚠ 跳過 {len(skipped)} 項：")
        for s in skipped:
            print(f"   · {s}")

    if dry:
        print("\n（--dry-run，沒有寫入）")
        return 0

    TARGET.write_text(json.dumps(ch12, ensure_ascii=False, indent=1) + "\n")
    print(f"\n→ {TARGET.relative_to(ROOT)}")
    print(f"記得把 course.config.json 的 CH12 配額改成 units={after_units}, drills={after_drills}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
