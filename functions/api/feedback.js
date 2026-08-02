/**
 * 策展者專用：把所有評價與**自由文字回饋**一次讀出來。
 *
 * 為什麼要跟 /api/rate 分開：
 * /api/rate 是公開端點，任何人都讀得到聚合數字。自由文字不能走那條路——
 * 匿名文字公開顯示等於在課程頁面上開一個沒人管的留言板，
 * 而這門課沒有帳號系統、沒有審核流程，也沒有人力做內容管理。
 *
 * 所以文字只在這裡、而且要帶對 token 才讀得到。
 * token 放 Cloudflare 的環境變數 FEEDBACK_TOKEN（不是寫在程式裡）。
 * 沒設 token 就整個端點關閉——寧可沒有這個功能，也不要留一個誰都能讀的洞。
 */

const NO_STORE = {
  "content-type": "application/json; charset=utf-8",
  "cache-control": "no-store, max-age=0",
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: NO_STORE });
}

/** 常數時間比較，避免用回應時間猜 token */
function sameToken(a, b) {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

export async function onRequestGet({ env, request }) {
  if (!env.HITS) return json({ error: "no-d1" }, 503);
  if (!env.FEEDBACK_TOKEN) return json({ error: "not-configured" }, 503);

  const url = new URL(request.url);
  const given =
    url.searchParams.get("token") ||
    (request.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
  if (!sameToken(given, env.FEEDBACK_TOKEN)) return json({ error: "unauthorized" }, 401);

  // since=<epoch 秒>：只要新的，做週期摘要用
  const since = Number(url.searchParams.get("since") || 0) || 0;

  try {
    const rows = await env.HITS.prepare(
      `SELECT video, score, reason, comment, ts
         FROM ratings
        WHERE ts >= ?
        ORDER BY ts DESC
        LIMIT 1000`,
    )
      .bind(since)
      .all();

    const items = rows?.results ?? [];
    return json({
      since,
      total: items.length,
      with_comment: items.filter((r) => r.comment).length,
      latest_ts: items.length ? Math.max(...items.map((r) => r.ts)) : since,
      items,
    });
  } catch {
    return json({ error: "query-failed" }, 503);
  }
}
