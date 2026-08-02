# 任務：建個由下列角色共同組成的專業團隊：

1. 內分泌新陳代謝科專科醫師
2. 甲狀腺與頸部超音波專家
3. 頭頸部放射科醫師
4. 甲狀腺細針穿刺與介入超音波專家
5. 醫學教育課程設計師
6. 系統性文獻搜尋與影音策展研究員
7. 靜態網站、GitHub 與 Cloudflare Pages 工程師
8. 醫療內容查核與著作權審查人員

請使用以下開源專案作為課程網站的基礎框架：

https://github.com/htlin222/gym-course

請將這個原本用於影音課程策展的框架，改造成一套：

> **Advanced Thyroid and Neck Ultrasonography for Endocrine Fellows and Specialists**
> **內分泌 Fellow 與專科醫師的進階甲狀腺及頸部超音波課程**

---

# 一、專案定位

這不是一般住院醫師或初學者的甲狀腺超音波入門課程。

主要受眾為：

* 內分泌新陳代謝科 fellow
* 已取得專科資格、希望補強超音波能力的醫師
* 已能完成基本甲狀腺掃描，但判讀經驗不足的臨床醫師
* 執行甲狀腺結節評估、細針穿刺、術前定位或術後追蹤的醫師
* 需要教授住院醫師或 fellow 的臨床教師

假設學員已經知道：

* 基本超音波原理
* 探頭方向與影像方位
* 甲狀腺基本解剖
* 結節大小測量方式
* cystic、solid、hypoechoic 等基本術語
* 甲狀腺結節與 FNA 的基本概念

因此，基礎內容只能作為：

1. 課前診斷測驗
2. 查漏補缺的快速複習
3. 進階內容所需的 prerequisite

不得讓整門課程退化成一般初學者教學。

---

# 二、核心教育目標

課程完成後，學員應能：

1. 使用標準化方式完成甲狀腺及中央、側頸部掃描。
2. 調整 depth、focus、gain、dynamic range、frequency、Doppler PRF、wall filter 等參數，改善困難影像。
3. 辨識正常解剖、常見變異、假性病灶與技術性 artifact。
4. 使用標準化 lexicon 描述結節，而非只憑「看起來像惡性」判斷。
5. 比較並正確應用最新版本的：

   * ACR TI-RADS
   * ATA sonographic pattern
   * EU-TIRADS
   * K-TIRADS
   * 其他具臨床影響力的區域性系統
6. 理解不同風險分層系統在 biopsy threshold、follow-up threshold、敏感度、特異度及避免不必要穿刺上的差異。
7. 辨識瀰漫性甲狀腺疾病、甲狀腺炎及特殊病變。
8. 評估可疑頸部淋巴結與甲狀腺外侵犯。
9. 執行或理解 ultrasound-guided FNA、core needle biopsy及其他介入程序。
10. 處理術後甲狀腺床與頸部淋巴結追蹤的困難影像。
11. 辨識副甲狀腺病灶及其他甲狀腺外腫塊。
12. 對疑難個案建立鑑別診斷、下一步處置與安全追蹤策略。
13. 清楚知道超音波「可以回答什麼」與「不能回答什麼」。
14. 避免 overdiagnosis、過度穿刺、過度追蹤與不適當的影像確定性。
15. 以結構化報告、影像保存及品質稽核方式提升跨醫師一致性。

---

# 三、先分析原始 Repository

開始搜尋影音前，先完整閱讀：

* `README.md`
* `.claude/skills/curate-course/SKILL.md`
* `.claude/skills/curate-course/reference/config.md`
* `.claude/skills/curate-course/reference/curating.md`
* `.claude/skills/curate-course/reference/evidence.md`
* `.claude/skills/curate-course/reference/quality.md`
* `course/`
* `src/build/`
* course schema
* audit 與 verify scripts

先輸出一份簡短的「框架適配分析」，說明：

1. 哪些功能可直接沿用。
2. 哪些只適用於 YouTube。
3. 如何支援非 YouTube 的醫學影音與病例網站。
4. 哪些改動只需要在 `course/` 完成。
5. 哪些功能必須最小幅度修改 `src/`、schema 或 verify scripts。
6. 如何維持原專案的 build、audit、verify、SEO 與 Cloudflare Pages 部署能力。

