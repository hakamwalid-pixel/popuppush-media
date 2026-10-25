"""PopupPush static posts 10–23 Nov (1080x1350), same look as the Kafu post set."""
import os
from PIL import Image, ImageDraw, ImageFont
from sprite import paste_kafu

FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + "/"
def font(s, w="Bold"): return ImageFont.truetype(FD + f"IBMPlexSansArabic-{w}.ttf", s, layout_engine=ImageFont.Layout.RAQM)
OUT = "/home/claude/popuppush-media/posts/nov2/"
W, H = 1080, 1350; R = 1000; L = 80
CY = (34, 211, 238); IND = (99, 102, 241); GOLD = (250, 206, 13); WH = (255, 255, 255)
TH = {
    "dark":  dict(bg=(10, 14, 26), fg=WH, mute=(170, 176, 210), acc=CY, chip=(CY, (10, 14, 26)), card=(26, 32, 58), line=(40, 46, 80)),
    "light": dict(bg=(238, 240, 251), fg=(10, 14, 26), mute=(90, 96, 130), acc=(80, 69, 233), chip=((80, 69, 233), WH), card=WH, line=(210, 214, 235)),
    "indigo":dict(bg=(80, 69, 233), fg=WH, mute=(220, 222, 255), acc=GOLD, chip=(GOLD, (10, 14, 26)), card=(64, 54, 200), line=(110, 100, 240)),
    "green": dict(bg=(10, 60, 45), fg=WH, mute=(190, 225, 210), acc=GOLD, chip=(GOLD, (10, 14, 26)), card=(18, 82, 62), line=(30, 96, 74)),
}
def T(d, xy, s, f, fill, anchor="ra"): d.text(xy, s, font=f, fill=fill, anchor=anchor, direction="rtl", language="ar")
def tw(d, s, f): b = d.textbbox((0, 0), s, font=f, direction="rtl", language="ar"); return b[2] - b[0]

def wrap(d, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        nxt = (cur + " " + w).strip()
        if tw(d, nxt, f) <= maxw or not cur: cur = nxt
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def slide(fn, theme, chip, title, accent=None, body=None, items=None, kafu=None, page=None, cta=None, big=None, ghost=None):
    th = TH[theme]; img = Image.new("RGB", (W, H), th["bg"]); d = ImageDraw.Draw(img)
    # chip + wordmark
    fc = font(26); cw = tw(d, chip, fc) + 44
    d.rounded_rectangle([L, 64, L + cw, 108], 22, fill=th["chip"][0]); T(d, (L + cw / 2, 85), chip, fc, th["chip"][1], "mm")
    d.text((R, 86), "PopupPush", font=font(34), fill=th["fg"], anchor="rm")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); y = 0
    if big:
        T(ld, (R, y), big, font(150), th["acc"]); y += 200
    ft = font(80)
    for k, ln in enumerate(title):
        T(ld, (R, y), ln, ft, th["acc"] if accent is not None and k in accent else th["fg"]); y += 104
    y += 24
    if body:
        fb = font(42, "SemiBold")
        for para in body:
            for ln in wrap(ld, para, fb, R - L - (380 if kafu == "side" else 0)):
                T(ld, (R, y), ln, fb, th["mute"]); y += 64
            y += 18
    if items:
        fi, fs = font(44), font(32, "SemiBold")
        for head, sub in items:
            subl = wrap(ld, sub, fs, R - L - 80) if sub else []
            h = (40 + 56 + len(subl) * 46 + 24) if subl else 110
            ld.rounded_rectangle([L, y, R, y + h], 28, fill=th["card"])
            T(ld, (R - 40, y + (30 if subl else 28)), head, fi, th["fg"])
            for j, ln in enumerate(subl): T(ld, (R - 40, y + 98 + j * 46), ln, fs, th["mute"])
            y += h + 22
    if ghost:
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.text((L - 10, 1235), ghost, font=font(520), fill=th["acc"] + (46,), anchor="ls")
        img.paste(gl, (0, 0), gl); d = ImageDraw.Draw(img)
    top, bot = 160, (1080 if cta else 1220)
    off = 170 if kafu else int(max(160, top + (bot - top - y) / 2 - 40))
    img.paste(lay, (0, off), lay); d = ImageDraw.Draw(img)
    if kafu == "side":
        paste_kafu(img, 230, 1010, 360, "happy", 0, "wave1")
    elif kafu == "phone":
        paste_kafu(img, 230, 1010, 360, "happy", 0, "phone")
    elif kafu == "center":
        paste_kafu(img, W / 2, 900, 480, "happy", 1, "cheer")
    d = ImageDraw.Draw(img)
    if cta:
        f = font(42); bw = tw(d, cta, f) + 90
        d.rounded_rectangle([R - bw, 1110, R, 1200], 45, fill=th["acc"]); T(d, (R - bw / 2, 1155), cta, f, th["bg"], "mm")
    d.line([L, 1250, R, 1250], fill=th["line"], width=2)
    d.text((L, 1290), "popuppush.com", font=font(30, "SemiBold"), fill=th["mute"], anchor="lm")
    T(d, (R, 1290), "واتساب 0583272051", font(30), th["fg"], "rm")
    if page: d.text((W / 2, 1290), page, font=font(26, "SemiBold"), fill=th["mute"], anchor="mm")
    os.makedirs(OUT, exist_ok=True); img.save(OUT + fn, quality=95)

