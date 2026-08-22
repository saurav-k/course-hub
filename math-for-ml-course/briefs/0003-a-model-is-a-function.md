# 0003 A model is a function, and depth is composition

| | |
|---|---|
| Module | M01 Foundations |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,200 to 1,400 prose words, excluding practice and quiz text |
| Source scout | `mlm-foundations-r2` L3 |

## One tight idea

`f : A -> B` is a contract about shapes, and a deep network is that contract applied L times in a row.

## Prerequisites

`0002`, because a domain is a set.

## Downstream

M05 owns the derivative and the chain rule; this page is what makes "the chain rule follows the chain of composition" a sentence the reader can already parse. `0005` needs function notation.

## Boundaries: what this page must not teach

- **Not** derivatives. M05 owns them.
- **Not** what a neural network *does*. `llm-papers-course` owns mechanism; this page owns only the shape contract.
- **Not** softmax. `0005` names it and M10 owns it.

## Beats, in order

1. A function as a rule with a **declared** input set and output set, not as a formula.
2. Domain, codomain and image, and the difference that matters. Say plainly that "range" is used in the literature for both meanings, and that this course says **image** when it means what the function actually hits.
3. Reading `f : R^784 -> R^10` as a shape contract, before any code.
4. Parameters against inputs, and the semicolon in `f(x; theta)`. The semicolon does real work and almost nobody explains it.
5. Composition, and that it does not commute.
6. A neural network **is** a composition, and the length of the chain is what the word "deep" refers to.
7. Shape algebra: why one chain of widths composes and a mismatched one does not. This is where a first shape error stops being mysterious.
8. Inverses exist only for one-to-one functions. ReLU has none, which is one honest reason a network is hard to run backwards.
9. The inverse pair the reader meets constantly: sigmoid and logit.
10. **Where the mathematics and the arithmetic part company.** Measured while writing this page's program, and not in the original scout report: a sigmoid's image is the open interval, so it never returns exactly 1, and yet in float64 it rounds to exactly `1.0` from an input of about **36.74** upward, and in float32 from about **16.64**. State both facts and say which is which. This is where `log(1 - yhat)` becomes `-inf` in a real training run, and telling the two apart is the whole skill.

## Figures

- **Orientation**, `flowchart`: *a set (`0002`)* -> **THIS PAGE: a function is a contract between two sets** -> *composition, and therefore depth* -> *(dotted) M05's chain rule*.
- **`svg.chart`**, required: sigmoid and logit drawn on one pair of axes as mirror images across the diagonal, which is what "inverse" looks like.
- **`flowchart`**: a three-layer composition with the shape written on every arrow, and a second copy with one width changed so the mismatch is visible.

## Worked example

A chain `784 -> 128 -> 64 -> 10`. State the domain and codomain of each layer, compose them, and give the shape of the whole. Then change one width and say exactly which composition breaks and why.

## Quiz seeds

1. **Misconception.** Does `f(g(x)) = g(f(x))`? Distractors should include "yes, composition is associative", which is a true statement about a different property.
2. **Mechanism.** What is the semicolon in `f(x; theta)` doing?

## Practice seed

**Stem.** Given four layer shapes, say which orderings compose. Then give the image of a ReLU applied to `R`, and say why it has no inverse.
**Hint.** Two functions compose when the codomain of the first is the domain of the second.
**Solution path.** Shape-match pairwise; then observe ReLU sends every negative to the same value, so no rule can undo it.
**`.p-check`.** A composed chain's input shape is the first layer's and its output shape is the last layer's. If your answer has anything from the middle in it, a step is wrong.

## Code and dataset

`code/0003-a-model-is-a-function.py` with NumPy only. Builds three weight matrices, composes them on random input, and asserts the output shape equals the shape the contract predicts; then flips two widths and shows the exception the mismatch raises.

## Sources

- Goodfellow, Bengio and Courville, *Deep Learning*, for depth as the length of the composition chain, and for its notation table's usage of "range".
