"""PopupPush NEW-identity reels (D-20261116-4): hook -> real footage -> feature panel -> official end card.
Dark #0D1016 + honey #F2A93B, Readex Pro / IBM Plex Sans Arabic, site logo.
usage: python3 make_newid_reel.py specs.json OUTDIR   (fonts in $FD, repo root in $REPO)
"""
import os, sys, json, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FD = os.environ.get("FD", ".") + "/"
REPO = os.environ.get("REPO", ".")
FPS = 30
BG = (13, 16, 22); L1 = (21, 26, 35); L2 = (30, 37, 49); LN = (42, 50, 64); TX = (238, 241, 246); MU = (154, 164, 181)
HO = (242, 169, 59); MINT = (79, 209, 165); VIO = (156, 140, 255); ROSE = (255, 122, 138); BRN = (58, 50, 41); CY = (34, 211, 238)
ACC = {"honey": HO, "mint": MINT, "violet": VIO, "rose": ROSE}

def rx(s, w=700):
    f = ImageFont.truetype(FD + "ReadexPro.ttf", s, layout_engine=ImageFont.Layout.RAQM); f.set_variation_by_axes([w, 0]); return f
def px(s, w="SemiBold"): return ImageFont.truetype(FD + f"IBMPlexSansArabic-{w}.ttf", s, layout_engine=ImageFont.Layout.RAQM)
def T(d, xy, s, f, fill, anchor="ra"): d.text(xy, s, font=f, fill=fill, anchor=anchor, direction="rtl", language="ar")
def tw(d, s, f): b = d.textbbox((0, 0), s, font=f, direction="rtl", language="ar"); return b[2] - b[0]
def wrap(d, s, f, maxw):
    out, cur = [], ""
    for w in s.split():
        n = (cur + " " + w).strip()
        if tw(d, n, f) <= maxw or not cur: cur = n
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out

def mark(d, x, y, s):
    d.rounded_rectangle([x, y + s*0.08, x + s, y + s*0.86], int(s*0.2), fill=BRN)
    d.rounded_rectangle([x + s*0.38, y + s*0.86, x + s*0.62, y + s*0.92], int(s*0.02), fill=BRN)
    sw = s*0.09; x0 = x + s*0.33; t = y + s*0.24
    d.rounded_rectangle([x0, t, x0 + sw, y + s*0.72], int(sw/2), fill=CY)
    d.rounded_rectangle([x0, t, x0 + s*0.34, t + s*0.28], int(s*0.14), outline=CY, width=int(sw))
    r = s*0.085; d.ellipse([x + s*0.80 - r, y + s*0.22 - r, x + s*0.80 + r, y + s*0.22 + r], fill=HO)
def lockup(d, x, y, s):
    mark(d, x, y, s); f = rx(int(s*0.62)); xx = x + s*1.22
    d.text((xx, y + s*0.47), "Popup", font=f, fill=TX, anchor="lm"); d.text((xx + d.textlength("Popup", font=f), y + s*0.47), "Push", font=f, fill=HO, anchor="lm")

def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

