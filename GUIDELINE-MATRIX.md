# 甲狀腺結節超音波風險分層系統對照矩陣

> **課程用途**：進階甲狀腺及頸部超音波
> **查證日期**：2026-08-02
> **查證原則**：本文件內每一個門檻、百分比、PMID、DOI、期刊名與年份，均取自實際擷取的原文或
> PubMed E-utilities esummary 回傳值。凡無法由可取得的原文核對者，一律標示
> `⚠️ 未能由原文查證，需人工確認`，不以記憶補寫。
> 引用格式：`[PMID]`。完整書目見文末「引用文獻」與 `course/data/guideline-refs.json`。

---

## 一頁式對照表

| 項目 | **ACR TI-RADS** | **ATA sonographic pattern** | **EU-TIRADS** | **K-TIRADS** |
|---|---|---|---|---|
| 現行版本 / 年份 | 2017 白皮書（ACR 官網現行 chart 內容與之一致） | **2015**（結節部分）；2025 ATA 指引已改為 DTC 專用 | 2017 | **2021**（2011 → 2016 → 2021） |
| 原始文獻 | J Am Coll Radiol 2017 `[28372962]` | Thyroid 2016 `[26462967]` | Eur Thyroid J 2017 `[29167761]` | Korean J Radiol 2021 `[34719893]` |
| 分類邏輯 | **Point-based**（5 個特徵類別加總） | **Pattern-based**（5 種型態） | **Pattern-based**（5 級） | **Pattern-based**（5 級） |
| 類別數 | TR1–TR5 | Benign / Very low / Low / Intermediate / High | EU-TIRADS 1–5 | K-TIRADS 1–5 |
| 最高類別惡性風險 | TR5 **35%**（風險門檻 >20%） | High **>70–90%** | 5 級 **26–87%** | 5 級 **>60%** |
| 最低（非良性）類別風險 | TR3 **4.8%** | Very low **<3%** | 3 級 **2–4%** | 3 級 **3–10%** |
| FNA 門檻（最高類別） | TR5 **≥1.0 cm** | High **≥1 cm** | 5 級 **>10 mm** | 5 級 **>1.0 cm** |
| FNA 門檻（中間類別） | TR4 **≥1.5 cm** | Intermediate **≥1 cm** | 4 級 **>15 mm** | 4 級 **>1.0–1.5 cm** |
| FNA 門檻（低類別） | TR3 **≥2.5 cm** | Low **≥1.5 cm** | 3 級 **>20 mm** | 3 級 **>2.0 cm** |
| 追蹤門檻 | TR3 ≥1.5 cm、TR4 ≥1.0 cm、TR5 ≥0.5 cm | 依 pattern 決定間隔（12 / 12–24 / ≥24 個月） | 未定義依類別的追蹤間隔；R11 反對以序列 US 測生長預測癌症 | K5 每 6 個月×1–2 年後每年；K3/K4 於第 1、3、5 年 |
| 是否有正式改版 | 無（PubMed 未檢索到改版白皮書） | **有，且為「拆分」**：2025 版只管 DTC，結節被移出 | 無（PubMed 標題檢索未發現） | **有**：2016 → 2021 |
| 4 系統整體診斷效能 | 一項 33,748 顆結節的統合分析結論為「四者整體效能相當」`[32303153]` ||||

**分類規則差異的一句話總結**：ACR 是**加總計分**，其餘三者是**型態比對**；同一顆部分囊性、低回音的結節，
K-TIRADS 依「composition 優先」判為 low，EU-TIRADS 依「只要有 hypoechoic 成分」判為 intermediate ——
這是 EU-TIRADS 原文自己點名的差異 `[29167761]`。

---

## 1. ACR TI-RADS

### 1.1 版本與原始文件

| 欄位 | 內容 |
|---|---|
| 版本 | ACR TI-RADS Committee White Paper，2017 |
| 期刊 | Journal of the American College of Radiology : JACR |
| PMID | 28372962 |
| DOI | 10.1016/j.jacr.2017.01.046 |
| 配套說明文件 | Radiology 2018「TI-RADS: A User's Guide」，PMID 29558300，DOI 10.1148/radiol.2017171240 |
| 官方 chart | https://www.acr.org/Clinical-Resources/Clinical-Tools-and-Reference/Reporting-and-Data-Systems/TI-RADS （HTTP 200，已下載官方 PDF 核對） |

原文摘要明確交代其沿革：ACR 於 2012 年成立委員會，分別處理 (1) 偶發結節報告建議、(2) 超音波
報告用詞 lexicon、(3) 基於 lexicon 的 TI-RADS；前兩項於 2015 年發表，本白皮書為第三項 `[28372962]`。

### 1.2 分類規則（point-based）

以下計分表逐格核對自 ACR 官網 `TI-RADS-Assessment-Categories.pdf`：

| 類別 | 選項 | 分數 |
|---|---|---|
| **Composition**（擇一） | Cystic or almost completely cystic | 0 |
| | Spongiform | 0 |
| | Mixed cystic and solid | 1 |
| | Solid or almost completely solid | 2 |
| **Echogenicity**（擇一） | Anechoic | 0 |
| | Hyperechoic or isoechoic | 1 |
| | Hypoechoic | 2 |
| | Very hypoechoic | 3 |
| **Shape**（擇一） | Wider-than-tall | 0 |
| | Taller-than-wide | 3 |
| **Margin**（擇一） | Smooth | 0 |
| | Ill-defined | 0 |
| | Lobulated or irregular | 2 |
| | Extra-thyroidal extension | 3 |
| **Echogenic foci**（**全選**） | None or large comet-tail artifacts | 0 |
| | Macrocalcifications | 1 |
| | Peripheral (rim) calcifications | 2 |
| | Punctate echogenic foci | 3 |

**判定不出來時的預設值**（官方 chart 明列，臨床上最常被忽略）：

- Composition 判定不出來 → **視為 solid**
- 因鈣化而無法判定 composition → **給 2 分**
- Echogenicity 判定不出來 → **視為 isoechoic（1 分）**
- Margin 判定不出來 → **給 0 分**

### 1.3 各類別、惡性風險、FNA 與追蹤門檻

| Level | 分數 | 定義 | 惡性風險 | FNA | 追蹤 |
|---|---|---|---|---|---|
| **TR1** | 0 | Benign | 0.3% | 不做 | 不追蹤 |
| **TR2** | 2 | Not suspicious | 1.5% | 不做 | 不追蹤 |
| **TR3** | 3 | Mildly suspicious | 4.8% | ≥2.5 cm | ≥1.5 cm（第 1、3、5 年） |
| **TR4** | 4–6 | Moderately suspicious | 9.1% | ≥1.5 cm | ≥1.0 cm（第 1、2、3、5 年） |
| **TR5** | ≥7 | Highly suspicious | 35% | ≥1.0 cm | ≥0.5 cm（每年，最多 5 年） |

- **分數、FNA 與追蹤 size cutoff**：核對自 ACR 官方 chart 兩份 PDF（主 chart 與 alternative chart），兩份完全一致。
- **惡性風險百分比與追蹤年度排程**：JACR 白皮書為付費牆，故以同儕審查的開放取用回顧
  TouchREVIEWS in Endocrinology 2024 Table 3 核對，該表明列引用 ACR 白皮書 `[39526062]`。
  ⚠️ 未能直接由 JACR 白皮書原文逐字核對此二項，需人工確認。
- 官方 chart 註明：5–9 mm 的 TR5 結節請參照 papillary microcarcinoma 的討論（即不是無條件穿刺）。
- 官方 chart 註明：definite extra-thyroidal extension 應視為 malignant until proven otherwise。

### 1.4 驗證資料

多中心驗證研究（AJR 2017，`[28402167]`）納入 **3422 顆結節、其中 352 顆為惡性**：

