#!/usr/bin/env python3
"""用 Gemini 的多模態影片理解，查核影片「內容」是否真的符合課程宣稱。

oEmbed 只能證明連結還活著，證明不了影片裡拍了什麼。使用者曾回報一支
「經皮喉部超音波」只有對話討論、沒有任何超音波影像；CH12 擴充時也抓到
「宣稱全片實機掃描、實為投影片講座」與「片頭卡直接印出最終病理」。
這支腳本把那一關從「agent 抽格人工看」（慢、而且可以被造假）換成
可重現的自動檢查：直接把 YouTube URL 餵給 Gemini，拿結構化 JSON 回來。

**Gemini 的判斷是輔助訊號，不是判決。**
它會看錯，最常見的是分不清「投影片上貼的靜態超音波截圖」與「實機動態掃描」，
也可能把解剖動畫誤認成超音波畫面。這支腳本刻意不會去改動任何課程資料：
被標記出來的影片一律需要人工開影片確認後，再由人決定要不要換片或補 `start`。

用法：
    python3 verify_content.py                 # 查核（有快取，只查新的或改過的）
    python3 verify_content.py --only ch12     # 只查某一章
    python3 verify_content.py --limit 5       # 最多查 5 支（先試水溫）
    python3 verify_content.py --refresh       # 忽略快取全部重查
    python3 verify_content.py --dry-run       # 只列出這次會查哪幾支，不打 API
    python3 verify_content.py --json          # 機器可讀輸出

一支 40 分鐘的影片約 10 萬 tokens（0.5 fps + MEDIA_RESOLUTION_LOW），
全部 257 支跑一輪大約 2,600 萬 tokens。先用 --dry-run／--limit 控制規模。

需要 .env 裡的 GEMINI_API_KEY（認證走 x-goog-api-key header）。
沒有金鑰時印一行說明並正常結束，不會讓 make 失敗。
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sources as SRC

ROOT = Path(__file__).resolve().parents[2]
COURSE_JSON = Path(os.environ.get("DIST") or ROOT / "dist").resolve() / "course.json"
DATA = Path(os.environ.get("COURSE") or ROOT / "course").resolve() / "data"
REPORT = DATA / "content-verify.json"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

DEFAULT_MODEL = "gemini-2.5-flash"
# 取樣頻率越低越便宜（0.2 fps 讓 45 分鐘的影片從 ~700k 掉到 ~38k video tokens），
# 但太低就分不出「靜態截圖」與「動態掃描」。0.5 是成本與可判性的折衷。
DEFAULT_FPS = 0.5
MAX_WORKERS = 4  # 併發上限，不要調高：YouTube 影片解析在 Gemini 端很吃資源
MIN_INTERVAL = 2.0  # 每個請求之間至少間隔幾秒
MAX_RETRY = 3
TIMEOUT = 600
# 問法改了就等於換了一個檢查，舊快取一律作廢。改 PROMPT／RESPONSE_SCHEMA 時請一起改。
PROMPT_VERSION = "2026-08-03.3"

DISCLAIMER = (
    "Gemini 的判斷是輔助訊號，不是判決。它會看錯，最常見的是分不清"
    "「投影片上貼的靜態超音波截圖」與「實機動態掃描」，也可能把解剖動畫"
    "誤認成超音波畫面、或漏掉只出現數秒的片段。同一支影片重跑，結果也可能"
    "不一樣（畫面取樣與模型輸出都有隨機性），所以這是篩選器不是分數。"
    "這份報告不會、也不該自動改動課程資料："
    "被標記的影片一律需要人工開影片確認後再決定處置。"
)

# 有這些字眼的資源，課程宣稱裡就帶著「畫面上會有超音波影像」的承諾
IMAGING_WORDS = (
    "超音波",
    "ultrasound",
    "sonograph",
    "影像",
    "image",
    "掃描",
    "scan",
    "b-mode",
    "doppler",
    "都卜勒",
    "彈性",
    "elastograph",
    "切面",
    "探頭",
    "probe",
)
# 這些字眼更強：宣稱有動態／實機操作
LIVE_WORDS = (
    "實機",
    "動態",
    "cine",
    "live scan",
    "hands-on",
    "hands on",
    "掃描示範",
    "操作示範",
    "手法",
    "sweep",
    "real-time",
    "real time",
    "即時",
    "錄影示範",
)

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "has_ultrasound": {"type": "boolean"},
        "is_live_scanning": {"type": "boolean"},
        "format": {
            "type": "string",
            "enum": ["live_scan", "slide_lecture", "talking_head", "mixed", "other"],
        },
        "matches_claim": {"type": "boolean"},
        "mismatch_reason": {"type": "string"},
        "spoiler_in_opening": {"type": "boolean"},
        "spoiler_text": {"type": "string"},
        "suggested_start": {"type": "integer"},
        "narration_language": {"type": "string"},
        "commercial": {"type": "boolean"},
        "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
        "notes": {"type": "string"},
    },
    "required": [
        "has_ultrasound",
        "is_live_scanning",
        "format",
        "matches_claim",
        "mismatch_reason",
        "spoiler_in_opening",
        "spoiler_text",
        "suggested_start",
        "narration_language",
        "commercial",
        "confidence",
        "notes",
    ],
}

PROMPT = """你是醫學影像教育內容的查核員。下面這支 YouTube 影片被一門「進階甲狀腺及頸部超音波」課程收錄，課程對它的宣稱是：

