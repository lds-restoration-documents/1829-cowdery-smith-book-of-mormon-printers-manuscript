#!/usr/bin/env python3
"""Word-level diff of two readings of the same page (first read vs blind second read).

Usage: python3 tools/wdiff.py book-of-mormon-printers-manuscript-pages/page-007.md work/proof/page-007.md

Strips <!-- comments --> and blank lines, compares word by word, and prints each
disagreement as "L<lineA>/<lineB>  A: ...  |  B: ...", then a count. Line numbers
count text lines only (comments and blank lines excluded). Capitalisation and
punctuation differences are shown too; judge them against the image.
Standard library only.
"""
import re
import sys
import difflib


def load(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f.read().split("\n"):
            line = re.sub(r"<!--.*?-->", "", line).strip()
            if line:
                out.append(line)
    return out


def tokens(lines):
    return [(n, w) for n, l in enumerate(lines, 1) for w in l.split()]


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    ta, tb = tokens(load(sys.argv[1])), tokens(load(sys.argv[2]))
    sm = difflib.SequenceMatcher(None, [w for _, w in ta], [w for _, w in tb], autojunk=False)
    n = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        n += 1
        la = ta[i1][0] if i1 < len(ta) else "-"
        lb = tb[j1][0] if j1 < len(tb) else "-"
        a = " ".join(w for _, w in ta[i1:i2]) or "∅"
        b = " ".join(w for _, w in tb[j1:j2]) or "∅"
        print(f"L{la}/{lb}  A: {a}  |  B: {b}")
    print(f"-- {n} disagreements; words A={len(ta)} B={len(tb)}")


if __name__ == "__main__":
    main()
