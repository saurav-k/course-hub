# M07-09 - PMF, PDF and CDF, and the relation between them

**Class:** core. **Rung:** working.

## The single tight idea

The CDF is the one description that always exists; the PMF and the PDF are what it looks like when it steps and when it slopes, and a density is not a probability.

## Prerequisites

| Page | What it supplies |
|---|---|
| M07-08 | random variables |
| M05, integrals | the definite integral, and the derivative as its inverse. **This is the hard scheduling edge: M05 must precede this page.** |

## Beats, in order

1. **Start with the CDF, not the PMF.** `F(c) = P{X <= c}`. It is defined for every random variable of either type, so it needs no case split, which is exactly why it goes first.
2. **The three properties that characterise it** (Hajek Proposition 3.1.5): nondecreasing, limits 0 and 1, right continuous. Show three candidate curves and ask which are legal.
3. **Discrete: the CDF is a staircase and the PMF is the jump.** Proof below. A PMF is non-negative and sums to 1.
4. **Continuous: the CDF is a ramp and the PDF is its slope.** `F(c)` is the integral of `f` up to `c`, and `f = F'` by the fundamental theorem of calculus. There are no jumps, so `P{X = v} = 0` for every single value, and therefore endpoints never matter.
5. **The heart of the page: a density is not a probability.** DLB states the condition exactly: "for all x, p(x) >= 0. Note that we do not require p(x) <= 1." Probability is **area**, never height. Prove it with a number the reader can hold: `Uniform(0, 0.5)` has density 2 everywhere on its support and its total area is still 1.
6. **The two pictures side by side**, so the relation is seen rather than asserted: a jump of height `p(k)` in the staircase, and a strip of area `f(u) du` under the ramp, are the same idea at two resolutions.
7. **The machine-learning section.** The quantile function is `F` inverse, which is why every sampler starts from `Uniform(0,1)` and pushes it through an inverse CDF. And `p99 latency` is a CDF statement: it is the `c` where `F(c) = 0.99`.

## Proof

**Named theorem: for any random variable, `P{X < c} = F(c-)` and `P{X = c} = F(c) - F(c-)`.**
In words: the probability sitting exactly on a point is the size of the CDF's jump there.

*Assumed:* only the axioms and the definition of the CDF.

*Shape:* build the event `{X < c}` as a countable union of disjoint pieces creeping up to `c`, apply axiom 2, and recognise the limit.

*Steps.* Take any increasing sequence `c1 < c2 < ...` with limit `c`. Let `G1 = {X <= c1}` and `Gj = {c(j-1) < X <= cj}` for `j >= 2`. These are mutually exclusive, and their union over all `j` is exactly `{X < c}`. Axiom 2 for a countable list gives `P{X < c}` as the sum of `P(Gj)`, and the partial sum to `n` telescopes to `P{X <= cn} = F(cn)`. Letting `n` grow gives `P{X < c} = F(c-)`. The second claim follows immediately: `P{X = c} = P{X <= c} - P{X < c} = F(c) - F(c-)`.

**The step that does the real work is the telescoping**, which is where countable additivity is spent. It is also why the CDF is defined with `<=` rather than `<`: that choice is what makes `F` right continuous and makes the jump land on the right side.

*Corollary the page uses immediately.* For a continuous-type random variable `F` has no jumps, so `P{X = v} = 0` for every `v`, and all four interval forms with and without endpoints are equal.

*Honest boundary.* Hajek's Proposition 3.1.5 says the three properties are not merely necessary but sufficient: any function with them is the CDF of some random variable. The forward direction is proved above. **The converse needs a construction that is beyond this course**, and the page says so plainly instead of gesturing.

## Planned figures

