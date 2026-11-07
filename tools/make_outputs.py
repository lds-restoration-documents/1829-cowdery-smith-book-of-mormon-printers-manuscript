#!/usr/bin/env python3
"""Build the layered output files in the repo root (see tools/compile.py for the layer definitions).
Usage: python3 tools/make_outputs.py [--outdir DIR]
Writes, per layer, STEM.md, STEM.txt and (clean layers) STEM-sparse.txt, each with a short header; checks that clean files have no
leftover markup; writes a join and warning report to work/outputs-report.txt."""
import argparse, datetime, json, re, subprocess, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import compile as C

STATUS = ("Draft, AI-assisted transcription from the page images (2026). Only pages 7, 8, 11 and 13 have had a second blind read; "
          "all other pages are first-pass with automated checks only. Words are written as the scribe wrote them, spelling included.")
PUNCT_NOTE = ("Added punctuation and pilcrows are tagged by ink (pencil or dark ink) as seen in the images, not attributed to a hand; "
              "the tagging is best-effort and is much thinner after about page 268, so punctuation is uneven across the book.")
LAYERS = [  # layer, stem, title, description
    ('full', 'printers-manuscript-all-layers', 'All layers shown inline',
     "Nothing is applied. The scribe's own strikes and insertions, every later-layer change with its tag (1830 compositor, 1837, later = layer "
     "unknown), and the added punctuation (pencil or ink) are all shown. Markdown shows strikes as strikethrough, insertions as superscript and "
     "tags in square brackets; the text file keeps the page-file notation (double tilde for a strike, carets for an insertion, @tag suffixes, "
     "braces for added marks). " + PUNCT_NOTE),
    ('first', 'printers-manuscript-first-inscription', 'First inscription',
     "The scribes' writing before any correction: their own struck words are kept as written, their own insertions above the line are left "
     "out, no later-layer change is applied, no added punctuation. Where letters were overwritten the text shows the best reading of the "
     "visible form, so the first inscription is not fully recoverable at those places (see the uncertain comments in the page files)."),
    ('scribal', 'printers-manuscript-scribal-corrections', 'With scribal corrections',
     "The first inscription plus the scribes' own corrections: their struck words removed and their own insertions applied. Immediate "
     "corrections cannot be told apart from later scribal proofreading, so this is the scribes' text as it stands, not necessarily the text "
     "as first delivered to the printer. No added punctuation, no later-layer change."),
    ('compositor', 'printers-manuscript-compositor-marks', 'With the compositor\'s marks',
     "Scribal corrections plus the compositor's marks (John H. Gilbert, 1830): added punctuation and pilcrows in pencil and in ink, and the few "
     "tagged 1830 word changes (about 12 in the whole manuscript, so this layer is almost all punctuation). " + PUNCT_NOTE),
    ('1837', 'printers-manuscript-1837-emendations', 'With 1837 emendations',
     "Compositor's marks plus the 1837 emendations (darker-ink word changes, Joseph Smith). The 1837 tag means darker ink as judged "
     "from the images, not a verified hand; about 400 marks of unknown layer (tagged later) are not applied here and appear only in the "
     "all-layers file. This is the manuscript with its 1837 emendations applied, not the printed 1837 edition. " + PUNCT_NOTE),
]
SPARSE_NOTE = ("Sparse: the Book of Mormon text only (from the first page of 1 Nephi to the end of Moroni; the title and copyright leaf, the "
               "preface and the witness testimonies are left out), without page markers, and with words broken across lines joined up. "
               "Line breaks otherwise follow the manuscript lines.")


SOURCE = ("https://archiveviewer.org/viewer/joseph-smith-papers/printers-manuscript-of-the-book-of-mormon-circa-august-1829-circa-january-1830 "
          "(Joseph Smith Papers; manuscript held by the Church History Library; page images downloaded with the Archive Viewer)")
METHOD = ("AI-assisted transcription from page images (Claude Opus, one fresh agent per page, plus automated structure and spelling checks; "
          "a Claude Sonnet patch added line-start hyphens on pages 5-94); second blind read of pages 7, 8, 11 and 13 only; "
          "no full human proofread")


REPO = 'https://github.com/lds-restoration-documents/1829-cowdery-smith-book-of-mormon-printers-manuscript'


