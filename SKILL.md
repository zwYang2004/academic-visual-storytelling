---
name: academic-visual-storytelling
description: >-
  End-to-end system for producing cinematic, narration-driven explainer videos
  in ANY domain (biology, medicine, physics, AI, engineering, economics,
  humanities) as deterministic motion graphics: a narration-first timeline, a
  single-file HTML/JS frame renderer captured headlessly, a Claude/Anthropic-
  inspired editorial design system (warm ivory, artifact cards, editorial
  serif), a multi-image/figure pipeline, beat-synced motion, credits and sound
  design, and a verify-before-render workflow.
---

# Academic Visual Storytelling — The General Explainer Video System
> **From narration script to finished MP4, for any subject.**
> *Design language inspired by Vox, 3Blue1Brown, Apple Keynote & Claude/Anthropic.
> Production language: deterministic frame rendering — the same mental model as
> Remotion, with zero runtime dependencies.*

---

## 0. The Two Halves of This Skill

This skill has two halves. Both are mandatory; skipping either produces either
beautiful garbage or ugly correctness.

1. **The Design Language** (§1–§7): what every frame should look like —
   domain-agnostic tokens, artifact containers, the 3-phase case architecture,
   beat-synced motion, captions, credits, sound.
2. **The Production Language** (§8–§11): how the film is actually built —
   narration-first timeline, deterministic frame renderer, headless capture,
   audio mastering, the verify-before-render loop, and data integrity.

**Domain neutrality**: nothing below is specific to biology. Every rule is
phrased as a *role* (FOCUS accent, SIGNAL color, RISK color, subject identity),
with per-domain recipes in §2.3. All worked examples are bio; swap tokens and
vocabulary for your domain.

---

## 1. Core Philosophy

An explainer video is a **visual research essay**, not a slide deck and not a
hype reel.

### The Five Pillars

1. **The Visual-First Rule (the prime directive)**:
   Every narration line must map to a visual event — a diagram, a chart, an
   image, an animated mechanism, or a highlighted artifact. A screen that only
   re-displays the narration as text is a **failure state**. If you cannot draw
   the sentence, redesign the sentence.
2. **The Mechanism-Before-Formula Rule** (3Blue1Brown):
   Show an intuitive animated schematic *before* any equation, table, or dense
   evidence. Concepts are drawn; evidence is shown; conclusions are stated.
3. **The Primary-Evidence Rule** (Vox):
   Real papers/photos/data are treated as artifacts: cropped to the decisive
   panel, shown large on an elevated panel, credited on-screen, probed by a
   lens. Never a full-page screenshot at 40% size.
4. **The Sculptural-Number Rule** (Apple Keynote):
   Colossal metrics (120–160px, tabular) paired with whisper-small mono labels.
   Every number counts up (odometer) and settles with a slight overshoot.
5. **The Claude Rule (Warm Editorial & Artifact Architecture)**:
   Warm ivory canvas, white rounded artifact cards with hairline borders and
   diffuse shadows, deep espresso ink, editorial serif headlines in Title Case,
   mono uppercase metadata — reject both cold corporate white and neon cyber.

### The Anti-Stagnation Rule
No visual state may hold still for more than ~10 seconds. Long chapters are
carried by per-line reveals, phase crossfades, camera drift (1.00→1.03 push),
and beat-synced activations. Static >10s = redesign the scene.

---

## 2. Design System (Domain-Agnostic)

### 2.1 Semantic Color Roles (the only colors you need)

Colors are **roles**, never decoration. Pick four roles once per project and
map every element to them consistently:

| Role | Meaning | Light-mode token (default) |
| :--- | :--- | :--- |
| Canvas | background | `#FAF7F2` warm ivory |
| Panel / Artifact | cards, plates, elevated figures | `#FFFFFF` @ `1px solid rgba(31,30,29,.07)` |
| Ink | primary text | `#1F1E1D` deep espresso |
| Muted | metadata, subtext | `#8A8178` warm taupe |
| Hairline | borders, grid | `#EAE3D8` |
| **FOCUS accent** | decisions, key claims, keywords, the lens | `#C05621` terracotta |
| **SIGNAL accent** | data, mechanism, the "AI/measurement" voice | `#4D8B7E` sage |
| **RISK accent** | limits, errors, drift, false alarms | `#C74A2E` terracotta-red |
| **Gold** | positive/ground-truth highlights | `#C49A3B` |