CH = "PopupPush"
# S1 — FAQ carousel (11 Nov)
slide("s1_1.jpg", "dark", "قبل التركيب", ["قبل ما تركّب…", "٥ أسئلة", "نسمعها كل يوم."], accent=[1],
      body=["جمعنا لك الأجوبة باختصار.", "اسحب ←"], kafu="side", page="١/٥")
slide("s1_2.jpg", "light", "سؤال ١", ["لازم أغيّر", "التلفزيونات؟"], accent=[1],
      body=["لا. نشتغل على نفس الشاشات اللي عندك.", "الشاشة اللي فيها أندرويد ينزل عليها تطبيق PopupPush مباشرة، والباقي نوصّل لها جهاز أندرويد صغير."], page="٢/٥", ghost="؟")
slide("s1_3.jpg", "dark", "سؤال ٢", ["ووقت", "الصلاة؟"], accent=[1],
      body=["الشاشة توقف لحالها وقت الصلاة مع عدّ تنازلي، وترجع لعرضها بعدها. بكل الباقات.", "توفير الواي فاي ووصوله للشاشات على المكان."], page="٣/٥", ghost="؟")
slide("s1_4.jpg", "green", "سؤال ٣", ["والماتش؟"], accent=[0],
      body=["باقة المباريات فيها جهاز PopupPush يستقبل البث: جهاز لكل مصدر، يعني beIN والدوري = جهازين.", "ومن جوالك توزّع القنوات على الشاشات وتنزّل عروضك حول المباراة بدون ما تغطيها."], page="٤/٥", ghost="؟")
slide("s1_5.jpg", "indigo", "سؤال ٤ و٥", ["أي باقة؟", "وكيف أبدأ؟"], accent=[1],
      items=[("باقة المحتوى", "المنيو والعروض وأوقات الصلاة على أي شاشة Android أو Google TV"),
             ("باقة المباريات", "جهازنا يستقبل البث، والقنوات والعروض حول المباراة من الريموت")],
      body=None, cta="زيارة بدون التزام", page="٥/٥")
# S2 — the daily math (12 Nov)
slide("s2_1.jpg", "dark", "حسبة بسيطة", ["أقل من ٢ ريال", "باليوم للشاشة."], accent=[0],
      body=["باقة المحتوى 50 ريال للشاشة شهرياً، يعني تقريباً 1.7 ريال باليوم.", "أقل من سعر كوب قهوة واحد بالأسبوع، والشاشة تشتغل لك كل يوم: منيو الصبح، عروض العصر، والماتش بالليل."],
      kafu="phone", page="الأسعار بدون الضريبة")
# S3 — hotels (13 Nov)
slide("s3_1.jpg", "dark", "الفنادق", ["كل شاشات الفندق…", "من لوحة وحدة."], accent=[1],
      body=["اللوبي، المطعم، الممرات، وكل الفروع."], kafu="side", page="١/٣")
slide("s3_2.jpg", "light", "الفنادق", ["وين تشتغل؟"], accent=[0],
      items=[("اللوبي", "ترحيب بالضيوف وفعاليات اليوم"),
             ("المطعم", "منيو الفطور والعشاء يتبدّل لحاله حسب الوقت"),
             ("الممرات والمصاعد", "عروض المطعم والخدمات داخل الفندق")], page="٢/٣")
