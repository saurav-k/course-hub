# 0048 - A long chain of Jacobians: what backprop costs, and how the signal decays

> Number claimed under #42 from the roadmap count in `../index.html`. Report label C08.

| | |
|---|---|
| Module | M05 Calculus |
| Rung | frontier (`pill hard`) |
| Label | `depth` |
| Prerequisites | 0046, 0047. |
| Enables | nothing in this module; it motivates clipping, residual connections and gated cells, all owned elsewhere |

## The single tight idea

The gradient costs about what the forward pass costs in time, far more in memory, and the
signal travelling a long chain decays or explodes geometrically.

## Beats, in order

1. **The cost result, quantitative and cited.** For `f : R^n -> R^m`, forward mode
   computes the Jacobian in `n c ops(f)` and reverse mode in `m c ops(f)`, with `c < 6`
   guaranteed and `c` typically in `[2, 3]`.
2. **Apply it.** Machine learning has one scalar loss and millions of parameters, so
   `m = 1` and `n` is huge, and reverse mode wins by a factor of `n`. That single
   inequality is why backpropagation exists and why forward mode does not.
3. **What you pay instead.** Memory grows with the number of operations, because every
   intermediate a backward rule needs must be kept alive. Name activation checkpointing
   as the trade of recompute against memory, and stop there.
4. **Backpropagation against symbolic differentiation against finite differences,** in
   one table. It is neither, and confusing it with either produces a wrong mental model
   of what it costs.
5. **The decay.** A gradient reaching back `k` steps is multiplied by a product of `k`
   Jacobians. Products of matrices shrink or blow up, and the base is what to look at.
6. **The condition, stated exactly and proved.** With `|sigma'| <= gamma`, long-term
   contributions vanish when the recurrent matrix's largest eigenvalue satisfies
   `lambda_1 < 1/gamma`. For `tanh`, `gamma = 1`. For the logistic sigmoid,
   `gamma = 1/4`, so vanishing is guaranteed for any `lambda_1 < 4`.
7. **Close by naming what this motivates without teaching it:** gradient clipping,
   residual connections, gated recurrent cells. One sentence each, no mechanism.

## Named results and their stated proofs

**Result 1 (the mode-cost bound).** Stated, attributed, not proved here.

> For `f : R^n -> R^m` with operation count `ops(f)`, the `m x n` Jacobian costs
> `n c ops(f)` by forward mode and `m c ops(f)` by reverse mode, where `c < 6` and
> typically `c` is in `[2, 3]`.
>
> This is Griewank and Walther's result as quoted by Baydin et al. (2018), section 3.
> **This page states it and does not prove it**, because the proof is an operation count
> over an evaluation trace and belongs to the automatic-differentiation literature rather
> than to a calculus module. What the page owes instead, and delivers, is a measurement:
> the program runs both modes on the same function and reports the observed ratio.
> Under D4 a stated proof is owed for a named theorem; this is a named bound whose proof
> is out of scope, and saying so plainly is the honest move.

**Result 2 (the vanishing-gradient condition).** Proved, because the proof is four lines
and it is the reason the condition has the shape it does.

> Consider `x_{k+1} = sigma(W x_k)` with `|sigma'(u)| <= gamma` for all `u`. Suppose the
> largest singular value of `W` satisfies `lambda_1 < 1/gamma`. Then the contribution of
> step `k` to the gradient at step `t` decays exponentially in `t - k`.
>
> *Proof.* The one-step Jacobian is `d x_{k+1} / d x_k = diag(sigma'(W x_k)) W`, whose
> operator norm obeys
>
>   `|| d x_{k+1}/d x_k || <= || diag(sigma'(W x_k)) || * || W || <= gamma * lambda_1 =: eta < 1`,
>
> using submultiplicativity of the operator norm and the fact that a diagonal matrix's
> operator norm is the largest absolute entry. The contribution of step `k` carries the
> product of `t - k` such factors, so by induction on `t - k`
>
>   `|| prod_{i=k}^{t-1} d x_{i+1}/d x_i || <= eta^(t-k)`,
>
> and since `eta < 1` this tends to zero exponentially fast in `t - k`. **QED**
>
> **What the converse does and does not say.** Reversing the argument gives that
> `lambda_1 > 1/gamma` is *necessary* for the gradient to explode, not sufficient. The
> program demonstrates the gap directly: at spectral radius exactly `1.00`, a random unit
> gradient pushed through thirty independent Jacobians still arrives with norm `0.063`.
> The radius bounds the largest growth any direction can see; a typical direction does
> worse. Say this on the page. It is the difference between the theorem and the slogan.

## Figures

1. **Orientation, `flowchart LR`.** "Backpropagation works (0047)" into "THIS PAGE: what
   it costs and where it breaks" into "clipping, residuals and gated cells".
2. **`svg.chart`, quantitative, log axis.** Two bars: Jacobian cost by forward mode and by
   reverse mode for `n = 10^7` parameters and `m = 1` loss at `c = 3`. Seven orders of
   magnitude apart. *Kills:* "backpropagation is one way among several".
3. **`svg.chart`, quantitative, log axis.** Gradient magnitude against depth for
   `lambda_1 gamma` of `0.9`, `1.0` and `1.1` over thirty layers.
   *Kills:* "vanishing gradients are about the sigmoid being flat". They are about a
   geometric product, and the base is the thing to look at.
4. **`flowchart TD`.** Memory: store every activation, against checkpoint every k-th and
   recompute. Two paths with the trade written on each.
   *Kills:* "out of memory at batch size 33 is a mystery".
