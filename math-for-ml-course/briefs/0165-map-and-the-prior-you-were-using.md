# 0165 MAP, and the prior you were already using

| | |
|---|---|
| Module | M09 Estimation, testing, and inference |
| Rung | `pill med` |
| Class | core |
| Word budget | 1,100 to 1,400 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S08 |

## One tight idea

Adding a penalty term to a loss is adding a prior, and which penalty you picked is which prior you assumed.

## Prerequisites

`0125` for Bayes' theorem, `0162` for the likelihood, `0164` for the Gaussian objective this page adds a term to, `0161` for the bias-variance trade the prior buys. `0110` for the L1 and L2 ball geometry, which M06 owns and this page does not redraw.

## Downstream

`0170` meets the same knob as a position on the complexity curve. `0173` places MAP and the MLE on the map of the two schools.

## Boundaries: what this page must not teach

- **Not the geometry.** M06's `0110` owns why the L1 ball's corner produces an exact zero. One sentence and a link, no picture of a diamond.
- **Not the full posterior.** `0173` owns credible intervals. This page stops at the mode.
- **Not empirical Bayes or hyperparameter tuning as a practice.** Name that `lambda` is chosen by validation and hand it to `0171`.
- Do not say "regularization is Bayesian inference". The correct sentence is narrower and the page must land it exactly.

## Beats, in order

1. Start from the reader's own code: `weight_decay=0.01` in an optimiser, which they have typed without being able to say what it assumes.
2. Take the log of Bayes' theorem. The evidence has no `theta` in it, so it drops out of the argmax and what is left is `log L(theta) + log p(theta)`. One line of algebra, and the whole page hangs off it.
3. **MLE is MAP with a flat prior**, said here, because it makes the two estimators one estimator with a knob.
4. Put a `Normal(0, tau^2)` prior on each weight. Its log is `-w^2/(2 tau^2)` plus a constant. Add it to `0164`'s objective and ridge falls out, with `lambda = sigma^2/tau^2`.
5. Swap the prior for a Laplace and the penalty becomes `|w|`. The lasso, with `lambda = sigma^2/b`.
6. **What `lambda` means now.** It is an exchange rate between the data and the belief, and a bigger `lambda` is a tighter prior. Show the fitted coefficients moving as `tau^2` shrinks.
7. **The limit the result carries**, in a `.callout.warn`. These are posterior **modes**. Ridge is also the posterior mean because a Gaussian posterior is symmetric; the lasso is not. The Laplace posterior is absolutely continuous, so `P(w_j = 0) = 0` and its mean has no exact zero in it. The sparsity belongs to the mode alone.
8. Tie to `0161`: a prior buys variance reduction with bias, which is the same trade with a different name.

## Named theorems and their stated proofs (D4)

**Theorem 1 (MAP is MLE plus a log-prior).** `argmax_theta p(theta | x) = argmax_theta [ log L(theta) + log p(theta) ]`.
**Proof.** By Bayes' theorem `p(theta | x) = p(x | theta) p(theta) / p(x)`. The logarithm is strictly increasing so it preserves the argmax, and `log p(x)` is an additive constant in `theta`, which cannot move a maximum. []

**Theorem 2 (L2 is a Gaussian prior).** With `y = Xw + e`, `e ~ Normal(0, sigma^2 I)` and independent `w_j ~ Normal(0, tau^2)`, the MAP estimate minimises `||y - Xw||^2 + lambda ||w||^2` with `lambda = sigma^2/tau^2`.
**Proof.** The log-prior of a `Normal(0, tau^2)` density is `-w_j^2/(2 tau^2)` plus a constant, so summing over `j` the MAP objective is `-(1/(2 sigma^2)) ||y - Xw||^2 - (1/(2 tau^2)) ||w||^2 + const`. Multiplying by `-2 sigma^2`, a positive constant, turns the argmax into an argmin and gives `||y - Xw||^2 + (sigma^2/tau^2) ||w||^2`. []

