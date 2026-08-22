# M06 L09 - Saddle points and plateaus: what actually slows deep training

**Page `lessons/0108-saddle-points-and-plateaus.html`** &middot; module M06, lesson 9 of 12 &middot; program `code/0108-saddle-points-and-plateaus.py` &middot; dataset `datasets/m06-credit.csv`

## The single tight idea

In high dimensions a point with a zero gradient is almost never a local minimum; it is a saddle, and the plateau around it is what a stalled training curve usually is.

## Prerequisites

| Needs | From |
|---|---|
| The Newton step, and that it needs `H` positive definite | M06 L08 |
| **Eigenvalues, and the sign pattern of a symmetric matrix's spectrum** | M04 |
| Convexity, so "no local minimum but the global one" is a contrast the reader already owns | M06 L02 |

## Beats, in order

1. **Classify a critical point by the signs of the Hessian's eigenvalues.** All positive, a minimum. All negative, a maximum. Mixed, a saddle: a minimum along one cross-section and a maximum along another. Draw it before writing it.
2. **The counting argument**, in the source's own coin-flip form, proved below.
3. **The second half, which is the good news and gets skipped.** Eigenvalues become more likely to be positive in regions of lower cost, so "local minima are much more likely to have low cost than high cost" and "critical points with high cost are far more likely to be saddle points". Empirically confirmed for real networks. **The local minimum you actually land in is usually a fine one.** This is the page's key callout, and it is what dissolves the folk fear.
4. **What a plateau costs.** The gradient is small but not zero over a wide region, so progress is slow without ever stopping. That is a flat stretch in a training curve, and it is not a local minimum.
5. **The twist that closes L08.** Newton rescales each direction by the inverse eigenvalue, so along a negative-curvature direction it steps *opposite* to gradient descent, "in the direction of increasing error", and "the saddle point becomes an attractor for the Newton method".
6. **The diagnostic the reader can run.** Plot the gradient norm. "If the norm of the gradient does not shrink to insignificant size, the problem is neither local minima nor any other kind of critical point."
7. **Honest limit, in a `.callout.warn`.** This is random-matrix theory plus experiments on particular networks, not a theorem about the network in front of you.

## Named theorems and their stated proofs (D4)

**Result 1 (the saddle-to-minimum ratio, under the coin-flip model).**
*Model, stated as a model.* At a critical point of a random function of `n` variables, treat the `n` eigenvalue signs as independent fair coin flips. This is the idealisation Goodfellow et al. use to carry the intuition; the real statement needs random-matrix theory and is cited, not proved.
*Under that model:* a local minimum needs all `n` signs positive, which has probability `2^-n`. A saddle needs at least one of each sign, which has probability `1 - 2*2^-n`.
So the expected ratio of saddles to minima is `(1 - 2^(1-n)) / 2^-n = 2^n - 2`, which **grows exponentially in `n`**. **QED, under the stated model.**
Numbers for the page: at `n = 2` the ratio is 2. At `n = 10` it is 1,022. At `n = 50` it is about `1.1e+15`. At the parameter count of even a small network it is a number with no name.
**The page must say plainly that the coin-flip independence is an idealisation.** Real Hessian spectra are not independent coin flips; what the sources establish is that the conclusion survives the more careful treatment.

**Result 2 (Newton is attracted to a saddle).**
Work in the eigenbasis of the Hessian at a critical point `x*`, and write a displacement as `d = sum_i d_i * e_i`. Near `x*` the gradient along `e_i` is approximately `lambda_i * d_i`.
*Gradient descent* moves by `-eta * lambda_i * d_i`. When `lambda_i < 0` this has the same sign as `d_i`, so the step grows `|d_i|`: it moves **away** from `x*` along the negative-curvature direction, which is what you want.
*Newton* moves by `-(1/lambda_i) * lambda_i * d_i = -d_i`. That is towards `x*` along **every** direction, whatever the sign of `lambda_i`, because dividing by a negative eigenvalue flips the step exactly as often as the eigenvalue flipped the gradient.
So the Newton step drives every coordinate of the displacement to zero, and `x*` is an attracting fixed point of the iteration. **QED**
This is a five-line argument with a large payoff, and it is the page's reason to exist alongside L08.

## Planned figures