- 各特徵（composition、echogenicity、margin、echogenic foci）與惡性風險皆顯著相關（p < 0.0001）
- 惡性風險隨 point level 0→10 與 TR1→TR5 遞增（p < 0.0001）
- **2948/3422（86.1%）** 的結節其實際風險落在 TI-RADS 風險門檻 ±1% 內
- 偏離超過 1% 的 474 顆中，**88.0%（417/474）是風險低於門檻**（即系統偏保守）

### 1.5 主要優點

1. **可稽核性最高**：分數可回推，報告品質可被審查，也最適合做 AI／structured reporting 的底層。
2. **降低不必要 FNA 的效果在多項研究中最好**：477 名前瞻性個案中，ACR TI-RADS 判定
   **268/502（>50%）** 的切片為不必要，false-negative rate 僅 **2.2%**、NPV **97.8%（95% CI 95.2–99.2）**，
   為五套系統中降幅最大者 `[30299457]`。
3. 統合分析（12 篇、18,750 顆結節）顯示 ACR TI-RADS 的相對 DOR 顯著高於 ATA（P = .002）
   與 K-TIRADS（P = .002）`[31690937]`。
4. 判讀者間一致性佳：一項 1096 顆手術結節研究中 ACR TI-RADS 的 ICC 為 **0.937**，為五套系統最高 `[34777258]`。

### 1.6 常見誤用

1. **Echogenic foci 忘記可以複選**：這是唯一一個「Choose All That Apply」的欄位，漏選會系統性低估。
2. **把 large comet-tail artifact 當成 punctate echogenic foci**：前者 0 分、後者 3 分，一格之差可讓 TR3 變 TR5。
   官方 chart 對 large comet-tail artifact 的定義是「V 形、>1 mm、位於囊性成分內」。
3. **忽略 spongiform 的「短路」規則**：composition 選 spongiform 即 0 分，且**不再為其他類別加分**。
4. **忽略判定不出來時的預設值**（見 1.2），尤其是「因鈣化看不清 composition → 給 2 分」。
5. **對多發結節逐顆評分**：文獻指出應只對**分數最高的四顆**（不必然是最大的）評分、報告與追蹤 `[39526062]`。
   ACR 官方 sonographer worksheet 的措辭則是「兩顆最大的結節，加上任何具重要特徵者」——
   兩份可取得的來源措辭不一致，⚠️ 白皮書原文究竟如何規定，需人工確認。
6. **把 TR 分級當成「要不要開刀」**：TI-RADS 只回答「要不要穿刺／追蹤」。

### 1.7 改版狀況

PubMed 檢索未找到 ACR 發表的正式改版白皮書；ACR 官網現行 chart（本次已下載核對）
內容與 2017 白皮書計分規則一致。
⚠️ ACR 是否曾以非期刊形式（如官網勘誤、委員會聲明）發布修訂，未能由原文查證，需人工確認。

---

## 2. ATA sonographic pattern

### 2.1 版本與原始文件 —— **這是本課程最需要講清楚的一件事**

| 欄位 | 內容 |
|---|---|
| **結節風險分層的現行依據** | **2015 ATA guidelines**（Thyroid 2016 出版） |
| 期刊 | Thyroid : official journal of the American Thyroid Association |
| PMID | 26462967 |
| DOI | 10.1089/thy.2015.0020 |
| 開放全文 | PMC4739132 |

**2025 年 ATA 發表了新版指引，但它不再包含甲狀腺結節。** 2025 版標題為
《2025 American Thyroid Association Management Guidelines for Adult Patients with
**Differentiated Thyroid Cancer**》（Thyroid 2025，PMID 40844370，DOI 10.1177/10507256251363120），
其摘要原文寫道：

> "The practice guidelines of the American Thyroid Association (ATA) for DTC management in adult
> patients (**previously combined with thyroid nodules**) were published initially in 1996, with
> subsequent revisions based on advances in the field."

括號內 "previously combined with thyroid nodules" 即為結節被移出的直接證據。2025 版摘要所列的
涵蓋範圍從「initial cancer diagnosis」開始，涵蓋 staging、initial treatment、response assessment、
monitoring、subsequent therapies，並未涵蓋結節的超音波風險分層 `[40844370]`。
其 executive summary（PMID 41173539）列出的 2025 vs 2015 重點差異為：DATA 架構、分子診斷角色擴大、
風險分層精緻化、更強調 active surveillance 與 lobectomy、納入 ablative procedures、
低風險病人監測降階、引入 complete remission 概念——同樣不含結節超音波分層 `[41173539]`。

⚠️ 截至查證日，PubMed 未檢索到 ATA 另行發表的獨立「thyroid nodule」指引。
**因此臨床上引用「ATA sonographic pattern」時，仍應引 2015 版**；本課程須明確提醒學員，
「ATA 2025」與「ATA 結節五型態」是兩份不同範圍的文件，不可混用。

### 2.2 分類規則、惡性風險與 FNA 門檻（pattern-based）

以下逐格核對自 2015 ATA 指引 Table 5（PMC4739132）：

| Pattern | 超音波特徵 | 惡性風險 | FNA size cutoff |
|---|---|---|---|
| **High suspicion** | Solid hypoechoic nodule，或部分囊性結節的 solid hypoechoic 成分，具下列**任一**：irregular margins（infiltrative, microlobulated）、microcalcifications、taller-than-wide shape、rim calcifications with small extrusive soft tissue component、evidence of ETE | **>70–90%** | 建議 FNA 於 **≥1 cm** |
| **Intermediate suspicion** | Hypoechoic solid nodule，margins 平滑，無 microcalcifications、ETE、taller-than-wide | **10–20%** | 建議 FNA 於 **≥1 cm** |
| **Low suspicion** | Isoechoic 或 hyperechoic solid nodule，或部分囊性且 solid 成分偏心，無 microcalcification、irregular margin、ETE、taller-than-wide | **5–10%** | 建議 FNA 於 **≥1.5 cm** |
| **Very low suspicion** | Spongiform 或部分囊性結節，且不具上述 low / intermediate / high 之任何特徵 | **<3%** | **考慮** FNA 於 **≥2 cm**；不做 FNA 只觀察亦為合理選項 |
| **Benign** | 純囊性結節（無 solid 成分） | **<1%** | 不切片 |

原文另註明：high suspicion pattern 的結節「highly likely to be a PTC」；但在無 ETE、無頸部轉移
淋巴結、無遠端轉移的前提下，**<1 cm 的 micropapillary thyroid cancer 常呈 indolent 病程**，
是否穿刺可能因年齡而異 `[26462967]`。

### 2.3 Follow-up threshold

2015 ATA **RECOMMENDATION 23** 明定：良性細胞學結果之後的追蹤，應**依超音波型態而非依生長速度**決定
（原文理由：US-guided FNA 的偽陰性率低，且漏掉的惡性更常由型態而非生長揪出）`[26462967]`：

| 情境 | 建議 | 證據強度 |
|---|---|---|
| High suspicion US pattern | **12 個月內**重複 US 與 US-guided FNA | Strong, Moderate-quality |
| Low 至 Intermediate suspicion | **12–24 個月**重複 US | Weak, Low-quality |
| Very low suspicion（含 spongiform） | 若要重複 US，應在 **≥24 個月** | Weak, Low-quality |
| **已有兩次良性細胞學** | **不再需要**針對惡性風險的 US 監測 | Strong, Moderate-quality |

**「生長」的操作型定義**（ATA 原文）：至少兩個徑線增加 20%，且最小增幅 ≥2 mm；或體積變化 >50%。
原文並引用 Brauer 等人的資料說明此定義的由來（50% 體積增加 ≒ 三個徑線中兩個各增 20%），
且若採 50% 體積增加為切點，平均 18 個月時僅 **4%–10%** 的結節會被判定為變大 `[26462967]`。

### 2.4 主要優點

1. **與細胞學／臨床決策的銜接最完整**：ATA 指引本身涵蓋 FNA 判讀、分子標記、良性結節處置，
   pattern 只是入口，後續路徑在同一份文件內接得起來。
