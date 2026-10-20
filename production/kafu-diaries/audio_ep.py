import numpy as np, wave

SR = 44100; DUR = 16.0
n = int(SR * DUR); t = np.arange(n) / SR
mix = np.zeros(n)
rng = np.random.default_rng(7)

def env(length, a=0.005, r=0.2):
    e = np.ones(length); ai = int(a * SR); ri = min(int(r * SR), length)
    e[:ai] = np.linspace(0, 1, ai); e[-ri:] *= np.exp(-np.linspace(0, 5, ri)); return e
def add(sig, at, gain=1.0):
    i = int(at * SR)
    if i >= n: return
    j = min(n, i + len(sig)); mix[i:j] += sig[: j - i] * gain
def tone(f, d, wav="sine"):
    tt = np.arange(int(d * SR)) / SR
    if wav == "sine": return np.sin(2 * np.pi * f * tt)
    if wav == "tri": return 2 * np.abs(2 * ((f * tt) % 1) - 1) - 1
def note(f, d, g=1.0, r=0.25, wav="tri"):
    s = tone(f, d, wav) * 0.7 + tone(2 * f, d) * 0.15
    return s * env(len(s), 0.01, r) * g

# ---- background music: 104 bpm, 4-chord loop, light and upbeat ----
bpm = 104; beat = 60 / bpm
chords = [(220.0, 277.18, 329.63), (174.61, 220.0, 261.63), (130.81, 164.81, 196.0), (196.0, 246.94, 293.66)]
bass = [110.0, 87.31, 65.41, 98.0]
music = np.zeros(n)
def madd(sig, at, g):
    i = int(at * SR)
    if i >= n: return
    j = min(n, i + len(sig)); music[i:j] += sig[: j - i] * g
bar = 0; x = 0.0
while x < DUR:
    c = chords[bar % 4]
    for k in range(4):
        at = x + k * beat
        # pluck arpeggio on 8ths
        for h in range(2):
            f = c[(k * 2 + h) % 3] * (2 if h else 1)
            madd(note(f, beat * 0.5, 1, 0.18), at + h * beat / 2, 0.09)
        madd(note(bass[bar % 4], beat * 0.9, 1, 0.3, "sine"), at, 0.22)
        # kick on 1 & 3, clap on 2 & 4, hats on 8ths
        if k % 2 == 0:
            kt = np.arange(int(0.18 * SR)) / SR
            kick = np.sin(2 * np.pi * (50 + 90 * np.exp(-kt * 30)) * kt) * np.exp(-kt * 18)
            madd(kick, at, 0.45)
        else:
            cl = rng.standard_normal(int(0.12 * SR)) * np.exp(-np.arange(int(0.12 * SR)) / SR * 35)
            madd(cl, at, 0.10)
        for h in range(2):
            hh = rng.standard_normal(int(0.03 * SR)); hh = np.diff(hh, prepend=0) * np.exp(-np.arange(len(hh)) / SR * 150)
            madd(hh, at + h * beat / 2, 0.05)
    x += 4 * beat; bar += 1
# worried intro (0–4.5s) softer, music swells after the phone appears
ramp = np.interp(t, [0, 0.08, 4.4, 5.0, 12.3, 12.7, 15.4, 16.0], [0.3, 0.45, 0.45, 1.0, 1.0, 0.75, 0.75, 0])
mix += music * ramp

# ---- sound effects synced to the video ----
def whoosh(d=0.45, up=True):
    s = rng.standard_normal(int(d * SR)); k = np.linspace(0, 1, len(s))
    s = np.convolve(s, np.ones(12) / 12, "same")
    return s * (np.sin(np.pi * k) ** 2)
def pop():
    tt = np.arange(int(0.12 * SR)) / SR
    return np.sin(2 * np.pi * (300 + 900 * tt / 0.12) * tt) * np.exp(-tt * 30)
def click():
    tt = np.arange(int(0.04 * SR)) / SR
    return np.sin(2 * np.pi * 2200 * tt) * np.exp(-tt * 120)
def ding(f=1318.5):
    return note(f, 0.6, 1, 0.5, "sine") + note(f * 1.5, 0.6, 0.4, 0.5, "sine")
def chaching():
    s = np.zeros(int(0.7 * SR)); s[:len(click())] += click() * 0.8
    d2 = note(1760, 0.6, 1, 0.5, "sine") + note(2637, 0.6, 0.5, 0.4, "sine")
    s[int(0.08 * SR):int(0.08 * SR) + len(d2)] += d2[: len(s) - int(0.08 * SR)]
    return s
