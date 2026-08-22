# 0184 - Softmax and log-sum-exp

**Module** M10 - lesson 05  **Rung** working  **Class** core

## The single tight idea

The exponential you write is never the exponential you compute, and the one line that makes it
computable also hands you the most-used gradient in machine learning.

## Prerequisites

0181 (cross-entropy, which this page produces the `q` for). M01 for the exponential and for the
arithmetic case for log space; **M01 stops short of the log-sum-exp identity and this page owns
it**, per the boundary M01's own brief proposes. M03 for the dot product, since logits are a
matrix-vector product. M05 for the chain rule and the gradient.

## Beats, in order

1. **One-minute version.** `softmax(z)_i = e^{z_i} / sum_j e^{z_j}`. Adding a constant to every
   logit changes nothing. It is a softened **argmax**, not a softened max. You never evaluate it
   as written: `LSE(z) = a + log sum_j e^{z_j - a}` with `a = max z`. And the loss gradient is `p - y`.
2. **Orientation figure.** M03's dot product produces logits, into "this page: logits become a
   probability vector, safely", into 0181 (which scores it), 0190 (which reports it) and M06
   (which descends on the gradient it produces).
3. **Mental model.** Exponentiate to make everything positive, then divide by the total to make it
   sum to one. Two steps, no magic. Bar chart before and after.
4. **Mechanism, with arithmetic.** Logits `[2.0, 1.0, 0.1]` become `[0.6590, 0.2424, 0.0986]`.
5. **Shift invariance**, proved in one line by cancelling `e^c`, then shown numerically: add 137 to
   every logit and the output is unchanged to 6.6e-15. **Named identity, see proof.**
6. **The name is wrong, key callout.** *Deep Learning* 6.2.2.3: "It would perhaps be better to call
   the softmax function 'softargmax,' but the current name is an entrenched convention." The soft
   version of `max(z)` is `softmax(z) . z`, a scalar. Once the reader knows it is a smoothed argmax,
   `T -> 0` giving one-hot stops being a fact to memorise.
7. **Where softmax comes from**, one paragraph so it does not look invented: it is the
   natural-parameter form of the multinomial in the exponential family, PRML eq 2.213, "the
   normalized exponential", exactly as the logistic sigmoid is the same construction for the
   Bernoulli. Sigmoid is softmax over two classes with one logit pinned at zero.
8. **The failure, with real thresholds.** Blanchard, Higham and Higham table 2: `log r_max` is
   **11.0 for float16**, 88.7 for bfloat16 and float32, 710 for float64. Half precision is the
   ordinary inference precision. On the committed dataset **28.7 per cent of rows carry a logit
   above 11.0** and the naive route returns not-a-number on 5,586 of 20,000 rows.
9. **The shift, and why it is legal.** `log sum e^{z_i} = a + log sum e^{z_i - a}` for any real `a`.
   With `a = max z` the largest exponent is exactly zero, so nothing overflows, and at least one
   term equals 1, so the denominator cannot underflow to zero.
10. **The loss in one line.** `-log softmax(z)_y = -z_y + LSE(z)`. Same number, two routes, one of
    which cannot overflow. Worked below.
11. **The loop this page closes, key callout. The gradient of log-sum-exp IS the softmax.** So
    `d/dz_j (-z_y + LSE(z)) = p_j - 1[j = y]`, the famous `p - y`. Two of M05's tools, one line,
    the single most reused derivative in the field. **Named theorem, see proof.**
12. **Temperature.** `softmax(z/T)`. `T -> 0` is the hard argmax, `T -> infinity` is uniform, and
    the argmax never moves at any `T`. Hinton, Vinyals and Dean eq 1, with their `1/T^2`
    gradient-scaling correction named.
13. **Warning callout, one only.** The division-free form `g_j = exp(z_j - LSE(z))`, used by SciPy
    1.4.1 and the PRML companion code, "can suffer from loss of accuracy" per Blanchard et al. The
    shifted forms are fine; that specific rewrite is not.
14. **Trade-off, same section.** Softmax has `k` outputs and `k - 1` degrees of freedom, so a single
    logit is not readable as a score and saturation is about *differences* becoming extreme.
    Computing the loss from probabilities rather than logits throws away precision that cannot be
    recovered downstream, which is why the framework API takes logits.