2. **型態式判讀上手快**，不需計分，適合非放射科的內分泌科／外科臨床情境。
3. 在 33,748 顆結節的統合分析中，ATA category 5 的敏感度 **74%**、特異度 **88%**，
   其敏感度高於 ACR（66%）與 K-TIRADS（55%）`[32303153]`。

### 2.5 常見誤用

1. **最重要的一項**：引用「ATA 2025」來支持結節超音波分層——2025 版已不含結節（見 2.1）。
2. **把 "not classifiable" 硬塞進某一型**：ATA 是型態比對，臨床上相當比例的結節不完全吻合任一型態；
   一項 45 例 FTC 的研究中，**每 3 例就有 1 例無法被各系統分類** `[31899594]`。
3. **忘記 very low suspicion 的「不穿刺也合理」**：原文寫的是 "Consider FNA at ≥2 cm.
   Observation without FNA is also a reasonable option."，不是強制穿刺。
4. **以生長作為重複 FNA 的主要觸發**：ATA 明確把追蹤策略建立在**型態**而非生長之上。
5. **兩次良性後仍持續每年追蹤**：Recommendation 23(D) 明講不再需要。

### 2.6 改版狀況

- 1996 首版，其後多次改版（2025 版摘要自述）。
- 2015 版：結節 + DTC 合併。
- **2025 版：拆分，只涵蓋 DTC**，PMID 40844370；另有 executive summary（PMID 41173539）
  與一則 corrigendum（Thyroid 2025 Nov，PMID 41182278）。
- ⚠️ ATA 是否計畫或已發表獨立的結節指引，未能由原文查證，需人工確認。

---

## 3. EU-TIRADS

### 3.1 版本與原始文件

| 欄位 | 內容 |
|---|---|
| 版本 | ETA Guidelines，2017 |
| 期刊 | European thyroid journal |
| PMID | 29167761 |
| DOI | 10.1159/000478927 |
| 開放全文 | PMC5652895（本次已完整擷取核對） |

原文自述其設計來源：以文獻回顧為基礎，並參考 AACE、ATA 與 Korean guidelines 的良性／低／中／
高風險定義與 FNA 建議 `[29167761]`。

### 3.2 分類規則、惡性風險與 FNA 門檻（pattern-based）

以下核對自 PMC5652895 的分類表與各級 Recommendation 內文：

| 類別 | 超音波型態 | 惡性風險 | FNA |
|---|---|---|---|
| **EU-TIRADS 1**（normal） | 無結節 | — | — |
| **EU-TIRADS 2**（benign） | 純／無回音囊腫；完全 spongiform 結節 | **接近 0%**（原文 "close to 0%"） | **不建議**（除非治療性，如壓迫症狀） |
| **EU-TIRADS 3**（low risk） | 橢圓形、邊緣平滑、iso-/hyperechoic，無任何高風險特徵 | **2–4%** | 通常只在 **>20 mm** 才做 |
| **EU-TIRADS 4**（intermediate） | 橢圓形、邊緣平滑、**mildly hypoechoic**，無任何高風險特徵 | **6–17%** | 通常在 **>15 mm** 做 |
| **EU-TIRADS 5**（high risk） | 具下列**至少一項**：non-oval shape、irregular margins、microcalcifications、marked hypoechogenicity（且為 solid） | **26–87%** | **>10 mm** 做 |

> 註：PMC 版表格中 EU-TIRADS 2 的風險欄位渲染為 `$0`（HTML 呈現瑕疵）；
> 本文採用內文明確文字「Risk of malignancy: close to 0%」。

**15 mm 這個門檻的由來（原文自述）**：task force 認為 EU-TIRADS 4 屬中間風險，
故將門檻訂在 EU-TIRADS 5（10 mm）與 EU-TIRADS 3（20 mm）**之間** `[29167761]`。
這是四套系統中唯一把「門檻怎麼來的」寫進正文的。

### 3.3 特殊情境規則（原文明列，臨床最實用）

1. **Subcentimeter EU-TIRADS 5**：若無異常淋巴結，且病人願意接受規則追蹤，**建議 active surveillance**；
   若追蹤中證實生長或出現可疑淋巴結，則做 FNA。病人可在 active surveillance 與 FNA 之間選擇。
2. **EU-TIRADS 5 第一次細胞學為良性**：應於 **3 個月內重複 FNA**，以降低偽陰性。
3. **多結節甲狀腺的掃描順序**：先找高風險結節並描述之（**不論大小**），>10 mm 則穿刺；再找中risk 結節……
   ——即「風險優先於大小」，而非「先挑最大顆」。
4. **有疑慮時往下歸類**：若無法確定囊腫內的回音物是 fibrin clot 還是真的 solid 成分，
   該結節應歸入 low-risk 類別；若微囊腔未占滿整顆結節，亦應視為 low risk。

### 3.4 Follow-up threshold

**EU-TIRADS 未定義依類別的追蹤間隔。** 相對地，其 **Recommendation R11** 明確寫道：

> "Routine determination of nodule growth by serial thyroid US assessments, in order to predict
> cancer, is not justified."（QOE = ++; SOR = grade 2）`[29167761]`

⚠️ ETA 是否在其他文件另訂追蹤間隔，未能由原文查證，需人工確認。

### 3.5 驗證資料

統合分析（Eur J Endocrinol 2020，7 篇研究、5672 顆結節，以組織學為 reference standard）`[32544875]`：

| EU-TIRADS 類別 | 實際惡性盛行率（95% CI） | 指引宣稱範圍 |
|---|---|---|
| 2 | **0.5%**（0.0–1.3） | ~0% |
| 3 | **5.9%**（2.6–9.2） | 2–4% |
| 4 | **21.4%**（11.1–31.7） | 6–17% |
| 5 | **76.1%**（63.7–88.5） | 26–87% |

EU-TIRADS 5 的表現：敏感度 **83.5%**（74.5–89.8）、特異度 **84.3%**（66.2–93.7）、
PPV **76.1%**、NPV **85.4%**、LR+ **4.9**、LR− **0.2**、DOR **24.5**（11.7–51.0）。

> **教學重點**：第 3 級與第 4 級的實測盛行率（5.9%、21.4%）都**高於**指引宣稱上限（4%、17%）。
> 這是 EU-TIRADS 最值得討論的校準問題。

### 3.6 主要優點

1. **最簡單、最快上手**：只有四個高風險特徵要記，且「有一個就是 5 級」。
2. **敏感度高**：33,748 顆結節的統合分析中，EU-TIRADS category 5 的**敏感度 82%，為四系統最高**；
   category 4 or 5 的敏感度 **96%**，同樣最高 `[32303153]`。
3. **把不確定性寫成規則**（見 3.3 第 4 點），減少判讀者自由心證。
4. 2026 年 ESR Essentials（European Society of Head and Neck Radiology）仍將 EU-TIRADS
   列為歐洲主流系統，並獨立複述其 >20 / >15 / >10 mm 門檻 `[41258456]`。

### 3.7 常見誤用

1. **把所有 hypoechoic 結節都當 5 級**：EU-TIRADS 5 要求的是 **marked** hypoechogenicity（且為 solid）；
   **mildly** hypoechoic 且形狀邊緣正常者是 4 級。原文並提醒 marked hypoechogenicity 是四個特徵中
   **敏感度最低**者，且「只有在結節為 solid、而非已癒合囊腫的疤痕時才具特異性」。
2. **忽略「部分囊性也可能是 4 級」**：EU-TIRADS 刻意與 K-TIRADS 分道揚鑣——只要 solid 成分中有任何
   hypoechoic 組織，就歸中風險，含有囊性成分者亦然（原文明講此為與 Korean TIRADS 的差異點）。
