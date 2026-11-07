#!/usr/bin/env python3
"""Build combined text from the page files, one cumulative layer at a time.
Usage: compile.py [--layer LAYER] [--punct none|pencil|ink|all] [--format md|txt] [--sparse] [--out FILE]

Layers (each one includes the ones before it):
  first       first inscription: the scribe's own strikes kept as written, the scribe's own ^insertions^ left out, no later-layer
              mark applied, no added punctuation.
  scribal     + the scribe's own corrections (untagged ~~strikes~~ removed, untagged ^insertions^ applied).
  compositor  + the compositor's marks: @1830 word changes and all added punctuation and pilcrows ({..}@pencil and {..}@ink).
  1837        + @1837 word changes (darker-ink emendations; tagged by ink color, not verified by hand).
  full        everything inline (nothing applied): all tags, strikes, insertions and added marks shown; @later appears only here.
  everything  scribal + @1830 + @1837 + @later applied, all punctuation (legacy 'emended').
  Legacy names: base = first, emended = everything. @later (layer unknown) is never applied except in 'everything'.
--punct overrides the layer's default punctuation (first/scribal none; compositor/1837/everything all).
--sparse keeps the Book of Mormon proper only (pages 5 to the end of Moroni on page 467), with no page markers, and rejoins words
broken across lines; txt only. A report of joins goes to stderr.
A bare overwrite tag (word@1837 with no strike/insertion) keeps the visible word in every layer and warns on stderr.
md keeps `<!-- page NNN -->` markers and hard line breaks; txt has no markers. Lines stay as the scribe wrote them (one per manuscript line)."""
import argparse, re, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / 'book-of-mormon-printers-manuscript-pages'
ALIASES = {'base': 'first', 'emended': 'everything'}
LAYERS = ('first', 'scribal', 'compositor', '1837', 'full', 'everything')
APPLIED = {'first': set(), 'scribal': {None}, 'compositor': {None, '1830'}, '1837': {None, '1830', '1837'},
           'everything': {None, '1830', '1837', 'later'}}
PUNCT = {'first': 'none', 'scribal': 'none', 'compositor': 'all', '1837': 'all', 'everything': 'all', 'full': 'inline'}
SPARSE_FIRST, SPARSE_LAST, SPARSE_END_LINE = 5, 467, 'The Testimony of three witnesses'  # page 467 line 23 starts the Three Witnesses
TAG = r'(?:@(1837|1830|later))?'
BARE = r'(\S+)@(?:1837|1830|later)\b'
try: DICT = {w.strip().lower() for w in open('/usr/share/dict/words')}  # optional guard against joining two real words
except OSError: DICT = set()


def render_page(s, n, layer, punct, fmt, warn):
    """Return the rendered lines of one page file."""
    full = layer == 'full'
    parts = re.split(r'(<!--.*?-->)', s, flags=re.S)  # odd items are comments
    out = []
    for i, p in enumerate(parts):
        if i % 2:
            out.append(p if (full and fmt == 'md') else '')
        else:
            out.append(p)
    body = ''.join(out)
    # comments may have been dropped: lines that were comment-only become empty and are filtered at the end
    pre = body.split('\n')
    if full:
        if fmt == 'md':
            body = re.sub(r'~~([^~\n]*)~~' + TAG, lambda m: f'~~{m.group(1)}~~' + (f'[@{m.group(2)}]' if m.group(2) else ''), body)
            body = re.sub(r'\^([^^\n]*)\^' + TAG, lambda m: f'<sup>{m.group(1)}</sup>' + (f'[@{m.group(2)}]' if m.group(2) else ''), body)
            body = re.sub(r'(\{[^}\n]*\})@(pencil|ink)', r'\1[@\2]', body)
            body = re.sub(r'(?<=\w)@(1837|1830|later)\b', r'[@\1]', body)  # bare overwrite tag
    else:
        applied = APPLIED[layer]
        def mark(kind, m):  # kind '~' strike or '^' insertion; group(2) = tag or None
            on = m.group(2) in applied
            return ('' if on else m.group(1)) if kind == '~' else (m.group(1) if on else '')
        body = re.sub(r'\{([^}\n]*)\}@(pencil|ink)', lambda m: m.group(1) if punct in ('all', m.group(2)) else '', body)
        body = re.sub(r'~~([^~\n]*)~~' + TAG, lambda m: mark('~', m), body)
        body = re.sub(r'\^([^^\n]*)\^' + TAG, lambda m: mark('^', m), body)
        for m in re.finditer(BARE, body):
            warn.add(f'page {n}: bare overwrite {m.group(0)!r} kept as {m.group(1)!r} in all layers')
        body = re.sub(BARE, r'\1', body)
    lines = []
    for p0, l in zip(pre, body.split('\n')):
        if not l.strip():
            continue
        # a mark removal must not leave a leading space the page file did not have
        l = l if p0[:1] in ' \t' else l.lstrip()
        l = re.sub(r' {2,}', ' ', l).rstrip()
        lines.append(l)
    return lines


