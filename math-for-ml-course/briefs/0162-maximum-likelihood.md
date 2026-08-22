# 0162 Maximum likelihood: the parameter that makes your data least surprising

| | |
|---|---|
| Module | M09 Estimation, testing, and inference |
| Rung | `pill med` |
| Class | core |
| Word budget | 1,000 to 1,300 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S05 |

## One tight idea

Choose the parameter under which the data you actually saw was most probable, and take the logarithm because the product is unusable.

## Prerequisites

`0006` and `0007` for logs turning products into sums and for why ML lives in log space. `0128` for the PMF. `0124` for independence, which is what licenses the product. M05 for setting a derivative to zero.

## Downstream

`0163` and `0164` are this recipe applied. `0165` adds one term to it. M10's cross-entropy page depends on the equivalence `0164` derives.

## Boundaries: what this page must not teach

- **No distribution is fully derived here.** This page is the recipe and the reasoning; `0163` and `0164` are the derivations. If a derivation appears here the page has become two pages.
- **Not MAP.** The likelihood is not a distribution over the parameter, and this page says so loudly precisely so that `0165` can explain what turns it into one.
- **Not cross-entropy as an information quantity.** M10 owns that. `0164` owns the equivalence.
- Not asymptotic normality of the MLE, not the Cramer-Rao bound. Name them as the onward road in one sentence each.

## Beats, in order

1. Flip the conditional, in words: you know how to compute `P(data | theta)` for any candidate `theta`, so slide `theta` until that number is largest. No new machinery is needed and the reader already has all of it.
2. The likelihood defined, `L(theta) = prod_i f(x_i | theta)`, with independence named as the assumption that produces the product.
3. **What it is not**, immediately and in a `.callout.warn`: `L(theta)` is a density in the data read as a function of the parameter. It does not integrate to one over `theta` and it is not a probability that `theta` is anything.
4. The log-likelihood, and the theorem that the log does not move the argmax.
5. **Why the log is not merely convenient.** The raw product underflows to exactly zero at modest `n`, and once it is zero every candidate ties and the maximum cannot be located at all. Show the number.
6. The three-step recipe stated as a recipe: write the likelihood, take logs, maximise. Note that "maximise" is not always "differentiate", and hand that to `0163`.
7. One line forward: the same three steps produce every loss function the reader has used, which `0164` pays off.

## Named theorem and its stated proof (D4)

**Theorem.** If `g` is strictly increasing then `argmax_theta h(theta) = argmax_theta g(h(theta))`.

**Proof.** Suppose `h(a) >= h(b)` for all `b`. Since `g` is strictly increasing, `g(h(a)) >= g(h(b))` for all `b`, so `a` maximises `g o h` too. Running the argument with `g^-1`, which exists and is also strictly increasing, gives the converse. []

**Corollary.** The logarithm is strictly increasing on the positive reals and a likelihood is positive wherever it matters, so maximising `l(theta) = log L(theta)` is maximising `L(theta)`. Every derivation in this module therefore works with a sum rather than a product.

**The honest boundary.** The theorem is about the location of the maximum and nothing else. The *value* changes, the curvature changes, and the second derivative of the log-likelihood is a different object from that of the likelihood, which matters later because it is what the Fisher information is built from. Say that the log is free for the argmax and not free for everything.

## Figures

- **Orientation**, `flowchart`: *data plus a model family (M07)* -> **THIS PAGE: pick the parameter that makes the data least surprising** -> *`0163`, `0164` the derivations, `0165` add a prior*.
- **`svg.chart`**, required: the Bernoulli log-likelihood curve against `p` for a concrete count, with the peak dropped to the axis and annotated `k/n`. Kills: maximum likelihood as an abstraction rather than a curve with a top.
- **`svg.chart`**: the same curve drawn at `n = 10`, `n = 50`, `n = 200` at a fixed observed rate, each sharper than the last. Kills: "more data moves the estimate", when what it moves is the confidence.
- **`svg.chart`**: the raw likelihood against the log-likelihood as `n` grows, the first hitting the floor at zero and the second staying an ordinary number.

## Worked example

`sessions.csv`, column `returning`, 8,238 of 20,000. Tabulate the log-likelihood at five candidate `p` and show the peak at `k/n = 0.4119`. Then the underflow table: the raw product at 10, 50, 200, 700 and 2,000 observations, reaching exactly `0.0` by 2,000, beside the log-likelihood which is still an ordinary number. Close by integrating `L(p)` over `p` on a 40-row subsample to show the area is not one.

## Quiz seeds

1. **Misconception.** `L(theta)` is a function of `theta`. Is it a probability distribution over `theta`? Answer: no, it does not integrate to one. Distractors must include "yes, once it is normalised", with feedback naming what normalising actually requires, which is a prior.
2. **Mechanism.** Why take the log before maximising? Answer: it keeps the argmax and stops underflow. Distractors: it makes the answer more accurate; it makes the estimate unbiased.

## Practice seed

**Stem.** A model is evaluated on 10 held-out items and gets 7 right. Write the likelihood, write the log-likelihood, differentiate and solve for `p_hat`, then evaluate the log-likelihood at `0.5`, `0.7` and `0.9`.
**Hint.** The derivative of `k log p + (n-k) log(1-p)` is `k/p - (n-k)/(1-p)`.
**Solution path.** `L(p) = p^7 (1-p)^3`; `l(p) = 7 log p + 3 log(1-p)`; setting `7/p = 3/(1-p)` gives `7(1-p) = 3p`, so `p_hat = 0.7`; `l(0.5) = -6.931`, `l(0.7) = -6.108`, `l(0.9) = -7.650`.
**`.p-check`.** The middle value must be the largest of the three. If `l(0.9)` came out highest, the second term was dropped: a model that is right 7 times in 10 is not best explained by `p = 0.9`.

## Code and dataset

`code/0162-maximum-likelihood.py` against `datasets/sessions.csv`, already on main from #57. It carries an assertion that the argmax of the raw likelihood and of the log-likelihood agree on a subsample small enough for the product to survive, which is the theorem in executable form. Reference it; do not rewrite it.

## Sources

- Hastie, Tibshirani and Friedman, *ESL* 2nd edition, section 8.2.2, for the likelihood, the log-likelihood and the score.
