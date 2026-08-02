"""甲狀腺與頸部超音波的詞彙模組：把散落在文字裡的術語正規化成可篩選的標籤。

體態課的分面是肌群，這門課的分面是**影像特徵、疾病、解剖分區、風險分層系統與處置**。
重點跟原框架一樣是正規化同義詞：`taller-than-wide`、`縱橫比 > 1`、「高大於寬」
指的是同一件事，不該變成三個標籤。

`extract()` 的輸入是策展資料裡的自由文字（單元的判讀能力與陷阱、資源的教學重點），
所以 pattern 只能用**特徵與疾病名稱**，不能用「甲狀腺」「超音波」這種到處都是的字。
"""

from __future__ import annotations

import re

GROUPS = ["影像特徵", "疾病", "解剖與分區", "風險分層", "處置與介入", "技術"]

# 標籤 -> (分組, 比對用的 pattern)。pattern 一律小寫比對，中英文都收。
TERMS: dict[str, tuple[str, str]] = {
    # ── 影像特徵（結節描述語言）────────────────────────────────────────
    "囊實比例": ("影像特徵", r"composition|囊實|cystic component|solid component|實質成分"),
    "海綿樣": ("影像特徵", r"spongiform|海綿樣|海綿狀"),
    "低回音": ("影像特徵", r"hypoechoic|低回音|低迴音"),
    "極低回音": ("影像特徵", r"markedly hypoechoic|very hypoechoic|極低回音"),
    "等回音／高回音": ("影像特徵", r"isoechoic|hyperechoic|等回音|高回音"),
    "縱橫比大於一": ("影像特徵", r"taller[- ]than[- ]wide|縱橫比|高大於寬|a/?t ratio|非平行位向"),
    "邊緣不規則": ("影像特徵", r"irregular margin|spiculated|lobulated|微分葉|邊緣不規則|毛刺"),
    "邊緣光滑": ("影像特徵", r"smooth margin|well[- ]defined margin|邊緣光滑|邊界清楚"),
    "微鈣化": ("影像特徵", r"microcalcification|punctate echogenic foci|微鈣化|點狀強回音"),
    "巨鈣化": ("影像特徵", r"macrocalcification|粗鈣化|巨鈣化|coarse calcification"),
    "邊緣鈣化": (
        "影像特徵",
        r"rim calcification|eggshell|peripheral calcification|蛋殼樣|邊緣鈣化",
    ),
    "彗星尾偽影": ("影像特徵", r"comet[- ]tail|彗星尾|reverberation artifact"),
    "暈環": ("影像特徵", r"\bhalo\b|暈環|halo sign"),
    "甲狀腺外侵犯": (
        "影像特徵",
        r"extrathyroidal extension|\bete\b|甲狀腺外侵犯|capsular contact|包膜接觸",
    ),
    "血流分布": ("影像特徵", r"vascularity|color doppler|power doppler|血流|都卜勒"),
    "假性結節": ("影像特徵", r"pseudonodule|pseudolesion|假性結節|假性病灶"),
    "偽影": ("影像特徵", r"\bartifact\b|artefact|偽影|shadowing|聲影|posterior enhancement"),
    # ── 疾病 ──────────────────────────────────────────────────────────
    "Graves 病": ("疾病", r"graves|葛瑞夫茲|突眼性甲狀腺腫|thyroid inferno"),
    "橋本甲狀腺炎": ("疾病", r"hashimoto|橋本|chronic lymphocytic thyroiditis|慢性淋巴球性"),
    "亞急性甲狀腺炎": ("疾病", r"subacute thyroiditis|de quervain|亞急性甲狀腺炎"),
    "無痛性甲狀腺炎": (
        "疾病",
        r"painless thyroiditis|silent thyroiditis|無痛性甲狀腺炎|產後甲狀腺炎|postpartum thyroiditis",
    ),
    "急性化膿性甲狀腺炎": (
        "疾病",
        r"suppurative thyroiditis|化膿性甲狀腺炎|thyroid abscess|甲狀腺膿瘍",
    ),
    "Riedel 甲狀腺炎": ("疾病", r"riedel"),
    "IgG4 相關疾病": ("疾病", r"igg4"),
    "藥物相關甲狀腺病變": (
        "疾病",
        r"amiodarone|checkpoint inhibitor|immune[- ]related thyroiditis|藥物相關甲狀腺",
    ),
    "乳突癌": ("疾病", r"papillary thyroid|\bptc\b|乳突癌|乳頭狀癌"),
    "濾泡癌": (
        "疾病",
        r"follicular thyroid carcinoma|\bftc\b|濾泡癌|follicular neoplasm|濾泡性腫瘤",
    ),
    "髓質癌": ("疾病", r"medullary thyroid|\bmtc\b|髓質癌"),
    "未分化癌": ("疾病", r"anaplastic|未分化癌"),
    "低分化癌": ("疾病", r"poorly differentiated|低分化"),
    "甲狀腺淋巴瘤": ("疾病", r"thyroid lymphoma|甲狀腺淋巴瘤"),
    "甲狀腺轉移癌": (
        "疾病",
        r"metastas[ei]s to the thyroid|metastatic tumor to thyroid|甲狀腺轉移",
    ),
    "瀰漫硬化型": ("疾病", r"diffuse sclerosing|瀰漫硬化"),
    "多結節性甲狀腺腫": ("疾病", r"multinodular goiter|\bmng\b|多結節|甲狀腺腫大"),
    "副甲狀腺腺瘤": (
        "疾病",
        r"parathyroid adenoma|副甲狀腺腺瘤|parathyroid hyperplasia|副甲狀腺增生",
    ),
    "甲狀舌管囊腫": ("疾病", r"thyroglossal|甲狀舌管"),
    "鰓裂囊腫": ("疾病", r"branchial cleft|鰓裂"),
    "神經鞘瘤": ("疾病", r"schwannoma|神經鞘瘤"),
    "食道憩室": ("疾病", r"esophageal diverticulum|zenker|食道憩室"),
    # ── 解剖與分區 ────────────────────────────────────────────────────
    "峽部與錐狀葉": ("解剖與分區", r"isthmus|pyramidal lobe|峽部|錐狀葉"),
    "Zuckerkandl 結節": ("解剖與分區", r"zuckerkandl"),
    "異位甲狀腺": ("解剖與分區", r"ectopic thyroid|lingual thyroid|異位甲狀腺"),
    "帶狀肌與頸長肌": (
        "解剖與分區",
        r"strap muscle|longus colli|帶狀肌|頸長肌|sternocleidomastoid|胸鎖乳突肌",
    ),
    "喉返神經": ("解剖與分區", r"recurrent laryngeal|喉返神經|\brln\b"),
    "中央區": ("解剖與分區", r"central compartment|level vi|level 6|中央區|中央淋巴"),
    "側頸分區": (
        "解剖與分區",
        r"lateral neck|level ii|level iii|level iv|level v|側頸|頸部分區|neck level",
    ),
    "氣管與食道": ("解剖與分區", r"trachea|esophagus|氣管|食道(?!憩室)"),
    "頸動脈與頸靜脈": ("解剖與分區", r"carotid|jugular|頸動脈|頸靜脈"),
    "胸骨後延伸": ("解剖與分區", r"substernal|retrosternal|胸骨後|胸骨下"),
    "甲狀腺床": ("解剖與分區", r"thyroid bed|甲狀腺床|殘餘組織|thyroid remnant"),
    # ── 風險分層 ──────────────────────────────────────────────────────
    "ACR TI-RADS": ("風險分層", r"acr ti[- ]?rads|美國放射學會.*ti[- ]?rads"),
    "ATA 分層": ("風險分層", r"\bata\b|american thyroid association|sonographic pattern"),
    "EU-TIRADS": ("風險分層", r"eu[- ]?tirads|european thyroid association|\beta\b guideline"),
    "K-TIRADS": ("風險分層", r"k[- ]?tirads|korean society of thyroid radiology|\bksthr\b"),
    "Bethesda 分類": ("風險分層", r"bethesda"),
    "系統間不一致": ("風險分層", r"discordan|不一致|系統間差異|inter[- ]?system"),
    "穿刺門檻": ("風險分層", r"fna threshold|size threshold|穿刺門檻|biopsy threshold"),
    "追蹤門檻": ("風險分層", r"follow[- ]?up threshold|surveillance interval|追蹤門檻|追蹤間隔"),
    # ── 處置與介入 ────────────────────────────────────────────────────
    "細針穿刺": ("處置與介入", r"\bfna\b|fine[- ]needle aspiration|細針"),
    "粗針切片": ("處置與介入", r"core needle biopsy|\bcnb\b|粗針"),
    "沖洗液檢驗": ("處置與介入", r"washout|沖洗液|thyroglobulin washout|pth washout"),
    "熱消融": (
        "處置與介入",
        r"radiofrequency ablation|\brfa\b|microwave ablation|laser ablation|熱消融|射頻",
    ),
    "酒精注射": ("處置與介入", r"ethanol ablation|\bpei\b|酒精注射|酒精消融"),
    "主動監測": ("處置與介入", r"active surveillance|主動監測|積極監測"),
    "檢體適足性": (
        "處置與介入",
        r"specimen adequacy|nondiagnostic|檢體適足|\brose\b|rapid on[- ]site",
    ),
    "併發症處理": ("處置與介入", r"complication|hematoma|血腫|併發症"),
    # ── 技術 ──────────────────────────────────────────────────────────
    "彈性造影": ("技術", r"elastograph|strain elastography|shear[- ]wave|彈性造影|彈性成像"),
    "顯影劑超音波": ("技術", r"contrast[- ]enhanced ultrasound|\bceus\b|顯影劑超音波"),
    "微血流成像": ("技術", r"microvascular flow|superb microvascular|\bsmi\b|微血流"),
    "機器參數最佳化": (
        "技術",
        r"gain|dynamic range|\bfocus\b|frequency|\bprf\b|wall filter|參數|機器設定|preset",
    ),
    "複合與諧波成像": ("技術", r"compound imaging|harmonic imaging|複合成像|諧波"),
    "人工智慧": (
        "技術",
        r"artificial intelligence|deep learning|machine learning|人工智慧|深度學習|radiomics|影像組學",
    ),
    "三維與融合影像": ("技術", r"3d ultrasound|fusion imaging|三維超音波|融合影像"),
    "結構化報告": ("技術", r"structured report|reporting template|結構化報告|報告模板"),
    "判讀者間一致性": ("技術", r"interobserver|inter[- ]reader|一致性|kappa"),
}

GROUP_OF = {name: grp for name, (grp, _) in TERMS.items()}
_COMPILED = [(name, re.compile(pat, re.I)) for name, (_, pat) in TERMS.items()]


def extract(*texts: str | None) -> list[str]:
    """從任意數量的自由文字中抽出出現過的術語標籤（去重、保持定義順序）。"""
    blob = " ".join(t for t in texts if t)
    if not blob.strip():
        return []
    return [name for name, rx in _COMPILED if rx.search(blob)]
