# 0081 - The chain rule is the only differentiation rule that matters at scale

> Number claimed under #42 from the roadmap count in `../index.html`. Report label C02.

| | |
|---|---|
| Module | M05 Calculus |
| Rung | foundation (`pill easy`) |
| Label | `core` |
| Prerequisites | 0080. M01: `exp` and `log` algebra. |
| Enables | 0085 (Jacobian), 0086 (backpropagation), M09's MLE, M10's softmax gradient |

## The single tight idea

A model is a composition, so its derivative is a product of local derivatives
multiplied along a path.

## Beats, in order

1. **The other rules first, and briefly.** Sum, product and quotient in one table with
   one worked line each. Say plainly that these are fluency and the next one is insight.
2. **The chain rule as a picture before a formula.** `x -> u -> y`. If `u` moves three
   times as fast as `x`, and `y` moves twice as fast as `u`, then `y` moves six times as
   fast as `x`. Multiplication along a path.
3. **Why it is load-bearing.** Every layer, every activation, every loss is a link in
   one chain. A model with 200 layers is a 200-link chain and nothing else.
4. **Worked: the sigmoid.** Differentiate `sigma(z) = 1/(1 + e^-z)` by the quotient rule
   and land on `sigma' = sigma(1 - sigma)`. Plot it. Its maximum is `0.25` at `z = 0`,
   and that number is the whole vanishing-gradient story in 0087.
5. **Worked: cross-entropy on a logit,** four steps, ending at `dL/dz = sigma(z) - y`.
   The sigmoid and the logarithm cancel, which is exactly why frameworks ship a fused
   operation instead of two.
   **Boundary:** stop at the binary logit. The multi-class form is M10's (r1 edge 11).
6. **The trade-off, in the same section.** Writing a chained derivative out by hand
   explodes. Show the four-line derivative of
   `f(x) = sqrt(x^2 + exp(x^2)) + cos(x^2 + exp(x^2))` as the cautionary example.
   That is the debt 0086 pays.

## Named theorem and its stated proof

**The chain rule.** This page's whole reason to exist, so it gets a real proof and not
the "cancel the `du`" gesture, which is not a proof and teaches a wrong habit.

