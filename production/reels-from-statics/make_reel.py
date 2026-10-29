import sys, subprocess, json, os
from PIL import Image, ImageFilter, ImageEnhance
W,H,FPS=1080,1920,30
REPO="/home/claude/repo/"
OUT="/home/claude/work/reels/"
def bg_for(im):
    s=max(W/im.width,H/im.height)
    b=im.resize((int(im.width*s)+2,int(im.height*s)+2)).filter(ImageFilter.GaussianBlur(40))
    b=ImageEnhance.Brightness(b).enhance(0.45)
    l=(b.width-W)//2;t=(b.height-H)//2
    return b.crop((l,t,l+W,t+H))
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def render(name, files):
    ims=[Image.open(REPO+f).convert("RGB") for f in files]
    n=len(ims)
    if n==1: durs=[6.5]
    else: durs=[2.8]+[3.2]*(n-2)+[4.0]
    XF=0.35
    starts=[];t=0
    for d in durs: starts.append(t); t+=d-XF
    total=starts[-1]+durs[-1]
    bgs=[bg_for(im) for im in ims]
    TOP=210
    def frame(i,lt,d):
        im=ims[i]; z=1.0+0.045*(lt/d)
        w=int(im.width*z); h=int(im.height*z)
        r=im.resize((w,h),Image.BILINEAR)
        r=r.crop(((w-im.width)//2,(h-im.height)//2,(w-im.width)//2+im.width,(h-im.height)//2+im.height))
        f=bgs[i].copy()
        dy=int(36*(1-ease(lt/0.45)))
        f.paste(r,(0,TOP+dy))
        return f
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
        "-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p",OUT+name+"_v.mp4"],stdin=subprocess.PIPE)
    N=int(total*FPS)
    for k in range(N):
        tt=k/FPS
        cur=max(i for i in range(n) if starts[i]<=tt)
        f=frame(cur,tt-starts[cur],durs[cur])
        if cur>0 and tt-starts[cur]<XF:
            prev=frame(cur-1,tt-starts[cur-1],durs[cur-1])
            f=Image.blend(prev,f,(tt-starts[cur])/XF)
        p.stdin.write(f.tobytes())
    p.stdin.close(); p.wait()
    cuts=",".join(f"{s:.2f}" for s in starts)
    subprocess.run(["python3","/home/claude/work/scripts/music_bed.py",name,f"{total:.2f}",cuts],check=True)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",OUT+name+"_v.mp4","-i",OUT+name+".wav","-c:v","copy",
        "-af","loudnorm=I=-14:TP=-1.5:LRA=11","-c:a","aac","-b:a","160k","-ar","48000","-shortest","-movflags","+faststart",OUT+name+".mp4"],check=True)
    os.remove(OUT+name+"_v.mp4"); os.remove(OUT+name+".wav")
    print(name, round(total,1),"s")
if __name__=="__main__":
    jobs=json.load(open(sys.argv[1]))
    for name in sys.argv[2:]: render(name,jobs[name])
