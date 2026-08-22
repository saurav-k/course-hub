# 0005 - argmax, argmin, and what training actually is

| | |
|---|---|
| Module | M01 Foundations |
| Rung | foundation (`pill easy`) |
| Partition | core |
| Prose budget | 1,100 to 1,300 words |
| Prerequisites | `0003` (function notation), `0004` (monotonicity) |
| Needed by | M06 (everything that descends), M10 (softmax as a function) |
| Code | `code/0005-argmax-and-what-training-is.py` |
| Dataset | `datasets/tickets.csv` |
| Named theorem | **softmax shift invariance.** Proved (D4). |

## Boundary

This page owns **reading** the objective, never solving it: M06 owns optimization.
It owns why softmax's name is wrong; M10 owns softmax as a function and the log-sum-exp identity.

## The one idea

`max` gives you the value, `argmax` gives you the place, and every model you train is an `argmin`.

## Beats, in order

1. `max` against `argmax` on three numbers in a table. Make the **type** difference the point: one is a score in R, one is a class label.
2. `argmin`, and the sign flip that turns any maximization into a minimization. This is why loss functions are negative log-likelihoods.
3. The one-line statement of supervised learning, every symbol named in words first: `theta* = argmin_theta (1/n) Sum_i L(f(x^(i); theta), y^(i))`. Point back at `0001` for the index and `0003` for the semicolon.
4. Prediction is also an `argmax`, over classes rather than parameters. Same operator, different search space. "Over what?" is the question the subscript answers.
5. Ties. `argmax` is a **set** in general, and library code picks a convention: NumPy returns the first. A reader never told this will one day debug it.
6. `argmax` is not differentiable and its one-hot output is a step. This is the whole reason softmax exists.
7. The naming correction, on the Deep Learning Book's authority: softmax "is more closely related to the arg max function than the max function ... It would perhaps be better to call the softmax function 'softargmax,' but the current name is an entrenched convention."
8. **Softmax shift invariance**, stated and proved, and immediately cashed: it is the stabilisation trick `0007` needs, and it is why temperature never moves the prediction.

## The proof (D4)

**Theorem.** For any vector `z` in `R^K` and any scalar `c`, `softmax(z + c*1) = softmax(z)`, where `1` is the all-ones vector.

*Proof.* Write the `i`-th component of the left-hand side and factor the constant out of both the numerator and every term of the denominator:

`softmax(z + c)_i = exp(z_i + c) / Sum_j exp(z_j + c) = (exp(c) exp(z_i)) / (exp(c) Sum_j exp(z_j))`

using `exp(a + b) = exp(a) exp(b)`, which is the product rule of `0006` read in the exponential direction. The factor `exp(c)` is the same in the numerator and the denominator and is never zero, so it cancels, leaving `exp(z_i) / Sum_j exp(z_j) = softmax(z)_i`.

**The step that does the real work** is that `exp(c)` factors out of a **sum** of exponentials, which it can only do because it is a common factor of every term. Nothing here needs `c` to be small or positive.

**The consequence the next pages spend.** Choosing `c = -max_j z_j` changes no output and makes the largest argument to `exp` exactly zero, which is the Deep Learning Book's stabilisation. And since `argmax` reads only the ordering, and adding a constant preserves it, the prediction is untouched too, which is `0004`'s theorem arriving as a special case.

## Figures (4, at least one `svg.chart`)

- **F1 orientation, `flowchart LR`.** "Functions and shapes" to "THIS PAGE: training is an argmin" to "gradient descent (M06), softmax (M10)".
- **F2 inline `svg.chart`.** Three logit bars. One arrow points at the tallest bar's **height**, labelled `max`. A second arrow points at that bar's **label on the axis**, labelled `argmax`. Kills the whole max/argmax confusion by pointing at two different parts of the same bar.
- **F3 inline `svg.chart`.** Grouped bars: softmax of one real ticket's logits at `T = 0.5`, `T = 1`, `T = 2`, with the tallest bar the same one in all three groups. Kills: that temperature changes the prediction. It changes the confidence.
- **F4 `flowchart LR`.** The training loop stated as an objective: data to `f(x; theta)` to loss to `argmin` over theta to `theta*`. Kills: that "training" is a verb with no object.

## Worked example (eight parts)

Logits `[2.0, 1.0, 0.1]`: exponentials `7.3891, 2.7183, 1.1052`, sum `11.2125`, softmax `0.659, 0.242, 0.099`, `argmax` class 0.
Then the failure the Deep Learning Book describes, with real float64 numbers this course computed: set all three logits to `c`. At `c = 800`, `exp` overflows (float64 stops at an exponent of `709.78`) and naive softmax returns `[nan, nan, nan]`. At `c = -800` it underflows to zero, the denominator is 0, and the result is `[nan, nan, nan]` again. Subtract `max_i x_i` first and both cases give `[0.3333, 0.3333, 0.3333]`.

- **Sanity check.** The three outputs sum to 1 and the largest input has the largest output.
- **What changes if** the gap between the top two logits widens: the distribution sharpens and `argmax` still does not move.

## Code

`code/0005-argmax-and-what-training-is.py`.
Against the three logit columns of `tickets.csv`: computes `max` and `argmax` and prints their different types and shapes; computes softmax naively and stably; **asserts the naive version produces non-finite values once a constant of 800 is added while the stable version is unchanged to machine precision**; and asserts `argmax` is identical across three temperatures for every one of the 9,000 rows, which is shift invariance and `0004`'s theorem checked at scale.

## Quizzes

- **Q1** (misconception): `max_c p(c given x) = 0.91` and `argmax_c p(c given x) = 7`. Which is the prediction?
  `0.91, the model's output value` / `7, the index of the class chosen` / `Both, they are the same quantity` / `Neither, you need the logits too`
  Feedback: option 1 is the model's confidence, a useful number answering a different question; option 3 is the misconception, and the two have different types; option 4 is false, the logits add nothing here.
- **Q2** (misconception): the Deep Learning Book calls softmax misnamed. What is it a soft version of?
  `The max function over the logits` / `The sum of the exponentials used` / `The min function, with signs flipped` / `The arg max, with a one-hot output`
  Feedback: option 1 is the name and it is the error, since the soft version of the maximum is `softmax(z) . z`; option 2 is the denominator, not the function; option 3 is unrelated.

## Practice

Logits `[1000, 999, 998]`.
(a) What does a naive `exp` do here, and why? (b) Apply the stabilisation and compute the softmax. (c) Compare with the softmax of `[2, 1, 0]`. What does the comparison show?

- **Hint.** For (c), subtract the largest entry from each vector and look at what is left.
- **Solution.** (a) `e^1000` overflows float64, which stops at an exponent of 709.78, so every term is `inf` and the result is `nan`. (b) subtract `max = 1000` to get `[0, -1, -2]`; exponentials `1, 0.3679, 0.1353`; sum `1.5032`; divide to get `[0.665, 0.245, 0.090]`. (c) identical, because the two vectors differ by a constant and softmax is shift-invariant, which is this page's theorem arriving as arithmetic.
- **`.p-check`.** The three outputs must sum to 1. If they sum to `nan` you stabilised after exponentiating rather than before.

## Primary source to go deeper

Goodfellow, Bengio and Courville, *Deep Learning*, sections 4.1 and 6.2.2.3.
