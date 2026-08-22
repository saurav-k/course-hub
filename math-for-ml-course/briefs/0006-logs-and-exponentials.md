# 0006 - Logarithms and exponentials: the rules and the shapes

| | |
|---|---|
| Module | M01 Foundations |
| Rung | foundation (`pill easy`) |
| Partition | core |
| Prose budget | 1,300 to 1,500 words (at its ceiling) |
| Prerequisites | `0003` (inverse functions), `0004` (monotonicity, shapes) |
| Needed by | `0007`, `0009`, M06 (decay schedules), M07, M09, M10 |
| Code | `code/0006-logs-and-exponentials.py` |
| Dataset | `datasets/tickets.csv` |
| Named theorems | **the three logarithm identities and change of base.** All four proved (D4). |

## Boundary

M10 owns entropy, perplexity and the log-sum-exp identity.
This page owns the arithmetic only, and it may state that no rule exists for `log(a+b)` and point at a `logsumexp` routine without deriving it.

## The one idea

A logarithm answers "what exponent?", and all four rules follow from that one sentence.

## Beats, in order

1. Exponential first, because the log is defined from it. `b^x`, growth against decay, and the thing to notice: the rate is proportional to the current size.
2. `e`, and why it is the base the field defaults to. DLMF 4.2 gives `exp z = 1 + z/1! + z^2/2! + ...`, worth showing once: the exponential is built out of factorials, which is a forward link to `0008`.
3. The logarithm as the inverse: `log_b(y) = x` means `b^x = y`. Domain `(0, infinity)`, which is why `log 0` is minus infinity and why that shows up in a training log as `-inf` or `nan`.
4. **In machine learning, `log` means `ln`.** State it flatly, cite the Deep Learning Book's notation table, and say where `log2` appears instead (when the answer is in bits) and that M10 owns that.
5. **The four rules**, each derived from the "what exponent?" reading rather than asserted.
6. The one that is not a rule: `log(a + b)` is not `log a + log b`. Show a counterexample with numbers. Then the useful part: this is precisely why a `logsumexp` routine has to exist, and hand the identity to M10.
7. Reading a log axis. A straight line on a log-y axis is exponential; on log-log it is a power law. Transferable, and it pays off in every scaling-law plot in the hub.
8. Worked conversion on real data: fit `lambda` from a median.

## The proofs (D4)

Write `u = ln a` and `v = ln b`, so by definition `a = e^u` and `b = e^v`, with `a, b > 0`. Every proof below is that substitution plus one exponent rule.

**Product.** `ln(ab) = ln a + ln b`.
*Proof.* `ab = e^u e^v = e^(u+v)`. Taking `ln` of both sides and using that `ln` and `exp` are inverses, `ln(ab) = u + v = ln a + ln b`.

**Quotient.** `ln(a/b) = ln a - ln b`.
*Proof.* `a/b = e^u / e^v = e^(u-v)`, and the same step gives `ln(a/b) = u - v`.

**Power.** `ln(a^n) = n ln a`.
*Proof.* `a^n = (e^u)^n = e^(un)`, so `ln(a^n) = un = n ln a`.

**Change of base.** `log_b(x) = ln x / ln b`.
*Proof.* Let `y = log_b(x)`, so `b^y = x` by definition. Take `ln` of both sides: `ln(b^y) = ln x`. By the power rule `y ln b = ln x`, and `ln b` is non-zero for `b > 0`, `b != 1`, so `y = ln x / ln b`.

**The step that does the real work**, in all four, is `e^u e^v = e^(u+v)`: a single exponent law, read once forwards and three times sideways. That is why the page teaches one sentence rather than four rules.

**Honest boundary.** These hold unconditionally for positive reals, which is the only case this course needs. DLMF states them for complex arguments with a restriction on the phase, and the page says so in one line rather than pretending the unrestricted version is universal.

**And the non-rule.** There is no identity for `ln(a + b)`, and the counterexample is one line: `ln(1 + 1) = 0.693` while `ln 1 + ln 1 = 0`. Nothing can be factored out of a sum inside a logarithm, which is exactly the gap `logsumexp` is built to cross.

## Figures (4, at least one `svg.chart`)

