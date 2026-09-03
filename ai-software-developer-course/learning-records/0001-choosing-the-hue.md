# Learning record - choosing the course hue

Not published. This records the measurement behind `:root[data-course="ai-software-developer-course"] { --course-hue: -122; }`
in `assets/hub.css`, so the next person adding a course does not repeat the reasoning.

It follows the method in [`staff-ai-course/learning-records/0001-choosing-the-hue.md`](../../staff-ai-course/learning-records/0001-choosing-the-hue.md), which is the file that made this cheap to repeat.
The measurement itself was run during the architecture audit for this course, on a clean worktree, against the real `assets/hub.css`.

## The state of the circle

Twenty courses were registered when this one was proposed, at **eighteen distinct absolute angles**.
Read as absolute hue - the only reading that matters, because `calc(h + offset)` is periodic - the 25-degree grid is full:

| Absolute | Written | Course |
|---:|---:|---|
| 0 | 0 | `llm-papers-course` |
| 25 | 25 | `production-systems-course` |
| 50 | 50 | `llm-inference-course` |
| 75 | 75 | `agent-engineering-course` |
| 100 | 100 | `herdr-course` |
| 125 | 125 | `math-for-ml-course` |
| 150 | 150 | `coding-harness-course` |
| 175 | 175 | `llm-efficiency-course` **and** `aws-course` - the recorded collision |
| 200 | 200 / -160 | `gcp-course` **and** `go-course` - an unrecorded collision, found by this audit |
| 212 | 212 | `staff-ai-course` |
| 225 | -135 | `oci-course` |
| 250 | -110 | `azure-course` |
| 260 | -100 | `probability-you-build-course` |
| 275 | -85 | `cloud-comparison-course` |
| 285 | -75 | `llm-evolution-course` |
| 300 | -60 | `backend-engineering-course` |
| 310 | -50 | `statistical-foundations-ml-course` |
| 335 | -25 | `ai-system-design-course` |

So this course splits a gap, exactly as `staff-ai-course` and `backend-engineering-course` did.
**The `go-course` / `gcp-course` collision at 200 is real and is not this course's to repair.** It is recorded here because the measurement found it; `_hue_problems()` in `scripts/validate_site.py` compares the written literal rather than the angle, which is why `-160` and `200` do not read as one hue to the checker.

## Which gap, and why

By adjacency of readership rather than by arithmetic, which is the rule the two previous split records established.

An AI-software-developer reader interleaves with eight courses: `llm-papers` (0), `production-systems` (25), `agent-engineering` (75), `herdr` (100), `coding-harness` (150), `staff-ai` (212), `llm-evolution` (285) and `ai-system-design` (335).
Every 25-degree gap on the low half of the circle sits between two of those, so the honest candidates all lie in the **200-to-260 arc**, where the immediate neighbours are cloud courses this reader is unlikely to hold open in the same hour.
That is the same trade `staff-ai-course` made, and it applies here more strongly rather than less, because this course's two nearest reader-siblings are `coding-harness-course` at 150 and `agent-engineering-course` at 75.

## The measurement

Method: a scratch page linking the real `assets/hub.css`; candidate offsets registered as scratch `data-course` blocks; `var(--course-accent)` painted into an element; the computed colour written into a canvas and the pixel read back through `getImageData`, so whatever Chrome clipped to sRGB is what is measured; chroma computed in OKLab from that pixel; contrast as WCAG relative luminance.
Seven palettes times two modes, headless Chrome. Six candidates were probed rather than two, so the recommendation is chosen against evidence rather than against arithmetic.
The scratch registrations were reverted and `validate_site.py` re-run green afterwards.

`minSurf` is the lowest contrast against `--surface` over all fourteen cells; `minTint` is against the accent's own 14% tint, `--course-soft`.

