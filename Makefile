    OUT ?= data
    DOMAINS ?= domains.txt
    PY := .venv/bin/python

    run: $(OUT)
	$(PY) tools/url_collector.py --domains $(DOMAINS) --out $(OUT)/urls.ndjson
	$(PY) tools/js_crawler.py --in $(OUT)/urls.ndjson --out $(OUT)/urls.ndjson --dedupe
	$(PY) tools/llm_url_expander.py --in $(OUT)/urls.ndjson --out $(OUT)/url_candidates.ndjson
	$(PY) - <<'PY'
import json,sys
json.dump({"note":"compute real metrics later"}, open("$(OUT)/metrics.json","w"))
print("Wrote $(OUT)/metrics.json")
PY

    $(OUT):
	mkdir -p $(OUT)

    format:
	ruff check --fix || true
	ruff format || true
