# Per-page line-start/trailing hyphen counts (text only; run from repo root, prints a table). Heuristic, not accuracy: see transcription-notes.md (hyphen check entries).
import re,glob,sys
rows=[]
for f in sorted(glob.glob('book-of-mormon-printers-manuscript-pages/page-*.md')):
    n=int(re.search(r'(\d+)\.md',f).group(1))
    L=[]
    for l in open(f).read().split('\n'):
        t=re.sub(r'<!--.*?-->','',l).strip()
        if t: L.append(t)
    brk=pair=0
    for a,b in zip(L,L[1:]):
        # strip trailing tags
        a2=re.sub(r'(\{[^}]*\}@\w+|@\w+)\s*$','',a).rstrip()
        if re.search(r'[A-Za-z]-$',a2):
            brk+=1
            if b.startswith('-'): pair+=1
    start=sum(1 for l in L if l.startswith('-'))
    rows.append((n,len(L),brk,pair,start))
print("page lines endhyph paired linestart")
for r in rows: print(*r)
