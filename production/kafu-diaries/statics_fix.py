"""Replacement posts (31 Oct, 4 Nov 2026) after the official feature guide of 25 Oct 2026. Same look as statics.py."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "statics.py"), encoding="utf-8").read()
src = src.split('CH = "PopupPush"')[0]
src = src.replace('"/home/claude/popuppush-media/posts/nov2/"', repr(os.path.join(HERE, "..", "..", "posts", "fix") + "/"))
os.chdir(HERE)
exec(src)

# 31 Oct — Kafu: screens status page (replaces the offline post)
slide("oct31_status.jpg", "dark", "كفو", ["شاشة طفت…", "وإنت برّا المحل؟"], accent=[1],
      body=["صفحة الشاشات تقولك حالة كل شاشة بنظرة: تعمل، موقوفة، أو الصوت مكتوم.",
            "و«وش صار اليوم» يوريك مين غيّر وش لآخر ٧ أيام."], kafu="phone", cta="زيارة بدون التزام")

# 4 Nov — all branches from one dashboard (4 slides)
slide("nov4_1.jpg", "dark", "الفروع", ["كل فروعك…", "من لوحة وحدة."], accent=[1],
      body=["من داشبورد واحد، أو من تطبيق الريموت على جوالك.", "اسحب ←"], kafu="side", page="١/٤")
slide("nov4_2.jpg", "light", "الفروع", ["لمين؟"], accent=[0],
      items=[("الفنادق", "اللوبي والمطعم والممرات بكل الفروع"),
             ("المستشفيات والعيادات", "صالات الانتظار بكل الفروع"),
             ("سلاسل المطاعم", "نفس العرض بكل الفروع، أو عرض لكل فرع")], page="٢/٤")
slide("nov4_3.jpg", "indigo", "الفروع", ["مطمّن عليها:"], accent=[0],
      items=[("صفحة الشاشات", "حالة كل شاشة بكل فرع بنظرة"),
             ("وش صار اليوم؟", "سجل لآخر ٧ أيام: مين غيّر وش"),
             ("وقت الصلاة", "العرض يوقف لحاله ويرجع بعدها")], page="٣/٤")
slide("nov4_4.jpg", "green", "الفروع", ["عندكم شاشات", "بأكثر من فرع؟"], accent=[1],
      body=["خلّنا نوريك النظام على شاشاتكم."], kafu="center", cta="زيارة بدون التزام", page="٤/٤")

# 5 Nov — «عروضي»: design an offer in a minute (replaces the 14-for-12 price post)
slide("nov5_1.jpg", "dark", "عروضي", ["عرضك…", "جاهز بدقيقة."], accent=[1],
      body=["بدون مصمم ولا طباعة.", "اسحب ←"], kafu="phone", page="١/٣")
slide("nov5_2.jpg", "light", "عروضي", ["كيف؟"], accent=[0],
      items=[("اختار ثيم", "١٢ ثيم جاهز، أو ارفع تصميمك"),
             ("حط السعر والشعار", "برمز الريال الرسمي وشعار مكانك"),
             ("أضف QR", "لإنستغرام أو تقييم جوجل، والمنصة تعدّ المسحات")], page="٢/٣")
slide("nov5_3.jpg", "indigo", "عروضي", ["شوفه…", "واعرضه الآن."], accent=[1],
      body=["معاينة حية قبل ما ينزل، وتختار وقته: الصبح، الظهر، المسا، أو طول اليوم."], cta="زيارة بدون التزام", page="٣/٣")

# 12 Nov — birthday on every screen (replaces the daily-price math post)
slide("nov12_bday.jpg", "indigo", "عيد ميلاد", ["اسم الضيف…", "على كل الشاشات."], accent=[1],
      body=["احتفال باسم الضيف بفيديو وموسيقى، والطاولة كلها تصوّر. لحظة يتذكرها، ويرجع لك."],
      kafu="center", cta="زيارة بدون التزام")
print("ok")
