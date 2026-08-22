# M07-11 - Uniform, continuous and discrete

**Class:** core. **Rung:** working.

## The single tight idea

The uniform distribution is the one where every value in a range is equally likely, and it is the distribution that proves a density is not a probability.

## Prerequisites

| Page | What it supplies |
|---|---|
| M07-09 | PMF, PDF, CDF, and the density-is-not-probability idea |
| M07-03 | equally likely outcomes, and that it is an assumption |
| M05, integrals | integrating a constant |

## Beats, in order

1. **Discrete uniform first**, because it needs no calculus. Over `k` states the PMF is `1/k` (DLB eq 3.1). Its CDF is a staircase of equal steps.
2. **Continuous uniform.** `f(u) = 1 / (b - a)` on `[a, b]` and 0 elsewhere. Every symbol named.
3. **The CDF is the ramp.** Proof below.
4. **Mean and variance**, as table entries with a forward link to M08: `(a + b) / 2` and `(b - a)^2 / 12`.
5. **The point of the page.** Make `b - a` smaller than 1 and the density exceeds 1. `Uniform(0, 0.5)` has density 2. Nothing is wrong: the area is still 1, because the rectangle got taller exactly as fast as it got narrower.
6. **The machine-learning section.** Glorot and Bengio's initialiser is **uniform**, not Gaussian - their equation 1 is `U[-1/sqrt(n), 1/sqrt(n)]` and their normalized initialisation, equation 16, is `U[-sqrt(6)/sqrt(n_in + n_out), +sqrt(6)/sqrt(n_in + n_out)]`. For a 512-to-512 layer that is plus or minus 0.07655, a density of 6.532 per unit. Also: `Uniform(0,1)` is the seed of every sampler through inverse-transform sampling, and a random train/test split is a discrete uniform over row orders.
7. **Where it is the wrong model, said plainly.** Uniform says the endpoints are as likely as the middle and that outside the range is impossible. Both are strong claims. M07-03 already showed what assuming uniform costs on this file's routes: an error of 79 percent on the most common one.

## Proof

**Named result: the CDF of `Uniform(a, b)` is the ramp `F(c) = (c - a) / (b - a)` on `[a, b]`, 0 below and 1 above.**

*Assumed:* `a < b`, and the density is the constant `1/(b-a)` on the interval.

*Shape:* the CDF is the integral of the density, and integrating a constant is multiplying by a width.

*Steps.* For `c` below `a` the density is 0 everywhere up to `c`, so the integral is 0. For `c` in `[a, b]`, the integral from minus infinity to `c` is the integral from `a` to `c` of the constant `1/(b-a)`, which is that constant times the width `c - a`, giving `(c - a)/(b - a)`. For `c` above `b` the whole rectangle is included and the integral is `(b - a)/(b - a) = 1`.

**The step that does the real work is that the density is constant**, which turns an integral into a multiplication. That is the entire reason this distribution is the one every course starts with.

*Corollary the page uses immediately.* Setting `F(c) = 1` at `c = b` is the check that the density had to be `1/(b-a)` and could not have been anything else: the height is forced by the requirement that the area is 1, which is why a narrow interval must have a tall density.

## Planned figures

1. **Orientation, `flowchart LR`.** `M07-09 PMF and PDF` and `M07-03 equally likely` feed `THIS PAGE - the uniform`, which enables `weight initialisation`, `inverse-transform sampling` and `the contrast every other distribution is read against`.
2. **`svg.chart` - the density that is 2.** `Uniform(0, 0.5)` to scale: height 2, width 0.5, area shaded, labelled `area = 1` and `f(u) = 2`, with a second faint rectangle for `Uniform(0, 4)` at height 0.25 beside it. Same area, wildly different heights.
3. **`svg.chart` - rectangle and ramp.** The density above its own CDF on a shared x-axis, with a vertical dropline at `c` showing the shaded area on the top panel equal to the height on the bottom panel.
4. **`svg.chart` - the real initialiser.** A histogram of 100,000 draws from Glorot's `U[-0.07655, 0.07655]` as `m-prob` bars with the flat theoretical density drawn over it as an `s-signal` line at 6.532, and the shaded slice for `P(|W| < 0.01) = 0.1306`.

