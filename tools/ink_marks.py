#!/usr/bin/env python3
"""List @later (and a seeded sample of @1837) marks per page with line numbers (text lines as in reconcile.py).
Usage: python3 tools/ink_marks.py PAGE... [--n1837 K] -> prints 'pNNN Lnn KIND mark | line'"""
import re, sys, random
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
k = int(sys.argv[sys.argv.index('--n1837') + 1]) if '--n1837' in sys.argv else 5
pages = [a for a in sys.argv[1:] if a.isdigit() and a != str(k) or a.isdigit() and '--n1837' not in sys.argv]
if '--n1837' in sys.argv: pages = [a for a in sys.argv[1:sys.argv.index('--n1837')] if a.isdigit()]
M = re.compile(r'(~~[^~]*~~|\^[^^]*\^)@(later|1837)')
for n in map(int, pages):
    L = [l for l in (re.sub(r'<!--.*?-->', '', x).strip() for x in (ROOT / f'book-of-mormon-printers-manuscript-pages/page-{n:03d}.md').read_text().split('\n')) if l]
    later = []; e37 = []
    for i, l in enumerate(L, 1):
        for m in M.finditer(l): (later if m.group(2) == 'later' else e37).append((i, m.group(1), m.group(2), l))
    random.Random(n).shuffle(e37)
    for i, mk, kd, l in later + sorted(e37[:k]): print(f'p{n:03d} L{i} {kd} {mk} | {l}')
