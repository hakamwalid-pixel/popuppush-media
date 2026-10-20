import sys, math, subprocess
from PIL import Image, ImageDraw
from render import font as _font
TINY = _font(28)
from render import (W, H, FPS, DUR, N, F, NAVY, WALL, FLOOR, CYAN, INDIGO, RED, WHITE, LIGHT, MUTED,
                    GREEN, BLUE, GOLD, INK, ease, seg, text_c, text_w, caption, kafu, chip, logo, endcard)

BROWN = (120, 72, 44); SKIN = (224, 172, 128); SHOP = (44, 44, 100); AWN = (23, 195, 214)
CAP_Y = 1330   # inside the Reels/TikTok safe zone
CHIP_Y = 230

def person(d, x, y, s=1.0, shirt=(240, 240, 240), step=0.0):
    leg = math.sin(step * 2 * math.pi) * 18 * s
    d.line([(x, y + 150 * s), (x - leg, y + 250 * s)], fill=(60, 60, 80), width=int(22 * s))
    d.line([(x, y + 150 * s), (x + leg, y + 250 * s)], fill=(60, 60, 80), width=int(22 * s))
    d.rounded_rectangle([x - 45 * s, y + 40 * s, x + 45 * s, y + 165 * s], int(30 * s), fill=shirt)
    d.ellipse([x - 32 * s, y - 25 * s, x + 32 * s, y + 39 * s], fill=SKIN)
    d.pieslice([x - 36 * s, y - 32 * s, x + 36 * s, y + 20 * s], 180, 360, fill=WHITE)

def bubble(d, cx, y, text, tail_x=None):
    tw = text_w(d, text, F["small"]) + 56
    d.rounded_rectangle([cx - tw / 2, y, cx + tw / 2, y + 74], 30, fill=WHITE)
    tx = cx if tail_x is None else tail_x
    d.polygon([(tx - 14, y + 70), (tx + 14, y + 70), (tx, y + 100)], fill=WHITE)
    text_c(d, cx, y + 10, text, F["small"], NAVY)

def phone_buttons(d, r, labels, sel_idx, t, tap_t=6.4):
    if not r or r[4] <= 0.9: return
    px0, py0, px1, py1, _ = r
    n = len(labels); gap = (py1 - py0 - 30) / n; bh = min(gap - 12, 90)
    fnt = F["small"] if (px1 - px0) > 120 else TINY
    top = py0 + 18 + ((py1 - py0 - 30) - n * gap) / 2
    for k, lab in enumerate(labels):
        by = top + k * gap
        on = (t >= tap_t + 0.2 and k == sel_idx)
        d.rounded_rectangle([px0 + 12, by, px1 - 12, by + bh], 14, fill=GOLD if on else (60, 60, 110))
        text_c(d, (px0 + px1) / 2, by + bh / 2 - (30 if fnt is not TINY else 22), lab, fnt, INK if on else WHITE)
    if tap_t <= t < tap_t + 0.6:
        rr = 24 + 30 * seg(t, tap_t, tap_t + 0.6)
        cx, cy = (px0 + px1) / 2, top + sel_idx * gap + bh / 2
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=WHITE, width=5)

def talkf(t, a, b): return 1 if (a <= t <= b and int(t * 8) % 2 == 0) else 0

def finish(img, t):
    a = 1 - seg(t, DUR - 0.5, DUR)
    if 12.3 <= t < 12.7: a = min(a, abs(t - 12.5) / 0.2)
    if a < 1: img = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), img, a)
    return img

