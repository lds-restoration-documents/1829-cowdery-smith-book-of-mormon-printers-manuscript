# Puts a blank line between the lines of each page file (so Markdown shows one manuscript line per paragraph). Idempotent.
# Usage (repo root): python3 tools/space_page_lines.py [--check]   Tools ignore blank lines, so text-line numbers do not change.
import re, sys
from pathlib import Path
CO = re.compile(r'\s*(<!--.*?-->\s*)+')
changed = 0
for f in sorted(Path('book-of-mormon-printers-manuscript-pages').glob('page-*.md')):
    s = f.read_text(); lines = [l for l in s.split('\n') if l.strip()]
    out = []
    for l in lines:
        if out and not (CO.fullmatch(out[-1]) and CO.fullmatch(l)): out.append('')
        out.append(l)
    new = '\n'.join(out) + '\n'
    if new != s:
        changed += 1
        if '--check' not in sys.argv: f.write_text(new)
print(changed, 'file(s)', 'would change' if '--check' in sys.argv else 'changed')
