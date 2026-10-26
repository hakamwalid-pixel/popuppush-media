import math, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 16.0
N = int(FPS * DUR)
FD = "/home/claude/kafu3/fonts/"
def font(sz, w="Bold"):
    return ImageFont.truetype(FD + f"IBMPlexSansArabic-{w}.ttf", sz, layout_engine=ImageFont.Layout.RAQM)
F = {k: font(v) for k, v in {"cap": 64, "big": 88, "mid": 52, "chip": 40, "scr": 58, "small": 36, "logo": 50}.items()}
F["offer"] = font(40, "SemiBold")

NAVY = (20, 20, 60); NAVY2 = (34, 34, 90); WALL = (28, 28, 74); FLOOR = (16, 16, 44)
CYAN = (23, 195, 214); INDIGO = (99, 102, 241); RED = (215, 38, 61); WHITE = (255, 255, 255)
LIGHT = (232, 234, 246); MUTED = (197, 200, 234); GREEN = (31, 122, 77); BLUE = (43, 108, 176)
GOLD = (245, 183, 0); INK = (11, 11, 38)

def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3
def seg(t, a, b): return max(0.0, min(1.0, (t - a) / (b - a)))

def text_c(d, cx, y, s, f, fill):
    bb = d.textbbox((0, 0), s, font=f, direction="rtl", language="ar")
    d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], y), s, font=f, fill=fill, direction="rtl", language="ar")
def text_w(d, s, f):
    bb = d.textbbox((0, 0), s, font=f, direction="rtl", language="ar"); return bb[2] - bb[0]

def caption(d, s, alpha=1.0, y=1330):
    if not s or alpha <= 0: return
    tw = text_w(d, s, F["cap"]); pw = tw + 90; x0 = (W - pw) / 2
    off = (1 - ease(alpha)) * 40
    d.rounded_rectangle([x0, y + off, x0 + pw, y + 120 + off], 30, fill=WHITE)
    text_c(d, W / 2, y + 14 + off, s, F["cap"], NAVY)

def kafu(d, cx, cy, s=1.0, mood="happy", mouth=0, arm=None, phone=0.0, wave=0.0):
    # body box 360x260 centered at (cx, cy)
    bw, bh = 360 * s, 260 * s
    x0, y0 = cx - bw / 2, cy - bh / 2
    # shemagh
    d.polygon([(x0 + 10 * s, y0 + 20 * s), (cx, y0 - 150 * s), (x0 + bw - 10 * s, y0 + 20 * s)], fill=RED)
    d.polygon([(x0 + 10 * s, y0 + 20 * s), (x0 - 36 * s, y0 + 170 * s), (x0 + 30 * s, y0 + 140 * s)], fill=RED)
    d.polygon([(x0 + bw - 10 * s, y0 + 20 * s), (x0 + bw + 36 * s, y0 + 170 * s), (x0 + bw - 30 * s, y0 + 140 * s)], fill=RED)
    d.ellipse([cx - 115 * s, y0 - 78 * s, cx + 115 * s, y0 - 30 * s], outline=(17, 17, 17), width=int(18 * s))
    # arms
    if arm == "phone":
        d.line([(x0 + bw, cy + 20 * s), (x0 + bw + 70 * s, cy - 10 * s)], fill=LIGHT, width=int(16 * s))
    if wave > 0:
        ang = math.sin(wave * math.pi * 4) * 0.5
        ex, ey = x0 + bw + 40 * s, cy - 10 * s
        hx, hy = ex + 90 * s * math.cos(-1.1 + ang), ey + 90 * s * math.sin(-1.1 + ang)
        d.line([(x0 + bw - 6 * s, cy + 20 * s), (ex, ey)], fill=LIGHT, width=int(16 * s))
        d.line([(ex, ey), (hx, hy)], fill=LIGHT, width=int(16 * s))
        d.ellipse([hx - 20 * s, hy - 20 * s, hx + 20 * s, hy + 20 * s], fill=LIGHT)
    d.line([(x0, cy + 20 * s), (x0 - 50 * s, cy + 90 * s)], fill=LIGHT, width=int(16 * s))
    # tv
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], int(46 * s), fill=INK, outline=LIGHT, width=int(15 * s))
    ex1, ex2, ey = cx - 60 * s, cx + 60 * s, y0 + 105 * s
    r = 28 * s
    d.ellipse([ex1 - r, ey - r, ex1 + r, ey + r], fill=CYAN)
    d.ellipse([ex2 - r, ey - r, ex2 + r, ey + r], fill=INDIGO)
    if mood == "worried":
        d.line([(ex1 - 34 * s, ey - 46 * s), (ex1 + 22 * s, ey - 62 * s)], fill=WHITE, width=int(9 * s))
        d.line([(ex2 + 34 * s, ey - 46 * s), (ex2 - 22 * s, ey - 62 * s)], fill=WHITE, width=int(9 * s))
    my = y0 + 185 * s
    if mouth:
        d.ellipse([cx - 34 * s, my - 22 * s, cx + 34 * s, my + 26 * s], fill=WHITE)
        d.ellipse([cx - 20 * s, my - 4 * s, cx + 20 * s, my + 20 * s], fill=RED)
    elif mood == "worried":
        d.arc([cx - 50 * s, my - 10 * s, cx + 50 * s, my + 50 * s], 200, 340, fill=WHITE, width=int(12 * s))
    else:
        d.arc([cx - 60 * s, my - 50 * s, cx + 60 * s, my + 20 * s], 20, 160, fill=WHITE, width=int(13 * s))
    # stand
    d.rectangle([cx - 30 * s, y0 + bh, cx + 30 * s, y0 + bh + 34 * s], fill=LIGHT)
    d.rounded_rectangle([cx - 95 * s, y0 + bh + 28 * s, cx + 95 * s, y0 + bh + 48 * s], int(10 * s), fill=LIGHT)
    # phone
    if phone > 0:
        k = ease(phone)
        pw, ph = 130 * s * k, 230 * s * k
        px, py = x0 + bw + 70 * s, cy - 10 * s
        d.rounded_rectangle([px - pw / 2, py - ph, px + pw / 2, py], int(20 * s * k + 1), fill=INK, outline=LIGHT, width=max(1, int(8 * s * k)))
        return (px - pw / 2, py - ph, px + pw / 2, py, k)
    return None

