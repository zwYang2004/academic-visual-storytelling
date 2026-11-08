#!/usr/bin/env python3
"""Generate per-line narration MP3s with Edge-TTS (same tool as previous group project)."""
import asyncio, json, sys
from pathlib import Path
import edge_tts

BASE = Path(__file__).resolve().parent
CFG = json.loads((BASE / "narration.json").read_text(encoding="utf-8"))
OUT = BASE / "audio_lines"
OUT.mkdir(exist_ok=True)
VOICE = CFG["meta"]["voice"]
RATE = CFG["meta"]["rate"]

async def synth(text, path):
    comm = edge_tts.Communicate(text, VOICE, rate=RATE)
    with open(path, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])

async def main():
    n = 0
    for ch in CFG["chapters"]:
        for i, text in enumerate(ch["lines"]):
            out = OUT / f"{ch['id']}_l{i:02d}.mp3"
            await synth(text, out)
            n += 1
            print(f"{ch['id']}_l{i:02d} {len(text.split()):3d}w", flush=True)
    print(f"DONE {n} lines")

asyncio.run(main())
