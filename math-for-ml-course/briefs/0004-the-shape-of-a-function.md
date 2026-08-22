# 0004 The shape of a function, and what a monotone change preserves

| | |
|---|---|
| Module | M01 Foundations |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,200 to 1,400 prose words, excluding practice and quiz text |
| Source scout | `mlm-foundations-r2` L4 |

## One tight idea

A strictly increasing transform can change every number on the page without changing a single decision that depends only on order.

## Prerequisites

`0003`.

## Downstream

`0005` (argmax), `0006`, and critically `0007`, whose entire legality argument is this page's theorem. Also M09's maximum-likelihood derivation, and M06, which needs "flat means slow".

## Boundaries: what this page must not teach

- **Not** the derivative. "Flat" and "steep" are read off a picture here; M05 owns the machinery.
- **Not** why saturation kills a gradient. Name the effect, hand the mechanism to M05.
- **Not** log space. `0007` owns the payoff; this page owns only the theorem that licenses it.

## Beats, in order

1. Six shapes with one line each on where each shows up: linear, quadratic, exponential, logarithmic, sigmoid, ReLU.
2. How to read a shape: where it is flat, where it is steep, where it saturates. This is a picture skill and M05 and M06 will lean on it.
3. Increasing, decreasing, monotone, strictly monotone. The word **strictly** is what rules out ties, and ties are exactly where the guarantee fails.
4. The theorem, stated in words before symbols: if `g` is strictly increasing then the place where `f` is largest is the place where `g(f)` is largest.
5. What that buys, twice: you may optimise `log L` instead of `L`, and you may rescale scores freely without touching a ranking metric.
6. What it does **not** buy. The **value** changes, so anything compared against a fixed threshold changes. Contrast a ranking metric with a thresholded one.
7. Saturation as a shape fact with a training consequence: flat tails mean a small signal. Name it, hand it to M05.
8. Close on the reading habit: before asking whether a transform is allowed, ask what the downstream decision depends on, the value or the order.

## Stated proof (D4)

**The monotone-argmax theorem.** Required by D4 and it is three lines, so there is no excuse for asserting it.

Assume `g` is strictly increasing and let `x*` be a maximiser of `f`. For any `x`, `f(x) <= f(x*)`. Apply `g`: because `g` is increasing, `g(f(x)) <= g(f(x*))`, so `x*` also maximises `g . f`.

**Name the step that does the work:** applying `g` to both sides of an inequality preserves its direction, and that is exactly what "increasing" means. **Name where strictness is needed:** without it `g` may be flat over an interval, and then a non-maximiser of `f` can tie, so the argmax **set** can grow. The maximum value never moves either way.

## Figures

- **Orientation**, `flowchart`: *a function is a contract (`0003`)* -> **THIS PAGE: its shape, and what a monotone change keeps** -> *`0007` may take logs, M09 may take log-likelihoods* -> *(dotted) M01*.
- **`svg.chart`**, required: `f` and `log f` drawn on one x-axis with their maxima marked by a shared vertical line, so the reader sees two different curves with the same argmax. This single figure is the page.
- **`svg.chart`**: the six shapes as a small-multiples row inside one `<figure>`, with the flat and steep regions annotated.

## Worked example

Four scores whose ordering is obvious. Apply `log`, then a linear rescale, then a squaring (which is **not** monotone on the reals). Tabulate value and rank at each step. The squaring is the one that breaks, and it breaks the rank only because a negative was present.

## Quiz seeds

1. **Misconception.** Taking logs of a loss changes the optimum. Distractors should include "yes, because the loss values all change", which is a true statement answering a different question: the values do change, the argmin does not.
2. **Mechanism.** Which of four transforms is safe on a metric that thresholds at 0.5?

## Practice seed

**Stem.** Given five model scores and a threshold of 0.5, apply a monotone rescale and report what happens to (a) the ranking, (b) the accuracy at that threshold.
**Hint.** Ask what each metric reads: an order or a value.
**Solution path.** Ranking unchanged by the theorem; accuracy changes because the threshold is fixed in value space and the transform moved the values across it.
**`.p-check`.** If your rescale changed the ranking, it was not monotone. Check it on the two closest scores first.

## Code and dataset

`code/0004-the-shape-of-a-function.py` against `datasets/sessions.csv`. Ranks 20,000 sessions by `spend`, applies `log1p`, and asserts the rank order is identical (Spearman correlation exactly 1.0) while the Pearson correlation and every value change. Then thresholds both at a fixed value and shows the counts differ.

## Sources

- A source for the ranking-against-threshold contrast, fetched and linked on the page.