def tv(d, x, y, w, h, kind, offer=0.0, flash=0.0):
    d.rounded_rectangle([x - 14, y - 14, x + w + 14, y + h + 14], 22, fill=LIGHT)
    col, label = {"bein": (GREEN, "قناة ١"), "league": (BLUE, "قناة ٢")}[kind]
    d.rectangle([x, y, x + w, y + h], fill=col)
    d.ellipse([x + w / 2 - 50, y + h / 2 - 50, x + w / 2 + 50, y + h / 2 + 50], outline=(168, 230, 196), width=5)
    d.line([(x + w / 2, y), (x + w / 2, y + h)], fill=(168, 230, 196), width=4)
    d.rounded_rectangle([x + w - 170, y + 16, x + w - 16, y + 76], 10, fill=INK)
    text_c(d, x + w - 93, y + 16, label, F["small"], WHITE)
    if offer > 0:
        bh = 86 * ease(offer)
        d.rectangle([x, y + h - bh, x + w, y + h], fill=GOLD)
        if offer > 0.6:
            text_c(d, x + w / 2, y + h - 78, "٢ مشروب بسعر ١", F["offer"], INK)
    if flash > 0:
        a = int(255 * (1 - flash))
        ov = Image.new("RGBA", (int(w), int(h)), (255, 255, 255, a))
        return ov
    return None

def chip(d, s, x_right, y, bg, fg):
    tw = text_w(d, s, F["chip"]); pw = tw + 60
    d.rounded_rectangle([x_right - pw, y, x_right, y + 76], 38, fill=bg)
    text_c(d, x_right - pw / 2, y + 10, s, F["chip"], fg)

def logo(d, cx, y):
    lw = d.textlength("PopupPush", font=F["logo"])
    total = 28 + 12 + 28 + 18 + lw; x = cx - total / 2
    d.ellipse([x, y + 22, x + 28, y + 50], fill=CYAN); x += 40
    d.ellipse([x, y + 22, x + 28, y + 50], fill=INDIGO); x += 46
    d.text((x, y), "PopupPush", font=F["logo"], fill=WHITE)

