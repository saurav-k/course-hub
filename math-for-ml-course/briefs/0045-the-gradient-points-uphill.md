# 0045 - The gradient points uphill, and it is steepest only in the Euclidean sense

> Number claimed under #42 from the roadmap count in `../index.html`. Report label C05.

| | |
|---|---|
| Module | M05 Calculus |
| Rung | working (`pill med`) |
| Label | `core` |
| Prerequisites | 0044. M03: dot product, unit vector, Euclidean norm. |
| Enables | M06's entire descent family |

## The single tight idea

Among all unit directions the gradient changes the function fastest, and "unit" quietly
depends on how you measure length.

## Beats, in order

1. **The question.** You are on a surface and may step one unit in any direction. Which
   direction rises the most? Make the reader want the answer before deriving it.
2. **The directional derivative,** defined as the derivative of `f(x + alpha u)` at
   `alpha = 0`, which the chain rule from 0042 collapses to `u . grad f`. One line, and
   it reuses the previous page rather than introducing machinery.
3. **The cos-theta argument, worked in full.** `u . grad f = ||u|| ||grad f|| cos theta`.
   With `||u|| = 1` everything turns on `cos theta`, which is smallest at `180` degrees.
   The negative gradient is the steepest descent direction and its rate is `-||grad f||`.
4. **Geometric consequence.** The gradient is perpendicular to the level set. Draw it,
   and give the one-line reason: moving along a contour does not change `f`, so the
   directional derivative along it is zero, so the gradient is orthogonal to it.
5. **Worked: five named directions ranked on real data**, with the negative gradient
   winning and by how much.
6. **The trade-off, in the same section, and it is the page's honest half.** "Steepest"
   was defined by the Euclidean unit ball. Change the ball to an ellipsoid and the
   steepest direction rotates. Show both balls in one figure and give the measured angle.
7. **Hand-off, one sentence.** M06 owns what to do with the direction. This page stops
   at "here is the direction, and here is exactly what it is optimal for".

## Named theorem and its stated proof

**The steepest-ascent theorem.**

> Let `f` be differentiable at `x` with `grad f(x) != 0`. Over all unit vectors `u` in
> the Euclidean norm, the directional derivative `D_u f(x) = u . grad f(x)` is maximised
> at `u = grad f(x) / ||grad f(x)||` with value `+||grad f(x)||`, and minimised at
> `u = -grad f(x) / ||grad f(x)||` with value `-||grad f(x)||`.
>
> *Proof.* By the Cauchy-Schwarz inequality, for any `u` with `||u|| = 1`,
>
>   `|u . grad f(x)| <= ||u|| ||grad f(x)|| = ||grad f(x)||`,
>
> so `-||grad f(x)|| <= u . grad f(x) <= ||grad f(x)||` for every admissible `u`.
> Cauchy-Schwarz holds with equality exactly when the two vectors are parallel, so the
> upper bound is attained by `u = grad f(x)/||grad f(x)||`, where the dot product is
> `||grad f(x)||^2 / ||grad f(x)|| = ||grad f(x)||`, and the lower bound by its negative.
> Since a bound that is attained is the extremum, both claims follow. **QED**

**The caveat, stated as a proposition rather than left as a remark**, because the
unqualified sentence "the negative gradient is the steepest descent direction" is the
single most repeated wrong thing in this territory.

> For any norm `||.||` on `R^n`, define the normalised steepest descent direction as
> `argmin { grad f(x) . v : ||v|| = 1 }`. Taking the Euclidean norm returns
> `-grad f(x)/||grad f(x)||_2`, by the theorem above. Taking the quadratic norm
> `||z||_P = sqrt(z^T P z)` for positive definite `P` returns a direction parallel to
> `-P^-1 grad f(x)` instead.
>
> *Proof sketch, and it is enough here.* Substitute `zbar = P^(1/2) z`. The constraint
> `||z||_P = 1` becomes `||zbar||_2 = 1`, and the objective `grad f . z` becomes
> `(P^(-1/2) grad f) . zbar`. That is the Euclidean problem with gradient
> `P^(-1/2) grad f`, whose solution is `zbar = -P^(-1/2) grad f / ||.||`. Mapping back
> through `z = P^(-1/2) zbar` gives `z` parallel to `-P^-1 grad f`. **QED**
>
> So steepest descent is not one direction. It is a family indexed by the norm, and
> gradient descent is the member you get by choosing the Euclidean one, usually without
> noticing that you chose.

## Figures

1. **Orientation, `flowchart LR`.** "The gradient exists (0044)" into "THIS PAGE: what it
   is optimal for" into "gradient descent (M06)", with "why Adam is not just a heuristic"
   dotted in.
2. **`svg.chart`, quantitative.** Directional derivative against the angle `theta` from
   `0` to `360` degrees: a cosine, minimum marked at `180`. *Kills:* taking the
   cos-theta argument on faith. The reader sees the curve and where its bottom is.