# ---------------- Episode 4: كفو برّا المحل ----------------
def ep4(i):
    t = i / FPS
    img = Image.new("RGB", (W, H), (36, 40, 92)); d = ImageDraw.Draw(img)
    if t < 12.5:
        FL = 1100
        d.rectangle([0, FL, W, H], fill=(70, 70, 86))
        d.rectangle([0, FL - 10, W, FL + 10], fill=(150, 150, 170))
        d.rectangle([40, 400, 1040, FL], fill=SHOP)
        for k in range(9):
            d.rectangle([40 + k * 112, 340, 96 + k * 112, 420], fill=AWN if k % 2 == 0 else WHITE)
        text_c(d, 540, 440, "المقهى", F["mid"], WHITE)
        # door (centre) — kiosk stands on the right, Kafu on the left
        dx0, dx1, dy0 = 470, 650, 640
        d.rectangle([dx0, dy0, dx1, FL], fill=(22, 22, 58))
        d.ellipse([dx0 + 20, 860, dx0 + 40, 880], fill=GOLD)
        chip(d, "يوميات كفو · الحلقة ٤", W - 50, CHIP_Y, RED, WHITE)
        kx, ky, kw, kh = 650, 540, 360, 440
        d.rounded_rectangle([kx - 16, ky - 16, kx + kw + 16, ky + kh + 16], 26, fill=LIGHT)
        d.rectangle([kx + kw / 2 - 26, ky + kh + 16, kx + kw / 2 + 26, FL], fill=LIGHT)
        if t < 8.0:
            d.rectangle([kx, ky, kx + kw, ky + kh], fill=(14, 14, 30))
        else:
            morning = t < 10.0
            d.rectangle([kx, ky, kx + kw, ky + kh], fill=GOLD if morning else CYAN)
            text_c(d, kx + kw / 2, ky + 50, "عرض الصبح" if morning else "عرض المسا", F["mid"], INK)
            lines = ["قهوة + كرواسون", "بـ ١٥ ريال"] if morning else ["قهوتين", "بـ ٢٠ ريال"]
            for k2, ln in enumerate(lines):
                text_c(d, kx + kw / 2, ky + 180 + k2 * 100, ln, F["mid"], INK)
            for a0 in (8.0, 10.0):
                if a0 <= t < a0 + 0.35:
                    ov = Image.new("RGBA", (kw, kh), (255, 255, 255, int(255 * (1 - seg(t, a0, a0 + 0.35)))))
                    img.paste(Image.alpha_composite(img.crop((kx, ky, kx + kw, ky + kh)).convert("RGBA"), ov).convert("RGB"), (kx, ky))
                    d = ImageDraw.Draw(img)
        PY = FL - 250   # person's head y so feet touch the pavement
        # passer-by 1: walks past the dark screen, right -> left, never looks
        if t < 4.4:
            person(d, 1150 - seg(t, 0.2, 4.4) * 1450, PY, 1.0, (200, 200, 215), t * 1.6)
        # passer-by 2: walks in from the right, stops at the lit screen, goes in through the door
        if 9.4 <= t < 12.3:
            if t < 10.4:
                gx = 1160 - ease(seg(t, 9.4, 10.4)) * 600; step = t * 1.6
            else:
                gx = 560; step = 0
            sc = 1.0 - 0.35 * seg(t, 11.3, 12.2)
            person(d, gx, PY + (1 - sc) * 250, sc, (240, 200, 160), step)
            if 10.4 <= t < 11.3:
                bubble(d, 560, PY - 130, "أووه! عرض")
        # Kafu on the pavement, left
        if t < 4.5:
            mood, arm, ph, mouth = "worried", None, 0.0, talkf(t, 0.6, 3.9)
            caption(d, "الناس تمشي من قدام المحل…" if t < 2.4 else "وما تدري عن عرض اليوم!",
                    seg(t, -1 if t < 2.4 else 2.4, -0.5 if t < 2.4 else 2.7), y=CAP_Y)
        elif t < 8.0:
            mood, arm, ph, mouth = "happy", "phone", seg(t, 4.5, 5.1), talkf(t, 4.8, 6.6)
            caption(d, "شاشة الواجهة؟ من الجوال", seg(t, 4.6, 4.9), y=CAP_Y)
        else:
            mood, arm, ph, mouth = "happy", "phone", 1.0, talkf(t, 8.3, 12.2)
            caption(d, "عرض الصبح…" if t < 10.0 else "وعرض المسا… والزبون دخل!",
                    seg(t, 8.2 if t < 10 else 10.0, 8.5 if t < 10 else 10.3), y=CAP_Y)
        r = kafu(d, 300, 1000 + math.sin(t * 3) * 5, 1.0, mood, mouth, arm, ph)
        sel = 1 if t >= 9.8 else 0
        tap = 9.6 if t >= 9.6 else 6.4
        phone_buttons(d, r, ["الصبح", "المسا", "الماتش"], sel, t, tap)
    else:
        d = endcard(d, img, t, "٤")
    return finish(img, t)

