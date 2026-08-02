# 進階甲狀腺及頸部超音波

**Advanced Thyroid and Neck Ultrasonography for Endocrine Fellows and Specialists**

給內分泌新陳代謝科 fellow 與專科醫師的進階甲狀腺及頸部超音波課程。
14 章、68 個單元、220 個病例與示範資源欄位。

> **不是入門課。** 假設你已經會掃、會量、知道基本術語。這門課處理的是**判讀落差**：
> 機器參數怎麼救回困難影像、ACR TI-RADS 與 ATA／EU／K-TIRADS 在同一顆結節上為什麼
> 給出不同答案、頸部淋巴結與術後甲狀腺床怎麼追、副甲狀腺與甲狀腺外病灶怎麼鑑別。

> **全部是影音。** 每一個資源欄位都是看得到的影片——YouTube、Vimeo、學會與醫院的
> 影音頻道，機構官方與個人專家頻道都收。期刊原文與指引 PDF 不佔資源欄位，
> 它們的位置在實證層的 `citations` 與 `GUIDELINE-MATRIX.md`。
>
> **每個網址都查得到來源。** 每個資源標示分級（Tier A/B/C）、存取條件、授權與**最後查核日期**；
> 每個論斷標示證據等級（7 級，含 `contested` 與 `educational_demo_only`）。
> 找不到合格資源的地方**誠實留空**並寫清楚查過什麼——留空比捏造一個看起來合理的連結誠實。

