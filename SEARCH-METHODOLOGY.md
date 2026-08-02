# 搜尋方法學

這份文件記錄課程資源是**怎麼找到的**、**用什麼標準納入或排除**、以及**怎麼驗證**。
目的是讓任何人都能重跑同一套搜尋、得到可比較的結果——包括發現我們漏掉了什麼。

搜尋執行日期：**2026-08-02**（所有 `last_verified` 欄位的基準日）

---

## 一、搜尋來源

### 資料庫與 API

| 來源 | 用途 | 存取方式 |
|---|---|---|
| PubMed / MEDLINE | 文獻查證、PMID 取得、指引原文定位 | E-utilities（`esearch` / `esummary` / `efetch`） |
| PubMed Central | 全文核對分類門檻與數字 | `https://www.ncbi.nlm.nih.gov/pmc/` |
| doi.org | DOI 解析與最終網址確認 | `curl -sL` |
| YouTube | 第三級影音來源 | `yt-dlp ytsearch` + oEmbed API |

**不使用**任何搜尋引擎排名作為納入依據。搜尋結果只是候選池，納入與否一律看內容。

### 網站（第一級：專業學會與學術機構）

American Thyroid Association、European Thyroid Association、American College of Radiology、
Korean Society of Thyroid Radiology、American Institute of Ultrasound in Medicine、
Radiological Society of North America、Society of Radiologists in Ultrasound、
European Federation of Societies for Ultrasound in Medicine and Biology、
World Federation for Ultrasound in Medicine and Biology、Endocrine Society、
其他國家級甲狀腺／內分泌／放射／超音波學會、大學醫院與正式 fellowship program。

### 網站（第二級：同儕審查教育來源）

Radiology、AJR、European Radiology、Thyroid、JCEM、Korean Journal of Radiology、
European Thyroid Journal、Journal of the American College of Radiology 等期刊；
期刊 supplementary video；Radiopaedia 等專業影像病例庫；
學術會議錄影、webinar、grand round；專科醫學會的 case conference；正式 CME 課程。

### 網站（第三級：高品質公開影音）

YouTube、Vimeo、專業醫療網站內嵌影片、醫院教學平台、超音波設備廠商的進階教育內容。

設備廠商內容的處理規則：可以納入**操作教學**，但（一）不得直接把產品宣傳視為臨床證據，
（二）必須在 `coi` 欄位標示廠商利益關係，（三）診斷與治療主張仍須以指引或同儕審查文獻查核。

---

## 二、搜尋語言

| 語言 | 角色 | 納入條件 |
|---|---|---|
| 英文 | 主要搜尋語言 | 無額外條件 |
| 韓文 | K-TIRADS、甲狀腺介入與病例教學 | 需符合下述非英文條件 |
| 日文 | 日本甲狀腺與超音波教育資源 | 同上 |
| 中文（繁／簡） | 臺灣、香港及華語臨床教學 | 同上 |
| 其他歐洲語言 | 必要時（義大利的消融教學、法國的 EU-TIRADS 教材） | 同上 |

**非英文資源的納入條件**（四項全部滿足才收）：

1. 影像示範價值高
2. 可取得英文字幕、自動字幕或可靠摘要
3. 影片內容可由其他英文來源交叉驗證
4. 課程頁面提供繁體中文重點說明

網站文字以**繁體中文**為主，保留必要英文醫學術語（TI-RADS、FNA、extrathyroidal
extension、taller-than-wide 等不硬翻）。資源標題一律照抄原文，不翻譯。

---

## 三、Query matrix

每個單元建立可重複的 query matrix，由下列元素組合：

