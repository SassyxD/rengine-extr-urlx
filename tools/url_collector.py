#!/usr/bin/env python
import argparse, subprocess
from tools.util import write_ndjson, now_iso

def run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
        return out.splitlines()
    except Exception:
        return []

def make_records(urls, source):
    ts = now_iso()
    for u in urls:
        u = u.strip()
        if not u:
            continue
        yield {
            "url": u,
            "source": source,
            "first_seen": ts,
            "depth": 0,
            "from_js": False,
            "from_sourcemap": False,
            "parent": None
        }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domains", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    domains = [l.strip() for l in open(args.domains) if l.strip()]
    all_recs = []
    for d in domains:
        g = run_cmd(f"gau --threads 20 {d} || true")
        w = run_cmd(f"waybackurls {d} || true")
        if not g and not w:
            g = [f"https://{d}/", f"http://{d}/robots.txt"]
        all_recs.extend(make_records(g, "gau"))
        all_recs.extend(make_records(w, "wayback"))

    write_ndjson(args.out, all_recs)
    print(f"wrote {args.out}")

if __name__ == "__main__":
    main()
