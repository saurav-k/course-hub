# 0160 A statistic is a random variable

| | |
|---|---|
| Module | M09 Estimation, testing, and inference |
| Rung | `pill med` |
| Class | core |
| Word budget | 1,000 to 1,300 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S03 |

## One tight idea

The number you computed is one draw from a distribution of numbers you could have computed, and that distribution is what the rest of the module reasons about.

## Prerequisites

`0022` for the mean, `0027` for how units get chosen. M07 for random variables, M08 for the expectation operator and for the Central Limit Theorem, which this page quotes and does not prove.

## Downstream

Everything. `0161` measures this distribution's centre and width, `0166` puts a ruler on it, and every test in the module is a statement about it.

## Boundaries: what this page must not teach

- **Not the CLT.** M08 owns the statement and the picture. This page uses it in one sentence and links out.
- **Not intervals.** `0166` owns them. This page stops at the standard error.
- **Not the bootstrap.** Name it once as the onward road for statistics with no closed form, then stop.
- The word "sampling" here means drawing from a distribution. `0027` used it for survey design. Say so, because the reader met the other meaning seven pages ago.

## Beats, in order

1. Two analysts run the same experiment on different weeks and report different numbers. Neither made a mistake. That is the whole page in one observation.
2. The reframe: `p` against `p_hat`, `mu` against `xbar`. The hat marks a number computed from data; the bare symbol is the thing you never see.
3. **The sampling distribution**, defined constructively: re-run the whole procedure a thousand times, histogram the answers. That histogram is the object.
4. Its centre and its width, derived rather than asserted, for the sample mean and then for a proportion. Both proofs are short and both are on the page.
5. **The standard error is not the standard deviation.** One describes the data, one describes the estimate, and they differ by `sqrt(n)`. This is the beat the page exists for and it gets a `.callout.warn`.
6. The square root as economics: four times the data buys half the error, a hundred times buys a tenth. Say what that means for an experiment budget before M09 spends one.
7. One sentence handing the bell shape to M08's CLT, and one naming what happens when `n` is small, which `0166` picks up.

## Named theorem and its stated proof (D4)

**Theorem.** For independent draws `X_1..X_n` with mean `mu` and variance `sigma^2`, the sample mean satisfies `E[Xbar] = mu` and `Var(Xbar) = sigma^2 / n`.

**Proof.** Expectation is linear, so `E[Xbar] = (1/n) sum_i E[X_i] = (1/n)(n mu) = mu`. For the variance, scaling pulls out as a square and independence makes variances add: `Var(Xbar) = (1/n^2) Var(sum_i X_i) = (1/n^2) sum_i Var(X_i) = (1/n^2)(n sigma^2) = sigma^2/n`. []

**Corollary, for a proportion.** A proportion is a sample mean of 0/1 draws, so with `X_i` Bernoulli(`p`), `E[p_hat] = p` and `Var(p_hat) = p(1-p)/n`, using `E[X^2] = E[X] = p` because `X` only takes the values 0 and 1.

**The honest boundary.** Independence is doing real work in the variance, and nothing in the mean. Correlated observations leave `Xbar` unbiased and make `sigma^2/n` wrong, usually too small. Say this: it is why a repeated-measures dataset with 10,000 rows can carry less information than 200 independent ones.

## Figures

- **Orientation**, `flowchart`: *a column and a design (`0022`, `0027`)* -> **THIS PAGE: the statistic is itself random** -> *`0161` bias and variance, `0166` intervals* -> *(dotted) M08's CLT*.
- **`svg.chart`**, required: a population histogram beside a histogram of 1,000 sample means drawn from it, on a shared axis, the second visibly narrower and more symmetric. Kills: "the sampling distribution is the data's distribution".
- **`svg.chart`**: standard error against `n`, the `sqrt` curve annotated at `n`, `4n` and `100n` with the error halving and then falling to a tenth.
- **`flowchart`**: population -> sample -> statistic -> distribution of the statistic, with the loop arrow labelled "re-run the whole procedure".

## Worked example

`sessions.csv`, column `session_seconds`, treated as the population so the truth is known. Resample at `n = 5, 25, 100, 400, 1600` and show the measured spread of the estimate sitting on `sigma/sqrt(n)` at every size. Then one sample of 400: its standard deviation is about 8.6 and its standard error about 0.43, and the two differ by exactly `sqrt(400) = 20`. Close on `returning` as a proportion, since that is the column the rest of the module tests.

## Quiz seeds

1. **Misconception.** A model scores 95.4 per cent on 50,000 held-out images. What does the standard error of that number describe? Answer: how much the score would move on a re-draw. Distractors must include "how much the images vary in difficulty", which is the standard deviation and is about 224 times larger here.
2. **Mechanism.** You quadruple the test set. The standard error falls to what fraction? Answer: a half. Distractors: a quarter (linear scaling), unchanged, three quarters.

## Practice seed

**Stem.** A classifier gets 47,700 of 50,000 right. Compute `p_hat`, the standard deviation of a single per-image 0/1 outcome, and the standard error of the accuracy, then show the first divided by the second is `sqrt(n)`.
**Hint.** A 0/1 outcome has variance `p(1-p)`; the accuracy is their mean.
**Solution path.** `p_hat = 0.954`; `sd = sqrt(0.954 x 0.046) = 0.2095`; `se = 0.2095/sqrt(50000) = 0.000937`, that is 0.094 percentage points; ratio `223.6 = sqrt(50000)`.
**`.p-check`.** The standard error must be far smaller than the standard deviation. If they are close, `n` was left out of the denominator, and the error bar you would draw is 224 times too wide.

## Code and dataset

`code/0160-a-statistic-is-a-random-variable.py` against `datasets/sessions.csv`, already on main from #57. It resamples the column, prints `E[xbar]`, the bias, the measured spread and the predicted `sigma/sqrt(n)` with their ratio, then repeats the whole table for the `returning` proportion. Reference it; do not rewrite it.

## Sources

- Wasserman, *All of Statistics*, chapter 6, for the sampling distribution and the standard error.