> Let `g` be differentiable at `a` and `f` differentiable at `g(a)`. Then `f . g` is
> differentiable at `a` and `(f . g)'(a) = f'(g(a)) g'(a)`.
>
> *Proof (Caratheodory's formulation, which avoids dividing by zero).* Differentiability
> of `f` at `b = g(a)` is equivalent to the existence of a function `phi`, continuous at
> `b`, with `f(y) - f(b) = phi(y)(y - b)` for all `y` near `b`, and `phi(b) = f'(b)`.
> Likewise there is `psi`, continuous at `a`, with `g(x) - g(a) = psi(x)(x - a)` and
> `psi(a) = g'(a)`. Substituting `y = g(x)`,
>
>   `f(g(x)) - f(g(a)) = phi(g(x)) (g(x) - g(a)) = phi(g(x)) psi(x) (x - a)`.
>
> The factor `phi(g(x)) psi(x)` is continuous at `a`, being a product of compositions of
> continuous functions, and its value there is `phi(b) psi(a) = f'(g(a)) g'(a)`.
> By the same equivalence in reverse, `f . g` is differentiable at `a` with exactly that
> derivative. **QED**
>
> **Why this formulation and not the obvious one.** The familiar proof writes the
> quotient `(f(g(x)) - f(g(a))) / (g(x) - g(a)) * (g(x) - g(a)) / (x - a)` and takes
> limits. That divides by `g(x) - g(a)`, which can be zero in every neighbourhood of `a`
> even when `g` is perfectly well behaved: take `g(x) = x^2 sin(1/x)`. The step above has
> no division in it and so has no gap.

Put the "why this formulation" paragraph in a `.callout`. It is the most honest thing on
the page and it takes forty words.

## Figures

1. **Orientation, `flowchart LR`.** "The derivative of one function (0080)" into
   "THIS PAGE: the derivative of a composition" into "backpropagation (0086)" and
   "maximum likelihood (M09)".
2. **`flowchart LR`.** `x -> u -> v -> y`, each edge labelled with its local derivative,
   the product written beneath. *Kills:* the chain rule as a formula to memorise.
3. **`sequenceDiagram`.** Loss asks Layer 3 "how much do you move if I nudge you",
   Layer 3 asks Layer 2, Layer 2 asks Layer 1, answers return multiplied.
   *Kills:* confusion about order, which is what a sequence diagram is for.
4. **`svg.chart`, quantitative.** `sigma(z)` and `sigma'(z)` on one pair of axes, peak of
   `sigma'` marked at `(0, 0.25)`. *Kills:* "the sigmoid derivative is small" with no number.

## Worked example, in eight parts

1. **Setting.** One row of the score table: a logit of `2.0` on a positive example.
2. **Symbolic.** `.math` for `L = -[y log sigma(z) + (1-y) log(1 - sigma(z))]`,
   `.gloss` naming `L`, `y`, `z`, `sigma`.
3. **Picture.** Figure 4.
4. **`ol.worked`.**
   - **Differentiate the loss in `sigma`.** `dL/d sigma = -y/sigma + (1-y)/(1-sigma)`.
   - **Differentiate `sigma` in `z`.** `d sigma/dz = sigma(1 - sigma)`.
   - **Multiply, by the chain rule.** `dL/dz = [-y/sigma + (1-y)/(1-sigma)] sigma(1-sigma)`.
   - **Cancel.** `= -y(1 - sigma) + (1 - y) sigma = sigma - y`.
   - **Evaluate.** `0.880797 - 1 = -0.119203`.
5. **`.keynum`** on nothing: all derived here.
6. **Sanity check.** The label is 1 and the prediction is below 1, so the loss should
   fall when the logit rises, so the derivative must be negative. It is. The magnitude
   must be below 1, because `sigma - y` is a difference of two numbers in `[0,1]`.
7. **What changes if** the label were `0` instead of `1`? `dL/dz = 0.880797`, positive
   and seven times larger. The model is confidently wrong, and the gradient says so.
8. **In words.** The gradient of a cross-entropy on a logit is the prediction error.
   Nothing more complicated is happening.

## Quiz seeds

**Q1.** What is the largest value the logistic sigmoid's derivative can take, and where?
*Answer:* `0.25`, at `z = 0`.
*Distractors:* `1.0` confuses `sigma` with `sigma'`; `0.5` is `sigma(0)`, not `sigma'(0)`;
"it is unbounded" describes `exp`.

**Q2, misconception.** Frameworks fuse the sigmoid and the cross-entropy into one
operation. What is the calculus reason?
*Answer:* the chained derivative collapses to `sigma(z) - y`, so the fused operation
skips the intermediate and is cheaper and numerically stabler.
*Distractors:* "so the loss stays positive" is not a calculus reason; "so the gradient
never vanishes" is false, it vanishes exactly when `sigma(z) = y`; "to save memory on
the forward pass" is a side effect, not the reason.

## Practice seed

**Stem.** Derive `dL/dz` for the binary cross-entropy from scratch, then evaluate it at
`y = 1, z = 2.0`. Then say what the derivative is when the model is exactly right.

**Hint.** Two links: `z -> sigma -> L`. Differentiate each, multiply, and look for the
cancellation before you reach for a calculator.

**Solution.** `dL/dz = sigma(z) - y`; at `y = 1, z = 2.0` it is `-0.119203`. When the
model is exactly right, `sigma(z) = y`, the derivative is zero, and training stops
pushing that example. For a hard label that only happens in the limit `z -> +/- inf`.

**`.p-check`.** The answer must be a number in `[-1, 1]` for any logit and any label,
because it is a difference of two numbers in `[0,1]`. An answer outside that range means
the cancellation went wrong.

## Code and dataset


`../code/0081-the-chain-rule.py` against `../datasets/failures.csv` (20,000 rows). The
dataset ships features and a label, not scores, so the program fits the logistic model
itself by Newton's method in ten lines. It then differentiates the composition two ways
for every row and asserts they agree, and finally shows why the fused form exists.

Verified output to quote: 20,000 rows, 3,401 positive; the fitted logits run from
`-10.637` to `4.906`; the largest disagreement between the closed form and a central
difference across all rows is `7.241e-11` and the mean is `1.799e-12`; the mean
cross-entropy is `0.301045`. The mean gradient is `-7.283063e-18`, exactly zero, and the
reason is worth a sentence on the page: it **is** the intercept's partial derivative, and
Newton drove it to zero. The gradient is bounded by one in both directions, running from
`-0.997907` to `+0.967737`. Evaluated naively the loss returns `inf` at a logit of 40 and
above, where the stable form returns the correct `40.0` and `800.0`.

## Sources

- Deisenroth, Faisal and Ong, *Mathematics for Machine Learning*, sections 5.2.2 and
  5.6, for the chain rule and for the expression-swell example.
  `https://mml-book.github.io/book/mml-book.pdf`
- Goodfellow, Bengio and Courville, *Deep Learning*, section 6.5.2 for the chain rule in
  the form backpropagation uses, and 6.5.9 for the cross-entropy gradient stated as
  `q_i - p_i`. `https://www.deeplearningbook.org/contents/mlp.html`
