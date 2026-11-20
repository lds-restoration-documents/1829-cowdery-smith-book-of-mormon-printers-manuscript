# Filter margin-hyphen agent results before patching (tools/README.md step 3b). Usage: python3 tools/accept_hyphen_results.py "work/hy/r95-104.tsv" OUT.tsv   (appends accepted rows "PAGE<TAB>lines" to OUT.tsv, skipped lines to work/hy/skipped2.txt). Keeps a reported line only if the page file line already starts with "-" or its first 2 letters match the reported letters; then run tools/patch_linestart_hyphens.py --file OUT.tsv (dry run) and --apply.
import re,glob,sys
from pathlib import Path
P=Path('book-of-mormon-printers-manuscript-pages'); CO=re.compile(r'\s*(<!--.*?-->\s*)+')
import subprocess
acc={};sus=[];tot=0
for f in sorted(glob.glob(sys.argv[1])):
    for row in open(f):
        pg,_,s=row.strip().partition('\t'); pg=int(pg)
        if s in('','-'):continue
        lines=[l for l in (P/f'page-{pg:03d}.md').read_text().split('\n') if l.strip() and not CO.fullmatch(l)]
        for it in s.split(','):
            n,_,L=it.partition(':'); n=int(n); tot+=1
            if n>len(lines): sus.append(f'{pg}:{n}:{L}:range');continue
            t=re.sub(r'[\^~{}@\[\]<>*_|\s-]','',lines[n-1]).lower()
            if lines[n-1].startswith('-') or t[:2]==L.lower()[:2]: acc.setdefault(pg,[]).append(n)
            else: sus.append(f'{pg}:{n}:{L}')
print('reported',tot,'accepted',sum(len(v) for v in acc.values()),'skipped',len(sus))
open(sys.argv[2],'a').write(''.join(f"{pg}\t{','.join(map(str,sorted(set(v))))}\n" for pg,v in sorted(acc.items())))
open('work/hy/skipped2.txt','a').write(' '.join(sus)+'\n')
