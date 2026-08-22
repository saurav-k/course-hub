# M07-12 - Waiting: the geometric distribution and memorylessness

**Class:** depth. **Rung:** working.

## The single tight idea

When you repeat a trial until it works, the number of trials is geometric, its mean is `1/p`, and it has no memory: the run so far tells you nothing about the run remaining.

## Prerequisites

| Page | What it supplies |
|---|---|
| M07-10 | Bernoulli trials |
| M07-05 | independence |
| M07-04 | conditional probability, which memorylessness is stated in |
| M01, geometric series | the sum that makes the PMF total 1 |

## Beats, in order

1. **Setup.** Independent Bernoulli(`p`) trials; `L` is the index of the first success. Walk the first three cases before generalising: `P(L=1) = p`, `P(L=2) = (1-p)p`, `P(L=3) = (1-p)^2 p`.
2. **The PMF**, proved below: `P(L = k) = (1-p)^(k-1) p` for `k >= 1`.
3. **The tail is cleaner than the PMF, and you should reach for it first.** `P(L > k) = (1-p)^k`, because `L` exceeds `k` exactly when the first `k` trials all failed. One line, and it makes every later step short.
4. **Mean `1/p`**, proved below by conditioning rather than by summing a series, because the conditioning argument is three lines and teaches M07-04 again.
5. **Variance `(1-p)/p^2`**, as a table entry with a forward link to M08. State Hajek's operational remark: when `p` is small the standard deviation is nearly as large as the mean, so **a mean wait is not a typical wait**.
6. **The mode is always 1.** The PMF's largest value is at `k = 1` for every `p`, because each successive term multiplies by `(1-p) < 1`. A distribution whose mean is 5 and whose single most likely value is 1 is worth sitting with.
7. **Memorylessness**, proved below. The gambler's fallacy is exactly the denial of this sentence.
8. **The convention trap.** Two definitions circulate: trials-until-success, support from 1, mean `1/p`, which is Hajek's and `scipy.stats.geom`'s; and failures-before-success, support from 0, mean `(1-p)/p`. On this module's data those two predict 1.1765 and 0.1765 for the same column. State which the course uses and check the library before trusting a number.
9. **The machine-learning section.** Rejection sampling: the expected draws until acceptance is one over the acceptance rate. Speculative decoding: under an i.i.d. acceptance assumption the tokens produced per iteration are, in the authors' own words, "a capped geometric variable, with success probability 1 - alpha and cap gamma + 1". Retry-until-success against a flaky upstream, which is exactly what the module's `retries` column is.

## Proof

**Named theorem 1: the geometric PMF.** `P(L = k) = (1-p)^(k-1) p` for `k >= 1`.

*Assumed:* the trials are independent and each succeeds with the same probability `p`, with `0 < p <= 1`.

*Shape:* the event is one specific sequence, so independence prices it directly.

*Steps.* `{L = k}` happens exactly when the first `k - 1` trials fail and the `k`th succeeds. That is one specific sequence of outcomes, not a set of them, so no counting is needed. By independence its probability is the product `(1-p)` taken `k-1` times, times `p`.

**The step that does the real work is that `{L = k}` is a single sequence.** Compare the binomial, where the same idea needed a coefficient because many sequences qualified. Here exactly one does, which is why the geometric has no binomial coefficient in it.

*That it sums to 1* is the geometric series: `sum over k>=1 of (1-p)^(k-1) p = p / (1 - (1-p)) = p / p = 1`.

**Named theorem 2: `E[L] = 1/p`.**

*Shape:* condition on the first trial, notice the problem repeats, and solve for the unknown.

*Steps.* With probability `p` the first trial succeeds and `L = 1`. With probability `1-p` it fails, one trial has been spent, and **the number of further trials needed has exactly the same distribution as `L` did at the start**, because the trials are independent and identical. So `E[L] = p x 1 + (1-p)(1 + E[L])`. Expanding: `E[L] = p + 1 - p + (1-p)E[L] = 1 + (1-p)E[L]`. Collecting, `p E[L] = 1`, so `E[L] = 1/p`.

**The step that does the real work is the bolded one**, and it is memorylessness used before it has been named. Everything else is algebra on one unknown.

*Honest note.* M08 owns expectation as an operator. This derivation treats `E[L]` as a single unknown number and never uses linearity, so it stands on its own, and M08's machinery makes it routine rather than replacing it.

**Named theorem 3: memorylessness.** `P(L > n + k | L > n) = P(L > k)`.

*Steps.* By the definition of conditional probability, the left side is `P(L > n+k and L > n) / P(L > n)`. But `L > n+k` already implies `L > n`, so the intersection is just `{L > n+k}`. Using the tail formula, that is `(1-p)^(n+k) / (1-p)^n = (1-p)^k`, which is `P(L > k)`.

**The step that does the real work is the containment**, which collapses the joint event to one of its two parts. After that it is cancelling powers.

*Converse, stated and not proved:* Hajek notes that any positive-integer random variable with this property is geometric for some `p`. The proof is a short induction and is left as a pointer.

## Planned figures