class Reel:
    def __init__(self, spec):
        self.s = spec; self.W = 1080; self.H = spec.get("h", 1920); self.A = ACC[spec.get("color", "honey")]
        self.top = 120 if self.H == 1920 else 70

    def header(self, d):
        lockup(d, 70, self.top, 74)
        chip = self.s["chip"]; fc = rx(34, 600); cw = tw(d, chip, fc) + 60; R = self.W - 70
        d.rounded_rectangle([R - cw, self.top + 6, R, self.top + 70], 32, fill=L2, outline=self.A, width=3)
        T(d, (R - cw/2, self.top + 38), chip, fc, self.A, "mm")

    def footer(self, d):
        y = self.H - 150 if self.H == 1920 else self.H - 110
        d.line([70, y, self.W - 70, y], fill=LN, width=2)
        T(d, (self.W - 70, y + 50), "مكانك كله، من تطبيق واحد.", rx(34, 600), TX, "rm")
        d.text((70, y + 50), "popuppush.com", font=px(32), fill=MU, anchor="lm")

    def hook(self, t):  # t seconds into slide
        img = Image.new("RGB", (self.W, self.H), BG); d = ImageDraw.Draw(img)
        # soft glow
        g = Image.new("RGB", (self.W, self.H), BG); gd = ImageDraw.Draw(g)
        gd.ellipse([-300, self.H*0.35, self.W + 300, self.H*0.35 + 900], fill=tuple(int(c*0.22 + b*0.78) for c, b in zip(self.A, BG)))
        img = Image.blend(img, g.filter(ImageFilter.GaussianBlur(160)), 1.0); d = ImageDraw.Draw(img)
        self.header(d)
        lines = self.s["hook"]; R = self.W - 70; maxw = self.W - 140; ts = self.s.get("hsize", 118)
        while ts > 70 and max(tw(d, l, rx(ts)) for l in lines) > maxw: ts -= 4
        ft = rx(ts); lh = int(ts * 1.32); y0 = self.H*0.40 - lh*len(lines)/2
        for k, ln in enumerate(lines):
            p = ease((t - 0.15 - k*0.35) / 0.5);
            if p <= 0: continue
            lay = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
            T(ld, (R, y0 + k*lh + (1-p)*60), ln, ft, (self.A if k == len(lines)-1 else TX) + (int(255*p),))
            img.paste(lay, (0, 0), lay)
        d = ImageDraw.Draw(img)
        if self.s.get("sub"):
            p = ease((t - 1.0) / 0.5)
            if p > 0:
                fb = px(46); yy = y0 + len(lines)*lh + 40
                for ln in wrap(d, self.s["sub"], fb, maxw):
                    lay = Image.new("RGBA", (self.W, self.H), (0,0,0,0)); ld = ImageDraw.Draw(lay)
                    T(ld, (R, yy), ln, fb, MU + (int(255*p),)); img.paste(lay, (0,0), lay); yy += 70
        d = ImageDraw.Draw(img); self.footer(d)
        return img

    def footage_frame(self, fr, t, dur):
        # fr: PIL frame already scaled to cover W x H
        img = fr.copy(); d = ImageDraw.Draw(img, "RGBA")
        d.rectangle([0, 0, self.W, 260 if self.H == 1920 else 190], fill=(13, 16, 22, 170))
        self.header(d)
        cap = self.s["cap"]; p = ease((t - 0.3) / 0.5)
        fc = rx(self.s.get("capsize", 62)); R = self.W - 70; maxw = self.W - 200
        lines = []
        for c in cap: lines += wrap(d, c, fc, maxw)
        lh = int(fc.size * 1.35); boxh = lh*len(lines) + 70
        yb = self.H - (300 if self.H == 1920 else 220) - boxh + (1-p)*80
        lay = Image.new("RGBA", (self.W, self.H), (0,0,0,0)); ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle([60, yb, self.W - 60, yb + boxh], 36, fill=(13, 16, 22, int(225*p)), outline=self.A + (int(255*p),), width=3)
        yy = yb + 35
        for k, ln in enumerate(lines):
            T(ld, (R - 30, yy), ln, fc, (self.A if k == len(lines)-1 and len(lines) > 1 else TX) + (int(255*p),)); yy += lh
        img.paste(lay, (0,0), lay)
        return img.convert("RGB")

    def panel(self, t):
        img = Image.new("RGB", (self.W, self.H), BG); d = ImageDraw.Draw(img); self.header(d)
        R = self.W - 70; maxw = self.W - 140
        ft = rx(self.s.get("psize", 78)); y = (470 if self.H == 1920 else 230)
        for k, ln in enumerate(self.s["ptitle"]):
            T(d, (R, y), ln, ft, self.A if k == len(self.s["ptitle"]) - 1 else TX); y += int(ft.size * 1.3)
        y += 30
        items = self.s["items"]; rowh = 118 if self.H == 1920 else 96
        cardh = rowh*len(items) + 150
        d.rounded_rectangle([70, y, self.W - 70, y + cardh], 36, fill=L1, outline=LN, width=2)
        fi = px(50 if self.H == 1920 else 44); yy = y + 50
        for k, it in enumerate(items):
            p = ease((t - 0.3 - k*0.35) / 0.4)
            lay = Image.new("RGBA", (self.W, self.H), (0,0,0,0)); ld = ImageDraw.Draw(lay)
            if p > 0:
                ld.ellipse([R - 70, yy + 18, R - 34, yy + 54], fill=self.A + (int(255*p),))
                T(ld, (R - 100 + (1-p)*-40, yy + 36), it, fi, TX + (int(255*p),), "rm")
                if k < len(items) - 1: ld.line([130, yy + rowh - 22, R - 30, yy + rowh - 22], fill=LN + (int(255*p),), width=2)
            img.paste(lay, (0,0), lay); yy += rowh
        d = ImageDraw.Draw(img)
        # control row
        cy = y + cardh - 70
        d.rounded_rectangle([130, cy - 30, 230, cy + 30], 30, fill=self.A); d.ellipse([178, cy - 25, 228, cy + 25], fill=BG)
        T(d, (R - 30, cy), "من لوحة تحكم واحدة أو من جوالك", px(40), MU, "rm")
        yn = y + cardh + 50
        p = ease((t - 1.6) / 0.5)
        if p > 0:
            fcta = rx(54); cta = "احجز ديمو مجاني"; bw = tw(d, cta, fcta) + 120
            lay = Image.new("RGBA", (self.W, self.H), (0,0,0,0)); ld = ImageDraw.Draw(lay)
            ld.rounded_rectangle([R - bw, yn, R, yn + 110], 55, fill=HO + (int(255*p),)); T(ld, (R - bw/2, yn + 55), cta, fcta, BG + (int(255*p),), "mm")
            img.paste(lay, (0,0), lay)
        d = ImageDraw.Draw(img)
        if self.s.get("note"):
            fn = px(34, "Medium"); yy = yn + 150
            for ln in wrap(d, self.s["note"], fn, maxw): T(d, (R, yy), ln, fn, MU); yy += 50
        self.footer(d)
        return img