def rejoin(lines, report):
    """Join words broken across lines, moving the tail up to the previous line (no reflow)."""
    vocab = Counter()
    for l in lines:
        toks = re.findall(r"[A-Za-z']+", l)
        vocab.update(t.lower() for t in toks[1:-1])
    def cnt(w): return vocab[re.sub(r"[^a-z']", '', w.lower())]
    out = [l for l in lines]
    for i in range(len(out) - 1):
        cur, nxt = out[i], out[i + 1]
        if not cur.strip() or not nxt.strip():
            continue
        ctok = cur.split(' ')[-1]
        ntok = nxt.split(' ')[0]
        rest = ' '.join(nxt.split(' ')[1:])
        kind = None
        if nxt.startswith('-') and len(ntok) > 1:       # scribe's line-start hyphen: certain
            frag = ntok[1:]; head = ctok[:-1] if ctok.endswith('-') else ctok; kind = 'hyphen'
        elif ctok.endswith('-') and re.match(r'[A-Za-z]', ntok):  # hyphen at line end only
            frag = ntok; head = ctok[:-1]
            joined = re.sub(r'[^a-z]', '', (head + frag).lower())
            if vocab[joined] >= 1 or cnt(frag) <= 2: kind = 'end-hyphen'
            else: report['kept-hyphen'].append(f'{ctok} / {ntok}'); continue
        elif re.match(r'[A-Za-z]+$', ctok) and re.match(r'[a-z]+', ntok):  # no hyphen: vocabulary test
            frag = ntok; head = ctok
            m = re.match(r"[A-Za-z']+", ntok); core = m.group(0) if m else ntok
            joined = (ctok + core).lower()
            jc = vocab[joined]
            if jc >= 2 and (cnt(ctok) <= 3 or cnt(core) <= 3 or (jc > cnt(ctok) and jc > cnt(core))): kind = 'vocab'
            elif (cnt(ctok) <= 1 and cnt(core) <= 1 and len(ctok) > 1 and len(core) <= 7 and len(ctok) <= 10
                  and not (ctok.lower() in DICT and (core.lower() in DICT or (len(ctok) >= 5 and len(core) >= 4)))): kind = 'rare-pair'  # neither side is a word, or only one is
            else:
                if cnt(ctok) <= 1 and cnt(core) <= 1 and len(ctok) > 1: report['unjoined'].append(f'{ctok} / {ntok}')
                continue
        else:
            continue
        report[kind].append(f'{ctok} / {ntok}')
        out[i] = cur[:len(cur) - len(ctok)] + head + frag
        out[i + 1] = rest
    return [l for l in out if l.strip()]


def build(layer='first', fmt='txt', punct=None, sparse=False, pages_dir=PAGES, warn=None, report=None):
    layer = ALIASES.get(layer, layer)
    assert layer in LAYERS, layer
    punct = punct or PUNCT[layer]
    warn = warn if warn is not None else set()
    chunks, flat = [], []
    for f in sorted(Path(pages_dir).glob('page-*.md')):
        n = int(f.stem[-3:])
        if sparse and not (SPARSE_FIRST <= n <= SPARSE_LAST):
            continue
        lines = render_page(f.read_text(), n, layer, punct, fmt, warn)
        if sparse and n == SPARSE_LAST:
            lines = lines[:next(i for i, l in enumerate(lines) if l.startswith(SPARSE_END_LINE))]
        if sparse:
            flat += lines
        else:
            chunks.append((n, lines))
    if sparse:
        return '\n'.join(rejoin(flat, report if report is not None else defaultdict(list))) + '\n'
    eol = '  ' if fmt == 'md' else ''
    out = []
    for n, lines in chunks:
        out.append((f'<!-- page {n:03d} -->\n' if fmt == 'md' else '') + '\n'.join(l + eol for l in lines) + '\n')
    return '\n'.join(out)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--layer', default='first'); ap.add_argument('--format', default='txt')
    ap.add_argument('--punct', default=None, choices=['none', 'pencil', 'ink', 'all']); ap.add_argument('--sparse', action='store_true')
    ap.add_argument('--out'); ap.add_argument('--dir', default=str(PAGES)); a = ap.parse_args()
    if a.layer in ALIASES: print(f'note: --layer {a.layer} is now --layer {ALIASES[a.layer]}', file=sys.stderr)
    warn = set(); rep = defaultdict(list)
    text = build(a.layer, a.format, a.punct, a.sparse, a.dir, warn, rep)
    for w in sorted(warn): print('warning:', w, file=sys.stderr)
    if a.sparse: print('joins:', {k: len(v) for k, v in rep.items()}, file=sys.stderr)
    Path(a.out).write_text(text) if a.out else print(text)