5. **`quadrantChart`.** Four differentiation methods on accuracy against scalability: by
   hand, symbolic, finite differences, reverse-mode autodiff. Keep every point label under
   26 characters. *Kills:* both AD misconceptions in one picture.

## Worked example, in eight parts

1. **Setting.** A thirty-layer network whose per-layer Jacobian has largest singular
   value `0.9`. How much of the gradient reaches layer one?
2. **Symbolic.** `.math` for the product of Jacobians and the bound `eta^(t-k)`, with a
   `.gloss` naming `eta`, `gamma`, `lambda_1`, `t`, `k`.
3. **Picture.** Figure 3, before the arithmetic.
4. **`ol.worked`.** `0.9^30 = 0.0424`, a 24-fold shrink. `1.1^30 = 17.45`, a 17-fold
   growth. `1.0^30 = 1`, nothing happens. The base is what matters and the exponent is
   the depth.
5. **`.keynum`** on `gamma = 1` and `gamma = 1/4`, which are quoted from Pascanu et al.,
   and on nothing else.
6. **Sanity check.** `0.9^30` must be between `0.9^40 = 0.0148` and `0.9^20 = 0.122`, and
   `0.0424` is. Any answer above `0.9` or below `0.001` is an exponent error.
7. **What changes if** the activation is the logistic sigmoid rather than `tanh`?
   `gamma` drops from `1` to `1/4`, so the vanishing threshold rises from `lambda_1 < 1`
   to `lambda_1 < 4`. Almost any sensibly initialised recurrent matrix is below `4`, which
   is why the field abandoned sigmoid recurrent units rather than tuning them.
8. **In words.** Depth multiplies. Nothing about a single layer is pathological, and
   thirty of them in a row is.

## Quiz seeds

**Q1.** For a scalar loss over `n` parameters, how many reverse-mode sweeps does the full
gradient need?
*Answer:* one.
*Distractors:* "`n`" is the forward-mode count and is the trap; "two" confuses sweeps with
phases; "it depends on the depth" confuses cost per sweep with number of sweeps.

**Q2, misconception.** A recurrent network uses the logistic sigmoid, so
`|sigma'| <= 1/4`. Vanishing gradients are guaranteed when the largest eigenvalue of the
recurrent matrix is below what?
*Answer:* `4`.
*Distractors:* `1` is the `tanh` answer, where `gamma = 1`; `0.25` is `gamma` itself
rather than `1/gamma`; `0` would mean never, which is false.

## Practice seed

**Stem.** A thirty-layer network has a per-layer Jacobian whose largest singular value is
`0.9`. By what factor does a gradient signal shrink across all thirty layers? Repeat for
`1.1`. Then name the mitigation each case motivates, without describing how it works.

**Hint.** The bound in the proof is `eta^(t-k)`. You need one power, twice.

**Solution.** `0.9^30 = 0.0424`, a shrink of about 24 times. `1.1^30 = 17.45`, a growth
of about 17 times. Vanishing motivates residual connections and gated cells; exploding
motivates gradient clipping. Both belong to M06 and to the architectures courses.

**`.p-check`.** The two answers must be reciprocal-ish in character but not in value:
`0.9` and `1.1` are not reciprocals, so `0.0424 x 17.45` is `0.74` and not `1`. If you
got exactly `1` you used `1/0.9` instead of `1.1`.

## Code and dataset

`../code/m05_08_reverse_vs_forward.py`. No csv: the object is a chain of maps, built
explicitly so the reader can change the depth and the spectral radius.

Verified output to quote: on `R^60 -> R` with twelve layers the two modes agree to
`2.776e-16`; reverse mode takes `0.106 ms` and forward mode `3.408 ms`, **a measured
ratio of 32x against a bound that predicts about `n = 60`**. Say why the measurement is
below the bound rather than hiding it: numpy's forward-mode sweeps share the same matrix
multiplies at the library level, so the constant differs between the two modes. The decay
table gives `0.9^30 = 0.04239` and `1.1^30 = 17.45`, and the measured Jacobian-product
run gives arrival norms of `0.01454`, `0.06314` and `2.43` at radii `0.90`, `1.00` and
`1.10`, which is the necessary-not-sufficient point made numerical.

## Sources

- Baydin, Pearlmutter, Radul and Siskind, "Automatic Differentiation in Machine Learning:
  a Survey", *JMLR* 18(153), 2018. Section 2 for AD being neither symbolic nor numerical
  differentiation and for "expression swell"; section 3 for the `n c ops(f)` against
  `m c ops(f)` bound with `c < 6` and typically `[2, 3]`, and for reverse mode needing
  only one application when the output is scalar. `https://arxiv.org/abs/1502.05767`
- Pascanu, Mikolov and Bengio, "On the difficulty of training Recurrent Neural Networks",
  arXiv:1211.5063, section 2.1, for the sufficient condition `lambda_1 < 1/gamma`, for the
  necessary condition for exploding, and for `gamma = 1` for `tanh` and `gamma = 1/4` for
  the sigmoid. `https://ar5iv.labs.arxiv.org/html/1211.5063`
- Goodfellow, Bengio and Courville, *Deep Learning*, section 6.5.9, for `O(#edges)`, for
  forward mode being preferable when outputs outnumber inputs, and for the `ABCD`
  matrix-ordering analogy. `https://www.deeplearningbook.org/contents/mlp.html`
