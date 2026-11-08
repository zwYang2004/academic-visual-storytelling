---
name: science-storytelling
description: >-
  Write and humanize the words of scientific talks, explainer videos and
  academic reports. Two halves: (1) Bruce Kirchoff's storytelling laws for
  scientific presentations — state the finding in the title, use 'but' for
  dramatic effect, build the talk as repeated problems and solutions; and
  (2) a rigorous de-AI (humanize) checklist that removes LLM fingerprints —
  mechanical parallelism, dash insertions, hedging boilerplate, god-view
  declarations, banned buzzwords — replacing them with methodological
  trade-offs, insider-lab voice, concrete metrics and sentence burstiness.
  Standalone; pairs with the academic-visual-storytelling skill for
  explainer videos.
---

# Scientific Storytelling & De-AI Narration
> **Make a talk feel like a story a scientist actually lived — not a document a model generated.**

Use this skill whenever you *write or rewrite* narration, talk scripts,
abstracts, reports or on-screen claims. It is standalone; for explainer
videos it plugs into the narration.json step of the
academic-visual-storytelling pipeline (every rule here applies per line).

Source of the storytelling laws: Bruce Kirchoff, "How to tell a compelling
story in scientific presentations" (Nature 600, S88–S89, 2021), distilling
Presenting Science Concisely (CABI, 2021).

---

## 1. The Three Storytelling Laws

### Law 1 — State the finding in the title (and in the first 10 seconds)
- The best titles tell the audience **what you found and what it's good for**,
  with the direction of the effect included.
  - Good: *"Supply chain diversity buffers cities against food shocks"* —
    result + direction, in one line.
  - Weak: *"Effect of supply chain diversity on food shocks"* — topic only;
    the audience wonders whether the talk is a waste of time.
- Works for descriptive work too: *"A highly magnetized and rapidly rotating
  white dwarf as small as the Moon"* beats *"Use of the facility to search
  for short-period objects"*.
- **In a video**: the cover states the finding, not the topic; every chapter
  headline is a claim, not a label.

### Law 2 — 'But' is good; use it for dramatic effect
- A talk structured as *"we did X and Y and ran Z and found W and …"* is an
  and-list: mind-numbing, regardless of quality.
- One contradiction wakes the room up:
  **"X is the current state of knowledge, and we know Y. *But* Z problem
  remains. *Therefore*, we carried out ABC."**
- Contradictions introduce problems, tension and a reason to keep listening.

### Law 3 — Repeated problems and solutions build the story
String the whole talk as a but/therefore loop:

1. Present the first part of your results.
2. Introduce the problem that remains (but).
3. Solve it with more results (therefore).
4. Introduce the next problem.
5. Present results addressing it.
6–7. Continue the loop through the talk.
8. **End by restating the main finding** and how the intermediate results
   produce it.

Worked pattern (SARS-CoV-2 translation paper, Nature 594, 240–245, 2021):
infection reduces translation *but* viral transcripts are not preferentially
translated → how does viral mRNA dominate? *therefore* look at degradation →
translation of induced immune genes is impaired → what is the mechanism? →
nuclear mRNA export is inhibited. Final summary restates the multipronged
strategy. **In a video**: each chapter is one loop; the film's closing
statement restates the cover.

---

## 2. The De-AI Checklist (Humanize Pass)

Run this pass on every draft, line by line. An LLM draft fails most of these;
a human scientist's draft fails some.

### 2.1 Break mechanical symmetry
- Kill four-point alignment and tidy verb+object parallelism. Real academic
  prose weights by evidence: the important point gets a deep dive, minor
  findings are folded in or dropped.
- Ban scaffolding transitions: *first/second/third/finally*, *not only… but
  also*, *from the perspective of…*, 以及中文的"第一/第二/第三"、"不仅…而且…"、
  "从……维度来看"。

### 2.2 Root out AI punctuation & rhetorical boilerplate
- No double dashes (`--`/`——`) as insertions or explanations.
- No scare quotes around ordinary technical terms.
- No uplifting closers: "paves the way", "unlocks the potential", "opens new
  horizons", "shows great promise", "为未来铺平道路", "展现了无限潜力".
- A conclusion states the **current boundary, unresolved deviations, and the
  next actionable verification** — nothing more festive.

