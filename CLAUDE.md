# CLAUDE.md

給在這個 repo 工作的 Claude Code。**先讀這一份，再動手。**

---

## 這是什麼專案

一門線上影音課程：**進階甲狀腺及頸部超音波**，受眾是內分泌新陳代謝科 fellow
與已取得專科資格的醫師。14 章、68 個單元、288 個資源欄位。

- 線上：<https://thyroid-us.pages.dev>
- Repo：`zinojeng/advanced-thyroid-echo`
- 框架衍生自 [`htlin222/gym-course`](https://github.com/htlin222/gym-course)（MIT）

原始需求規格在 `docs/BRIEF.md`——**改任何東西之前先確認沒有違反那份規格**，
特別是第十八節「不得接受的產出」。

---

## 不可協商的三條

這三條是整個專案的價值所在。違反其中任何一條，這門課就不值得存在。

### 1. 不得憑記憶生成任何識別碼

video ID、PMID、DOI、網址——**一律取自實際的搜尋結果或 API 回應**。
捏造一個看起來合理的 ID，比留空糟一百倍。

```bash
# YouTube：ID 只能從這裡來
yt-dlp "ytsearch20:<query>" --flat-playlist --no-update \
  --print "%(id)s|%(title)s|%(channel)s|%(duration)s|%(view_count)s"
curl -s "https://www.youtube.com/oembed?url=<URL編碼>&format=json"

# 文獻：title/journal/year 一律照抄 esummary 回傳值
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=<PMID>"
```

### 2. 找不到就留空，並寫清楚查過什麼

```json
{ "url": null, "note": "查過 <query 1>、<query 2>…；候選 N 支不合格，原因：…" }
```

留空而沒有 `note` 會被 `make audit` 判為錯誤。**留空比硬塞不對題的內容好。**

### 3. 不信任任何上游宣稱，包括自己剛才說驗過的

交付前一定跑 `make verify`。這是最後一道關卡。

---

## 每次改完課程資料必跑

```bash
make check        # lint + build + audit（離線，秒回）
make verify       # 重打 YouTube oEmbed 與 PubMed API
```

`make check` 必須**零錯誤**才算完成。警告要逐條看過並能說明為什麼接受。

---

## 專案特有的規則

### 這是純影音課程

**每個資源欄位都必須是可以看的影片。** 期刊原文與指引 PDF 不佔資源欄位，
它們的位置在實證層（`drill-evidence-*.json` / `oe-*.json` 的 `citations`）
與 `GUIDELINE-MATRIX.md`。

`source_type` 只能是 `video` 或 `webinar`，違反會被 `audit.requireVideo` 擋下。

### oEmbed 證明不了影片拍了什麼

使用者曾回報一支「經皮喉部超音波」影片**只有對話討論、沒有任何超音波影像**。
連結是活的、標題也對，但內容不合格——這類錯誤自動化查核抓不到。

選片時務必看描述與章節確認真的有動態掃描：

```bash
yt-dlp --no-update --skip-download --print "%(description)s" "<url>"
```

站上的**影片評價**（`make ratings`）就是為了接住這類問題而做的。

### provider 是託管平台，不是發布機構

學會把影片放上 YouTube，`provider` 仍然是 `youtube`，發布機構寫在 `channel`。
標錯會讓那支影片從 oEmbed 驗證漏掉，改由外部驗證器去打 youtube.com 然後撞 429,
看起來像死連結。`sources.py` 現在會擋這種標錯。

### 單色調 UI

色相這個維度已經整個拿掉，只留一條 13 階中性色 `--ink-0`…`--ink-12`。
語意層級用**明度與填滿程度**編碼，不要為了「強調」而引入新顏色。

分類圓點用 `--dotColor-*`，**不要**用 `--fgColor-<tone>`——
後者在單色調下是反白字色，畫在淺色底上會消失。

### 醫學內容的紅線

- 不得宣稱超音波可以單獨確定組織型別
- 不得把 AI／elastography／CEUS 的研究成果講成標準照護
- 不得把單一 TI-RADS 當成全球唯一標準；指引不一致要用比較表呈現
- 不得暗示公開影音可以取代 credentialing、supervision 或感染控制規範
- 誠實比好看重要：證據薄弱就標 `limited` / `contested`，即使對課程不利

---

## 目錄與職責

```
course/                    ← 課程內容，多數改動只會動到這裡
  course.config.json       站台設定、章節配額、品質門檻、所有 UI 文案
  data/ch*.json            各章策展資料（一章一檔）
  data/registry-ch*.json   搜尋紀錄：評估過的來源與納入／排除理由
  data/oe-*.json           單元層級實證
  data/drill-evidence-*.json  類別層級實證
  taxonomy/lexicon.py      影像特徵／疾病／分區／系統的分面標籤
  taxonomy/resources.py    資源分類（讓文獻掛在類別上）
src/build/                 建置與查核工具
  sources.py               provider 判定、URL 合法性、影音判定 ← 規則的單一事實來源
  build.py / audit.py / seo.py
  verify_links.py          YouTube oEmbed
  verify_refs.py           PubMed 引用
  verify_external.py       非 YouTube 連結（目前課程全是 YouTube，備而不用）
  ratings.py / gaps.py / merge_registry.py
src/web/                   前端（css / js / index.html）
functions/                 Cloudflare Pages Functions（瀏覽次數、影片評價）
docs/                      BRIEF、策展契約、病例格式、評量題庫
```

**程式裡不寫死任何文案。** 所有顯示文字都從 `course.config.json` 讀。

---

## 常用指令

```
make build            course/ → dist/，配額不符直接失敗
make check            lint + build + audit，提交前跑這個
make verify           重驗 YouTube 連結與 PubMed 引用
make meta             用 yt-dlp 補齊影片長度／觀看數／頻道
make ratings          讀線上評價，印出建議換片清單
make gaps             列出誠實留空的欄位與證據不足的主題
make registry         合併搜尋紀錄成 SOURCE-REGISTRY.json
make og               重新產生社群預覽圖（Chrome headless + sips）
make deploy           部署到 Cloudflare Pages
```

部署需要環境變數 `CLOUDFLARE_API_TOKEN` 與 `CLOUDFLARE_ACCOUNT_ID`。
**推 GitHub 不會更新網站**，要另外跑 `make deploy`。

---

## 改配額的注意事項

章節配額寫在 `course.config.json` 的 `chapters[]`（`units` 與 `drills`）。
`make build` 會強制檢查，數字不符直接失敗。改配額時要同步更新：

- `COURSE-PLAN.md` 的章節表與單元清單
- `README.md`、`KNOWN-GAPS.md` 裡引用的總數
- `src/web/og.html` 的數字（靜態模板，不會自動跟著變）
- `hero.lede` / `landing.ctaLede` 的佔位符文案

---

## 平行策展的教訓

多個 agent 同時策展時，**每個 agent 給獨立的輸出檔**，最後由主流程合併。
共用一個檔一定會互相覆蓋。暫存檔也要各給一個子目錄。

YouTube 在短時間內大量請求後會限流，而且 **yt-dlp 在限流下會回傳部分資料
（有標題有觀看數但沒有長度）而不是直接失敗**。`build.py` 遇到 `seconds=0`
會保留策展時的長度，不用 `0:00` 覆蓋——不要把這個保護拿掉。

---

## 目前狀態

見 `PROGRESS.md`。已知缺口與仍需人工審查的部分見 `KNOWN-GAPS.md`——
**那份文件是這個專案誠實性的一部分，不要為了讓數字好看而修改它。**