不要在尚未完成課程架構以前大量搜尋影片。

---

# 四、資料來源範圍

## 4.1 優先搜尋來源

優先順序如下：

### 第一級：專業學會與學術機構

* American Thyroid Association
* European Thyroid Association
* American College of Radiology
* Korean Society of Thyroid Radiology
* American Institute of Ultrasound in Medicine
* Radiological Society of North America
* Society of Radiologists in Ultrasound
* European Federation of Societies for Ultrasound in Medicine and Biology
* World Federation for Ultrasound in Medicine and Biology
* Endocrine Society
* 其他國家級甲狀腺、內分泌、放射或超音波學會
* 大學醫院、醫學院及正式 fellowship program

### 第二級：同儕審查教育來源

* PubMed／MEDLINE 文獻
* 學術期刊 supplementary video
* Radiology、AJR、European Radiology、Thyroid、JCEM 等相關期刊
* Radiopaedia 等專業影像病例庫
* 學術會議錄影、webinar、grand round
* 專科醫學會的 case conference
* 正式 continuing medical education 課程

### 第三級：高品質公開影音

* YouTube
* Vimeo
* 專業醫療網站內嵌影片
* 醫院教學平台
* 超音波設備廠商的進階教育內容

設備廠商內容可以納入操作教學，但：

* 不得直接把產品宣傳視為臨床證據。
* 必須標示廠商利益關係。
* 診斷與治療主張仍須以指引或同儕審查文獻查核。

---

# 五、搜尋語言

至少使用以下語言搜尋：

* 英文：主要搜尋語言
* 韓文：K-TIRADS、甲狀腺介入與病例教學
* 日文：日本甲狀腺與超音波教育資源
* 中文：臺灣、香港及華語臨床教學
* 必要時加入歐洲其他語言

非英文影片只有在下列情況納入：

* 影像示範價值高
* 可取得英文字幕、自動字幕或可靠摘要
* 影片內容可由其他英文來源交叉驗證
* 課程頁面可提供繁體中文重點說明

最後網站文字以**繁體中文**為主，保留必要英文醫學術語。

---

# 六、建議課程架構

請先驗證架構是否完整，再依搜尋結果微調。建議建立 12–14 章。

## CH0　能力地圖、前測與查漏補缺

* Fellow 應具備的甲狀腺超音波能力
* 影像方位、探頭操作與標準掃描的快速複習
* 20–30 題影像前測
* 常見基礎錯誤診斷
* 依前測結果推薦補強單元
* 如何建立個人掃描 logbook

本章應精簡，不應成為全課主體。

## CH1　進階掃描技術與機器最佳化

* 不同體型、短頸、肥胖、胸骨後延伸的掃描策略
* depth、focus、gain、frequency 與 dynamic range
* compound imaging、harmonic imaging
* Color Doppler 與 power Doppler
* PRF、wall filter、aliasing 與低流速訊號
* calcification、colloid、air、shadowing 等 artifact
* 壓迫、吞嚥、Valsalva 與動態掃描
* 影像保存與可重現性

## CH2　正常解剖、變異與頸部分區

* 甲狀腺、氣管、食道、頸動脈、頸靜脈
* strap muscles、longus colli、胸鎖乳突肌
* recurrent laryngeal nerve 相關解剖
* pyramidal lobe、Zuckerkandl tubercle
* ectopic thyroid、thyroglossal duct remnant
* 中央與側頸淋巴結分區
* 常見 normal variants 與 pseudolesions

## CH3　瀰漫性甲狀腺疾病

* Graves disease
* Hashimoto thyroiditis
* painless thyroiditis
* subacute thyroiditis
* acute suppurative thyroiditis
* Riedel thyroiditis
* IgG4-related thyroid disease
* amiodarone-related thyroid abnormalities
* immune checkpoint inhibitor-related thyroiditis
* 瀰漫性疾病中的假性結節
* 何時需要進一步 FNA、CT、MRI 或核醫檢查

避免把 vascularity 當成單一確診標準。

## CH4　結節描述語言與風險分層

