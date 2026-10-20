import sys, math, subprocess
from PIL import Image, ImageDraw
from render import (W, H, FPS, DUR, N, F, NAVY, WALL, FLOOR, CYAN, INDIGO, RED, WHITE, LIGHT, MUTED,
                    GREEN, GOLD, INK, ease, seg, text_c, text_w, caption, kafu, chip, endcard)
from eps import person, bubble, phone_buttons, talkf, finish, BROWN, CAP_Y, CHIP_Y

AR = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
PINK = (244, 114, 182)

def screen(d, sx, sy, sw, sh):
    d.rounded_rectangle([sx - 16, sy - 16, sx + sw + 16, sy + sh + 16], 26, fill=LIGHT)
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=(22, 22, 58))

def table_guest(d, gx, t, shirt, walk=None):
    d.rounded_rectangle([700, 1080, 1020, 1110], 10, fill=BROWN)
    d.rectangle([845, 1110, 875, 1250], fill=BROWN)
    person(d, gx, 1080 - 230, 0.92, shirt, walk or 0)

def cake(d, cx, y, s=1.0):
    d.rounded_rectangle([cx - 90 * s, y + 40 * s, cx + 90 * s, y + 120 * s], int(16 * s), fill=PINK)
    d.rounded_rectangle([cx - 70 * s, y, cx + 70 * s, y + 50 * s], int(14 * s), fill=WHITE)
    for k in (-40, 0, 40):
        d.rectangle([cx + k * s - 5 * s, y - 40 * s, cx + k * s + 5 * s, y], fill=GOLD)
        d.ellipse([cx + k * s - 9 * s, y - 62 * s, cx + k * s + 9 * s, y - 38 * s], fill=(255, 140, 0))

# ---------------- Episode 6: عيد ميلاد الضيف ----------------
def ep6(i):
    t = i / FPS
    img = Image.new("RGB", (W, H), WALL); d = ImageDraw.Draw(img)
    if t < 12.5:
        d.rectangle([0, 1250, W, H], fill=FLOOR)
        chip(d, "يوميات كفو · الحلقة ٦", W - 50, CHIP_Y, RED, WHITE)
        sx, sy, sw, sh = 140, 340, 800, 420
        party = t >= 8.0
        if party:
            for c in range(60):
                cx = (c * 131) % W; cy = 300 + ((c * 71 + int((t - 8.0) * 520)) % 560)
                d.rectangle([cx, cy, cx + 14, cy + 22], fill=[CYAN, GOLD, RED, INDIGO, PINK][c % 5])
        screen(d, sx, sy, sw, sh)
        if not party:
            text_c(d, sx + sw / 2, sy + sh / 2 - 40, "أهلاً بضيوفنا", F["scr"], MUTED)
        else:
            k = ease(seg(t, 8.0, 8.5))
            d.rectangle([sx, sy, sx + sw, sy + sh], fill=(70, 30, 110))
            cake(d, sx + sw / 2, sy + 90 - (1 - k) * 60, 0.9)
            if k > 0.5:
                text_c(d, sx + sw / 2, sy + 230, "كل عام وأنتِ بخير", F["mid"], WHITE)
                text_c(d, sx + sw / 2, sy + 310, "يا نورة!", F["mid"], GOLD)
            if 8.0 <= t < 8.35:
                ov = Image.new("RGBA", (sw, sh), (255, 255, 255, int(255 * (1 - seg(t, 8.0, 8.35)))))
                img.paste(Image.alpha_composite(img.crop((sx, sy, sx + sw, sy + sh)).convert("RGBA"), ov).convert("RGB"), (sx, sy))
                d = ImageDraw.Draw(img)
        table_guest(d, 860, t, PINK)
        if t > 10.6: bubble(d, 900, 850 - 70, "يا سلام!", tail_x=860)
        if t < 4.5:
            mood, arm, ph, mouth = "worried", None, 0.0, talkf(t, 0.6, 4.0)
            caption(d, "ضيفة عندها عيد ميلاد…" if t < 2.6 else "والشاشات عادية؟", seg(t, -1 if t < 2.6 else 2.6, -0.5 if t < 2.6 else 2.9), y=CAP_Y)
        elif t < 8.0:
            mood, arm, ph, mouth = "happy", "phone", seg(t, 4.5, 5.1), talkf(t, 4.8, 6.8)
            caption(d, "وضع عيد الميلاد؟ من الجوال", seg(t, 4.6, 4.9), y=CAP_Y)
        else:
            mood, arm, ph, mouth = "happy", "phone", 1.0, talkf(t, 8.3, 12.2)
            caption(d, "كل الشاشات تحتفل فيها…" if t < 10.4 else "وهالليلة ما تنتسى!", seg(t, 8.2 if t < 10.4 else 10.4, 8.5 if t < 10.4 else 10.7), y=CAP_Y)
        r = kafu(d, 440, 1032 + math.sin(t * 3) * 6, 1.1, mood, mouth, arm, ph)
        phone_buttons(d, r, ["عيد ميلاد", "العروض"], 0, t, 6.4)
    else:
        d = endcard(d, img, t, "٦")
    return finish(img, t)