slide("s3_3.jpg", "indigo", "الفنادق", ["مطمّن عليها:"], accent=[0],
      items=[("كل الفروع من مكان واحد", "لوحة وحدة لكل الشاشات"),
             ("صفحة الشاشات", "حالة كل شاشة بنظرة: تعمل، موقوفة، أو الصوت مكتوم"),
             ("وقت الصلاة", "العرض يوقف لحاله ويرجع بعدها")], cta="زيارة بدون التزام", page="٣/٣")
# S4 — clinics & hospitals (16 Nov)
slide("s4_1.jpg", "dark", "العيادات والمستشفيات", ["صالة الانتظار…", "خلّها تفيد."], accent=[1],
      body=["المريض قاعد ينتظر وعينه على الشاشة. خلّ اللي يشوفه يفيده."], kafu="side", page="١/٣")
slide("s4_2.jpg", "light", "العيادات والمستشفيات", ["وش تعرض؟"], accent=[0],
      items=[("توعية وإرشادات", "محتوى صحي ونصايح المراجعين"),
             ("خدمات العيادة", "الأقسام والعروض والباقات"),
             ("حسب الوقت", "المحتوى يتبدّل لحاله بالجدول اللي تحدده")], page="٢/٣")
slide("s4_3.jpg", "indigo", "العيادات والمستشفيات", ["عندكم أكثر", "من فرع؟"], accent=[1],
      items=[("لوحة وحدة لكل الفروع", "تغيّر المحتوى بكل الفروع من مكان واحد"),
             ("وش صار اليوم؟", "سجل لآخر ٧ أيام: مين غيّر وش ومن وين")], cta="زيارة بدون التزام", page="٣/٣")
# S5 — Riyadh Season urgency (17 Nov)
slide("s5_1.jpg", "green", "موسم الرياض", ["موسم الرياض شغّال…", "والدوري شغّال."], accent=[1],
      body=["اللي يركّب الحين يلحق الزحمة: عروضك على كل الشاشات حول المباراة، وكله من المنصة أو جوالك."],
      kafu="center", cta="احجز زيارتك")
# S6 — retail & malls (19 Nov)
slide("s6_1.jpg", "dark", "المحلات والمولات", ["واجهة محلك…", "أقوى بائع عندك."], accent=[1],
      body=["الزبون الماشي برّا يقرر بثواني. خلّ شاشتك تقنعه."], kafu="side", page="١/٣")
slide("s6_2.jpg", "light", "المحلات والمولات", ["وش تسوي الشاشة؟"], accent=[0],
      items=[("عرض الصبح وعرض المسا", "يتبدّلون لحالهم حسب الوقت"),
             ("عدّاد تنازلي", "العرض يخلص بعد ساعة؟ الزبون يشوف الوقت"),
             ("من جوالك", "تغيّر العرض بثواني بدون فلاشة")], page="٢/٣")
slide("s6_3.jpg", "indigo", "المحلات والمولات", ["سلسلة فروع؟"], accent=[0],
      items=[("كل الفروع من لوحة وحدة", "نفس العرض بكل الفروع، أو عرض لكل فرع"),
             ("إيقاف الطوارئ", "كل الشاشات توقف بضغطة وحدة")], cta="زيارة بدون التزام", page="٣/٣")
# S7 — ordering from the screen (20 Nov)
slide("s7_1.jpg", "light", "اطلب من طاولتك", ["يمسح الكود…", "ويطلب من مكانه."], accent=[1],
      body=["الضيف يمسح الكود ويطلب من طاولته، والطلب يوصل المطبخ والكاشير، والشاشة تناديه لما يجهز: «طلبك جاهز». أقل انتظار عند الكاشير."],
      kafu="phone", cta="زيارة بدون التزام")
# S8 — content tier for any Android screen (21 Nov)
slide("s8_1.jpg", "dark", "باقة المحتوى", ["عندك شاشة أندرويد؟", "تشتغل اليوم."], accent=[1],
      items=[("نزّل التطبيق", "تطبيق PopupPush من Google Play"),
             ("بدون جهاز إضافي", "أي شاشة Android أو Google TV"),
             ("أدرها من المنصة أو جوالك", "المنيو والعروض على كل الشاشات")])
# S9 — Kafu engagement question (23 Nov)
slide("s9_1.jpg", "indigo", "كفو يسألك", ["وش نوع مكانك؟"], accent=[0],
      items=[("مقهى", ""), ("لاونج", ""), ("مطعم", ""), ("محل أو عيادة", "")],
      kafu="side", page="اكتب جوابك بالتعليقات")
print("ok")
