# 0501 - A derivative is the exchange rate between a small input change and a small output change

> **PLACEHOLDER NUMBER.** Real number assigned by the scaffold (#41). Report label C01.

| | |
|---|---|
| Module | M05 Calculus |
| Rung | foundation (`pill easy`) |
| Label | `core` |
| Prerequisites | M01: functions and composition, limit intuition. Nothing else. |
| Enables | 0502 (chain rule), and every page after it |

## The single tight idea

The derivative is not a formula you look up. It is the number that says how much the
output moves when you nudge the input, and it is different at every point.

## Beats, in order

1. **Open on a question a stakeholder actually asks.** A credit model outputs a logit.
   Product asks: if we shift the score by 0.01, how many more people get approved?
   The answer is a number, and it changes depending on where you already are.
2. **The difference quotient as a measurement.** Pick a step `h`, compute
   `(f(x+h) - f(x)) / h`. This is something you can do with a calculator, not a
   definition to accept.
3. **Shrink `h`.** The secant rotates onto the tangent. Name the limit, name `f'(x)`
   and `dy/dx`, and say they are the same object.
4. **Continuity, only as far as this course needs it.** A function with a jump has no
   derivative at the jump. Connect it forward: this is why models train on
   cross-entropy and report accuracy, because accuracy is a step function and a step
   function has nothing to descend.
5. **The payoff, in a `.card.callout.key`:** `f(x + eps) ~= f(x) + f'(x) eps`.
   Every training step in this course is that sentence, trusted for one step.
6. **The trade-off, in the same section as the technique.** On a real machine the
   limit does not converge. Truncation error falls as `h` shrinks and round-off error
   rises, so the error curve is a V with a floor you cannot get under.
7. **Close by naming the debt.** Real models are compositions. 0502 pays it.

## Named theorem and its stated proof

**Differentiability implies continuity.** The one theorem this page owes, and it is
the one that makes beat 4 more than an assertion.

> If `f` is differentiable at `a` then `f` is continuous at `a`.
>
> *Proof.* For `x != a` write
> `f(x) - f(a) = ((f(x) - f(a)) / (x - a)) * (x - a)`.
> Both factors have limits as `x -> a`: the first tends to `f'(a)` because `f` is
> differentiable at `a`, and the second tends to `0`. The limit of a product of two
> convergent sequences is the product of their limits, so
> `lim_{x -> a} (f(x) - f(a)) = f'(a) * 0 = 0`, which is exactly
> `lim_{x -> a} f(x) = f(a)`, the definition of continuity at `a`. **QED**

State the converse is false and give the one-line witness: `|x|` is continuous at 0
and not differentiable there. That witness is 0503's whole page, so name it and move on.

## Figures

1. **Orientation, `flowchart LR`.** "A function you can evaluate (M01)" into
   "THIS PAGE: how fast it changes" into "the chain rule (0502)" and "every gradient
   in this course". Dotted: "Calculus for machine learning".
2. **`svg.chart`.** `f(x) = sin(x) e^(x/3)` with three secants at `h = 1.0, 0.5, 0.1`
   collapsing onto the tangent at `x = 1.2`, each labelled with its slope.
   *Kills:* the derivative as a formula. It is a limit of slopes you can measure.
3. **`svg.chart`, log-log, quantitative.** Forward and central difference error against
   `h` from `1e-1` to `1e-12`. Both curves show the V.
   *Kills:* "smaller h is always more accurate".
4. **`svg.chart`.** The sigmoid with tangents drawn at `z = 0` and `z = 2`, annotated
   with the probability change a `+0.01` logit nudge causes at each.
   *Kills:* "the derivative is the same everywhere".

Two kinds, four figures, two of them quantitative. Clears r1 5.3.

## Worked example, in r1 5.4's eight parts

1. **Setting.** A credit model at logit `z = 2.0`. Does a `+0.01` shift matter?
2. **Symbolic first.** `.math` with `sigma(z) = 1 / (1 + e^-z)` and
   `sigma'(z) = sigma(z)(1 - sigma(z))`, `.gloss` naming `z`, `sigma`, `e`.
3. **Picture before algebra.** Figure 4 above.
4. **`ol.worked`.**
   - **Evaluate the probability.** `sigma(2.0) = 0.880797`.
   - **Evaluate the derivative.** `0.880797 x 0.119203 = 0.104994`.
   - **Multiply by the nudge.** `0.104994 x 0.01 = 0.00105`.
   - **Repeat at the boundary.** `sigma'(0) = 0.25`, so the same nudge moves the
     probability by `0.0025`.
5. **`.keynum`** on nothing here: every number is derived on the page.
6. **Sanity check.** `sigma'` is a product of two numbers each below 1, so it must be
   below 1, and it is largest when the two factors are equal, which is at `sigma = 0.5`
   giving `0.25`. A derivative above `0.25` anywhere would be an arithmetic error.
7. **What changes if** the logit is `-2.0` instead of `+2.0`? Nothing:
   `sigma'` is symmetric about zero, so the answer is `0.00105` again. The sensitivity
   depends on distance from the decision boundary, not on which side of it you are.
8. **In words.** The same score change is worth 2.4 times more to someone sitting on
   the boundary than to someone already comfortably approved.

## Quiz seeds

**Q1, misconception.** Why does the central-difference error stop improving below
about `h = 1e-5`?
*Answer:* round-off in `f(x+h) - f(x-h)` grows as `h` shrinks, and eventually beats
the falling truncation error.
*Distractors:* "the derivative does not exist there" (false, the function is smooth);
"the central difference is only second-order accurate" (true, and it explains the
falling part, not the floor); "floating point cannot represent 1e-5" (false).

**Q2.** A logistic model sits at logit `z = 2.0` and the logit rises by `0.01`.
Roughly how much does the predicted probability rise?
*Answer:* about `0.00105`.
*Distractors:* `0.01` assumes the derivative is 1; `0.0025` uses the derivative at
`z = 0`, which is the maximum and not this point; `0.0088` multiplies by `sigma` rather
than `sigma'`.

## Practice seed

**Stem.** For `f(x) = sin(x) e^(x/3)` at `x = 1.2`: write the exact derivative,
evaluate it, compute the central difference at `h = 1e-3` and at `h = 1e-10`, and say
which is closer and why.

**Hint.** Product rule. And look at the error table before assuming the smaller step wins.

**Solution.** `f'(x) = cos(x) e^(x/3) + (1/3) sin(x) e^(x/3)`, so
`f'(1.2) = 1.004053890048`. Central-difference errors are `2.832e-07` at `h = 1e-3`
and `3.830e-07` at `h = 1e-10`. The larger step is closer, because the error curve is a
V and `1e-10` is past its bottom.

**`.p-check`.** The derivative of a function that is rising steeply at `x = 1.2` must be
positive and of order 1, and `1.004` is. A negative answer means a sign slipped in the
product rule.

## Code and dataset

`../code/m05_01_derivative_limit.py`. No dataset: this page's object is a function.
It computes the exact derivative, then both difference formulas at twelve step sizes,
and reports where each bottoms out and the measured order of accuracy.

Verified output to quote: exact `f'(1.2) = 1.004053890048`; central difference best at
`h = 1e-5` with error `2.865e-11`; forward difference best at `h = 1e-8` with error
`2.777e-08`; measured error ratios from `1e-2` to `1e-3` are `10.06` and `100.00`
against the predicted `10` and `100`.

## Sources

- Goodfellow, Bengio and Courville, *Deep Learning*, section 4.3, for the derivative as
  the scale factor on a small change. `https://www.deeplearningbook.org/contents/numerical.html`
- Deisenroth, Faisal and Ong, *Mathematics for Machine Learning*, section 5.1, for the
  difference quotient and the limit. `https://mml-book.github.io/book/mml-book.pdf`
- Baydin, Pearlmutter, Radul and Siskind, JMLR 18(153) 2018, section 2, for numerical
  differentiation's round-off and truncation error and why it scales poorly.
  `https://arxiv.org/abs/1502.05767`
