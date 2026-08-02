#!/usr/bin/env python3
"""驗證非 YouTube 來源的連結是否真的存在（YouTube 的部分交給 verify_links.py）。

醫學教育資源多半在學會、期刊、醫院教學站與病例圖譜，沒有 oEmbed 可查。
這裡實際發出請求，記錄：HTTP 狀態、重導向鏈、最終網址、網域、content-type、
頁面標題、是否疑似需要登入。**不信任策展 agent 說「我查過了」**。

用法：
    python3 verify_external.py               # 驗證並列出問題
    python3 verify_external.py --json        # 機器可讀報告
    python3 verify_external.py --stamp       # 把通過的連結 last_verified 更新為今天（改 course/data/）
"""

from __future__ import annotations

import contextlib
import datetime
import html
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sources as SRC

ROOT = Path(__file__).resolve().parents[2]
COURSE = Path(os.environ.get("COURSE") or ROOT / "course").resolve()
DATA = COURSE / "data"
DIST = Path(os.environ.get("DIST") or ROOT / "dist").resolve()
COURSE_JSON = DIST / "course.json"
REPORT = DATA / "external-verify.json"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0 Safari/537.36"
)
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
CANON = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', re.I)
LOGIN_HINTS = re.compile(
    r"sign in to continue|please log ?in|subscription required|purchase access|"
    r"institutional login|member login|create an account to",
    re.I,
)


# 小型期刊站（例如 kjronline.org）承受不住 8 條連線同時打過去，會直接斷線——
# 那不是連結失效，是我們太粗魯。每個網域一次只發一個請求，並在請求之間留間隔。
_HOST_LOCKS: dict[str, threading.Lock] = {}
_LOCKS_GUARD = threading.Lock()
HOST_DELAY = 0.7


def _host_lock(url: str) -> threading.Lock:
    host = urllib.parse.urlparse(url).netloc.lower()
    with _LOCKS_GUARD:
        return _HOST_LOCKS.setdefault(host, threading.Lock())


CHROME = re.compile(r"<(nav|header|footer)\b.*?</\1>", re.I | re.S)


def strip_chrome(text: str) -> str:
    """去掉導覽列、頁首與頁尾再找登入牆。

    幾乎每個學會網站的導覽列都有「Please login」，那是站台的會員入口，
    不代表這一頁需要登入。不先拿掉，偵測器會把一半的公開頁面誤報成付費牆。
    """
    return CHROME.sub(" ", text)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """自己跟重導向，才記得住整條鏈。"""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(url: str, retries: int = 2) -> dict:
    """同一網域序列化請求；連線層失敗會退避重試，避免把伺服器的節流誤判成死連結。"""
    with _host_lock(url):
        try:
            return _fetch(url, retries)
        finally:
            time.sleep(HOST_DELAY)