3. **>10 mm 的高風險結節一律穿刺**：原文有例外——病人不可手術或因共病預期壽命短者除外。
4. **對 <10 mm 的 5 級結節直接穿刺**：原文建議先討論 active surveillance。
5. **多結節時先挑最大顆**：原文的順序是先找高風險、不論大小。
6. **特徵數量不計入分級**：原文說明惡性風險**隨可疑特徵數量增加**，且 spiculation／lobulation／
   punctate echogenic foci 的**數量**會提高特異度——但分級本身仍是「有一個就 5 級」。
   這正是 26–87% 這個極寬風險區間的來源。

### 3.8 改版狀況

PubMed 標題檢索（`"EU-TIRADS"[ti]`，41 筆）未發現任何正式改版或 2.0 版文件。
⚠️ ETA 是否有非期刊形式的更新，未能由原文查證，需人工確認。

---

## 4. K-TIRADS

### 4.1 版本與原始文件

| 版本 | 文獻 | PMID | DOI |
|---|---|---|---|
| 2011 | KSThR 首版建議 | ⚠️ 本次未檢索到，需人工確認 | — |
| 2016 | Korean J Radiol 2016（Shin JH 等） | 27134526 | 10.3348/kjr.2016.17.3.370 |
| **2021（現行）** | Korean J Radiol 2021（Ha EJ, Chung SR, Na DG 等） | **34719893** | **10.3348/kjr.2021.0713** |

兩版皆為開放取用（PMC4842857 / PMC8628155），本次已完整擷取核對。

### 4.2 分類規則（pattern-based，2021 版）

2021 K-TIRADS 以 **composition + echogenicity + 三個可疑特徵**的組合來分層。
**三個可疑 US 特徵**為：**punctate echogenic foci、nonparallel orientation、irregular margins**。

原文明確說明其結構原理：單一 US 預測因子無法準確估計惡性風險，且三個可疑特徵的預測力
**會隨 composition 與 echogenicity 而異**，故必須組合使用 `[34719893]`。

### 4.3 各類別、惡性風險與 biopsy 門檻（2021 版 Table 5，逐格核對）

| 類別 | US 型態 | 惡性風險 | Biopsy size 門檻 |
|---|---|---|---|
| **K-TIRADS 5**（high suspicion） | Solid hypoechoic nodule 具三個可疑特徵**任一** | **>60%** | **>1.0 cm** |
| **K-TIRADS 4**（intermediate） | (1) Solid hypoechoic nodule 不具任一可疑特徵；或 (2) 部分囊性或 iso-/hyperechoic 結節具**任一**可疑特徵；或 (3) **完全鈣化結節** | **10–40%** | **>1.0–1.5 cm** |
| **K-TIRADS 3**（low suspicion） | 部分囊性或 iso-/hyperechoic 結節，不具任一可疑特徵 | **3–10%** | **>2.0 cm** |
| **K-TIRADS 2**（benign） | (1) Iso-/hyperechoic spongiform；(2) 部分囊性且含 intracystic echogenic foci 與 comet-tail artifact；(3) 純囊腫 | **<3%** | 不常規建議 |
| **K-TIRADS 1** | 無結節 | — | — |

補充規則（原文明列）：

- **1.0–1.5 cm 這個「區間」是刻意的**：原文寫明採用 cutoff **range**（1–1.5 cm）以利臨床彈性應用；
  在無特殊風險因子時，建議 **>1.5 cm** 才切片。
- **無論大小都要切片的情況**：合併不良預後因子（如懷疑頸部淋巴結轉移）時，應對最可疑的結節切片。
- 廣泛的實質內 punctate echogenic foci 而無明確結節（懷疑 diffuse sclerosing variant PTC）、
  以及 diffusely infiltrative lesions（懷疑轉移或淋巴瘤）→ 歸 **K-TIRADS 4**。
- K-TIRADS 2 通常不切片，但**持續且顯著生長**、或在 ablation／手術前，仍可切片。

### 4.4 Follow-up threshold

2021 版明列（與 PTMC active surveillance 策略一致）`[34719893]`：

| 類別 | 追蹤排程 |
|---|---|
| **K-TIRADS 5** | 每 **6 個月** 追蹤 1–2 年；若無生長，其後每年一次 |
| **K-TIRADS 3 / 4** | 於第 **1、3、5 年** 追蹤 |
| 5 年無變化後 | K-TIRADS 4 每 **3–5 年**；K-TIRADS 3 於第 **5 年** |

### 4.5 改版：2016 → 2021 改了什麼

原文自述「與 2016 版相比，2021 版在結構與建議惡性風險上差異不大」，實際更動如下
（逐項核對 2016 Table 與 2021 Table 5）：

| 項目 | 2016 | 2021 |
|---|---|---|
| K-TIRADS 5 風險 | >60% | >60%（不變） |
| K-TIRADS 4 風險 | **15–50%** | **10–40%** |
| K-TIRADS 3 風險 | **3–15%** | **3–10%** |
| K-TIRADS 2 風險 | <3% | <3%（不變） |
| **完全鈣化結節** | ⚠️ 2016 表格未單獨列出，需人工確認 | 明確歸 **K-TIRADS 4** |
| **K-TIRADS 2 型態合併可疑特徵** | 歸 **K-TIRADS 4** | **仍歸 K-TIRADS 2**（不論是否合併可疑特徵） |
| FNA：K5 | ≥1 cm（>0.5 cm 選擇性） | **>1.0 cm** |
| FNA：K4 | ≥1 cm | **>1.0–1.5 cm** |
| FNA：K3 | ≥1.5 cm | **>2.0 cm** |
| FNA：K2 | ≥2 cm | **不常規建議** |

**改版動機（原文明講）**：降低良性結節的不必要切片，同時在 **1–2 cm 小結節**維持適當敏感度；
K-TIRADS 3、4 惡性風險的修訂則是根據兩項近期大型世代研究 `[34719893]`。

### 4.6 改版的量化代價（2021 原文引用之多中心資料，最值得放進課程）

一項 **5708 顆結節（惡性率 19.5%）** 的多中心回溯研究 `[34719893]`：

| K-TIRADS 4 的切片 cutoff | 敏感度 | 特異度 | 良性結節不必要切片率 |
|---|---|---|---|
| **1.5 cm**（2021 採用） | **76.1%** | **50.2%** | **40.1%** |
| **1.0 cm** | **91.0%** | 39.7% | 48.6% |

同一份資料：採 1.5 cm cutoff 時，對 **>2 cm 的惡性腫瘤**仍維持 **98.0%** 的高敏感度；
且 **≤2.0 cm 小結節的不必要切片率為 17.6%**，顯著**低於** AACE/ACE/AME、EU-TIRADS 與
ACR TI-RADS 的 **18.6%–28.1%**。

> **這就是 K-TIRADS 2021 的核心取捨**：用「小結節少穿刺」換「整體敏感度從 91.0% 降到 76.1%」，
> 其正當性建立在「漏掉的多是 <2 cm、預後良好的 PTC」這個假設上。

### 4.7 主要優點

1. **唯一把改版取捨用數字攤開來寫的系統**（見 4.6），教學價值極高。
2. **對小結節最節制**：≤2 cm 結節不必要切片率 17.6%，優於其餘系統。
3. **特異度最高**：33,748 顆結節統合分析中，K-TIRADS category 5 的**特異度 95%，為四系統最高** `[32303153]`。
4. **追蹤排程最具體**（見 4.4），四套系統中唯一給出明確年度表者。
5. 內容涵蓋 lexicon、biopsy criteria、ETE 的 US 判準、甲狀腺 CT protocol、切片前後追蹤，
   是四份文件中最完整的操作手冊。

### 4.8 常見誤用

1. **用 2016 版的門檻做 2021 版的判讀**：K3 從 ≥1.5 cm 變成 >2.0 cm、K4 從 ≥1 cm 變成 >1.0–1.5 cm，
   差異足以改變處置。
2. **把 K-TIRADS 2 的結節因為合併可疑特徵而升級**——這正是 2021 版改掉的（2016 版才升到 4）。
3. **忽略完全鈣化結節屬 K-TIRADS 4**。
4. **把 1.0–1.5 cm 讀成「1.0 cm」**：原文的預設是「無特殊風險因子時用 >1.5 cm」。
5. **敏感度最低的系統當成敏感度足夠**：K-TIRADS category 5 的統合敏感度僅 **55%** `[32303153]`。