Rules: text-safe accents only (gold is for fills/dots, not small text);
true-positive vs false-positive must differ in **hue**, not just brightness;
warn/positive pairs must stay distinguishable for color-blind viewers (pair
color with position or label).

**Token-migration rule**: when a palette changes, grep and migrate *both* the
CSS variables **and** the bare color strings inside JS canvas code (gradient
stops, dot fills, rung colors live as inline `'r,g,b'` arrays, not `var()`).
A CSS-only swap leaves the canvas painting the old palette — this exact bug
occurred in a real re-theme.

### 2.2 Domain Palette Recipes (swap the accents, keep the system)

| Domain | FOCUS | SIGNAL | RISK | Signature motif |
| :--- | :--- | :--- | :--- | :--- |
| Bio / medicine | terracotta `#C05621` | sage `#4D8B7E` | `#C74A2E` | double helix, chromatogram, dot population |
| Physics / math | copper `#B4552D` | indigo `#3E5C94` | `#C0392B` | orbit paths, vector fields, construction lines |
| CS / AI tech | burnt orange `#C05621` | slate blue `#44639C` | `#C74A2E` | terminal grid, node graphs, token streams |
| Environment / climate | olive `#7A7A2E` | teal `#2E7D74` | `#B65438` | contour bands, time spirals, map choropleths |
| Economics / society | oxblood `#8E3B2F` | slate `#4A6274` | `#B65438` | flow bands, stacked rivers, archival photos |
| Humanities / history | sepia `#8E6B3E` | iron-gall ink `#3E4A5A` | `#A03B2E` | manuscript panels, timeline ribbons, maps |

Canvas stays warm ivory in almost all cases (projector-safe, prints well,
Claude-recognizable). Dark "observatory" mode exists for immersive/cosmic
topics (`#0A0F1C` base, luminous accents) but is a deliberate exception, not
the default — and must be a full-token swap, never a hybrid.

### 2.3 Typography

| Layer | Family | Spec |
| :--- | :--- | :--- |
| Display headlines | Editorial serif — Playfair Display / Newsreader / Fraunces | **Title Case, never all-caps**; 64–112px; lh 1.1–1.2 |
| Body / explainers | Space Grotesk / Inter | 26–32px; lh 1.4–1.5 |
| Sculptural metrics | Space Grotesk 700 (tabular) | 120–160px |
| Metadata / data / labels | IBM Plex Mono / JetBrains Mono | 16–20px; UPPERCASE tracking .15–.25em |

### 2.4 The Artifact Container & Anti-Empty-Space

- Related content lives in white rounded cards: `border-radius 16–24px`,
  `1px solid rgba(31,30,29,.07)`, shadow `0 10px 30px rgba(31,30,29,.06)`.
- Backgrounds are never bare: blueprint grid (120px lines @ ~4.5% ink) + dot
  grid (46px) + soft vignette fill the periphery.
- Every chapter opens with a **chapter anchor**: mono kicker (`CH 04 · THREE
  CASES`) + serif headline (`Why it matters.`) at top-left.
- Persistent HUD: 2px progress line (top), chapter code (bottom-left),
  timecode (bottom-right) — denominators derived from data, never hardcoded.

---

## 3. The Five Screen Archetypes

Almost every scene in an explainer is one of five archetypes. Choose per
chapter; an 11–13 min film typically uses: Cover → Route → Mechanism → Data
Engine → 3–6 Cases → Conclusions → Close.

1. **Cover Film (45–60s)** — see §7. Never a static title card.
2. **Route / Overview (15–25s)** — numbered markers/cards laid out spatially;
   pop in order; narration questions highlight (amber) their marker; a
   progress rail teases the case count.
3. **Mechanism Chain (40–70s)** — 3–5 connected node-cards with a travelling
   pulse; live mini-instruments (oscilloscope, chromatogram, gauge) activate
   as named; the final "human/decision" node stays hollow with a lock badge.
