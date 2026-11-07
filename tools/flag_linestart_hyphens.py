#!/usr/bin/env python3
"""Flag lines that probably continue a word broken across lines, so a reader can check the image for a
scribal line-start hyphen (see transcription-notes.md, batch 7 note). Local only; changes no files.
Usage: python3 tools/flag_linestart_hyphens.py [A-B] [--detail]
A line N+1 is flagged when its first word is not an English word (macOS /usr/share/dict/words) and
either the joined word (last word of line N + first word of N+1) is one or the last word of line N is not.
Old spellings make this over-flag; that is fine, the image decides. Prints per page: text lines, flagged
lines, flagged lines already starting with '-', flagged lines without. Line number = n-th text line of the
page file (comment-only lines skipped), which is the manuscript line number."""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / 'book-of-mormon-printers-manuscript-pages'
args = [a for a in sys.argv[1:] if not a.startswith('--')]
detail = '--detail' in sys.argv
lo, _, hi = (args[0] if args else '1-468').partition('-')
lo, hi = int(lo), int(hi or lo)
try:
    WORDS = {w.strip().lower() for w in open('/usr/share/dict/words', errors='ignore')}
except OSError:
    raise SystemExit('no /usr/share/dict/words')

def clean(s):
    s = re.sub(r'<!--.*?-->', '', s)
    s = re.sub(r'\{[^}]*\}@\w+', '', s)          # added punctuation
    s = re.sub(r'~~.*?~~(@\w+)?', '', s)         # struck words
    s = re.sub(r'\^([^^]*)\^(@\w+)?', r'\1', s)  # insertions
    s = re.sub(r'@\w+', '', s)
    return s

def words(s):
    return re.findall(r"[A-Za-z]+", s)

tot_flag = tot_missing = 0
for n in range(lo, hi + 1):
    f = PAGES / f'page-{n:03d}.md'
    if not f.exists():
        continue
    raw = [l.rstrip('\n') for l in f.read_text().split('\n')]
    lines = [l for l in raw if l.strip() and not re.fullmatch(r'\s*(<!--.*?-->\s*)+', l)]
    flagged, missing = [], []
    for i in range(1, len(lines)):
        cur = clean(lines[i]).strip()
        prev = clean(lines[i - 1]).strip()
        cw, pw = words(cur), words(prev)
        if not cw or not pw:
            continue
        first, last = cw[0].lower(), pw[-1].lower()
        if first in WORDS and first not in ('a', 'i'):
            continue
        if (last + first) in WORDS or last not in WORDS:
            flagged.append(i + 1)
            if not lines[i].lstrip().startswith('-'):
                missing.append(i + 1)
    tot_flag += len(flagged); tot_missing += len(missing)
    print(f'{n:03d}: lines={len(lines)} flagged={len(flagged)} already-hyphen={len(flagged) - len(missing)} to-check={len(missing)}'
          + (f' lines={missing}' if detail else ''))
print(f'TOTAL flagged={tot_flag} to-check={tot_missing}')
