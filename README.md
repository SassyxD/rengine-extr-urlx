# rengine-ext-urlx (Task 2 + 7)

Add-on pipeline for rengine:
1) Collect more URLs (Wayback, GAU, HTML crawl, JS extraction, sourcemaps)
2) Expand endpoints via LLM suggestions with HTTP validation

## Quickstart
- python -m venv .venv && source .venv/bin/activate
- pip install -r requirements.txt
- npm install
cp .env.example .env

# domains.txt contains in-scope roots (one per line)
make run DOMAINS=domains.txt OUT=data

Outputs:
- data/urls.ndjson
- data/url_candidates.ndjson
- data/metrics.json

Integration with rengine: import NDJSON via DB/webhook; tag `source=crawler|js|sourcemap|llm`.
