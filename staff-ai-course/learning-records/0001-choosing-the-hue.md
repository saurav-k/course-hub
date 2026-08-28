# Learning record - choosing the course hue

Not published. This records the measurement behind `:root[data-course="staff-ai-course"] { --course-hue: 212; }`
in `assets/hub.css`, so the next person adding a course does not repeat the reasoning.

## The finding that changes the advice

**The 25-degree course-accent grid is full.** `new-course.md` still says to extend the grid outwards,
and `AGENTS.md` already warns to pick the offset on the circle rather than on the offset list. Those two
pieces of advice now collide, because reading the block as absolute hue shows the circle is populated at
every 25-degree step:

- 0 to +200 in steps of 25 - nine courses
- +225 (written -135) through +335 (written -25) - seven more

Sixteen courses cannot all sit 25 degrees apart on a 360-degree circle, and two pairs already ship closer
than that: azure at -110 and probability-you-build at -100 are 10 degrees apart in absolute hue.

The research report that proposed this course suggested "+225 or -160" as the next free steps. Both are
already taken: +225 is `oci-course` and -160 is 25 degrees from `gcp-course` at +200 in the wrong
direction. That is the exact wrap-past-180 collision `AGENTS.md` warns about, made by somebody who had
read the warning.

## What was chosen, and why

**+212**, splitting the 25-degree gap between `gcp-course` (+200) and `oci-course` (+225).

The gap was chosen by who the reader actually interleaves with rather than by which gap is widest. A
staff-ai reader moves between this course, `ai-system-design-course` (-25), `agent-engineering-course`
(+75), `llm-papers-course` (0), `llm-inference-course` (+50) and `production-systems-course` (+25).
From +212 the nearest of those is 123 degrees away. Its two close neighbours are cloud courses, which
this reader is unlikely to hold open in the same hour.

## The measurement

Canvas readback of the painted pixel, across all six palettes in both modes, on the course map page.
Chroma computed in OKLCH from the clipped sRGB value; contrast as WCAG relative luminance.

| Course | hue | mean chroma loss | worst cell | min contrast against surface | min contrast against its own 14% tint |
|---|---|---|---|---|---|
| **staff-ai-course** | **+212** | **9.8%** | **45.0%** | **5.73:1** | **4.62:1** |
| gcp-course | +200 | 12.1% | 45.8% | 5.45:1 | 4.39:1 |
| oci-course | -135 | 7.2% | 37.6% | 5.97:1 | 4.87:1 |
| math-for-ml-course | +125 | 5.4% | 32.1% | 5.23:1 | 4.24:1 |

The candidate sits inside the band of hues already published on every measure, which is the bar
`new-course.md` sets. Its worst cell is `sage/dark` for chroma and `paper/light` for contrast, the same
two cells as its neighbours.

**A stale sentence found while doing this.** `assets/hub.css` states that "the worst of the 84 course
accents sits at 5.06:1 against the surface it is painted on and 4.69:1 against its own 14% tint". Those
84 cells are six palettes times two modes times the original **seven** courses. Nine courses have been
added since and the sentence was not re-measured: `gcp-course` reads 4.39:1 and `math-for-ml-course`
4.24:1 against their own tints today. All of them still clear WCAG AA at 4.5:1 against the surface,
which is the claim that matters; the specific figures in that paragraph are historical.

## What the next course should do

Split a 25-degree gap, and pick which gap by adjacency of readership rather than by arithmetic. Run the
canvas readback above and compare against this table rather than against the paragraph in `hub.css`.