- **F1 orientation, `flowchart LR`.** "Inverse functions, from 0003" to "THIS PAGE: what exponent?" to "log space (0007), the growth ladder (0009), entropy (M10)".
- **F2 inline `svg.chart`.** `exp` and `log` on the same axes with the line `y = x` dashed as a `ref`, so the mirror is visible. Kills: that they are two unrelated buttons.
- **F3 inline `svg.chart`.** The same response-time data plotted twice side by side, linear-y and log-y, the curve becoming a straight line on the right. Kills: that a log axis "squashes" the data. It straightens exponentials, and that is what makes it diagnostic.
- **F4 `mindmap`.** Root "what exponent?", four branches for product, quotient, power and change of base, and a fifth clearly-marked branch for the **non-rule**. Note for the author: a `mindmap` takes branch colours from the `--branch-0..7` tokens.

## Worked example (eight parts)

The exponential's median satisfies `P(X > m) = 0.5`, so `e^(-lambda m) = 0.5`.
Take logs: `-lambda m = ln(0.5) = -ln 2`, so `lambda = ln(2) / m`.
With the observed median of `tickets.csv`'s `first_response_seconds`, `m = 410.891 s`, this gives `lambda = 0.693 / 410.891 = 0.00168693` per second.
Then change of base on a number the reader meets in M10: a score of 20 is `ln 20 = 2.996` in nats and `log2 20 = 4.322` in bits, and the ratio is exactly `ln 2 = 0.693`.

- **Sanity check.** `lambda` has units of "per second", and a larger median must give a smaller `lambda`, which it does. An exponential's mean is `1/lambda = 592.8 s`, and the observed mean is `601.1 s`, which is the right size.
- **What changes if** the median doubles: `lambda` halves, because the median sits in the denominator.

## Code

`code/0006-logs-and-exponentials.py`.
Against `tickets.csv`: verifies all four identities numerically on the response-time column (product, quotient, power, change of base, each asserted to machine precision), then **produces a counterexample to `log(a+b) = log a + log b` on real values**, then fits `lambda = ln(2)/median` and checks the fitted exponential against the empirical survival curve at several thresholds.

## Quizzes

- **Q1** (misconception): a paper writes `log p(x)` with no base. Which base should you assume?
  `Base e, the natural logarithm` / `Base 10, the common logarithm` / `Base 2, because bits are used` / `Whichever base the data uses`
  Feedback: option 2 is the school convention and gets a cross-entropy wrong by a factor of 2.303; option 3 is right only where the paper states an answer in **bits**, which it will say; option 4 is not a thing.
- **Q2** (misconception): which of these is **not** a logarithm rule?
  `log(ab) = log a + log b` / `log(a/b) = log a - log b` / `log(a+b) = log a + log b` / `log(a to the n) = n log a`
  Feedback: options 1, 2 and 4 are the three genuine rules and this page proves all three; option 3 is the most common algebra error in the subject, and the fact that no such rule exists is why a `logsumexp` routine has to be written by hand.

## Practice

A schedule halves the learning rate every ten epochs: `lr(t) = 0.1 x 0.5^(t/10)`.
(a) Is this growth or decay, and what is the half-life? (b) At which epoch does `lr` first reach 0.0125? (c) Rewrite it as `lr(t) = 0.1 x e^(-k t)` and give `k`.

- **Hint.** For (c), write `0.5` as `e^(ln 0.5)` and use the power rule.
- **Solution.** (a) decay, half-life 10 epochs by construction. (b) `0.0125 / 0.1 = 0.125 = 0.5^3`, so `t/10 = 3` and `t = 30`. (c) `0.5^(t/10) = e^((t/10) ln 0.5) = e^(-(t ln 2)/10)`, so `k = ln(2)/10 = 0.0693` per epoch. This is the same `ln 2 / half-life` relationship as the worked example, met from the other direction.
- **`.p-check`.** `k` must be positive for a decay, and `k` times the half-life must come to `ln 2 = 0.693`.

## Primary sources to go deeper

NIST Digital Library of Mathematical Functions, sections 4.2 and 4.8, `https://dlmf.nist.gov/4.8`.
