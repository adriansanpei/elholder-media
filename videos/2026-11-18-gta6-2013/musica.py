# Melodía synthwave original (estilo Vice City) generada con numpy
import numpy as np, wave
SR=44100; BPM=100; beat=60/BPM; DUR=44.5
N=int(SR*DUR); t=np.arange(N)/SR
out=np.zeros(N)
def note(f): return 440*2**((f-69)/12)
def env(n,a=0.01,r=0.3):
    e=np.ones(n); A=int(a*SR); Rl=int(min(r*SR,n))
    e[:A]=np.linspace(0,1,A) if A else 1
    e[-Rl:]*=np.linspace(1,0,Rl); return e
def saw(f,n,det=0.0):
    tt=np.arange(n)/SR; s=0
    for d in (-det,0,det): s=s+2*((tt*f*(1+d))%1)-1
    return s/3
def add(sig,start):
    i=int(start*SR); j=min(N,i+len(sig))
    if i<N: out[i:j]+=sig[:j-i]
# Progresión Am - F - C - G (2 compases c/u... 1 compás = 4 tiempos)
prog=[(57,[57,60,64]),(53,[53,57,60]),(48,[48,52,55]),(55,[55,59,62])]
bar=4*beat
nbars=int(DUR/bar)+1
for b in range(nbars):
    root,ch=prog[b%4]; t0=b*bar
    # pad
    n=int(bar*SR)
    pad=sum(saw(note(m+12),n,0.004) for m in ch)/3
    pad=np.convolve(pad,np.ones(40)/40,'same')*env(n,0.25,0.4)*0.10
    add(pad,t0)
    # bajo en corcheas
    for k in range(8):
        n=int(beat/2*SR); f=note(root-12)
        s=np.sign(np.sin(2*np.pi*f*np.arange(n)/SR))*0.5+saw(f,n)*0.5
        s=np.convolve(s,np.ones(25)/25,'same')*env(n,0.005,0.12)*0.16
        add(s,t0+k*beat/2)
    # arpegio (entra en el compás 2)
    if b>=1:
        arp=[ch[0]+24,ch[1]+24,ch[2]+24,ch[1]+24]
        for k in range(16):
            n=int(beat/4*SR); f=note(arp[k%4])
            s=saw(f,n,0.003)*env(n,0.003,0.08)*0.055
            add(s,t0+k*beat/4)
    # batería (entra en el compás 1)
    for k in range(4):
        tb=t0+k*beat
        n=int(0.35*SR); tt=np.arange(n)/SR
        kick=np.sin(2*np.pi*(50+90*np.exp(-tt*35))*tt)*np.exp(-tt*9)*0.45
        add(kick,tb)
        if k%2==1:
            n=int(0.25*SR); tt=np.arange(n)/SR
            sn=(np.random.randn(n)*0.6+np.sin(2*np.pi*190*tt)*0.4)*np.exp(-tt*14)*0.22
            add(sn,tb)
        for h in (0,0.5):
            n=int(0.06*SR); hh=np.random.randn(n)*np.exp(-np.arange(n)/SR*70)*0.05
            hh=hh-np.convolve(hh,np.ones(8)/8,'same'); add(hh,tb+h*beat)
# fade in/out
fi=int(0.8*SR); fo=int(2.5*SR)
out[:fi]*=np.linspace(0,1,fi); out[-fo:]*=np.linspace(1,0,fo)
out=out/np.max(np.abs(out))*0.8
st=np.stack([out,np.roll(out,int(0.012*SR))*0.95],1)
with wave.open('musica.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st*32767).astype(np.int16).tobytes())
print('ok')
