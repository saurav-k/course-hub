# 0043 - Where the derivative does not exist, and why machine learning ships anyway

> Number claimed under #42 from the roadmap count in `../index.html`. Report label C03.

| | |
|---|---|
| Module | M05 Calculus |
| Rung | working (`pill med`) |
| Label | `core` |
| Prerequisites | 0041, 0042. |
| Enables | 0047 (ReLU gating in the backward pass), M06's L1 geometry |

## The single tight idea

A kink is not a disqualification. It is a point where the derivative stops being a
number and becomes a set, and optimisation carries on regardless.

## Beats, in order

1. **ReLU is `max(0, z)`.** Draw it. Ask what its slope is at exactly zero, and let the
   reader notice there are two defensible answers.
2. **Left and right derivatives, defined.** For ReLU at zero they are `0` and `1`. They
   disagree, so the derivative does not exist there. That is a fact, not a problem yet.
3. **What frameworks actually do.** Return one of the one-sided values rather than
   raising. Cite Goodfellow 6.3 for the practice and for the phrasing.
4. **Why it is fine.** Training does not land on exact critical points, and the
   non-differentiable set is a handful of points. Quote the book's reasoning rather than
   paraphrasing it.
5. **The subgradient, by picture.** At a kink, every slope between the two one-sided
   slopes gives a line lying below the function. That set is the subdifferential, and
   "zero is in it" replaces "the derivative is zero".
6. **The worked result.** Squared error picks the mean by one derivative and one root.
   Absolute error picks the median, has no derivative anywhere near it, and its
   minimising set is an interval.
7. **Forward pointer, one sentence.** This is the machinery behind the corner of the L1
   ball, and M06 owns what that corner does.

## Named theorems and their stated proofs

**Theorem 1. The mean minimises total squared error.**

> For real `x_1 ... x_n`, the function `S(c) = sum (x_i - c)^2` is minimised uniquely at
> `c = xbar = (1/n) sum x_i`.
>
> *Proof.* `S` is differentiable everywhere with `S'(c) = -2 sum (x_i - c) = -2(n xbar - n c)`,
> which vanishes exactly at `c = xbar`. `S''(c) = 2n > 0`, so `S` is strictly convex and
> that single critical point is the unique global minimum. **QED**
>
> A second proof, with no calculus, worth one line because it shows where the variance
> comes from: `sum (x_i - c)^2 = sum (x_i - xbar)^2 + n (xbar - c)^2`, and only the last
> term depends on `c`. It is a sum of squares, so it is smallest when it is zero.

**Theorem 2. A median minimises total absolute error, and the minimising set is an
interval.**

> For real `x_1 ... x_n` sorted as `x_(1) <= ... <= x_(n)`, the function
> `A(c) = sum |x_i - c|` is minimised exactly on the interval
> `[x_((n+1)/2), x_((n+1)/2)]` when `n` is odd, and on `[x_(n/2), x_(n/2 + 1)]` when `n`
> is even.
>
> *Proof.* `A` is convex, being a sum of convex functions, so a point is a global
> minimiser if and only if `0` lies in its subdifferential there. Away from every data
> point `A` is differentiable with
>
>   `A'(c) = #{i : x_i < c} - #{i : x_i > c}`,
>
> because each term contributes `+1` when `c` is above it and `-1` when below. That
> difference is non-decreasing in `c`, is negative while fewer than half the points lie
> below `c`, and is positive once more than half do. At a data point the two one-sided
> derivatives differ by twice the multiplicity of that point and the subdifferential is
> the closed interval between them. Zero lies in that set precisely when the count below
> and the count above are each at most `n/2`, which is the definition of a median. For
> even `n` with distinct middle values, every `c` strictly between `x_(n/2)` and
> `x_(n/2 + 1)` has exactly `n/2` points on each side, so `A'(c) = 0` there and the whole
> open interval minimises; the endpoints join it by continuity. **QED**

The even case is the beat readers remember, so let the proof reach it rather than
stopping at "a median works".

## Figures

1. **Orientation, `flowchart LR`.** "The rules work everywhere (0042)" into "THIS PAGE:
   the points where they stop" into "ReLU networks (0047)" and "the L1 corner (M06)".
2. **`svg.chart`, quantitative, real data.** Two panels over the same spend table.
   Left: total squared error against `c`, a parabola with one bottom at the mean.
   Right: total absolute error against `c`, piecewise linear with a **flat bottom**
   between the two middle values. *Kills:* "the minimum is where the derivative is zero,
   and there is one of them".
3. **`stateDiagram-v2`.** States `differentiable` (one-sided derivatives agree), `kink`
   (they differ, subdifferential is an interval), `undefined` (a one-sided derivative
   does not exist). *Kills:* treating "not differentiable" as one undifferentiated failure.
4. **`svg.chart`.** ReLU magnified at zero, left slope `0`, right slope `1`, the fan of
   supporting lines between them shaded. *Kills:* "the gradient at 0 is undefined so the
   code must crash".

