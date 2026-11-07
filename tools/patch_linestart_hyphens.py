#!/usr/bin/env python3
"""Add the scribe's line-start hyphen to page lines that the image shows begin with one (and nothing else).
Usage: python3 tools/patch_linestart_hyphens.py PAGE LINES [--apply]       e.g. 71 2,11,12,14
       python3 tools/patch_linestart_hyphens.py --file RESULTS.tsv [--apply]  (lines: "PAGE<TAB>2,11,12", '#' comments ok)
Dry run by default: prints each change; --apply writes the page files. Line numbers count the page file's text
lines (comment-only lines skipped), the same numbering as tools/flag_linestart_hyphens.py. Lines that already
start with '-' are left alone (idempotent); a line number past the last text line is an error and the page is not
touched. Do not use it to guess: the line numbers must come from viewing the image."""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / 'book-of-mormon-printers-manuscript-pages'
COMMENT_ONLY = re.compile(r'\s*(<!--.*?-->\s*)+')

def parse_lines(s):
    out = []
    for part in s.replace(' ', '').split(','):
        if part:
            out.append(int(part))
    return sorted(set(out))

def patch(page, wanted, apply):
    f = PAGES / f'page-{page:03d}.md'
    if not f.exists():
        print(f'{page:03d}: no page file'); return False
    raw = f.read_text().split('\n')
    idx = [i for i, l in enumerate(raw) if l.strip() and not COMMENT_ONLY.fullmatch(l)]
    bad = [n for n in wanted if n < 1 or n > len(idx)]
    if bad:
        print(f'{page:03d}: line(s) {bad} out of range (page has {len(idx)} text lines); not touched'); return False
    changed = []
    for n in wanted:
        i = idx[n - 1]
        if raw[i].startswith('-'):
            continue
        raw[i] = '-' + raw[i]
        changed.append(n)
        print(f'{page:03d} l{n}: {raw[i][:50]}')
    skipped = [n for n in wanted if n not in changed]
    print(f'{page:03d}: {len(changed)} hyphen(s) {"added" if apply else "would be added"}'
          + (f', already present on {skipped}' if skipped else ''))
    if apply and changed:
        f.write_text('\n'.join(raw))
    return True

def main():
    argv = sys.argv[1:]
    apply = '--apply' in argv
    argv = [a for a in argv if a != '--apply']
    jobs = []
    if argv and argv[0] == '--file':
        for l in Path(argv[1]).read_text().split('\n'):
            l = l.strip()
            if l and not l.startswith('#'):
                p, _, ls = l.partition('\t')
                jobs.append((int(p), parse_lines(ls)))
    elif len(argv) == 2:
        jobs.append((int(argv[0]), parse_lines(argv[1])))
    else:
        raise SystemExit(__doc__)
    ok = all([patch(p, ls, apply) for p, ls in jobs])
    if not apply:
        print('(dry run; add --apply to write)')
    raise SystemExit(0 if ok else 1)

main()
