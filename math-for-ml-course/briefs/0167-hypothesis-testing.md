# 0167 Hypothesis testing: making the null do the work

| | |
|---|---|
| Module | M09 Estimation, testing, and inference |
| Rung | `pill med` |
| Class | core |
| Word budget | 1,100 to 1,400 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S10 |

## One tight idea

You cannot compute anything under "there is an effect", so you compute everything under "there is not" and ask how strange the data looks.

## Prerequisites

`0166` for the interval and the standard error, `0160` for the sampling distribution. M08 for the Central Limit Theorem.

## Downstream

`0168` catalogues what the p-value this page produces is not. `0169` runs the test in production. `0172` runs it on a slope.

## Boundaries: what this page must not teach

- **Not the misuse catalogue.** `0168` owns it. This page defines the p-value correctly once and moves on.
- **Not multiple comparisons, not peeking.** `0168` and `0169` respectively.
- **Not a menu of tests.** Name that `t`, chi-square and F exist for other shapes of question and derive exactly one, the two-proportion `z`, in full.
- **The word "accept" appears nowhere on this page** except inside the sentence that forbids it.

## Beats, in order

1. Why the null gets to be the null: it is the hypothesis you can compute under. "There is an effect" is a family with no single sampling distribution; "there is none" pins it down completely. That, and nothing more principled, is the reason.
2. The five steps, named and then walked once end to end on real counts.
3. **Pooled, and why.** The standard error is computed *under* `H0`, and `H0` says the two rates are equal, so the best estimate of the shared rate uses all the data. Using the two separate estimates answers a different question, and it is the same error as reading two overlapping intervals as a verdict.
4. The decision rule two ways, critical value and p-value, shown to be the same rule.
5. **The wording, in a `.callout.warn`.** When the test does not reject, the conclusion is "the data is compatible with `H0`", never "`H0` is true". A test never *accepts* the null. This is D16 and it is the load-bearing correction of the page.
6. Type I and Type II error, and the trade between them: lowering `alpha` lowers the false-positive rate and lowers the power with it. At fixed `n` the two move together and only more data buys both.
7. Power defined as `1 - beta`, and the question turned around: given the effect you care about, how much data do you need. Hand the arithmetic to `0169`.

## Named theorem and its stated proof (D4)

**Theorem (the pooled two-proportion test).** Under `H0: p_A = p_B = p`, with independent samples of sizes `n_A` and `n_B`, `Var(p_hat_A - p_hat_B) = p(1-p)(1/n_A + 1/n_B)`, so

  `Z = (p_hat_B - p_hat_A) / sqrt( p_pool(1-p_pool)(1/n_A + 1/n_B) )`,  `p_pool = (k_A + k_B)/(n_A + n_B)`,

is approximately standard normal for large samples.

**Proof.** Each proportion is a sample mean of Bernoulli draws, so by `0160` `Var(p_hat_A) = p(1-p)/n_A` and likewise for B. The two samples are independent, so the variance of the difference is the sum of the variances, which factorises as stated. Under `H0` both arms share one rate, so the efficient estimate of it pools the data. The normal approximation is the Central Limit Theorem applied to each arm. []

**The honest boundary.** "Approximately standard normal" is doing work, and it fails in the same regime `0166`'s coverage did: small `n`, or a rate near zero or one. The rule of thumb is that both arms should expect at least about ten successes and ten failures. Below that, use an exact test and say so; the page names Fisher's exact test in one sentence and does not derive it.

## Figures

- **Orientation**, `flowchart`: *intervals (`0166`)* -> **THIS PAGE: compute under the null and see how strange the data looks** -> *`0168` what the p-value is not, `0169` production, `0172` a slope*.
- **`svg.chart`**, required: the null sampling distribution with the observed statistic marked and both tail areas beyond it shaded. Kills: reading a p-value off the data rather than off the null.
- **`svg.chart`**: two overlapping densities, null and alternative, `alpha` shaded in one tail and `beta` in the other, power labelled as the remainder. Kills: "reduce both errors at once".
- **`stateDiagram-v2`**: the four decision states, reject/fail-to-reject crossed with `H0` true/false, transitions labelled `alpha` and `beta`. Kills: "fail to reject" and "accept" as the same state.

## Worked example

Two runs, deliberately. First, the counts the hub's sibling course *Statistical Foundations* works to two overlapping intervals on its lesson `0005`, saying the sharper tool is a two-proportion test: A `300/1,000`, B `340/1,000`. Do it. `p_pool = 0.320`, `SE = 0.020861`, `Z = 1.9174`, two-sided `p = 0.0552`. The overlap reading and the proper test agree on the verdict, and only the test says how close it was: a hair above 0.05, which is "not established", not "no difference". One-way cross-link to that course; it is a separate live course and nothing here edits it.

Second, `experiment.csv`: `596/12,000` against `643/12,000`, `p_pool = 0.05162`, `Z = 1.3711`, `p = 0.1703`, fail to reject. Then the sting the generator makes possible: the true rates are 0.0500 and 0.0560, so there *is* an effect and this test missed it. That is not a contradiction, it is what 54.6 per cent power means, and `0169` computes that number before the experiment rather than after.

## Quiz seeds

1. **Misconception.** `p = 0.31`, so you do not reject. What have you shown? Answer: the data is compatible with `H0`. Distractors must include "the null hypothesis is true", which is the D16 error, and "the effect size is very small", which confuses compatibility with magnitude.
2. **Mechanism.** At fixed `n` you lower `alpha` from 0.05 to 0.01. What happens to `beta`? Answer: it rises, so power falls. Distractor "it falls, so power rises" must be present.

## Practice seed

**Stem.** Group A: 300 clicks of 1,000. Group B: 340 of 1,000. State `H0` and `H1`, compute the pooled proportion, the standard error under `H0`, `Z`, and the two-sided p-value, then write the sentence you would send to a stakeholder.
**Hint.** Under `H0` the two arms share one rate, so the standard error uses the pooled estimate and not the two separate ones.
**Solution path.** `H0: p_A = p_B`; `p_pool = 640/2000 = 0.320`; `SE = sqrt(0.32 x 0.68 x (1/1000 + 1/1000)) = 0.020861`; `Z = 0.04/0.020861 = 1.9174`; `p = 0.0552`; fail to reject at 0.05.
**`.p-check`.** The pooled standard error must sit between the two separate ones, and the sentence must not contain the words "no difference". At `p = 0.055` the honest report is that the lift is not established and a larger sample is worth the traffic.

## Code and dataset

`code/0167-hypothesis-testing.py` against `datasets/experiment.csv`, already on main from #57. It walks both examples step by step, prints pooled against unpooled standard errors on the same counts, and measures the Type I rate and the power at three `alpha` levels. Reference it; do not rewrite it.

## Sources

- Greenland et al. (2016), *European Journal of Epidemiology* 31, 337-350, misinterpretation 6, for why a large p-value is not evidence of no effect. `https://pmc.ncbi.nlm.nih.gov/articles/PMC4877414/`