* composition
* echogenicity
* shape
* margin
* echogenic foci
* halo
* capsule contact
* extrathyroidal extension
* vascularity 的適當角色
* comet-tail artifact
* macrocalcification、rim calcification、punctate echogenic foci
* taller-than-wide 的正確測量平面
* spongiform 與 partially cystic nodules
* ACR TI-RADS、ATA、EU-TIRADS、K-TIRADS 的逐項比較

每個系統均須提供：

1. 最新版本與公布日期
2. 原始文件
3. 分類規則
4. FNA threshold
5. follow-up threshold
6. 主要優點
7. 常見誤用
8. 系統間不一致的病例
9. 臨床上如何選擇

## CH5　細針穿刺與介入超音波

* FNA indication
* informed consent
* anticoagulant／antiplatelet considerations
* needle visualization
* parallel 與 perpendicular approach
* trans-isthmic approach
* cystic lesion aspiration
* calcified nodule
* posterior lesion
* small or deep lesion
* suspicious lymph-node FNA
* thyroglobulin washout
* PTH washout
* specimen adequacy
* rapid on-site evaluation
* nondiagnostic cytology
* core needle biopsy
* complications and emergency management
* 如何連結 Bethesda cytology 與超音波風險

不得以公開影音取代當地 credentialing、supervision 或感染控制規範。

## CH6　甲狀腺惡性腫瘤影像

* classical papillary thyroid carcinoma
* follicular variant PTC
* follicular thyroid carcinoma
* medullary thyroid carcinoma
* poorly differentiated thyroid carcinoma
* anaplastic thyroid carcinoma
* primary thyroid lymphoma
* metastatic tumor to thyroid
* intrathyroidal thymic carcinoma／CASTLE
* cribriform-morular thyroid carcinoma
* diffuse sclerosing variant
* tall-cell、hobnail 等重要變異型
* multifocal、bilateral、diffuse involvement
* ultrasound–pathology correlation

避免宣稱超音波可以單獨確定組織型別。

## CH7　頸部淋巴結與術前分期

* benign vs suspicious lymph nodes
* fatty hilum
* cortical change
* round shape
* cystic change
* calcification
* peripheral vascularity
* extranodal extension
* central compartment
* lateral neck levels
* skip metastasis
* bilateral neck mapping
* preoperative reporting template
* 哪些病灶應 FNA
* 何時搭配 CT、MRI 或其他影像

## CH8　術後追蹤與復發

* thyroid bed normal postoperative appearance
* scar、suture granuloma、remnant tissue
* recurrent tumor
* recurrent lymph-node metastasis
* thyroglobulin-positive／scan-negative 情境
* undetectable thyroglobulin 但可疑影像
* active surveillance
* low-risk papillary microcarcinoma
* nonsurgical treatment 後影像
* thermal ablation 後變化
* ethanol ablation 後追蹤
* longitudinal image comparison

## CH9　副甲狀腺及甲狀腺外病灶

* parathyroid adenoma
* hyperplasia
* parathyroid carcinoma
* intrathyroidal parathyroid lesion
* lymph node
* schwannoma
* branchial cleft cyst
* thyroglossal duct cyst
* esophageal diverticulum
* vascular lesion
* lipoma
* ectopic thymus
* cervical sympathetic chain lesion
* metastatic disease
* 甲狀腺旁病灶的鑑別流程
* Doppler、PTH washout 與其他檢查的角色

## CH10　特殊族群與特殊情境

* pediatric thyroid nodules
* pregnancy
* elderly patients
* familial thyroid cancer
* MEN2
* prior neck irradiation
* multinodular goiter
* substernal goiter
* dialysis／secondary hyperparathyroidism
* postoperative distorted anatomy
* prior ablation
* difficult airway or inability to extend neck
* incidental thyroid findings on other imaging
* emergency neck swelling or hemorrhage

## CH11　進階技術與新興議題

* strain elastography
* shear-wave elastography
* contrast-enhanced ultrasound
* 3D ultrasound
* fusion imaging
* microvascular flow imaging
* AI／deep learning
* automated segmentation
* automated TI-RADS
* radiomics
* interobserver agreement
* domain shift 與 external validation
* device dependence
* AI automation bias
* 新技術是否真正改變臨床決策

每項技術均須區分：