def footage_frames(src, start, dur, W, H):
    tmp = "/tmp/ppf"; os.makedirs(tmp, exist_ok=True)
    for f in os.listdir(tmp): os.remove(os.path.join(tmp, f))
    # autorotate is default; scale to cover then crop; slow push-in
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"zoompan=z='1+0.0009*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},eq=brightness=-0.04:saturation=1.05")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(dur), "-i", src, "-vf", vf, "-r", str(FPS), f"{tmp}/%04d.png"], check=True)
    return sorted(os.path.join(tmp, f) for f in os.listdir(tmp))

def render(spec, outdir):
    r = Reel(spec); W, H = r.W, r.H; name = spec["name"]; fdir = f"/tmp/ppr_{name}"; os.makedirs(fdir, exist_ok=True)
    for f in os.listdir(fdir): os.remove(os.path.join(fdir, f))
    n = 0
    def put(im):
        nonlocal n; n += 1; im.save(f"{fdir}/{n:05d}.jpg", quality=92)
    D1, D2, D3 = 3.4, 4.2, 4.6
    for i in range(int(D1*FPS)): put(r.hook(i/FPS))
    if spec.get("src"):
        frs = footage_frames(os.path.join(REPO, spec["src"]), spec.get("ss", 0), D2, W, H)
        for i in range(int(D2*FPS)):
            fr = Image.open(frs[min(i, len(frs)-1)]).convert("RGB"); put(r.footage_frame(fr, i/FPS, D2))
    for i in range(int(D3*FPS)): put(r.panel(i/FPS))
    body = f"/tmp/ppr_{name}_body.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{fdir}/%05d.jpg", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", body], check=True)
    tot = n / FPS
    # end card (official, 3s) scaled/padded to WxH
    ec = os.path.join(REPO, "reels/newid/endcard_1080x1920.mp4")
    ecv = f"/tmp/ppr_{name}_ec.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", ec, "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", ecv], check=True)
    total = tot + 3.0
    cuts = f"0,{D1},{D1 + (D2 if spec.get('src') else 0)},{tot}"
    subprocess.run(["python3", os.path.join(REPO, "production/reels-from-statics/music_bed.py"), name, str(total), cuts], check=True, cwd="/tmp")
    out = os.path.join(outdir, name + ".mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", body, "-i", ecv, "-i", f"/home/claude/work/reels/{name}.wav",
                    "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]", "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out], check=True)
    print("ok", out, round(total, 1))

if __name__ == "__main__":
    specs = json.load(open(sys.argv[1])); outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
    only = sys.argv[3].split(",") if len(sys.argv) > 3 else None
    for s in specs:
        if only and s["name"] not in only: continue
        render(s, outdir)
