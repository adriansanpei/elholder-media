import json, numpy as np, functools, glob, os
from PIL import Image
S=2.25; H=1350; MAXH=1300
info=json.load(open('info.json')); im=Image.open('full.png').convert('RGB'); a=np.asarray(im)
start=int(info['gm'][0]*S)-22; end=None
end0=int(info['abrazo'][0]*2.25)
c=a[:,200:900,:].astype(int)
blank=((c.max(axis=1)-c.min(axis=1)).max(axis=1)<=2)&(c.min(axis=1).min(axis=1)>=225)
while not blank[start]: start+=1
end=int(info['abrazo'][0]*S)-10
while not blank[end]: end-=1
r0=end
while blank[r0-1]: r0-=1
end=min(end,r0+40)
runs=[];r=start
while r<end:
    if blank[r]:
        r0=r
        while r<end and blank[r]: r+=1
        m=(r0+r)//2
        if r-r0>=38 and not any(i0*S-4<m<i1*S+4 for i0,i1 in info['imgs']): runs.append(m)
    else: r+=1
def before(y): return max(p for p in runs if p<y*S)
forced=[before(info['ftm'][0]),before(info['sponsor'][0]),before(info['una'][0])]
def seg(a0,a1):
    pts=[a0]+[p for p in runs if a0+200<p<a1-200]+[a1]; n=len(pts)
    @functools.lru_cache(None)
    def best(i):
        if i==n-1: return (0,0,())
        res=None
        for j in range(i+1,n):
            h=pts[j]-pts[i]
            if h>MAXH: break
            sub=best(j)
            if sub is None: continue
            cand=(sub[0]+1, sub[1]+(1100-h)**2, (j,)+sub[2])
            if res is None or cand[:2]<res[:2]: res=cand
        return res
    b=best(0); return [pts[j] for j in b[2]]
cuts=[start]; bounds=[start]+forced+[end]
for x,y in zip(bounds[:-2],bounds[1:-1]): cuts+=seg(x,y)
cuts.append(end)
print(cuts,[y-x for x,y in zip(cuts,cuts[1:])])
for f in glob.glob('../slide-*.jpg'): os.remove(f)
for i,(y0,y1) in enumerate(zip(cuts,cuts[1:])):
    t_=max(0,(y1-y0-1310+1)//2); y0+=t_; y1-=t_; s=im.crop((0,y0,1080,y1)); h=y1-y0; out=Image.new('RGB',(1080,H),(255,255,255)); top=(H-h)//2
    out.paste(s,(0,top))
    # side strips continue full height
    for x0,x1 in ((0,12),(1068,1080)):
        col=s.crop((x0,0,x1,1)); out.paste(col.resize((x1-x0,top)),(x0,0)); out.paste(col.resize((x1-x0,H-top-h)),(x0,top+h))
    out.save(f'../slide-{i+2:02d}.jpg',quality=92)