# ---------------- Episode 7: العرض يخلص ----------------
def ep7(i):
    t = i / FPS
    img = Image.new("RGB", (W, H), WALL); d = ImageDraw.Draw(img)
    if t < 12.5:
        d.rectangle([0, 1250, W, H], fill=FLOOR)
        chip(d, "يوميات كفو · الحلقة ٧", W - 50, CHIP_Y, RED, WHITE)
        sx, sy, sw, sh = 140, 340, 800, 420
        screen(d, sx, sy, sw, sh)
        timer = t >= 8.0
        d.rectangle([sx, sy, sx + sw, sy + sh], fill=GOLD if timer else (40, 40, 90))
        col = INK if timer else MUTED
        text_c(d, sx + sw / 2, sy + 40, "عرض الماتش", F["mid"], col)
        text_c(d, sx + sw / 2, sy + 125, "قهوتين بـ ٢٠ ريال", F["mid"], col)
        if timer:
            left = 30 * 60 - int((t - 8.0) * 1)  # real-time ticking
            mm, ss = divmod(left, 60)
            k = ease(seg(t, 8.0, 8.4))
            bw = 420 * k
            d.rounded_rectangle([sx + sw / 2 - bw / 2, sy + 240, sx + sw / 2 + bw / 2, sy + 360], 30, fill=INK)
            if k > 0.9:
                text_c(d, sx + sw / 2, sy + 252, f"باقي {mm:02d}:{ss:02d}".translate(AR), F["mid"], GOLD)
            if 8.0 <= t < 8.35:
                ov = Image.new("RGBA", (sw, sh), (255, 255, 255, int(255 * (1 - seg(t, 8.0, 8.35)))))
                img.paste(Image.alpha_composite(img.crop((sx, sy, sx + sw, sy + sh)).convert("RGBA"), ov).convert("RGB"), (sx, sy))
                d = ImageDraw.Draw(img)
        # guest: sits and ignores, then gets up and heads to the counter (right)
        d.rounded_rectangle([700, 1080, 1020, 1110], 10, fill=BROWN)
        d.rectangle([845, 1110, 875, 1250], fill=BROWN)
        GY = 1080 - 230
        if t < 9.6:
            person(d, 860, GY, 0.92, (200, 200, 215))
            if 9.0 <= t < 9.6: bubble(d, 900, GY - 70, "أوه! باقي وقت", tail_x=860)
        else:
            gx = 860 + ease(seg(t, 9.6, 11.0)) * 300
            person(d, gx, GY, 0.92, (200, 200, 215), t * 1.6 if t < 11.0 else 0)
            if t > 10.4: bubble(d, min(gx, 880), GY - 70, "ألحق قبل يخلص!", tail_x=min(gx, 960))
        if t < 4.5:
            mood, arm, ph, mouth = "worried", None, 0.0, talkf(t, 0.6, 4.0)
            caption(d, "العرض على الشاشة…" if t < 2.6 else "والزبون ما تحرّك!", seg(t, -1 if t < 2.6 else 2.6, -0.5 if t < 2.6 else 2.9), y=CAP_Y)
        elif t < 8.0:
            mood, arm, ph, mouth = "happy", "phone", seg(t, 4.5, 5.1), talkf(t, 4.8, 6.8)
            caption(d, "حط له عدّاد… من الجوال", seg(t, 4.6, 4.9), y=CAP_Y)
        else:
            mood, arm, ph, mouth = "happy", "phone", 1.0, talkf(t, 8.3, 12.2)
            caption(d, "العدّاد يمشي…" if t < 10.4 else "والزبون يطلب قبل ما يخلص!", seg(t, 8.2 if t < 10.4 else 10.4, 8.5 if t < 10.4 else 10.7), y=CAP_Y)
        r = kafu(d, 440, 1032 + math.sin(t * 3) * 6, 1.1, mood, mouth, arm, ph)
        phone_buttons(d, r, ["عدّاد ٣٠ د", "إيقاف"], 0, t, 6.4)
    else:
        d = endcard(d, img, t, "٧")
    return finish(img, t)

if __name__ == "__main__":
    ep = sys.argv[1]; fn = {"6": ep6, "7": ep7}[ep]
    if len(sys.argv) > 2:
        for ts in sys.argv[2:]:
            fn(int(float(ts) * FPS)).save(f"/home/claude/kafu3/e{ep}_{ts}.png")
    else:
        out = {"6": "Kafu_Ep6_EidMilad.mp4", "7": "Kafu_Ep7_AlArdYikhlas.mp4"}[ep]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "slow", "-g", "60", "-profile:v", "high", "-level", "4.1", "-movflags", "+faststart", "/home/claude/kafu3/silent_" + out], stdin=subprocess.PIPE)
        for i in range(N): p.stdin.write(fn(i).tobytes())
        p.stdin.close(); p.wait(); print("done", out, p.returncode)
