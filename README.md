# rengine-ext-urlx (Task 2 + 7)

Add-on pipeline for rengine:
1) Collect more URLs (Wayback, GAU, HTML crawl, JS extraction, sourcemaps)
2) Expand endpoints via LLM suggestions with HTTP validation

## Quickstart
- python -m venv .venv && source .venv/bin/activate
- pip install -r requirements.txt
- npm install
- cp .env.example .env

# domains.txt contains in-scope roots (one per line)
make run DOMAINS=domains.txt OUT=data

# or 
- python tools/url_collector.py --domains domains.txt --out data/urls.ndjson
- python tools/js_crawler.py --in data/urls.ndjson --out data/urls.ndjson --dedupe
- python tools/llm_url_expander.py --in data/urls.ndjson --out data/url_candidates.ndjson

# check data by using
- wc -l data/urls.ndjson data/url_candidates.ndjson
- head -n 5 data/urls.ndjson
- head -n 5 data/url_candidates.ndjson


Outputs:
- data/urls.ndjson
- data/url_candidates.ndjson
- data/metrics.json

Integration with rengine: import NDJSON via DB/webhook; tag `source=crawler|js|sourcemap|llm`.
