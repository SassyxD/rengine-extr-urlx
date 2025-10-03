#!/usr/bin/env python 
import argparse, re, anyio, httpx from selectolax.parser import HTMLParser from tools.util import read_ndjson, write_ndjson, now_iso

SCRIPT_RE = re.compile(r"<script[^>]+src="([^"]+)"", re.I) SRCMAP_RE = re.compile(r"//# sourceMappingURL=([^\n]+)") URL_RE = re.compile(r"(?:(?:/|https?://)[a-zA-Z0-9_-./]+).(?:php|asp|aspx|jsp|json|xml|html|txt|map|zip|bak)") API_HINT = re.compile(r"/(api|v\d+|graphql|admin|internal|health|status|auth|users|orders|search)\b", re.I)

ALLOW = {200,204,301,302}

async def fetch_text(client, url): try: r = await client.get(url, follow_redirects=True) if r.status_code in ALLOW: return r.text except Exception: return None

async def process_page(client, url): text = await fetch_text(client, url) if not text: return [], [] html = HTMLParser(text) scripts = [n.attributes.get('src') for n in html.css('script[src]') if n.attributes.get('src')] # also regex fallback for m in SCRIPT_RE.finditer(text): scripts.append(m.group(1)) return list(dict.fromkeys(scripts)), html

async def process_js(client, base_url, js_url): try: if js_url.startswith('/'): from urllib.parse import urljoin js_url = urljoin(base_url, js_url) r = await client.get(js_url, follow_redirects=True) if r.status_code not in ALLOW: return [] , [] body = r.text candidates = set() for m in URL_RE.finditer(body): u = m.group(0) if API_HINT.search(u): candidates.add(u) sm = [] sm_m = SRCMAP_RE.search(body) if sm_m: sm = [sm_m.group(1)] return list(candidates), sm except Exception: return [], []

async def main_async(inp, outp, dedupe): seen = set() records = [] async with httpx.AsyncClient(timeout=10) as client: pages = [it['url'] for it in read_ndjson(inp)] async with anyio.create_task_group() as tg: async def handle(u): scripts, _ = await process_page(client, u) for s in scripts: endpoints, smaps = await process_js(client, u, s) ts = now_iso() for ep in endpoints: url = ep if ep.startswith('http') else u.rstrip('/') + '/' + ep.lstrip('/') if dedupe and url in seen: continue seen.add(url) records.append({ 'url': url, 'source': 'js', 'first_seen': ts, 'depth': 1, 'from_js': True, 'from_sourcemap': False, 'parent': s }) for sm in smaps: sm_url = sm if sm.startswith('http') else u.rstrip('/') + '/' + sm.lstrip('/') if dedupe and sm_url in seen: continue seen.add(sm_url) records.append({ 'url': sm_url, 'source': 'sourcemap', 'first_seen': ts, 'depth': 1, 'from_js': False, 'from_sourcemap': True, 'parent': s }) for p in pages: tg.start_soon(handle, p) write_ndjson(outp, records) print(f"appended JS-derived to {outp}")

if name == 'main': ap = argparse.ArgumentParser() ap.add_argument('--in', dest='inp', required=True) ap.add_argument('--out', dest='outp', required=True) ap.add_argument('--dedupe', action='store_true') a = ap.parse_args() anyio.run(main_async, a.inp, a.outp, a.dedupe)