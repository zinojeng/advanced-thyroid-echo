/**
 * 影片評價。GET 讀聚合結果，POST 投票。
 *
 * 為什麼要收「低分原因」而不只是分數：
 * 這門課的評價不是給影片打人氣，是**產生換片工作清單**。
 * 只有平均分的話，策展者知道某支片有問題卻不知道問題在哪，
 * 換片時等於把使用者已經看出來的事再猜一次。
 * 所以低分必須附一個原因標籤（沒有實際影像／影像模糊／內容過時／與單元不符…），
 * `make ratings` 才能直接印出「這支要換，因為 N 個人說它沒有實際掃描畫面」。
 *
 * 沒有綁 D1（例如本機預覽）時一律回 503，前端安靜地不顯示評價區塊。
 * 寧可沒有這個功能，也不要在頁面上留一個壞掉的空殼。
 */

const NO_STORE = {
  "content-type": "application/json; charset=utf-8",
  "cache-control": "no-store, max-age=0",
};

const BOT =
  /bot|crawl|spider|slurp|bingpreview|facebookexternalhit|headless|lighthouse|monitor|preview|curl|wget|python-requests/i;

const VIDEO_ID = /^[\w-]{11}$/;
const MAX_REASON = 40;
const MAX_COMMENT = 600;

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: NO_STORE });
}

/** 單支影片的聚合：平均、票數、各分數分布、低分原因次數 */
async function one(db, video) {
  const agg = await db
    .prepare(
      `SELECT COUNT(*) AS n, AVG(score) AS avg,
              SUM(score <= 2) AS low,
              SUM(comment IS NOT NULL AND comment <> '') AS comments
         FROM ratings WHERE video = ?`,
    )
    .bind(video)
    .first();

  const reasons = await db
    .prepare(
      `SELECT reason, COUNT(*) AS n FROM ratings
        WHERE video = ? AND reason IS NOT NULL AND reason <> ''
        GROUP BY reason ORDER BY n DESC`,
    )
    .bind(video)
    .all();

  return {
    video,
    n: agg?.n ?? 0,
    avg: agg?.n ? Math.round(agg.avg * 100) / 100 : null,
    low: agg?.low ?? 0,
    // 有幾則文字回饋（內容不公開，只讓使用者知道有人寫過）
    comments: agg?.comments ?? 0,
    reasons: (reasons?.results ?? []).map((r) => ({ reason: r.reason, n: r.n })),
  };
}

export async function onRequestGet({ env, request }) {
  if (!env.HITS) return json({ error: "no-d1" }, 503);
  const url = new URL(request.url);
  const video = url.searchParams.get("v");

  try {
    if (video) {
      if (!VIDEO_ID.test(video)) return json({ error: "bad-video" }, 400);
      return json(await one(env.HITS, video));
    }
    // 沒指定影片就回全部聚合，給 make ratings 產換片清單用
    const rows = await env.HITS.prepare(
      `SELECT video, COUNT(*) AS n, ROUND(AVG(score), 2) AS avg,
              SUM(score <= 2) AS low
         FROM ratings GROUP BY video ORDER BY avg ASC, n DESC`,
    ).all();
    const reasons = await env.HITS.prepare(
      `SELECT video, reason, COUNT(*) AS n FROM ratings
        WHERE reason IS NOT NULL AND reason <> ''
        GROUP BY video, reason`,
    ).all();

    const byVideo = {};
    for (const r of reasons?.results ?? []) {
      (byVideo[r.video] ||= []).push({ reason: r.reason, n: r.n });
    }
    return json({
      videos: (rows?.results ?? []).map((r) => ({ ...r, reasons: byVideo[r.video] ?? [] })),
    });
  } catch {
    return json({ error: "query-failed" }, 503);
  }
}

export async function onRequestPost({ env, request }) {
  if (!env.HITS) return json({ error: "no-d1" }, 503);
  if (BOT.test(request.headers.get("user-agent") || "")) {
    return json({ error: "bot" }, 403);
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: "bad-json" }, 400);
  }

  const video = String(body.video || "");
  const score = Number(body.score);
  const voter = String(body.voter || "");
  const reason = body.reason ? String(body.reason).slice(0, MAX_REASON) : null;
  // 自由文字：只有標籤的話，策展者知道有問題卻不知道問題在哪。
  // 這段**不會**回傳給一般讀者（匿名文字公開顯示等於開一個沒人管的留言板），
  // 只在 /api/feedback 帶對 token 時才讀得到。
  const comment = body.comment ? String(body.comment).trim().slice(0, MAX_COMMENT) : null;

  if (!VIDEO_ID.test(video)) return json({ error: "bad-video" }, 400);
  if (!Number.isInteger(score) || score < 1 || score > 5) {
    return json({ error: "bad-score" }, 400);
  }
  // voter 是前端產生的隨機 token；長度限制只是防止有人塞大字串進資料庫
  if (voter.length < 8 || voter.length > 64) return json({ error: "bad-voter" }, 400);

  try {
    await env.HITS.prepare(
      `INSERT INTO ratings (video, voter, score, reason, comment, ts)
       VALUES (?, ?, ?, ?, ?, unixepoch())
       ON CONFLICT(video, voter) DO UPDATE SET
         score = excluded.score, reason = excluded.reason,
         comment = excluded.comment, ts = excluded.ts`,
    )
      .bind(video, voter, score, reason, comment)
      .run();
    return json(await one(env.HITS, video));
  } catch {
    return json({ error: "write-failed" }, 503);
  }
}
