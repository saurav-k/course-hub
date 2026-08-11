# 0001 - Quoting a deck whose arithmetic does not recompute

**Date:** 2026-08-11
**Status:** Accepted
**Applies to:** `lessons/0007-leading-indicators-and-correlation.html`

## Context

Slides 17 and 18 of Lecture 1 develop Pearson's correlation coefficient on a five-user table.
Slide 17 prints the table and the two cross-product sums.
Slide 18 divides each sum by a normalising constant and states two results.

The cross-product sums on slide 17 both reproduce exactly from the table:

- `sum of (x - x̄)(y - ȳ) = 18,550`
- `sum of (z - z̄)(y - ȳ) = -2,250`

The normalising constants on slide 18 do not.
Slide 18 writes `sqrt(300 × 1,125,000)` for the session-time correlation.
Recomputing the sums of squares from slide 17's own table gives `316` and `1,160,000`, not `300` and `1,125,000`.

Worse, the fraction slide 18 prints does not evaluate to the value slide 18 states:

- As printed: `18,550 / sqrt(300 × 1,125,000) = 1.010`, which is outside the range of a correlation coefficient.
- From the table: `18,550 / sqrt(316 × 1,160,000) = 0.969`.
- Stated on the slide: `0.71`.

The screen-brightness correlation is far less affected, because it is near zero either way:

- As printed: `-2,250 / sqrt(3,250 × 1,125,000) = -0.037`.
- From the table: `-2,250 / sqrt(2,950 × 1,160,000) = -0.038`.
- Stated on the slide: `-0.03`.

## The tension

Two rules in this repository pull in opposite directions here.

`AGENTS.md` says teaching materials must be grounded, and that a confident wrong explanation is worse than no lesson.
The course brief says every number must match the deck exactly, and names `r_XY ~ 0.71` among them.

Silently substituting `0.97` would break the brief and would also break the learner's ability to follow along with the lecture he is actually attending.
Silently printing `0.71` as though it fell out of the table would teach a number that a reader who does the arithmetic cannot reproduce, which is exactly the habit this course is trying to build against.

## Decision

Do all three, in this order, on the page:

1. **Quote the deck.** Print slide 18's fractions and its stated results, `0.71` and `-0.03`, exactly as the deck gives them, marked with `.keynum` so the reader can see they are quoted rather than derived.
2. **Show the arithmetic the table gives.** State the sums of squares that recompute from slide 17, `316` and `1,160,000`, and the values they produce.
3. **Name the difference in a `.callout.warn`,** and say what survives it: session time is strongly positively associated with spend and screen brightness is not, on every version of the arithmetic. The conclusion of the slide is safe. The intermediate constants are not.

Do not guess at which is intended, and do not correct the deck.
The page presents both and lets the reader see that the qualitative answer does not depend on the resolution.

## Why this and not something else

- **Not "just print 0.71".** A reader who does the multiplication gets a different number and concludes he has made a mistake. That is the single worst outcome for a course whose mission is that the reader never has to reconstruct a missing step.
- **Not "correct it to 0.97".** The learner is attending this lecture. A course that quietly disagrees with the deck in his hand costs him more than it saves, and the brief is explicit.
- **Not "leave the numbers out".** Correlation is the entire point of these three slides. Removing the arithmetic removes the lesson.
- **Not "raise it and stop".** The qualitative conclusion is unaffected, so the lecture is still teaching the right thing. This is a note to make, not a blocker to escalate.

## Cost of this decision

The page carries a paragraph that a smoother page would not.
That is the accepted trade, and it fits the course: noticing that a number does not reproduce, and saying so out loud, is the statistical habit this whole lecture is trying to install.

## Revisit when

The instructors publish corrected slides, or Lecture 8 (Variance, Covariance and Correlation) restates the same example.
If the constants change, update the page to the corrected deck and keep the honesty note only if it is still true.
