#!/usr/bin/env python3
"""把各章策展 agent 的搜尋紀錄合併成 SOURCE-REGISTRY.json。

每個 agent 只寫自己的 `course/data/registry-chN.json`（避免互相覆蓋），
這裡合併成一份可查證的總表：所有評估過的來源、納入或排除、以及理由。

用法：
    python3 src/build/merge_registry.py
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COURSE = Path(os.environ.get("COURSE") or ROOT / "course").resolve()
DATA = COURSE / "data"
OUT = ROOT / "SOURCE-REGISTRY.json"


def main() -> int:
    chapters, evaluated, queries = [], [], []
    seen_urls: set[str] = set()
    decisions: Counter = Counter()
    dupes = 0

    for path in sorted(DATA.glob("registry-ch*.json")):
        try:
            blob = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            print(f"  ✗ {path.name} JSON 解析失敗：{e}", file=sys.stderr)
            return 1
        code = blob.get("chapter") or path.stem.replace("registry-", "").upper()
        rows = blob.get("evaluated") or []
        chapters.append({"chapter": code, "evaluated": len(rows), "file": path.name})
        for q in blob.get("searched") or []:
            queries.append({"chapter": code, "query": q})
        for row in rows:
            if not isinstance(row, dict):
                continue
            row.setdefault("chapter", code)
            url = row.get("url")
            # 同一份資源可能被多章評估過，保留每一筆但標出來
            if url and url in seen_urls:
                row["also_evaluated_elsewhere"] = True
                dupes += 1
            if url:
                seen_urls.add(url)
            decisions[row.get("decision") or "unspecified"] += 1
            evaluated.append(row)

    if not chapters:
        print("找不到任何 registry-ch*.json", file=sys.stderr)
        return 1

    OUT.write_text(
        json.dumps(
            {
                "generated_from": [c["file"] for c in chapters],
                "summary": {
                    "chapters": len(chapters),
                    "queries": len(queries),
                    "evaluated": len(evaluated),
                    "unique_urls": len(seen_urls),
                    "evaluated_in_more_than_one_chapter": dupes,
                    "decisions": dict(decisions),
                },
                "per_chapter": chapters,
                "queries": queries,
                "evaluated": evaluated,
            },
            ensure_ascii=False,
            indent=1,
        )
        + "\n"
    )

    print(f"→ {OUT.relative_to(ROOT)}")
    print(f"   {len(chapters)} 章 · 查詢 {len(queries)} 筆 · 評估 {len(evaluated)} 個來源")
    print("   " + " / ".join(f"{k} {v}" for k, v in sorted(decisions.items())))
    if not decisions.get("excluded"):
        print("   ⚠ 沒有任何排除紀錄——策展過程若真的來者不拒，品質門檻等於沒有")
    return 0


if __name__ == "__main__":
    sys.exit(main())
