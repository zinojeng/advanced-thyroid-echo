-- 累計瀏覽次數。只有一列，k 固定是 'total'。
-- 建表：make counter（或 npx wrangler d1 execute <DB> --file functions/schema.sql --remote）
CREATE TABLE IF NOT EXISTS hits (
  k TEXT PRIMARY KEY,
  n INTEGER NOT NULL DEFAULT 0
);
INSERT OR IGNORE INTO hits (k, n) VALUES ('total', 0);

-- 影片評價。低分的片子要被換掉，所以除了分數還要收「為什麼低分」——
-- 只有分數的話，策展者知道有問題卻不知道問題在哪，換片時等於重猜一次。
--
-- voter 是瀏覽器端產生的隨機 token，存在 localStorage。
-- 這**不是**身分驗證：清掉瀏覽器資料就能再投一次。
-- 它擋的是誤觸與同一個人連按，不是有意灌票。誠實說明見 README。
CREATE TABLE IF NOT EXISTS ratings (
  video  TEXT    NOT NULL,          -- YouTube video id
  voter  TEXT    NOT NULL,          -- 匿名 client token
  score  INTEGER NOT NULL,          -- 1–5
  reason TEXT,                      -- 低分原因標籤，見 course.config.json 的 ratings.reasons
  comment TEXT,                     -- 選填自由文字。只有點標籤的話，策展者知道有問題卻不知道問題在哪
  ts     INTEGER NOT NULL,          -- epoch 秒
  PRIMARY KEY (video, voter)        -- 一個人一支片一票，重投就覆蓋
);

-- 報告要問的是「哪些片子分數低」，所以照 video 聚合
CREATE INDEX IF NOT EXISTS ratings_by_video ON ratings (video);

-- 既有資料庫補欄位。D1 不支援 ADD COLUMN IF NOT EXISTS，
-- 所以 setup_counter.py 會單獨跑這一句並容忍「duplicate column」錯誤。
-- ALTER TABLE ratings ADD COLUMN comment TEXT;