* 技術可行性
* 診斷準確度
* 臨床效益
* 是否已進入正式指引
* 是否僅為研究用途
* 主要限制與爭議

## CH12　高難度病例與影像陷阱

建立 case-based 模組，例如：

* Hashimoto pseudonodule vs malignancy
* spongiform nodule with suspicious focus
* rim-calcified nodule
* tiny posterior lesion
* ectopic parathyroid lesion
* thyroid lymphoma vs severe thyroiditis
* medullary carcinoma without typical appearance
* diffuse sclerosing PTC
* metastatic lymph node with occult primary
* postoperative scar vs recurrence
* esophageal diverticulum mimicking thyroid nodule
* intrathyroidal parathyroid adenoma
* hemorrhagic cyst
* abscess
* invasive anaplastic carcinoma
* discordant TI-RADS systems
* suspicious ultrasound but benign cytology
* benign-appearing ultrasound but clinically high-risk patient

每一病例使用固定格式：

1. 臨床背景
2. 第一眼影像
3. 學員先作判斷
4. 影像關鍵特徵
5. 鑑別診斷
6. 風險分層
7. 是否需要 FNA
8. 下一步檢查
9. 病理或追蹤結果
10. 認知陷阱
11. Take-home message

## CH13　報告、品質保證與能力認證

* structured reporting
* minimum image set
* lesion numbering
* longitudinal comparison
* interobserver variability
* discrepancy review
* peer review
* missed cancer conference
* inappropriate biopsy audit
* image adequacy audit
* logbook
* direct observation
* OSCE／image-based examination
* competency-based progression
* credentialing and maintenance of competence
* train-the-trainer resources

另外搜尋並整理：

* 國際學會的正式課程或認證
* advanced neck ultrasound course
* hands-on workshop
* image challenge
* quiz competition
* award-winning educational cases
* conference best-case／best-image material

「得獎」本身不得作為內容正確性的證據；仍須另外查核。

---

# 七、影音搜尋策略

每個單元建立可重複搜尋的 query matrix。

至少包含：

1. 主題名稱
2. 同義詞
3. disease-specific terms
4. “ultrasound”
5. “sonography”
6. “case”
7. “lecture”
8. “webinar”
9. “how I scan”
10. “pitfall”
11. “pathology correlation”
12. “FNA” 或 “biopsy”
13. “advanced”
14. “fellowship”
15. 學會或醫院名稱

例如：

* thyroid ultrasound advanced lecture
* thyroid sonography fellowship curriculum
* difficult thyroid nodule ultrasound cases
* thyroid ultrasound pitfalls webinar
* cervical lymph node mapping thyroid cancer
* postoperative thyroid bed ultrasound recurrence
* intrathyroidal parathyroid adenoma ultrasound
* Hashimoto pseudonodule ultrasound
* thyroid FNA needle visualization
* ultrasound pathology correlation thyroid carcinoma

搜尋時不得只看搜尋結果排名。必須檢查：

* 影片內容
* 作者身分
* 上傳機構
* 日期
* 是否過時
* 是否有廣告或商業偏誤
* 是否真正包含動態掃描
* 是否有足夠影像解析度
* 是否只是口頭演講而沒有實際影像
* 是否能合法連結或嵌入

---

# 八、每個影音資源的納入標準

每個資源至少記錄：

* title
* speaker
* speaker credentials
* institution
* channel／publisher
* URL
* platform
* publication date
* access date
* duration
* language
* subtitle availability
* resource type
* target level
* topic tags
* disease tags
* procedure tags
* guideline system
* anatomy region
* why selected
* key teaching points
* recommended timestamps
* prerequisites
* evidence references
* conflicts of interest
* access status
* embedding status
* copyright／license note
* verification status
* last verified date

## 影音品質分級

### Tier A：核心教材

* 正式學會、大學、醫學中心或公認專家
* 內容完整
* 影像清楚
* 與現行指引一致
* 有明確教學目的
* 可作為單元主要課程

### Tier B：病例補充

* 特殊或少見病例
* 具有明顯影像價值
* 但內容不夠完整，或缺乏正式證據討論
* 僅作補充，不作唯一依據

### Tier C：技術示範

