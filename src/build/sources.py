#!/usr/bin/env python3
"""來源判定：把「什麼算合法連結」從 YouTube 專屬抽成可插拔規則。

原框架只認 `youtube.com/watch?v=`。醫學教育資源散在學會、期刊、醫院教學站與
病例圖譜，多數不是 YouTube，也不見得可嵌入。build / audit / verify_external
共用這裡的規則，避免三個地方各寫一份而慢慢走鐘。
"""

from __future__ import annotations

import re

PROVIDERS = (
    "youtube",
    "vimeo",
    "society",  # 專業學會（ATA / ETA / ACR / KSThR …）
    "journal",  # 期刊與其 supplementary video
    "hospital",  # 大學醫院、fellowship program 教學站
    "case_library",  # Radiopaedia 等病例／影像圖譜
    "external",  # 其他（含廠商教育內容）
)

SOURCE_TYPES = ("video", "webinar", "case", "atlas", "guideline", "article", "quiz")

ACCESS = ("open", "registration", "subscription", "institutional")

TIERS = ("A", "B", "C")

# 這門課是影音課程：每個資源欄位都必須是「看得到的影片」。
# 期刊原文與指引 PDF 仍然重要，但它們的位置在實證層（citations）與
# GUIDELINE-MATRIX.md，不是課程的資源欄位。
VIDEO_PROVIDERS = ("youtube", "vimeo", "society", "hospital", "external")
VIDEO_SOURCE_TYPES = ("video", "webinar")

YT = re.compile(
    r"^https://(?:www\.)?youtube\.com/watch\?v=[\w-]{11}(?:&\S*)?$|^https://youtu\.be/[\w-]{11}"
)
VIMEO = re.compile(r"^https://(?:www\.)?vimeo\.com/\d+")
HTTPS = re.compile(r"^https://[^\s\"'<>]+$")

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def youtube_id(url: str | None) -> str | None:
    m = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", url or "")
    return m.group(1) if m else None


def vimeo_id(url: str | None) -> str | None:
    m = re.search(r"vimeo\.com/(\d+)", url or "")
    return m.group(1) if m else None


def infer_provider(v: dict) -> str | None:
    """沒寫 provider 就從網址推。沒有網址回 None（誠實留空的格子）。"""
    if v.get("provider"):
        return v["provider"]
    url = v.get("url") or ""
    if not url:
        return None
    if YT.match(url):
        return "youtube"
    if VIMEO.match(url):
        return "vimeo"
    return "external"


def is_youtube(v: dict) -> bool:
    return infer_provider(v) == "youtube"


def url_problem(v: dict) -> str | None:
    """回傳不合法的原因；合法回 None。"""
    url = v.get("url")
    if not url:
        return None
    provider = infer_provider(v)
    if provider not in PROVIDERS:
        return f"provider「{provider}」不在允許清單"
    if provider == "youtube" and not YT.match(url):
        return f"標為 youtube 但不是合法的 watch 網址：{url}"
    if provider == "vimeo" and not VIMEO.match(url):
        return f"標為 vimeo 但不是合法的 vimeo 網址：{url}"
    # provider 是「託管平台」不是「發布機構」。學會把影片放上 YouTube，provider 仍是
    # youtube（發布機構寫在 channel）。標錯會讓這支影片從 oEmbed 驗證漏掉，
    # 改由外部驗證器去打 youtube.com，然後撞上 429 看起來像連結失效。
    if YT.match(url) and provider != "youtube":
        return f"是 YouTube 網址卻標成 {provider}；provider 指的是託管平台，發布機構請寫在 channel"
    if VIMEO.match(url) and provider != "vimeo":
        return f"是 Vimeo 網址卻標成 {provider}；provider 指的是託管平台"
    if not HTTPS.match(url):
        return f"不是 https 網址：{url}"
    return None


def metadata_problems(v: dict) -> list[str]:
    """非 YouTube 來源沒有 oEmbed 可查，中繼資料只能靠策展時填齊。

    YouTube 的長度／頻道／觀看數由 `make meta` 覆寫，這裡不重複要求。
    """
    url = v.get("url")
    if not url:
        return []
    provider = infer_provider(v)
    out = []

    if (st := v.get("source_type")) and st not in SOURCE_TYPES:
        out.append(f"source_type「{st}」不在允許清單")
    if (ac := v.get("access")) and ac not in ACCESS:
        out.append(f"access「{ac}」不在允許清單")
    if (tier := v.get("tier")) and tier not in TIERS:
        out.append(f"tier「{tier}」必須是 A／B／C")
    if (lv := v.get("last_verified")) and not ISO_DATE.match(str(lv)):
        out.append(f"last_verified「{lv}」不是 YYYY-MM-DD")

    if provider != "youtube":
        # YouTube 靠 oEmbed 就能確認公開可看；其他來源必須人工標示存取與授權
        for field in ("source_type", "access", "license", "last_verified"):
            if not v.get(field):
                out.append(f"非 YouTube 來源缺少 {field}")
    return out


def is_video(v: dict) -> bool:
    """這個欄位是不是影音資源。

    判定看 source_type：YouTube／Vimeo 的網址一定是影片；其他平台
    （學會自架播放器、醫院教學站、廠商頻道）要靠 source_type 宣告。
    """
    if infer_provider(v) in ("youtube", "vimeo"):
        return True
    return v.get("source_type") in VIDEO_SOURCE_TYPES


def not_video_reason(v: dict) -> str | None:
    """不是影片就回傳原因；是影片回 None。沒有網址的欄位不在此檢查範圍。"""
    if not v.get("url") or is_video(v):
        return None
    st = v.get("source_type") or "未標示"
    return f"source_type「{st}」不是影音（本課程的資源欄位只收影片，文獻請放實證層）"


def embeddable(v: dict) -> bool:
    """能不能在站內嵌入播放。預設只有 YouTube／Vimeo 可以。"""
    if v.get("embeddable") is not None:
        return bool(v["embeddable"])
    return infer_provider(v) in ("youtube", "vimeo")
