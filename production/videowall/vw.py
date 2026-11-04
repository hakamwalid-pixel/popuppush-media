"""PopupPush — video wall reel (1080x1920, 30fps). Usage: python3 vw.py <scene|all> [still_t ...]"""
import sys, os, math, subprocess
sys.path.insert(0, "/root/vw/media/production/kafu-diaries")
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from sprite import paste_kafu

FD = "/root/vw/media/production/kafu-diaries/fonts/"
_fc = {}
def F(s, w="Bold"):
    k = (s, w)
    if k not in _fc: _fc[k] = ImageFont.truetype(FD + f"IBMPlexSansArabic-{w}.ttf", s, layout_engine=ImageFont.Layout.RAQM)
    return _fc[k]
W, H, FPS = 1080, 1920, 30
BG = (10, 14, 26); CY = (34, 211, 238); IND = (99, 102, 241); GOLD = (250, 206, 13); WH = (255, 255, 255)
MUTE = (170, 176, 210); LINE = (40, 46, 80)
def T(d, xy, s, f, fill, anchor="ra"): d.text(xy, s, font=f, fill=fill, anchor=anchor, direction="rtl", language="ar")
def ease(x): x = max(0, min(1, x)); return x * x * (3 - 2 * x)
def seg(t, a, b): return ease((t - a) / (b - a))

# ---------- wall geometry ----------
SW, SH, BZ, GAP = 220, 440, 11, 12
N = 4
SEAM = 4  # thin seam when the screens are joined
def pitch(j): return SW + (2 * BZ + GAP) * (1 - j) + SEAM * j
def bz(j): return BZ * (1 - j) + (SEAM / 2) * j
def wall_w(j): return N * SW + (N - 1) * (pitch(j) - SW) + 2 * bz(j)
WALL_W = wall_w(0)
WX0 = (W - WALL_W) // 2; WY0 = 840
def inner(i, j=0.0):  # i=0 is rightmost (RTL reading), x from left
    k = N - 1 - i
    x0 = (W - wall_w(j)) / 2 + bz(j)
    x = int(round(x0 + k * pitch(j)))
    return (x, WY0 + BZ, x + SW, WY0 + BZ + SH)
UW, UH = N * SW, SH  # the ad is split into equal slices — nothing hides behind bezels
UY0 = WY0 + BZ