4. **Data Engine (50–80s)** — a population/chart on one side, a sculptural
   number + warning stamp on the other; parameters step while the number
   animates continuously (derive displayed values from a formula, not presets).
5. **Case Dossier (55–90s)** — the 3-Phase architecture (§4).
6. **Conclusions + Close (50–70s)** — 3 underlined statement rows (fade out as
   the quote card overlays), a dark quote panel, then a static references wall
   (8–10s, readable, no scrolling blur), then the CRediT dossier card (≥6s).

---

## 4. The 3-Phase Case Architecture

A 60–90s case study is **three sequential phases gated by narration lines**
(never one crowded screen). Crossfade phases over 0.4–0.6s; gate all later
phase elements by the phase-alpha so nothing collides.

```
Shot A · Concept Schematic      Shot B · Primary Evidence       Shot C · Critical Boundary
(narration: setup lines)        (narration: mechanism/result)   (narration: limitation lines)
Clean vector animation          Reproduced figure, cropped,     Drop-off chart / warning stamp /
explaining the mechanism        lens-probed, hero metrics       "≠" statement + evidence list
```

- **Shot A** is a *simplified vector diagram unique to the case* — reads→tensor→CNN
  scan; healthy vs flagged cfDNA in a vessel; H&E tile grid with tags;
  colony→laser→fingerprint; ancestry dot census; supply/demand curves…
- **Shot B** is the reproduced journal figure (cropped to the decisive panel) on
  a paper panel with an on-screen credit, a lens magnifier over the decisive
  region, and hero metrics **verified from the paper or the figure itself**.
- **Shot C** is the boundary: drop-off bars, drift curves, "A ≠ B" statements in
  serif with the ≠ in RISK color, plus the evidence list that would be required.
- When a contributor's domain has no dedicated narration, **write 3 new VO
  lines in the established voice and give it a real chapter** (ask the user;
  they approved this for a "Case 5 · Ethics" chapter).

---

## 5. Motion Language

- **Easing**: entrances easeOutExpo `cubic-bezier(.16,1,.3,1)`; stagger 40–80ms;
  camera drift 1.00→1.03 per chapter; nothing bounces except odometer settle.
- **Odometer**: every stat counts up 900ms, settles at 1.04×, mono tabular.
- **Nominal activation ("read it → light it")**: when narration names a thing,
  the matching visual ignites (helix for DNA, peaks for proteins, ripple for
  signals). Trigger at the word's proportional offset within the line. This is
  the single highest-impact device in an opening film.
- **Noise→Clean sweep**: during a "problem" line, traces glitch (seeded sine
  jitter); a FOCUS-colored pulse then sweeps L→R and the trace behind it renders
  clean and bright. Metaphor made motion.
- **The travelling pulse**: chains/routes light node-by-node under a glowing dot
  (sage) travelling between them; decision/end nodes stay hollow with a lock
  badge (`HUMAN JUDGMENT`, `CONTINUOUS AUDITING`).
- **Signal wipe**: 400–500ms vertical scanline L→R at every chapter boundary.
- **Pen underline**: key claims draw a FOCUS underline (`scaleX 0→1`).
- **Lens magnifier**: a circular 2.4–3× lens (border + soft shadow, background
  = the figure image scaled/offset) sweeps the decisive region of a reproduced
  figure while narration explains it.
- **Damped spring chips**: pills/status capsules pop with slight overshoot.

---

## 6. Captions (the subtitle system)

- **No boxes.** Plain text on canvas: upcoming words at 30% ink, spoken words
  transition to 100% espresso; **keywords** (domain terms: DNA, AI, evidence…)
  turn FOCUS accent. Shadow `0 1px 10px rgba(canvas,.95)` for lift.
- **Word timing**: character-proportional within the line
  `word_at = line.off + line.dur × chars_before/total`. Good enough to feel
  synced; no forced alignment needed.
- **Position**: bottom-center 28px (max-width 1460px). On dense scenes (cases
  with corner metrics), switch to **top mode**: `top:22px`, wider (1600px).
  Never center-popup; never over the focal card.
