#!/usr/bin/env python3
"""Inject timeline.json into renderer.html (replace __TIMELINE__ placeholder)."""
import json
from pathlib import Path
BASE = Path(__file__).resolve().parent
tl = (BASE / "timeline.json").read_text(encoding="utf-8")
html = (BASE / "renderer.html").read_text(encoding="utf-8")
html = html.replace("__TIMELINE__", tl)
(BASE / "renderer_final.html").write_text(html, encoding="utf-8")
print("renderer_final.html written,", len(html), "bytes")