* 掃描、穿刺、機器操作或 procedure demonstration
* 必須另外搭配正式文獻與安全說明

### Excluded

排除：

* 無法確認作者或來源
* 影像過度模糊
* 明顯錯誤
* 把單一病例當成普遍規則
* 缺乏利益揭露的高度商業宣傳
* 使用過時分類卻未說明
* 無法確認網址真實存在
* 未經授權重新上傳完整付費課程
* 只有吸睛標題、沒有可用教學影像
* 宣稱超音波可以取代病理或完整臨床判斷

---

# 九、非 YouTube 資源的技術處理

原始框架偏重 YouTube。請先確認目前 schema 是否允許其他來源。

若不支援，請以最小變更擴充，例如加入：

```json
{
  "provider": "youtube | vimeo | society | journal | hospital | case_library | external",
  "source_type": "video | webinar | case | atlas | guideline | article | quiz",
  "url": "...",
  "embed_url": "...",
  "embeddable": true,
  "access": "open | registration | subscription | institutional",
  "license": "...",
  "timestamps": [],
  "last_verified": "YYYY-MM-DD"
}
```

驗證機制至少應能確認：

* HTTP status
* redirect
* page title
* canonical URL
* domain
* content type
* 是否需要登入
* 是否可嵌入
* 是否已移除
* 最後驗證日期

YouTube 仍使用實際 API／oEmbed 驗證。

不得憑記憶生成 video ID、PMID、DOI 或網址。

找不到合格資源時：

```json
{
  "url": null,
  "note": "列出搜尋過的 query、來源與未納入原因"
}
```

留空比捏造更好。

---

# 十、影片「截取」與著作權規則

本專案不得任意下載、剪輯、重新上傳或重新散布他人的影片。

優先採取：

1. 原始頁面連結
2. 官方允許的 embed
3. YouTube timestamp deep link
4. 課程頁面列出建議觀看區間
5. 自行撰寫繁體中文重點摘要
6. 以文字描述應觀察的影像特徵

只有在下列情況才能真正擷取片段：

* 明確屬於 public domain
* 採允許重製或改作的 Creative Commons license
* 已取得權利人書面授權
* 或符合法域內可確認的合理使用條件

若授權狀況不明，絕對不要下載或重新上傳。

患者影像必須確認：

* 已去識別化
* 來源合法
* 沒有姓名、病歷號、生日或可識別資訊
* 不以截圖繞過原網站的存取限制

---

# 十一、文獻與實證架構

每一個重要單元需搜尋：

1. 最新專業指引
2. 系統性回顧或 meta-analysis
3. 重要診斷準確度研究
4. interobserver agreement 研究
5. 具臨床決策影響的 cohort
6. 重要爭議或相反證據

每個主張標記：

* `guideline_supported`
* `strong`
* `moderate`
* `limited`
* `contested`
* `expert_consensus`
* `educational_demo_only`

不要把以下項目混為一談：

* 影片品質
* 講者知名度
* 診斷準確度證據
* 臨床效益證據
* 指引是否正式推薦

所有 PMID、DOI、指引網址與版本均須實際驗證。

若不同指引不一致，需建立比較表，而不是強迫選出唯一答案。

---

# 十二、每個單元的固定結構

每個 unit 至少包含：

```json
{
  "id": "ch4-u3",
  "name": "單元名稱",
  "level": "advanced",
  "learning_objectives": [],
  "prerequisites": [],
  "clinical_question": "",
  "assessment": "",
  "core_lesson": {},
  "case_videos": [],
  "procedure_demos": [],
  "image_atlas": [],
  "guidelines": [],
  "evidence_summary": "",
  "pitfalls": [],
  "discordant_cases": [],
  "take_home_points": [],
  "self_test": [],
  "references": []
}
```

`assessment` 必須可實際操作，例如：

* 看一段未標示診斷的影片後完成 structured description。
* 分別以 ACR TI-RADS、ATA 與 K-TIRADS 分級。
* 判斷是否需要 FNA。
* 標示應穿刺位置。
* 說明哪一個影像特徵最可能造成誤判。
* 對術後甲狀腺床病灶提出下一步處置。

不得只寫「了解本主題」或「熟悉相關知識」。

