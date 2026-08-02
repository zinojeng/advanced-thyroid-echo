// rate.js — 影片評價。低分會進入換片清單，所以低分一定要問「哪裡不合格」。
//
// 兩個設計上的決定：
//
// 1. **一點就送出。** 星星要先想「這值幾分」再瞄準第幾顆，成本高到大部分人直接跳過。
//    改成幾顆語意明確的 chip（很好／好／普通／差／內容有錯），點一下就記錄；
//    分數對應仍是 1–5，後端與 `make ratings` 完全不用改。
//
// 2. **低分才問原因，高分不問。** 每次評價都要選標籤會讓人懶得評；
//    但只有分數的低分對策展沒有用——知道某支片不好卻不知道為什麼，
//    換片時等於把使用者已經看出來的事再猜一次。
//    「內容有錯」是最需要可操作資訊的一種，所以它一定追問是哪一種錯。
//
// 沒有 D1 時 /api/rate 一律回 503，整個區塊安靜地不顯示。
import { esc } from "./render.js";

const $ = (s, r = document) => r.querySelector(s);

let CFG = {};
let ENABLED = true; // 一旦確認後端沒接，就不再重試
const CACHE = new Map(); // videoId -> 聚合結果
const VOTER_KEY = "rating-voter";
const MINE_KEY = "rating-mine";

export function setConfig(c) {
  CFG = c || {};
}

export function enabled() {
  return ENABLED && !!CFG.label && (CFG.quick || []).length > 0;
}

/** 匿名投票 token。不是身分驗證——清掉瀏覽器資料就能再投一次。
 *  它擋的是誤觸與同一個人連按，不是有意灌票。 */
function voter() {
  let v = localStorage.getItem(VOTER_KEY);
  if (!v) {
    v = (crypto.randomUUID?.() || String(Math.random()).slice(2) + Date.now()).replace(/-/g, "");
    localStorage.setItem(VOTER_KEY, v);
  }
  return v;
}

function myScores() {
  try {
    return JSON.parse(localStorage.getItem(MINE_KEY) || "{}");
  } catch {
    return {};
  }
}

function rememberMine(video, score) {
  const m = myScores();
  m[video] = score;
  localStorage.setItem(MINE_KEY, JSON.stringify(m));
}

async function fetchAgg(video) {
  if (CACHE.has(video)) return CACHE.get(video);
  try {
    const res = await fetch(`/api/rate?v=${encodeURIComponent(video)}`, { cache: "no-store" });
    if (res.status === 503) {
      ENABLED = false;
      return null;
    }
    if (!res.ok) return null;
    const data = await res.json();
    CACHE.set(video, data);
    return data;
  } catch {
    return null;
  }
}

async function send(video, score, reason, comment) {
  try {
    const res = await fetch("/api/rate", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ video, score, reason, comment, voter: voter() }),
    });
    if (!res.ok) return null;
    const data = await res.json();
    CACHE.set(video, data);
    return data;
  } catch {
    return null;
  }
}

/* --- 標記 ---------------------------------------------------------------- */

/** 常駐在摘要區塊下方的快速回饋區。內容在 attach() 時填。 */
export function block() {
  if (!enabled()) return "";
  // aria-live 不能掛在整塊上：attach() 每換一支影片會 render 兩次（先快取、再 fetch），
  // 第二次是非同步變動，讀屏會把整塊樣板重念一遍。狀態訊息改由內部一個常駐節點承接。
  return `<div class="Rate" id="rateBlock" hidden></div>`;
}

/** chip 的分數與文案全部來自 course.config.json 的 ratings.quick */
function chips(current) {
  return (CFG.quick || [])
    .map((q) => {
      const score = Number(q.score);
      if (!Number.isInteger(score) || score < 1 || score > 5) return "";
      const on = current === score ? " is-on" : "";
      return `<button class="Rate__chip${on}" type="button"
                      data-score="${score}"${q.ask ? " data-ask=\"1\"" : ""}
                      aria-pressed="${current === score}">${esc(q.label || "")}</button>`;
    })
    .join("");
}

function summary(agg) {
  if (!agg || !agg.n) return `<span class="Rate__none">${esc(CFG.noneLabel || "")}</span>`;
  return `<span class="Rate__avg">${agg.avg.toFixed(1)}</span>
          <span class="Rate__n">${agg.n} ${esc(CFG.countLabel || "")}</span>`;
}