---

## 5. 其他具臨床影響力的區域性系統

### 5.1 C-TIRADS（中國，2020）

| 欄位 | 內容 |
|---|---|
| 原始文獻 | Zhou J, Yin L, Wei X 等，Endocrine 2020 Nov |
| PMID | 32827126 |
| DOI | 10.1007/s12020-020-02441-y |
| 制訂單位 | 中華醫學會超音波醫學分會淺表器官與血管超音波學組 |

**制訂動機（原文摘要明講）**：全球無任何一版 TIRADS 被普遍採用，而中國境內
**多達十個版本的 TIRADS 同時在不同醫院使用，造成大量混亂**；C-TIRADS 以文獻回顧、專家共識，
以及中國甲狀腺與乳腺超音波人工智慧聯盟提供的多中心資料為基礎建立 `[32827126]`。

**分類規則（point-based）** —— 核對自兩份獨立的開放取用同儕審查文獻 `[41695694]`、`[39526062]`：

惡性特徵，**各 +1 分**：
1. Solid composition
2. Microcalcifications
3. Vertical orientation（taller-than-wide）
4. **Marked hypoechogenicity**（定義：回音低於相鄰頸部帶狀肌）
5. Ill-defined / irregular margins 或 extrathyroidal extension

良性特徵，**−1 分**：comet-tail artifact

| 類別 | 總分 | 定義 | 惡性風險 |
|---|---|---|---|
| 1 | — | 無結節 | 0% |
| **2** | **−1** | Benign | 0% |
| **3** | **0** | Probably benign | **<2%** |
| **4A** | **1** | Low suspicion | **2–10%** |
| **4B** | **2** | Moderate suspicion | **10–50%** |
| **4C** | **3–4** | High suspicion | **50–90%** |
| **5** | **5** | Highly suggestive of malignancy | **>90%** |
| 6 | — | 已由切片證實之惡性 | — |

補充規則：若一顆結節內有一種以上 hyperechoic pattern，只計最高分者 `[39526062]`。

**與 Kwak TI-RADS 的關鍵差異**：C-TIRADS 把 Kwak 的 "hypoechogenicity" 換成
**marked** hypoechogenicity，並移除 "mainly solid"；同時把 comet-tail artifact 當作**負分**的
良性指標——這是所有主流系統中唯一有負分項的 `[34777258]`、`[41695694]`。

**⚠️ C-TIRADS 依大小的 FNA threshold 與 follow-up threshold：未能由原文查證，需人工確認。**
（Endocrine 2020 原文為付費牆，可取得的次級文獻未複述其 size cutoff。）

**驗證資料**（Front Endocrinol 2021，1096 顆手術病理結節）`[34777258]`：

- **不必要切片率最低：49.02%**（p < 0.001，五系統中最佳）
- **特異度 82.3%、PPV 69.2%**，皆為五系統最高
- AUC **0.816**，高於 Kwak（0.789）、K-TIRADS（0.773）、ACR（0.763）、EU-TIRADS（0.734）
- 判讀者間一致性 ICC 0.854
- ≤10 mm 與 >10 mm 結節的 AUC 無統計差異（all P > 0.05）

另有 1721 顆結節的研究顯示，把 marked hypoechogenicity 的定義從「低於帶狀肌」放寬為
**「低於或等於帶狀肌」**，敏感度由 **15.1% 升至 74.5%**、AUC 由 0.563 升至 0.836，
特異度僅由 97.4% 微降至 92.6%，judge 間 kappa 由 0.652 升至 0.722 `[41695694]`。

### 5.2 Kwak TI-RADS（韓國，2011）

| 欄位 | 內容 |
|---|---|
| 原始文獻 | Kwak JY 等，Radiology 2011 Sep |
| PMID | 21771959 |
| DOI | 10.1148/radiol.11110206 |

**建構方式（原文摘要）**：納入 1638 名病人的 **1658 顆 ≥1 cm 結節**，以 generalized estimating
equations 做單變項與多變項分析，各顯著因子依 logistic regression 的 β 係數給分後加總，
建立擬合惡性機率的方程式；**惡性風險依「可疑 US 特徵的數目」判定** `[21771959]`。

**與惡性顯著相關的六個 US 特徵**（原文明列）：
solid component、hypoechogenicity、**marked** hypoechogenicity、microlobulated or irregular margins、
microcalcifications、taller-than-wide shape。

**各類別惡性風險**（核對自 Front Endocrinol 2021 之 reference malignancy risk 欄）`[34777258]`：

| 類別 | 惡性風險 |
|---|---|
| 2 | 0% |
| 3 | ≤5% |
| 4A | 5–10% |
| 4B | 10–50% |
| 4C | 50–85% |
| 5 | 85–100% |

**⚠️ 各類別確切對應幾個可疑特徵（4A=1、4B=2……）：未能由原文查證，需人工確認。**
（Radiology 2011 原文為付費牆。）

**臨床意義**：Kwak TI-RADS 至今仍在中國與部分亞洲中心廣泛使用，且在 1096 顆結節的比較中
**敏感度 89.9%、NPV 91.0% 皆為五系統最高** `[34777258]`——它是「不想漏掉」時的系統。

### 5.3 日本 JSUM / JABTS

**⚠️ 未能由原文查證，需人工確認。**

本次以多組關鍵字檢索 PubMed（含 `JSUM`、`JABTS`、`Japan Association of Breast and Thyroid Sonology`、
`Japan Thyroid Association guidelines thyroid nodule`、`Japanese thyroid nodule ultrasound classification`），
**未能取得日本甲狀腺結節超音波風險分層系統的英文原始文件**。
檢索到的 JABTS 相關文獻多屬乳房超音波領域。

本節不填入任何分類門檻或風險百分比。若課程須涵蓋，建議人工向日本超音波醫學會（JSUM）／
日本乳腺甲状腺超音波医学会（JABTS）取得日文原始文件後補寫。

---

## A. 系統間不一致

### A.1 四系統的敏感度與特異度（最大規模統合分析）

**Ha EJ 等，Thyroid 2020，29 篇研究、33,748 顆結節** `[32303153]`：

| 系統 | Category 5 敏感度 | Category 5 特異度 | Category 4 or 5 敏感度 | Category 4 or 5 特異度 |
|---|---|---|---|---|
| **ACR TI-RADS** | 66% | **91%** | **95%** | 55% |
| **ATA** | 74% | 88% | 91% | **64%** |
| **K-TIRADS** | **55%** | **95%** | 89% | **64%** |
| **EU-TIRADS** | **82%** | 90% | **96%** | **52%** |

該研究結論：**四套系統的整體診斷效能相當（comparable）**；研究地點、女性比例、惡性結節比例
與研究設計皆與異質性有關。

> **教學用一句話**：Category 5 這一層，EU-TIRADS 最敏感（82%）、K-TIRADS 最特異（95%），
> 兩者相差 27 個百分點的敏感度——這不是誤差，這是設計取向的差異。

### A.2 Unnecessary FNA rate 與降低切片的能力

