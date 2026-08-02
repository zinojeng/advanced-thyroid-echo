"""把資源歸類，讓文獻可以掛在「類別」而不是「單支影片」上。

單一病例影片沒有自己的 RCT，「ACR TI-RADS 的診斷準確度」才有。
`classify()` 決定一個資源屬於哪一類，`drill-evidence-*.json` 再為每一類附上
PubMed 查證過的文獻與證據等級。

踩過的坑（沿用原框架的教訓）：pattern 只能用**做法／系統名稱**，不能用會出現在
`target`（教學重點）裡的通用字，否則所有提到該字的資源都會掉進同一類。
"""

from __future__ import annotations

import re

NAMES = {
    "acr-tirads": "ACR TI-RADS 分層",
    "ata-pattern": "ATA sonographic pattern",
    "eu-tirads": "EU-TIRADS 分層",
    "k-tirads": "K-TIRADS 分層",
    "system-discordance": "風險分層系統間的不一致",
    "us-lexicon": "標準化描述語言與判讀者間一致性",
    "scan-optimization": "機器參數與掃描最佳化",
    "diffuse-thyroid": "瀰漫性甲狀腺疾病的超音波判讀",
    "nodule-vascularity": "血流分布在結節分層中的角色",
    "fna-technique": "細針穿刺技術與檢體適足性",
    "core-biopsy": "粗針切片",
    "washout": "沖洗液 thyroglobulin／PTH 檢驗",
    "ln-assessment": "頸部淋巴結評估與術前 mapping",
    "postop-surveillance": "術後甲狀腺床與復發追蹤",
    "active-surveillance": "低危險乳突微小癌的主動監測",
    "thermal-ablation": "熱消融與酒精消融後的影像追蹤",
    "parathyroid-localization": "副甲狀腺病灶定位",
    "elastography": "彈性造影",
    "ceus": "顯影劑超音波",
    "ai-tirads": "AI 與自動化風險分層",
    "pediatric-pregnancy": "兒童與孕期的甲狀腺結節",
    "incidentaloma": "其他影像意外發現的甲狀腺病灶",
    "structured-reporting": "結構化報告與品質稽核",
}

KINDS = ("case", "procedure", "atlas", "guideline", "lecture")

# 順序有意義：先比對專一性高的，避免「TI-RADS 比較」被歸進單一系統
PATTERNS: list[tuple[str, str]] = [
    ("system-discordance", r"discordan|系統間|不一致|比較器|cross[- ]system|四大系統|系統比較"),
    ("acr-tirads", r"acr ti[- ]?rads|acr白皮書|acr white paper"),
    ("eu-tirads", r"eu[- ]?tirads|european thyroid association"),
    ("k-tirads", r"k[- ]?tirads|korean society of thyroid radiology"),
    ("ata-pattern", r"ata (?:guideline|pattern|sonographic)|american thyroid association"),
    ("us-lexicon", r"lexicon|標準化描述|structured description|interobserver|判讀者間"),
    ("scan-optimization", r"機器參數|preset|gain|dynamic range|\bprf\b|wall filter|掃描技巧|probe|探頭|optimi[sz]ation"),
    ("diffuse-thyroid", r"thyroiditis|甲狀腺炎|graves|橋本|hashimoto|瀰漫性"),
    ("nodule-vascularity", r"vascularity|血流|doppler|都卜勒"),
    ("core-biopsy", r"core needle|\bcnb\b|粗針"),
    ("washout", r"washout|沖洗液"),
    ("fna-technique", r"\bfna\b|fine[- ]needle|細針|穿刺技術|needle visuali|檢體適足|nondiagnostic|\brose\b"),
    ("ln-assessment", r"lymph node|淋巴結|neck mapping|頸部分區|level vi|側頸"),
    ("active-surveillance", r"active surveillance|主動監測|積極監測|microcarcinoma|微小癌"),
    ("thermal-ablation", r"ablation|消融|射頻|\brfa\b|ethanol|酒精"),
    ("postop-surveillance", r"postoperative|術後|thyroid bed|甲狀腺床|recurrence|復發|remnant"),
    ("parathyroid-localization", r"parathyroid|副甲狀腺"),
    ("elastography", r"elastograph|彈性造影|shear[- ]wave"),
    ("ceus", r"contrast[- ]enhanced|\bceus\b|顯影劑"),
    ("ai-tirads", r"artificial intelligence|deep learning|machine learning|人工智慧|深度學習|radiomics|自動化"),
    ("pediatric-pregnancy", r"p(a?)ediatric|兒童|pregnan|孕期|懷孕"),
    ("incidentaloma", r"incidental|意外發現|\bpet\b|\bct\b 意外"),
    ("structured-reporting", r"structured report|結構化報告|audit|稽核|品質保證|logbook|credential"),
]

_COMPILED = [(cid, re.compile(pat, re.I)) for cid, pat in PATTERNS]


def classify(item: dict) -> str | None:
    """依資源的名稱、英文名與教學重點歸類。歸不出來回 None（由 build 印出來人工看）。"""
    blob = " ".join(
        str(item.get(f) or "")
        for f in ("name", "en", "target", "title", "cat_hint")
    )
    if not blob.strip():
        return None
    for cid, rx in _COMPILED:
        if rx.search(blob):
            return cid
    return None
