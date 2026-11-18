import subprocess, os
from playwright.sync_api import sync_playwright
H=os.path.abspath('reel.html'); FPS=30; END=44.5
SC=[0,4.2,8.6,12.6,23.6,28.6,34.6,40.1,44.5]
os.makedirs('scenes',exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file://'+H); pg.wait_for_timeout(800)
    for i in range(len(SC)-1):
        f0=round(SC[i]*FPS); f1=round(SC[i+1]*FPS)
        tmp=f'scenes/s{i:02d}.tmp.mp4'
        ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-i','-',
            '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',tmp],stdin=subprocess.PIPE)
        for f in range(f0,f1):
            pg.evaluate(f'setT({f/FPS})')
            ff.stdin.write(pg.screenshot(type='jpeg',quality=92))
        ff.stdin.close()
        if ff.wait()==0: os.replace(tmp,f'scenes/s{i:02d}.mp4')
    b.close()
with open('scenes/list.txt','w') as l:
    for i in range(len(SC)-1): l.write(f"file 's{i:02d}.mp4'\n")
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','scenes/list.txt','-c','copy','video.mp4'],check=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','video.mp4','-i','musica.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','160k','-shortest','reel-gta6-2013.mp4'],check=True)
print('listo')