- Language consistency: VO, captions, and on-screen text all in ONE language
  decided upfront (the group's presentation language).

---

## 7. Cover Choreography (The Title Film, 45–60s)

A cover is a 4-act short film keyed to the intro narration — never a static
card, never a center caption popup:

1. **Converge (0–10s)**: faint alphabet/data motes drift and converge; a
   **semi-transparent artifact plate** (white @ ~66%) fades in and floats up.
2. **Settle (10s→)**: eyebrow kicker; **Title Case serif title**, word-by-word;
   subtitle in FOCUS italic serif; contributor **pills** (name · ID) stagger in
   — two rows max, equal geometry.
3. **Nominal activation**: as the intro narration names the domain objects,
   three labeled micro-instruments light up in sequence (e.g., helix / peaks /
   ripple). One per named noun.
4. **Complication & sweep**: a "problem" line makes the traces glitch; three
   question capsules pop with damped springs; a FOCUS pulse sweeps and cleans
   the traces; a small badge states the gap (`THE HOSPITAL GAP`). Slow push-in,
   signal wipe, out.

---

## 8. The Narration-First Production Pipeline (制作语言)

### 8.1 Architecture

```
narration.json ──► gen_tts.py ──► audio_lines/*.mp3
      │                                │
      └────────► build_timeline.py ────┴──► timeline.json + master_audio.wav
                    │                            │
                    ▼                            ▼
            renderer.html ──► inject_timeline.py ──► renderer_final.html
                                                          │
                                            capture.js (+ capture_resume.js)
                                                          ▼
                                              frames/*.jpg ──► encode.sh ──► MP4
                                            synth_mix.py ──► master_mix.wav ─┘
```

- **timeline.json is the single source of truth**: chapter starts/ends, and
  every line's `off`/`dur` (measured with ffprobe). Scene beats, captions, and
  audio assembly all derive from it. **Never hardcode seconds in scenes** —
  beats are `L(chap,lineIdx)` and `LD(chap,lineIdx)`.
- Renderer: single-file HTML, fixed 1920×1080 stage, one `render(t)` that is a
  pure function of time; a `SCENES` registry (`{id, a, b, tick}`); canvases are
  sized once and cleared per frame; all randomness via seeded PRNG.
- `?render=1` exposes `window.SEEK(t)` + `window.READY` (fonts+images loaded)
  and disables autoplay.

### 8.2 Rules

- **Per-line TTS** in the established voice & rate (reuse whatever the team has
  used before); new chapters get *targeted* synthesis of only the new lines.
- **Chapter lead/tail** padding (1.2s / 1.4s; final chapter tail 6s for the
  credits card) lives in narration.json, not in scenes.
- **Audio master** assembled sample-exactly in Python: VO + BGM (user-supplied
  mp3, tiled with 6s crossfades, gain ≈ −21 to −26 dBFS relative to VO, fade in
  3s / fade out 9s) + procedural SFX (whoosh on chapter starts, stamp/ticks on
  warnings). Verify continuity with RMS probes at 4 timestamps.
- **Audio-only change ⇒ remux, never re-render**:
  `ffmpeg -i video.mp4 -i master_mix.wav -map 0:v -map 1:a -c:v copy -c:a aac`.
- **BGM tiling**: advance the timeline cursor by (trackLen − crossfade); fade
  each copy's head/tail; verify with RMS probes (a source-cursor loop silently
  plays the track exactly once — classic bug).
- **Cost model** (1080p30): capture ≈ 18–20 min per 21–22k frames; encode ≈ 2
  min; audio remix ≈ 1 min; remux ≈ seconds. Budget feedback rounds around
  this; batch visual changes, then render once.

### 8.3 File manifest

```
video_build/
├─ narration.json          # chapters → lines (verbatim VO), voice, rate, gaps
├─ gen_tts.py              # per-line edge-tts synth → audio_lines/
├─ build_timeline.py       # durations → timeline.json + master_audio.wav
├─ synth_mix.py            # BGM tile + SFX + VO → master_mix.wav
├─ renderer.html           # the film as code (templates + scenes + HUD)
├─ inject_timeline.py      # renderer.html + timeline.json → renderer_final.html
├─ capture.js              # Playwright: SEEK(f/fps) → JPEG per frame
├─ capture_resume.js       # resume from a frame index after a crash
├─ encode.sh               # ffmpeg frames+audio → MP4 (faststart)
└─ assets/                 # figures/images (trimmed, credited)
```