1. **Orientation, `flowchart LR`.** `M07-08 random variables` and `M05 integrals` feed `THIS PAGE - PMF, PDF, CDF`, which enables `every named distribution in the module`.
2. **`svg.chart` - the four panels.** Two by two. Top left, the `retries` PMF as bars at 0.8480, 0.1290, 0.0199, 0.0027; top right, its staircase CDF at 0.8480, 0.9770, 0.9969, 0.9996, with the jump at `k = 2` annotated as equal to the bar above it. Bottom left, the `latency_ms` density as a smooth curve; bottom right, its CDF, with one shaded area on the left matched to one vertical rise on the right.
3. **`svg.chart` - the density that is 2.** `Uniform(0, 0.5)` drawn to scale: a rectangle of height 2 and width 0.5, area shaded and labelled `area = 1`, height labelled `f(u) = 2`, with a `t-alarm` note reading "a density of 2, not a probability of 2".
4. **`flowchart LR` - the two loops.** `f(u)` to `F(c)` by integrating and back by differentiating; `p(k)` to `F(c)` by cumulative sum and back by taking the jump.

## The worked example, eight parts

1. **Setting.** The `retries` column of `requests.csv`, discrete, with all its mass on 1 to 8.
2. **Symbolic.** `F(c) = P{X <= c}` and `p(k) = F(k) - F(k-1)`, gloss naming `c` as any real number and `k` as an attainable value.
3. **Picture first.** Figure 2 above.
4. **`ol.worked`.** Read the PMF off the file: 0.8480, 0.1290, 0.0199, 0.0027. Accumulate: 0.8480, 0.9770, 0.9969, 0.9996. Now go back the other way: `F(2) - F(1) = 0.9770 - 0.8480 = 0.1290`, which is the PMF at 2. Then evaluate `F(1.5)`: it is 0.8480, because the CDF is flat between attainable values.
5. **`keynum`.** Proportions read from the file; every accumulation and difference derived here.
6. **Sanity check.** The CDF must reach exactly 1 at the largest attainable value, 8, and must never decrease. Both hold.
7. **What changes if.** Ask for `P{X < 2}` instead of `P{X <= 2}`. The answer drops from 0.9770 to 0.8480, a difference of 0.1290, which is precisely the mass sitting on 2. For `latency_ms` the same question changes nothing at all, because a continuous variable has no mass on any point.
8. **Interpretation.** Two descriptions, one object. Reach for the CDF when the question is "at most" or "at least", and for the PMF or PDF when the question is "what shape".

## Code and dataset

`code/M07-09-pmf-pdf-cdf.py` against `datasets/requests.csv`.

For `retries`, computes the PMF by counting and the CDF by cumulative sum, then recovers the PMF from the CDF by differencing and asserts it matches the original. For `latency_ms`, computes the empirical CDF two ways: once by sorting and taking rank over `n`, and once by counting rows at or below each of a grid of thresholds, asserting agreement. Prints `F(150)`, `F(180)`, `F(200)` and `F(300)` at 0.1360, 0.4807, 0.7414 and 0.9915, and the 0.99 quantile at 283.93, so the page can quote them.

## Quiz seeds

1. **Misconception.** A published initialiser draws weights uniformly on plus or minus 0.0766. What is the height of its density? *Correct:* 6.532, which is fine because probability is area. *Distractors:* 0.0766, because that is the range; 1, because a density cannot exceed 1; 0.1531, because that is the width.
2. Which CDF property does a curve that jumps downward violate? *Correct:* nondecreasing.

## Practice seed

**Stem.** For `retries`, `F(1) = 0.8480` and `F(3) = 0.9969`. Find `P{2 <= X <= 3}` and `P{X > 3}`. Then say why the first answer would be written differently for a continuous variable.
**Hint.** Both are differences of CDF values. For the first, be careful which endpoint is included.
**Solution.** `P{2 <= X <= 3} = F(3) - F(1) = 0.9969 - 0.8480 = 0.1489`. `P{X > 3} = 1 - F(3) = 0.0031`. For a continuous variable there is no mass on 2, so the `2 <=` and `2 <` versions are the same number and `F(2) - F(1)` would be irrelevant.
**`.p-check`.** The two answers plus `F(1)` must total 1: `0.8480 + 0.1489 + 0.0031 = 1.0000`. If they do not, an endpoint was included twice or dropped.

## Sources

- Hajek, ECE 313, sections 3.1 and 3.2: Propositions 3.1.2 and 3.1.5, Definition 3.2.1.
- Goodfellow, Bengio, Courville, *Deep Learning*, ch 3.3.1 and 3.3.2.
