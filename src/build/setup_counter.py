#!/usr/bin/env python3
"""一次把瀏覽次數計數器的雲端資源建好：D1 資料庫 → 建表 → 寫出 wrangler 設定。

冪等：重跑會沿用已存在的資料庫，不會重建、不會清空數字。

用法：
    make counter
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COURSE = ROOT / os.environ.get("COURSE", "course")
CFG = json.loads((COURSE / "course.config.json").read_text())
PROJECT = CFG["site"]["project"]
DB_NAME = f"{PROJECT}-hits"
WRANGLER = ["npx", "--yes", "wrangler@4"]


def run(args: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(WRANGLER + args, capture_output=True, text=True, timeout=300, **kw)


def find_db() -> str | None:
    """回傳既有資料庫的 uuid，沒有就 None。"""
    proc = run(["d1", "list", "--json"])
    try:
        for db in json.loads(proc.stdout):
            if db.get("name") == DB_NAME:
                return db.get("uuid") or db.get("database_id")
    except json.JSONDecodeError:
        pass
    return None


def create_db() -> str | None:
    proc = run(["d1", "create", DB_NAME])
    out = proc.stdout + proc.stderr
    m = re.search(r"database_id\s*=\s*\"([0-9a-f-]{36})\"", out) or re.search(
        r"\"database_id\"\s*:\s*\"([0-9a-f-]{36})\"", out
    )
    if m:
        return m.group(1)
    print(out.strip()[-600:], file=sys.stderr)
    return None


def main() -> int:
    # 同一個 D1 資料庫同時服務瀏覽次數與影片評價，兩個功能都是選用的。
    # 只要其中一個有設定就該把資料庫建起來——原本只看 counter，
    # 導致「只開評價、不要瀏覽次數」的課程建不了資料庫。
    features = [k for k in ("counter", "ratings") if k in CFG]
    if not features:
        print(
            "✗ course.config.json 沒有 counter 也沒有 ratings 區塊——"
            "這兩個功能都是選用的，至少加一個再跑",
            file=sys.stderr,
        )
        return 1
    print(f"啟用的功能：{'、'.join(features)}")

    print(f"專案 {PROJECT} · 資料庫 {DB_NAME}")

    db_id = find_db()
    if db_id:
        print(f"  ✓ 沿用既有資料庫 {db_id}")
    else:
        print("  · 建立資料庫…")
        db_id = create_db()
        if not db_id:
            print("✗ 建立失敗，請看上面的錯誤訊息（多半是還沒 wrangler login）", file=sys.stderr)
            return 1
        print(f"  ✓ 已建立 {db_id}")

    print("  · 套用 schema（CREATE TABLE IF NOT EXISTS，不會清掉既有數字）…")
    proc = run(
        ["d1", "execute", DB_NAME, "--file", "functions/schema.sql", "--remote", "-y"], cwd=ROOT
    )
    if proc.returncode != 0:
        print((proc.stdout + proc.stderr).strip()[-600:], file=sys.stderr)
        return 1
    print("  ✓ schema 就緒")

    cfg_path = ROOT / "wrangler.jsonc"
    cfg_path.write_text(
        json.dumps(
            {
                "name": PROJECT,
                "pages_build_output_dir": os.environ.get("DIST", "dist"),
                "compatibility_date": "2025-01-01",
                "d1_databases": [
                    {"binding": "HITS", "database_name": DB_NAME, "database_id": db_id}
                ],
            },
            indent=2,
        )
        + "\n"
    )
    print(f"  ✓ 已寫出 {cfg_path.relative_to(ROOT)}（含 D1 綁定，已被 gitignore）")
    print("\n接著跑 `make deploy`，徽章就會出現在 header。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
