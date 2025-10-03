import os, anyio, httpx

TIMEOUT = float(os.getenv("HTTP_TIMEOUT", 10)) CONC = int(os.getenv("HTTP_CONCURRENCY", 20)) UA = os.getenv("USER_AGENT", "urlx/0.1")

ALLOW = {200,204,301,302,401,403,405}

async def _check_one(client, url): try: r = await client.head(url, follow_redirects=True) if r.status_code not in ALLOW: r = await client.get(url, follow_redirects=True) ok = r.status_code in ALLOW clen = int(r.headers.get("content-length", "0") or 0) return ok, r.status_code, clen except Exception: return False, 0, 0

async def validate_urls(urls): results = {} limits = anyio.CapacityLimiter(CONC) async with httpx.AsyncClient(timeout=TIMEOUT, headers={"User-Agent": UA}) as client: async def worker(u): async with limits: ok, sc, clen = await _check_one(client, u) results[u] = (ok, sc, clen) async with anyio.create_task_group() as tg: for u in urls: tg.start_soon(worker, u) return results