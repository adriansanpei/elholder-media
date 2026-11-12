import json, numpy as np, functools
from PIL import Image
S=2.25; H=1350; MAXH=1350
info=json.load(open('info.json')); im=Image.open('full.png').convert('RGB'); a=np.asarray(im)
start=int(info['marcador'][0]*S)-45; end=int(info['criterio'][1]*S)+70
c=a[:,200:900,:].astype(int)
blank=((c.max(axis=1)-c.min(axis=1)).max(axis=1)<=2)&(c.min(axis=1).min(axis=1)>=225)
while not blank[start]: start+=1
runs=[];r=start
while r<end:
    if blank[r]:
        r0=r
        while r<end and blank[r]: r+=1
        m=(r0+r)//2
        if r-r0>=45 and not any(i0*S-4<m<i1*S+4 for i0,i1 in info['imgs']): runs.append(m)
    else: r+=1
pts=[start]+[p for p in runs if start+200<p<end-200]+[end]; n=len(pts)
@functools.lru_cache(None)
def best(i):
    if i==n-1: return (0,0,())
    res=None
    for j in range(i+1,n):
        h=pts[j]-pts[i]
        if h>MAXH: break
        sub=best(j)
        if sub is None: continue
        cand=(sub[0]+1, sub[1]+(1150-h)**2, (j,)+sub[2])
        if res is None or cand[:2]<res[:2]: res=cand
    return res
b=best(0); cuts=[start]+[pts[j] for j in b[2]]; print(cuts,[y-x for x,y in zip(cuts,cuts[1:])])
for i,(y0,y1) in enumerate(zip(cuts,cuts[1:])):
    s=im.crop((0,y0,1080,y1)); h=y1-y0; out=Image.new('RGB',(1080,H)); top=(H-h)//2
    out.paste(s.crop((0,0,1080,1)).resize((1080,max(top,1))),(0,0)); out.paste(s,(0,top))
    out.paste(s.crop((0,h-1,1080,h)).resize((1080,max(H-top-h,1))),(0,top+h))
    out.save(f'../slide-{i+2:02d}.jpg',quality=92)