def frame(i):
    t = i / FPS
    img = Image.new("RGB", (W, H), WALL)
    d = ImageDraw.Draw(img)
    talk = lambda a, b: 1 if (a <= t <= b and int(t * 8) % 2 == 0) else 0
    if t < 12.5:
        d.rectangle([0, 1250, W, H], fill=FLOOR)
        chip(d, "يوميات كفو · الحلقة ٣", W - 50, 230, RED, WHITE)
        # screens (right = first in RTL)
        right_kind = "league" if t >= 8.0 else "bein"
        offer = seg(t, 10.3, 10.9)
        tv(d, 590, 360, 420, 250, right_kind, offer)
        tv(d, 70, 360, 420, 250, "bein", offer)
        if 8.0 <= t < 8.4:
            ov = Image.new("RGBA", (420, 250), (255, 255, 255, int(255 * (1 - seg(t, 8.0, 8.4)))))
            img.paste(Image.alpha_composite(img.crop((590, 360, 1010, 610)).convert("RGBA"), ov).convert("RGB"), (590, 360))
            d = ImageDraw.Draw(img)
        if t < 4.5:
            mood, arm, ph = "worried", None, 0.0
            mouth = talk(0.6, 3.8)
            # thought bubble
            if t > 1.0:
                k = ease(seg(t, 1.0, 1.4))
                d.rounded_rectangle([700 - 200 * k, 600, 700 + 200 * k, 600 + 110 * k], 40, fill=WHITE)
                if k > 0.9:
                    d.polygon([(620, 706), (660, 706), (610, 750)], fill=WHITE)
                    text_c(d, 700, 610, "والقناة الثانية؟!", F["mid"], NAVY)
            caption(d, "ماتشين بنفس الوقت؟!" if t < 2.4 else "والشاشات كلها على قناة وحدة…", seg(t, -1 if t < 2.4 else 2.4, (-0.5 if t < 2.4 else 2.7)))
        elif t < 8.0:
            mood, arm, ph = "happy", "phone", seg(t, 4.5, 5.1)
            mouth = talk(4.8, 6.6)
            caption(d, "ولا يهمك… كله من الجوال", seg(t, 4.6, 4.9))
        else:
            mood, arm, ph = "happy", "phone", 1.0
            mouth = talk(8.4, 12.2)
            if t < 10.3:
                caption(d, "هذي قناة ١… وهذي قناة ٢", seg(t, 8.3, 8.6))
            else:
                caption(d, "والعرض نزل على كل الشاشات", seg(t, 10.4, 10.7))
        bob = math.sin(t * 3) * 6
        r = kafu(d, 560, 1032 + bob, 1.25, mood, mouth, arm, ph)
        if r and r[4] > 0.9:
            px0, py0, px1, py1, _ = r
            sel = 1 if t >= 6.6 else 0
            for k2, (lab, col) in enumerate([("قناة ١", GREEN), ("قناة ٢", BLUE)]):
                by = py0 + 40 + k2 * 80
                fill = col if (k2 == 1 and sel) or k2 == 0 else (60, 60, 110)
                d.rounded_rectangle([px0 + 14, by, px1 - 14, by + 62], 12, fill=fill)
                text_c(d, (px0 + px1) / 2, by + 10, lab, F["small"], WHITE)
            if 6.4 <= t < 7.0:
                rr = 26 + 30 * seg(t, 6.4, 7.0)
                cx2, cy2 = (px0 + px1) / 2, py0 + 151
                d.ellipse([cx2 - rr, cy2 - rr, cx2 + rr, cy2 + rr], outline=WHITE, width=5)
    else:
        d = endcard(d, img, t, "٣")
    # fades
    a = 1 - seg(t, DUR - 0.5, DUR)
    if 12.3 <= t < 12.7:
        a = min(a, abs(t - 12.5) / 0.2)
    if a < 1:
        img = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), img, a)
    return img


# ---- Kafu from the original character design (overrides the simple drawing above) ----
from sprite import paste_kafu
def kafu(d, cx, cy, s=1.0, mood="happy", mouth=0, arm=None, phone=0.0, wave=0.0):
    img = d._image
    width = 360 * s * 1.6
    sc = width / 360.0
    if wave > 0:
        arms = "wave1" if int(wave * 14) % 2 == 0 else "wave2"
    elif arm == "phone":
        arms = "phone"
    elif mood == "worried":
        arms = "worried"
    else:
        arms = "idle"
    x0, y0, sc = paste_kafu(img, cx, cy + (200 - 194) * sc, width, mood, mouth, arms)
    if arm == "phone" and phone > 0:
        k = ease(phone)
        hx, hy = x0 + 73 * sc, y0 + 290 * sc
        pw, ph = 200 * s * k, 330 * s * k
        px1 = hx - 24 * s; px0 = px1 - pw
        if px0 < 20: px0, px1 = 20, 20 + pw
        py1 = hy + 40 * s; py0 = py1 - ph
        if k > 0.3:
            d.line([(hx - 10, hy - 20), (px1, (py0 + py1) / 2)], fill=(129, 140, 248), width=4)
        d.rounded_rectangle([px0, py0, px1, py1], int(26 * s * k + 1), fill=(10, 14, 26), outline=(224, 231, 255), width=max(1, int(7 * s * k)))
        return (px0, py0, px1, py1, k)
    return None


def endcard(d, img, t, ep):
    img.paste(NAVY, [0, 0, W, H]); d = ImageDraw.Draw(img)
    talk = 1 if (12.9 <= t <= 14.4 and int(t * 8) % 2 == 0) else 0
    k = ease(seg(t, 12.5, 13.0))
    kafu(d, W / 2, 640 - (1 - k) * 80, 1.25, "happy", talk, None, 0.0, wave=seg(t, 12.6, 15.0))
    if t > 12.8: text_c(d, W / 2, 1010, "أبشر، خلّها على كفو!", F["big"], WHITE)
    if t > 13.2: text_c(d, W / 2, 1140, f"يوميات كفو · الحلقة {ep}", F["mid"], MUTED)
    if t > 13.6:
        bw = text_w(d, "راسلنا واتساب", F["mid"]) + 120
        d.rounded_rectangle([(W - bw) / 2, 1250, (W + bw) / 2, 1370], 60, fill=CYAN)
        text_c(d, W / 2, 1268, "راسلنا واتساب", F["mid"], INK)
        logo(d, W / 2, 1430)
    return d

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for ts in sys.argv[1:]:
            frame(int(float(ts) * FPS)).save(f"/home/claude/kafu3/f_{ts}.png")
    else:
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "slow", "-g", "60", "-profile:v", "high", "-level", "4.1", "-movflags", "+faststart", "/home/claude/kafu3/silent_Kafu_Ep3_Matchain.mp4"], stdin=subprocess.PIPE)
        for i in range(N):
            p.stdin.write(frame(i).tobytes())
        p.stdin.close(); p.wait(); print("done", p.returncode)