1. **Orientation, `flowchart`.** "L08: Newton needs a positive-definite Hessian" into "THIS PAGE - in high dimensions the critical points are saddles, not minima" into "so a stalled curve is a plateau, and it will move", with "what a deep network's loss landscape is actually like" dotted in.
2. **`svg.chart`.** A saddle in contours, `f-prob` below the critical value, with two paths from the same start: gradient descent in `s-signal` leaving along the descending direction, Newton in `s-alarm` walking into the saddle. Kills "second-order methods would escape faster", which is exactly backwards.
3. **`svg.chart`.** Saddle-to-minimum ratio `2^n - 2` against `n` on a log y-axis, with three real parameter counts marked. Kills the intuition transferred from two-dimensional pictures, where local minima genuinely are everywhere.
4. **`svg.chart`.** Three gradient-norm traces against step: a plateau flat then falling in `s-signal`, a genuine convergence decaying in `s-stat`, a divergence rising in `s-alarm`. Kills the habit of diagnosing a flat loss curve by staring at the loss curve.

## The worked example, in eight parts

Reading a flat training curve correctly, then proving the diagnosis on a real saddle.

1. The situation: training loss flat for 2,000 steps.
2. Candidate one, a local minimum. Almost certainly not, by Result 1 and by the low-cost argument in beat 3.
3. Candidate two, a saddle or plateau. Likely: the gradient norm is small but not zero, and it will move.
4. Candidate three, not a critical point at all. Also likely, and the commonest in practice.
5. Candidate four, a learning rate past `2/L`. Ruled out by L04's picture, because that diverges rather than flattening.
6. **The test that separates them**: if the gradient norm has not shrunk to insignificance, candidates one, two and four are all out at once.
7. Now demonstrate it. On the explicit saddle `f(x, y) = x^2 - y^2` from `(0.01, 0.01)`, gradient descent leaves along `y` and Newton converges to `(0, 0)` - the saddle - to machine precision. The Hessian there is `diag(2, -2)`: one sign each, so it is a saddle by definition and not by inspection.
8. **The sentence to carry: one logged quantity separates three situations that look identical on the loss curve.** The action is to log the gradient norm, not to stare at the loss.

## Quiz seeds

**Q1 (misconception).** In a network with many parameters, a point with zero gradient is most likely a saddle point with mixed Hessian eigenvalue signs.
Distractors: a global minimum (the surface is not that kind); a local maximum (rarer still, needing all `n` negative); **"a local minimum with much worse loss than the best"** - the folk belief this page exists to kill, since critical points at high cost are far more likely to be saddles.

**Q2.** Your training loss has been flat for 2,000 steps. What do you log first?
Correct: the gradient norm. Distractors: the validation loss, the weight histogram, the learning rate. All three are reasonable *later* checks, and the feedback must say so - each answers a narrower question than the flat curve raised.

## Practice seed

**Stem.** Three runs, all with a flat loss. Run A's gradient norm is steady at 0.4. Run B's has decayed to `1e-7`. Run C's is climbing past `1e3`. Diagnose each and name the next action.
**Hint.** Apply the one test before you consider anything else, and notice it splits the three immediately. Then, for the run it does not settle, ask which of L04's four regimes produces a loss that stops changing while a gradient keeps growing.
**Solution.** A: not a critical point, so the flat loss has another cause - a plateau, or a step too small for the local curvature. Raise the learning rate or wait. B: a genuine critical point; given the dimension it is far more likely a flat minimum than anything worrying. Stop, or decay and confirm. C: divergence, L04's `eta > 2/L`, and the flat loss is a saturated or overflowing value rather than a real one. Lower the learning rate immediately.
**`.p-check`.** Your three diagnoses must be three *different* ones. If two come out the same you have used the loss curve, which is identical in all three runs, rather than the gradient norm, which is not.

## Code and dataset

**Program:** `code/m06-09-saddle.py`. **Dataset:** none needed for the saddle itself; `datasets/m06-credit.csv` for the gradient-norm traces.
**What it computes twice:** the character of a critical point, once by the eigenvalue signs of the analytic Hessian and once by sampling the objective on a small sphere around the point and checking that some directions rise and some fall. The two must agree. The sampling route is what you can do when you cannot form a Hessian, which is the real case, so seeing it agree with the eigenvalues on a problem where both are available is the point. The program also runs Result 2 directly: gradient descent and Newton from the same start near `(0,0)` on `x^2 - y^2`, reporting that one leaves and the other arrives.

## Sources, primary only

- Goodfellow, Bengio & Courville, ch. 8, sections 8.2.2 and 8.2.3, for the coin-flip argument, the low-cost result, and the gradient-norm test.
- Dauphin, Pascanu, Gulcehre, Cho, Ganguli & Bengio, arXiv:1406.2572, section 3, for the experimental confirmation and for the Newton-as-attractor argument.
- **Not opened, so not cited on the page:** Choromanska et al. (2015), which Goodfellow et al. cite as additional theoretical support. If a writer wants it, open it first.
