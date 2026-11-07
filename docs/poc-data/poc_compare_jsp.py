#!/usr/bin/env python3
"""Compare our page files against the JSP transcript text (work/jsp.txt, extracted from the JSP PDF).
Scoring aid only; the JSP text was never used while transcribing."""
import re, difflib, sys, json, os
from pathlib import Path
R = Path(__file__).resolve().parents[1]
jsp = (R/'work/jsp.txt').read_text()
jsp = jsp.replace('=====PAGE=====', ' ')
jsp = re.sub(r'\[p\. (\[?[ivx\d]+\]?)\]', r'@@P\1@@', jsp)
parts = re.split(r'@@P(.*?)@@', jsp)  # text0, label1, text1, label2, text2...
pages = {parts[i]: parts[i+1] for i in range(1, len(parts)-1, 2)}
def jclean(t):
    t = t.replace('[verso blank]', ' ')
    t = re.sub(r'[<>\[\]\(\)]', '', t)
    return t
def tok(t):
    t = t.lower()
    t = re.sub(r'[—–\-.,;:?!&~"“”’\'^*/|]+', lambda m: ' & ' if '&' in m.group() else ' ', t)
    t = t.replace('@', ' ')
    return [w for w in t.split() if w]
def ours(n):
    t = (R/(os.environ.get('PAGES_DIR','printers-manuscript-test-pages'))/f'page-{n:03d}.md').read_text()
    t = re.sub(r'<!--.*?-->', ' ', t, flags=re.S)
    t = t.replace('[illegible]', ' ').replace('[…]', ' ').replace('[...]', ' ')
    t = t.replace('~~', ' ').replace('^', ' ')
    t = re.sub(r'[\[\]]', '', t)
    return t
def jsp_page(n):
    if n == 5:
        r = (R/'work/jsp.txt').read_text().replace('=====PAGE=====', ' ')
        return r[r.index('First Nephi, Chapter 1'):r.index('[p. 1]')]
    if n >= 6:
        return pages[str(n-5)]
    if n == 1:
        return parts[0].split('Document Transcript')[1].split('Preface')[0]
    if n == 3:
        return 'Preface' + parts[0].split('[verso blank] [p. [ii]]')[-1].split('First Nephi, Chapter 1')[0] if False else None
out = []; tot_e = tot_w = 0
for n in ([int(x) for x in os.environ['PAGES'].split(',')] if 'PAGES' in os.environ else [1,3]+list(range(5,21))):
    raw = (R/'work/jsp.txt').read_text().replace('=====PAGE=====', ' ')
    if n == 1:
        j = raw[raw.index('Title Page'):raw.index('Preface\nPreface')]
    elif n == 3:
        j = raw[raw.index('Preface\nPreface'):raw.index('The Author')+10]
    else:
        j = jsp_page(n)
    a, b = tok(jclean(j)), tok(ours(n))
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    diffs = []; err = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != 'equal':
            diffs.append((op, ' '.join(a[i1:i2]), ' '.join(b[j1:j2]), ' '.join(a[max(0,i1-4):i1])))
            err += max(i2-i1, j2-j1)
    tot_e += err; tot_w += len(a)
    out.append((n, len(a), len(b), err, diffs))
with open(R/os.environ.get('OUT','work/jsp_diff.txt'), 'w') as f:
    for n, la, lb, err, d in out:
        f.write(f'### page {n}: JSP words {la}, ours {lb}, differing words {err} ({100*err/la:.1f}%)\n')
        for op, x, y, ctx in d:
            f.write(f'  [{op}] ...{ctx} | JSP: {x!r} | OURS: {y!r}\n')
for n, la, lb, err, d in out: print(n, la, lb, err, f'{100*err/la:.1f}%')
print('TOTAL', tot_w, tot_e, f'{100*tot_e/tot_w:.1f}%')
