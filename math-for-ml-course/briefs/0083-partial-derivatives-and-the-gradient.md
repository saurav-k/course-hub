# 0083 - Partial derivatives put every dial on its own axis, and the gradient collects them

> Number claimed under #42 from the roadmap count in `../index.html`. Report label C04.

| | |
|---|---|
| Module | M05 Calculus |
| Rung | foundation (`pill easy`) |
| Label | `core` |
| Prerequisites | 0080, 0081. M03: vector, transpose, matrix-vector product, the data matrix. |
| Enables | 0084, 0085, 0088, and everything M06 descends along |

## The single tight idea

With many inputs you vary one at a time, and the collection of those answers is a single
vector object with a shape you can check.

## Beats, in order

1. **Two parameters instead of one.** A surface instead of a curve. Draw it.
2. **The partial derivative.** Hold everything else fixed and differentiate as if it
   were the only variable. Nothing new is required, which is the point worth making.
3. **Collect them.** The gradient is the vector of all the partials, and it is one
   object rather than a list of separate facts.
4. **The shape ledger, stated once and referred to for the rest of the course.**
   `R -> R` gives a scalar. `R^D -> R` gives `D` numbers. `R -> R^E` gives `E` numbers.
   `R^D -> R^E` gives an `E x D` matrix. Draw it as boxes.
5. **The convention, in a `.callout.warn`.** Textbooks disagree on whether a gradient is
   written as a row or a column. This course fixes one: **a gradient has the shape of
   the thing you differentiate by**, so `d(scalar)/d(column)` is a column. Point at
   `reference/notation.html`. Never mix.
6. **Worked: a real gradient, as two numbers you can check.** Compute both partials of a
   squared-error loss at one parameter point on real data and assemble them.
   **Boundary:** do not derive the normal equations. M03 owns them and derives them by
   projection precisely so that module needs no calculus (r1 edge 31). Say "set the
   gradient to zero is the move", link to M03 for the answer, and let 0091 show the
   calculus route.
7. **The trade-off.** A zero gradient is a critical point, not a minimum. 0088 owns the
   test that tells them apart. Do not let the reader leave believing otherwise.

## Named theorem and its stated proof

**Differentiability implies the partials exist, and the converse fails.** The one result
this page owes, because the converse failing is what makes "the gradient exists" a real
claim rather than a bookkeeping remark.

> If `f : R^n -> R` is (totally) differentiable at `a`, then every partial derivative of
> `f` exists at `a` and the gradient's `i`-th entry is `d f / d x_i (a)`.
>
> *Proof.* Total differentiability at `a` means there is a vector `g` with
> `f(a + h) = f(a) + g . h + r(h)` where `r(h)/||h|| -> 0`. Take `h = t e_i`, the `i`-th
> coordinate direction. Then `f(a + t e_i) - f(a) = t g_i + r(t e_i)`, so
> `(f(a + t e_i) - f(a)) / t = g_i + r(t e_i)/t`, and `|r(t e_i)/t| = |r(h)|/||h|| -> 0`.
> So the limit defining the `i`-th partial exists and equals `g_i`. **QED**
>
> **The converse is false**, and the standard witness belongs on the page because it
> stops the reader treating the two as the same thing. Let
> `f(x, y) = xy / (x^2 + y^2)` for `(x, y) != (0, 0)` and `f(0, 0) = 0`. Both partials at
> the origin are zero, because `f` is identically zero on both axes. But `f` is not even
> continuous there: along the line `y = x` it takes the constant value `1/2`, so it does
> not tend to `f(0,0) = 0`. A function can have every partial derivative at a point and
> still fail to be differentiable there, or continuous.

Put the counterexample in a `.callout.warn`. It costs four lines and it is the reason
"the gradient exists" is worth saying.

## Figures

1. **Orientation, `flowchart LR`.** "One dial (0080 to 0082)" into "THIS PAGE: many dials
   at once" into "which way to move (0084)" and "the object every optimiser reads (M06)".
2. **`svg.chart`.** Contour map of a two-parameter squared-error surface. At one point,
   the two axis-aligned partial arrows drawn, and their vector sum drawn as the gradient.
   *Kills:* "the gradient is a slope". It is a vector assembled from slopes.
3. **`flowchart TD`.** The shape ledger as four boxes, operand shape to derivative shape.
   *Kills:* the shape confusion that ruins every hand-derived backward pass.
4. **`svg.chart`.** The same contour map with the gradient drawn at four points, each
   perpendicular to the contour through it. Sets up 0084.

## Worked example, in eight parts

1. **Setting.** Fit `spend = a + b * day` to ten days. You are at the guess
   `a = 1000, b = 0`, which is wrong. Which way should each dial move?
2. **Symbolic.** `.math` for `L(a, b) = sum (y_i - a - b d_i)^2`, `.gloss` naming
   `L`, `a`, `b`, `y_i`, `d_i`, `n`.
