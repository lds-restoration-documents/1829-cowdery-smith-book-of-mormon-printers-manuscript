# Builds a local human-review page for the low-confidence readings (work/settle3/lowconf.tsv). Run from repo root:
#   ~/.venvs/lds-transcribe/bin/python tools/make_lowconf_review.py
# Writes work/lowconf-review/index.html and img/ (gitignored; images stay local). Decisions are kept in the browser
# (localStorage) and exported with a button as lowconf-decisions.tsv / .json.
import re, csv, json
from pathlib import Path
from PIL import Image, ImageDraw
IM = sorted(Path('source-images').glob('*.jpg'), key=lambda p: [int(x) for x in p.stem.split('_pm_')[1].split('_')[0].split('-')])
out = Path('work/lowconf-review'); (out / 'img').mkdir(parents=True, exist_ok=True)
def raw_lines(n):
    r = []
    for l in Path(f'book-of-mormon-printers-manuscript-pages/page-{n:03d}.md').read_text().split('\n'):
        if re.sub(r'<!--.*?-->', '', l).strip(): r.append(l)
    return r
strip = lambda l: re.sub(r'<!--.*?-->', '', l).strip()
s2 = {(r[0], r[1]): r for r in csv.reader(open('work/settle2/lowconf.tsv'), delimiter='\t')}
rows = sorted(csv.reader(open('work/settle3/lowconf.tsv'), delimiter='\t'), key=lambda r: (int(r[0]), int(r[1])))
geom = {}
cards = []
for r in rows:
    p, ln = int(r[0]), int(r[1])
    A = raw_lines(p)
    if p not in geom:
        im = Image.open(IM[p - 1]).convert('RGB'); w, h = im.size
        col = im.convert('L').crop((int(w * .04), 0, int(w * .96), h)).point(lambda v: 255 if v < 130 else 0).resize((1, h), Image.BOX)
        pr = list(col.getdata()); sm = [sum(pr[max(0, i - 8):i + 8]) / 16 for i in range(h)]
        ys = [i for i, v in enumerate(sm) if v > max(sm) * .12]; top, bot = float(ys[0]), float(ys[-1])
        geom[p] = (im, top, (bot - top) / len(A))
    im, top, lh = geom[p]; w, h = im.size
    y0 = int(max(0, top + (ln - 1 - 1.25) * lh)); y1 = int(min(h, top + (ln + 1.1) * lh))
    c = im.crop((0, y0, w, y1)); d = ImageDraw.Draw(c)
    ya = int(top + (ln - 1) * lh) - y0; yb = int(top + ln * lh) - y0
    d.rectangle((0, ya, 10, yb), fill=(220, 0, 0))   # red bar = estimated line (may drift a little)
    c.save(out / f'img/p{p:03d}_{ln:02d}.jpg', quality=88)
    a = lambda i: A[i - 1] if 1 <= i <= len(A) else ''
    x = s2.get((r[0], r[1]), [''] * 5)
    cards.append(dict(page=p, line=ln, prev=strip(a(ln - 1)), cur=strip(a(ln)), curraw=a(ln), next=strip(a(ln + 1)),
                      verdict=r[2], conf=r[3], reading=r[4], note=r[5] if len(r) > 5 else '',
                      s2verdict=x[2], s2reading=x[4] if len(x) > 4 else '', s2note=x[5] if len(x) > 5 else ''))
tpl = Path(__file__).with_name('lowconf_review_template.html').read_text()
(out / 'index.html').write_text(tpl.replace('/*DATA*/', json.dumps(cards)))
print('wrote', out / 'index.html', len(cards), 'rows')
