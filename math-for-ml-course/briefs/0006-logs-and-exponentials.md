# 0006 Logarithms and exponentials: the rules and the shapes

| | |
|---|---|
| Module | M01 Foundations |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,300 to 1,500 prose words, excluding practice and quiz text |
| Source scout | `mlm-foundations-r2` L6 |

## One tight idea

A logarithm answers "what exponent?", and all four rules follow from that one sentence.

## Prerequisites

`0003` for inverse functions, `0004` for monotonicity and shapes.

## Downstream

`0007`, `0009` (the growth ladder), M06 (learning-rate decay), M07, M09, M10.

## Boundaries: what this page must not teach

- **Not** entropy, perplexity or log-sum-exp. M10 owns all three. This page owns the arithmetic only.
- **Not** the derivative of `log` or `exp`. M05 owns that.
- It may **state** that `log(a+b)` is not `log a + log b` and that this is why a `logsumexp` routine exists. It must **not** derive that identity.

## Beats, in order

1. Exponential first, because the log is defined from it. Growth against decay, and the one thing to notice: the rate is proportional to the current size.
2. `e`, and why it is the base the field defaults to.
3. The logarithm as the inverse. Domain is the positive reals, which is why `log 0` is minus infinity and why that shows up in a training log as `-inf` or `nan`.
4. **In machine learning, `log` means natural log.** State it flatly, and say where `log2` appears instead (when the answer is in bits) and that M10 owns that.
5. The four rules, each derived from the "what exponent?" reading rather than asserted: product, quotient, power, change of base.
6. The one that is not a rule: `log(a + b)` is not `log a + log b`. Show a counterexample with numbers, then say the useful thing and hand the identity to M10.
7. Reading a log axis. A straight line on a log-y axis is exponential; a straight line on log-log is a power law. This pays off in every scaling-law plot in the hub.
8. One worked conversion tying a rate to a half-life or a median.

## Stated proof (D4)

**The product rule for logarithms.** Derive it rather than asserting it, because the derivation *is* the "what exponent?" reading and it makes the other three rules obvious.

Let `log_b m = x` and `log_b n = y`, so `b^x = m` and `b^y = n`. Then `mn = b^x b^y = b^(x+y)`, so by definition `log_b(mn) = x + y`. **The step that does the work** is `b^x b^y = b^(x+y)`, which is the exponent law; the logarithm rule is that law read backwards. Say so explicitly, then state the quotient and power rules as the same move and leave them as an exercise on the page rather than three more derivations.

## Figures

- **Orientation**, `flowchart`: *inverse functions (`0003`)* -> **THIS PAGE: the log answers "what exponent?"** -> *`0007` uses it to survive floating point, M10 to measure surprise* -> *(dotted) M01*.
- **`svg.chart`**, required: the same exponential data plotted on a linear y-axis and on a log y-axis, side by side in one `<figure>`, so the curve becomes a straight line. This is the transferable skill.
- **`svg.chart`**: `exp` and `log` as mirror images across the diagonal, with the asymptote at zero annotated.

## Worked example

Convert a decay rate to a half-life and back. Show every rule used, named as it is used. Then a counterexample table for `log(a+b)` with three pairs, so the reader sees the size of the error rather than just its existence.

## Quiz seeds

1. **Misconception.** Is `log(a + b) = log a + log b`? The distractors should include "only when a and b are positive", which is a true-sounding constraint attached to the wrong rule.
2. **Mechanism.** A straight line on a log-log plot means what? Options: exponential, power law, linear, logarithmic.

## Practice seed

**Stem.** Given a quantity that halves every 3 units, find the decay rate. Then say what the plot of that quantity looks like on a log-y axis and why.
**Hint.** Halving means the ratio is one half; take logs of both sides of that statement.
**Solution path.** From the ratio to `ln(1/2)`, divide by the interval, then the sign; then the straight-line argument.
**`.p-check`.** A decay rate must be negative and a half-life positive. If the signs disagree, a `ln(1/2)` was written as `ln 2`.

## Code and dataset

`code/0006-logs-and-exponentials.py` against `datasets/sessions.csv`. Verifies each of the four rules numerically across the `session_seconds` column, then shows the `log(a+b)` counterexample at scale by reporting the maximum absolute error over all pairs in a sample. Prints the numbers the page quotes.

## Sources

- NIST DLMF chapter 4 for the exponential series and the logarithm rules.

## As built

Written by `mlm-foundations-r2` alongside this brief; where the shipped page departs from the plan above, this is what it does and why.

All four identities are proved, each in two lines from `e^u e^v = e^(u+v)`, and the page says outright that this is one sentence used four times.
The four rules and **the rule that does not exist** are drawn as a `mindmap`, with the non-rule as a fifth clearly-marked branch. The exponential fit is worked on `tickets.csv`'s response times, and the page carries a one-way link to the Statistical Foundations course's version of the same `ln 2` relationship on different data.