3. **`svg.chart`.** One point, two unit balls. A circle with its steepest direction and
   an ellipse with a visibly different one, with the angle between them labelled.
   *Kills:* "the negative gradient is the steepest direction", full stop.
4. **`svg.chart`, quantitative.** Horizontal bars: five candidate unit directions against
   their directional derivatives on the housing loss. *Kills:* "any downhill direction is
   about as good".

## Worked example, in eight parts

1. **Setting.** At `theta = 0`-ish on the five-parameter housing regression, you may step
   one unit in any direction. Which?
2. **Symbolic.** `.math` for `D_u f = u . grad f = ||grad f|| cos theta` with a `.gloss`
   naming `u`, `theta`, and why `||u|| = 1` is required for the question to have an answer.
3. **Picture.** Figure 2.
4. **`ol.worked`.** Compute `||grad f||`, then the directional derivative for each of
   five named directions, then express each as a percentage of the best available.
5. **`.keynum`** on nothing: derived here.
6. **Sanity check.** No unit direction can beat `-||grad f||`, by Cauchy-Schwarz, so every
   entry in the table must lie between `-||grad f||` and `+||grad f||`. A number outside
   that range is an arithmetic error, and the program checks it against 50,000 random
   directions for exactly this reason.
7. **What changes if** the columns are standardised first? The gradient rotates, and the
   "lot only" direction stops being nearly optimal. The ranking is a fact about units,
   not about the features, and 0050 is where that becomes a number.
8. **In words.** On this table, stepping along the lot-size axis alone recovers 97 per
   cent of the best possible rate of descent, and stepping along the bedrooms axis alone
   recovers 0.04 per cent. Neither number says anything about which feature predicts price.

## Quiz seeds

**Q1.** The directional derivative along `u` is `u . grad f`. Why must `u` be a unit
vector for "which direction is steepest" to have an answer?
*Answer:* otherwise the value can be made arbitrarily large by scaling `u`, and the
question has no maximum.
*Distractors:* "because the dot product requires it" is false; "because the gradient is a
unit vector" is false; "so that cos theta stays between -1 and 1" reverses the mechanism.

**Q2, misconception.** On the raw housing regression, `-g/||g||` gives a directional
derivative of `-3,474,082.69` and "bedrooms only" gives `+1,239.50`. What does the gap say?
*Answer:* the loss is overwhelmingly sensitive to the columns with large units, which is
a symptom of unscaled features and reappears in 0050 as a condition number.
*Distractors:* "bedrooms do not predict price" confuses gradient scale with importance;
"the gradient is wrong" is not a thing; "the loss has no minimum in that direction" is
unsupported and false.

## Practice seed

**Stem.** With `grad f = (-850000, -862)` in two dimensions, compute the directional
derivative for the unit vectors `(1, 0)`, `(0, 1)` and `(0.7071, 0.7071)`, then confirm
that `-g/||g||` attains `-||grad f||`.

**Hint.** Four dot products and one norm. Do the norm first: it is the number every
other answer is measured against.

**Solution.** `||grad f|| = 850,000.44`. The three directions give `-850,000.00`,
`-862.00` and `-601,650.29`. `-g/||g|| = (0.99999, 0.00101)` gives `-850,000.44`, which
is exactly `-||grad f||` and therefore the best available.

**`.p-check`.** No answer may be more negative than `-850,000.44`. If one is, the
direction was not normalised.

## Code and dataset

`../code/m05_05_steepest_ascent.py` against `../datasets/m05-housing.csv`.
It computes the gradient, ranks five named directions, then brute-forces 50,000 random
unit directions to confirm none beats the bound, then computes the steepest direction
under the Hessian's own norm and reports the angle.

Verified output to quote: `||grad f|| = 3,474,082.69`; lot-only reaches `97.44%` of the
best rate, equal-on-all-five `53.77%`, bedrooms-only `0.04%`; across 50,000 random unit
directions the most negative found is `-3,472,017.29`, none beats the bound, and the best
random direction reaches `99.94%`; and **the steepest direction under the quadratic norm
sits 89.9 degrees from the Euclidean one**, which is very nearly perpendicular and is the
strongest single number on the page.

## Sources

- Goodfellow, Bengio and Courville, *Deep Learning*, section 4.3, equations 4.3 and 4.4,
  for the directional derivative and the cos-theta minimisation.
  `https://www.deeplearningbook.org/contents/numerical.html`
- Boyd and Vandenberghe, *Convex Optimization*, sections 9.4 and 9.4.1, pages 475 to 477,
  for the normalised steepest descent direction with respect to an arbitrary norm, for
  "the steepest descent method for the Euclidean norm coincides with the gradient descent
  method", and for the quadratic-norm direction `-P^-1 grad f`.
  `https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf`
