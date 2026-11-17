import sys, os, subprocess
from playwright.sync_api import sync_playwright
H=os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
FPS=30
SC=[0, 2.42, 8.62, 13.66, 21.17, 24.67, 38.7, 53.45, 61.36, 75.83, 77.5]
mode=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file://'+H+'/reel.html'); pg.wait_for_timeout(800)
    if mode=='test':
        for t in [float(x) for x in sys.argv[2:]]:
            pg.evaluate(f'setT({t})'); pg.screenshot(path=f'/tmp/claude-0/-home-claude/bf5dafc8-53d1-5030-892a-b60a1fbdbbf7/scratchpad/f{t}.jpg',type='jpeg',quality=80)
    else:
        os.makedirs('scenes',exist_ok=True)
        f0=0
        for k in range(len(SC)-1):
            f1=round(SC[k+1]*FPS); tmp=f'scenes/tmp{k:02d}.mp4'; out=f'scenes/s{k:02d}.mp4'
            ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','-r',str(FPS),tmp],stdin=subprocess.PIPE)
            for f in range(f0,f1):
                pg.evaluate(f'setT({f/FPS})'); ff.stdin.write(pg.screenshot(type='jpeg',quality=92))
            ff.stdin.close(); assert ff.wait()==0; os.rename(tmp,out); print(k,f1-f0,flush=True); f0=f1
    b.close()
