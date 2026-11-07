#!/usr/bin/env python3
"""Cut left-margin strips (default 420 px wide; top and bottom half of each page) from the page images, to check
line-start hyphens (tools/README.md step 3b). Needs Pillow: ~/.venvs/lds-transcribe/bin/python.
Usage: python tools/cut_margin_strips.py PAGES [--out work/strips] [--width 420] [--clean]   PAGES e.g. 5-13 or 71,85
Writes <out>/sNNN_1.jpg (top half) and sNNN_2.jpg (bottom half; the halves overlap ~120 px). Page number = position
in source-images/manifest.tsv, same as prepare_bands.py."""
import argparse, shutil
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument('pages'); ap.add_argument('--out', default='work/strips'); ap.add_argument('--width', type=int, default=420); ap.add_argument('--clean', action='store_true')
a = ap.parse_args()
out = ROOT / a.out
if a.clean:
    shutil.rmtree(out, ignore_errors=True); raise SystemExit
names = [l.split('\t')[1] for l in (ROOT / 'source-images' / 'manifest.tsv').read_text().split('\n') if l.strip()]
pages = []
for part in a.pages.split(','):
    lo, _, hi = part.partition('-'); pages += range(int(lo), int(hi or lo) + 1)
out.mkdir(parents=True, exist_ok=True)
for n in pages:
    im = Image.open(ROOT / 'source-images' / names[n - 1]).convert('RGB'); w, h = im.size
    half = h // 2 + 60
    for i, (y0, y1) in enumerate([(0, half), (h - half, h)], 1):
        im.crop((0, y0, a.width, y1)).save(out / f's{n:03d}_{i}.jpg', quality=92)
    print(n, 'strips')
