#!/usr/bin/env python
import argparse, orjson
from tools.util import read_ndjson, write_ndjson, now_iso
from tools.validators import validate_urls

# Simple local heuristic generator (replace with real LLM call later)
def suggest_paths(observed):
    seeds = set(['/api/health','/healthz','/metrics','/.well-known/openid-configuration','/graphql'])
    for u in observed:
        if '/v1/' in u:
            parts = u.split('/v1/', 1)
            seeds.add(parts[0] + '/v2/' + parts[1])
            seeds.add(u.rstrip('/') + '/search')
            seeds.add(u.rstrip('/') + '/export')
        if '/api/' in u:
            seeds.add(u.rstrip('/') + '/health')
            seeds.add(u.rstrip('/') + '/status')
    return sorted(seeds)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp', required=True)
    ap.add_argument('--out', dest='outp', required=True)
    args = ap.parse_args()

    observed = [it['url'] for it in read_ndjson(args.inp)]

    # group by base
    from urllib.parse import urlparse
    by_base = {}
    for u in observed:
        try:
            p = urlparse(u)
            base = f"{p.scheme}://{p.netloc}"
            by_base.setdefault(base, []).append(u)
        except Exception:
            pass

    out_items = []
    for base, urls in by_base.items():
        paths = suggest_paths(urls[:50])
        cands = [(base.rstrip('/') + p if p.startswith('/') else base.rstrip('/') + '/' + p) for p in paths]
        import anyio
        results = anyio.run(validate_urls, cands)
        ts = now_iso()
        for url, (ok, sc, clen) in results.items():
            out_items.append({
                'url': url,
                'reason': 'heuristic-LLM-stub',
                'score': 0.7 if ok else 0.4,
                'validated': bool(ok),
                'status': sc,
                'content_length': clen,
                'validator': 'HEAD|GET',
                'derived_from': urls[:5],
                'ts': ts
            })

    write_ndjson(args.outp, out_items)
    print(f"wrote {args.outp} ({len(out_items)} lines)")

if __name__ == '__main__':
    main()