---

# 十三、病例與影像圖譜

除影片課程外，另外建立可搜尋的「影像病例圖譜」。

篩選欄位包括：

* diagnosis
* benign／malignant／indeterminate
* diffuse／focal
* thyroid／lymph node／parathyroid／other
* adult／pediatric／pregnancy
* preoperative／postoperative
* cytology category
* pathology
* TIRADS category
* ultrasound feature
* difficulty
* pitfall
* procedure
* modality
* source type

每個病例頁面應呈現：

* 臨床資訊
* 靜態影像或合法嵌入內容
* 動態影片
* 結構化影像描述
* 風險分類
* 鑑別診斷
* 最終診斷
* learning pearl
* common mistake
* 來源與授權
* 相關文獻

---

# 十四、評量設計

建立三層評量。

## Level 1：影像辨識

* anatomy
* artifact
* lexicon
* benign vs suspicious features

## Level 2：結構化判讀

* 完成報告
* 使用不同 TI-RADS
* 選擇 FNA 或追蹤
* 辨識 guideline discordance

## Level 3：臨床整合

* 結合年齡、病史、TSH、cytology、prior imaging
* 決定下一步處置
* 面對不確定性
* 解釋何時應轉介
* 避免不必要穿刺或手術

建議產出：

* 30 題前測
* 每章 5–10 題 formative quiz
* 50 題影像後測
* 10 個完整 case-based OSCE stations
* procedure checklist
* structured reporting checklist
* fellow portfolio／logbook template

不要用觀看影片分鐘數當作唯一完成標準。

---

# 十五、網站介面

保留原框架的：

* 章節樹
* 上課模式
* 影片播放器
* 全文搜尋
* 多條件篩選
* localStorage 進度
* 深淺色模式
* 引用與證據分級
* SEO
* sitemap
* `llms.txt`
* Cloudflare Pages 部署

新增或調整：

1. 依疾病、影像特徵與難度篩選。
2. Core、Advanced、Rare Case、Procedure 標籤。
3. Guideline year／version 標籤。
4. 「先作答，再顯示診斷」病例模式。
5. 圖片放大與 side-by-side comparison。
6. 同一病灶 longitudinal comparison。
7. ACR／ATA／EU／K-TIRADS 比較器。
8. FNA decision table。
9. 醫師個人學習進度與錯題標記。
10. 顯示影片最後查核日期。
11. 顯示來源、利益關係、授權與證據等級。
12. 對需要註冊或付費的來源明確標示。
13. 手機、平板與桌機均可使用。

---

# 十六、工作流程

依序執行，不得跳步：

## Phase 1：需求與能力框架

* 定義受眾
* 建立 competency map
* 建立章節與單元
* 設定每章資源配額
* 估算總影片數與總時數

## Phase 2：Repository 適配

* fork／clone
* 分析 schema
* 規劃 non-YouTube support
* 建立 course config
* 建立 taxonomy

## Phase 3：平行搜尋

每章由獨立 subagent 搜尋，但必須共用：

* metadata schema
* quality criteria
* evidence grading
* deduplication rules
* terminology rules

每個 subagent 只能寫入自己的章節檔案，避免相互覆寫。

## Phase 4：人工式內容檢查

逐支確認：

* 影片真的存在
* 內容與標題相符
* 講者可信
* 適合 fellow 程度
* 沒有明顯錯誤
* 沒有不當患者識別資訊
* 沒有侵權重製

## Phase 5：文獻查核

* 最新指引
* PMID
* DOI
* evidence grade
* disputed claims

## Phase 6：Metadata 與技術驗證

* duration
* title
* channel
* views，若平台提供
* URL status
* embed status
* duplicate detection
* last verified date

## Phase 7：建立與稽核

執行：

```bash
make build
make audit
make verify
make check
make serve
```

若擴充了非 YouTube 來源，增加相對應的：

```bash
make verify-external
```

## Phase 8：介面與教學測試

測試：

* fellow 能否找到特定疾病
* 能否由影像特徵反查病例
* 能否比較不同 TI-RADS
* quiz 是否能正常使用
* 手機是否溢出
* 影片失效時是否有替代來源
* 付費或需登入內容是否清楚標示

