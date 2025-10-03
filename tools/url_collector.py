#!/usr/bin/env python
import argparse, subprocess, re, sys, time
from urllib.parse import urlparse
from tools.util import write_ndjson, now_iso
WB_API = "https://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&collapse=urlkey"


# Minimal: call GAU/waybackurls if present; else fallback to naive seeds


def run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
        return out.splitlines()
    except Exception:
        return []


RE_HTTP = re.compile(r"^https?://", re.I)


def normalize(u):
    if not RE_HTTP.search(u):
        u = "http://" + u
    return u


def from_gau(domain):
    return run_cmd(f"gau --threads 20 {domain} || true")


def from_waybackurls(domain):
    return run_cmd(f"waybackurls {domain} || true")


def make_records(urls, source):
    ts = now_iso()
    for u in urls:
        yield {
            "url": u.strip(),
            "source": source,
            "first_seen": ts,
            "depth": 0,
            "from_js": False,
            "from_sourcemap": False,
            "parent": None,
        }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domains", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()


    with open(args.domains) as f:
        domains = [l.strip() for l in f if l.strip()]


    all_recs = []
    for d in domains:
        g = from_gau(d)
        w = from_waybackurls(d)
        if not g and not w:
            # minimal seed
            g = [f"https://{d}/", f"http://{d}/robots.txt"]
        all_recs.extend(make_records(g, "gau"))
        all_recs.extend(make_records(w, "wayback"))


    write_ndjson(args.out, all_recs)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()