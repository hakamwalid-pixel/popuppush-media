"""PopupPush video wall — cinematic cut (1080x1920, 30fps). python3 cin.py <scene|all|still t...>"""
import sys, os, math, subprocess
import numpy as np
sys.path.insert(0, "/root/vw")
import vw
from vw import inner, menu_img, SW, SH, N, UW, UH, W, H, FPS, seg, ease, T as TR
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

FDIR = "/root/vw/fonts/"
_fc = {}
def K(size, wght=500):  # Noto Kufi Arabic (variable)
    k = ("kufi", size, wght)
    if k not in _fc:
        f = ImageFont.truetype(FDIR + "NotoKufiArabic[wght].ttf", size, layout_engine=ImageFont.Layout.RAQM)
        f.set_variation_by_axes([wght]); _fc[k] = f
    return _fc[k]
def CZ(size, wght=600):
    k = ("cz", size, wght)
    if k not in _fc:
        f = ImageFont.truetype(FDIR + "Cinzel[wght].ttf", size); f.set_variation_by_axes([wght]); _fc[k] = f
    return _fc[k]
PB = vw.F  # IBM Plex (brand wordmark)
GOLD = (232, 190, 110); CREAM = (245, 232, 210); WH = (255, 255, 255)
PIC_Y0, PIC_H = 285, 1350  # picture area inside letterbox
TOTAL = 24.0
SCENES = [("c1", 0.0, 3.8), ("c2", 3.8, 6.6), ("c3", 6.6, 13.6), ("c4", 13.6, 17.6), ("c5", 17.6, TOTAL)]

def spaced(s, n=1): return s  # Arabic must stay joined — no letter-spacing hacks

