"""X (@popuppush_sa) avatar 400x400 and header 1500x500, same brand style as statics."""
from PIL import Image, ImageDraw
import os
from PIL import ImageFont
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + "/"
def font(s, w="Bold"): return ImageFont.truetype(FD + f"IBMPlexSansArabic-{w}.ttf", s, layout_engine=ImageFont.Layout.RAQM)
def T(d, xy, s, f, fill, anchor="ra"): d.text(xy, s, font=f, fill=fill, anchor=anchor, direction="rtl", language="ar")
CY = (34, 211, 238); GOLD = (250, 206, 13); WH = (255, 255, 255)
from sprite import paste_kafu
OUT = "/mnt/user-data/outputs/"
BG = (10, 14, 26); MUTE = (170, 176, 210)
# avatar
a = Image.new("RGB", (400, 400), (80, 69, 233))
paste_kafu(a, 200, 215, 300, "happy", 0, "idle")
a.save(OUT + "x_avatar.png")
# header
h = Image.new("RGB", (1500, 500), BG); d = ImageDraw.Draw(h)
for i in range(0, 1500, 60): d.line([(i, 0), (i - 200, 500)], fill=(16, 21, 38), width=2)
paste_kafu(h, 560, 255, 300, "happy", 0, "wave1")
R = 1430
T(d, (R, 95), "شاشاتك", font(84), WH)
T(d, (R, 190), "تبيع عنك.", font(84), CY)
T(d, (R, 305), "منيو وعروض ومباريات · من داشبورد واحد أو ريموت بجوالك", font(30, "SemiBold"), MUTE)
T(d, (R, 355), "مقاهي · مطاعم · فنادق · مستشفيات · جهات حكومية", font(28, "SemiBold"), GOLD)
d.text((R, 420), "popuppush.com", font=font(26, "SemiBold"), fill=WH, anchor="ra")
h.save(OUT + "x_header.png")
print("ok")
