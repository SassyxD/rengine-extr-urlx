import os, time, orjson, sys
from datetime import datetime, timezone


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def write_ndjson(path, items):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "ab") as f:
        for it in items:
            f.write(orjson.dumps(it) + b"\n")


def read_ndjson(path):
    with open(path, "rb") as f:
        for line in f:
            if line.strip():
                yield orjson.loads(line)