def _fetch(url: str, retries: int) -> dict:
    out = {"url": url, "ok": False, "status": None, "redirects": [], "final_url": url}
    opener = urllib.request.build_opener(NoRedirect)
    seen = []
    cur = url
    for _ in range(6):
        req = urllib.request.Request(
            cur,
            headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml,application/pdf,*/*",
                "Accept-Language": "en,zh-TW;q=0.8",
                "Accept-Encoding": "gzip",
            },
        )
        try:
            res = opener.open(req, timeout=25)
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308) and e.headers.get("Location"):
                nxt = urllib.parse.urljoin(cur, e.headers["Location"])
                seen.append(nxt)
                cur = nxt
                continue
            out["status"] = e.code
            out["note"] = {
                403: "被擋（可能是 bot 防護，需人工確認）",
                404: "頁面不存在",
                410: "已移除",
            }.get(e.code, f"HTTP {e.code}")
            # 403 常常只是 WAF 擋 bot，網頁對真人是活的——標為待人工確認而非死連結
            out["manual"] = e.code in (403, 429)
            out["redirects"] = seen
            out["final_url"] = cur
            return out
        except Exception as e:
            # 一次網路抖動不該被寫成「連結失效」——重試一次再判定
            if retries > 0:
                time.sleep(2.0 * (3 - retries))  # 2s、4s 退避
                return _fetch(url, retries - 1)
            out["note"] = f"連線失敗：{type(e).__name__}"
            out["redirects"] = seen
            return out

        body = res.read(400_000)
        if res.headers.get("Content-Encoding") == "gzip":
            # 我們只讀前 400 KB，gzip 串流一定是截斷的——用 decompressobj 才能
            # 拿到已解出的部分；gzip.decompress() 會因為找不到結尾標記而丟 EOFError。
            with contextlib.suppress(zlib.error, OSError, EOFError):
                body = zlib.decompressobj(zlib.MAX_WBITS | 16).decompress(body)
        text = body.decode("utf-8", "replace")
        out.update(
            ok=True,
            status=res.status,
            redirects=seen,
            final_url=res.geturl(),
            domain=urllib.parse.urlparse(res.geturl()).netloc,
            content_type=(res.headers.get("Content-Type") or "").split(";")[0].strip(),
        )
        if m := TITLE.search(text):
            out["title"] = html.unescape(re.sub(r"\s+", " ", m.group(1))).strip()[:160]
        if m := CANON.search(text):
            out["canonical"] = html.unescape(m.group(1))
        out["login_wall"] = bool(LOGIN_HINTS.search(strip_chrome(text)))
        return out
    out["note"] = "重導向次數過多"
    out["redirects"] = seen
    return out


def walk(course: dict):
    for ch in course["chapters"]:
        for u in ch["units"]:
            for les in u.get("lessons") or ([u["lesson"]] if u.get("lesson") else []):
                yield ch["code"], u["id"], "主課", les
            for d in u.get("drills") or []:
                yield ch["code"], u["id"], d.get("name", "?"), d


def stamp(passed: set[str]) -> int:
    """把驗證通過的連結在 course/data/*.json 裡的 last_verified 更新為今天。"""
    today = datetime.date.today().isoformat()
    touched = 0
    for path in sorted(DATA.glob("*.json")):
        if path.name in ("video-meta.json", "external-verify.json"):
            continue
        try:
            blob = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        changed = _stamp_node(blob, passed, today)
        if changed:
            path.write_text(json.dumps(blob, ensure_ascii=False, indent=1) + "\n")
            touched += changed
    return touched


def _stamp_node(node, passed: set[str], today: str) -> int:
    """就地更新 last_verified，回傳改了幾個欄位。"""
    changed = 0
    if isinstance(node, dict):
        if node.get("url") in passed and node.get("last_verified") != today:
            node["last_verified"] = today
            changed += 1
        for v in node.values():
            changed += _stamp_node(v, passed, today)
    elif isinstance(node, list):
        for v in node:
            changed += _stamp_node(v, passed, today)
    return changed


def main() -> int:
    as_json = "--json" in sys.argv
    do_stamp = "--stamp" in sys.argv

    if not COURSE_JSON.exists():
        print("找不到 dist/course.json，先跑 make build", file=sys.stderr)
        return 1
    course = json.loads(COURSE_JSON.read_text())

    nodes = [(c, u, lbl, v) for c, u, lbl, v in walk(course) if v.get("url")]
    urls = sorted({v["url"] for *_, v in nodes if not SRC.is_youtube(v)})
    if not urls:
        print("沒有非 YouTube 來源，不用驗。")
        return 0

    if not as_json:
        print(f"檢查 {len(urls)} 個外部連結…\n")

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = {r["url"]: r for r in pool.map(fetch, urls)}

    dead = {u: r for u, r in results.items() if not r["ok"] and not r.get("manual")}
    manual = {u: r for u, r in results.items() if r.get("manual")}
    walled = {u: r for u, r in results.items() if r.get("ok") and r.get("login_wall")}
    passed = {u for u, r in results.items() if r["ok"]}

    REPORT.write_text(
        json.dumps(
            {"checked": datetime.date.today().isoformat(), "results": results},
            ensure_ascii=False,
            indent=1,
        )
        + "\n"
    )

    if as_json:
        print(
            json.dumps(
                {
                    "ok": not dead,
                    "total": len(urls),
                    "dead": list(dead),
                    "manual": list(manual),
                    "login_wall": list(walled),
                },
                ensure_ascii=False,
                indent=1,
            )
        )
        return 1 if dead else 0

    for label, group, mark in (
        ("失效", dead, "✗"),
        ("被 bot 防護擋下，需人工開一次確認", manual, "⚠"),
        ("疑似需要登入或訂閱（課程頁面必須標示 access）", walled, "⚠"),
    ):
        if not group:
            continue
        print(f"{mark} {len(group)} 個連結{label}：")
        for code, uid, lbl, v in nodes:
            if v["url"] in group:
                r = group[v["url"]]
                print(f"   {code} {uid} · {lbl}")
                print(f"      {v['url']} — {r.get('note') or r.get('title') or ''}")
        print()

    ok = len(passed)
    print(
        f"通過 {ok} / {len(urls)}（{ok / len(urls) * 100:.1f}%）· 報告寫入 {REPORT.relative_to(ROOT)}"
    )

    if do_stamp:
        n = stamp(passed)
        print(f"→ 已更新 {n} 個欄位的 last_verified 為今天")

    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
