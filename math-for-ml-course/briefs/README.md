# M05 Calculus briefs

Twelve briefs, one per planned page, written from `mlm-calculus-r5`'s scout report
and reconciled against `mlm-audit-r1`'s architecture.

## Numbers, claimed

The scaffold merged (#55) and left the roadmap as unnumbered titles, so under #42 a brief
claims its number by existing. Counting the roadmap in `../index.html`: lesson zero is
`0000`, M01 takes `0001`-`0009`, M02 `0010`-`0017`, M03 `0018`-`0030`, M04 `0031`-`0040`.
**M05 therefore begins at `0041`, and these twelve pages take `0041` to `0052`.**

**M05 takes twelve numbers, not the eleven the roadmap planned, so M06 begins at `0053`.**
That is a cross-module fact and it is stated here rather than left to be discovered.

| Number | Report label | Page |
|---|---|---|
| 0041 | C01 | A derivative is the exchange rate between a small input change and a small output change |
| 0042 | C02 | The chain rule is the only differentiation rule that matters at scale |
| 0043 | C03 | Where the derivative does not exist, and why machine learning ships anyway |
| 0044 | C04 | Partial derivatives put every dial on its own axis, and the gradient collects them |
| 0045 | C05 | The gradient points uphill, and it is steepest only in the Euclidean sense |
| 0046 | C06 | The Jacobian is the chain rule when both ends are vectors |
| 0047 | C07 | Backpropagation is the chain rule run right to left on a computation graph |
| 0048 | C08 | A long chain of Jacobians: what backprop costs, and how the signal decays |
| 0049 | C09 | Curvature is the second derivative, and the Hessian holds it for every direction at once |
| 0050 | C10 | Taylor expansion: every loss is a quadratic if you stand close enough |
| 0051 | C12 | Integrals in machine learning: the area you report is a number you actually compute |
| 0052 | C13 | Six matrix-calculus identities, and the layout convention that breaks them |

`C11` in the report is deliberately absent. It was a loss-surface page and it is
withdrawn to `mlm-optim-r6` L09, which declares the same beats from the same source.
Its one unclaimed asset, filter normalisation, is beat 8 of brief 0049.

## Module boundaries, from `mlm-audit-r1` section 4.4

- Owns the derivative, the chain rule, and backpropagation as the chain rule (edge 11).
  M10 owns the softmax gradient. 0042 stops at the binary logit.
- Owns the gradient and its picture (edge 12). M06 owns everything that descends along it.
- Owns Taylor (edge 13). M06 owns "gradient descent is the first-order model".
- Owns integrals (edge 14). **M07 depends on 0051**: a density integrating to one is an integral.
- Does not own the normal equations (edge 31). M03 derives them by projection.
  0052 reaches the same answer by calculus and says so explicitly.
- **Amendment on edge 8, proposed in the scout report section 12.2:** this module owns the
  second-derivative test, because M05 precedes M06 and M06's saddle page consumes it.
  M06 owns the consequences.

## Every brief owes, per #42 and #48

Single idea, prerequisites, beats, **a stated proof for every named theorem (D4)**,
figures by widget kind with an orientation figure and at least one `svg.chart`,
a worked example in the eight parts of r1 5.4, two quiz seeds of which one tests a
misconception, one practice seed with hint and `.p-check`, the code and dataset plan,
primary sources, and the `core` or `depth` label.

## Code and datasets

Committed and verified. Three generators plus three datasets in `../datasets/`,
twelve programs in `../code/`. Every number quoted in these briefs is that program's
actual output, reproducible from the committed seed.