3. **Picture.** Figure 2.
4. **`ol.worked`.**
   - **Differentiate in `a`.** `dL/da = -2 sum (y_i - a - b d_i)`.
   - **Evaluate.** Residuals sum to `12,250 - 10,000 = 2,250`, so `dL/da = -4,500`.
   - **Differentiate in `b`.** `dL/db = -2 sum d_i (y_i - a - b d_i)`.
   - **Evaluate.** The weighted sum is `63,560 - 1,000 x 55 = 8,560`, so `dL/db = -17,120`.
   - **Assemble.** The gradient is `(-4,500, -17,120)`.
5. **`.keynum`** on nothing: derived here.
6. **Sanity check.** `dL/da` is `-2` times the total residual, and the total residual at
   `a = 1000` is positive because one day is Rs 8,500. So `dL/da` must be negative, and
   it is. A positive value means a sign slipped.
7. **What changes if** the Rs 8,500 day were Rs 450 like its neighbours? The total
   residual becomes `4,200 - 10,000 = -5,800`, `dL/da` flips to `+11,600`, and the
   intercept should come down instead. One point owns the sign of the gradient.
8. **In words.** The gradient is not a verdict about the model. It is a local
   instruction: at this exact guess, raising both dials reduces the loss right now.

## Quiz seeds

**Q1.** For `f: R^D -> R`, how many numbers does the derivative object hold, and what
decides whether they are written as a row or a column?
*Answer:* `D` numbers, and the layout convention the course declared, not the mathematics.
*Distractors:* "`D x D` numbers" is the Hessian; "one number, the slope" is the `R -> R`
case; "it depends on whether `f` is linear" is a true-sounding claim about a different
question.

**Q2, misconception.** Setting the gradient of a squared loss to zero and solving
establishes what, on its own?
*Answer:* that the point is a critical point of the loss. Nothing more, until the
second-order test is run.
*Distractors:* "it is the global minimum" skips the second-order argument; "it is where
the loss is zero" confuses the gradient with the loss; "it is the point closest to the
data" is true here, and is a statement about projection, which is M03's question.

## Practice seed

**Stem.** For the ten-day table fitted as `spend = a + b * day` at `a = 1000, b = 0`:
write both partial derivatives symbolically, evaluate both, and say which way each dial
should move and why the two magnitudes differ so much.

**Hint.** The residual at day `i` is `y_i - 1000`, and you already have
`sum y_i = 12,250` and `sum d_i y_i = 63,560`.

**Solution.** `dL/da = -2 sum (y_i - a - b d_i) = -4,500` and
`dL/db = -2 sum d_i (y_i - a - b d_i) = -17,120`. Both negative, so both dials rise.
The magnitudes differ because the day column runs `1` to `10` against an all-ones
intercept column. That is a scale artefact, not a statement about importance, and 0089
turns it into a condition number.

**`.p-check`.** `dL/da` must be `-2` times the total residual. The total residual is
`2,250`, so `dL/da` must be `-4,500` exactly. If it is not, recheck `sum y_i`.

## Code and dataset


`../code/0083-partial-derivatives-and-the-gradient.py` against `../datasets/sensors.csv`
(12,000 rows, seven parameters: an intercept and six sensors predicting `temp_c`). Every
partial is computed from the closed form and again by nudging that one parameter, with
the step scaled to the parameter because the parameters do not share a scale.

Verified output to quote: the loss at the starting guess is `54.275914`; the six feature
partials run from `-10.023853` (humidity) to `-777.001313` (pressure), a spread of
`77.5`; and the closed form agrees with the definition to between `5.97e-08` and
`1.14e-06`.

**The intercept partial is `-9.597e-15`, which is zero, and the page should say why.**
The starting guess is the intercept-only model, predicting the overall mean, and that
makes the residuals sum to zero. Their sum **is** the intercept's partial derivative, so
the guess already solves one dial exactly. It is the first time in the module a partial
derivative vanishes for a reason the reader can name, and it sets up 0091's ridge beat.

The step ladder is the other beat to quote, because it shows the curvature limit before
0089 explains it: stepping along the negative gradient takes the loss from `54.275914` to
`54.269776` at `1e-8`, to `53.721475` at `1e-6`, back **up** to `54.127890` at `1e-5`,
and to `592.431856` at `1e-4`.

## Sources

- Deisenroth, Faisal and Ong, *Mathematics for Machine Learning*, section 5.2, for the
  partial derivative, the gradient, and Figure 5.6's shape ledger. Note that the book
  writes the gradient as a `1 x n` row and says so explicitly; this course takes the
  other convention and must say that it is doing so.
  `https://mml-book.github.io/book/mml-book.pdf`
- Goodfellow, Bengio and Courville, *Deep Learning*, section 4.3, for the gradient as the
  vector of partials and for critical points being where every element is zero.
  `https://www.deeplearningbook.org/contents/numerical.html`
