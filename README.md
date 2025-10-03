# rengine-ext-urlx (Task 2 + 7)


Add-on pipeline for rengine to:
1) Collect more URLs (Wayback, GAU, HTML crawl, JS-aware extraction, sourcemaps)
2) Expand endpoints using LLM suggestions (Task 7) with validation


## Quickstart


# 0) Setup
cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
npm install


# 1) Run end-to-end (domain list in domains.txt)
make run DOMAINS=domains.txt OUT=data


# 2) Review outputs
- data/urls.ndjson # ground-truth URLs found by collectors/crawler
- data/url_candidates.ndjson # LLM-suggested endpoints + validation
- data/metrics.json # discovery lift & validation stats


## Integration with rengine
- Push NDJSON into rengine scope via DB writer or webhook (out of scope here)
- Tag sources: source=crawler|js|sourcemap|llm


## Notes
- GAU/wayback binaries optional; we fallback to APIs when possible
- LLM provider is pluggable via env (OpenAI/local); or skip with --no-llm