| 研究 | 設計 | 主要發現 | PMID |
|---|---|---|---|
| Grani G 等，JCEM 2019 | 前瞻，477 名病人、502 次切片 | 各系統可減少切片 **17.1%–53.4%**；**ACR TI-RADS 減幅最大（268/502）且 FNR 最低（2.2%，NPV 97.8%，95% CI 95.2–99.2）**；**除 K-TIRADS 外**其餘系統皆有顯著鑑別力，但減幅顯著較小 | `[30299457]` |
| Castellana M 等，JCEM 2020 | 統合分析，12 篇、18,750 顆結節 | DOR 範圍 **2.2–4.9**；head-to-head 顯示 **ACR TI-RADS 的相對 DOR 顯著高於 ATA（P = .002）與 K-TIRADS（P = .002）**，源於較高的 positive LR | `[31690937]` |
| Qi Q 等，Front Endocrinol 2021 | 單中心，1096 顆手術結節 | **不必要切片率：C-TIRADS 49.02% 最低（p < 0.001）**；Kwak 敏感度 89.9%／NPV 91.0% 最高；C-TIRADS 特異度 82.3%／PPV 69.2% 最高；AUC C 0.816 > Kwak 0.789 > K 0.773 ≈ ACR 0.763 > EU 0.734 | `[34777258]` |
| Ultrasound Q 2023 | 266 顆結節，惡性率 10.5% | Category 5 敏感度／特異度：ACR 60.7/95.4、EU 71.4/93.3、ATA 71.4/93.3、K 67.9/93.3；**ACR 不必要切片率最低（141/238 = 46%）**；AUC 相當 | `[37918114]` |
| K-TIRADS 2021 原文引用之多中心資料 | 5708 顆結節，惡性率 19.5% | **≤2 cm 小結節**的不必要切片率：**K-TIRADS 2021 為 17.6%**，顯著低於 AACE/ACE/AME、EU-TIRADS、ACR TI-RADS 的 **18.6%–28.1%** | `[34719893]` |

> **注意這裡的矛盾**：Grani 2019 與 Castellana 2020 說 ACR TI-RADS 減切片最有效；
> K-TIRADS 2021 引用的資料卻說**在 ≤2 cm 的小結節**上 K-TIRADS 才是最節制的。
> 兩者不衝突——**它們評的不是同一群結節**。這正是課程要教學員讀比較研究時第一個要問的問題。

### A.3 判讀者間一致性與系統間一致性

| 指標 | 數值 | 來源 |
|---|---|---|
| ICC（1096 顆結節，2 位判讀者） | ACR **0.937** > EU **0.858** > C **0.854** > K **0.835** > Kwak **0.811** | `[34777258]` |
| ACR TI-RADS vs K-TIRADS 系統間一致性 | **κ = 0.61（substantial）**，4 位資深判讀者、481 張影像 | `[42306147]` |
| 兩系統 mean AUC 差異 | **無顯著差異（p = 0.52）** | `[42306147]` |
| ACR vs K-TIRADS 的方向性 | ACR **敏感度與 NPV 顯著較高**，但**特異度、PPV 與不必要切片率顯著較低**（皆 p < 0.001） | `[42306147]` |

> κ = 0.61 意味著大約每 5 顆結節就有 1 顆，兩套系統給出不同的最終分級。

### A.4 各系統最容易吵架的結節類型

以下每一項都對應到已查證的原文或研究：

**① Follicular thyroid carcinoma（分歧最大，臨床風險最高）**

Castellana M 等，Cancer Cytopathol 2020，45 例 FTC `[31899594]`：

- 中位腫瘤直徑 32 mm（範圍 11–100），**最常見的表現是 ovoid isoechoic nodule**，
  有或無 lobulated margins
- 各系統把 FTC 歸為 **high risk / high suspicion / malignant 的比例為 11%–74%**，
  **系統間差異達統計顯著**
- **每 3 例就有 1 例無法被分類（not classifiable）**
- 但因為各系統的 size cutoff，**FNA 仍被建議於 69%–100% 的病例**——AACE/ACE/AME、
  ACR TI-RADS 與 Kwak TIRADS 之間一致性良好

> **這是最重要的臨床訊息**：這些系統救 FTC 靠的是**大小門檻**，不是型態辨識。
> 原文結論明講：鑑於 FTC 的超音波表現不可疑，加上細胞學本身偵測 FTC 的已知限制，
> **用超音波來處置細胞學不確定的結節時應格外謹慎**。

**② 這些系統本質上只針對 PTC 驗證過**

Trimboli P 等，Rev Endocr Metab Disord 2021，9 篇研究、19,494 顆結節、6162 例組織學確診惡性 `[32959174]`：

- **PTC 佔 95%**、FTC 2%、MTC 1%、其他 1%
- 原文結論：**TIRADS 應被視為只能診斷 PTC 的工具**；所提出的 pattern 與 cut-off 應予修訂，
  並考慮其他策略以改善對 FTC、MTC 與其他惡性的評估

**③ 部分囊性 / iso-hyperechoic 結節：EU-TIRADS 與 K-TIRADS 的公開分歧**

EU-TIRADS 原文直接點名此爭議 `[29167761]`：

> "In the Korean TIRADS, partially cystic nodules are considered to be low-risk lesions regardless
> of their echogenicity, and only entirely solid hypoechoic nodules are included in the intermediate-risk
> category. However, the Korean low-risk category has a 3–15% risk of malignancy, which is closer to
> the intermediate-risk category as defined by the present ETA guidelines. Thus, we consider all
> hypoechoic nodules as intermediate risk, including those with cystic areas..."

即：**一顆部分囊性、mildly hypoechoic 的 1.8 cm 結節**——
K-TIRADS 判 3 級（門檻 >2.0 cm，**不穿刺**）；EU-TIRADS 判 4 級（門檻 >15 mm，**穿刺**）。
這是同一顆結節、兩個相反建議，且雙方都在照著自己的原文做。

**④ 完全鈣化結節**

- **K-TIRADS 2021**：明確歸 **K-TIRADS 4**（10–40% 風險）`[34719893]`
- **ACR TI-RADS**：無「完全鈣化」此一類目；官方 chart 的處理方式是
  「因鈣化而無法判定 composition → composition 給 2 分」，再加上 macrocalcification 1 分
  或 peripheral calcification 2 分——最終分級取決於判讀者如何歸類該鈣化

**⑤ 最高類別的風險區間寬度**

- ACR TR5：風險門檻 **>20%**（實測 35%）
- EU-TIRADS 5：**26–87%**
- K-TIRADS 5：**>60%**
- C-TIRADS 4C：50–90%；5：>90%

Qi 等人明白指出：ACR 與 EU-TIRADS 最高級別的惡性率範圍**過寬，令臨床醫師困惑**；
且對 solid hypoechoic 結節而言，**多一個惡性特徵就能讓 Kwak 與 EU-TIRADS 的分級衝到 4C／5** `[34777258]`。

**⑥ 校準漂移：EU-TIRADS 3 與 4 級的實測風險高於宣稱值**

見 3.5：實測 5.9%（宣稱 2–4%）與 21.4%（宣稱 6–17%）`[32544875]`。

---

## B. 臨床上如何選擇

**先講結論：不需要選出唯一答案，但同一個單位必須選定一套並前後一致。**
四套系統的整體診斷效能在最大規模的統合分析中被判定為 comparable `[32303153]`，
真正的差異在於**你想把錯誤放在哪一邊**。

### B.1 依情境選擇

| 情境 | 較合適的系統 | 依據 |
|---|---|---|
| **放射科主導、需要 structured reporting／稽核／接 AI** | **ACR TI-RADS** | Point-based 可回推、ICC 0.937 為最高 `[34777258]` |
| **首要目標是減少不必要切片（一般成人族群）** | **ACR TI-RADS** | 減切片 >50%，FNR 2.2%、NPV 97.8% `[30299457]`；相對 DOR 顯著優於 ATA 與 K-TIRADS `[31690937]` |
| **首要目標是不漏掉（高盛行率、轉診中心、有頸部放射線病史）** | **EU-TIRADS**（cat 5 敏感度 82%）或 **Kwak**（敏感度 89.9%、NPV 91.0%） | `[32303153]`、`[34777258]` |
| **1–2 cm 小結節為主的族群、想避免過度診斷** | **K-TIRADS 2021** | ≤2 cm 不必要切片率 17.6% vs 其他系統 18.6–28.1% `[34719893]` |
| **內分泌科／外科門診，需要從結節一路接到細胞學與後續處置** | **ATA 2015** | 單一文件涵蓋 FNA 判讀、分子標記與良性結節處置 `[26462967]` |
| **判讀人力經驗不均、需要最短學習曲線** | **EU-TIRADS** | 只有四個高風險特徵，且把不確定情境寫成規則 `[29167761]` |
| **FNA 取得不易、需要以超音波直接支持手術決策** | **C-TIRADS** | 原文即為此情境設計；不必要切片率 49.02% 最低、特異度 82.3% 最高 `[32827126]`、`[34777258]` |
| **歐洲、需與當地放射科報告接軌** | **EU-TIRADS** | 2026 ESR Essentials 仍列為歐洲主流 `[41258456]` |
| **懷疑 follicular neoplasm** | **任何一套都不可靠** | 各系統把 FTC 歸高風險的比例僅 11%–74%，1/3 無法分類 `[31899594]`；系統本質上只針對 PTC 驗證 `[32959174]` |

