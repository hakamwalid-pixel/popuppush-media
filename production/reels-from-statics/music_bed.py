import sys, json, numpy as np, wave
SR = 44100
name, total = sys.argv[1], float(sys.argv[2]); cuts = [float(x) for x in sys.argv[3].split(",")]
n = int(SR * total); mix = np.zeros(n); rng = np.random.default_rng(11)
def add(sig, at, g):
    i = int(at * SR)
    if i >= n: return
    j = min(n, i + len(sig)); mix[i:j] += sig[: j - i] * g
def env(L, a=0.01, r=0.25):
    e = np.ones(L); ai = int(a * SR); ri = min(int(r * SR), L); e[:ai] = np.linspace(0, 1, ai); e[-ri:] *= np.exp(-np.linspace(0, 5, ri)); return e
def tone(f, d): tt = np.arange(int(d * SR)) / SR; return np.sin(2 * np.pi * f * tt)
def tri(f, d): tt = np.arange(int(d * SR)) / SR; return 2 * np.abs(2 * ((f * tt) % 1) - 1) - 1
def note(f, d, r=0.25, w=tri): s = w(f, d) * 0.7 + tone(2 * f, d) * 0.15; return s * env(len(s), 0.01, r)
bpm = 112; beat = 60 / bpm
chords = [(220.0, 277.18, 329.63), (185.0, 220.0, 277.18), (146.83, 185.0, 220.0), (164.81, 207.65, 246.94)]
bass = [110.0, 92.5, 73.42, 82.41]
x = 0.0; bar = 0
while x < total:
    c = chords[bar % 4]
    for k in range(4):
        at = x + k * beat
        for h in range(2): add(note(c[(k * 2 + h) % 3] * (2 if h else 1), beat * 0.5, 0.18), at + h * beat / 2, 0.09)
        add(note(bass[bar % 4], beat * 0.9, 0.3, tone), at, 0.22)
        if k % 2 == 0:
            kt = np.arange(int(0.18 * SR)) / SR; add(np.sin(2 * np.pi * (50 + 90 * np.exp(-kt * 30)) * kt) * np.exp(-kt * 18), at, 0.45)
        else:
            L = int(0.12 * SR); add(rng.standard_normal(L) * np.exp(-np.arange(L) / SR * 35), at, 0.10)
        for h in range(2):
            L = int(0.03 * SR); hh = np.diff(rng.standard_normal(L), prepend=0) * np.exp(-np.arange(L) / SR * 150); add(hh, at + h * beat / 2, 0.05)
    x += 4 * beat; bar += 1
t = np.arange(n) / SR; endt = cuts[-1]
mix *= np.interp(t, [0, 0.05, endt - 0.3, endt + 0.2, total - 0.6, total], [0.6, 1, 1, 0.7, 0.7, 0])
def whoosh(d=0.4):
    s = np.convolve(rng.standard_normal(int(d * SR)), np.ones(12) / 12, "same"); k = np.linspace(0, 1, len(s)); return s * np.sin(np.pi * k) ** 2
for c in cuts[1:]: add(whoosh(0.35), c - 0.2, 0.28)
for k2, f in enumerate([523.25, 659.25, 783.99, 1046.5]): add(note(f, 0.5, 0.4, tone), endt + 0.3 + k2 * 0.12, 0.22)
tt = np.arange(int(0.12 * SR)) / SR; add(np.sin(2 * np.pi * (300 + 900 * tt / 0.12) * tt) * np.exp(-tt * 30), endt + 1.1, 0.35)
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
pcm = (np.repeat(mix[:, None], 2, axis=1) * 32767).astype(np.int16)
with wave.open(f"/home/claude/work/reels/{name}.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok", name)