### 2.3 Insider voice: trade-offs, not declarations
- The AI fingerprint is announcing results ("the method is highly accurate and
  robust"). The researcher fingerprint is explaining the trade-off:
  *"Given the drop-out structure of single-cell data, we abandoned the
  fully-connected head for a sparsely regularized one with strong priors."*
- Write the concrete compromises, assumptions and取舍: batch effects,
  sequencing-depth bias, small-n variance, cold start, over-smoothing,
  gradient explosion, prior contamination, distribution shift, SNR limits —
  not "the data is heterogeneous, proceed with caution".

### 2.4 No over-defense, no false declarations
- Delete stacked-adverb hedges ("notably, while some limitations remain, this
  undoubtedly provides…").
- Replace vague defensiveness with named methodological trade-offs and their
  quantitative consequence.

### 2.5 Evidence texture & burstiness
- Vary sentence length and structure; break the smooth probability flow.
- Strengthen causal chains: name the data structure, the baseline, the control
  condition, the metric (AUROC, Pearson/Spearman, MSE, F1) instead of
  qualitative verdicts.
- Keep the tone sober and matter-of-fact; let the numbers carry the drama.

### 2.6 Banned vocabulary (replace with field-native terms)
- 中文: 画卷、基石、前沿、颠覆、维度、多层次、全方位、不谋而合、深远意义、
  赋能、抓手、闭环(非工程语境)。
- English: *paves the way, unlocks, delve into, showcase, robust and
  accurate, cutting-edge, in the ever-evolving landscape, holistic,
  multifaceted, groundbreaking*.
- Replace with the problem's own engineering vocabulary: distribution shift,
  SNR, prior contamination, cold start, over-smoothing, batch effect,
  homopolymer error, ancestry bias…

**Grep gate (run before shipping):**
```bash
grep -nEi "paves the way|unlocks|delve|cutting-edge|ever-evolving|groundbreaking|holistic|multifaceted" file.md
grep -nE "画卷|基石|前沿|颠覆|多层次|全方位|不谋而合|深远意义|赋能" file.md
grep -nE "——|--" file.md   # dash insertions (allow code/table syntax)
```
Every hit needs a human justification or a rewrite.

---

## 3. Using This Skill (standalone or with the video pipeline)

### 3.1 Writing order
1. Draft with Law 1: what is the finding sentence? If you cannot write it,
   the work is not finished.
2. Structure with Laws 2–3: list your results, then find the *but* between
   them; the talk becomes a chain of problems and solutions.
3. Run the De-AI pass (§2) on the whole draft.
4. Grep gate (§2.6) + read aloud: sentence lengths should be uneven; you
   should hear at least one *but* per chapter and zero banned words.

### 3.2 In the explainer-video pipeline (academic-visual-storytelling)
- **Chapter titles** = findings (Law 1). A chapter named "Methods" is a red
  flag; name the result.
- **Each chapter** = one problem→solution loop; the *but* lands as the
  limitation beat (the pen underline), the *therefore* as the next capability.
- **On-screen claims** are compressed ≠ statements ("Prediction ≠
  classification"); the narration carries the hedge and the trade-off.
- **Burstiness rule for VO**: alternate a long mechanistic sentence with a
  short verdict ("*It holds. 0.95 at the variant site.*") — TTS reads rhythm,
  and rhythm reads as human.
- Never let the De-AI pass weaken honesty: trade-offs must name real
  limitations with their quantitative consequence, not perform humility.

### 3.3 Two worked rewrites
- **AI version**: "This groundbreaking deep-learning approach paves the way
  for accurate and robust multi-cancer early detection."
- **Human version**: "The model found 67% of cancers overall — and 39% of
  stage I. Screening is not diagnosis: a positive result still needs imaging
  and tissue."
- **AI version**: "值得注意的是，尽管数据存在一定异质性，该方法依然展现出
  良好的鲁棒性，为后续研究奠定了基础。"
- **Human version**: "三个批次的批次效应使 AUROC 方差偏大；我们用
  ComBat 校正后重训，外部队列仍掉了 0.15——这部分差异没有解决。"

---

## 4. Quick Verification

1. **Contrarian scan**: does every chapter contain at least one real *but*?
2. **Title test**: does the title state a finding (with direction), not a topic?
3. **Banned-word grep**: zero hits, or each hit justified in writing.
4. **Burstiness read-aloud**: any 3 consecutive sentences of similar length?
   Rewrite one long, one short.
5. **Trade-off check**: for every "robust/accurate" claim, is there a named
   limitation with a number attached?