## Phase 9：部署

* 更新 site title
* favicon
* OG image
* metadata
* structured data
* sitemap
* `llms.txt`
* 部署 Cloudflare Pages

---

# 十七、最低內容配額

先提出合理配額並說明理由，參考目標：

* 12–14 章
* 50–70 個單元
* 60–100 支核心課程影音
* 100–180 支病例或短片段資源
* 80–150 個結構化病例
* 30–50 個介入或掃描技術示範
* 100 篇以上經查核文獻
* 每章至少一個高難度病例
* 每章至少一個常見誤判
* 每個主要惡性腫瘤類型至少一個病例
* 每個主要 TIRADS 系統至少一個完整教學單元

配額應加權分配，不要平均填充。

常見且重要的主題應有更多資源；罕見疾病可以較少，但必須精選。

---

# 十八、不得接受的產出

不得：

* 只產生影片標題清單
* 只搜尋 YouTube 前幾頁
* 用觀看數取代專業品質
* 產生不存在的網址
* 產生虛構 PMID 或 DOI
* 未看內容就宣稱影片已驗證
* 把初學內容大量填入進階課程
* 只教結節，不教頸部淋巴結與術後追蹤
* 忽略副甲狀腺及甲狀腺外病灶
* 把 AI、elastography 或 CEUS 的研究成果誇大成標準照護
* 把單一 TI-RADS 當成全球唯一標準
* 任意下載或重製受著作權保護的影片
* 使用可識別患者資料
* 為了配額納入低品質內容
* 對找不到的內容進行猜測

---

# 十九、最終交付物

請完成並交付：

1. `COURSE-PLAN.md`

   * 受眾
   * competency map
   * 章節
   * 單元
   * 配額
   * 預估時數

2. `SEARCH-METHODOLOGY.md`

   * database
   * website
   * query matrix
   * language
   * inclusion／exclusion criteria
   * search date

3. `SOURCE-REGISTRY.csv` 或 JSON

   * 所有曾評估的來源
   * 納入與排除理由

4. `GUIDELINE-MATRIX.md`

   * ACR、ATA、EU、K-TIRADS 等系統比較

5. `COMPETENCY-FRAMEWORK.md`

6. `COPYRIGHT-AND-PRIVACY-AUDIT.md`

7. 完整的 `course/` 資料

8. 必要的 schema 與 external-link verifier 修改

9. 影音及文獻驗證報告

10. 前測、章節測驗、後測與 OSCE 題庫

11. Fellow logbook 與 procedure checklist

12. 建置成功的靜態網站

13. Cloudflare Pages 部署設定

14. 最終 `README.md`

15. `KNOWN-GAPS.md`
    誠實列出：

    * 找不到高品質影片的主題
    * 僅有付費內容的主題
    * 證據不足的技術
    * 指引不一致處
    * 仍需專家人工審查處

---

# 二十、回報格式

先不要立刻大量修改程式。

第一輪先回報：

## A. Repository 適配分析

* 可直接沿用功能
* 必須修改功能
* 非 YouTube 來源支援方案

## B. Fellow 能力框架

列出完整 competencies。

## C. 課程章節草案

以表格呈現：

| Chapter | Unit | Fellow-level question | Resource type | Assessment |
| ------- | ---- | --------------------- | ------------- | ---------- |

## D. 搜尋策略

* 搜尋平台
* 搜尋語言
* query matrix
* 納入排除標準

## E. 預計資料結構

提供 JSON 範例。

## F. 風險與待人工確認事項

完成以上規劃後，再開始正式搜尋、策展、驗證、寫入 repository、建置及部署。

---

# 最終品質原則

這門課的價值不在於「收集最多影片」，而在於：

* 找出 fellow 真正容易漏掉的知識
* 提供罕見但臨床重要的病例
* 讓影像描述連結到臨床決策
* 比較不同指引，而非背誦單一系統
* 清楚標示證據、不確定性與爭議
* 讓每一個網址、引用與影像來源都能查證
* 讓學員從被動觀看進展到主動判讀
* 讓課程能長期更新，而非建立後迅速失效

遇到資料不足時，請誠實留下缺口，不得用生成內容假裝已經找到真實病例、影片或文獻。
