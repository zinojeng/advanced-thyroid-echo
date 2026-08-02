// rate.js — 影片評價。低分會進入換片清單，所以低分一定要問「哪裡不合格」。
//
// 設計上的一個決定：**低分才問原因，高分不問。**
// 每次評價都要選標籤會讓人懶得評；但只有分數的低分對策展沒有用——
// 知道某支片不好卻不知道為什麼，換片時等於把使用者已經看出來的事再猜一次。
//
// 沒有 D1 時 /api/rate 一律回 503，整個區塊安靜地不顯示。
import { icon } from "./icons.js";
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
  return ENABLED && !!CFG.label;
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

async function send(video, score, reason) {
  try {
    const res = await fetch("/api/rate", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ video, score, reason, voter: voter() }),
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

/** 播放器動作列上的評價按鈕（與「討論」並排） */
export function button() {
  if (!enabled()) return "";
  return `<button class="btn btn-icon" data-rate-toggle type="button" title="${esc(CFG.label || "")}">
            ${icon("star", 16)}<span class="Rate__btnCount" data-rate-count></span>
          </button>`;
}

/** 面板骨架。內容在展開時才填，避免每次換片都打 API */
export function panel() {
  if (!enabled()) return "";
  return `<div class="Rate" id="ratePanel" hidden></div>`;
}

function stars(current) {
  return [1, 2, 3, 4, 5]
    .map(
      (n) =>
        `<button class="Rate__star${current && n <= current ? " is-on" : ""}"
                 type="button" data-score="${n}" aria-label="${n} 分">${icon("star", 18)}</button>`,
    )
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

/** 低分才問原因——高分每次都要選標籤會讓人懶得評 */
function needsReason(score) {
  return score <= (CFG.lowThreshold ?? 2);
}

function render(video, agg, state = {}) {
  const el = $("#ratePanel");
  if (!el) return;
  const mine = state.mine ?? myScores()[video];
  el.innerHTML = `
    <div class="Rate__head">
      <strong>${esc(CFG.label || "")}</strong>
      ${summary(agg)}
    </div>
    <div class="Rate__stars" data-rate-stars>${stars(state.pending || mine)}</div>
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
           </div>`
        : ""
    }
    ${state.done ? `<p class="Rate__thanks">${esc(CFG.thanks || "")}</p>` : ""}
    ${reasonList(agg)}
    <p class="Rate__note">${esc(CFG.anonNote || "")}</p>`;
}

/* --- 掛載 ---------------------------------------------------------------- */

let current = null;

/** 換片時呼叫：更新按鈕上的平均分，並把面板收起來 */
export async function attach(video) {
  current = video;
  if (!enabled() || !video) return;
  const badge = $("[data-rate-count]");
  const agg = await fetchAgg(video);
  if (!agg) {
    // 後端沒接：把按鈕藏起來，不留壞掉的空殼
    const btn = $("[data-rate-toggle]");
    if (btn && !ENABLED) btn.hidden = true;
    return;
  }
  if (badge) badge.textContent = agg.n ? agg.avg.toFixed(1) : "";
  const panelEl = $("#ratePanel");
  if (panelEl && !panelEl.hidden) render(video, agg);
}

export function init() {
  if (!enabled()) return;

  document.addEventListener("click", async (e) => {
    const toggle = e.target.closest("[data-rate-toggle]");
    if (toggle) {
      const el = $("#ratePanel");
      if (!el) return;
      el.hidden = !el.hidden;
      if (!el.hidden) render(current, await fetchAgg(current));
      return;
    }

    const star = e.target.closest(".Rate__star");
    if (star && current) {
      const score = Number(star.dataset.score);
      if (needsReason(score)) {
        // 低分：先問原因再送出，這樣換片清單才有可操作的資訊
        render(current, CACHE.get(current), { pending: score, askReason: true });
        $("#ratePanel").dataset.pendingScore = String(score);
      } else {
        rememberMine(current, score);
        const agg = await send(current, score, null);
        render(current, agg, { mine: score, done: true });
        await attach(current);
      }
      return;
    }

    const reason = e.target.closest(".Rate__reasonBtn");
    if (reason && current) {
      const score = Number($("#ratePanel")?.dataset.pendingScore || 0);
      if (!score) return;
      rememberMine(current, score);
      const agg = await send(current, score, reason.dataset.reason);
      render(current, agg, { mine: score, done: true });
      await attach(current);
    }
  });
}