【資源名稱】{name}
【教學重點】{target}

請實際看完整支影片（畫面與旁白都要），依下列準則回答，全部以整支影片實際內容為準，不要憑標題或簡介推測。

- has_ultrasound：畫面中是否出現**真正的超音波影像**（B-mode／Doppler／彈性造影的實際掃描畫面，不論是實機錄影或投影片上的截圖）。只有講者說話、純文字投影片、示意圖、解剖繪圖、3D 動畫、體表定位示範，都**不算**。
- is_live_scanning：是否出現**動態**超音波影像——探頭移動、畫面隨時間變化的實機錄影或 cine loop。投影片上貼的**靜態**超音波截圖不算。若畫面切換太少而無法確定是靜態圖或動態片段，回 false，並在 notes 說明你不確定。
- format：整支影片的主要形式。live_scan＝以實機掃描錄影為主；slide_lecture＝以投影片講授為主（即使投影片上有很多超音波圖）；talking_head＝以人講話／對談為主，畫面幾乎沒有教學影像；mixed＝講授與實機掃描各佔相當份量；other＝其他。
- matches_claim：影片的**主題**能不能支撐上面的【教學重點】。這一題只看主題層級：宣稱教穿刺技巧、實際只談流行病學＝false。**下列情況一律算 true**：教學重點裡提到的某個細節、限制或提醒沒有在片中出現；影片用的是別的器官或一般性原理而教學重點要求讀者自行遷移到甲狀腺；影片比教學重點涵蓋得更多或更少但仍是同一主題。false 時在 mismatch_reason 用一句繁體中文寫出主題差在哪（true 時給空字串）。
- spoiler_in_opening：影片**前 10 秒**的片頭卡、標題畫面或字幕，是否直接寫出最終診斷／病理結果（例如標題就寫「papillary carcinoma」），讓學員還沒看影像就知道答案。是的話 spoiler_text 照抄那段字（原文，30 字以內），suggested_start 給一個建議的起播秒數（整數，跳過該片頭卡之後、教學內容開始之前）；不是的話 spoiler_text 給空字串、suggested_start 給 0。
- narration_language：旁白的主要語言（用 en／zh-TW／zh-CN／ja／ko／es／pt 之類的代碼；無旁白寫 none）。
- commercial：是否有**大段**商業推銷（推銷自營課程／會員方案／特定廠商機型），而不只是片尾一兩句致謝或贊助字卡。
- confidence：你對上述判斷的整體把握（low／medium／high）。取樣的畫面偏少、或難以分辨靜態圖與動態片段時，請誠實給 low。
- notes：一句話（繁體中文，40 字以內）說明畫面主要是什麼。

