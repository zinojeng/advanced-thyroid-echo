# 策展契約（所有章節 agent 共用）

每個章節由獨立 agent 策展，但必須共用同一套 metadata schema、品質門檻、證據分級、
去重規則與術語規則。這份檔案就是那套規則。**不符合這裡的規定，`make audit` 會擋下來。**

---

## 鐵則

1. **策展不是生成。** YouTube video ID 一律取自 `yt-dlp` 實際搜尋結果；外部網址一律取自
   實際打開過的頁面。**憑記憶拼湊一個看起來合理的 ID 或網址，比留空糟一百倍。**
2. **留空要說明。** 找不到合格資源就 `"url": null` 加 `"note"`，寫清楚查過哪些 query、
   哪些來源、為什麼都不合格。留空而沒有 note 會被稽核判為錯誤。
3. **不信任任何上游宣稱**，包括自己剛才說已經驗證過的。每一個連結都要實際打過。
4. **誠實比好看重要。** 查證結果對課程不利就照實寫。
5. **不得下載、剪輯或重新上傳任何影片。** 只存連結與公開中繼資料。
6. **不得使用可識別患者資料。** 看到有姓名、病歷號、生日的影像，直接排除。

---

## 受眾

內分泌新陳代謝科 fellow 與已取得專科資格的醫師。**假設他們已經會掃、會量、知道基本術語。**

所以：

- ❌ 不要收「什麼是甲狀腺超音波」「探頭怎麼拿」這種入門內容（CH0 的複習單元除外）。
- ✅ 要收判讀落差、指引比較、困難病例、操作細節、陷阱與爭議。

---

## 資料格式

寫進 `course/data/chN.json`：

```json
{
  "chapter": "CH4",
  "title": "結節描述語言與風險分層",
  "units": [{
    "id": "ch4-u1",
    "name": "單元名稱（繁體中文，保留必要英文術語）",
    "type": "lexicon",
    "assessment": "至少 80 字、fellow 自己就能執行的驗收方式。",
    "tight": ["這個單元最容易誤判的地方 A", "B"],
    "weak": ["本單元必須練成的判讀能力 A", "B"],
    "lesson": {
      "title": "資源原標題（照抄，不要翻譯）",
      "channel": "頻道或發布機構",
      "url": "https://…",
      "duration": "18:42",
      "why": "為什麼選這個當核心教材（1–2 句，要講出它解決什麼判讀落差）",
      "tier": "A",
      "source_type": "video",
      "provider": "youtube",
      "access": "open",
      "license": "版權歸原頻道，本站僅連結",
      "last_verified": "2026-08-02"
    },
    "drills": [{
      "name": "資源名稱（繁中）",
      "en": "English title if any",
      "kind": "case",
      "target": "教學重點：這個資源要學員看出什麼",
      "dose": "建議怎麼用（例如「先自己分級再看解答」或「重點在 04:10–09:30」）",
      "title": "…", "channel": "…", "url": "https://…", "duration": "12:03",
      "tier": "B", "source_type": "case", "provider": "case_library",
      "access": "open", "license": "…", "last_verified": "2026-08-02",
      "timestamps": [{"at": "04:10", "note": "微鈣化與後方聲影的對照"}]
    }]
  }]
}
```

### 欄位規則

| 欄位 | 規則 |
|---|---|
| `type` | 只能用 `scan` / `anatomy` / `disease` / `lexicon` / `procedure` / `case` / `quality` / `assessment` |
| `kind` | 只能用 `case` / `procedure` / `atlas` / `guideline` / `lecture` |
| `tier` | `A` 核心教材 · `B` 病例補充 · `C` 技術示範。定義見下 |
| `provider` | `youtube` / `vimeo` / `society` / `journal` / `hospital` / `case_library` / `external` |
| `source_type` | `video` / `webinar` / `case` / `atlas` / `guideline` / `article` / `quiz` |
| `access` | `open` / `registration` / `subscription` / `institutional` |
| `license` | 一句話寫清楚版權狀態。**不確定就寫「授權狀況未確認，僅連結不重製」** |
| `last_verified` | `YYYY-MM-DD`，你實際打開連結那天 |
| `coi` | 選填。廠商內容、講者與廠商有關係一定要寫 |
| `duration` | `分:秒` 或 `時:分:秒`。非影片資源（指引 PDF、圖譜頁）省略 |

**非 YouTube 來源缺少 `source_type` / `access` / `license` / `last_verified` 任何一個，
`make audit` 會直接報錯。**

`assessment` 必須是**可操作的**，例如：

