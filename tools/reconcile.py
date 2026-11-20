#!/usr/bin/env python3
"""Reconcile a blind second read: list lines whose letters differ (case, spacing, added punctuation and tag layer
ignored) and write one stacked crop image of those lines for checking by eye.
Usage (venv python, needs Pillow): ~/.venvs/lds-transcribe/bin/python tools/reconcile.py PAGE... [--out DIR] [--no-img]
Writes DIR/stNNN.jpg (default work/recon): each crop is one manuscript line, labelled Lnn (line number in the first read's
text lines). Line positions come from the ink block divided by the line count, so they can drift by a fraction of a line on
pages with a short last line; check the words in the crop before editing. Hyphen differences are listed with the others."""
import re, sys, difflib
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[1]
args = [a for a in sys.argv[1:] if not a.startswith('--')]
out = ROOT / (sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else 'work/recon')
if '--out' in sys.argv: args.remove(sys.argv[sys.argv.index('--out') + 1])
noimg = '--no-img' in sys.argv
def load(p):
    r = []
    for l in p.read_text().split('\n'):
        l = re.sub(r'<!--.*?-->', '', l).strip()
        if l: r.append(l)
    return r
def norm(l):
    l = re.sub(r'\{[^}]*\}@(pencil|ink)', '', l); l = re.sub(r'@(1837|1830|later)', '', l)
    return l.replace('~~', '').replace('^', '')
key = lambda l: re.sub(r'\s+', '', norm(l)).lower()
IM = sorted((ROOT / 'source-images').glob('*.jpg'), key=lambda p: [int(x) for x in p.stem.split('_pm_')[1].split('_')[0].split('-')])
out.mkdir(parents=True, exist_ok=True)
for n in map(int, args):
    A = load(ROOT / f'book-of-mormon-printers-manuscript-pages/page-{n:03d}.md'); B = load(ROOT / f'work/proof/page-{n:03d}.md')
    sm = difflib.SequenceMatcher(None, [key(x) for x in A], [key(x) for x in B], autojunk=False); lines = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal': continue
        for k in range(max(i2 - i1, j2 - j1)):
            a = norm(A[i1 + k]) if i1 + k < i2 else '∅'; b = norm(B[j1 + k]) if j1 + k < j2 else '∅'
            wa, wb = a.split(), b.split()
            d = [(' '.join(wa[a1:a2]), ' '.join(wb[b1:b2])) for t, a1, a2, b1, b2 in difflib.SequenceMatcher(None, wa, wb).get_opcodes() if t != 'equal']
            print(f'p{n:03d} L{i1 + k + 1}: ' + ' ; '.join(f'{x} | {y}' for x, y in d)[:200]); lines.append(i1 + k + 1)
    print(f'-- p{n:03d}: {len(lines)} differing lines (A | B), A {len(A)} lines, B {len(B)} lines')
    if noimg or not lines: continue
    im = Image.open(IM[n - 1]).convert('RGB'); w, h = im.size
    col = im.convert('L').crop((int(w * .04), 0, int(w * .96), h)).point(lambda v: 255 if v < 130 else 0).resize((1, h), Image.BOX)
    pr = list(col.getdata()); sm_ = [sum(pr[max(0, i - 8):i + 8]) / 16 for i in range(h)]
    ys = [i for i, v in enumerate(sm_) if v > max(sm_) * .12]; top, bot = float(ys[0]), float(ys[-1]); lh = (bot - top) / len(A)
    crops = []
    for ln in sorted(set(min(l, len(A)) for l in lines)):
        c = im.crop((0, int(max(0, top + (ln - 1 - .15) * lh)), w, int(min(h, top + (ln + .75) * lh))))
        ImageDraw.Draw(c).text((w - 300, 2), f'L{ln}', fill=(255, 0, 0)); crops.append(c)
    st = Image.new('RGB', (w, sum(c.size[1] for c in crops)), 'white'); y = 0
    for c in crops: st.paste(c, (0, y)); y += c.size[1]
    st.save(out / f'st{n:03d}.jpg', quality=85)
