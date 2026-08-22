# M07-08 - Random variables: a function from outcomes to numbers

**Class:** core. **Rung:** foundation.

## The single tight idea

A random variable is a function from outcomes to numbers; it is neither random nor a variable, and once you see it as a function the rest of probability is bookkeeping.

## Prerequisites

| Page | What it supplies |
|---|---|
| M07-02 | the sample space and events |
| M01, functions | domain, codomain, a rule that maps one to the other |

## Beats, in order

1. **Say the misnomer out loud in the first paragraph.** `X : Omega -> R`. It is a fixed, deterministic rule. The randomness is entirely in which outcome gets drawn.
2. **Why the definition buys anything.** `{X <= c}` is shorthand for the set of outcomes whose value is at most `c`. That is a subset of `Omega`, so it is an event, so by M07-02 it has a probability. Every probability statement about `X` is a statement about `Omega` wearing a disguise.
3. **Two random variables on one sample space.** On `requests.csv`, `R` is the retry count and `F` is 1 when flagged and 0 otherwise. Same rows, two functions, two completely different distributions. **The random variable is the question you asked; `Omega` is the world.**
4. **Notation drill.** Write `P{X = k}` the long way once, as `P({omega : X(omega) = k})`, so the short way is readable for the rest of the module.
5. **Discrete and continuous type**, as a preview only: the split decides whether you sum or integrate, and M07-09 does it properly.
6. **A function of a random variable is a random variable.** `2R`, `R - 1` and "is `R` greater than 1" are all functions on the same `Omega`. This is the move M07-14's Z-transform will make.
7. **The machine-learning section.** The count of flagged requests in a minibatch is a random variable: `Omega` is the set of possible minibatches and `X` counts. So is the loss, so is the minibatch gradient, so is validation accuracy under a seed. "Gradient noise" is precisely the spread of a function of the draw, which is why the same code gives a different curve on a different seed.

## Proof

No named theorem. The page defines an object; there is nothing here to prove, and the page says so rather than inventing a result to look rigorous.

## Planned figures

1. **Orientation, `flowchart LR`.** `M07-02 events` and `M01 functions` feed `THIS PAGE - random variables`, which enables `PMF, PDF and CDF` and `every named distribution`.
2. **`flowchart LR` - two functions, one world.** A box for `Omega` drawn as request rows, with two labelled arrows out: `R` to the retry counts and `F` to `{0, 1}`. A dashed arrow back from `{R >= 2}` to the subset of rows it came from, showing the pullback.
3. **`svg.chart` - the induced distribution.** The 97 consecutive batches of 256 rows from `requests.csv`, with `X` = flagged in the batch. Bars at `X` = 0, 1, 2, 3, 4 with counts 37, 34, 16, 7 and 3. The bars are not the data; they are what the function did to the data.

## The worked example, eight parts

1. **Setting.** `requests.csv` split into 97 consecutive batches of 256 rows, the last 168 rows dropped so every batch is the same size. `X` counts flagged requests in a batch.
2. **Symbolic.** `X : Omega -> {0, 1, ..., 256}`, gloss naming `Omega` as the set of batches, `X` as the counting rule, and `{X = 0}` as a set of batches rather than a number.
3. **Picture first.** Figure 3 above.
4. **`ol.worked`.** Count the batches at each value: 37 at 0, 34 at 1, 16 at 2, 7 at 3, 3 at 4. Check they sum to 97. Divide to get proportions: `37 / 97 = 0.3814`. Take the mean: `(0 x 37 + 1 x 34 + 2 x 16 + 3 x 7 + 4 x 3) / 97 = 99 / 97 = 1.0206`.
5. **`keynum`.** Batch counts are read off the file; the proportions and the mean are derived here.
6. **Sanity check.** The total flagged across all batches must be 99 minus whatever fell in the dropped tail. It is 99, so no request was lost or double counted.
7. **What changes if.** Use batches of 1,024 instead. The same 99 flags land in 24 batches, so `X` rarely reads 0 and its typical value is four times larger. **The world did not change; the function did.**
8. **Interpretation.** Two thirds of batches carry at most one flagged request. That is not a property of the data alone, nor of the batch size alone, but of the function you built out of both, and it is why "how many positives per batch" is a design decision.

## Code and dataset

`code/M07-08-random-variables.py` against `datasets/requests.csv`.

Builds `X` twice: once with an explicit loop over the 97 batches that counts flags one row at a time, so the reader sees the function being applied, and once vectorised by reshaping the flag column and summing along an axis. Asserts the two arrays are identical. Then demonstrates the pullback by printing, for `X = 3`, the batch indices in the preimage and confirming each really contains three flagged rows.

## Quiz seeds

1. **Misconception.** What part of a random variable is random? *Correct:* none of it - the randomness is in which outcome is drawn. *Distractors:* the output value; the function itself; both the input and the function.
2. Why does `P{X <= 7}` have a probability at all? *Correct:* because the outcomes with `X` at most 7 form a subset of the sample space, which is an event.

## Practice seed

**Stem.** On the same 97 batches, define `Y` as 1 when the batch contains at least one flagged request and 0 otherwise. Write down what `Y` is as a function, give its distribution, and say what `Y` throws away that `X` kept.
**Hint.** `Y` is a function of `X`, not of the rows directly. Work out which values of `X` map to 1.
**Solution.** `Y = 1` exactly when `X >= 1`, so `Y` is 0 on 37 batches and 1 on 60. Its distribution is `P(Y = 0) = 37/97 = 0.3814` and `P(Y = 1) = 0.6186`. It throws away how many: a batch with four flags and a batch with one are the same to `Y`.
**`.p-check`.** `P(Y = 0)` must equal `P(X = 0)` exactly, because those are the same set of batches described two ways. If they differ, the mapping was applied wrongly.

## Sources

- Hajek, ECE 313, sections 2.1 and 3.1, the definition of a random variable and of its CDF.
- Goodfellow, Bengio, Courville, *Deep Learning*, ch 3.2.