**Do not do here:** attention, mixture-of-experts routing, calibration methods beyond naming
temperature scaling.

## The stated proofs (D4)

**Identity (shift invariance).** For any real `c`, `softmax(z + c1) = softmax(z)`, and
`LSE(z + c1) = LSE(z) + c`.

*Proof, in full.* `e^{z_i + c} = e^{z_i} e^{c}`, so both numerator and denominator of the softmax
pick up the same factor `e^c` and it cancels. For `LSE`,
`log sum_j e^{z_j + c} = log (e^c sum_j e^{z_j}) = c + log sum_j e^{z_j}`. Setting `c = -max_j z_j`
gives the computational form. **The step that does the real work** is that `e^c` is a *common*
factor, which is true only because the shift is the same in every coordinate. A per-coordinate
shift is not free and does change the answer.

**Theorem.** `d LSE(z) / d z_j = softmax(z)_j`, and therefore, for the cross-entropy loss
`L(z) = -z_y + LSE(z)` with a one-hot label `y`, `dL/dz_j = softmax(z)_j - 1[j = y]`.

*Proof, in full.* Differentiate `LSE(z) = log sum_m e^{z_m}` with respect to one coordinate. The
chain rule on `log u` gives `1/u` times `du/dz_j`, and only the `m = j` term of the sum depends on
`z_j`:

```
d/dz_j  log sum_m e^{z_m}  =  (1 / sum_m e^{z_m}) * e^{z_j}  =  e^{z_j} / sum_m e^{z_m}  =  softmax(z)_j
```

The loss adds the term `-z_y`, whose derivative with respect to `z_j` is `-1` when `j = y` and `0`
otherwise, which is exactly `-1[j = y]`. Adding the two gives `p_j - 1[j = y]`.

**The step that does the real work** is noticing that the denominator of the softmax is the *same*
`sum_m e^{z_m}` that `LSE` takes the log of. The softmax is not something extra you differentiate
through; it falls out of `1/u` times `du/dz_j` and nothing else happens.

**Two checks the page should state.** First, the gradient sums to zero over `j`, because the
probabilities sum to one and the one-hot sums to one. That must be true: shift invariance says the
loss cannot see a constant added to a whole row, so it can have no gradient in that direction.
Second, the code file verifies both derivatives against central differences and the largest
disagreement over twelve rows is 1.6e-9.

## Planned figures

1. **Orientation, `flowchart LR`,** as beat 2.
2. **`sequenceDiagram`, the overflow step by step.** Participants Logits, exp, sum, divide. Messages
   showing `[800, 801, 802]` becoming `inf, inf, inf`, then `inf`, then `nan`; then the same run
   with the shift. The right kind, because the reader's confusion is about *at which step* it
   breaks. **No semicolons anywhere in the message text** - fatal in a sequenceDiagram.
3. **`svg.chart`, the precision ceilings.** A bar per format at its `log r_max` on a log axis:
   float16 11.0, bfloat16 and float32 88.7, float64 710, with the dataset's own logit range marked.
4. **`svg.chart`, temperature.** Grouped bars for `T = 0.25, 0.5, 1, 2, 5` over one real row of
   logits, with the argmax marked and unchanged in every group.
5. **`flowchart TB`, the gradient loop drawn as a loop.** `LSE(z)` -> differentiate -> `softmax(z)`
   -> feeds the loss -> `-z_y + LSE(z)` -> differentiate -> `p - y`. Kills "the softmax gradient is
   a messy special case".

## The worked example, with its numbers

The same loss two ways, then the cliff. Eight parts, derived, plus one quoted threshold.

1. Logits `z = [2.0, 1.0, 0.1]`, true class 0.
2. Naive: `exp(z) = [7.3891, 2.7183, 1.1052]`, sum `11.2126`, `q = [0.6590, 0.2424, 0.0986]`,
   loss `-ln 0.6590 = 0.4170` nats.
3. Stable: `a = 2.0`; shifted `[0, -1, -1.9]`; `sum e = 1 + 0.3679 + 0.1496 = 1.5175`.
4. `LSE = 2.0 + ln 1.5175 = 2.4170`.
5. Loss `= -z_y + LSE = -2.0 + 2.4170 = 0.4170` nats. **The same number.**
6. Now `z = [800, 801, 802]`. The naive route overflows even in float64 and returns `nan`. The
   stable route gives `LSE = 802.4170` and the loss for class 2 is `0.4170` again, because softmax
   sees only differences.