**Theorem 3 (L1 is a Laplace prior).** With the same likelihood and independent `w_j ~ Laplace(0, b)`, density `(1/(2b)) exp(-|w_j|/b)`, the MAP estimate is the lasso with `lambda = sigma^2/b`.
**Proof.** Identical substitution: the log-density contributes `-|w_j|/b`. []

**The honest boundary.** All three theorems are about the **mode** of the posterior, which is one summary among several. Ridge happens to coincide with the posterior mean; the lasso does not, and the difference is not cosmetic. So the defensible sentence is that these penalties are the log-densities of particular priors and the estimator is a particular summary of the resulting posterior. Anything stronger overstates it.

## Figures

- **Orientation**, `flowchart`: *the likelihood (`0162`, `0164`)* -> **THIS PAGE: add a log-prior** -> *`0170` the same knob as complexity, `0173` the two schools* -> *(dotted) M06's geometry*.
- **`svg.chart`**, required: likelihood, prior and posterior as three curves on one `theta` axis, the posterior mode sitting between the other two peaks and closer to the likelihood's. Kills: "the prior overrides the data" and its mirror.
- **`svg.chart`**: Gaussian and Laplace priors overlaid at matched scale, the Laplace's point at the origin shaded. Kills: why one shrinks and the other zeroes, without redrawing M06's ball.
- **`svg.chart`**: fitted coefficients against `lambda` on a log axis, the five real ones separating from the twenty-five null ones and all of them collapsing towards zero at the right.

## Worked example

`features.csv`, fitting on 60 rows so the problem is nearly as wide as it is tall and the prior has work to do. Ridge at `tau^2 = 1e6, 1, 0.25, 0.05`: the flat-prior row is the MLE and has fitted the noise columns hard, and the distance to the true coefficient vector falls and then rises again as the prior tightens. Then the lasso at four `lambda`, tabulating how many of the thirty coefficients are exactly zero and how many of the five real ones survive.

## Quiz seeds

1. **Misconception.** L2 regularization corresponds to which prior? Answer: a Gaussian centred at zero. Distractors: a Laplace centred at zero, which is L1; a uniform over the reals, which is no penalty at all and is the MLE.
2. **Mechanism.** You increase `lambda` in ridge. In prior terms, what did you do? Answer: narrowed the prior's spread. Distractor "widened it" must be present, since `lambda = sigma^2/tau^2` inverts the relationship and that is the trap.

## Practice seed

**Stem.** One weight `w`, Gaussian likelihood with `sigma^2 = 1`, a single observation putting the MLE at `4.0`, and a `Normal(0, tau^2)` prior. Write the MAP objective, show the solution is `w_MLE/(1 + lambda)` with `lambda = sigma^2/tau^2`, and evaluate at `tau^2 = 1`, `0.25` and `100`.
**Hint.** Differentiate `-(1/2)(w - 4)^2 - w^2/(2 tau^2)` and set it to zero.
**Solution path.** `-(w - 4) - w/tau^2 = 0`, so `w(1 + 1/tau^2) = 4` and `w = 4/(1 + lambda)`. At `tau^2 = 1`, `lambda = 1` and `w = 2.0`; at `0.25`, `lambda = 4` and `w = 0.8`; at `100`, `lambda = 0.01` and `w = 3.96`.
**`.p-check`.** As `tau^2` grows the answer must approach the MLE of 4.0, never exceed it, and never change sign. A prior centred at zero can only pull towards zero.

## Code and dataset

`code/0165-map-and-the-prior-you-were-using.py` against `datasets/features.csv`, already on main from #57. It prints the log-likelihood and log-prior separately at three prior widths so the exchange rate is visible, then both sweeps. Reference it; do not rewrite it.

## Sources

- Hastie, Tibshirani and Friedman, *ESL* 2nd edition, section 3.4.3, which states the lasso as the posterior mode under an independent double-exponential prior with `tau = 1/lambda`, and notes ridge is also the posterior mean while the lasso is not.
