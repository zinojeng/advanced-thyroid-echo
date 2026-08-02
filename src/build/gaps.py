#!/usr/bin/env python3
"""把所有誠實留空的欄位與低證據等級的判定收集起來，產出 KNOWN-GAPS 的資料區塊。

「找不到就留空並寫清楚為什麼」只有在**留空會被看見**時才有意義。
這支腳本把散在 14 個章節檔裡的留空欄位、需註冊／訂閱的來源、
以及被判為 limited / contested / educational_demo_only 的證據，統一列出來。

用法：
    python3 src/build/gaps.py            # 人類可讀
    python3 src/build/gaps.py --json     # 機器可讀
    python3 src/build/gaps.py --md       # markdown 區塊，貼進 KNOWN-GAPS.md
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COURSE = Path(os.environ.get("COURSE") or ROOT / "course").resolve()
DATA = COURSE / "data"

CFG = json.loads((COURSE / "course.config.json").read_text())
TITLES = {c["code"]: c["title"] for c in CFG["chapters"]}
SOFT_GRADES = ("limited", "contested", "expert_consensus", "educational_demo_only")


def load(path: Path):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def chapter_nodes():
    """yield (chapter_code, unit_id, label, node)。"""
    for path in sorted(DATA.glob("ch*.json")):
        blob = load(path)
        if not isinstance(blob, dict):
            continue
        nodes = blob.get("chapters") or [blob]
        for node in nodes:
            code = node.get("chapter") or "?"
            for u in node.get("units") or []:
                uid = u.get("id") or "?"
                if les := u.get("lesson"):
                    yield code, uid, f"核心教材：{u.get('name', '')}", les
                for d in u.get("drills") or []:
                    yield code, uid, d.get("name") or "?", d


def collect() -> dict:
    empty, gated, unlicensed = [], [], []
    providers: Counter = Counter()
    per_chapter_empty: Counter = Counter()

    for code, uid, label, v in chapter_nodes():
        if not v.get("url"):
            empty.append(
                {
                    "chapter": code,
                    "unit": uid,
                    "label": label,
                    "note": (v.get("note") or "").strip() or "⚠️ 沒有寫 note",
                }
            )
            per_chapter_empty[code] += 1
            continue
        providers[v.get("provider") or "?"] += 1
        if (acc := v.get("access")) and acc != "open":
            gated.append(
                {"chapter": code, "unit": uid, "label": label, "access": acc, "url": v["url"]}
            )
        lic = v.get("license") or ""
        if "未確認" in lic or not lic:
            unlicensed.append(
                {
                    "chapter": code,
                    "unit": uid,
                    "label": label,
                    "license": lic or "（未填）",
                    "url": v["url"],
                }
            )

    soft = []
    for pattern, key, idfield in (
        ("drill-evidence-*.json", "categories", "id"),
        ("oe-*.json", "conditions", "unit"),
    ):
        for path in sorted(DATA.glob(pattern)):
            blob = load(path)
            for row in (blob or {}).get(key, []) if isinstance(blob, dict) else []:
                if isinstance(row, dict) and row.get("evidence_grade") in SOFT_GRADES:
                    soft.append(
                        {
                            "id": row.get(idfield),
                            "name": row.get("name"),
                            "grade": row["evidence_grade"],
                            "summary": (row.get("summary") or "")[:200],
                            "citations": len(row.get("citations") or []),
                        }
                    )

    return {
        "empty_slots": empty,
        "empty_by_chapter": dict(per_chapter_empty),
        "gated_sources": gated,
        "unclear_license": unlicensed,
        "soft_evidence": soft,
        "providers": dict(providers),
    }


def as_markdown(g: dict) -> str:
    out = []
    grouped = defaultdict(list)
    for e in g["empty_slots"]:
        grouped[e["chapter"]].append(e)

    out.append("### 找不到合格資源而誠實留空的欄位\n")
    if not grouped:
        out.append("目前沒有留空的欄位。\n")
    else:
        out.append(f"共 {len(g['empty_slots'])} 個欄位。\n")
        out.append("| 章節 | 單元 | 欄位 | 查過什麼、為什麼不合格 |")
        out.append("|---|---|---|---|")
        for code in sorted(grouped, key=lambda c: (len(c), c)):
            for e in grouped[code]:
                note = e["note"].replace("|", "／").replace("\n", " ")
                out.append(
                    f"| {code} {TITLES.get(code, '')} | `{e['unit']}` | {e['label']} | {note} |"
                )
        out.append("")

    out.append("### 需要註冊、訂閱或機構帳號才能完整取用的來源\n")
    if not g["gated_sources"]:
        out.append("目前全部來源皆為公開取用。\n")
    else:
        labels = {
            "registration": "需免費註冊",
            "subscription": "需訂閱",
            "institutional": "需機構帳號",
        }
        out.append(f"共 {len(g['gated_sources'])} 個。網站上會以標籤標示，點進去前就看得到。\n")
        out.append("| 章節 | 單元 | 資源 | 存取條件 |")
        out.append("|---|---|---|---|")
        for s in g["gated_sources"]:
            out.append(
                f"| {s['chapter']} | `{s['unit']}` | {s['label']} | "
                f"{labels.get(s['access'], s['access'])} |"
            )
        out.append("")

    out.append("### 授權狀況未能確認的來源\n")
    if not g["unclear_license"]:
        out.append("目前所有來源的授權狀況都已標示。\n")
    else:
        out.append(
            f"共 {len(g['unclear_license'])} 個。這些連結本身是安全的（本站只連結、"
            "不重製），但若要引用其內容或截圖，必須先取得授權。\n"
        )
        out.append("| 章節 | 單元 | 資源 |")
        out.append("|---|---|---|")
        for s in g["unclear_license"]:
            out.append(f"| {s['chapter']} | `{s['unit']}` | {s['label']} |")
        out.append("")

    out.append("### 證據不足或互斥的主題\n")
    if not g["soft_evidence"]:
        out.append("尚未產出實證資料。\n")
    else:
        names = {gr["id"]: gr["label"] for gr in CFG.get("grades", [])}
        counts = Counter(s["grade"] for s in g["soft_evidence"])
        out.append(
            "共 " + "、".join(f"{names.get(k, k)} {v} 條" for k, v in counts.most_common()) + "。\n"
        )
        out.append("| 主題 | 判定 | 引用數 | 摘要 |")
        out.append("|---|---|---:|---|")
        for s in sorted(g["soft_evidence"], key=lambda x: x["grade"]):
            summary = (s["summary"] or "").replace("|", "／").replace("\n", " ")
            out.append(
                f"| {s['name'] or s['id']} | {names.get(s['grade'], s['grade'])} | "
                f"{s['citations']} | {summary} |"
            )
        out.append("")

    return "\n".join(out)


def main() -> int:
    g = collect()
    if "--json" in sys.argv:
        print(json.dumps(g, ensure_ascii=False, indent=1))
        return 0
    if "--md" in sys.argv:
        print(as_markdown(g))
        return 0

    print(
        f"留空欄位 {len(g['empty_slots'])} 個"
        f"（{'、'.join(f'{k} {v}' for k, v in sorted(g['empty_by_chapter'].items())) or '無'}）"
    )
    print(f"需註冊／訂閱／機構帳號 {len(g['gated_sources'])} 個")
    print(f"授權未確認 {len(g['unclear_license'])} 個")
    print(f"證據不足或互斥 {len(g['soft_evidence'])} 條")
    print("來源分布：" + " / ".join(f"{k} {v}" for k, v in sorted(g["providers"].items())))
    missing_note = [e for e in g["empty_slots"] if "沒有寫 note" in e["note"]]
    if missing_note:
        print(f"\n✗ {len(missing_note)} 個留空欄位沒有寫 note（make audit 會擋）")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
