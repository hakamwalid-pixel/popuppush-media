"""New-identity static carousel slides (4:5 or 9:16) — same look as the new reels/X cards."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from make_newid_reel import *

def slide(fn, W, H, color, chip, title, body=None, items=None, cta=True, page=None, note=None, tsize=96):
    A = ACC[color]; img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
    top = 70; lockup(d, 70, top, 70)
    fc = rx(32, 600); cw = tw(d, chip, fc) + 56; R = W - 70
    d.rounded_rectangle([R - cw, top + 4, R, top + 66], 31, fill=L2, outline=A, width=3); T(d, (R - cw/2, top + 35), chip, fc, A, "mm")
    maxw = W - 140
    while tsize > 60 and max(tw(d, l, rx(tsize)) for l in title) > maxw: tsize -= 4
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); y = 0
    ft = rx(tsize); lh = int(tsize * 1.3)
    for k, ln in enumerate(title): T(ld, (R, y), ln, ft, A if k == len(title) - 1 else TX); y += lh
    y += 24
    if body:
        fb = px(44)
        for para in body:
            for ln in wrap(ld, para, fb, maxw): T(ld, (R, y), ln, fb, MU); y += 66
            y += 12
    if items:
        y += 10; rowh = 104; ch = rowh * len(items) + 40
        ld.rounded_rectangle([70, y, R, y + ch], 32, fill=L1, outline=LN, width=2); yy = y + 30
        fi = px(46)
        for k, it in enumerate(items):
            ld.ellipse([R - 66, yy + 22, R - 34, yy + 54], fill=A); T(ld, (R - 92, yy + 38), it, fi, TX, "rm")
            if k < len(items) - 1: ld.line([110, yy + rowh - 10, R - 30, yy + rowh - 10], fill=LN, width=2)
            yy += rowh
        y += ch + 10
    if cta:
        y += 34; fcta = rx(48); t = "احجز ديمو مجاني"; bw = tw(ld, t, fcta) + 110
        ld.rounded_rectangle([R - bw, y, R, y + 100], 50, fill=HO); T(ld, (R - bw/2, y + 50), t, fcta, BG, "mm"); y += 100
    if note:
        y += 30; fn_ = px(32, "Medium")
        for ln in wrap(ld, note, fn_, maxw): T(ld, (R, y), ln, fn_, MU); y += 48
    avail_top, avail_bot = top + 130, H - 150
    off = avail_top + max(0, (avail_bot - avail_top - y) // 2)
    img.paste(lay, (0, off), lay); d = ImageDraw.Draw(img)
    yb = H - 110; d.line([70, yb - 30, R, yb - 30], fill=LN, width=2)
    T(d, (R, yb + 10), "مكانك كله، من تطبيق واحد.", rx(32, 600), TX, "rm")
    d.text((70, yb + 10), "popuppush.com", font=px(30), fill=MU, anchor="lm")
    if page: T(d, (W/2, yb + 10), page, px(28), MU, "mm")
    img.save(fn, quality=93)

O = sys.argv[1]; os.makedirs(O, exist_ok=True)
TAX = "الأسعار لا تشمل ضريبة القيمة المضافة."
# LI 17 Nov 13:00 — 3 questions
slide(O+"/li17_1.jpg", 1080, 1350, "honey", "قبل أن تركّب", ["قبل أن تركّب شاشاتك…", "ثلاثة أسئلة نسمعها كل يوم."], items=["هل أحتاج شاشات جديدة؟", "ووقت الصلاة؟", "وأي باقة تناسبني؟"], cta=False, page="١/٣ — اسحب")
slide(O+"/li17_2.jpg", 1080, 1350, "mint", "سؤال ١ و٢", ["هل أحتاج شاشات جديدة؟", "في أغلب الحالات، لا."], body=["تعمل شاشاتك الحالية في أغلب الحالات، وبالديمو نحدّد الأنسب.", "ووقت الصلاة؟ يتوقف العرض تلقائياً ويعود بعدها."], cta=False, page="٢/٣", tsize=84)
slide(O+"/li17_3.jpg", 1080, 1350, "honey", "سؤال ٣", ["أي باقة تناسبني؟", "نبدأ من مكانك."], items=["باقة المحتوى: ٥٠ ريال للشاشة شهرياً", "المنيو والعروض والجدولة", "لوحة تحكم واحدة أو جوالك"], note=TAX, page="٣/٣")
# LI 19 Nov 09:00 — storefront
slide(O+"/li19_1.jpg", 1080, 1350, "violet", "المحلات والفروع", ["واجهة محلك…", "أول ما يراه الزبون."], body=["الزبون يمرّ بجانب محلك كل يوم. اجعل واجهتك تقول له شيئاً واضحاً."], cta=False, page="١/٣ — اسحب")
slide(O+"/li19_2.jpg", 1080, 1350, "violet", "عرض لكل وقت", ["عرض الصباح والمساء…", "يتبدّلان وحدهما."], items=["عرض الصباح في وقته", "عرض المساء في وقته", "عدّاد تنازلي يوضّح متى ينتهي العرض"], cta=False, page="٢/٣")
slide(O+"/li19_3.jpg", 1080, 1350, "honey", "سلسلة فروع؟", ["كل الفروع…", "من حساب واحد."], items=["العرض نفسه في كل الفروع", "أو عرض خاص لكل فرع", "وكل مدير يرى فرعه"], page="٣/٣")
# TikTok 19 Nov 18:00 — 9:16 carousel
slide(O+"/tt19_1.jpg", 1080, 1920, "rose", "واجهة المحل", ["يمرّ بجانب محلك…", "فماذا يرى؟"], items=["واجهة مطفأة", "نفس البوستر منذ شهور", "خط صغير لا يُقرأ", "بلا سعر واضح"], cta=False, page="١/٣ — اسحب", tsize=104)
slide(O+"/tt19_2.jpg", 1080, 1920, "mint", "واجهة واضحة", ["عرض لكل وقت…", "وسعر بارز."], items=["عرض الصباح للفطور", "عرض المساء للعشاء", "سعر كبير وواضح", "يتبدّل وحده في وقته"], cta=False, page="٢/٣", tsize=104)
slide(O+"/tt19_3.jpg", 1080, 1920, "honey", "احفظ المنشور", ["٤ قواعد", "لواجهة تبيع."], items=["خط كبير يُقرأ من بعيد", "سعر واحد بارز", "صورة واحدة واضحة", "عرض لكل وقت"], page="٣/٣", tsize=110)
# LI 26 Nov 09:00 — white friday
slide(O+"/li26_1.jpg", 1080, 1350, "rose", "الجمعة البيضاء", ["العرض ينتهي منتصف الليل…", "والعدّاد يعمل."], body=["ضع عرضك على كل شاشاتك مع عدّاد تنازلي، وغيّره في ثوانٍ من لوحة تحكم واحدة أو من جوالك."], items=["العرض نفسه في كل الفروع", "وكل مدير يرى فرعه"], tsize=84)
print("done")