def cheer(d=1.6):
    s = rng.standard_normal(int(d * SR)); s = np.convolve(s, np.ones(40) / 40, "same")
    k = np.linspace(0, 1, len(s)); return s * np.sin(np.pi * k) ** 1.5 * 4

import sys
EP = sys.argv[1]
if EP == "4":
    add(note(196, 0.5, 1, 0.4, "sine") + note(185, 0.5, 0.6, 0.4, "sine"), 0.7, 0.25)
    for k in range(6): add(click(), 0.5 + k * 0.6, 0.12)            # footsteps of passer-by
    add(note(233, 0.35, 1, 0.3, "sine"), 2.4, 0.2)
    add(whoosh(0.4), 4.4, 0.25); add(pop(), 4.75, 0.4)
    add(click(), 6.45, 0.6)
    add(whoosh(0.35), 7.75, 0.3); add(ding(), 8.0, 0.35)            # kiosk lights up: morning offer
    add(click(), 9.65, 0.6); add(ding(1568), 10.0, 0.3)             # switch to evening offer
    add(pop(), 10.4, 0.35)                                          # «أووه! عرض»
    add(note(880, 0.25, 1, 0.2, "sine"), 11.4, 0.25); add(note(1175, 0.4, 1, 0.3, "sine"), 11.6, 0.25)  # door chime
    add(whoosh(0.5), 12.3, 0.3)
elif EP == "6":
    add(note(196, 0.5, 1, 0.4, "sine") + note(185, 0.5, 0.6, 0.4, "sine"), 0.7, 0.25)
    add(note(233, 0.35, 1, 0.3, "sine"), 2.6, 0.2)
    add(whoosh(0.4), 4.4, 0.25); add(pop(), 4.75, 0.4)
    add(click(), 6.45, 0.6)
    add(whoosh(0.35), 7.75, 0.3); add(chaching(), 8.0, 0.4); add(cheer(2.2), 8.0, 0.2)   # party mode on all screens
    for k2, f in enumerate([523.25, 523.25, 587.33, 523.25, 698.46, 659.25]):        # birthday-style chime
        add(note(f, 0.32, 1, 0.25, "sine"), 8.6 + k2 * 0.3, 0.2)
    add(pop(), 10.6, 0.35)
    add(whoosh(0.5), 12.3, 0.3)
elif EP == "7":
    add(note(196, 0.5, 1, 0.4, "sine") + note(185, 0.5, 0.6, 0.4, "sine"), 0.7, 0.25)
    add(note(233, 0.35, 1, 0.3, "sine"), 2.6, 0.2)
    add(whoosh(0.4), 4.4, 0.25); add(pop(), 4.75, 0.4)
    add(click(), 6.45, 0.6)
    add(whoosh(0.35), 7.75, 0.3); add(ding(), 8.0, 0.35)          # countdown appears
    for k in range(4): add(click(), 8.5 + k * 1.0, 0.25)           # ticking
    add(pop(), 9.0, 0.3)
    for k in range(5): add(click(), 9.6 + k * 0.28, 0.12)          # guest walks to the counter
    add(chaching(), 10.6, 0.45)
    add(whoosh(0.5), 12.3, 0.3)
else:
    add(note(196, 0.5, 1, 0.4, "sine") + note(185, 0.5, 0.6, 0.4, "sine"), 0.7, 0.25)
    for k in range(5): add(click(), 2.7 + k * 0.32, 0.12)           # guest walks away
    add(note(233, 0.35, 1, 0.3, "sine"), 2.6, 0.2)
    add(whoosh(0.4), 4.4, 0.25); add(pop(), 4.75, 0.4)
    add(click(), 6.45, 0.6)
    for k in range(3): add(click(), 8.0 + k * 0.25, 0.12)           # guest comes back
    for k2, at in enumerate([8.0, 9.0, 9.8]): add(ding(1046.5 * (1.122 ** (k2 * 2))), at, 0.28)   # points rising
    add(chaching(), 10.4, 0.45); add(cheer(1.6), 10.4, 0.15)        # gift unlocked
    add(pop(), 10.6, 0.35)
    add(whoosh(0.5), 12.3, 0.3)
for k2, f in enumerate([523.25, 659.25, 783.99, 1046.5]):
    add(note(f, 0.5, 1, 0.4, "sine"), 12.8 + k2 * 0.12, 0.22)
add(pop(), 13.6, 0.35)

mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
pcm = (np.repeat(mix[:, None], 2, axis=1) * 32767).astype(np.int16)
with wave.open(f"/home/claude/kafu3/ep{EP}_audio.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok")