## The worked example, eight parts

1. **Setting.** Glorot and Bengio's normalized initialisation for a 512-to-512 layer, which is a real published initialiser and genuinely uniform.
2. **Symbolic.** `f(w) = 1 / (2r)` on `[-r, r]` with `r = sqrt(6) / sqrt(n_in + n_out)`, gloss naming `r` as the half-width, `n_in` and `n_out` as the fan-in and fan-out.
3. **Picture first.** Figure 4 above.
4. **`ol.worked`.** `n_in + n_out = 1,024`. `sqrt(1,024) = 32`. `sqrt(6) = 2.4495`. `r = 2.4495 / 32 = 0.07655`. Width `2r = 0.15309`. Density `1 / 0.15309 = 6.532`. Then `P(|W| < 0.01) = 0.02 / 0.15309 = 0.1306`.
5. **`keynum`.** `sqrt(6)` and the formula are quoted from the paper; every division is derived here.
6. **Sanity check.** The density times the width must be 1: `6.532 x 0.15309 = 1.0000`. And `P(|W| < 0.01)` must be well under 1 because 0.02 is a small slice of 0.153.
7. **What changes if.** A 2,048-to-2,048 layer. `r` falls to `2.4495 / 64 = 0.03827` and the density doubles to 13.06. **Wider layers get smaller weights and a taller density**, and the area is 1 in both cases.
8. **Interpretation.** A published, widely used initialiser has a probability density of 6.5. If a density were a probability that number would be nonsense, and it is not: the probability of any single weight value is exactly zero.

## Code and dataset

`code/M07-11-the-uniform-distribution.py`, self-contained with no dataset load, because the object of study is an initialiser rather than a data column. It documents that exception in its docstring, as the BUILDER-SPEC requires when a program does not read `datasets/`.

Computes the Glorot bound from the formula, draws 200,000 weights with `default_rng`, then computes `P(|W| < 0.01)` twice: once from the definition as width-over-width, and once as the empirical fraction of draws, asserting they agree to three decimals. Prints the empirical density estimate from a histogram beside the exact 6.532. Also verifies the mean and variance against `(a+b)/2` and `(b-a)^2/12`.

## Quiz seeds

1. **Misconception.** A distribution has density 6.532 over an interval of width 0.153. What is wrong? *Correct:* nothing - the area is 1, and a density is not a probability. *Distractors:* the density must be at most 1; the width must exceed 1; the two must multiply to more than 1.
2. Glorot and Bengio's published initialiser draws weights from which distribution? *Correct:* uniform on a symmetric interval.

## Practice seed

**Stem.** A layer has 256 inputs and 1,024 outputs. Find Glorot's normalized bound, the density, and the probability that a weight lands in the middle tenth of the range.
**Hint.** The bound uses the **sum** of fan-in and fan-out. The middle tenth is a width, and for a uniform, probability is width over width.
**Solution.** `n_in + n_out = 1,280`; `sqrt(1,280) = 35.777`; `r = 2.4495 / 35.777 = 0.06847`; width `0.13693`; density `1 / 0.13693 = 7.303`. The middle tenth has width `0.013693`, so the probability is `0.1` exactly.
**`.p-check`.** The last answer must be exactly 0.1 without any arithmetic, because a uniform gives every equal-width slice equal probability. If your route to it needed the density at all, you did more work than the distribution required.

## Sources

- Hajek, ECE 313, section 3.3 and appendix 6.3.2.
- Goodfellow, Bengio, Courville, *Deep Learning*, ch 3.3.1 eq 3.1 and ch 3.3.2.
- Glorot and Bengio, "Understanding the difficulty of training deep feedforward neural networks", AISTATS 2010, eqs 1 and 16. <https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf>
