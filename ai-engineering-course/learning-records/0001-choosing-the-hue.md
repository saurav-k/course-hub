# Choosing the hue: 136

A learning record, not a published page. It exists so the next course does not repeat the measurement, and so a later reader can tell whether `136` was chosen or measured.

**Result: `:root[data-course="ai-engineering-course"] { --course-hue: 136; }`**

Mean chroma loss **6.8%**, worst cell **28.5%** (press, light), minimum contrast against `--surface` **5.10:1**, minimum against its own 14% tint `--course-soft` **4.12:1**, over seven palettes and both modes.

## The method, and why it is the method

The method is the one `staff-ai-course/learning-records/0001-choosing-the-hue.md` records and `ai-software-developer-course/learning-records/0001-choosing-the-hue.md` repeats.

A scratch harness links the real `assets/hub.css`, writes the candidate as an inline `--course-hue` on `<html>`, paints `var(--course-accent)` into an element, writes the computed colour into a canvas, and reads the pixel back through `getImageData`.
The inline property beats the `(0,2,0)` `:root[data-course=...]` blocks, so **`hub.css` was never edited to take a measurement**.
Reading the pixel back rather than the computed value is the whole point: hue rotation in OKLCH preserves lightness and chroma while the sRGB gamut is not a cylinder, so at some hues the browser clips and quietly changes what the reader sees. The canvas is what sees the clipping.

Chroma is computed in OKLab from that pixel; contrast is WCAG relative luminance.
**Seven palettes times two modes is fourteen cells per candidate**, and every figure below is over all fourteen.

The harness reuses `scripts/style_snapshot.py`'s `Chrome`, `find_chrome` and `serve_repository`, and `scripts/contrast.py`'s `contrast`, so it measures what CI measures rather than something adjacent to it.

## The harness reproduces both shipped records

Before it was asked anything new, it was asked to re-measure four hues that already ship:

| Course | hue | this run | the record it reproduces |
|---|---:|---|---|
| `staff-ai-course` | 212 | 8.7% mean / 45.0% worst / 5.73:1 / 4.62:1 | 8.5% / 45.0% / 5.74:1 / 4.62:1 |
| `gcp-course` and `go-course` | 200 | 11.3% / 45.8% / 5.45:1 / 4.39:1 | 11.2% / 45.8% / 5.45:1 / 4.39:1 |
| `coding-harness-course` | 150 | 7.7% / 37.6% / 4.99:1 / 4.04:1 | 7.6% / 37.6% / 5.00:1 / 4.04:1 |
| `math-for-ml-course` | 125 | 6.0% / 32.1% / 5.23:1 / 4.24:1 | 5.8% / 32.1% / 5.23:1 / 4.24:1 |

Worst cells and both contrasts agree exactly and the means differ in the first decimal, so the harness is measuring the same thing the two previous records measured.

## Which gap, and why

Twenty-one courses sat at nineteen distinct **absolute** angles when this was chosen, and read as absolute hue the 25-degree grid is full: 0 to 200 in steps of 25, then 225 through 335 written as negatives.
So a twenty-second course splits a gap rather than extending outwards, and the rule the three previous split records establish is that the gap is chosen **by adjacency of readership**.

**This course's reader interleaves with more of the hub than any previous course's.**
The courses they plausibly hold open beside a page here are `llm-papers` (0), `production-systems` (25), `llm-inference` (50), `agent-engineering` (75), `staff-ai` (212), `ai-software-developer` (238), `backend-engineering` (300) and `ai-system-design` (335).
That is eight courses spread right around the circle, and it rules out every free gap on the 0-to-100 arc and both gaps between 310 and 360.

The courses this reader has no reason to open beside it are `math-for-ml` (125), the four cloud courses, `go` (200), `probability-you-build` (260), `llm-evolution` (285) and `statistical-foundations-ml` (310).
`coding-harness` (150) is a weak case: it is harness internals at source level and this syllabus never opens a harness. `llm-efficiency` (175) is weak for the same reason: it is desk hardware and local models, and this syllabus uses hosted APIs throughout.

That leaves three honest candidates, and the measurement decides between them:

| Candidate | Gap it splits | mean chroma loss | worst cell | worst cell name | min vs surface | min vs tint |
|---|---|---:|---:|---|---:|---:|
| **136 - chosen** | math-for-ml (125) / coding-harness (150) | **6.8%** | **28.5%** | press/light | **5.10:1** | **4.12:1** |
| 162 | coding-harness (150) / llm-efficiency and aws (175) | 10.1% | 39.7% | press/light | 5.01:1 | 4.06:1 |
| 187 | llm-efficiency and aws (175) / gcp and go (200) | 12.6% | 52.8% | slate/light | 5.20:1 | 4.20:1 |

`187` has the best adjacency of the three and fails on chroma: 12.6% mean is worse than every hue in the hub and 52.8% in its worst cell is worse than anything shipped.
`ai-software-developer-course`'s record measured the same candidate at 188 and rejected it for the same reason, so rejecting it again is consistent rather than novel.
`162` is dominated by `136` on every measure and is no better on adjacency.

**From 136, the nearest strongly-interleaved course is `agent-engineering-course` at 61 degrees**, which is better separation from the pages that actually matter than either `staff-ai-course` (123 degrees, but with only cloud courses near it) or `ai-software-developer-course` (26 degrees) achieved.

## 136 rather than 137: the split point is measured, not halved