7. **Sanity check.** `LSE(z)` must always lie between `max z` and `max z + log k`. Here
   `2.0 <= 2.4170 <= 2.0 + ln 3 = 3.0986`. If your `LSE` came out below the maximum logit, you
   subtracted the shift and forgot to add it back.
8. **What changes if** you run this in float16? **Quoted:** `log r_max` for float16 is 11.0
   (Blanchard, Higham and Higham, table 2). On `m10_classifier.csv`, 28.7 per cent of rows carry a
   logit above that and the naive route returns `nan` on 5,586 of 20,000. The shifted route is
   finite on all 20,000, with a largest error against float64 of 2.0e-3.
9. The gradient, from the same numbers: `p - y = [0.6590 - 1, 0.2424, 0.0986] =
   [-0.3410, 0.2424, 0.0986]`, which sums to zero as it must.

**A note the page must carry.** The dataset has 5,746 rows above 11.0 but only 5,586 produce `nan`.
The published 11.0 is `log r_max` rounded to three significant figures; `exp` actually overflows
float16 at `ln 65504 = 11.0899`, so the 160 rows in between survive. Say this. A course that hides
a 3 per cent discrepancy teaches the reader not to check.

## Quiz seeds

- **Q1 (misconception, M4 "softmax is a soft max").** Softmax is a smooth version of which
  function? **Answer: argmax.** Distractors: max; the sigmoid; normalising by the sum.
- **Q2.** Why does every implementation subtract `max(z)` before exponentiating? **Answer: so the
  largest exponent is zero, which makes overflow impossible and guarantees one term equals 1.**
  Distractors: to make the probabilities sum to one (they already do); to centre the logits; to
  make the exponential faster.

## Practice seed

**Stem.** A model produces logits `[12.0, 9.0, 3.0]` and the computation runs in float16, where
`exp` overflows above about 11.09. The true class is 0. (a) Say what the naive route returns and at
which step it first fails. (b) Compute the loss the stable way. (c) Compute the gradient with
respect to all three logits and check it sums to zero.

**Hint.** In (a), work out `exp(12.0)` before you look at anything else.

**Solution.** (a) `exp(12.0) = 162754`, above float16's largest finite value of 65504, so it becomes
`inf` at the very first exponential, before any summation. The denominator becomes `inf`, the
division gives `nan`, and the loss is `nan`. (b) `a = 12.0`; shifted `[0, -3, -9]`;
`sum e = 1 + 0.049787 + 0.00012341 = 1.049910`; `LSE = 12.0 + ln 1.049910 = 12.048703`;
loss `= -12.0 + 12.048703 = 0.048703` nats. (c) `p = [0.952465, 0.047420, 0.000118]`;
`p - y = [-0.047535, 0.047420, 0.000118]`; the sum is 0.000003, zero to rounding.

**`.p-check`.** The loss must be small and positive, because the model put 95 per cent on the right
class. If you got a number above `ln 3 = 1.0986` you have done worse than a uniform guess, which
these logits cannot produce.

## Code and dataset plan

`code/0184-softmax-log-sum-exp.py` against `m10_classifier.csv`. Naive against shifted in float64
and again in float16; shift invariance; the `log softmax = z - LSE` identity to 3.6e-15 over
100,000 entries; **both gradients checked against central differences**; and the temperature table.

## Sources, primary only

- Goodfellow, Bengio and Courville, *Deep Learning* (2016) sections 4.1, 6.2.2.3, eq 4.1, 6.29-6.33.
- Blanchard, D. J. Higham and N. J. Higham, *Accurately computing the log-sum-exp and softmax
  functions*, IMA J. Numer. Anal. 41(4) (2021), table 2, eq 1.2 and 1.3, and the division-free
  warning. https://webhomes.maths.ed.ac.uk/~dhigham/Publications/P149.pdf
- Bishop, *PRML* (2006) eq 2.213 and 2.226.
- Hinton, Vinyals and Dean, *Distilling the Knowledge in a Neural Network* (2015) eq 1.
  https://arxiv.org/pdf/1503.02531

## Primary source to go deeper

Blanchard, Higham and Higham 2021. Twenty pages of rounding-error analysis on the one function
every classifier calls.
