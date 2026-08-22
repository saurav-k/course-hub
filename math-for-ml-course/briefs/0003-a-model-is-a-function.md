# 0003 - A model is a function, and depth is composition

| | |
|---|---|
| Module | M01 Foundations |
| Rung | foundation (`pill easy`) |
| Partition | core |
| Prose budget | 1,200 to 1,400 words |
| Prerequisites | `0002` (a domain is a set) |
| Needed by | M05 (the chain rule follows the chain of composition), M03 (a matrix is a linear map) |
| Code | `code/0003-a-model-is-a-function.py` |
| Dataset | `datasets/tickets.csv` |
| Named theorem | **none.** The page says so plainly rather than dressing a definition up as a result. |

## The one idea

`f : A -> B` is a contract about shapes, and a deep network is that contract applied `L` times in a row.

## Beats, in order

1. A function as a rule with a **declared** input set and output set, not as a formula.
2. Domain, codomain and image, and the difference that matters. Be careful and honest: the Deep Learning Book's own notation table writes "the function f with domain A and range B", using "range" for the codomain. Say that both words are in use and that this course says **image** when it means what the function actually hits.
3. Reading `f : R^d -> R^3` as a shape contract, before any code.
4. Parameters against inputs: `f(x; theta)`. The semicolon is doing real work and almost nobody explains it.
5. Composition, and that it does not commute.
6. A neural network **is** a composition. Use the Deep Learning Book's own formula `f(x) = f3(f2(f1(x)))` and its sentence that the length of the chain gives the depth of the model, which is where the name "deep learning" came from.
7. Shape algebra: why one chain of widths composes and a mismatched one does not. This is where a reader's first shape error stops being mysterious.
8. Inverses exist only for one-to-one functions. ReLU has none, which is one honest reason a network is hard to run backwards.
9. The inverse pair the reader will meet constantly: sigmoid and logit.
10. **Where the mathematics and the arithmetic part company**, which the program for this page measured: the image of a sigmoid is open, so it never returns exactly 1, and yet in float64 it rounds to exactly `1.0` from an input of about **36.74** upward, and in float32 from about **16.64**. State both facts and say which is which. This is where `log(1 - yhat)` becomes `-inf` in a real training run, and knowing which of the two facts you are looking at is the whole skill.

## Figures (4, at least one `svg.chart`)

- **F1 orientation, `flowchart LR`.** "Sets, from 0002" to "THIS PAGE: a model is a function" to "the chain rule (M05), linear maps (M03)".
- **F2 `flowchart LR`.** The shape chain `R^45 -> R^32 -> R^16 -> R^3`, each arrow labelled with its layer function, and a crossed-out arrow showing a mismatched pair that will not compose. Kills: the first shape error.
- **F3 inline `svg.chart`.** The sigmoid curve with the **domain** marked along the whole x-axis, the **codomain** `R` marked as the whole y-axis, and the **image** marked as the open interval `(0,1)` with hollow endpoints. Kills: that codomain and image are the same thing, and that a sigmoid can return exactly 1.
- **F4 `flowchart LR`.** Sigmoid and logit as a round trip that returns to where it started, beside a second row where a value goes through ReLU and the return arrow is crossed out. Kills: that every function can be run backwards.

## Worked example (eight parts)

A ticket classifier `f : R^45 -> R^3`, built as `f = f3 . f2 . f1` with widths 45, 32, 16, 3, one row of `tickets.csv` per input.

| Layer | Signature | Parameters |
|---|---|---|
| `f1` | `R^45 -> R^32` | `45 x 32 + 32` |
| `f2` | `R^32 -> R^16` | `32 x 16 + 16` |
| `f3` | `R^16 -> R^3` | `16 x 3 + 3` |

The codomain of each layer is the domain of the next, which is what "composes" means, and the parameter count is a fact about the shapes alone, before any training.

- **Sanity check.** The widest layer touches the most inputs and holds the most parameters.
- **What changes if** the first hidden width doubles: parameters roughly double, because the count is linear in that width.

## Code

`code/0003-a-model-is-a-function.py`.
Builds the 45-32-16-3 forward pass over `tickets.csv` token counts with NumPy only, prints the shape after every layer so the contract is visible at run time, counts parameters from the shapes alone, asserts the composed function's output shape equals the declared codomain, and demonstrates that `logit(sigmoid(x))` returns `x` to within floating-point tolerance while `relu` cannot be inverted.

## Quizzes

- **Q1** (misconception): a sigmoid is declared `sigma : R -> R`. Can it return exactly 1.0?
  `No, its image is an open interval` / `Yes, its codomain is all of R` / `Yes, once the input is large enough` / `No, because R excludes the value 1`
  Feedback: option 2 confuses the declared codomain with what the function hits; option 3 is what float32 does, which is a rounding fact and not a mathematical one, and the page says so; option 4 is false about R.
- **Q2** (misconception): given `f1 : R^45 -> R^32` and `f2 : R^32 -> R^16`, which composition is defined?
  `Both, since composition commutes` / `f1 . f2, giving R^32 -> R^32` / `f2 . f1, giving R^45 -> R^16` / `Neither, the widths do not match`
  Feedback: option 1 is the misconception, composition never commutes in general; option 2 has `f1` receiving a vector it cannot take; option 4 is the panic answer, and the widths do match in one direction.

## Practice

An autoencoder on the ticket features: encoder `45 -> 32 -> 8`, decoder `8 -> 32 -> 45`.
(a) Write the signature of each of the four layers and of the two halves.
(b) Count the parameters.
(c) `decoder . encoder` has domain `R^45` and codomain `R^45`. Why is it not the identity function?

- **Hint.** For (c), count how many numbers go in and how many survive the middle.
- **Solution.** (a) `R^45 -> R^32`, `R^32 -> R^8`, `R^8 -> R^32`, `R^32 -> R^45`; encoder `R^45 -> R^8`, decoder `R^8 -> R^45`. (b) `(45 x 32 + 32) + (32 x 8 + 8) + (8 x 32 + 32) + (32 x 45 + 45)`. (c) the encoder maps a 45-dimensional space into an 8-dimensional one, so it cannot be one-to-one: distinct tickets must collide. A function with no inverse cannot compose to the identity, and that unavoidable collision is the point of a bottleneck.
- **`.p-check`.** The two halves are near mirror images, so their parameter counts should be close but not equal, because the biases follow the output width.

## Primary source to go deeper

Goodfellow, Bengio and Courville, *Deep Learning*, chapter 6, `https://www.deeplearningbook.org/contents/mlp.html`.