| Candidate | Written | Absolute | mean chroma loss | worst cell | worst cell name | minSurf | minTint |
|---|---:|---:|---:|---:|---|---:|---:|
| **A - chosen** | **-122** | **238** | **3.8%** | **25.8%** | aubergine/light | **6.08:1** | **4.97:1** |
| B | 237 | 237 | 4.0% | 25.8% | aubergine/light | 6.04:1 | 4.94:1 |
| C - second choice | -37 | 323 | 3.3% | 28.8% | ink/light | 6.37:1 | 5.13:1 |
| D | 12 | 12 | 0.8% | 5.8% | sage/light | 6.26:1 | 5.06:1 |
| E | 163 | 163 | 10.4% | 39.7% | press/light | 5.00:1 | 4.05:1 |
| F | 188 | 188 | 12.5% | **52.9%** | slate/light | 5.25:1 | 4.25:1 |
| G | -92 | 268 | 5.6% | **54.9%** | slate/light | 6.17:1 | 4.90:1 |

Against the shipped hues, measured in the same run:

| Shipped course | Written | mean chroma loss | worst cell | minSurf | minTint |
|---|---:|---:|---:|---:|---:|
| `staff-ai-course` | 212 | 8.5% | 45.0% | 5.74:1 | 4.62:1 |
| `gcp-course` | 200 | 11.2% | 45.8% | 5.45:1 | 4.39:1 |
| `go-course` | -160 | 11.2% | 45.8% | 5.45:1 | 4.39:1 |
| `oci-course` | -135 | 6.2% | 37.5% | 5.97:1 | 4.87:1 |
| `coding-harness-course` | 150 | 7.6% | 37.6% | 5.00:1 | 4.04:1 |
| `math-for-ml-course` | 125 | 5.8% | 32.1% | 5.23:1 | 4.24:1 |

**The harness reproduces the `staff-ai-course` record, which is the point of quoting both.**
That record reports staff-ai at 9.8% mean / 45.0% worst / 5.73:1 / 4.62:1; this run measures 8.5% / 45.0% / 5.74:1 / 4.62:1.
Worst cell and both contrasts agree to two decimals. The mean differs because `press` was added as a seventh palette after that record was written, and it is a low-loss cell for that hue.

## What was chosen

**`--course-hue: -122`**, absolute 238, splitting the 25-degree gap between `oci-course` (225) and `azure-course` (250).

- **Chroma.** 3.8% mean loss, 25.8% in its worst cell. Better than every hue in the comparison table, and less than half `gcp`'s worst cell. Comfortably inside the 0-to-8-percent-mean, up-to-55-percent-worst band `new-course.md` names as the bar.
- **Contrast.** 6.08:1 against the surface and 4.97:1 against its own tint, over all fourteen cells. Both clear WCAG AA at 4.5:1 and both beat `staff-ai-course`'s shipped 5.74 / 4.62.
- **Adjacency.** Nearest reader-sibling is `staff-ai-course` at 26 degrees. Immediate neighbours at 13 and 12 degrees are `oci-course` and `azure-course`.
- **What it looks like.** In `paper`/light it paints roughly `rgb(70, 89, 182)`, an indigo, distinguishable at a glance from `coding-harness-course`'s green and `agent-engineering-course`'s warm accent - the two pages this reader most often has open beside it.

## Rejected, so nobody re-proposes them

- **`-37`** (absolute 323) is marginally better on every number and loses on the check that matters: `ai-system-design-course` is 12 degrees away and is one of the eight courses this reader genuinely interleaves with. It is the second choice, and it would be right only if the best measured cell mattered more than the best separation.
- **`+12`** has the best chroma of anything measured, 0.8% mean, and sits 12 degrees from both `llm-papers` and `production-systems`, two sibling courses.
- **`+163`** and **`+188`** both fail on chroma against the shipped band, and `+188` sits between the two already-doubled slots at 175 and 200.
- **`-92`** looks fine on the mean and has the worst single cell of anything measured, 54.9% in `slate`/light.

## What the next course should do

Split a 25-degree gap, and pick which gap by adjacency of readership rather than by arithmetic.
Run the canvas readback and compare against the tables above rather than against the paragraph in `hub.css`, whose "worst of the 84 course accents" figures were measured when the hub had seven courses and have never been re-run.