| 軸 | 值 |
|---|---|
| 主題名稱 | thyroid / neck / nodule / lymph node / parathyroid… |
| 同義詞 | ultrasound / sonography / ultrasonography / echography / 超音波 / 초음파 / 超音波検査 |
| Disease-specific terms | Hashimoto、Graves、papillary carcinoma、medullary carcinoma、lymphoma… |
| 形式 | case / lecture / webinar / grand rounds / how I scan / tutorial |
| 深度 | pitfall / pearls / advanced / fellowship / difficult / challenging |
| 對照 | pathology correlation / cytology correlation / surgical correlation |
| 處置 | FNA / biopsy / washout / ablation / active surveillance |
| 來源 | 學會或醫院名稱（ATA、AIUM、RSNA、Mayo、MD Anderson、Seoul National…） |

### 實際使用的核心 query（每章另有擴充，記錄在 `course/data/registry-ch*.json`）

```
thyroid ultrasound advanced lecture
thyroid sonography fellowship curriculum
difficult thyroid nodule ultrasound cases
thyroid ultrasound pitfalls webinar
cervical lymph node mapping thyroid cancer
postoperative thyroid bed ultrasound recurrence
intrathyroidal parathyroid adenoma ultrasound
Hashimoto pseudonodule ultrasound
thyroid FNA needle visualization
ultrasound pathology correlation thyroid carcinoma
ACR TI-RADS how to score
K-TIRADS versus ACR TI-RADS comparison
thyroid ultrasound knobology optimization
shear wave elastography thyroid nodule
contrast enhanced ultrasound thyroid
deep learning thyroid nodule external validation
```

完整的 query 清單與每一筆評估結果（含排除理由）記錄在
`course/data/registry-ch*.json`，合併輸出為 `SOURCE-REGISTRY.json`。

---

## 四、納入標準

> **2026-08-02 改版：資源欄位一律只收影音。**
> 期刊原文、指引 PDF 與病例圖譜網頁不再佔用資源欄位，改列在實證層的 `citations`
> 與 `GUIDELINE-MATRIX.md`。`source_type` 只能是 `video` 或 `webinar`，
> 違反會被 `make audit`（`requireVideo`）判為錯誤。
> 機構官方頻道與個人專家頻道**同等接受**，判準是作者可確認、影像品質足夠、內容正確。


每個資源至少記錄下列欄位（實際 schema 見 `docs/CURATION-BRIEF.md`）：

title、speaker／channel、institution、URL、platform（`provider`）、publication date、
access date（`last_verified`）、duration、language、subtitle availability、
resource type（`source_type`）、target level（`tier`）、topic tags（由 `taxonomy/lexicon.py`
自動抽取）、why selected（`why`）、key teaching points（`target`）、
recommended timestamps（`timestamps`）、conflicts of interest（`coi`）、
access status（`access`）、embedding status（`embeddable`）、
copyright／license note（`license`）、verification status、last verified date。

### 品質分級

| Tier | 定義 | 用途 |
|---|---|---|
| **A** | 正式學會、大學、醫學中心或公認專家；內容完整、影像清楚、與現行指引一致、有明確教學目的 | 可作為單元主要教材 |
| **B** | 特殊或少見病例，影像價值高，但內容不夠完整或缺乏正式證據討論 | 僅作補充，不作唯一依據 |
| **C** | 掃描、穿刺、機器操作或 procedure demonstration | 必須另外搭配正式文獻與安全說明 |

### 檢查項目（搜尋時逐項確認，不看排名）

影片內容 · 作者身分 · 上傳機構 · 日期 · 是否過時 · 是否有廣告或商業偏誤 ·
是否真正包含動態掃描 · 影像解析度是否足夠 · 是否只是口頭演講而沒有實際影像 ·
是否能合法連結或嵌入。

---

## 五、排除標準

一律排除：

- 無法確認作者或來源
- 影像過度模糊
- 明顯錯誤
- 把單一病例當成普遍規則
- 缺乏利益揭露的高度商業宣傳
- 使用過時分類卻未說明版本
- 無法確認網址真實存在
- 未經授權重新上傳的完整付費課程
- 只有吸睛標題、沒有可用教學影像
- 宣稱超音波可以取代病理或完整臨床判斷
- 含可識別患者資訊（姓名、病歷號、生日、可辨識面容）