# ---------- static world (Najdi-toned night interior) ----------
def build_bg():
    a = np.zeros((H, W, 3), np.float32)
    y = np.linspace(0, 1, H)[:, None]
    base = np.array([22, 16, 13], np.float32); top = np.array([8, 7, 8], np.float32)
    a[:] = top * (1 - y[..., None] * 0) * (1 - y)[..., None] + base * y[..., None]
    # mud-wall texture
    rng = np.random.default_rng(3)
    tex = rng.normal(0, 1, (H // 6, W // 6)).astype(np.float32)
    tex = np.array(Image.fromarray(((tex * 20) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(3)), np.float32) - 128
    a += tex[..., None] * 0.18
    img = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    # far warm bokeh
    bo = Image.new("RGB", (W, H), 0); bd = ImageDraw.Draw(bo)
    for k in range(26):
        x = rng.uniform(0, W); yy = rng.uniform(380, 760); r = rng.uniform(10, 34)
        c = (int(rng.uniform(150, 255)), int(rng.uniform(90, 160)), int(rng.uniform(30, 70)))
        bd.ellipse((x - r, yy - r, x + r, yy + r), fill=c)
    bo = bo.filter(ImageFilter.GaussianBlur(14))
    img = ImageChops.add(img, ImageChops.multiply(bo, Image.new("RGB", (W, H), (110, 110, 110))))
    # Najdi triangle frieze above the wall
    d = ImageDraw.Draw(img)
    for x in range(-20, W + 40, 40):
        d.polygon([(x, 700), (x + 20, 676), (x + 40, 700)], fill=(44, 33, 26))
    # glossy counter
    cy = vw.WY0 + SH + 2 * vw.BZ + 70
    d.rectangle((0, cy, W, cy + 6), fill=(80, 60, 44))
    d.rectangle((0, cy + 6, W, H), fill=(14, 11, 10))
    return img, cy
BG, COUNTER_Y = build_bg()

# lamp glow layer (static)
def lamp_layer(j):
    L = Image.new("RGB", (W, H), 0); d = ImageDraw.Draw(L)
    for k in range(N):
        x0, _, x1, _ = inner(k, 0.0); cx = (x0 + x1) // 2; wy = vw.WY0
        d.line((cx, 0, cx, wy - 120), fill=(40, 34, 30), width=3)
        d.pieslice((cx - 40, wy - 150, cx + 40, wy - 70), 180, 360, fill=(52, 42, 34))
        d.ellipse((cx - 12, wy - 116, cx + 12, wy - 100), fill=(255, 214, 150))
    return L
LAMPS = lamp_layer(0)
GL = Image.new("RGB", (W, H), 0); _gd = ImageDraw.Draw(GL)
for k in range(N):
    x0, _, x1, _ = inner(k, 0.0); cx = (x0 + x1) // 2
    _gd.polygon([(cx - 14, vw.WY0 - 104), (cx + 14, vw.WY0 - 104), (cx + 120, vw.WY0 + 40), (cx - 120, vw.WY0 + 40)], fill=(120, 80, 40))
    _gd.ellipse((cx - 40, vw.WY0 - 140, cx + 40, vw.WY0 - 70), fill=(255, 190, 110))
LAMP_GLOW = GL.filter(ImageFilter.GaussianBlur(38))

# ---------- the ad (luxury, one picture split evenly across screens) ----------
def ad_cin(t):
    yy, xx = np.mgrid[0:UH, 0:UW].astype(np.float32)
    cx = UW * (0.5 + 0.18 * math.sin(t * 0.5)); r = np.sqrt(((xx - cx) / UW) ** 2 + ((yy - UH * 0.45) / UH) ** 2 * 0.6)
    g = np.clip(1 - r * 1.6, 0, 1)[..., None]
    arr = np.array([12, 8, 6], np.float32) * (1 - g) + np.array([92, 54, 26], np.float32) * g
    im = Image.fromarray(arr.astype(np.uint8)); d = ImageDraw.Draw(im)
    # thin gold frame
    d.rectangle((26, 26, UW - 27, UH - 27), outline=(150, 112, 60), width=2)
    # gold text with vertical gradient
    def gold_text(s, f, cy):
        m = Image.new("L", (UW, UH), 0); md = ImageDraw.Draw(m)
        TR(md, (UW // 2, cy), s, f, 255, "mm")
        grad = np.linspace(0, 1, UH)[:, None, None]
        ga = np.array([255, 232, 170], np.float32) * (1 - grad) + np.array([190, 130, 50], np.float32) * grad
        gimg = Image.fromarray(np.broadcast_to(ga, (UH, UW, 3)).astype(np.uint8))
        sh = m.filter(ImageFilter.GaussianBlur(8))
        im.paste((0, 0, 0), (0, 0), sh.point(lambda v: int(v * 0.6)))
        im.paste(gimg, (0, 0), m)
    gold_text("عرض الليلة", K(150, 700), int(UH * 0.36))
    TR(d, (UW // 2, int(UH * 0.66)), "قهوتك + حلاك المفضّل", K(46, 500), CREAM, "mm")
    d.line((UW // 2 - 120, int(UH * 0.80), UW // 2 + 120, int(UH * 0.80)), fill=(170, 125, 65), width=2)
    # drifting gold dust
    rng = np.random.default_rng(7); dust = Image.new("L", (UW, UH), 0); dd = ImageDraw.Draw(dust)
    for k in range(60):
        x0 = rng.uniform(0, UW); y0 = rng.uniform(0, UH); sp = rng.uniform(8, 30); ph = rng.uniform(0, 6.28)
        x = (x0 + t * sp) % UW; y = (y0 - t * sp * 0.6) % UH; s = rng.uniform(1, 3)
        dd.ellipse((x - s, y - s, x + s, y + s), fill=int(140 + 110 * math.sin(t * 2 + ph)))
    im.paste((255, 214, 150), (0, 0), dust.filter(ImageFilter.GaussianBlur(0.8)))
    # slow light sweep
    sx = int((t * 260) % (UW + 700)) - 350
    sw = Image.new("L", (UW, UH), 0); sd = ImageDraw.Draw(sw)
    sd.polygon([(sx, 0), (sx + 90, 0), (sx - 10, UH), (sx - 100, UH)], fill=55)
    im.paste((255, 240, 210), (0, 0), sw.filter(ImageFilter.GaussianBlur(22)))
    return im

# ---------- screens layer ----------
def screens(t, wipe, back, j, power):
    S = Image.new("RGB", (W, H), 0); d = ImageDraw.Draw(S)
    b = vw.bz(j)
    for i in range(N):
        x0, y0, x1, y1 = inner(i, j)
        d.rounded_rectangle((x0 - b, y0 - vw.BZ, x1 + b, y1 + vw.BZ), int(8 * (1 - j)), fill=(3, 3, 4))
    ad = ad_cin(t) if (wipe > 0 and back < 1) else None
    edge_in = UW - (UW + 60) * wipe; edge_out = -60 + (UW + 60) * back
    for i in range(N):
        x0, y0, x1, y1 = inner(i, j); ox = (N - 1 - i) * SW
        scr = menu_img(i, t)
        if ad is not None:
            piece = ad.crop((ox, 0, ox + SW, UH)); m = Image.new("L", (SW, SH), 0); md = ImageDraw.Draw(m)
            lo = int(max(0, edge_in - ox)); hi = int(min(SW, edge_out - ox))
            if lo < SW: md.rectangle((lo, 0, SW, SH), fill=255)
            if back > 0 and hi > 0: md.rectangle((0, 0, hi, SH), fill=0)
            scr.paste(piece, (0, 0), m)
        p = power[i]
        if p < 1: scr = Image.blend(Image.new("RGB", (SW, SH), (3, 3, 4)), scr, p)
        S.paste(scr, (x0, y0))
    return S

def flare(t, wipe, back, j):
    """Anamorphic streak riding the wipe edge."""
    F = Image.new("RGB", (W, H), 0)
    for e, w in ((wipe, 1), (back, -1)):
        if 0.02 < e < 0.98:
            ux0 = inner(N - 1, j)[0]; ux1 = inner(0, j)[2]
            x = ux1 - (ux1 - ux0 + 60) * e if w == 1 else ux0 - 60 + (ux1 - ux0 + 60) * e
            yc = vw.UY0 + SH * 0.42
            L = Image.new("RGB", (W // 8, H // 8), 0); ld = ImageDraw.Draw(L)
            ld.ellipse(((x - 520) / 8, (yc - 4) / 8, (x + 520) / 8, (yc + 4) / 8), fill=(120, 200, 255))
            ld.ellipse(((x - 30) / 8, (yc - 30) / 8, (x + 30) / 8, (yc + 30) / 8), fill=(255, 240, 220))
            L = L.filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR)
            a = math.sin(math.pi * e)
            F = ImageChops.add(F, Image.eval(L, lambda v: int(v * a)))
    return F

# grain + vignette
_rng = np.random.default_rng(1)
GRAIN = [(_rng.normal(0, 7, (PIC_H, W, 1))).astype(np.float32) for _ in range(6)]
yy, xx = np.mgrid[0:PIC_H, 0:W].astype(np.float32)
VIG = (1 - 0.55 * np.clip(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - PIC_H / 2) / (PIC_H * 0.7)) ** 2, 0, 1))[..., None]

def grade(img, t):
    a = np.asarray(img, np.float32)
    lum = a.mean(axis=2, keepdims=True) / 255
    # teal shadows / warm highlights
    a = a + (1 - lum) * np.array([-6, 2, 10], np.float32) + lum * np.array([10, 4, -8], np.float32)
    a = (a - 128) * 1.06 + 124
    a = a * VIG + GRAIN[int(t * FPS) % 6]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

def caption(img, t):
    CAPS = [(0.9, 3.6, "كل شاشة… تحكي لحالها."), (4.0, 6.6, "إلا لما تصير… شاشة وحدة."),
            (7.4, 13.4, "إعلان واحد. حضور أكبر."), (13.9, 17.0, "وبعدها… كل شاشة ترجع لمنيوها.")]
    for a, b, s in CAPS:
        if a <= t < b:
            al = min(seg(t, a, a + 0.6), 1 - seg(t, b - 0.5, b))
            lay = Image.new("RGBA", (W, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            TR(d, (W // 2, 100), s, K(54, 500), (240, 232, 220, 255), "mm")
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * al)))
            img.paste(lay, (0, PIC_Y0 + PIC_H + 40), lay)

def top_bar(img, a=1.0):
    lay = Image.new("RGBA", (W, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((W // 2, 92), "PopupPush", font=PB(44), fill=(235, 235, 235, 255), anchor="mm")
    d.text((W // 2, 150), "V I D E O   W A L L", font=CZ(24, 600), fill=GOLD + (255,), anchor="mm")
    lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
    img.paste(lay, (0, 60), lay)

def world(t):
    wipe = seg(t, 6.6, 8.0); back = seg(t, 13.6, 15.0)
    j = seg(t, 4.0, 6.0) * (1 - seg(t, 15.0, 16.0))
    power = [seg(t, 0.6 + i * 0.35, 1.0 + i * 0.35) for i in range(N)]
    S = screens(t, wipe, back, j, power)
    img = ImageChops.add(BG, LAMPS)
    img = ImageChops.add(img, LAMP_GLOW)
    img = ImageChops.lighter(img, S) if False else img
    # screens on top (opaque where they are)
    mask = Image.new("L", (W, H), 0); md = ImageDraw.Draw(mask); b = vw.bz(j)
    for i in range(N):
        x0, y0, x1, y1 = inner(i, j); md.rectangle((x0 - b, y0 - vw.BZ, x1 + b, y1 + vw.BZ), fill=255)
    img.paste(S, (0, 0), mask)
    # light spill from screens onto wall + counter
    small = S.resize((W // 6, H // 6), Image.BILINEAR).filter(ImageFilter.GaussianBlur(9)).resize((W, H), Image.BILINEAR)
    img = ImageChops.add(img, Image.eval(small, lambda v: int(v * 0.75)))
    # reflection in glossy counter
    top = vw.UY0 + SH
    ref = S.crop((0, vw.UY0, W, top)).transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(6))
    rm = Image.linear_gradient("L").resize((W, SH)).transpose(Image.FLIP_TOP_BOTTOM).point(lambda v: int(v * 0.22))
    img.paste(ref, (0, COUNTER_Y + 8), rm)
    img = ImageChops.add(img, flare(t, wipe, back, j))
    # pin (crop) the picture area with a slow camera push
    z = 1.0 + 0.10 * ease(t / 13.5) if t < 13.5 else 1.10 - 0.10 * seg(t, 13.5, 17.0)
    cx, cy = W / 2, PIC_Y0 + 560
    cw, ch = W / z, PIC_H / z
    box = (cx - cw / 2, cy - ch * 0.47, cx + cw / 2, cy + ch * 0.53)
    pic = img.crop(tuple(int(round(v)) for v in box)).resize((W, PIC_H), Image.BICUBIC)
    return grade(pic, t)

def end_card(t):
    img = Image.new("RGB", (W, H), (4, 4, 5)); d = ImageDraw.Draw(img)
    a = seg(t, 0.3, 1.2)
    # wordmark with gold light sweep
    wm = Image.new("L", (W, 220), 0); wd = ImageDraw.Draw(wm)
    wd.text((W // 2, 110), "PopupPush", font=PB(150), fill=255, anchor="mm")
    base = Image.new("RGB", (W, 220), (236, 232, 226))
    sx = -300 + 1700 * seg(t, 0.8, 2.6)
    sw = Image.new("L", (W, 220), 0); sd = ImageDraw.Draw(sw); sd.polygon([(sx, 0), (sx + 140, 0), (sx + 40, 220), (sx - 100, 220)], fill=255)
    base.paste(GOLD, (0, 0), sw.filter(ImageFilter.GaussianBlur(20)))
    lay = Image.new("RGB", (W, 220), 0); lay.paste(base, (0, 0), wm)
    img.paste(Image.blend(Image.new("RGB", (W, 220), (4, 4, 5)), lay, a), (0, 640), wm)
    d.text((W // 2, 900), "V I D E O   W A L L", font=CZ(30, 600), fill=tuple(int(c * a) for c in GOLD), anchor="mm")
    b = seg(t, 1.6, 2.4)
    for k, (s, sz, wg, col) in enumerate([("شاشاتك… صارت فيديو وول.", 60, 600, (240, 234, 224)),
                                         ("حتى ٦ شاشات · بدون أي أجهزة إضافية", 38, 400, (200, 192, 180)),
                                         ("من داشبورد واحد، أو من تطبيق الريموت كنترول على جوالك", 32, 400, (196, 188, 176))]):
        col = tuple(int(c * b) for c in col)
        TR(d, (W // 2, 1060 + k * 86 + (12 if k else 0)), s, K(sz, wg), col, "mm")
    c = seg(t, 2.6, 3.3)
    gc = tuple(int(v * c) for v in GOLD)
    d.rounded_rectangle((W // 2 - 270, 1390, W // 2 + 270, 1500), 55, outline=gc, width=3)
    TR(d, (W // 2, 1445), "اطلب عرض تجريبي", K(44, 600), gc, "mm")
    TR(d, (W // 2, 1640), "راسلنا واتساب  ·  popuppush.com", K(32, 400), tuple(int(v * c * 0.8) for v in (230, 230, 230)), "mm")
    if t > 5.6: img = Image.blend(img, Image.new("RGB", (W, H), 0), seg(t, 5.6, 6.4))
    a2 = np.asarray(img, np.float32) + _rng.normal(0, 4, (H, W, 1)).astype(np.float32)
    return Image.fromarray(a2.clip(0, 255).astype(np.uint8))

def frame(t):
    if t >= 17.6: return end_card(t - 17.6)
    out = Image.new("RGB", (W, H), 0)
    pic = world(t)
    fade = seg(t, 0.0, 0.9) * (1 - seg(t, 17.0, 17.6))
    if fade < 1: pic = Image.blend(Image.new("RGB", pic.size, 0), pic, fade)
    out.paste(pic, (0, PIC_Y0))
    top_bar(out, seg(t, 0.4, 1.4) * (1 - seg(t, 17.0, 17.6)))
    caption(out, t)
    return out

def render(name, a, b):
    out = f"/root/vw/{name}.mp4"; tmp = f"/root/vw/{name}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    for n in range(round(a * FPS), round(b * FPS)): p.stdin.write(frame(n / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, out)

if __name__ == "__main__":
    if sys.argv[1] == "still":
        for s in sys.argv[2:]: frame(float(s)).save(f"/root/vw/cin_{s}.jpg", quality=90)
    else:
        import concurrent.futures as cf
        todo = [sc for sc in SCENES if sys.argv[1] in ("all", sc[0])]
        with cf.ProcessPoolExecutor(max_workers=min(5, os.cpu_count() or 2)) as ex:
            list(ex.map(render, *zip(*todo)))