---

## 9. Verify-Before-Render (The Iteration Protocol)

1. **Still-frame review**: `SEEK(t)` screenshots at every beat timestamp before
   any full render. Five-point checklist per still: null references (pageerror),
   element collisions, out-of-frame overflow, parent-opacity gates, HUD values.
2. **Batch edits in Python with `assert old in s`** and a single atomic write —
   a failed assert is a clean no-op. **Anchors drift**: re-grep the file before
   each batch; `s.index()` failures are your friend (atomic), silent partial
   writes are not.
3. **Slice-replacement hazard**: replacing `[anchorA, anchorB)` swallows
   everything between — anchor B must be the *next function you intend to
   keep*, and re-list all scene sections afterwards to confirm none vanished
   (count `id="sc-` occurrences).
4. **Transform overwrites**: helper `popIn()` writes `translateY` — chips that
   need horizontal centering must anchor with `right:`/`left:` + margin, not a
   style-attribute transform that gets clobbered every frame.
5. **Parent gates**: a parent stuck at `opacity:0` makes child opacity moot —
   set the parent (container) in the tick, or drop the parent's inline zero.
6. **Crash protocol**: Chromium can die around ~20k screenshots (memory). The
   frames directory is the checkpoint: verify `count == ceil(TOTAL×fps)`, then
   `capture_resume.js <firstMissingFrame>`. Never restart a full capture for a
   tail crash (17 min → 2 min).
7. **Never ship a render you have not spot-checked** at: cover, one case phase
   A, one phase C, densest scene, credits.

---

## 10. Data & Citation Integrity

- **Every number on screen traces to the user's own corpus** (their literature
  folder: `pdftotext -f 1 -l 1` for titles/authors, `pdfinfo` for metadata) or
  their deck. **Never invent a metric** — including "improvement" numbers from
  review notes; if a review suggests an unverified stat, replace it with a
  figure-embedded verifiable value (e.g., the `0.95` likelihood printed in the
  reproduced figure).
- Reproduced figures: crop white margins (content-bbox trim), show large,
  credit line inside the panel (`Reproduced from … (Fig. X)`), lens-probe the
  decisive region, and prefer **numbers printed in the figure** for callouts.
- References wall: full NLM-style entries (authors, full title, journal,
  year;vol(issue):pages, DOI), grouped by theme, **static and readable for
  8–10s** (two columns, no scroll blur, no gradient masks). A separate
  citations document ships with the deliverable.
- Credits: CRediT-style — **activity line on top, contributor name + ID below**,
  equal geometry for everyone, no hierarchy labels ("lead"), no name-hanging in
  scene corners; the final dossier card holds 6+ seconds.

---

## 11. Sound Design

- VO per line (48 kHz), music bed tiled at **−21 to −26 dBFS** relative to VO
  (user-tunable; "a bit louder" = +1.5–2 dB steps), duck −3 dB under stats.
- SFX palette: soft tick (odometer), air whoosh (chapter wipe), stamp thud
  (warning lock), pen scratch (underline). Procedural synthesis is fine; keep
  gains ≤ 0.2 relative to VO.
- Final chapter: music fades over 9s into a quiet tail so the credits card
  reads in near-silence.

---

## 12. Starting a New Topic (Generalization Checklist)

1. **Corpus first**: collect the user's papers/decks; verify titles, authors,
   DOIs, and the numbers you will animate.
2. **Narration**: reuse or write the script; split into lines; pick voice/rate;
   every line gets a visual event (Visual-First Rule).
3. **Pick domain recipe** (§2.2) and the five archetypes per chapter (§3).
4. **Gather assets**: reproduce figures, crop, credit; schematic canvas plans
   for Shot A of each case.
5. **Scaffold** the pipeline (§8.3), set tokens (§2.1), then implement chapters
   in order — verifying stills at beats as you go (§9.1).
6. **Render**: full capture → encode → QA (loudness/silence/freeze/stills) →
   deliver MP4 + citations document + the editable project.