### B.2 同一顆結節四個系統給出不同穿刺建議時的處理原則

**原則 0：先確認不是判讀錯誤，而是真的系統分歧。**
先檢查是否誤用了預設值（ACR 的「判不出來」規則）、是否用了舊版門檻（K-TIRADS 2016 vs 2021）、
是否把 mildly 誤讀為 marked hypoechogenicity。**大多數「四系統打架」其實是同一顆結節被描述成四種樣子。**
支持這一點的證據：當 4 位資深判讀者在**同一批影像**上作業時，ACR 與 K-TIRADS 的
系統間一致性可達 κ = 0.61，且 mean AUC 無差異 `[42306147]`。

**原則 1：先問「差異來自型態分級，還是來自 size cutoff？」**

- **若分級一致、只是門檻不同**（例：1.8 cm、中風險結節，EU 建議穿、K-TIRADS 不建議）——
  這是**取捨問題不是對錯問題**，應交由臨床脈絡與病人偏好決定，而非再找第五套系統。
- **若分級本身不一致**（例：部分囊性 hypoechoic 結節被判 3 級 vs 4 級）——
  回到 US 影像重新確認 composition 與 echogenicity 這兩個上游變數；
  這兩者一旦定調，三套 pattern-based 系統的結果通常就會收斂。

**原則 2：讓臨床風險因子做決勝局，而不是讓系統做。**
四套原文都把臨床因子留在系統之外：

- **ATA 2015**：<1 cm 的 high suspicion 結節是否穿刺「may depend upon patient age」`[26462967]`
- **EU-TIRADS**：FNA 指徵「should also be based on clinical risk factors and be in agreement with
  the patient」；且 TSH 偏低時應先做 scintigraphy——**warm/hot 結節不應穿刺** `[29167761]`
- **K-TIRADS 2021**：建議切片時應納入病人風險因子（PET 上 FDG avid、家族性癌症、
  dysphonia 等 worrisome symptoms）與病人特性（年齡、共病、偏好）；
  且**合併不良預後因子時，不論大小都應切片** `[34719893]`

**原則 3：任一系統判為「高風險 + 有頸部淋巴結異常」→ 直接穿刺，不再比對其他系統。**
K-TIRADS 明列此為 override 條件 `[34719893]`；EU-TIRADS 的 subcentimeter active surveillance
也以「無異常淋巴結」為前提 `[29167761]`。

**原則 4：<1 cm 的高風險結節，四套系統的分歧應導向討論而非穿刺。**

- EU-TIRADS：建議 **active surveillance**，讓病人在 surveillance 與 FNA 之間選擇 `[29167761]`
- ATA 2015：無 ETE／無轉移淋巴結／無遠端轉移時，micropapillary carcinoma 常為 indolent `[26462967]`
- ACR 官方 chart：5–9 mm 的 TR5 請參照 papillary microcarcinoma 的討論

**原則 5：懷疑 follicular neoplasm 時，主動宣告「系統不適用」。**
不要在四套系統之間找一個給出穿刺建議的來背書。應直接依大小門檻與臨床判斷處置，
並向臨床端說明超音波在此情境下的限制 `[31899594]`、`[32959174]`。

**原則 6：報告時寫下你用的是哪一套、哪一版。**
「TI-RADS 4」在 ACR、Kwak、C-TIRADS 三套系統裡是三個不同的意思；
「K-TIRADS 3，>1.5 cm 穿刺」是 2016 版、「K-TIRADS 3，>2.0 cm 穿刺」才是 2021 版。
報告若不寫系統與版本，接手的臨床醫師無從還原你的建議。

**原則 7：機構層級選定一套，個案層級才允許例外。**
系統間一致性 κ = 0.61 意味著在單位內混用系統，約每 5 顆結節就會產生 1 次不一致的建議 `[42306147]`；
而四套系統整體效能 comparable `[32303153]`——**混用的代價明確，收益卻沒有證據支持。**

---

## 查證缺口總覽

本文件共 **8 處**標示為「⚠️ 未能由原文查證，需人工確認」：

| # | 項目 | 章節 | 原因 |
|---|---|---|---|
| 1 | ACR TI-RADS 各類別惡性風險百分比（0.3/1.5/4.8/9.1/35%）與追蹤年度排程 | 1.3 | JACR 白皮書付費牆；已以開放取用同儕審查回顧 `[39526062]` 核對，但未由白皮書原文逐字確認 |
| 2 | ACR TI-RADS 多發結節時應評分幾顆（四顆最高分 vs 兩顆最大） | 1.6 | 兩份可取得來源措辭不一致 |
| 3 | ACR TI-RADS 是否曾以非期刊形式發布修訂 | 1.7 | 無可查證之官方聲明 |
| 4 | ATA 是否已／將發表獨立的 thyroid nodule 指引 | 2.6 | PubMed 未檢索到 |
| 5 | ETA 是否在其他文件另訂 EU-TIRADS 追蹤間隔；是否有非期刊形式的更新 | 3.4 / 3.8 | 原文未定義，PubMed 未檢索到 |
| 6 | K-TIRADS 2011 首版文獻；2016 版對完全鈣化結節的歸類 | 4.1 / 4.5 | 本次未檢索到 / 2016 表格未單獨列出 |
| 7 | C-TIRADS 依大小的 FNA threshold 與 follow-up threshold | 5.1 | Endocrine 2020 原文付費牆，次級文獻未複述 |
| 8 | Kwak TI-RADS 各類別對應的可疑特徵數目；日本 JSUM / JABTS 全部內容 | 5.2 / 5.3 | Radiology 2011 付費牆 / PubMed 未檢索到日本系統之英文原始文件 |

---

## 引用文獻

以下 25 筆的 title、journal、year 一律照抄 PubMed E-utilities esummary 回傳值。
機器可讀版本見 `course/data/guideline-refs.json`。

### 原始指引文件（primary）

