from PIL import Image, ImageDraw, ImageFont
import numpy as np
K='/home/claude/popuppush-media/kafu/'; O=K+'v2/'
F='/home/claude/popuppush-media/production/kafu-diaries/fonts/IBMPlexSansArabic-Bold.ttf'
def font(s): return ImageFont.truetype(F,s,layout_engine=ImageFont.Layout.RAQM)
def near(a,c,t=40): return np.abs(a.astype(int)-np.array(c)).sum(-1)<t
def bbox(mask):
    ys,xs=np.where(mask); return xs.min(),ys.min(),xs.max(),ys.max()
def text_c(d,box,txt,col,size):
    f=font(size); cx=(box[0]+box[2])/2; cy=(box[1]+box[3])/2
    d.text((cx,cy),txt,font=f,fill=col,anchor='mm',direction='rtl',language='ar')
def fix_chip(name,label='يوميات كفو'):
    im=Image.open(K+name).convert('RGB'); a=np.array(im)
    bg=tuple(a[20,20]); 
    # find chip color at x=90
    col=None
    for y in range(30,260):
        if not near(a[y:y+1,90:91],bg,30)[0,0]: col=tuple(int(v) for v in a[y+6,95]); ys=y; break
    reg=np.zeros(a.shape[:2],bool); reg[ys-2:ys+55,60:450]=near(a[ys-2:ys+55,60:450],col,30)
    x0,y0,x1,y1=bbox(reg)
    lum=sum(col)/3; tc=(10,14,26) if lum>140 else (255,255,255)
    d=ImageDraw.Draw(im)
    d.rectangle((x0-3,y0-3,x1+3,y1+3),fill=bg)
    h=y1-y0; f=font(int(h*0.5)); w=d.textlength(label,font=f,direction='rtl',language='ar')
    nx1=x0+int(w+h*0.9)
    d.rounded_rectangle((x0,y0,nx1,y1),radius=h//2,fill=col)
    text_c(d,(x0,y0-2,nx1,y1-2),label,tc,int(h*0.5))
    print(name,col,(x0,y0,x1,y1)); return im
for n in ['01_hello.jpg','02_day.jpg','03_remote.jpg']:
    fix_chip(n).save(O+n,quality=95)
# 04: chip + pad to 4:5
im=fix_chip('04_offline.jpg'); bg=im.getpixel((20,20))
c=Image.new('RGB',(1080,1350),bg); c.paste(im,(0,135)); c.save(O+'04_offline.jpg',quality=95)
# 05 story: chip + button text
im=fix_chip('05_matchnight_story.jpg'); a=np.array(im)
reg=np.zeros(a.shape[:2],bool); reg[1730:1830,300:780]=near(a[1730:1830,300:780],(255,255,255),20)
x0,y0,x1,y1=bbox(reg); d=ImageDraw.Draw(im); bg=tuple(a[1890,40])
d.rectangle((x0-3,y0-3,x1+3,y1+3),fill=bg)
lab='واتساب 0583272051'; f=font(34); w=d.textlength(lab,font=f,direction='rtl',language='ar')
cx=540; hw=int(w/2+50); d.rounded_rectangle((cx-hw,y0,cx+hw,y1),radius=(y1-y0)//2,fill=(255,255,255))
text_c(d,(cx-hw,y0-3,cx+hw,y1-3),lab,(10,60,45),34)
print('btn',(x0,y0,x1,y1)); im.save(O+'05_matchnight_story.jpg',quality=95)
# 06 footer
im=Image.open(K+'06_main.jpg').convert('RGB'); a=np.array(im); bg=tuple(a[1340,20])
reg=np.zeros(a.shape[:2],bool); reg[1240:1310,600:1010]=near(a[1240:1310,600:1010],(255,255,255),120)
x0,y0,x1,y1=bbox(reg); d=ImageDraw.Draw(im); d.rectangle((560,y0-6,1010,y1+6),fill=bg)
f=font(30); d.text((x1,(y0+y1)/2-2),'واتساب 0583272051',font=f,fill=(255,255,255),anchor='rm',direction='rtl',language='ar')
print('foot',(x0,y0,x1,y1)); im.save(O+'06_main.jpg',quality=95)
