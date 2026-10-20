"""Real-footage reels from PopupPush installations (no venue name). 1080x1920, 30fps."""
import sys, subprocess, numpy as np
from PIL import Image, ImageDraw
from render import W, H, FPS, F, NAVY, CYAN, INDIGO, WHITE, MUTED, GOLD, INK, RED, ease, seg, text_c, text_w, caption, chip, logo
from sprite import paste_kafu

RAW = "/home/claude/popuppush-media/gg-arena/raw/"
OUT = "/home/claude/kafu3/reels/"
END = 4.0
_g = np.zeros((H, W, 4), np.uint8); _a = np.clip((np.arange(H) - 1050) / 500, 0, 1) * 120
_g[..., 3] = _a[:, None].astype(np.uint8)
GRAD = Image.fromarray(_g, "RGBA")

REELS = {
 "R1_Tour": dict(
    chip="من تركيباتنا بالرياض",
    clips=[("video_bar_menus", 7.0, 3.2), ("hd_04_bar_menus", 0.0, 3.0), ("hd_02_neon_vertical_screen", 3.4, 3.0), ("video_pool_zone", 8.0, 3.0)],
    caps=["شاشات حقيقية بمكان حقيقي", "المنيو فوق الكاشير", "وشاشة عمودية للحملات", "ومحتوى يتبدّل بكل زاوية"],
    end=("وكلها من جوال واحد.", "زيارة بدون التزام")),
 "R2_Counter": dict(
    chip="من تركيباتنا بالرياض",
    clips=[("hd_04_bar_menus", 0.0, 3.6), ("video_bar_menus", 11.0, 4.0), ("hd_04_bar_menus", 4.0, 3.5)],
    caps=["الزبون واقف عند الكاشير…", "وعينه على الشاشة", "المنيو والعروض تتبدّل حسب الوقت"],
    end=("شاشة الكاشير… خلّها تبيع.", "زيارة بدون التزام")),
 "R3_Vertical": dict(
    chip="من تركيباتنا بالرياض",
    clips=[("hd_02_neon_vertical_screen", 0.0, 3.0), ("hd_02_neon_vertical_screen", 3.2, 4.6), ("video_pool_zone", 8.0, 3.2)],
    caps=["عندك جدار فاضي؟", "شاشة عمودية… وحملتك عليها", "وتغيّر الحملة من جوالك"],
    end=("كل جدار ممكن يبيع.", "زيارة بدون التزام")),
}

def base_video(name, cfg):
    parts, inputs = [], []
    for k, (clip, ss, dur) in enumerate(cfg["clips"]):
        inputs += ["-ss", str(ss), "-t", str(dur), "-i", RAW + clip + ".mp4"]
        parts.append(f"[{k}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,unsharp=5:5:0.6,eq=saturation=1.08[v{k}]")
    n = len(cfg["clips"])
    fc = ";".join(parts) + ";" + "".join(f"[v{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=0[v]"
    out = f"/tmp/claude-0/-home-claude/60d84580-54d6-556c-83f8-7138ab1af8df/scratchpad/base_{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", out], check=True)
    return out, sum(c[2] for c in cfg["clips"])

def endcard(t, cfg):
    img = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(img)
    k = ease(seg(t, 0, 0.5))
    paste_kafu(img, W / 2, 640 - (1 - k) * 80, 560, "happy", 1 if (0.4 <= t <= 1.8 and int(t * 8) % 2 == 0) else 0, "wave1" if int(t * 3) % 2 else "wave2")
    d = ImageDraw.Draw(img)
    if t > 0.3: text_c(d, W / 2, 1000, cfg["end"][0], F["big"], WHITE)
    if t > 0.7: text_c(d, W / 2, 1130, cfg["end"][1], F["mid"], MUTED)
    if t > 1.1:
        s = "واتساب 0583272051"; bw = text_w(d, s, F["mid"]) + 120
        d.rounded_rectangle([(W - bw) / 2, 1240, (W + bw) / 2, 1360], 60, fill=CYAN)
        text_c(d, W / 2, 1258, s, F["mid"], INK)
        logo(d, W / 2, 1430)
    return img

def build(name):
    cfg = REELS[name]
    src, dur = base_video(name, cfg)
    total = dur + END
    bounds = np.cumsum([0] + [c[2] for c in cfg["clips"]])
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "slow", "-g", "60", "-profile:v", "high", "-level", "4.1",
                            "-movflags", "+faststart", OUT + f"silent_{name}.mp4"], stdin=subprocess.PIPE)
    nf = int(round(total * FPS)); fsz = W * H * 3; last = None
    for i in range(nf):
        t = i / FPS
        if t < dur:
            buf = dec.stdout.read(fsz)
            if len(buf) == fsz: last = Image.frombytes("RGB", (W, H), buf)
            img = Image.alpha_composite(last.convert("RGBA"), GRAD).convert("RGB"); d = ImageDraw.Draw(img)
            chip(d, cfg["chip"], W - 50, 230, RED, WHITE)
            k = int(np.searchsorted(bounds, t, side="right") - 1); k = min(k, len(cfg["caps"]) - 1)
            caption(d, cfg["caps"][k], seg(t, bounds[k], bounds[k] + 0.3), y=1330)
            fo = 1 - seg(t, dur - 0.3, dur)
            if fo < 1: img = Image.blend(Image.new("RGB", (W, H)), img, fo)
        else:
            img = endcard(t - dur, cfg)
            if t > total - 0.4: img = Image.blend(Image.new("RGB", (W, H)), img, (total - t) / 0.4)
        enc.stdin.write(img.tobytes())
    enc.stdin.close(); enc.wait(); dec.kill()
    print(name, round(total, 2), list(bounds))
    return total, list(bounds)

if __name__ == "__main__":
    import os, json
    os.makedirs(OUT, exist_ok=True)
    meta = {}
    for nm in (sys.argv[1:] or REELS):
        meta[nm] = build(nm)
    json.dump(meta, open(OUT + "meta.json", "w"))
