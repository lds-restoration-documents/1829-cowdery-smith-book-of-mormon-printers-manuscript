#!/usr/bin/env python3
"""Politely download every page image of the Printer's Manuscript listed on the Archive Viewer page.
Sequential, one request at a time, 4-7 s random pause between images, resumable (skips files already present and valid),
honours Retry-After, backs off exponentially on 429/5xx, and stops after 5 consecutive failures.
Usage: python3 tools/download_images.py [--limit N] [--delay 4]   -> source-images/ + source-images/manifest.tsv"""
import argparse, random, re, sys, time, urllib.request, urllib.error
from pathlib import Path
VIEWER = 'https://archiveviewer.org/viewer/joseph-smith-papers/printers-manuscript-of-the-book-of-mormon-circa-august-1829-circa-january-1830'
OUT = Path(__file__).resolve().parents[1] / 'source-images'
UA = 'Mozilla/5.0 (personal research download; low rate)'
ap = argparse.ArgumentParser(); ap.add_argument('--limit', type=int, default=0); ap.add_argument('--delay', type=float, default=4.0)
a = ap.parse_args()
def get(url, tries=6):
    wait = 20
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60) as r: return r.read()
        except urllib.error.HTTPError as e:
            ra = e.headers.get('Retry-After'); w = int(ra) if ra and ra.isdigit() else wait
            print(f'  HTTP {e.code}; waiting {w}s', flush=True)
            if e.code not in (429, 500, 502, 503, 504): raise
            time.sleep(w); wait = min(wait * 2, 600)
        except Exception as e:
            print(f'  {type(e).__name__}; waiting {wait}s', flush=True); time.sleep(wait); wait = min(wait * 2, 600)
    raise RuntimeError('gave up on ' + url)
OUT.mkdir(exist_ok=True)
html = get(VIEWER).decode('utf-8', 'replace')
urls = []
for u in re.findall(r'<img src="(https://www\.josephsmithpapers\.org/bc-jsp/content/jsp/images/\d+/[^"]*_download\.jpg)"', html):
    if u not in urls: urls.append(u)
print(len(urls), 'images listed', flush=True)
fails = 0; done = 0
for i, u in enumerate(urls, 1):
    name = u.rsplit('/', 1)[1]; dst = OUT / name
    if dst.exists() and dst.stat().st_size > 10000 and dst.read_bytes()[:3] == b'\xff\xd8\xff': continue
    if a.limit and done >= a.limit: break
    try:
        data = get(u)
        if data[:3] != b'\xff\xd8\xff' or len(data) < 10000: raise ValueError('not a JPEG')
        dst.write_bytes(data); done += 1; fails = 0
        print(f'{i}/{len(urls)} {name} {len(data)//1024} KB', flush=True)
    except Exception as e:
        fails += 1; print(f'{i}/{len(urls)} {name} FAILED: {e}', flush=True)
        if fails >= 5: print('5 consecutive failures; stopping'); sys.exit(1)
    time.sleep(a.delay + random.uniform(0, 3))
with open(OUT / 'manifest.tsv', 'w') as m:
    for i, u in enumerate(urls, 1): m.write(f"{i}\t{u.rsplit('/',1)[1]}\t{(OUT/u.rsplit('/',1)[1]).exists()}\n")
print('done; manifest written')
