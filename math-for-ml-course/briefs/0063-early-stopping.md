# M06 L12 - Early stopping is the regularizer you did not write

**Page `lessons/0063-early-stopping.html`** &middot; module M06, lesson 12 of 12 &middot; program `code/0063-early-stopping.py` &middot; dataset `datasets/m06-credit.csv`

## The single tight idea

Stopping training early confines the parameters to a region around where they started, which is L2 regularization applied with the clock instead of the loss.

## Prerequisites

| Needs | From |
|---|---|
| Regularization as a constraint region | M06 L11 |
| The update rule, and that `eta` bounds one step | M06 L03 |
| Training against validation loss, and why they diverge | M09 owns the generalization story - **one cross-link line, no derivation** |

## Beats, in order

1. **The observation first.** Training loss falls monotonically, validation loss falls and then turns up. The turn is the stopping point. Draw it before explaining it.
2. **The mechanism.** `tau` steps at rate `eta` can only reach so far from `theta_0`, so `tau*eta` is a measure of effective capacity. Proved below.
3. **The equivalence, with its conditions said out loud before its conclusion.** A linear model, a quadratic error surface, plain gradient descent, a small step size. Under exactly those, `tau*eta` behaves as the reciprocal of the weight-decay coefficient. **A deep network satisfies none of the four**, so this is an explanation of the mechanism, not a licence to substitute one for the other.
4. **The mechanics that make it work.** A patience window, restoring the **best** checkpoint rather than the last one, and why the validation curve's noise means the first uptick is not the signal.
5. **The costs, which the usual account omits.** Early stopping spends validation data. The stopping point is itself a parameter fitted on that data. And it couples to L04's schedule, because `tau*eta` is a product and halving one is not the same as halving the other when `eta` is not constant.
6. **Trade-off.** The cheapest regularizer there is - one extra evaluation loop - and the one whose hyperparameter does not transfer between runs.

## Named theorem and its stated proof (D4)

**Result 1 (a step budget bounds the reachable region).**
If every gradient is bounded, `||grad J(theta)|| <= G`, then after `tau` steps of size `eta` from `theta_0`,
`||theta_tau - theta_0|| = ||sum_{k=1..tau} eta * grad J(theta_{k-1})|| <= sum_{k=1..tau} eta*||grad J(theta_{k-1})|| <= tau*eta*G`
by the triangle inequality. **QED**
So the reachable set is a ball of radius `tau*eta*G` around the initialisation. **That is a constraint region, and L11 proved a constraint region is a penalty.** The two pages meet exactly here.

**Result 2 (early stopping equals L2, under four conditions).**
*Conditions, stated first because they are the result's real content:* (i) the model is linear in its parameters, (ii) the error surface is quadratic, `J~(w) = J(w*) + 0.5*(w - w*)'H(w - w*)`, (iii) plain gradient descent with a constant `eta` from `w_0 = 0`, (iv) `eta` small enough that `|1 - eta*lambda_i| < 1` for every Hessian eigenvalue, and (v) for the closing approximation only, **`eta*lambda_i << 1` and `lambda_i/alpha << 1`** for every `i`.

*Proof.* The gradient of the quadratic model is `H*(w - w*)`, so the iteration is
`w_tau - w* = (I - eta*H)*(w_{tau-1} - w*)`, and from `w_0 = 0`, `w_tau - w* = (I - eta*H)^tau * (-w*)`.
Diagonalise `H = Q*Lambda*Q'`. In the eigenbasis each coordinate evolves independently, and condition (iv) is what makes the power converge:
`Q'w_tau = [ I - (I - eta*Lambda)^tau ] * Q'w*`.
Now take the L2 solution from L11 Result 2, `Q'w~ = (Lambda + alpha*I)^-1 * Lambda * Q'w*`, and rearrange it into the same shape using `lambda/(lambda + alpha) = 1 - alpha/(lambda + alpha)`:
`Q'w~ = [ I - (Lambda + alpha*I)^-1 * alpha ] * Q'w*`.
Comparing the two bracketed factors, early stopping at `tau` steps and L2 with coefficient `alpha` give the same answer exactly when
**`(I - eta*Lambda)^tau = (Lambda + alpha*I)^-1 * alpha`.**
That is the equivalence. Everything after it is an approximation, and the page must mark the transition.
Componentwise, `(1 - eta*lambda)^tau = alpha/(lambda + alpha)`. Take logarithms:
`tau * log(1 - eta*lambda) = -log(1 + lambda/alpha)`.
Apply `log(1 + x) ~ x` on each side, which needs **both** halves of condition (v): `log(1 - eta*lambda) ~ -eta*lambda` needs `eta*lambda << 1`, and `log(1 + lambda/alpha) ~ lambda/alpha` needs `lambda/alpha << 1`.
That gives `tau * eta * lambda ~ lambda/alpha`, and the `lambda` cancels:
**`tau ~ 1/(eta*alpha)`, equivalently `alpha ~ 1/(tau*eta)`.** **QED, under (i) to (v).**

