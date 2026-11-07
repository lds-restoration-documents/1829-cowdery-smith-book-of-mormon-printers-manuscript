#!/usr/bin/env python3
"""Word-diff page files against a reference text (the Joseph Smith Papers transcript, which holds the ORIGINAL
inscription only). A scoring/review aid: never show the reference to a transcriber.
Usage: compare_reference.py --ref work/jsp.txt --dir DIR --map 10:5,18:13 [--drop-insertions] [--out work/diff.txt]
  --map PDFPAGE:JSPPAGE pairs; JSP pages are the `[p. N]` markers in the JSP PDF text (extract it with
  pypdfium2: get_textpage().get_text_range() per page). Front matter and the first leaf have no number: slice by hand.
  --drop-insertions removes ^insertions^ (keeps struck words) to approximate the original layer;
  `@1837`/`@1830`/`@later`-tagged later-layer marks are always dropped (insertions) / kept as plain text (strikes).
Differences that are artifacts of the JSP PDF (footnote numbers, headings, line-break splits) are not filtered."""
import argparse, difflib, re
from pathlib import Path
ap = argparse.ArgumentParser()
ap.add_argument('--ref', required=True); ap.add_argument('--dir', required=True); ap.add_argument('--map', required=True)
ap.add_argument('--drop-insertions', action='store_true'); ap.add_argument('--out')
a = ap.parse_args()
raw = Path(a.ref).read_text().replace('=====PAGE=====', ' ')
def ref_page(n):
    s = raw.index(f'[p. {n}]'); m = re.search(rf'\[p\. {n+1}\]', raw[s:]); e = s + m.start() if m else len(raw)
    return re.sub(r'[<>\[\]\(\)]', '', raw[s:e])
def tok(t):
    t = re.sub(r'[—–\-.,;:?!"“”’\'*/|~]+', ' ', t.lower().replace('&', ' & '))
    return [w for w in t.split() if w]
def ours(path):
    t = re.sub(r'<!--.*?-->', ' ', Path(path).read_text(), flags=re.S).replace('[illegible]', ' ').replace('[…]', ' ')
    t = re.sub(r'\{[^}\n]*\}@(?:pencil|ink)', ' ', t)
    t = re.sub(r'\^[^^\n]*\^@(?:1837|1830|later)', ' ', t)
    if a.drop_insertions: t = re.sub(r'\^[^^\n]*\^', ' ', t)
    return t.replace('~~', ' ').replace('^', ' ').replace('@1837', ' ').replace('@1830', ' ').replace('@later', ' ').replace('[', '').replace(']', '')
tot_e = tot_w = 0; lines = []
for pair in a.map.split(','):
    pdfp, jp = (int(x) for x in pair.split(':'))
    x, y = tok(ref_page(jp)), tok(ours(f'{a.dir}/page-{pdfp:03d}.md'))
    sm = difflib.SequenceMatcher(None, x, y, autojunk=False); err = 0; rows = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != 'equal':
            err += max(i2-i1, j2-j1); rows.append(f"  [{op}] ...{' '.join(x[max(0,i1-4):i1])} | REF: {' '.join(x[i1:i2])!r} | OURS: {' '.join(y[j1:j2])!r}")
    tot_e += err; tot_w += len(x)
    lines.append(f'### page {pdfp} (JSP {jp}): ref words {len(x)}, differing {err} ({100*err/len(x):.1f}%)'); lines += rows
lines.append(f'TOTAL ref words {tot_w}, differing {tot_e} ({100*tot_e/tot_w:.1f}%)')
print('\n'.join(lines) if not a.out else lines[-1]); 
if a.out: Path(a.out).write_text('\n'.join(lines))