# ---------------- Episode 5: الضيف اللي يرجع ----------------
def ep5(i):
    t = i / FPS
    img = Image.new("RGB", (W, H), WALL); d = ImageDraw.Draw(img)
    if t < 12.5:
        d.rectangle([0, 1250, W, H], fill=FLOOR)
        chip(d, "يوميات كفو · الحلقة ٥", W - 50, CHIP_Y, RED, WHITE)
        sx, sy, sw, sh = 140, 340, 800, 420
        # confetti falls around the screen, behind it, so it never covers the text
        if t >= 10.4:
            for c in range(60):
                cx = (c * 131) % W; cy = 300 + ((c * 71 + int((t - 10.4) * 520)) % 560)
                d.rectangle([cx, cy, cx + 14, cy + 22], fill=[CYAN, GOLD, RED, INDIGO, WHITE][c % 5])
        d.rounded_rectangle([sx - 16, sy - 16, sx + sw + 16, sy + sh + 16], 26, fill=LIGHT)
        d.rectangle([sx, sy, sx + sw, sy + sh], fill=(22, 22, 58))
        if t < 8.0:
            text_c(d, sx + sw / 2, sy + sh / 2 - 40, "أهلاً بضيوفنا", F["scr"], MUTED)
        else:
            visits = 2 if t < 9.0 else (3 if t < 9.8 else 4)
            pts = {2: 40, 3: 70, 4: 100}[visits]; prev = {2: 20, 3: 40, 4: 70}[visits]
            a0 = {2: 8.0, 3: 9.0, 4: 9.8}[visits]
            cur = prev + (pts - prev) * ease(seg(t, a0, a0 + 0.5))
            ar = lambda v: str(v).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))
            text_c(d, sx + sw / 2, sy + 34, f"أبو فهد · الزيارة {['','','٢','٣','٤'][visits]}", F["mid"], WHITE)
            text_c(d, sx + sw / 2, sy + 118, f"نقاطك {ar(int(round(cur)))} / ١٠٠", F["mid"], CYAN)
            bx0, bx1, by = sx + 80, sx + sw - 80, sy + 222
            d.rounded_rectangle([bx0, by, bx1, by + 44], 22, fill=(52, 52, 110))
            fillw = max(44, (bx1 - bx0) * cur / 100)
            d.rounded_rectangle([bx1 - fillw, by, bx1, by + 44], 22, fill=CYAN)
            if t >= 10.4:
                k = ease(seg(t, 10.4, 10.8))
                d.rounded_rectangle([sx + sw / 2 - 300 * k, sy + 296, sx + sw / 2 + 300 * k, sy + 392], 30, fill=GOLD)
                if k > 0.9: text_c(d, sx + sw / 2, sy + 306, "هديتك: قهوة مجانية", F["mid"], INK)
        # guest and table on the right; Kafu on the left so the phone never covers them
        d.rounded_rectangle([700, 1080, 1020, 1110], 10, fill=BROWN)
        d.rectangle([845, 1110, 875, 1250], fill=BROWN)
        GY = 1080 - 230
        if t < 2.6:
            person(d, 800, GY, 0.92, (200, 200, 215))
        elif t < 4.5:
            person(d, 800 + ease(seg(t, 2.6, 4.2)) * 420, GY, 0.92, (200, 200, 215), t * 1.6)
        elif t >= 8.0:
            person(d, 1220 - ease(seg(t, 8.0, 8.8)) * 420, GY, 0.92, (200, 200, 215), 0 if t > 8.8 else t * 1.6)
            if t > 10.6: bubble(d, 950, GY - 70, "يا سلام!", tail_x=860)
        if t < 4.5:
            mood, arm, ph, mouth = "worried", None, 0.0, talkf(t, 0.6, 4.0)
            caption(d, "ضيف جا مرة…" if t < 2.6 else "وما رجع؟", seg(t, -1 if t < 2.6 else 2.6, -0.5 if t < 2.6 else 2.9), y=CAP_Y)
        elif t < 8.0:
            mood, arm, ph, mouth = "happy", "phone", seg(t, 4.5, 5.1), talkf(t, 4.8, 6.8)
            caption(d, "خلّه يجمع نقاط من أول زيارة", seg(t, 4.6, 4.9), y=CAP_Y)
        else:
            mood, arm, ph, mouth = "happy", "phone", 1.0, talkf(t, 8.3, 12.2)
            caption(d, "كل زيارة نقاط…" if t < 10.4 else "والنقاط هدية!", seg(t, 8.2 if t < 10.4 else 10.4, 8.5 if t < 10.4 else 10.7), y=CAP_Y)
        r = kafu(d, 440, 1032 + math.sin(t * 3) * 6, 1.1, mood, mouth, arm, ph)
        phone_buttons(d, r, ["النقاط", "الهدايا"], 0, t, 6.4)
    else:
        d = endcard(d, img, t, "٥")
    return finish(img, t)

if __name__ == "__main__":
    ep = sys.argv[1]; fn = {"4": ep4, "5": ep5}[ep]
    if len(sys.argv) > 2:
        for ts in sys.argv[2:]:
            fn(int(float(ts) * FPS)).save(f"/home/claude/kafu3/e{ep}_{ts}.png")
    else:
        out = {"4": "Kafu_Ep4_BarraAlMahal.mp4", "5": "Kafu_Ep5_AlDaifYirja.mp4"}[ep]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "slow", "-g", "60", "-profile:v", "high", "-level", "4.1", "-movflags", "+faststart", "/home/claude/kafu3/silent_" + out], stdin=subprocess.PIPE)
        for i in range(N): p.stdin.write(fn(i).tobytes())
        p.stdin.close(); p.wait(); print("done", out, p.returncode)