**The direction of condition (v) is easy to get backwards and the page must state it as the source does:** the approximation needs the eigenvalues small *relative to `alpha`*, not `alpha` small relative to the eigenvalues. The exact equivalence above holds without it; only the tidy reciprocal needs it.

*Measured, so the writer does not have to trust the warning.* Solving `(1 - eta*lambda)^tau = alpha/(lambda + alpha)` for `tau` exactly at `eta = 1e-3`, against the approximation `1/(eta*alpha)`:

| `lambda` | `alpha` | `lambda/alpha` | exact `tau` | `1/(eta*alpha)` | ratio |
|---|---|---|---|---|---|
| 0.001 | 1.0 | 0.001 | 999.5 | 1000.0 | 0.999 |
| 0.01 | 1.0 | 0.01 | 995.0 | 1000.0 | 0.995 |
| 0.1 | 1.0 | 0.1 | 953.1 | 1000.0 | 0.953 |
| 1.0 | 1.0 | 1 | 692.8 | 1000.0 | 0.693 |
| 1.0 | 0.001 | 1000 | 6,905 | 1,000,000 | **0.007** |

In the regime the source names the approximation is good to a fraction of a per cent. With the condition inverted - `alpha` small relative to `lambda`, which is the natural misreading - it is wrong by a factor of 145. **This table is a candidate figure for the page**, because it is the honest version of "under these assumptions", and it costs four rows.

**The sentence the page must carry immediately after the proof:** every one of the four conditions fails for a deep network - the model is not linear, the surface is not quadratic, the optimizer is not plain gradient descent, and `eta` is not constant. The equivalence explains *why* a step budget regularises. It does not let you convert a patience setting into a weight-decay coefficient.

## Planned figures

1. **Orientation, `flowchart`.** "L11: regularization is a constraint on the weights" into "THIS PAGE - a step budget is also a constraint on the weights" into "how to actually pick the stopping step", with "the cheapest regularizer there is" dotted in.
2. **`svg.chart`.** Training loss in `s-signal` falling monotonically, validation loss in `s-plum` falling then turning up, the validation minimum in `m-gold`, the patience window shaded `f-prob`, the region past the stop shaded `alarm`. Kills "stop when the training loss stops improving", which is the wrong curve.
3. **`svg.chart`.** Distance travelled from `theta_0` against step count, with rings at fixed radii showing `tau*eta*G` bounding the reachable radius, drawn beside an L2 ball of matching radius. Kills early stopping read as impatience rather than as a constraint.
4. **`stateDiagram-v2`.** `improving` to `waiting (patience k)` to either `improving` again or `stop and restore best`, with the transitions labelled by the counter. Kills the off-by-one that makes people restore the *last* checkpoint instead of the best one.

## The worked example, in eight parts