只輸出 JSON。"""


# ---------------------------------------------------------------- 環境與輸入


def load_env_key() -> str | None:
    """取 GEMINI_API_KEY：先看環境變數，再看 .env。金鑰絕不印出。"""
    if key := os.environ.get("GEMINI_API_KEY"):
        return key.strip()
    env = ROOT / ".env"
    if not env.exists():
        return None
    for line in env.read_text().splitlines():
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        if k.strip() == "GEMINI_API_KEY":
            return v.strip().strip("\"'") or None
    return None


def walk(course: dict):
    """走訪所有影片欄位，yield (章節碼, 單元 id, 標籤, 欄位 dict)。"""
    for ch in course["chapters"]:
        for u in ch["units"]:
            for les in u.get("lessons") or ([u["lesson"]] if u.get("lesson") else []):
                yield ch["code"], u["id"], f"主課 {les.get('lang', '')}".strip(), les
            for d in u.get("drills") or []:
                yield ch["code"], u["id"], d.get("name", "?"), d


def claim_text(v: dict) -> tuple[str, str]:
    """課程對這支影片的宣稱：(名稱, 教學重點)。主課沒有 name/target，用 title/why。"""
    name = v.get("name") or v.get("title") or "（未命名）"
    target = v.get("target") or v.get("why") or v.get("note") or "（課程未寫明教學重點）"
    return name, target


def collect(course: dict, only: str | None) -> dict[str, dict]:
    """把 288 個欄位收斂成 {videoId: {...}}；同一支影片被多處引用時合併宣稱。"""
    want = (only or "").strip().lower().removeprefix("ch")
    videos: dict[str, dict] = {}
    for code, uid, label, v in walk(course):
        if not v.get("url") or not SRC.is_youtube(v):
            continue
        if want and code.lower().removeprefix("ch") != want:
            continue
        vid = SRC.youtube_id(v["url"])
        if not vid:
            continue
        name, target = claim_text(v)
        entry = videos.setdefault(
            vid,
            {
                "videoId": vid,
                "url": v["url"],
                "title": v.get("title"),
                "channel": v.get("channel"),
                "duration": v.get("duration"),
                "last_verified": v.get("last_verified"),
                "claims": [],
            },
        )
        entry["claims"].append(
            {
                "chapter": code,
                "unit": uid,
                "label": label,
                "name": name,
                "target": target,
                "start": v.get("start"),
            }
        )
        # 同一支影片在不同欄位可能有不同的 last_verified，取最新的當快取鍵
        lv = v.get("last_verified")
        if lv and (entry["last_verified"] or "") < lv:
            entry["last_verified"] = lv
    return videos


# ---------------------------------------------------------------- Gemini 呼叫

_gate = threading.Lock()
_last_call = [0.0]


def _throttle() -> None:
    """把請求之間拉開至少 MIN_INTERVAL 秒（併發已另外限制在 MAX_WORKERS）。"""
    with _gate:
        wait = MIN_INTERVAL - (time.monotonic() - _last_call[0])
        if wait > 0:
            time.sleep(wait)
        _last_call[0] = time.monotonic()


def ask_gemini(entry: dict, key: str, model: str, fps: float) -> dict:
    """問 Gemini 一支影片。回傳解析後的 dict；失敗時回 {"error": ...}。"""
    claims = entry["claims"]
    name = " ／ ".join(dict.fromkeys(c["name"] for c in claims))
    target = "\n".join(dict.fromkeys(c["target"] for c in claims))
    body = {
        "contents": [
            {
                "parts": [
                    {"text": PROMPT.format(name=name, target=target)},
                    {
                        "file_data": {"file_uri": entry["url"]},
                        "video_metadata": {"fps": fps},
                    },
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0,
            "mediaResolution": "MEDIA_RESOLUTION_LOW",
            "responseMimeType": "application/json",
            "responseSchema": RESPONSE_SCHEMA,
        },
    }
    payload = json.dumps(body).encode()
    last = "未知錯誤"
    for attempt in range(MAX_RETRY):
        _throttle()
        req = urllib.request.Request(
            ENDPOINT.format(model=model),
            data=payload,
            headers={"Content-Type": "application/json", "x-goog-api-key": key},
        )
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as res:
                raw = json.loads(res.read())
            break
        except urllib.error.HTTPError as e:
            detail = ""
            with contextlib.suppress(Exception):
                detail = json.loads(e.read()).get("error", {}).get("message", "")[:200]
            last = f"HTTP {e.code}{'：' + detail if detail else ''}"
            # 429／5xx 是暫時性的，退避後重試；4xx 多半是影片本身不給看，重試無益
            if e.code not in (429, 500, 502, 503, 504):
                return {"error": last}
            time.sleep(5 * (attempt + 1) ** 2)
        except Exception as e:  # 逾時、TLS、DNS
            last = f"連線失敗：{type(e).__name__}"
            time.sleep(5 * (attempt + 1) ** 2)
    else:
        return {"error": last}

    try:
        cand = raw["candidates"][0]
        text = "".join(p.get("text", "") for p in cand["content"]["parts"])
        out = json.loads(text)
        if not isinstance(out, dict):
            raise TypeError(type(out).__name__)
    except Exception:
        reason = (raw.get("candidates") or [{}])[0].get("finishReason") or "回應格式不符"
        return {"error": f"無法解析模型回應（{reason}）"}

    usage = raw.get("usageMetadata") or {}
    out["tokens"] = usage.get("totalTokenCount")
    # 沒有劇透就沒有建議起播點；模型有時會在沒劇透時仍填 0
    if not out.get("spoiler_in_opening") or not out.get("suggested_start"):
        out["suggested_start"] = None
    return out


# ---------------------------------------------------------------- 問題判定


def _mentions(text: str, words: tuple[str, ...]) -> bool:
    low = text.lower()
    return any(w in low for w in words)


def claims_imaging(entry: dict) -> bool:
    return any(_mentions(c["name"] + " " + c["target"], IMAGING_WORDS) for c in entry["claims"])


def claims_live(entry: dict) -> bool:
    return any(_mentions(c["name"] + " " + c["target"], LIVE_WORDS) for c in entry["claims"])


def spoiler_already_public(entry: dict, r: dict) -> bool:
    """片頭卡寫的東西，站上顯示的標題／資源名稱本來就寫著嗎？

    Solymosi 這類病例影片的標題本身就是「Chronic lymphocytic thyroiditis - case 85」，
    片頭卡只是把標題再印一次——學員在清單上早就看到了，設 start 也擋不住，
    這種不算需要處理的劇透。真正要抓的是「標題中性、片頭卡卻寫出病理」。
    """
    text = (r.get("spoiler_text") or "").lower()
    words = [w.strip(".,:;()[]/-") for w in text.split()]
    words = [w for w in words if len(w) > 3]
    if not words:
        return False
    shown = (
        (entry.get("title") or "") + " " + " ".join(c["name"] for c in entry["claims"])
    ).lower()
    hit = sum(1 for w in words if w in shown)
    return hit / len(words) >= 0.8


def problems(entry: dict, r: dict) -> list[str]:
    """回傳需要人工複驗的原因清單。空清單代表這支沒被標記。"""
    out = []
    if r.get("error"):
        out.append(f"查核失敗：{r['error']}")
        return out
    if not r.get("has_ultrasound") and entry["_claims_imaging"]:
        out.append("課程宣稱有超音波影像，模型看不到任何超音波畫面")
    if not r.get("is_live_scanning") and entry["_claims_live"]:
        out.append(f"課程宣稱有實機／動態掃描，模型判定為 {r.get('format')}（無動態影像）")
    if not r.get("matches_claim"):
        why = r.get("mismatch_reason") or ""
        out.append("內容與課程宣稱的教學重點對不上" + (f"：{why}" if why else ""))
    if r.get("commercial"):
        out.append("有大段商業推銷")
    if (
        r.get("spoiler_in_opening")
        and any(c.get("start") is None for c in entry["claims"])
        # start 只有在真的有東西可以跳過時才有意義；1～2 秒的片頭卡設了也沒差
        and (r.get("suggested_start") or 0) >= 3
        and not spoiler_already_public(entry, r)
    ):
        s = r.get("suggested_start")
        quote = f"「{r['spoiler_text']}」" if r.get("spoiler_text") else ""
        out.append(f"片頭 10 秒內疑似劇透{quote}，但課程資料沒設 start（建議 start={s}）")
    return out


# ---------------------------------------------------------------- 主流程


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="用 Gemini 查核影片內容是否符合課程宣稱")
    p.add_argument("--json", action="store_true", help="輸出機器可讀 JSON 到 stdout")
    p.add_argument("--only", metavar="CHAPTER", help="只查某一章（例如 ch12）")
    p.add_argument("--limit", type=int, metavar="N", help="這次最多查幾支（省錢用）")
    p.add_argument("--refresh", action="store_true", help="忽略快取，全部重查")
    p.add_argument("--dry-run", action="store_true", help="只列出這次會查哪些影片，不打 API")
    p.add_argument("--model", default=DEFAULT_MODEL, help=f"Gemini 模型（預設 {DEFAULT_MODEL}）")
    p.add_argument("--fps", type=float, default=DEFAULT_FPS, help=f"取樣頻率（預設 {DEFAULT_FPS}）")
    p.add_argument("--out", type=Path, default=REPORT, help="報告路徑")
    return p.parse_args(argv)


def load_cache(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text()).get("results") or {}
    except Exception:
        return {}


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    out_json = args.json

    key = load_env_key()
    if not key:
        msg = "略過影片內容查核：找不到 GEMINI_API_KEY（在 .env 設好後再跑 make verify-content）"
        print(json.dumps({"skipped": msg}, ensure_ascii=False) if out_json else f"– {msg}")
        return 0

    if not COURSE_JSON.exists():
        print(f"✗ 找不到 {COURSE_JSON}，請先跑 make build")
        return 1

    course = json.loads(COURSE_JSON.read_text())
    videos = collect(course, args.only)
    # 標記與 scope 統計要看**整門課**，不能只看這次的 --only 範圍：
    # 否則 `--only ch2` 會讓報告自稱 flagged: 0，把先前查出來的問題整批藏起來
    all_videos = collect(course, None) if args.only else videos
    if args.only and not videos:
        print(f"✗ --only {args.only} 沒有對到任何章節")
        return 1
    # all_videos 是 videos 的超集（--only 時），兩邊都要有 _claims_* 才算得出 problems
    for e in all_videos.values():
        e["_claims_imaging"] = claims_imaging(e)
        e["_claims_live"] = claims_live(e)
    if all_videos is not videos:
        for e in videos.values():
            e["_claims_imaging"] = claims_imaging(e)
            e["_claims_live"] = claims_live(e)

    cache = {} if args.refresh else load_cache(args.out)
    fresh = {
        vid: cache[vid]
        for vid, e in videos.items()
        if vid in cache
        and not cache[vid].get("error")
        and cache[vid].get("last_verified") == e["last_verified"]
        and cache[vid].get("model") == args.model
        # 問法改過就等於是另一個檢查，舊答案不能算數
        and cache[vid].get("prompt_version") == PROMPT_VERSION
    }
    todo = [e for vid, e in videos.items() if vid not in fresh]
    if args.limit is not None:
        todo = todo[: max(args.limit, 0)]

    if not out_json:
        print(
            f"影片內容查核：{len(videos)} 支候選（快取命中 {len(fresh)}，這次查 {len(todo)}）"
            f"，模型 {args.model}、取樣 {args.fps} fps、併發 {MAX_WORKERS}\n"
        )

    if args.dry_run:
        payload = [
            {
                "videoId": e["videoId"],
                "url": e["url"],
                "title": e["title"],
                "duration": e["duration"],
                "units": sorted({f"{c['chapter']} {c['unit']}" for c in e["claims"]}),
            }
            for e in todo
        ]
        if out_json:
            print(json.dumps({"dry_run": payload}, ensure_ascii=False, indent=1))
        else:
            for p in payload:
                print(f"  · {p['videoId']}  {p['duration'] or '?'}  {(p['title'] or '')[:60]}")
            print(f"\n（--dry-run：沒有送出任何請求；這 {len(todo)} 支才是要花錢的）")
        return 0

    results: dict[str, dict] = dict(fresh)
    if todo:
        now = datetime.now(UTC).isoformat(timespec="seconds")

        def run(entry: dict) -> tuple[str, dict]:
            r = ask_gemini(entry, key, args.model, args.fps)
            r.update(
                {
                    "videoId": entry["videoId"],
                    "url": entry["url"],
                    "title": entry["title"],
                    "channel": entry["channel"],
                    "last_verified": entry["last_verified"],
                    "model": args.model,
                    "fps": args.fps,
                    "prompt_version": PROMPT_VERSION,
                    "checked_at": now,
                    "claims": entry["claims"],
                }
            )
            if not out_json:
                mark = "✗" if r.get("error") else ("!" if problems(entry, r) else "✓")
                print(f"  {mark} {entry['videoId']}  {(entry['title'] or '')[:60]}", flush=True)
            return entry["videoId"], r

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            results.update(dict(pool.map(run, todo)))

    report = {
        "checked": datetime.now(UTC).isoformat(timespec="seconds"),
        "model": args.model,
        "disclaimer": DISCLAIMER,
        "scope": {
            "candidates": len(all_videos),
            "candidates_in_scope": len(videos),
            "chapter": args.only,
            "fps": args.fps,
        },
        "results": dict(sorted(results.items())),
    }

    # 快取要保留這次沒查到的舊結果，否則下次又要重查（全量一輪約 US$8）。
    # 只有「全量 refresh」——沒有 --only 也沒有 --limit——才可以整份重建；
    # `--refresh --only ch12` 是「把 ch12 重查一次」，不是「把其他章丟掉」。
    full_refresh = args.refresh and not args.only and not args.limit
    if not full_refresh:
        report["results"] = dict(sorted((load_cache(args.out) | report["results"]).items()))

    # 標記原因要寫進檔案，而且必須在合併之後算——這份報告的用途就是「待人工複驗」，
    # 只印在終端機等於一關掉視窗就沒人記得要複驗什麼。
    flagged = {}
    for vid, r in report["results"].items():
        if vid not in all_videos:
            continue
        ps = problems(all_videos[vid], r)
        if ps:
            r["problems"] = ps
            flagged[vid] = ps
        else:
            r.pop("problems", None)

    report["scope"]["verified"] = len(report["results"])
    report["scope"]["flagged"] = len(flagged)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n")

    if out_json:
        print(
            json.dumps(
                {
                    "checked": report["checked"],
                    "model": args.model,
                    "disclaimer": DISCLAIMER,
                    "scope": report["scope"],
                    "flagged": {
                        vid: {
                            "url": results[vid]["url"],
                            "title": results[vid].get("title"),
                            "problems": p,
                            "notes": results[vid].get("notes"),
                            "confidence": results[vid].get("confidence"),
                            "format": results[vid].get("format"),
                            "units": [f"{c['chapter']} {c['unit']}" for c in videos[vid]["claims"]],
                        }
                        for vid, p in flagged.items()
                    },
                    "report": str(args.out),
                },
                ensure_ascii=False,
                indent=1,
            )
        )
        return 0

    print()
    if flagged:
        print(f"! {len(flagged)} 支需要人工複驗：\n")
        for vid, probs in flagged.items():
            # 讀合併後的結果與全課索引：flagged 現在涵蓋整門課，
            # 不只這一次 --only 範圍內查到的那幾支
            r = report["results"][vid]
            where = "、".join(
                dict.fromkeys(f"{c['chapter']} {c['unit']}" for c in all_videos[vid]["claims"])
            )
            print(f"   {where} · {(r.get('title') or vid)[:70]}")
            print(f"      {r['url']}")
            for p in probs:
                print(f"      – {p}")
            if r.get("notes"):
                conf = r.get("confidence") or "?"
                print(f"      模型看到：{r['notes']}（把握度 {conf}）")
            print()
    else:
        print("✓ 這批影片沒有被標記出問題（不代表都合格，見下方說明）")

    lang = {}
    for r in results.values():
        if not r.get("error"):
            lang[r.get("format") or "?"] = lang.get(r.get("format") or "?", 0) + 1
    if lang:
        print("形式分佈：" + "、".join(f"{k} {v}" for k, v in sorted(lang.items())))
    spent = sum(results[e["videoId"]].get("tokens") or 0 for e in todo)
    if spent:
        print(
            f"這次用掉 {spent:,} tokens（{len(todo)} 支，平均 {spent // max(len(todo), 1):,}／支）"
        )
    print(f"\n報告：{args.out}")
    print(f"⚠ {DISCLAIMER}")
    # 這是輔助訊號，不是門檻：標記不代表影片不合格，所以不讓 make 失敗
    return 0


if __name__ == "__main__":
    sys.exit(main())