1. **Orientation, `flowchart LR`.** `M07-10 Bernoulli` and `M07-05 independence` feed `THIS PAGE - waiting and memorylessness`, which enables `the exponential`, `rejection sampling` and `retry budgets`.
2. **`stateDiagram-v2` - memorylessness, drawn.** Two states: `Trying` self-loops on "fail - probability 1 minus p", and goes to `Done` on "success - probability p". The caption's point is that the diagram has **nowhere to store how many failures have happened**, and that absence is the theorem.
3. **`svg.chart` - the PMF that peaks at 1.** Bars for `p = 0.85` at 0.8500, 0.1275, 0.0191, 0.0029, with the observed `retries` proportions 0.8480, 0.1290, 0.0199, 0.0027 overlaid as `m-stat` marks, a `ref` line at the mean 1.1765, and a `t-alarm` label on `k = 1` reading "the most likely wait is always one trial".
4. **`svg.chart` - memorylessness measured.** Three paired bars from the real column: `P(R > 2 | R > 1) = 0.15105` against `P(R > 1) = 0.15200`; the same pair for the arrival gaps at 0.10073 against 0.09928. The conditional and unconditional bars are the same height, which is the theorem observed rather than asserted.

## The worked example, eight parts

1. **Setting.** The `retries` column of `requests.csv`: attempts until an upstream call succeeded, generated with `p = 0.85`.
2. **Symbolic.** `P(L = k) = (1-p)^(k-1) p` and `P(L > k) = (1-p)^k`, gloss naming `L` as the trial index of the first success and `p` as the per-attempt success probability.
3. **Picture first.** Figure 3 above.
4. **`ol.worked`.** Theory at `p = 0.85`: `P(1) = 0.8500`, `P(2) = 0.15 x 0.85 = 0.1275`, `P(3) = 0.0225 x 0.85 = 0.0191`. Observed in the file: 0.8480, 0.1290, 0.0199. Mean: theory `1 / 0.85 = 1.1765`, observed `1.1786`. Tail: theory `P(L > 1) = 0.15`, observed 0.15200.
5. **`keynum`.** `p = 0.85` is quoted from the generator's docstring; every power and observed proportion is derived here.
6. **Sanity check.** The observed mean must exceed 1, because the support starts at 1. If it came out near 0.18 you used the other convention.
7. **What changes if.** Halve the success rate to `p = 0.425`. The mean doubles to 2.353 and the tail `P(L > 3)` rises from 0.0034 to 0.190, a factor of 56. **The mean scales gently and the tail does not**, which is why retry budgets are set from the tail.
8. **Interpretation.** 848 requests in 1,000 succeed first time and about 3 in 1,000 need four or more attempts. A retry budget of 3 covers 99.7 percent of traffic, and the 0.3 percent it does not cover is where a timeout policy earns its keep.

## Code and dataset

`code/M07-12-the-geometric-distribution.py` against `datasets/requests.csv`.

Computes the geometric PMF two ways: once from the definition as an explicit power times `p`, and once as the observed value counts of the `retries` column, printing them side by side. Asserts the fitted `1 / mean` recovers `p = 0.85` to two decimals. Then tests memorylessness directly on the column: computes `P(R > n + k | R > n)` for several `n` and `k` by filtering, and asserts each is within sampling tolerance of `P(R > k)`. Prints the tolerance it used and the count of rows behind each estimate, because the deep-tail estimates rest on very few rows and the program says so rather than pretending.

## Quiz seeds

1. **Misconception.** Trials succeed with probability 0.2. Which single number of trials is the most likely wait for the first success? *Correct:* one, even though the mean is five. *Distractors:* five, the mean; four, just below the mean; there is no single most likely value.
2. You have drawn twelve rejections in a row from a sampler with acceptance rate 0.12. What is the expected number of further draws? *Correct:* 8.33, exactly as before the twelve.

## Practice seed

**Stem.** A flaky endpoint succeeds on 60 percent of attempts. Find the probability the first success comes on attempt 3, the probability it takes more than 4 attempts, and the mean number of attempts. Then say how many retries you would budget to cover 99 percent of calls.
**Hint.** The tail form is shorter than the PMF for the second and fourth parts. For the budget, solve `(1 - p)^k <= 0.01`.
**Solution.** `P(L = 3) = 0.4^2 x 0.6 = 0.096`. `P(L > 4) = 0.4^4 = 0.0256`. Mean `1 / 0.6 = 1.667`. Budget: `0.4^k <= 0.01` gives `k >= ln(0.01)/ln(0.4) = 5.026`, so 6 attempts, that is 5 retries.
**`.p-check`.** The mean must lie between 1 and 2 because `p` is above 0.5, and `P(L > 4)` must be smaller than `P(L = 3)`, because the tail past 4 is thinner than a single early term.

## Sources

- Hajek, ECE 313, section 2.5 and appendix 6.3.1.
- Leviathan, Kalman and Matias, "Fast Inference from Transformers via Speculative Decoding", 2023, Definition 3.1 and eq 1. <https://arxiv.org/abs/2211.17192>