MENUS = [
    ("قهوة", [("قهوة سعودية", "١٢"), ("لاتيه", "١٨"), ("V60", "٢٢"), ("كورتادو", "١٦")], CY),
    ("باردة", [("آيس لاتيه", "١٩"), ("موهيتو", "٢١"), ("ليمون نعناع", "١٤"), ("سبانش", "٢٠")], IND),
    ("حلى", [("تشيز كيك", "٢٤"), ("كوكيز", "١٢"), ("تيراميسو", "٢٦"), ("كنافة", "٢٢")], GOLD),
    ("فطور", [("شكشوكة", "٢٨"), ("فول", "١٨"), ("كرواسون", "١٥"), ("بان كيك", "٢٥")], (244, 114, 182)),
]
def menu_img(i, t):
    title, items, acc = MENUS[i]
    im = Image.new("RGB", (SW, SH), (16, 20, 38)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, SW, 74), fill=acc)
    T(d, (SW // 2, 37), title, F(36), (10, 14, 26), "mm")
    for j, (n, p) in enumerate(items):
        y = 110 + j * 80
        T(d, (SW - 16, y), n, F(23, "SemiBold"), WH, "ra")
        T(d, (16, y + 28), p + " ر.س", F(21), acc, "la")
        d.line((16, y + 64, SW - 16, y + 64), fill=(36, 42, 70), width=1)
    # gentle live highlight bar
    hj = int(t * 0.8 + i) % 4; y = 110 + hj * 80
    d.rectangle((0, y - 6, 5, y + 50), fill=acc)
    return im

def ad_img(t):
    """One big picture across the whole wall."""
    im = Image.new("RGB", (UW, UH)); d = ImageDraw.Draw(im)
    for x in range(UW):  # warm gradient
        a = x / UW
        c = tuple(int(c1 * (1 - a) + c2 * a) for c1, c2 in zip((80, 69, 233), (255, 140, 40)))
        d.line((x, 0, x, UH), fill=c)
    # faint drifting bokeh (kept soft so the words stay clear)
    bo = Image.new("RGBA", (UW, UH), (0, 0, 0, 0)); bd = ImageDraw.Draw(bo)
    for k in range(9):
        cx = (k * 137 + t * 90 * (1 + k % 3)) % (UW + 200) - 100
        cy = 60 + (k * 71) % (UH - 120) + 18 * math.sin(t * 2 + k)
        r = 26 + (k * 13) % 40
        bd.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 255, 255, 60), width=2)
    im.paste(bo, (0, 0), bo)
    # small cup gliding along the bottom strip, below the words
    cx = UW + 120 - (UW + 240) * ((t * 0.16) % 1.0); cy = UH - 62
    d.rounded_rectangle((cx - 40, cy - 34, cx + 40, cy + 40), 14, fill=WH)
    d.ellipse((cx + 30, cy - 18, cx + 64, cy + 16), outline=WH, width=9)
    d.rectangle((cx - 40, cy - 34, cx + 40, cy - 24), fill=(120, 72, 40))
    # words with a soft shadow, fully inside the picture
    sh = Image.new("RGBA", (UW, UH), (0, 0, 0, 0)); sdd = ImageDraw.Draw(sh)
    T(sdd, (UW // 2 + 4, int(UH * 0.27) + 6), "عرض الليلة", F(176), (0, 0, 0, 110), "mm")
    T(sdd, (UW // 2 + 3, int(UH * 0.68) + 4), "قهوتك + حلاك المفضّل", F(60), (0, 0, 0, 110), "mm")
    im.paste(sh.filter(ImageFilter.GaussianBlur(6)), (0, 0), sh.filter(ImageFilter.GaussianBlur(6)))
    T(d, (UW // 2, int(UH * 0.27)), "عرض الليلة", F(176), WH, "mm")
    T(d, (UW // 2, int(UH * 0.68)), "قهوتك + حلاك المفضّل", F(60), (255, 240, 210), "mm")
    # light sweep
    sx = int((t * 520) % (UW + 600)) - 300
    sweep = Image.new("L", (UW, UH), 0); sd = ImageDraw.Draw(sweep)
    sd.polygon([(sx, 0), (sx + 120, 0), (sx + 20, UH), (sx - 100, UH)], fill=70)
    im.paste((255, 255, 255), (0, 0), sweep.filter(ImageFilter.GaussianBlur(18)))
    return im

def wall(img, t, wipe, back, j=0.0):
    """wipe: 0..1 ad sweeping in from right; back: 0..1 menus returning from left; j: 0..1 screens pulled together."""
    d = ImageDraw.Draw(img)
    # wall panel + pendant lamps
    d.rounded_rectangle((WX0 - 30, WY0 - 60, WX0 + WALL_W + 30, WY0 + SH + 2 * BZ + 60), 28, fill=(20, 25, 44))
    for k in range(N):
        x0, _, x1, _ = inner(k, j); cx = (x0 + x1) // 2
        d.line((cx, WY0 - 180, cx, WY0 - 92), fill=(60, 66, 100), width=3)
        d.pieslice((cx - 34, WY0 - 120, cx + 34, WY0 - 52), 180, 360, fill=(60, 66, 100))
        d.ellipse((cx - 10, WY0 - 94, cx + 10, WY0 - 80), fill=(255, 220, 140))
    ad = ad_img(t) if (wipe > 0 and back < 1) else None
    # wipe boundaries in wall coords
    edge_in = UW - (UW + 60) * wipe          # ad covers ad-x >= edge_in
    edge_out = -60 + (UW + 60) * back        # menus come back for ad-x <= edge_out
    b = bz(j)
    for i in range(N):
        x0, y0, x1, y1 = inner(i, j)
        d.rounded_rectangle((x0 - b, y0 - BZ, x1 + b, y1 + BZ), int(10 * (1 - j)), fill=(4, 5, 9))
    for i in range(N):
        x0, y0, x1, y1 = inner(i, j); ox = (N - 1 - i) * SW
        scr = menu_img(i, t)
        if ad is not None:
            piece = ad.crop((ox, 0, ox + SW, UH))
            m = Image.new("L", (SW, SH), 0); md = ImageDraw.Draw(m)
            lo = int(max(0, edge_in - ox)); hi = int(min(SW, edge_out - ox)) if back > 0 else -1
            if lo < SW: md.rectangle((lo, 0, SW, SH), fill=255)
            if back > 0 and hi > 0: md.rectangle((0, 0, hi, SH), fill=0)
            scr.paste(piece, (0, 0), m)
        img.paste(scr, (x0, y0))
        d.rectangle((x0, y0, x1, y0 + 2), fill=(70, 76, 110))  # glass glint
    # counter
    cy = WY0 + SH + 2 * BZ + 60
    d.rectangle((0, cy, W, cy + 22), fill=(48, 40, 34)); d.rectangle((0, cy + 22, W, cy + 140), fill=(30, 25, 22))

HEADS = [  # (start, end, line1, line2, accent, sub)
    (0.0, 4.6, "عندك صف شاشات", "كل وحدة لحالها؟", CY, "منيو هون… ومنيو هناك."),
    (4.6, 7.4, "خلّيها شاشة", "وحدة كبيرة.", GOLD, "بدون أي أجهزة إضافية."),
    (7.4, 13.8, "إعلان واحد", "على كل الشاشات.", GOLD, "يلفت نظر كل اللي بالمحل."),
    (13.8, 17.6, "وبعدها كل شاشة", "ترجع لمنيوها.", CY, "تلقائي، بدون ما تلمس شي."),
]
def headline(img, t):
    for a, b, l1, l2, acc, sub in HEADS:
        if a - 0.01 <= t < b:
            fi = seg(t, a, a + 0.45) if a > 0 else seg(t, 0.15, 0.6)
            fo = 1 - seg(t, b - 0.3, b) if b < 17.6 else 1 - seg(t, b - 0.35, b)
            al = min(fi, fo); dy = int(30 * (1 - fi))
            lay = Image.new("RGBA", (W, 460), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            T(d, (W - 80, 20), l1, F(92), WH)
            T(d, (W - 80, 140), l2, F(92), acc)
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * al)))
            img.paste(lay, (0, 250 + dy), lay)
            sl = Image.new("RGBA", (W, 120), (0, 0, 0, 0)); sd = ImageDraw.Draw(sl)
            T(sd, (W // 2, 60), sub, F(54, "SemiBold"), WH, "mm")
            sl.putalpha(sl.getchannel("A").point(lambda v: int(v * al)))
            img.paste(sl, (0, 1590 + dy // 2), sl)

def chrome(img, chip="فيديو وول"):
    d = ImageDraw.Draw(img)
    d.text((W - 80, 130), "PopupPush", font=F(44), fill=WH, anchor="rm")
    w = d.textlength(chip, font=F(30), direction="rtl", language="ar")
    d.rounded_rectangle((80, 104, 80 + w + 44, 156), 26, fill=CY)
    T(d, (80 + (w + 44) / 2, 130), chip, F(30), BG, "mm")
    d.line((80, 1760, W - 80, 1760), fill=LINE, width=2)
    T(d, (W - 80, 1812), "راسلنا واتساب", F(38), WH, "rm")
    d.text((80, 1812), "popuppush.com", font=F(36, "SemiBold"), fill=MUTE, anchor="lm")

def end_card(img, t):  # t local from 0
    d = ImageDraw.Draw(img)
    a = seg(t, 0, 0.5)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    T(ld, (W - 80, 300), "شاشاتك…", F(104), WH)
    T(ld, (W - 80, 430), "صارت فيديو وول.", F(104), GOLD)
    bul = ["حتى ٦ شاشات · عمودي أو أفقي", "بدون أي أجهزة إضافية", "من داشبورد واحد، أو من تطبيق", "الريموت كنترول على جوالك"]
    for k, s in enumerate(bul):
        y = 640 + k * 74 + (24 if k >= 3 else 0) - (24 if k == 3 else 0)
        if k == 3: y = 640 + 2 * 74 + 60
        if k < 3:
            ld.ellipse((W - 92, y + 22, W - 74, y + 40), fill=CY)
            T(ld, (W - 110, y), s, F(48, "SemiBold"), WH)
        else:
            T(ld, (W - 110, y), s, F(48, "SemiBold"), WH)
    b = seg(t, 0.6, 1.1)
    pw = 600; px1 = W - 80; px0 = px1 - pw; py = 1500 + int(30 * (1 - b))
    ld.rounded_rectangle((px0, py, px1, py + 120), 60, fill=GOLD + (int(255 * b),))
    T(ld, ((px0 + px1) // 2, py + 60), "اطلب عرض تجريبي", F(50), BG + (int(255 * b),), "mm")
    lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
    img.paste(lay, (0, 0), lay)
    bob = int(10 * math.sin(t * 4))
    paste_kafu(img, 270, 1240 + bob, 380, "happy", 0, "wave1" if int(t * 3) % 2 else "idle")

TOTAL = 21.0
SCENES = [("s1", 0.0, 4.6), ("s2", 4.6, 7.4), ("s3", 7.4, 13.8), ("s4", 13.8, 17.6), ("s5", 17.6, TOTAL)]

def frame(t):
    img = Image.new("RGB", (W, H), BG)
    if t < 17.6:
        intro = seg(t, 0, 0.9)
        wipe = seg(t, 7.2, 8.6); back = seg(t, 13.6, 15.0)
        jn = seg(t, 5.0, 6.4) * (1 - seg(t, 15.0, 16.0))
        wall(img, t, wipe, back, jn)
        if t < 1.6:
            d = ImageDraw.Draw(img)
            for i in range(N):
                on = seg(t, 0.2 + i * 0.25, 0.5 + i * 0.25)
                if on < 1:
                    x0, y0, x1, y1 = inner(i)
                    ov = Image.new("RGBA", (SW, SH), (4, 5, 9, int(255 * (1 - on))))
                    img.paste(ov, (x0, y0), ov)
        # "one screen" outline pulse in s2
        if 4.8 < t < 7.6:
            p = seg(t, 4.8, 5.4) * (1 - seg(t, 7.2, 7.6))
            d = ImageDraw.Draw(img)
            c = tuple(int(BG[k] * (1 - p) + GOLD[k] * p) for k in range(3))
            ux0 = inner(N - 1, jn)[0]; ux1 = inner(0, jn)[2]
            d.rounded_rectangle((ux0 - 26, UY0 - BZ - 14, ux1 + 26, UY0 + SH + BZ + 14), 18, outline=c, width=6)
        headline(img, t)
        if t > 17.2:
            fade = seg(t, 17.2, 17.6)
            img = Image.blend(img, Image.new("RGB", (W, H), BG), fade)
    else:
        end_card(img, t - 17.6)
    chrome(img)
    return img

def render(name, a, b):
    out = f"/root/vw/{name}.mp4"; tmp = f"/root/vw/{name}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    n0, n1 = round(a * FPS), round(b * FPS)
    for n in range(n0, n1): p.stdin.write(frame(n / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, out)

if __name__ == "__main__":
    if sys.argv[1] == "still":
        for s in sys.argv[2:]: frame(float(s)).save(f"/root/vw/still_{s}.jpg", quality=90)
    else:
        for nm, a, b in SCENES:
            if sys.argv[1] in ("all", nm): render(nm, a, b)