def build_version():
    """Latest release tag (if any), build date and the short hash of the last commit that touched the page files,
    e.g. 'v1.0.0 (2026-11-07, 88a940d)'; '+dirty' follows the hash for uncommitted page edits, '+modified' follows the tag when
    the page files differ from it. Without any tag: '2026-11-07+88a940d'."""
    def git(*a): return subprocess.run(['git', '-C', str(C.ROOT), *a], capture_output=True, text=True, check=True).stdout.strip()
    today = datetime.date.today().isoformat()
    try:
        h = git('log', '-1', '--format=%h', '--', str(C.PAGES)) or 'uncommitted'
        dirty = bool(git('status', '--porcelain', '--', str(C.PAGES)))
        if dirty: h += '+dirty'
        try: tag = git('describe', '--tags', '--abbrev=0')
        except subprocess.CalledProcessError: return f'{today}+{h}'
        if dirty or git('diff', '--name-only', tag, '--', str(C.PAGES)): tag += '+modified'
        return f'{tag} ({today}, {h})'
    except (OSError, subprocess.CalledProcessError):
        return f'{today}+unknown'


def frontmatter(title, layer, desc, version, sparse=False):
    q = json.dumps  # JSON strings are valid YAML double-quoted scalars
    pages = 'pages 5-467 (1 Nephi to the end of Moroni)' if sparse else 'pages 1-468 (all images)'
    rows = [('title', q(f"Printer's Manuscript of the Book of Mormon ({title})")),
            ('scribes', q('Oliver Cowdery, Hyrum Smith and an unidentified scribe ("scribe 2")')),
            ('date', q('ca. August 1829 - ca. January 1830')),
            ('layer', q(layer)), ('layer_description', q(desc)), ('contents', q(pages)), ('source_scan', q(SOURCE)),
            ('transcription_method', q(METHOD)), ('status', q(STATUS)),
            ('repository', REPO),
            ('version', q(version))]
    return '---\n' + ''.join(f'{k}: {v}\n' for k, v in rows) + '---\n\n'


def header(fmt, title, desc, sparse=False, layer='', version=''):
    d = desc + (' ' + SPARSE_NOTE if sparse else '')
    if fmt == 'md': return frontmatter(title, layer, d, version, sparse)
    return f"# Printer's Manuscript of the Book of Mormon, {title[0].lower() + title[1:]} ({'sparse, ' if sparse else ''}unreviewed AI draft) - {REPO}\n\n"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--outdir', default=str(C.ROOT)); a = ap.parse_args()
    out = Path(a.outdir); warn = set(); lines = []; version = build_version()
    for layer, stem, title, desc in LAYERS:
        for fmt in ('md', 'txt'):
            text = header(fmt, title, desc, False, layer, version) + C.build(layer, fmt, None, False, C.PAGES, warn)
            (out / f'{stem}.{fmt}').write_text(text)
        if layer != 'full':
            rep = defaultdict(list)
            body = C.build(layer, 'txt', None, True, C.PAGES, warn, rep)
            (out / f'{stem}-sparse.txt').write_text(header('txt', title, desc, True) + body)
            lines.append(f'{stem}-sparse: ' + ', '.join(f'{k} {len(v)}' for k, v in sorted(rep.items())))
            if layer == 'first':  # same joins in every layer; list them once
                for k in ('unjoined', 'kept-hyphen', 'rare-pair'): lines.append(f'  {k}: ' + '; '.join(rep[k]))
    bad = []
    for layer, stem, *_ in LAYERS:
        if layer == 'full': continue
        for suffix in ('.md', '.txt', '-sparse.txt'):
            t = (out / (stem + suffix)).read_text()
            body = t.split('\n\n', 1)[1] if suffix != '.md' else t.split('\n---\n', 1)[1]
            for ch in re.findall(r'@|~~|\^|[{}]', body): bad.append(f'{stem}{suffix}: leftover {ch!r}')
    work = C.ROOT / 'work'; work.mkdir(exist_ok=True)
    (work / 'outputs-report.txt').write_text('\n'.join(['warnings:'] + sorted(warn) + ['', 'sparse joins:'] + lines + ['', 'residual markup:'] + (sorted(set(bad)) or ['none'])) + '\n')
    print('residual markup:', sorted(set(bad)) or 'none'); print('warnings:', len(warn)); print('report: work/outputs-report.txt')
    return 1 if bad else 0


if __name__ == '__main__': sys.exit(main())