function reasonList(agg) {
  if (!agg?.reasons?.length) return "";
  const label = (id) => (CFG.reasons || []).find((r) => r.id === id)?.label || id;
  return `<ul class="Rate__reasons">${agg.reasons
    .map((r) => `<li><span>${esc(label(r.reason))}</span><b>${r.n}</b></li>`)
    .join("")}</ul>`;
}

/** 低分才問原因；宣告 ask 的 chip（內容有錯）不管分數一律問 */
function needsReason(score, ask) {
  return !!ask || score <= (CFG.lowThreshold ?? 2);
}

function render(video, agg, state = {}) {
  const el = $("#rateBlock");
  if (!el) return;
  const mine = state.mine ?? state.pending ?? myScores()[video];
  el.innerHTML = `
    <div class="Rate__head">
      <strong>${esc(CFG.quickPrompt || CFG.label || "")}</strong>
      ${summary(agg)}
    </div>
    <div class="Rate__chips">${chips(mine)}</div>
    ${
      state.askReason
        ? `<div class="Rate__ask">
             <p>${esc(CFG.reasonPrompt || "")}</p>
             <div class="Rate__reasonBtns">
               ${(CFG.reasons || [])
                 .map(
                   (r) =>
                     `<button class="btn Rate__reasonBtn" type="button" data-reason="${esc(r.id)}">${esc(r.label)}</button>`,
                 )
                 .join("")}
             </div>
             <label class="Rate__commentWrap">
               <span>${esc(CFG.commentPrompt || "")}</span>
               <textarea class="Rate__comment" rows="2" maxlength="600"
                         placeholder="${esc(CFG.commentPlaceholder || "")}"></textarea>
             </label>
             <p class="Rate__commentNote">${esc(CFG.commentNote || "")}</p>
           </div>`
        : ""
    }
    <p class="Rate__status" role="status" aria-live="polite">${state.done ? esc(CFG.thanks || "") : ""}</p>
    ${reasonList(agg)}
    <p class="Rate__note">${esc(CFG.anonNote || "")}</p>`;
  if (state.askReason) el.dataset.pendingScore = String(state.pending || "");
  else delete el.dataset.pendingScore;
}

/* --- 掛載 ---------------------------------------------------------------- */

let current = null;

/** 換片時呼叫：先用快取畫出 chips，再把這一支的聚合結果補上 */
export async function attach(video) {
  current = video;
  const el = $("#rateBlock");
  if (!el) return;
  if (!enabled() || !video) {
    el.hidden = true;
    return;
  }
  el.hidden = false;
  render(video, CACHE.get(video) || null);
  const agg = await fetchAgg(video);
  if (!agg && !ENABLED) {
    // 後端沒接：整區收起來，不留壞掉的空殼
    el.hidden = true;
    return;
  }
  if (current !== video) return; // 期間又換片了，別把舊資料畫回去
  render(video, agg);
}

export function init() {
  if (!enabled()) return;

  document.addEventListener("click", async (e) => {
    const chip = e.target.closest(".Rate__chip");
    if (chip && current) {
      const score = Number(chip.dataset.score);
      if (!score) return;
      if (needsReason(score, chip.dataset.ask === "1")) {
        // 低分與「內容有錯」：先問是哪一種問題再送出，換片清單才有可操作的資訊
        render(current, CACHE.get(current), { pending: score, askReason: true });
      } else {
        rememberMine(current, score);
        const agg = await send(current, score, null, null);
        render(current, agg || CACHE.get(current), { mine: score, done: true });
      }
      return;
    }

    const reason = e.target.closest(".Rate__reasonBtn");
    if (reason && current) {
      const score = Number($("#rateBlock")?.dataset.pendingScore || 0);
      if (!score) return;
      // 標籤說「哪一類問題」，文字說「到底哪裡不對」——後者才是換片時真正需要的
      const text = $("#rateBlock .Rate__comment")?.value?.trim() || null;
      rememberMine(current, score);
      const agg = await send(current, score, reason.dataset.reason, text);
      render(current, agg || CACHE.get(current), { mine: score, done: true });
    }
  });
}
