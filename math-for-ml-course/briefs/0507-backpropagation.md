# 0507 - Backpropagation is the chain rule run right to left on a computation graph

> **PLACEHOLDER NUMBER.** Real number assigned by the scaffold (#41). Report label C07.

| | |
|---|---|
| Module | M05 Calculus |
| Rung | working (`pill med`) |
| Label | `core` |
| Prerequisites | 0502, 0504, 0506. |
| Enables | 0508, and every training loop in the hub |

## The single tight idea

Draw the computation as a graph and the gradient is one sweep backwards, multiplying
local derivatives and accumulating.

## Beats, in order

1. **What backpropagation is not, first,** because the misconception is universal and
   correcting it afterwards never lands. It is not the learning algorithm: it computes
   the gradient and something else, usually stochastic gradient descent, does the
   learning. And it is not specific to neural networks: it differentiates any function
   expressible as a graph of differentiable operations. Quote Goodfellow 6.5 directly.
2. **The computation graph.** Nodes are variables, edges are operations. Draw the graph
   of a two-input, two-hidden-unit, one-output network.
3. **Forward pass, with a real number on every node.**
4. **Each edge carries one local derivative.** Label them all.
5. **Backward pass.** Start at `dL/dL = 1`, walk backwards, multiply and accumulate.
   Show every number.
6. **Why the order matters.** Computing a shared subexpression once per path wastes work,
   and for a graph with branching the waste compounds. Reverse order visits each local
   derivative once.
7. **The quantitative beat, which r1 5.3 makes mandatory.** Operation count against
   depth, naive re-evaluation against reverse accumulation.
8. **Gradient checking, as the closing practice.** Compare an analytic partial against a
   central difference, and point back to 0501's V-curve for why `h = 1e-6` and not `1e-12`.

## Named result and its stated proof

Backpropagation is an algorithm, not a theorem, so what this page owes is a **correctness
proposition** and a **cost proposition**, both proved.

**Proposition 1 (correctness).** Let a computation graph be a finite directed acyclic
graph whose nodes `u_1, ..., u_N` are ordered so that every edge goes from a lower index
to a higher one, with `u_N = L` the scalar output. Define adjoints by `abar_N = 1` and,
for `i < N`,

  `abar_i = sum over j in children(i) of  abar_j * (d u_j / d u_i)`,

where each local partial is evaluated at the forward values. Then `abar_i = dL / du_i`
for every `i`.

> *Proof, by reverse induction on `i`.*
> **Base.** `i = N`: `dL/du_N = dL/dL = 1 = abar_N`.
> **Step.** Suppose the claim holds for every index above `i`. Every path from `u_i` to
> `L` leaves `u_i` through exactly one child, so the total derivative of `L` with respect
> to `u_i` decomposes over the children. The multivariate chain rule (0506, Theorem 1)
> applied to `L` as a function of the children of `u_i`, each of which is a function of
> `u_i`, gives
>
>   `dL/du_i = sum over j in children(i) of (dL/du_j)(d u_j / d u_i)`.
>
> Every child `j` has index above `i` by the topological order, so the inductive
> hypothesis lets us replace `dL/du_j` with `abar_j`. The right-hand side is then exactly
> the defining sum for `abar_i`. **QED**
>
> Two things the proof makes visible and prose does not. The topological order is what
> the induction runs on, which is why the graph must be acyclic. And each local partial
> `d u_j / d u_i` is used exactly once, which is Proposition 2.

**Proposition 2 (cost).** If the forward graph has a single scalar output and each local
partial can be computed in constant time, the backward pass costs `O(#edges)`, the same
order as the forward pass.

> *Proof.* The recursion visits each node once and, at node `i`, does one multiplication
> and one addition per outgoing edge. Summing over nodes counts every edge exactly once,
> so the total is `O(#edges)` multiplications and additions plus `O(#nodes)` overhead,
> and `#nodes <= #edges + 1` in a connected graph. The forward pass also touches each edge
> once. **QED**
>
> This is why the gradient of a loss over a hundred billion parameters costs about what
> evaluating the loss costs, and it is the single most consequential fact in the module.
> Goodfellow states the same `O(#edges)` result in 6.5.9.

## Figures

1. **Orientation, `flowchart LR`.** "The vector chain rule (0506)" into "THIS PAGE:
   running it on a graph" into "training any network" and "what it costs (0508)".
2. **`flowchart LR`.** The graph of the worked 2-2-1 network, every node labelled with
   its forward value. *Kills:* "the graph is a metaphor". It is the data structure.
3. **`flowchart RL`.** The same graph backwards, every edge labelled with its local
   derivative and every node with its accumulated adjoint. Same shape, different numbers.
   *Kills:* backpropagation as magic.
4. **`sequenceDiagram`.** Forward phase then backward phase, with a note over the boundary
   listing what had to be stored. *Kills:* "the backward pass is free", and sets up 0508.
5. **`svg.chart`, quantitative, log axis. Not optional:** operation count against chain
   length for naive re-evaluation of shared subexpressions and for reverse accumulation.
   Linear against exponential. This is the page's `svg.chart` and without it the page is
   all Mermaid, which r1 5.3 forbids.

## Worked example, in eight parts

1. **Setting.** A two-input, two-hidden-unit ReLU network with one output, small enough
   to do entirely by hand and large enough to contain everything.
2. **Symbolic.** `.math` for the forward equations and for `L = 0.5 (yhat - y)^2`, with a
   `.gloss` naming every symbol.
3. **Picture.** Figure 2, before a single derivative appears.
4. **`ol.worked`.** Setup `x = [1, 2]`, `W1 = [[0.5, -0.5], [1.0, 0.5]]`, `b1 = [0, 0]`,
   ReLU, `w2 = [1.0, -2.0]`, `b2 = 0.5`, target `y = 1`.
   Forward: `z1 = [-0.5, 2.0]`, `h = [0, 2]`, `yhat = -3.5`, `L = 10.125`.
   Backward, seven steps: `dL/dyhat = -4.5`; `dL/dw2 = [0, -9]`; `dL/db2 = -4.5`;
   `dL/dh = [-4.5, 9]`; `dL/dz1 = [0, 9]`; `dL/dW1 = [[0, 0], [9, 18]]`; `dL/db1 = [0, 9]`.
5. **`.keynum`** on nothing: every number is derived on the page and every one is a small
   whole number, so a reader can redo the pass on paper.
6. **Sanity check.** The prediction is `-3.5` against a target of `1`, so the model is
   badly wrong and `dL/dyhat` must be large and negative. It is `-4.5`. And `dL/dW1`'s
   first row is all zeros, which is not a bug: `z1[0] = -0.5` so ReLU output zero, its
   local derivative is zero, and that zero blocks the gradient to both weights feeding
   the first hidden unit. **This is the dead-ReLU phenomenon, visible rather than described.**
7. **What changes if** `W1[0][0]` is raised from `0.5` to `1.0`? Then `z1[0] = 0`, the
   unit sits exactly on the kink, and the framework returns one of the one-sided
   derivatives from 0503. Raise it further and the whole first row of `dL/dW1` becomes
   non-zero and the unit starts learning again.
8. **In words.** A hidden unit that is off contributes nothing to the output and receives
   nothing from the gradient. Backpropagation routes the signal only along paths that
   were actually used.

## Quiz seeds

**Q1, misconception.** Backpropagation computes what, exactly?
*Answer:* the gradient. Something else, such as stochastic gradient descent, does the
learning with it.
*Distractors:* "it trains the network" is the misconception the page opens with; "it
updates the weights" is the optimiser's job; "it only works on neural networks" is false
and is the second misconception in the same sentence of the source.

**Q2, misconception.** In the worked network, `dL/dW1` has a first row of zeros. Why?
*Answer:* the first hidden pre-activation was `-0.5`, so ReLU output zero, its local
derivative is zero, and that blocks the gradient to every weight feeding that unit.
*Distractors:* "the weights were initialised to zero" is false, they were `0.5` and
`-0.5`; "the input was zero" is false, it was `[1, 2]`; "a rounding error" is not an
explanation and the finite-difference check returns exactly zero.

## Practice seed

**Stem.** For the network above, run the forward pass, then the backward pass, then check
`dL/dW1[0][0]` against a central difference at `h = 1e-5`.

**Hint.** Do the backward pass strictly in reverse order and write down the adjoint at
every node before moving on. If you jump ahead you will multiply by a derivative you have
not computed yet.

**Solution.** Forward `z1 = [-0.5, 2.0]`, `h = [0, 2]`, `yhat = -3.5`, `L = 10.125`.
Backward as listed in the worked example. The central-difference check on `W1[0][0]`
returns exactly `0.0000000000`, matching the analytic `0`.

**`.p-check`.** `L = 0.5(yhat - y)^2` with `yhat = -3.5` and `y = 1` must be
`0.5 x 20.25 = 10.125`. If the forward loss is not that, stop before differentiating.

## Code and dataset

`../code/m05_07_backprop.py` against `../datasets/m05-housing.csv`. It scales the hand
example up to a 4-32-1 network and gradient-checks **every** parameter, not one, then
measures what the backward pass costs against the forward pass.

Verified output to quote: 193 parameters, all of them checked; worst relative error
`1.582e-06` (in `W1`), best `6.658e-10`; the backward pass costs `1.58x` the forward pass;
and a full finite-difference gradient would need `386` forward passes, which measured
`0.71 s` against `0.00475 s` for one forward-and-backward pair.

## Sources

- Goodfellow, Bengio and Courville, *Deep Learning*, section 6.5, for what
  backpropagation is and is not, 6.5.1 for the computation graph, 6.5.2 for the chain
  rule in Jacobian-gradient form, 6.5.3 for repeated subexpressions being exponentially
  wasteful, and 6.5.9 for the `O(#edges)` guarantee.
  `https://www.deeplearningbook.org/contents/mlp.html`
- Deisenroth, Faisal and Ong, *Mathematics for Machine Learning*, section 5.6, for the
  layered form of the chain rule and for the attribution "(Kelley, 1960; Bryson, 1961;
  Dreyfus, 1962; Rumelhart et al., 1986)", which the page should use rather than dating
  backpropagation to 1986. `https://mml-book.github.io/book/mml-book.pdf`
- Rumelhart, Hinton and Williams, "Learning representations by back-propagating errors",
  *Nature* 323:533-536, 1986, DOI `10.1038/323533a0`, cited for the popularisation only.
  **The full text is behind authentication; the bibliographic record was confirmed
  through Crossref and the paper itself was not read.** Do not attribute a claim to it.