Picking the stopping step from a validation curve, and finding the trap.

1. The curve, eleven epochs: `0.90, 0.72, 0.61, 0.55, 0.52, 0.53, 0.51, 0.54, 0.55, 0.56, 0.58`.
2. Track two things only: the running best, and the number of epochs since it improved.
3. Epoch 5 sets `0.52`. Epoch 6 fails once.
4. Epoch 7 improves to `0.51`, which resets the counter.
5. Epochs 8 and 9 fail twice, so **patience 2 stops at epoch 9 and restores epoch 7**.
6. With patience 5 the counter runs from epoch 8 to epoch 11 and only reaches 4, so it **never fires** within this data.
7. **The trap.** At patience 1, epoch 6's single bad step ends the run at epoch 6 and restores epoch 5 at `0.52` - missing the genuinely better epoch 7 at `0.51`.
8. **The sentence to carry: patience buys tolerance for a noisy curve, and setting it too low throws away real improvements.** It is a hyperparameter fitted on the validation set like any other, which is beat 5's cost made concrete.

**Labelling note.** This curve is synthetic and the page must say so. No citable real validation curve was found during the analysis phase, and inventing an attribution would fail the sourcing bar.

## Quiz seeds

**Q1 (misconception).** Early stopping behaves like L2 regularization because a step budget bounds how far the weights leave the start.
Distractors: it shrinks each weight by a fixed amount every epoch; it adds a penalty term once the validation loss turns - **both invent a penalty term that early stopping never adds**, which is the whole point of calling it the regularizer you did not write; it selects the smallest-norm model seen (a rule nobody runs).

**Q2.** When early stopping fires after the patience window, you keep the best weights, from the epoch that set the minimum.
Distractors: the final ones (**the off-by-`patience` bug, and the commonest one in hand-rolled loops**); the average across the window (weight averaging, a different technique); the epoch just before the loss turned up - **the subtle one**, since with a noisy curve that epoch and the best epoch are often the same and are not guaranteed to be.

## Practice seed

**Stem.** Given the eleven-epoch curve above, apply patience 2 and then patience 5. For each, give the epoch training stops and the epoch whose weights are restored. Then say what patience 1 would have cost.
**Hint.** Keep two counters and nothing else: the best value so far, and epochs since it changed. Reset the second the moment the first changes, and do not reset it for an epoch that merely ties.
**Solution.** Patience 2 stops at epoch 9 and restores epoch 7 at `0.51`. Patience 5 never fires within the data; the best remains epoch 7. Patience 1 stops at epoch 6 and restores epoch 5 at `0.52`, losing the better epoch 7 entirely - a `0.01` worse model, bought by impatience.
**`.p-check`.** The restored epoch must never be later than the stopping epoch, and the gap between them must be exactly your patience value whenever the run fires. If the gap is smaller you have reset the counter on a tie.

## Code and dataset

**Program:** `code/m06-12-early-stopping.py`. **Dataset:** `datasets/m06-credit.csv`, split into train and validation with a fixed seed.
**What it computes twice:** the regularization strength that early stopping is applying, once as `1/(tau*eta)` from the stopping step, and once by fitting an explicit L2-regularised model and searching for the `alpha` whose coefficients best match the early-stopped ones. On a linear model with a quadratic loss the two must land close, which is Result 2 turned into a measurement. The program then repeats it on a model with a hidden nonlinearity and reports that they **do not** match - which is the honest half, and is what stops the equivalence being carried where it does not belong.

## Sources, primary only

- Goodfellow, Bengio & Courville, ch. 7, section 7.8, for the `tau*eta` capacity argument, the four conditions, and the quadratic-approximation route the proof above follows. The section attributes the volume argument to Bishop (1995a) and Sjoberg & Ljung (1995), **neither of which was opened** - so the page cites Goodfellow et al. for the statement and names the two originals as its sources, without claiming to have read them.
