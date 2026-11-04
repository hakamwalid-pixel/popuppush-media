import numpy as np, wave
SR = 44100; TOTAL = 24.0; n = int(SR * TOTAL); t = np.arange(n) / SR; mix = np.zeros(n)
rng = np.random.default_rng(5)
def add(sig, at, g):
    i = int(at * SR); j = min(n, i + len(sig)); mix[i:j] += sig[: j - i] * g
def lp(x, k): return np.convolve(x, np.ones(k) / k, "same")
# drone (A) with slow swell, fading for the end card
drone = (np.sin(2*np.pi*55*t) + 0.5*np.sin(2*np.pi*110*t) + 0.25*np.sin(2*np.pi*164.8*t)) * (0.6 + 0.4*np.sin(2*np.pi*0.08*t))
mix += drone * np.interp(t, [0, 2, 16.5, 17.6, 18.5, 24], [0, 0.22, 0.30, 0.05, 0.12, 0])
# pad chords (Am F C G), soft attack
chords = [(220, 261.63, 329.63), (174.61, 220, 261.63), (130.81, 196, 261.63), (196, 246.94, 293.66)]
for k in range(6):
    at = 1.0 + k * 2.8; L = int(3.4 * SR); tt = np.arange(L) / SR
    env = np.minimum(tt / 1.2, 1) * np.exp(-np.maximum(tt - 2.4, 0) * 2)
    s = sum(np.sin(2*np.pi*f*tt) + 0.3*np.sin(2*np.pi*2*f*tt) for f in chords[k % 4]) * env
    if at < 17: add(s, at, 0.05)
def boom(d=2.2, f0=90, f1=34):
    tt = np.arange(int(d * SR)) / SR; f = f1 + (f0 - f1) * np.exp(-tt * 6)
    ph = 2*np.pi*np.cumsum(f) / SR; return np.sin(ph) * np.exp(-tt * 2.2) + lp(rng.standard_normal(len(tt)), 40) * np.exp(-tt * 9) * 0.6
def riser(d):
    tt = np.arange(int(d * SR)) / SR; s = lp(rng.standard_normal(len(tt)), 6) * (tt / d) ** 2
    return s + 0.3 * np.sin(2*np.pi*(200 + 900*(tt/d)**2)*tt) * (tt / d) ** 2
def whoosh(d=1.2):
    s = lp(rng.standard_normal(int(d * SR)), 18); k = np.linspace(0, 1, len(s)); return s * np.sin(np.pi * k) ** 2
def blip(f=1760):
    tt = np.arange(int(0.25 * SR)) / SR; return np.sin(2*np.pi*f*tt) * np.exp(-tt * 18)
for i in range(4): add(blip(1320 + i * 220), 0.6 + i * 0.35, 0.08)          # screens power on
add(riser(1.6), 2.4, 0.12); add(boom(), 4.0, 0.55)                       # screens join
add(whoosh(1.4), 6.4, 0.30); add(boom(2.6, 120, 40), 6.8, 0.45)          # ad reveal
add(whoosh(1.4), 13.5, 0.22); add(boom(1.6, 70, 36), 15.0, 0.25)          # back to menus
add(riser(1.8), 15.8, 0.14); add(boom(3.0, 110, 30), 17.6, 0.6)           # logo hit
tt = np.arange(int(4 * SR)) / SR                                          # shimmer on the end card
for k, f in enumerate([880, 1108.7, 1318.5, 1760]):
    add(np.sin(2*np.pi*f*tt) * np.minimum(tt / 0.4, 1) * np.exp(-tt * 0.9), 18.4 + k * 0.15, 0.04)
mix *= np.interp(t, [0, 0.05, TOTAL - 1.2, TOTAL], [0, 1, 1, 0])
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.9
pcm = (np.repeat(mix[:, None], 2, axis=1) * 32767).astype(np.int16)
with wave.open("/root/vw/cin.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