底層是 [`htlin222/gym-course`](https://github.com/htlin222/gym-course) 的 `curate-course`
框架（MIT）。原框架只認 YouTube；醫學教育資源散在學會、期刊、醫院教學站與病例圖譜，
所以本專案把「什麼算合法來源」抽成可插拔規則——見下方「框架適配」。

---

## 快速開始

需要 [uv](https://docs.astral.sh/uv/)。建置腳本只用 Python 標準庫。

```bash
git clone https://github.com/zinojeng/advanced-thyroid-echo.git
cd advanced-thyroid-echo

make build            # course/ → dist/
make serve            # http://localhost:8899
```

---

## 指令

```
make build            合併資料 → dist/，含配額驗證與 SEO 產出
make meta             用 yt-dlp 補齊 video-meta.json（真實長度、觀看數、頻道）
make audit            離線稽核（設定檔、配額、來源中繼資料完整性、實證深度），不打網路
make verify           重驗每個 YouTube 連結（oEmbed）與每個 PMID（PubMed API）
make verify-external  重驗每個非 YouTube 來源（HTTP 狀態、重導向、標題、登入牆）
make verify-content   用 Gemini 直接看影片，查核內容是否與課程宣稱相符（輔助訊號）
make check            lint + build + audit，提交前跑這個
make serve            本機預覽
make icons            重新打包 Lucide 圖示
make og               重新產生社群預覽圖
make counter          建立 D1 資料庫（瀏覽次數與影片評價共用，冪等可重跑）
make ratings          讀線上評價，印出建議換片的影片清單
make deploy           部署到 Cloudflare Pages
```

---

## 框架適配分析

原框架是為 YouTube 健身影片設計的。醫學教育課程的結構性差異，決定了哪些能沿用、
哪些必須改。

### A. 可直接沿用（未修改）

| 功能 | 為什麼能沿用 |
|---|---|
| 章節 → 單元 → 項目三層結構 | 課程結構本來就是這個形狀 |
| `course.config.json` 驅動全部 UI 文案 | 程式裡沒有寫死任何字，換主題只換設定檔 |
| 配額強制（`make build` 不符即失敗） | 防止「這章 40 個、那章 3 個」的失衡 |
| `make audit` 的離線稽核骨架 | 確定性檢查，可放進修正迴圈 |
| SEO：JSON-LD、OG、sitemap、robots、`llms.txt` | 與主題無關 |
| 前端：章節樹、全文搜尋、分面篩選、localStorage 進度、深淺色主題 | 與主題無關 |
| 上課模式的播放清單、欄寬拖曳、深連結、鍵盤快捷鍵 | 與主題無關 |
| `taxonomy/` 可插拔詞彙模組 | 介面是 `extract()` / `classify()`，不認識任何主題 |
| PubMed 引用驗證（`verify_refs.py`） | 醫學課程更需要 |
| Cloudflare Pages 部署 | 與主題無關 |
| giscus 每個資源一串討論 | 換 `repo` / `repoId` / `categoryId` 即可 |

### B. 只適用於 YouTube、必須改的部分

| 原本 | 問題 | 改法 |
|---|---|---|
| `build.py` 的 `YT` regex 硬性要求 `youtube.com/watch?v=` | 學會 PDF、期刊 DOI、Radiopaedia 條目全部會被判為「格式錯誤」 | 抽出 `src/build/sources.py`，改為 provider-aware 驗證 |
| `audit.py` 的「不是合法 YouTube 網址」錯誤 | 同上 | 改用 `sources.url_problem()` |
| `audit.py` 的 `metaCoverage` 分母含所有欄位 | 非 YouTube 來源沒有 oEmbed／yt-dlp 可查，永遠達不到 100% | 分母只算 YouTube 欄位 |
| `verify_links.py` 對所有 URL 打 oEmbed | 非 YouTube 網址會全部回失敗 | 只驗 YouTube，其餘交給新的 `verify_external.py` |
| `player.js` 一律嵌入 `youtube-nocookie.com` | 學會與期刊多半不允許嵌入 | 三段式：YouTube 嵌入 → 有 `embed_url` 就通用嵌入 → 否則顯示外連卡片 |
| `app.js` 只攔截 `a[href*="youtube.com"]` | 外部資源點了會直接跳走，看不到授權與存取說明 | 改攔 `a.VideoCard, a.Drill__link` |
| 前端沒有存取／授權／查核日期的顯示 | 醫學資源常需註冊或訂閱，不標示等於騙使用者點進去撞牆 | `render.js` 新增 `sourceBadges()` / `sourceFootnote()` |

### C. 非 YouTube 來源的支援方案

框架原本只認 YouTube。本課程雖然是純影音，影片仍然散在 Vimeo、學會自架播放器與
醫院教學站上，所以來源判定還是必須可插拔——只是多了一條「資源欄位必須是影音」的規則
（`audit.requireVideo`，違反即錯誤）。

`src/build/sources.py` 定義單一事實來源，`build` / `audit` / `verify_external` 三者共用：

```jsonc
{
  "provider":    "youtube | vimeo | society | hospital | external",
  "source_type": "video | webinar",          // 影音課程：只收這兩種
  "url":         "https://…",
  "embed_url":   "…",            // 有才嵌入，沒有就顯示外連卡片
  "embeddable":  true,            // 預設：youtube / vimeo 為 true，其餘 false
  "access":      "open | registration | subscription | institutional",
  "license":     "版權歸原機構，本站僅連結",
  "tier":        "A | B | C",
  "coi":         "廠商教育內容，講者受 <廠商> 支持",   // 選填
  "timestamps":  [{"at": "04:10", "note": "微鈣化與後方聲影的對照"}],
  "last_verified": "2026-08-02"
}
```

`provider` 沒寫就從網址推（YouTube / Vimeo 認得出來，其餘算 `external`）。

**非 YouTube 來源缺少 `source_type` / `access` / `license` / `last_verified` 任一個，
`make audit` 直接報錯。** 理由：YouTube 靠 oEmbed 就能程式化確認「存在且公開」，
其他來源沒有這種端點，只能靠策展時人工標示——所以標示是強制的。

`make verify-external` 對每個外部網址實際發出請求，記錄 HTTP 狀態、重導向鏈、最終網址、
網域、content-type、頁面 `<title>`、canonical URL 與**是否偵測到登入牆**，
寫進 `course/data/external-verify.json`。判讀規則：

- `200` → 通過（`--stamp` 可把 `last_verified` 更新為今天）
- `403` / `429` → 標為「需人工開一次確認」，多半是 WAF 擋 bot 而非連結失效
- `404` / `410` / 連線失敗 → 判為失效
- 偵測到登入牆但 `access` 標成 `open` → 列出來要求修正

`audit.verifyStaleDays`（本課程設 180）超過就警告，逼你定期重驗。

### D. 只在 `course/` 完成的改動

- 全部 14 章的策展資料（`course/data/ch*.json`）
- 站台設定、章節、配額、UI 文案、品質門檻（`course/course.config.json`）
- 詞彙模組：`taxonomy/lexicon.py`（影像特徵／疾病／解剖與分區／風險分層／處置與介入／技術，
  6 個分組、約 70 個正規化術語）與 `taxonomy/resources.py`（23 個資源類別）
- 實證資料（`course/data/drill-evidence-*.json`、`oe-*.json`）
- 搜尋紀錄（`course/data/registry-ch*.json`）

### E. 必須改 `src/` 的部分（最小幅度）

| 檔案 | 改動 |
|---|---|
| `src/build/sources.py` | **新增**。provider 推斷、URL 合法性、來源中繼資料完整性 |
| `src/build/verify_external.py` | **新增**。非 YouTube 連結驗證 |
| `src/build/build.py` | 移除硬編 YT regex，改呼叫 `sources`；輸出 `provider` / `embeddable` 與 provider 統計 |
| `src/build/audit.py` | provider-aware URL 檢查、來源中繼資料檢查、`metaCoverage` 分母修正、`last_verified` 過舊警告 |
| `src/build/verify_links.py` | 只驗 YouTube，並印出交給 `verify-external` 的數量 |
| `src/build/course.schema.json` | 新增 `audit.requireSourceMetadata`、`audit.verifyStaleDays` |
| `src/build/build_icons.py` | 換成本課程的章節圖示 |
| `src/web/js/render.js` | `sourceBadges()` / `sourceFootnote()`；留空文案改由設定檔提供 |
| `src/web/js/player.js` | 三段式播放；外連卡片 `externalCard()` |
| `src/web/js/app.js` | 攔截範圍從 YouTube 連結擴大到所有資源連結 |
| `src/web/css/player.css`、`course.css` | 外連卡片與來源標籤的樣式 |
| `Makefile` | 新增 `verify-external` |

**沒有動到**：`seo.py`、`filters.js`、`keys.js`、`discuss.js`、版面與主題樣式、
Cloudflare Pages 部署流程。原框架的 build／audit／verify／SEO／部署能力全部保留。

---

## `make verify-content`：連結活著，不代表影片拍了它宣稱的東西

`make verify` 只能證明連結還在、PMID 存在。這門課最難防的錯誤是另一種：
**連結是活的、標題也對，但影片內容不合格**——使用者曾回報一支「經皮喉部超音波」
只有對話討論沒有任何超音波影像；CH12 擴充時稽核也抓到「宣稱全片實機掃描、
實為投影片講座」與「片頭卡直接印出最終病理」。

`make verify-content` 用 Gemini 的多模態影片理解直接看影片，回答：

- 畫面裡有沒有**真正的超音波影像**（不是只有投影片、講者或動畫）
- 是**實機動態掃描**，還是貼在投影片上的靜態截圖
- 內容對不對得上課程宣稱的教學重點
- 前 10 秒有沒有片頭卡劇透（有的話建議 `start` 秒數）
- 旁白語言、有沒有大段商業推銷

```bash
make verify-content                                # 有快取，只查新的或 last_verified 變過的
make verify-content ARGS="--only ch12 --limit 5"
make verify-content ARGS="--dry-run"               # 只列出這次會查哪幾支
```

報告寫在 `course/data/content-verify.json`。需要 `.env` 的 `GEMINI_API_KEY`；
沒有金鑰就印一行說明後正常結束，不會擋住 `make`。

**這是輔助訊號，不是判決。** 模型會看錯——最常見的是分不清「投影片上貼的靜態
超音波截圖」與「實機動態掃描」，也可能把解剖動畫當成超音波畫面；同一支影片重跑
結果可能不一樣。被標記的影片一律要**人工開影片確認**後再決定換片或補 `start`，
這支腳本刻意**不會自動改動任何課程資料**。

成本參考：一支影片約 9–10 萬 tokens，257 支跑一輪約 2,600 萬 tokens
（gemini-2.5-flash 約 US$8）。所以預設有快取，不要無意義地全量重跑。

---

## 影片評價：讓使用者的判斷變成換片清單

每支影片除了討論串，還有一個 1–5 分的評價。重點不在平均分，在**低分時追問原因**：

> 只有講解／對話，沒有實際超音波影像 · 影像太模糊 · 內容與這個單元不符 ·
> 用了過時的分類或做法 · 對 fellow 來說太基礎

理由很簡單：只有分數的低分對策展沒有用。知道某支片不好卻不知道哪裡不好，
換片時等於把使用者已經看出來的事再猜一次。所以**低分才問標籤，高分不問**——
每次都要選標籤會讓人懶得評。

```bash
make ratings
```

```
■ 建議換片 1 支（低分且有具體原因）
  1.5／5（2 票）  https://www.youtube.com/watch?v=…
      掛在 CH2 ch2-u1 · 資源：看不到神經，但看得到聲帶：經皮喉部超音波
      → 只有講解／對話，沒有實際超音波影像（2 人）
```

低分但**沒有**原因標籤的只列在「待觀察」，不進必換清單——不足以決定換成什麼。
門檻是平均 ≤ 2 且至少 3 票（`MIN_VOTES` 可調），避免單一使用者決定策展。

### 使用者寫的文字怎麼到你手上

點「差」或「內容有錯」時會多出一個**選填文字欄**。只有標籤的話，
你知道某支片有問題卻不知道哪裡有問題——文字才是換片時真正需要的東西。

**文字不會顯示在網站上。** 匿名文字公開顯示等於開一個沒人管的留言板，
而這門課沒有帳號系統也沒有審核流程。它只走 `/api/feedback`，要帶
`FEEDBACK_TOKEN` 才讀得到。

```bash
make feedback                    # 印出摘要（上次讀到哪之後的新回饋）
make feedback ARGS="--since 7d"
make feedback ARGS="--post"      # 開一則 GitHub Issue → GitHub 自動寄信通知你
```

`--post` 用 GitHub Issue 當送信管道，是為了**不再多接一個寄信服務、不再多存一組金鑰**：
repo 已經開了 Issues，GitHub 本來就會把新 Issue 寄到維護者信箱，
而且順便留下公開可討論的紀錄，其他人看得到也能回覆。

刻意**不做「每則寄一封信」**——單則通知很快變成噪音，看幾天就開始忽略，
忽略掉的通知等於沒有通知。

設定（兩邊要同一個值）：

```bash
openssl rand -hex 24                                   # 產生
echo 'FEEDBACK_TOKEN=<值>' >> .env                      # 本機
npx wrangler pages secret put FEEDBACK_TOKEN --project-name thyroid-us
```

**這個評價機制的誠實說明**：voter 是瀏覽器端產生的隨機 token，存在 localStorage。
這**不是身分驗證**——清掉瀏覽器資料就能再投一次。它擋的是誤觸與同一個人連按，
不是有意灌票。要防灌票需要真正的登入，而這門課刻意不做帳號系統。
評價因此是**參考訊號，不是投票結果**；換片前仍應自己打開影片確認。

沒有綁 D1 時 `/api/rate` 一律回 503，評價區塊安靜地不顯示——
寧可沒有這個功能，也不要在頁面上留一個壞掉的空殼。

---

## 網站有什麼

四個檢視：**首頁**（用法、立場摘要、章節總覽）· **課程內容**（章節樹、驗收方式、
分面標籤、資源清單、證據註記）· **上課模式**（左側播放或外連卡片、右側清單，
欄寬可拖曳、`?tab=player&play=12` 深連結）· **立場**（課程對自身限制的說明與原始文獻）。

每個資源顯示：**Tier 分級 · 來源平台 · 存取條件 · 資源類型 · 利益關係 ·
授權 · 最後查核日期**。不可嵌入的來源不會偷偷跳走，而是先給你一張卡片說明
存取條件與授權，再由你決定要不要連出去。

---

## 交付文件

| 檔案 | 內容 |
|---|---|
| [`COURSE-PLAN.md`](COURSE-PLAN.md) | 受眾、章節、68 個單元、配額與理由、預估時數 |
| [`COMPETENCY-FRAMEWORK.md`](COMPETENCY-FRAMEWORK.md) | 42 條 fellow 能力、畢業標準、對應驗收方式 |
| [`SEARCH-METHODOLOGY.md`](SEARCH-METHODOLOGY.md) | 資料庫、網站、query matrix、語言、納入／排除標準、驗證程序 |
| [`GUIDELINE-MATRIX.md`](GUIDELINE-MATRIX.md) | ACR／ATA／EU／K-TIRADS 逐項比較與系統間不一致 |
| [`COPYRIGHT-AND-PRIVACY-AUDIT.md`](COPYRIGHT-AND-PRIVACY-AUDIT.md) | 著作權處理原則、授權標示規則、患者隱私、稽核結果 |
| [`KNOWN-GAPS.md`](KNOWN-GAPS.md) | 誠實列出找不到資源的主題、僅有付費內容的主題、證據不足處、仍需專家審查處 |
| [`SOURCE-REGISTRY.json`](SOURCE-REGISTRY.json) | 所有評估過的來源與納入／排除理由 |
| [`docs/CURATION-BRIEF.md`](docs/CURATION-BRIEF.md) | 各章策展 agent 共用的契約 |
| [`docs/CASE-FORMAT.md`](docs/CASE-FORMAT.md) | 病例模組的 11 步固定格式 |
| [`docs/assessments/`](docs/assessments/) | 前測 30 題、各章 quiz、後測 50 題、10 站 OSCE、procedure／reporting checklist、fellow logbook |

---

## 免責聲明

本課程為**醫學教育內容，不構成對特定病人的診斷或治療建議**，也不能取代當地的
credentialing、supervision、感染控制與法規要求。課程中的「證據強度」註記附上原始文獻或
指引連結，反映的是**查核當下**的狀態；指引會改版，請以最新原文為準。
任何介入操作都應在具備資格的督導下、於符合規範的場域執行。

**所有影音與病例為原機構、期刊或創作者的作品，版權歸原權利人所有。**
本站只做策展、查核與連結，**不下載、不剪輯、不重新散布，也不代管任何患者影像。**

---

## 授權

框架與課程結構程式碼採 MIT，見 [LICENSE](LICENSE)。
框架衍生自 [htlin222/gym-course](https://github.com/htlin222/gym-course)（MIT）。
Lucide 圖示為 ISC。連結指向的內容不在本專案授權範圍內。
