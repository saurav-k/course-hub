# M07-14 - The normal distribution and the Z-transform

**Class:** core. **Rung:** working.

## The single tight idea

The normal distribution is two parameters that mean exactly what you want them to mean, and it is the default not because data is normal but because of two theorems.

## Prerequisites

| Page | What it supplies |
|---|---|
| M07-09 | PDF, CDF, and density-is-not-probability |
| M07-08 | that a function of a random variable is a random variable, which the Z-transform is |
| M05, integrals | integrating, and the substitution the Z-transform performs |
| M01, exp | `e` to a negative square |

## Beats, in order

1. **The density**, with every symbol named in the gloss: `f(u) = (1 / sqrt(2 pi sigma^2)) exp(-(u - mu)^2 / (2 sigma^2))`.
2. **`mu` is location, `sigma` is scale.** Replacing `mu` by `mu + 3` slides the curve right by three; the width is proportional to `sigma`. The peak height is `1 / sqrt(2 pi sigma^2)`, so at `sigma` = 0.5, 1 and 2 the peaks are 0.7979, 0.3989 and 0.1995 - and **the area is 1 in all three cases**, which is M07-09's point returning with numbers.
3. **That the density integrates to 1** is not obvious and is proved below.
4. **The standard normal and the Z-transform.** `Z = (X - mu) / sigma` turns any normal into `N(0,1)`. Proved below. Its CDF is written `Phi` and its tail `Q`, with `Q(u) = 1 - Phi(u) = Phi(-u)`.
5. **68-95-99.7, to four figures**: 68.27, 95.45, 99.73 percent inside, and the numbers you actually use, 31.73, 4.55 and 0.27 percent outside.
6. **Why it is the default**, and both reasons hand off. The central limit theorem: the sum of many independent contributions is approximately normal. **M08 owns the theorem**; state it, draw it, link, do not prove it. Maximum entropy: of all distributions with a given variance, the normal carries the most uncertainty. **M10 owns entropy**; one sentence and a link.
7. **The precision parametrisation** `beta = 1 / sigma^2`, and the practical reason it exists: evaluating the density repeatedly means inverting `sigma` repeatedly.
8. **The machine-learning section.** He initialisation is a zero-mean Gaussian with standard deviation `sqrt(2 / n)`, where `n` is the number of incoming connections - a real, published, Gaussian initialiser, in contrast to Glorot's uniform one from M07-11. Gaussian noise is the mechanism in diffusion models and in differentially private training. Z-scoring a feature is this page's transform applied column-wise.
9. **The warning callout, which the module's own data earns.** Real serving quantities are often not normal. On `requests.csv`, `latency_ms` has 79.58 percent within one standard deviation against the 68.27 the normal predicts, and **227 rows above `mean + 3 sd` against the 34 the normal predicts, 6.7 times too many.** Restrict to the bulk under 300 ms and it is 69.49, 95.45 and 99.44 percent, almost exactly normal. **The default is useful and it lies about the tail**, and three-sigma alerting on a heavy-tailed metric is how a page like this earns its keep.

## Proof

**Named theorem 1: the normal density integrates to 1.**

*Assumed:* only the definition of the density and the tools of M05.

*Shape:* the one-dimensional integral has no elementary antiderivative, so square it, read the square as an integral over the plane, and change to polar coordinates where it becomes elementary.

*Steps.* It is enough to do the standard case `mu = 0`, `sigma = 1`; the general case follows from theorem 2 below. Let `I` be the integral of `e^(-u^2/2)` over the whole line. Then `I^2` is a double integral of `e^(-(x^2 + y^2)/2)` over the plane. **Switch to polar coordinates**, where `x^2 + y^2 = r^2` and the area element is `r dr d(theta)`. The integral becomes the integral over `theta` from 0 to `2 pi`, of the integral over `r` from 0 to infinity, of `e^(-r^2/2) r dr`. The inner integral is now elementary because the extra factor of `r` is exactly the derivative needed: substituting `w = r^2 / 2` turns it into the integral of `e^(-w) dw`, which is 1. So `I^2 = 2 pi`, giving `I = sqrt(2 pi)`, and dividing by it is precisely the `1 / sqrt(2 pi)` in the density.

**The step that does the real work is squaring the integral**, which is the move that has no motivation until you see where it lands. The `r` that appears in the polar area element is what makes the inner integral solvable, and without it the problem is exactly as hard as before.

**Named theorem 2: the Z-transform.** If `X` is `N(mu, sigma^2)` then `Z = (X - mu) / sigma` is `N(0, 1)`.

*Steps.* Work with the CDF, because that is where a transform is easy. `P(Z <= z) = P((X - mu)/sigma <= z) = P(X <= mu + sigma z)`, which is the normal CDF evaluated at `mu + sigma z`. Writing that as an integral of the density up to `mu + sigma z` and substituting `v = (u - mu) / sigma`, so `du = sigma dv`, the `sigma` in `du` cancels the `sigma` in the density's leading constant and the exponent becomes `-v^2 / 2`. What is left is the standard normal density integrated up to `z`.

**The step that does the real work is the substitution**, and the reason it works is that the normal family is closed under shifting and scaling. Not every family is: the same move on a lognormal does not return a lognormal in this way.

*Corollary.* One table serves every normal, which is why `Phi` is tabulated and nothing else is.

*Honest boundary.* The central limit theorem is why the normal is a good default and it is **not proved here**. M08 states and proves the case this course needs. Saying that plainly is better than a hand-wave, because a reader who thinks they have seen a proof of the CLT on this page has been misled.