---

## 六、驗證程序

品質是**三道獨立關卡**，缺一不可。

| | `make audit` | `make verify` | `make verify-external` |
|---|---|---|---|
| 打不打網路 | 不打 | 打 YouTube oEmbed 與 PubMed | 打每一個外部網址 |
| 回答什麼 | 這批資料自己內部一致嗎 | YouTube 連結與 PMID 真的存在嗎 | 學會／期刊／醫院的連結還活著嗎 |
| 何時跑 | 每寫完一章 | 交付前、部署前 | 交付前、部署前 |

### YouTube

```bash
# 搜尋——video ID 只能從這裡來
yt-dlp "ytsearch20:<query>" --flat-playlist --no-update \
  --print "%(id)s|%(title)s|%(channel)s|%(duration)s|%(view_count)s"

# 驗證存在且可嵌入
curl -s "https://www.youtube.com/oembed?url=<URL編碼的watch網址>&format=json"
```

200 + 標題頻道相符 = 存在且公開；401/403/404 = 已刪除、設為私人或不允許嵌入。

長度、觀看數與頻道名以 `make meta`（yt-dlp）抓回的實際值為準，
覆寫策展時抄下來的數字；`make audit` 會檢查兩者的誤差是否超過 45 秒。

### 非 YouTube

`src/build/verify_external.py` 對每個外部網址實際發出請求，記錄：

HTTP status · 重導向鏈 · 最終網址 · 網域 · content-type · 頁面 `<title>` ·
canonical URL · 是否偵測到登入牆 · 查核日期

判讀規則：

- **200** → 通過，可 `--stamp` 更新 `last_verified`
- **403 / 429** → 標為「需人工開一次確認」，多半是 WAF 擋 bot 而非連結失效
- **404 / 410 / 連線失敗** → 判為失效，必須換掉或改為 `url: null` + `note`
- **偵測到登入牆** → 通過，但課程頁面必須把 `access` 標成
  `registration` / `subscription` / `institutional`

### 文獻

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&term=<query>"
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=<PMIDs>"
```

`title` / `journal` / `year` **一律照抄 esummary 回傳值**。
`make verify` 會重打 esummary 比對每一筆宣稱的標題是否對得上 PMID。

---

## 七、找不到合格資源時

```json
{
  "url": null,
  "note": "查過 <query 1>、<query 2>、<來源 A>、<來源 B>；候選 N 支全部不合格，原因：…"
}
```

**留空比捏造更好。** 留空而沒有 `note` 會被 `make audit` 判為錯誤。
所有留空的欄位彙整在 `KNOWN-GAPS.md`。

不得憑記憶生成 video ID、PMID、DOI 或網址——**這是本專案唯一不可協商的規則。**

---

## 八、去重規則

- 同一 URL 不得在同一單元內重複出現（`make build` 會直接失敗）
- 跨單元共用上限 30 支（`audit.maxSharedVideos`），超過視為內容重疊過多
- 多語言替代版本（`alt-lessons-*.json`）會被驗證與補中繼資料，但**不計入課程總時長**

---

## 九、這份方法學的限制

1. **搜尋深度受限於公開可及性。** 需要付費、機構帳號或會員資格的高品質內容
   （多數學會的完整 CME 課程）只能標示存取條件並連結，無法評估其內容品質。
2. **YouTube 搜尋有地區與個人化偏差。** `yt-dlp ytsearch` 的結果不保證與他人執行時完全相同。
3. **非英文資源的評估仰賴字幕與交叉驗證**，可能低估了沒有英文字幕的優質教材。
4. **「查核日期」只證明那天連結是活的**，不保證內容從此不變。`audit.verifyStaleDays`
   設為 180 天，超過會發出警告要求重跑 `make verify-external`。
5. 本方法學處理的是**資源的可查證性**，不是**內容的臨床正確性**。後者需要領域專家人工審查，
   仍待完成的部分列在 `KNOWN-GAPS.md`。
