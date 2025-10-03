#!/usr/bin/env python
if not line:
continue
if '/v1/' in line:
seeds.add(line.replace('/v1/', '/v2/'))
seeds.add(line.rstrip('/') + '/search')
seeds.add(line.rstrip('/') + '/export')
if '/api/' in line:
seeds.add(line.rstrip('/') + '/health')
seeds.add(line.rstrip('/') + '/status')
# ensure simple admin/common
seeds.update(['/api/health', '/healthz', '/metrics', '/graphql', '/.well-known/openid-configuration'])
return sorted(seeds)




def main():
ap = argparse.ArgumentParser()
ap.add_argument('--in', dest='inp', required=True)
ap.add_argument('--out', dest='outp', required=True)
args = ap.parse_args()


observed = []
bases = set()
for it in read_ndjson(args.inp):
url = it['url']
observed.append(url)
# derive base
try:
from urllib.parse import urlparse
p = urlparse(url)
bases.add(f"{p.scheme}://{p.netloc}")
except Exception:
pass


# Group observed by base for scoped generation
by_base = {b: [] for b in bases}
for u in observed:
from urllib.parse import urlparse
p = urlparse(u)
base = f"{p.scheme}://{p.netloc}"
by_base[base].append(u)


out_items = []
for base, urls in by_base.items():
prompt = PROMPT_TMPL.format(observed='\n'.join(urls[:50]))
paths = call_llm('\n'.join(urls[:50]))
# attach base
candidates = [ (base.rstrip('/') + p if p.startswith('/') else base.rstrip('/') + '/' + p) for p in paths ]
# validate
import anyio
results = anyio.run(validate_urls, candidates)
ts = now_iso()
for url, (ok, sc, clen) in results.items():
out_items.append({
'url': url,
'reason': 'LLM heuristic',
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