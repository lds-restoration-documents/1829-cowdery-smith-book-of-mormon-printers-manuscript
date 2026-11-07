# Left-margin strips at 2x for checking line-start hyphens by eye. Run from repo root: ~/.venvs/lds-transcribe/bin/python tools/margin_zoom.py OUTDIR PAGE... (writes OUTDIR/yNNN.jpg, 4 strips side by side; ruled paper, e.g. pp. 238, 239, 300, confuses it).
import sys
from pathlib import Path
from PIL import Image
IMGS=sorted(Path('source-images').glob('*.jpg'), key=lambda p:[int(x) for x in p.stem.split('_pm_')[1].split('_')[0].split('-')])
out=Path(sys.argv[1])
for n in map(int,sys.argv[2:]):
    im=Image.open(IMGS[n-1]).convert('RGB'); w,h=im.size
    W=150;k=4;q=h//k+30;s=2
    c=Image.new('RGB',(k*(W*s+8),q*s),'white')
    for i in range(k):
        y=max(0,i*h//k-15)
        c.paste(im.crop((0,y,W,y+q)).resize((W*s,q*s)),(i*(W*s+8),0))
    c.save(out/f'y{n:03d}.jpg',quality=88)
