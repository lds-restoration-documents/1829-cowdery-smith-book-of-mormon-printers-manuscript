# Builds a local human-review page for undecided folio numbers. Run from repo root:
#   ~/.venvs/lds-transcribe/bin/python tools/make_folio_review.py [PAGE ...]   (default: the 31 undecided pages + 250)
# Writes work/folio-review/index.html and img/ (gitignored; images stay local). Open index.html in a browser.
# Decisions are kept in the browser (localStorage) and exported with a button as folio-decisions.tsv / .json.
import sys, re, json, html
from pathlib import Path
from PIL import Image
DEFAULT=[23,27,62,70,101,103,105,108,112,154,164,173,229,244,250,279,284,293,302,314,316,326,331,347,349,353,377,384,387,420,455,457]
pages=[int(a) for a in sys.argv[1:]] or DEFAULT
IMGS=sorted(Path('source-images').glob('*.jpg'), key=lambda p:[int(x) for x in p.stem.split('_pm_')[1].split('_')[0].split('-')])
out=Path('work/folio-review'); (out/'img').mkdir(parents=True,exist_ok=True)
def folio_of(n):
    try: t=Path(f'book-of-mormon-printers-manuscript-pages/page-{n:03d}.md').read_text()
    except FileNotFoundError: return ''
    m=re.search(r'<!--\s*folio ([^;)\n]*?)\s*(?:[;)]|-->)',t); return m.group(1) if m else ''
def comment_of(n):
    t=Path(f'book-of-mormon-printers-manuscript-pages/page-{n:03d}.md').read_text()
    m=re.search(r'<!--\s*folio[^\n]*?-->',t); return m.group(0) if m else ''
fin={}
for l in Path('work/folio2/final.tsv').read_text().splitlines():
    f=l.split('\t')
    if f[0].isdigit(): fin[int(f[0])]=f
cards=[]
for n in pages:
    im=Image.open(IMGS[n-1]).convert('RGB'); w,h=im.size
    im.crop((0,0,w,int(h*0.13))).save(out/f'img/top{n:03d}.jpg',quality=90)
    im.crop((int(w*0.55),0,w,int(h*0.09))).resize((int(w*0.45)*2,int(h*0.09)*2)).save(out/f'img/tr{n:03d}.jpg',quality=90)
    im.crop((0,0,int(w*0.45),int(h*0.09))).resize((int(w*0.45)*2,int(h*0.09)*2)).save(out/f'img/tl{n:03d}.jpg',quality=90)
    im.resize((900,int(900*h/w))).save(out/f'img/full{n:03d}.jpg',quality=80)
    f=fin.get(n,[])
    cards.append(dict(page=n,file=comment_of(n),prev=folio_of(n-1),next=folio_of(n+1),
        blind=f[2] if len(f)>2 else '',blindc=f[3] if len(f)>3 else '',close=f[4] if len(f)>4 else '',closec=f[5] if len(f)>5 else '',note=f[6] if len(f)>6 else '',seq=str(n-4)))
tpl=Path(__file__).with_name('folio_review_template.html').read_text()
(out/'index.html').write_text(tpl.replace('/*DATA*/',json.dumps(cards)))
print('wrote',out/'index.html',len(cards),'pages')
