#!/usr/bin/env python3
"""Cut page images into overlapping horizontal bands at native resolution (the page photos are ~2000 px wide,
so bands are shown to the model unshrunk).
Usage (venv python, needs Pillow): ~/.venvs/lds-transcribe/bin/python tools/prepare_bands.py --pages 5-8 [--out work] [--clean]
       add --pdf SCAN.pdf to read a PDF instead of source-images/ (needs pypdfium2)
PAGE NUMBER = position in source-images/manifest.tsv (1 = 9153_chl_bom_pm_000, 2 = ..._000-01, 3 = ..._000-02,
4 = ..._000-03, 5 = ..._001, ...). Page files, bands and logs use this 3-digit number. `--list` prints the mapping.
Writes <out>/img/pNNN_B.jpg (B = 1..n), ~900 px tall, 120 px overlap."""
import argparse, shutil
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
BAND, OVER = 900, 120
ap = argparse.ArgumentParser()
ap.add_argument('--pdf'); ap.add_argument('--pages', default='1'); ap.add_argument('--out', default='work'); ap.add_argument('--clean', action='store_true'); ap.add_argument('--list', action='store_true'); ap.add_argument('--band', type=int, default=BAND, help='band height in px (default 900; 940 gives 4 bands on most pages)')
a = ap.parse_args()
IMGS = sorted((ROOT / 'source-images').glob('*.jpg'), key=lambda p: [int(x) for x in p.stem.split('_pm_')[1].split('_')[0].split('-')])
if a.list:
    for i, p in enumerate(IMGS, 1): print(i, p.name)
    raise SystemExit
out = (ROOT / a.out / 'img')
if a.clean:
    shutil.rmtree(out, ignore_errors=True); raise SystemExit
use_pdf = bool(a.pdf)
pdf = Path(a.pdf) if use_pdf else None
pages = []
for part in a.pages.split(','):
    lo, _, hi = part.partition('-'); pages += range(int(lo), int(hi or lo) + 1)
out.mkdir(parents=True, exist_ok=True)
if use_pdf:
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(pdf))
for n in pages:
    im = (next(o.get_bitmap().to_pil().convert('RGB') for o in doc[n-1].get_objects() if o.type == 3) if use_pdf
          else Image.open(IMGS[n-1]).convert('RGB'))
    w, h = im.size; y = 0; b = 1
    while y < h:
        im.crop((0, y, w, min(h, y + a.band))).save(out / f'p{n:03d}_{b}.jpg', quality=92)
        if y + a.band >= h: break
        y += a.band - OVER; b += 1
    print(n, b, 'bands')
