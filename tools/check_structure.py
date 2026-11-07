#!/usr/bin/env python3
"""Mechanical checks of page files. Usage: check_structure.py [pages_dir]  (default book-of-mormon-printers-manuscript-pages/)
Flags: missing `<!-- image N -->`, text-line count != 37 (pages 1-4, the front matter, and blank leaves are exempt),
unbalanced ~~ or ^, `@1837`/`@1830`/`@later` marks not attached to ~~..~~ or ^..^, `{mark}` without `@pencil`/`@ink`, missing folio comment."""
import re, sys
from pathlib import Path
d = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'book-of-mormon-printers-manuscript-pages')
bad = 0
for f in sorted(d.glob('page-*.md')):
    s = f.read_text(); n = f.stem[-3:]; msgs = []
    if not re.search(rf'<!-- image {n} -->', s): msgs.append('no image comment')
    lines = [l for l in s.split('\n') if l.strip() and not l.lstrip().startswith('<!--')]
    front = int(n) <= 4  # unnumbered front matter (title/copyright, blanks, preface): not 37 ruled lines
    if lines and not front and len(lines) != 37: msgs.append(f'{len(lines)} text lines (usually 37; some pages have more, check the page)')
    if lines and 'folio' not in s: msgs.append('no folio comment')
    if s.count('~~') % 2: msgs.append('unbalanced ~~')
    if s.count('^') % 2: msgs.append('unbalanced ^')
    if s.count('{') != s.count('}'): msgs.append('unbalanced { }')
    if re.search(r'\{[^}\n]*\}(?!@(?:pencil|ink))', s): msgs.append('{mark} without @pencil or @ink')
    if re.search(r'\{[^}\n]*[A-Za-z0-9][^}\n]*\}', s): msgs.append('word inside { } (only punctuation/pilcrow marks)')
    if re.search(r'(?<![~^}])@(1837|1830|later|pencil|ink)', s): msgs.append('stray @tag (not attached to ~~ ^ or { })')
    if re.search(r'(?:~~|\^)@(pencil|ink)|\}@(1837|1830|later)', s): msgs.append('wrong tag kind (@pencil/@ink only on { }; @1837/@1830/@later only on ~~ ^)')
    if re.search(r'@L(?!\w)|@(?!1837|1830|later|pencil|ink)\w+', s): msgs.append('unknown @tag (use @1837, @1830, @later, or @pencil/@ink on { })')
    if msgs: bad += 1; print(f'{f.name}: ' + '; '.join(msgs))
print(f'{bad} page(s) with warnings')