## Worked example, in eight parts

1. **Setting.** Five thousand daily card spends with a long right tail. What is the
   typical day?
2. **Symbolic.** `.math` for `S(c) = sum (x_i - c)^2` and `A(c) = sum |x_i - c|`,
   `.gloss` naming both.
3. **Picture.** Figure 2.
4. **`ol.worked`.**
   - **Differentiate the squared loss.** `S'(c) = -2 sum (x_i - c)`, zero at the mean.
   - **Evaluate.** Mean `583.0216`. `S'` there is `+5.97e-10`, zero to rounding.
   - **Try the same move on the absolute loss.** It has no derivative at any data point,
     so there is nothing to set to zero.
   - **Use the subgradient instead.** Count below minus count above. Zero across the
     whole interval between the two middle values, `410.41` and `410.56`.
   - **Check the flat bottom.** Total absolute error is `1,413,229.85` at both ends of
     that interval and at its middle, and `1,413,247.57` one rupee below it.
5. **`.keynum`** on nothing: every figure is computed here from the committed dataset.
6. **Sanity check.** The mean of a right-skewed table must exceed its median, and
   `583.02 > 410.49`. If they came out the other way round the tail would be on the
   wrong side and the arithmetic is wrong.
7. **What changes if** the single largest spend, `Rs 43,173.06`, is multiplied by ten?
   The mean moves from `583.02` to `660.73`. The median does not move at all. One point
   owns the mean and no point owns the median.
8. **In words.** Choosing squared error is choosing to let the biggest day decide what a
   typical day looks like.

## Quiz seeds

**Q1, misconception.** What does `torch.relu` return as the derivative at exactly `z = 0`?
*Answer:* one of the two one-sided derivatives, by convention, rather than an error.
*Distractors:* "it raises an exception" is what the mathematics suggests and what no
framework does; "it returns NaN" would poison training; "it returns 0.5, the average" is
a plausible invention.

**Q2, misconception.** Over the spend table the total absolute error is smallest at
`c = 410.49`. What else is true?
*Answer:* every `c` between `410.41` and `410.56` achieves the same total, so the
minimiser is an interval and not a point.
*Distractors:* "410.49 is the unique minimiser" is the trap; "the total there is
1,690,168" is the value at the mean; "the derivative is zero at 410.49" is wrong at a
data point, where the derivative does not exist and the subdifferential contains zero.

## Practice seed

**Stem.** Take the ten numbers `400, 350, 500, 420, 8500, 380, 410, 440, 390, 460`.
Show that setting the derivative of the squared loss to zero gives the mean. Compute the
mean and the median. Evaluate the total absolute error at both. Then explain why the
second answer needed a subgradient.

**Hint.** For the absolute loss, do not differentiate. Count how many points lie below
your candidate and how many above.

**Solution.** `d/dc sum (x_i - c)^2 = -2 sum (x_i - c) = 0` gives `c = 1225`, the mean.
The median is `415`. Total absolute error is `14,550` at the mean and `8,390` at the
median, and `8,390` at every `c` in `[410, 420]`. The absolute value is not
differentiable at its kink, so the optimality condition is "zero lies in the
subdifferential", and that holds across the whole interval.

**`.p-check`.** The mean must lie above nine of the ten values, because one value is
twenty times the others. It does: `1225` exceeds everything except `8500`. A mean inside
the bulk of the data would mean the `8500` was dropped.

## Code and dataset

`../code/m05_03_subgradient_median.py` against `../datasets/m05-spend.csv` (5,000 rows).
It evaluates both losses, differentiates the first, computes the subdifferential of the
second as a closed interval, and demonstrates the flat bottom and the robustness gap.

Verified output to quote: mean `583.0216`, median `410.4850`, middle values `410.41` and
`410.56`; squared-loss derivative at the mean `+5.966e-10` and at the median `-1.73e+06`;
total absolute error `1,413,229.85` across the whole interval and `1,413,247.57` one
rupee below it; the subdifferential is `[0, 0]` inside the interval and `[-26, -26]` a
rupee below; multiplying the largest spend by ten moves the mean to `660.73` and leaves
the median exactly where it was.

## Sources

- Goodfellow, Bengio and Courville, *Deep Learning*, section 6.3, for ReLU's one-sided
  derivatives at zero being `0` and `1`, for what software returns, and for why training
  never reaching a critical point makes it acceptable.
  `https://www.deeplearningbook.org/contents/mlp.html`
- Boyd and Vandenberghe, *Convex Optimization*, section 3.1 for convexity of a sum and
  the first-order condition. `https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf`

## Cross-course note

The ten-number table in the practice seed is the one
`statistical-foundations-ml-course` used to argue mean against median. Under D1 that
material is rewritten into M02, so the page links to M02's version rather than to the
old file. Confirm the target with the scaffold before writing the link.
