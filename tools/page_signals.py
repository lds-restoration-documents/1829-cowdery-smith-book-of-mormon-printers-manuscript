#!/usr/bin/env python3
"""Rank pages for a second blind read. Score = strikes + [illegible] + uncertain comments (the draft's own marks
predicted per-page error well in the POC: correlation ~0.8 on ordinary text pages).
Usage: page_signals.py [pages_dir] [--top N]"""
import re, sys
from pathlib import Path
args = [a for a in sys.argv[1:] if not a.startswith('--')]
top = int(sys.argv[sys.argv.index('--top')+1]) if '--top' in sys.argv else 0
d = Path(args[0] if args else Path(__file__).resolve().parents[1] / 'book-of-mormon-printers-manuscript-pages')
rows = []
for f in sorted(d.glob('page-*.md')):
    s = f.read_text(); st = s.count('~~')//2; il = s.count('[illegible]'); un = s.count('uncertain')
    rows.append((st+il+un, f.stem[-3:], st, il, un))
rows.sort(reverse=True)
print('score page strikes illegible uncertain')
for r in (rows[:top] if top else rows): print(*r)
