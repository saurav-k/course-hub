# 0004 - The shape of a function, and what a monotone change preserves

| | |
|---|---|
| Module | M01 Foundations |
| Rung | foundation (`pill easy`) |
| Partition | core |
| Prose budget | 1,200 to 1,400 words |
| Prerequisites | `0003` |
| Needed by | `0005`, `0007` (its whole legality argument), M09 (MLE), M06 ("flat means slow") |
| Code | `code/0004-the-shape-of-a-function.py` |
| Dataset | `datasets/tickets.csv` |
| Named theorem | **the monotone-transform theorem.** Proved (D4). |

## The one idea

A strictly increasing transform can change every number on the page without changing a single decision that depends only on order.

## Beats, in order

1. Six shapes, one line each on where each shows up: linear, quadratic, exponential, logarithmic, sigmoid, ReLU.
2. How to read a shape: where it is flat, where it is steep, where it saturates. This is the picture skill M05 and M06 lean on.
3. Increasing, decreasing, monotone, strictly monotone. The word "strictly" rules out ties, and ties are exactly where the guarantee fails.
4. **The theorem**, stated in words before symbols, then proved.
5. What it buys, twice over: you may optimise `log L` instead of `L` (forward reference to `0007`), and you may rescale scores freely without touching a ranking metric.
6. What it does **not** buy. The **value** changes, so anything compared against a fixed threshold changes. Use Fawcett's contrast: AUC "shows the ability of the classifier to rank the positive instances relative to the negative instances", while "the accuracy metric imposes a threshold".
7. Saturation as a shape fact with a training consequence: a sigmoid's tails are flat, so a signal arriving there is small. Name the effect, hand the mechanism to M05, derive no derivative on a foundation page.
8. Close on the reading habit: before asking whether a transform is allowed, ask what the downstream decision depends on, the value or the order.

## The proof (D4)

**Theorem.** Let `f : X -> R` and let `g : R -> R` be strictly increasing on the image of `f`. Then `x` maximises `f` if and only if `x` maximises `g . f`; that is, `argmax f = argmax (g . f)` as sets.

*Proof.* Suppose `x*` maximises `f`, so `f(x) <= f(x*)` for every `x`. A strictly increasing `g` is in particular non-decreasing, so `g(f(x)) <= g(f(x*))` for every `x`, and `x*` maximises `g . f`.
Conversely suppose `x*` maximises `g . f` but not `f`, so there is some `x'` with `f(x') > f(x*)`. Because `g` is **strictly** increasing, `g(f(x')) > g(f(x*))`, contradicting that `x*` maximises `g . f`. Hence `x*` maximises `f`.

**The step that does the real work** is the converse, and it is the only place strictness is used. A merely non-decreasing `g` breaks it: take `g` constant, and every point maximises `g . f` while only some maximise `f`. That is why the page insists on the word "strictly", and it is why clipping, which is non-decreasing and not strictly increasing, is the transform that can move an `argmax`.

**Honest boundary.** The theorem says nothing about *how much* larger the maximum is, and nothing about the second-best point's gap. It preserves the location and discards the scale, which is exactly the trade `0007` wants and exactly why a thresholded metric is not protected.

## Figures (4, at least one `svg.chart`)

- **F1 orientation, `flowchart LR`.** "Functions, from 0003" to "THIS PAGE: what a monotone change preserves" to "log space (0007), MLE (M09), saturation (M05)".
- **F2 inline `svg.chart`.** Six small-multiple panels on shared axes: linear, quadratic, exponential, logarithmic, sigmoid, ReLU, each with a one-line ML caption. Kills: that every ML curve is bespoke.
- **F3 inline `svg.chart`, the page's centrepiece.** Left panel: six items on a score axis with a threshold line at 0.5. Right panel: the same six after `g(s) = s^2`, threshold still at 0.5. Connecting ribbons show the order is identical while items have crossed the line. Kills: "the transform does not change anything" and "the transform broke my model", both at once.
- **F4 `quadrantChart`.** Axes: depends on order against depends on value. Points `AUC`, `accuracy at 0.5`, `log loss`, `top-5 accuracy`. Keep every point label under 26 characters.

## Worked example (eight parts)

Six held-out items, three positive with scores `0.80, 0.60, 0.55` and three negative with `0.52, 0.30, 0.10`.
`g(s) = s^2` is strictly increasing on `[0,1]`, so the ordering is untouched.

| Metric | Before | After |
|---|---|---|
| AUC | 1.000 | 1.000 |
| Accuracy at a fixed 0.5 cutoff | 0.833 | 0.667 |
| Log loss | 0.421 | 0.514 |

The mechanism is the sentence the page exists for: the threshold stayed at 0.5, but the score that now maps to 0.5 is `sqrt(0.5) = 0.707`, so two items crossed the line while the ranking did not move.

- **Sanity check.** AUC of 1.000 means every positive outranks every negative; reading down the score column confirms it.
- **What changes if** the threshold travels with the transform, to `0.5^2 = 0.25`: accuracy returns to 0.833, which shows the defect was the fixed threshold and never the transform.

## Code

`code/0004-the-shape-of-a-function.py`.
Against the 1,308 test rows of `tickets.csv`: computes AUC and accuracy at a fixed 0.5 cutoff from `score_urgent`, applies `g(s) = s^2`, recomputes both, and **asserts AUC is unchanged to machine precision while accuracy is not**. Then transports the threshold to `0.25` and asserts the original accuracy is recovered exactly. AUC is computed twice, once from the rank definition and once by counting concordant pairs, and the two are asserted equal.

## Quizzes

- **Q1** (misconception): every score in `[0,1]` is squared. Which metric is guaranteed unchanged?
  `Accuracy at a fixed 0.5 cutoff` / `AUC, which depends on rank only` / `Log loss, which is scale-free` / `Precision at a fixed 0.5 cutoff`
  Feedback: options 1 and 4 both compare against a fixed number, and the number that now maps to 0.5 is 0.707; option 3 is false, and this page's own worked example moves log loss from 0.421 to 0.514.
- **Q2** (misconception): which transform can change which class an `argmax` picks?
  `Adding 3 to every one of the scores` / `Multiplying every score by 2` / `Clipping every score at 0.5` / `Taking the log of every score`
  Feedback: options 1, 2 and 4 are strictly increasing on the relevant domain and all preserve the order exactly; clipping is only **non-decreasing**, it creates ties at the cap, and a tie is precisely where the theorem's converse fails.

## Practice

Apply the logit `g(s) = ln(s / (1 - s))`, strictly increasing on `(0,1)`, to the six scores above.
(a) What are the six transformed scores? (b) Recompute AUC and accuracy at a fixed 0.5 cutoff, before and after. (c) A downstream system takes the top 3 by score. Does its output change?

- **Hint.** For (c), ask which of the two things the theorem preserves that ranking depends on.
- **Solution.** (a) `1.386, 0.406, 0.201, 0.080, -0.847, -2.197`. (b) the order is unchanged, so AUC is 1.000 both times; accuracy at 0.5 was `5/6 = 0.833` and after the transform only one item exceeds 0.5, giving `4/6 = 0.667`. (c) top-k reads the ordering and nothing else, so the same three items come out.
- **`.p-check`.** If your AUC moved, you re-sorted rather than transformed: a strictly increasing map cannot reorder anything.

## Primary source to go deeper

Fawcett, *An introduction to ROC analysis*, Pattern Recognition Letters 27 (2006), section 7.