This is the one new finding in this record, and it is small.

The geometric midpoint of the 125-to-150 gap is 137.5. It is **not** the perceptual midpoint, because the seven palettes' accents sit at different base hues and sRGB clipping is not uniform around the circle.
Measuring the OKLab distance from each candidate to both neighbours over all fourteen cells, and taking the worse of the two:

| candidate | min distance to 125 | min distance to 150 | worse of the two |
|---:|---:|---:|---:|
| 134 | 0.0115 | 0.0179 | 0.0115 |
| 135 | 0.0136 | 0.0166 | 0.0136 |
| **136** | **0.0151** | **0.0136** | **0.0136** |
| 137 | 0.0170 | 0.0126 | 0.0126 |
| 138 | 0.0177 | 0.0103 | 0.0103 |
| 140 | 0.0200 | 0.0094 | 0.0094 |

**136 maximises the worse of the two**, and it sits 11 degrees from `math-for-ml` and 14 from `coding-harness` rather than 12 and 13.
The previous two split records halved their gap arithmetically. Halving is very slightly the wrong operation, and this is the record that says so.

## Is 0.0136 tight? Exactly as tight as what already ships

Nobody had previously measured what a 10-to-13-degree separation actually buys, so here is the comparison, minimum and mean OKLab distance over all fourteen cells:

| pair | degrees apart | min OKLab | mean OKLab | worst cell |
|---|---:|---:|---:|---|
| `azure` 250 / `probability-you-build` 260, the tightest shipped | 10 | 0.0141 | 0.0201 | harbor/light |
| `staff-ai` 212 / `gcp` and `go` 200 | 12 | 0.0153 | 0.0236 | harbor/light |
| `ai-software-developer` 238 / `oci` 225 | 13 | 0.0154 | 0.0247 | slate/light |
| **136 / `math-for-ml` 125** | **11** | **0.0151** | 0.0213 | harbor/light |
| **136 / `coding-harness` 150** | **14** | **0.0136** | 0.0259 | ink/light |

Both separations sit inside the band the three shipped tight pairs already occupy.
One cell is marginally tighter than anything shipped: 0.0136 against `coding-harness` in ink/light, 4% below the `azure` and `probability-you-build` floor.
That is worth stating plainly, and it is against the one neighbour this course's reader has least reason to hold open beside it.

**Against the courses that do matter, the separation is five to eleven times larger:**

| against | degrees | min | mean |
|---|---:|---:|---:|
| `agent-engineering-course` 75 | 61 | 0.0750 | 0.1079 |
| `staff-ai-course` 212 | 76 | 0.0901 | 0.1377 |
| `llm-inference-course` 50 | 86 | 0.1009 | 0.1476 |
| `ai-software-developer-course` 238 | 102 | 0.1148 | 0.1742 |
| `production-systems-course` 25 | 111 | 0.1221 | 0.1815 |
| `llm-papers-course` 0 | 136 | 0.1369 | 0.2065 |
| `ai-system-design-course` 335 | 161 | 0.1456 | 0.2177 |
| `backend-engineering-course` 300 | 164 | 0.1471 | 0.2136 |

The tightest of those, `agent-engineering-course`, is 5.5 times further away than the tightest neighbour.
That is what choosing the gap by readership buys, measured rather than argued.

## The full measurement for 136

| cell | chroma loss | vs `--surface` | vs `--course-soft` | painted rgb |
|---|---:|---:|---:|---|
| paper/light | 23.4% | 5.10:1 | 4.12:1 | rgb(0, 124, 85) |
| paper/dark | 0.0% | 8.81:1 | 6.81:1 | rgb(98, 198, 173) |
| slate/light | 12.8% | 8.35:1 | 6.41:1 | rgb(155, 23, 0) |
| slate/dark | 0.0% | 9.46:1 | 7.22:1 | rgb(241, 173, 131) |
| ink/light | 0.2% | 9.59:1 | 7.45:1 | rgb(129, 36, 7) |
| ink/dark | 0.0% | 10.74:1 | 8.21:1 | rgb(248, 178, 156) |
| sage/light | 0.0% | 8.14:1 | 6.52:1 | rgb(88, 68, 121) |
| sage/dark | 7.3% | 9.63:1 | 7.34:1 | rgb(201, 176, 255) |
| harbor/light | 0.3% | 8.14:1 | 6.49:1 | rgb(112, 63, 84) |
| harbor/dark | 0.3% | 9.06:1 | 7.05:1 | rgb(233, 161, 202) |
| aubergine/light | 21.7% | 7.13:1 | 5.74:1 | rgb(65, 95, 0) |
| aubergine/dark | 0.0% | 9.91:1 | 7.63:1 | rgb(179, 197, 116) |
| press/light | **28.5%** | 5.46:1 | 4.40:1 | rgb(0, 114, 84) |
| press/dark | 0.6% | 8.47:1 | 6.56:1 | rgb(83, 199, 176) |

## What the next course should take from this

1. **Compare a candidate against this table and the two earlier records**, not against the paragraph in `hub.css`, whose "worst of the 84 course accents" figures were measured when the hub had seven courses and were never re-run.
2. **Measure the split point rather than halving the gap.** It is one extra sweep and it moved this choice by one and a half degrees.
3. **Read the list as absolute hue.** A written offset of -175 and one of +175 differ by ten degrees of actual hue, which is how a full offset list collides once it wraps past 180.
