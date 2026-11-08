#!/usr/bin/env python3
"""Mix narration (master_audio.wav) + optional BGM bed + chapter SFX -> master_mix.wav.

BGM source and level come from narration.json meta:
  "bgm_file": "bgm.mp3",   # any audio file; tiled with 6s crossfades; omit/missing = no bed
  "bgm_gain": 0.09         # 0.05 = subtle, 0.09 = clearly present under VO
A soft air-whoosh fires at each chapter start. Output is 48 kHz mono, faststart-ready.
"""
import json, wave, math, subprocess
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parent
SR = 48000
CFG = json.loads((BASE / "narration.json").read_text(encoding="utf-8"))
TL = json.loads((BASE / "timeline.json").read_text(encoding="utf-8"))
TOTAL = TL["total"]

def rd_wav(name):
    with wave.open(str(BASE / name), "rb") as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0

def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "s16le",
                          "-acodec", "pcm_s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768.0

vo = rd_wav("master_audio.wav")
n = len(vo)
mix = vo.copy()

# ---------------- BGM bed: tiled with 6s crossfades ----------------
bgm_name = CFG["meta"].get("bgm_file")
bgm_gain = float(CFG["meta"].get("bgm_gain", 0.09))
bgm_path = BASE / bgm_name if bgm_name else None
if bgm_path and Path(bgm_path).exists():
    src = decode(bgm_path)
    src *= 0.9 / max(1e-9, np.abs(src).max())
    L = len(src); XF = int(6 * SR)
    if L > XF + SR:
        bgm = np.zeros(n)
        r_in, r_out = np.linspace(0, 1, XF), np.linspace(1, 0, XF)
        i0 = 0
        while i0 < n:
            e1 = min(n, i0 + L)
            seg = src[: e1 - i0].copy()
            if i0 > 0: seg[:XF] *= r_in[: len(seg)]
            if (e1 - i0) == L and i0 + L < n: seg[-XF:] *= r_out
            bgm[i0:e1] += seg
            i0 += L - XF
        fd = int(3 * SR); bgm[:fd] *= np.linspace(0, 1, fd)
        fd = int(9 * SR); bgm[-fd:] *= np.linspace(1, 0, fd)
        bgm *= 0.9 / max(1e-9, np.abs(bgm).max())
        mix += bgm * bgm_gain
        print(f"BGM: {bgm_path.name} tiled, gain {bgm_gain}")
else:
    print("BGM: none found — VO only")

# ---------------- SFX: air-whoosh at each chapter start ----------------
def whoosh():
    n = int(0.6 * SR)
    rng = np.random.default_rng(7)
    x = rng.standard_normal(n)
    out = np.zeros(n)
    K = np.linspace(500, 30, 12).astype(int)
    step = n // 12
    for i in range(12):
        ker = np.hanning(max(3, K[i])); ker /= ker.sum()
        s = i * step; e = min(n, s + step + len(ker))
        out[s:e] += np.convolve(x[s:e], ker)[: e - s]
    na = int(0.12 * SR)
    env = np.ones(n); env[:na] = np.linspace(0, 1, na); env[-int(.35*SR):] = np.linspace(1, 0, int(.35*SR))
    out *= env
    return out / max(1e-9, np.abs(out).max())

def add(sig, at, gain):
    s = int(at * SR); e = min(n, s + len(sig))
    if s < n: mix[s:e] += sig[: e - s] * gain

wh = whoosh()
for c in TL["chapters"][1:]:
    add(wh, c["start"] + 0.02, 0.16)

# ---------------- write ----------------
mix = np.clip(mix, -0.98, 0.98)
peak = np.abs(mix).max()
if peak > 0.89: mix *= 0.89 / peak
with wave.open(str(BASE / "master_mix.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print(f"master_mix.wav: {TOTAL:.1f}s, peak {20*math.log10(max(1e-9,peak)):.1f} dBFS")