> 找三顆自己門診的結節，各寫一段 structured description，再分別以 ACR TI-RADS 與
> K-TIRADS 分級；記錄兩個系統給出不同穿刺建議的比例，並說明差異來自哪一個影像特徵。

不得寫「了解本主題」「熟悉相關知識」。

---

## 品質分級

**Tier A（核心教材）** — 正式學會、大學、醫學中心或公認專家；內容完整、影像清楚、
與現行指引一致、有明確教學目的。可作為單元主課。

**Tier B（病例補充）** — 特殊或少見病例，影像價值高，但內容不夠完整或缺乏正式證據討論。
僅作補充，不作唯一依據。

**Tier C（技術示範）** — 掃描、穿刺或機器操作示範。必須另外搭配正式文獻與安全說明。

### 一律排除

- 無法確認作者或來源
- 影像過度模糊、沒有實際動態掃描（只有口頭演講、只有投影片）
- 明顯錯誤，或把單一病例當成普遍規則
- 缺乏利益揭露的高度商業宣傳
- 使用過時分類卻未說明版本
- 未經授權重新上傳的完整付費課程
- 只有吸睛標題、沒有可用教學影像
- 宣稱超音波可以取代病理或完整臨床判斷
- 含可識別患者資訊

設備廠商內容**可以**收作操作教學，但必須填 `coi`，且不得把產品宣傳當成臨床證據。

---

## 來源優先順序

**第一級**：ATA、ETA、ACR、KSThR（大韓甲狀腺影像醫學會）、AIUM、RSNA、SRU、EFSUMB、
WFUMB、Endocrine Society、各國甲狀腺／內分泌／放射／超音波學會、大學醫院與 fellowship program。

**第二級**：PubMed 文獻與期刊 supplementary video、Radiology／AJR／European Radiology／
Thyroid／JCEM、Radiopaedia 等專業影像病例庫、學術會議錄影與 webinar、正式 CME 課程。

**第三級**：YouTube、Vimeo、專業醫療網站內嵌影片、醫院教學平台、設備廠商進階教育內容。

**每一章至少要有 2 個非 YouTube 的第一或第二級來源。** 這門課不是 YouTube 播放清單。

---

## 搜尋語言

英文為主。K-TIRADS、韓國介入教學可用韓文；日本超音波教育資源可用日文；
臺灣、香港與華語臨床教學用中文。非英文資源只有在**影像示範價值高**且
**可由英文來源交叉驗證**時才納入，並在 `why` 註明語言與是否有字幕。

---

## 驗證方式（必做，不可省略）

### YouTube

```bash
# 搜尋——ID 從這裡來，不可自己拼
yt-dlp "ytsearch20:<查詢>" --flat-playlist --no-update \
  --print "%(id)s|%(title)s|%(channel)s|%(duration)s|%(view_count)s"

# 驗證存在且可嵌入
curl -s "https://www.youtube.com/oembed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D<ID>&format=json"
```

200 + 標題頻道相符 = 存在且公開。401/403/404 = 不可用，換一支。

### 非 YouTube

```bash
curl -sL -o /dev/null -w "%{http_code} %{url_effective} %{content_type}\n" "<URL>"
```

需要看標題與是否有登入牆時，抓回 HTML 看 `<title>` 與頁面文字。
**200 才算數；403 要人工判斷是 bot 防護還是真的擋。**

---

## 去重規則

- 同一個 URL **不得**在同一單元內出現兩次。
- 跨單元共用最多 30 支，能不共用就不共用。
- 交付前用 `sort | uniq -d` 檢查自己章節內的 URL。

---

## 術語規則

- 網站文字以**繁體中文**為主，保留必要英文醫學術語（TI-RADS、FNA、extrathyroidal
  extension、taller-than-wide 這類不要硬翻）。
- 資源的 `title` 照抄原文，不要翻譯。
- 分類系統一律寫全名與版本（`ACR TI-RADS (2017)`、`ATA 2015`、`EU-TIRADS 2017`、
  `K-TIRADS 2021`），不要只寫「TI-RADS」。

---

## 同時要交的搜尋紀錄

另外寫一份 `course/data/registry-chN.json`，記錄**所有評估過的來源**（含排除的）：

```json
{
  "chapter": "CH4",
  "searched": ["用過的 query 1", "query 2"],
  "evaluated": [
    {"title": "…", "url": "https://…", "source": "YouTube / ATA / Radiopaedia",
     "decision": "included" , "unit": "ch4-u1", "reason": "…"},
    {"title": "…", "url": "https://…", "source": "…",
     "decision": "excluded", "reason": "只有投影片沒有動態掃描"}
  ]
}
```

這份會併成 `SOURCE-REGISTRY.json`，是「查得到來源」這件事的底稿。
