#!/usr/bin/env python3
"""Measure per-line audio, assemble master WAV (48k mono) with exact offsets, emit timeline.json."""
import json, subprocess, wave, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
CFG = json.loads((BASE / "narration.json").read_text(encoding="utf-8"))
SR = 48000
GAP = CFG["meta"]["line_gap"]        # silence between lines within a chapter
TAIL = CFG["meta"]["chapter_tail"]   # silence after last line of a chapter
MASTER_EXTRA_END = 6.0               # final hold after last line (credits card reading time)

def decode(path):
    """Return (samples, duration) as list of ints, 48k mono s16."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "s16le", "-acodec", "pcm_s16le",
         "-ac", "1", "-ar", str(SR), "-"],
        capture_output=True, check=True).stdout
    return raw

import struct
chapters = []
cursor = 0.0  # seconds
total_frames = 0
segments = []  # (start_frame_samples, raw_bytes)
for ch in CFG["chapters"]:
    lead = ch.get("lead", 1.2)
    cursor += lead
    lines = []
    for i, text in enumerate(ch["lines"]):
        mp3 = BASE / "audio_lines" / f"{ch['id']}_l{i:02d}.mp3"
        raw = decode(mp3)
        dur = len(raw) / 2 / SR
        segments.append((int(round(cursor * SR)), raw))
        lines.append({"text": text, "off": round(cursor, 3), "dur": round(dur, 3)})
        cursor += dur + GAP
    cursor += TAIL - GAP  # tail replaces the last gap
    chapters.append({
        "id": ch["id"], "name": ch["name"], "lead": lead,
        "start": 0.0,  # filled below
        "lines": lines,
    })

# master length & chapter starts
total = cursor + MASTER_EXTRA_END
master = bytearray(int(round(total * SR)) * 2)
for start_samples, raw in segments:
    off = start_samples * 2
    master[off:off + len(raw)] = raw

# recompute chapter starts from first line offset minus lead, then ends from next start
for ch, cfg in zip(chapters, CFG["chapters"]):
    ch["start"] = round(ch["lines"][0]["off"] - ch["lead"], 3)
for i, ch in enumerate(chapters):
    ch["end"] = round(chapters[i + 1]["start"] if i + 1 < len(chapters) else total, 3)

wav_path = BASE / "master_audio.wav"
with wave.open(str(wav_path), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(bytes(master))

timeline = {
    "fps": None,  # set by capture script
    "total": round(total, 3),
    "voice": CFG["meta"]["voice"],
    "chapters": chapters,
}
(BASE / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"TOTAL {total:.1f}s = {total/60:.2f} min")
for ch in chapters:
    print(f"{ch['id']} {ch['start']:7.2f} -> {ch['end']:7.2f}  {ch['name']}")
