import json,subprocess
subs=json.load(open('src/subs.json'))
S='/mnt/user-data/attachments/bf5dafc8-53d1-5030-892a-b60a1fbdbbf7/7e4ee972-ZvtivW-jZy6xYSi0.mp4'
D=52.48
inp=['-i',S,'-f','lavfi','-i',f'color=c=0x152F46:s=1080x1920:r=30:d={D}',
     '-loop','1','-t',str(D),'-i','capas/titulo.png','-loop','1','-t',str(D),'-i','capas/fijo.png',
     '-loop','1','-t',str(D),'-i','capas/marca.png','-loop','1','-t','3','-i','capas/cierre.png','-i','musica.wav']
for i,_ in enumerate(subs): inp+=['-loop','1','-t',str(D),'-i',f'capas/sub-{i:02d}.png']
f=['[0:v]fps=30,crop=880:880:520:0,scale=1080:1080:flags=lanczos,format=gbrp[v]','[1:v]format=gbrp[bg]','[bg][v]overlay=0:600:format=gbrp[b0]',
'[2:v]format=rgba,fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st=14.6:d=0.4:alpha=1[ti]','[3:v]format=rgba,fade=t=in:st=15.0:d=0.4:alpha=1[fi]',
'[b0][ti]overlay=0:0:format=gbrp[b1]','[b1][fi]overlay=0:0:format=gbrp[b2]','[b2][4:v]overlay=0:0:format=gbrp[b3]']
last='b3'
for i,(a,z,t) in enumerate(subs):
    f.append(f"[{last}][{7+i}:v]overlay=0:0:format=gbrp:enable='between(t,{a},{z})'[s{i}]"); last=f's{i}'
f+=[f'[{last}]format=yuv420p,setsar=1[main]','[5:v]fps=30,scale=1080:1920,format=yuv420p,setsar=1,fade=t=in:st=0:d=0.35[end]','[main][end]concat=n=2:v=1:a=0[vout]',
'[0:a]aresample=44100,apad=pad_dur=3,atrim=0:55.48[voz]',f"[6:a]volume='if(lt(t,{D}),0.10,0.55)':eval=frame[mus]",'[voz][mus]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[aout]']
subprocess.run(['ffmpeg','-v','error','-y']+inp+['-filter_complex',';'.join(f),'-map','[vout]','-map','[aout]','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','warsh-fed-inflacion.mp4'],check=True)