## Planned figures

1. **Orientation, `flowchart LR`.** `M07-09 PDF` and `M05 integrals` feed `THIS PAGE - the normal and the Z-transform`, which enables `M08 the central limit theorem`, `M09 confidence intervals` and `weight initialisation`.
2. **`svg.chart` - three curves, one area.** Normals at `sigma` = 0.5, 1 and 2 sharing a mean, drawn to scale, peaks labelled 0.7979, 0.3989 and 0.1995, each shaded and each labelled `area = 1`.
3. **`svg.chart` - the three bands.** The standard normal with `f-prob` bands at 1, 2 and 3 sigma, labelled 68.27, 95.45 and 99.73 inside and 31.73, 4.55 and 0.27 in the tails.
4. **`svg.chart` - where the default fails, measured.** A histogram of the real `latency_ms` column as `m-stat` bars with the fitted normal drawn over it as an `s-prob` curve, the right tail beyond `mean + 3 sd` shaded `m-alarm`, and two counts printed in that region: **227 observed, 34 predicted**. This figure is the warning callout's evidence.

## The worked example, eight parts

1. **Setting.** The `latency_ms` column of `requests.csv`, restricted to the 24,788 rows under 300 ms, where the normal genuinely fits.
2. **Symbolic.** The density and the Z-transform together, gloss naming `mu`, `sigma`, `u` and `z`, and stating that `z` is a count of standard deviations and has no units.
3. **Picture first.** Figure 3 above.
4. **`ol.worked`.** Bulk mean `181.38` ms, bulk standard deviation `29.32` ms. Standardise a 240 ms request: `z = (240 - 181.38) / 29.32 = 2.00`. So a 240 ms request is two standard deviations slow, and the normal says about 2.28 percent of requests are at least that slow. Check against the file's bulk: within one sd, 69.49 percent against 68.27 predicted; within two, 95.45 against 95.45; within three, 99.44 against 99.73.
5. **`keynum`.** The 68.27, 95.45 and 99.73 figures are properties of the standard normal and are quoted; the mean, the standard deviation and every `z` are derived here.
6. **Sanity check.** A `z` of 2.00 must correspond to a tail near 2.3 percent, and standardising the mean itself must give exactly `z = 0`. Both hold.
7. **What changes if.** Put the 212 tail rows back in. The mean rises to 183.22 and the standard deviation to 37.18, so **the same 240 ms request now standardises to `z = 1.53` and looks unremarkable.** Two hundred rows in twenty-five thousand moved the yardstick, which is what a heavy tail does to a normal fit.
8. **Interpretation.** Fitting a normal to serving latency is defensible for the bulk and indefensible for the tail, and the two need different tools. A p99 read straight off the CDF is a fact; a p99 predicted from `mu + 2.33 sigma` is a normal assumption wearing a fact's clothes.

## Code and dataset

`code/M07-14-the-normal-distribution.py` against `datasets/requests.csv`.

Computes the standard normal CDF twice: once from the definition by numerically integrating the density on a fine grid with the trapezoid rule, and once with `math.erf` in closed form, asserting they agree to six decimals. That is the assertion that teaches, because the reader sees the area being added up. Then fits `mu` and `sigma` to `latency_ms` and to its sub-300 ms bulk, and prints the empirical against theoretical band occupancies for both, so the table in the warning callout is generated rather than typed. Prints the observed and predicted counts beyond three sigma, 227 against 34.

## Quiz seeds

1. **Misconception.** Two normals share a mean; one has `sigma = 0.5` and one has `sigma = 2`. Which carries more total probability? *Correct:* neither, both integrate to 1, and the peaks differ at 0.7979 against 0.1995. *Distractors:* the narrow one, its peak is higher; the wide one, it covers more ground; it depends on the mean.
2. Which of these is **not** one of the two stated reasons the normal is a good default? *Correct:* most real data is normally distributed. *Distractors:* the central limit theorem; it has maximum entropy at a fixed variance; it is closed under shifting and scaling.

## Practice seed

**Stem.** Using the bulk figures `mu = 181.38` ms and `sigma = 29.32` ms, find the `z` of a 150 ms request, the share of requests the normal says are faster than that, and the latency the normal puts at the 99th percentile. Then say why the last of the three is the least trustworthy.
**Hint.** `Phi(-1.07)` is about 0.142, and the 99th percentile sits at `z = 2.326`.
**Solution.** `z = (150 - 181.38) / 29.32 = -1.070`. `Phi(-1.070) = 0.1423`, so about 14.2 percent. The 99th percentile is `181.38 + 2.326 x 29.32 = 249.6` ms. It is the least trustworthy because it is a statement about the tail, the bulk fit excluded the tail by construction, and the full column's real 99th percentile is 283.93 ms - **34 ms higher than the normal predicts.**
**`.p-check`.** A negative `z` must give a share below 0.5, and the 99th percentile must exceed the mean by roughly two and a third standard deviations. If your percentile came out below the mean, the sign of `z` was dropped.

## Sources

- Hajek, ECE 313, section 3.6.2 and appendix 6.3.2.
- Goodfellow, Bengio, Courville, *Deep Learning*, ch 3.9.3, eqs 3.21 and 3.22, and the two stated reasons.
- He, Zhang, Ren and Sun, "Delving Deep into Rectifiers", 2015, eq 10. <https://arxiv.org/abs/1502.01852>
