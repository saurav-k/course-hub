# 0005 argmax, argmin, and what training actually is

| | |
|---|---|
| Module | M01 Foundations |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,100 to 1,300 prose words, excluding practice and quiz text |
| Source scout | `mlm-foundations-r2` L5 |

## One tight idea

`max` gives you the value, `argmax` gives you the place, and every model you train is an `argmin`.

## Prerequisites

`0003` for function notation, `0004` for monotonicity.

## Downstream

M06 owns optimization and needs this page's objective. M09's MLE is an argmax. M10 owns softmax as a function.

## Boundaries: what this page must not teach

- **Not** how to solve an argmin. M06 owns every method.
- **Not** softmax itself. M10 owns it; this page owns only why its name is wrong.
- **Not** the loss functions themselves. Name one, do not enumerate.

## Beats, in order

1. `max` against `argmax` on three numbers in a table. Make the **type** difference the point: one is a score in R, one is a class label.
2. `argmin`, and the sign flip that turns any maximisation into a minimisation. This is why loss functions are negative log-likelihoods.
3. The one-line statement of supervised learning, every symbol named in words first. Point back at `0001` for the index and `0003` for the semicolon.
4. Prediction is also an argmax, over classes rather than parameters. Same operator, different search space; "over what?" is the question the subscript answers.
5. Ties. `argmax` is a **set** in general, and library code picks a convention. A reader who has never been told this will one day debug it.
6. `argmax` is not differentiable and its output is a step. This is the whole reason softmax exists.
7. The naming correction: softmax is a soft **argmax**, not a soft max, and the name is an entrenched mistake.
8. Softmax is shift-invariant: adding a constant to every logit changes nothing. State it as a property of argmax and let `0007` collect the payment.

## Figures

- **Orientation**, `flowchart`: *a function and its shape (`0003`, `0004`)* -> **THIS PAGE: the operator that picks the place, not the value** -> *M06 solves it, M09 uses it* -> *(dotted) M01*.
- **`svg.chart`**, required: a curve with its maximum value marked on the y-axis and its argmax marked on the x-axis, in two different colours, with both labelled. One picture, the whole distinction.
- **`flowchart`**: training as argmin over parameters beside prediction as argmax over classes, drawn as the same shape with two different search spaces.

## Worked example

Three logits. Compute max, argmax, and then softmax by hand (reusing the arithmetic from lesson zero deliberately, so the reader sees a familiar calculation in a new role). Add 5 to all three and recompute, showing argmax and softmax both unmoved while max moves by exactly 5.

## Quiz seeds

1. **Misconception.** `max` and `argmax` of `[0.1, 0.7, 0.2]`. Distractors must include `0.7` offered as the argmax, which is the single most common slip.
2. **Mechanism.** Why can a network not train through a hard argmax? Options should distinguish "not differentiable" from "too slow" and from "not deterministic".

## Practice seed

**Stem.** For a 4-class logit vector, give max, argmax, the softmax weights, and then the argmax after adding 10 to every logit.
**Hint.** Two of those four answers cannot change. Decide which before computing.
**Solution path.** Max and softmax weights from arithmetic; argmax by inspection; then the shift argument.
**`.p-check`.** Adding a constant to every logit must leave argmax and every softmax weight unchanged. If a weight moved, the shift was not applied to every entry.

## Code and dataset

`code/0005-argmax-and-what-training-is.py` against `datasets/sensors.csv`. Treats each row's eight standardised readings as logits, computes `argmax` two ways (an explicit loop tracking the best index, and `np.argmax`) and asserts they agree; then adds a random per-row constant and asserts every argmax is unchanged.

## Sources

- Goodfellow, Bengio and Courville, *Deep Learning*, for the softmax naming point, quoted.
