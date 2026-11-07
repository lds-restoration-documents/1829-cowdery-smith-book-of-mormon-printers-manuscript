#!/usr/bin/env python3
"""Flag standard spellings where this scribe often wrote another form (list: tools/scribe-forms.tsv).
Flags only; a human checks the image (about half the flags on Opus output were false alarms in the POC).
Usage: check_spelling.py page-NNN.md [...]"""
import re, sys, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
forms = {}
for l in open(f'{R}/tools/scribe-forms.tsv'):
    if l.startswith('#') or '\t' not in l: continue
    a, b = l.rstrip('\n').split('\t'); forms.setdefault(a, b)
for p in sys.argv[1:]:
    s = open(p).read(); out = []
    lines = [l for l in s.split('\n') if l.strip() and not l.startswith('<!--')]
    for i, l in enumerate(lines, 1):
        for w in re.findall(r"[A-Za-z]+", re.sub(r'<!--.*?-->', '', l)):
            if w.lower() in forms: out.append(f'  line {i}: "{w}" (scribe may have written "{forms[w.lower()]}")')
    print(f'{p}: {len(out)} flag(s)'); print('\n'.join(out))
