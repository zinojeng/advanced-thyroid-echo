PY := uv run python
COURSE ?= course
DIST ?= dist
PORT ?= 8899
PROJECT ?= $(shell $(PY) -c "import json;print(json.load(open('$(COURSE)/course.config.json'))['site']['project'])")

export COURSE
export DIST

.DEFAULT_GOAL := help

help: ## 列出可用指令
	@grep -E '^[a-z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

build: ## 合併資料 → public/course.json，含配額驗證與 SEO 產出
	$(PY) src/build/build.py

icons: ## 重新下載 Lucide 圖示並打包成內嵌 sprite
	$(PY) src/build/build_icons.py

og: ## 用 headless Chrome 重新產生社群預覽圖
	@"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
		--headless --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
		--window-size=1200,630 --screenshot="$(PWD)/$(DIST)/og.png" "$(PWD)/src/web/og.html"
	@# headless Chrome 以 2x 出圖，要縮回 og:image 宣告的 1200x630。
	@# ImageMagick 不是每台機器都有，macOS 內建的 sips 可以頂替。
	@if command -v magick >/dev/null 2>&1; then \
		magick $(DIST)/og.png -resize 1200x630 -strip $(DIST)/og.png; \
	elif command -v sips >/dev/null 2>&1; then \
		sips -Z 1200 $(DIST)/og.png --out $(DIST)/og.png >/dev/null; \
	else \
		echo "⚠ 找不到 magick 或 sips，og.png 維持 2x 尺寸（社群平台仍可用，但與 og:image 宣告的尺寸不符）"; \
	fi
	@echo "→ $(DIST)/og.png"

meta: ## 用 yt-dlp 補齊 video-meta.json（長度、觀看數、頻道）
	$(PY) src/build/fetch_meta.py

counter: ## 建立瀏覽次數用的 D1 資料庫並寫出 wrangler 綁定（冪等，可重跑）
	$(PY) src/build/setup_counter.py

audit: ## 離線稽核設定檔、配額、影片長度與實證深度（確定性，不打網路）
	$(PY) src/build/audit.py

verify: ## 重驗所有影片連結與 PubMed 引用（打真實 API，會跑一陣子）
	$(PY) src/build/verify_links.py
	$(PY) src/build/verify_refs.py

verify-external: ## 重驗非 YouTube 來源（學會、期刊、醫院、病例圖譜）的連結狀態
	$(PY) src/build/verify_external.py

registry: ## 合併各章搜尋紀錄成 SOURCE-REGISTRY.json
	$(PY) src/build/merge_registry.py

gaps: ## 列出誠實留空的欄位、需登入的來源與證據不足的主題
	$(PY) src/build/gaps.py

ratings: ## 讀線上評價，印出建議換片的影片清單（低分且有具體原因）
	$(PY) src/build/ratings.py

serve: ## 本機預覽
	@echo "→ http://localhost:$(PORT)"
	@$(PY) -m http.server $(PORT) --directory $(DIST)

deploy: build ## 建置後部署到 Cloudflare Pages
	npm exec --yes -- wrangler@4 pages deploy $(DIST) \
		--project-name $(PROJECT) --branch main --commit-dirty=true

lint: ## ruff 檢查
	uv run ruff check .

fmt: ## ruff 格式化
	uv run ruff format .
	uv run ruff check --fix .

check: lint build audit ## 提交前跑這個（含離線稽核）

clean: ## 清掉建置暫存
	rm -rf .tmp .wrangler .ruff_cache dist **/__pycache__

.PHONY: help build icons og meta counter audit verify verify-external registry gaps ratings serve deploy lint fmt check clean