1. **PMID 28372962** — ACR Thyroid Imaging, Reporting and Data System (TI-RADS): White Paper of the ACR TI-RADS Committee. *Journal of the American College of Radiology : JACR*, 2017. DOI: 10.1016/j.jacr.2017.01.046 — https://pubmed.ncbi.nlm.nih.gov/28372962/
2. **PMID 29558300** — Thyroid Imaging Reporting and Data System (TI-RADS): A User's Guide. *Radiology*, 2018. DOI: 10.1148/radiol.2017171240 — https://pubmed.ncbi.nlm.nih.gov/29558300/
3. **PMID 26462967** — 2015 American Thyroid Association Management Guidelines for Adult Patients with Thyroid Nodules and Differentiated Thyroid Cancer: The American Thyroid Association Guidelines Task Force on Thyroid Nodules and Differentiated Thyroid Cancer. *Thyroid : official journal of the American Thyroid Association*, 2016. DOI: 10.1089/thy.2015.0020 — https://pubmed.ncbi.nlm.nih.gov/26462967/
4. **PMID 40844370** — 2025 American Thyroid Association Management Guidelines for Adult Patients with Differentiated Thyroid Cancer. *Thyroid : official journal of the American Thyroid Association*, 2025. DOI: 10.1177/10507256251363120 — https://pubmed.ncbi.nlm.nih.gov/40844370/
5. **PMID 41173539** — Executive Summary of the 2025 American Thyroid Association Management Guidelines for Adult Patients with Differentiated Thyroid Cancer. *Thyroid : official journal of the American Thyroid Association*, 2025. DOI: 10.1177/10507256251390877 — https://pubmed.ncbi.nlm.nih.gov/41173539/
6. **PMID 41182278** — Corrigendum to: 2025 American Thyroid Association Management Guidelines for Adult Patients with Differentiated Thyroid Cancer. *Thyroid : official journal of the American Thyroid Association*, 2025. DOI: 10.1177/10507256251387671 — https://pubmed.ncbi.nlm.nih.gov/41182278/
7. **PMID 29167761** — European Thyroid Association Guidelines for Ultrasound Malignancy Risk Stratification of Thyroid Nodules in Adults: The EU-TIRADS. *European thyroid journal*, 2017. DOI: 10.1159/000478927 — https://pubmed.ncbi.nlm.nih.gov/29167761/
8. **PMID 27134526** — Ultrasonography Diagnosis and Imaging-Based Management of Thyroid Nodules: Revised Korean Society of Thyroid Radiology Consensus Statement and Recommendations. *Korean journal of radiology*, 2016. DOI: 10.3348/kjr.2016.17.3.370 — https://pubmed.ncbi.nlm.nih.gov/27134526/
9. **PMID 34719893** — 2021 Korean Thyroid Imaging Reporting and Data System and Imaging-Based Management of Thyroid Nodules: Korean Society of Thyroid Radiology Consensus Statement and Recommendations. *Korean journal of radiology*, 2021. DOI: 10.3348/kjr.2021.0713 — https://pubmed.ncbi.nlm.nih.gov/34719893/
10. **PMID 32827126** — 2020 Chinese guidelines for ultrasound malignancy risk stratification of thyroid nodules: the C-TIRADS. *Endocrine*, 2020. DOI: 10.1007/s12020-020-02441-y — https://pubmed.ncbi.nlm.nih.gov/32827126/
11. **PMID 21771959** — Thyroid imaging reporting and data system for US features of nodules: a step in establishing better stratification of cancer risk. *Radiology*, 2011. DOI: 10.1148/radiol.11110206 — https://pubmed.ncbi.nlm.nih.gov/21771959/

### 驗證研究（validation）

12. **PMID 28402167** — Multiinstitutional Analysis of Thyroid Nodule Risk Stratification Using the American College of Radiology Thyroid Imaging Reporting and Data System. *AJR. American journal of roentgenology*, 2017. DOI: 10.2214/AJR.16.17613 — https://pubmed.ncbi.nlm.nih.gov/28402167/
13. **PMID 39526062** — The Horizon of Thyroid Imaging Reporting and Data System in the Diagnostic Performance of Thyroid Nodules: Clinical Application and Future Perspectives. *TouchREVIEWS in endocrinology*, 2024. DOI: 10.17925/EE.2024.20.2.11 — https://pubmed.ncbi.nlm.nih.gov/39526062/
14. **PMID 32544875** — Performance of EU-TIRADS in malignancy risk stratification of thyroid nodules: a meta-analysis. *European journal of endocrinology*, 2020. DOI: 10.1530/EJE-20-0204 — https://pubmed.ncbi.nlm.nih.gov/32544875/
15. **PMID 32852733** — Thyroid imaging reporting and data system (TIRADS) for ultrasound features of nodules: multicentric retrospective study in China. *Endocrine*, 2021. DOI: 10.1007/s12020-020-02442-x — https://pubmed.ncbi.nlm.nih.gov/32852733/
16. **PMID 41695694** — Chinese thyroid imaging reporting and data system with redefined marked hypoechogenicity for thyroid malignancy risk stratification demonstrates improved diagnostic accuracy. *PeerJ*, 2026. DOI: 10.7717/peerj.20817 — https://pubmed.ncbi.nlm.nih.gov/41695694/

### 比較研究（comparison）

17. **PMID 30299457** — Reducing the Number of Unnecessary Thyroid Biopsies While Improving Diagnostic Accuracy: Toward the "Right" TIRADS. *The Journal of clinical endocrinology and metabolism*, 2019. DOI: 10.1210/jc.2018-01674 — https://pubmed.ncbi.nlm.nih.gov/30299457/
18. **PMID 31690937** — Performance of Five Ultrasound Risk Stratification Systems in Selecting Thyroid Nodules for FNA. *The Journal of clinical endocrinology and metabolism*, 2020. DOI: 10.1210/clinem/dgz170 — https://pubmed.ncbi.nlm.nih.gov/31690937/
19. **PMID 32303153** — Diagnostic Performance of Four Ultrasound Risk Stratification Systems: A Systematic Review and Meta-Analysis. *Thyroid : official journal of the American Thyroid Association*, 2020. DOI: 10.1089/thy.2019.0812 — https://pubmed.ncbi.nlm.nih.gov/32303153/
20. **PMID 31899594** — Can ultrasound systems for risk stratification of thyroid nodules identify follicular carcinoma? *Cancer cytopathology*, 2020. DOI: 10.1002/cncy.22235 — https://pubmed.ncbi.nlm.nih.gov/31899594/
21. **PMID 32959174** — The ultrasound risk stratification systems for thyroid nodule have been evaluated against papillary carcinoma. A meta-analysis. *Reviews in endocrine & metabolic disorders*, 2021. DOI: 10.1007/s11154-020-09592-3 — https://pubmed.ncbi.nlm.nih.gov/32959174/
22. **PMID 34777258** — Explore the Diagnostic Efficiency of Chinese Thyroid Imaging Reporting and Data Systems by Comparing With the Other Four Systems (ACR TI-RADS, Kwak-TIRADS, KSThR-TIRADS, and EU-TIRADS): A Single-Center Study. *Frontiers in endocrinology*, 2021. DOI: 10.3389/fendo.2021.763897 — https://pubmed.ncbi.nlm.nih.gov/34777258/
23. **PMID 37918114** — Diagnostic Performance of Thyroid Nodule Risk Stratification Systems: Comparison of ACR-TIRADS, EU-TIRADS, K-TIRADS, and ATA Guidelines. *Ultrasound quarterly*, 2023. DOI: 10.1097/RUQ.0000000000000653 — https://pubmed.ncbi.nlm.nih.gov/37918114/
24. **PMID 42306147** — Comparative Analysis of ACR TI-RADS and K-TIRADS: Inter-System Agreement and Diagnostic Performance Using a Single Study Cohort. *Journal of the Korean Society of Radiology*, 2026. DOI: 10.3348/jksr.2025.0054 — https://pubmed.ncbi.nlm.nih.gov/42306147/
25. **PMID 42344421** — Comparative diagnostic performance of C-TIRADS versus Kwak TI-RADS for thyroid nodules: implications for fine-needle aspiration biopsy referral. *Frontiers in endocrinology*, 2026. DOI: 10.3389/fendo.2026.1743112 — https://pubmed.ncbi.nlm.nih.gov/42344421/
26. **PMID 41258456** — ESR Essentials: thyroid imaging-practice recommendations by the European Society of Head and Neck Radiology. *European radiology*, 2026. DOI: 10.1007/s00330-025-12101-2 — https://pubmed.ncbi.nlm.nih.gov/41258456/

### 非期刊來源（官方文件，本次已下載核對）

- ACR TI-RADS 官方頁面：https://www.acr.org/Clinical-Resources/Clinical-Tools-and-Reference/Reporting-and-Data-Systems/TI-RADS （HTTP 200）
- `TI-RADS-Assessment-Categories.pdf`（ACR 官方計分 chart，HTTP 200）
- `TI-RADS-Assessment-Categories-Alternative-chart.pdf`（ACR 官方替代 chart，HTTP 200）
- `Sonographers-Worksheet-TI-RADS.pdf`（ACR 官方超音波技術師工作表，HTTP 200）
