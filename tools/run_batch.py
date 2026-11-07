#!/usr/bin/env python3
"""Batch helper: fewer tool calls and less output per batch. Does NOT launch agents.
Usage:
  run_batch.py prepare A-B    cut bands (default 900 px) for pages in A-B whose page file does not exist yet;
                              prints the pages to transcribe, grouped in waves of 3 (--wave N to change)
  run_batch.py check A-B      one line per page: lines, tags, spelling flags, structure warnings
                              (--detail also prints the flagged spelling lines)
  run_batch.py clean          delete work/img (bands)
  run_batch.py note "text"    append a bullet to transcription-notes.md
Pages: A-B or comma lists (6-14 or 5,7,9-11). Standard library; bands need ~/.venvs/lds-transcribe/bin/python."""
import argparse, re, subprocess, sys
from datetime import date
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / 'book-of-mormon-printers-manuscript-pages'
VENV = Path.home() / '.venvs/lds-transcribe/bin/python'

def parse(spec):
    out = []
    for part in spec.split(','):
        lo, _, hi = part.partition('-'); out += range(int(lo), int(hi or lo) + 1)
    return out

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)

ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
p = sub.add_parser('prepare'); p.add_argument('pages'); p.add_argument('--wave', type=int, default=3); p.add_argument('--band', type=int, default=900)
p = sub.add_parser('check'); p.add_argument('pages'); p.add_argument('--detail', action='store_true')
sub.add_parser('clean')
p = sub.add_parser('note'); p.add_argument('text')
a = ap.parse_args()

if a.cmd == 'prepare':
    todo = [n for n in parse(a.pages) if not (PAGES / f'page-{n:03d}.md').exists()]
    skipped = [n for n in parse(a.pages) if n not in todo]
    if skipped: print('skip (page file exists):', ','.join(map(str, skipped)))
    if not todo: sys.exit('nothing to do')
    r = run([str(VENV), 'tools/prepare_bands.py', '--pages', ','.join(map(str, todo)), '--band', str(a.band)])
    if r.returncode: sys.exit(r.stderr.strip() or r.stdout.strip())
    nb = {int(l.split()[0]): int(l.split()[1]) for l in r.stdout.splitlines() if l.strip()}
    for i in range(0, len(todo), a.wave):
        print(f'wave {i // a.wave + 1}: ' + ', '.join(f'{n} ({nb.get(n, "?")} bands)' for n in todo[i:i + a.wave]))
elif a.cmd == 'check':
    pages = parse(a.pages)
    st = run([sys.executable, 'tools/check_structure.py']).stdout
    warn = {}
    for l in st.splitlines():
        m = re.match(r'page-(\d{3})\.md: (.*)', l)
        if m: warn[int(m.group(1))] = m.group(2)
    for n in pages:
        f = PAGES / f'page-{n:03d}.md'
        if not f.exists(): print(f'{n:03d}: MISSING'); continue
        s = f.read_text()
        lines = [l for l in s.split('\n') if l.strip() and not l.lstrip().startswith('<!--')]
        c = lambda pat: len(re.findall(pat, s))
        sp = run([sys.executable, 'tools/check_spelling.py', str(f)]).stdout
        m = re.search(r'(\d+) flag', sp); nflag = int(m.group(1)) if m else 0
        w = warn.get(n, '')
        w = re.sub(r'\d+ text lines \(usually 37[^)]*\)', '', w).strip('; ') if len(lines) in (37, 38, 39) else w
        print(f'{n:03d}: {len(lines)} lines; 1837={c("@1837")} later={c("@later")} ink={c("}@ink")} pencil={c("}@pencil")} '
              f'unc={c("uncertain")} illeg={c("illegible")}; spell flags={nflag}' + (f'; WARN: {w}' if w else ''))
        if a.detail and nflag: print('\n'.join(l for l in sp.splitlines() if l.startswith('  line')))
elif a.cmd == 'clean':
    run([str(VENV), 'tools/prepare_bands.py', '--clean']); print('bands removed')
elif a.cmd == 'note':
    f = ROOT / 'transcription-notes.md'
    f.write_text(f.read_text().rstrip('\n') + f'\n- ({date.today().isoformat()}) {a.text}\n'); print('noted')
