# rengine-ext-urlx — Task 2 + 7 (Short README)

Add-on for **rengine** to 1) collect more URLs (Wayback/GAU/JS/sourcemaps) and 2) expand endpoints via LLM-style heuristics + HTTP validation. Outputs **NDJSON** ready to import.

---

## Install
```bash
git clone <your-repo> rengine-ext-urlx && cd rengine-ext-urlx
python -m venv .venv && source .venv/bin/activate   # Windows PS: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
npm install
cp .env.example .env
```
**Optional (Go seeds):**
```bash
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/tomnomnom/waybackurls@latest
```

---

## Quick Start
```bash
# in-scope domains
echo "example.com" > domains.txt && echo "api.example.com" >> domains.txt

# output dir
mkdir -p data

# run pipeline (from repo root)
python -m tools.url_collector --domains domains.txt --out data/urls.ndjson
python -m tools.js_crawler --in data/urls.ndjson --out data/urls.ndjson --dedupe
python -m tools.llm_url_expander --in data/urls.ndjson --out data/url_candidates.ndjson
```
**Windows Git Bash tips:** use `/` paths and `source .venv/Scripts/activate`  
**PowerShell:** set `$env:PYTHONPATH = (Get-Location).Path` if module import fails.

---

## Outputs
- `data/urls.ndjson` — collected/crawled URLs
- `data/url_candidates.ndjson` — heuristics + validation (`status`, `validated`, `content_length`)
- `data/metrics.json` — placeholder

---

## Troubleshooting (speedrun)
- `No module named 'tools'` → run from repo root using `python -m ...`
- Backslash swallowed (Git Bash) → use `/` paths
- Python mismatch → use Python **3.11**, recreate `.venv`
