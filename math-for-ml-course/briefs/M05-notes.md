# M05 Calculus - module notes

Provenance for the twelve calculus briefs. `README.md` in this folder is the course-wide
contract and it wins wherever this file appears to disagree.

## Numbers

M05's block is `0080-0099`, read from the table in `README.md`. These twelve pages take
`0080` to `0091`, leaving eight slots of headroom.

Two earlier revisions of these briefs claimed the wrong block: first `0041-0052`, counted
off the roadmap before any table existed, and then `0100-0111`, taken from the
"module N starts at N x 20" mnemonic, which is M06's block. `README.md` now warns everyone
off that mnemonic; this note records that M05 was one of the crews it caught.

## The map from the scout report

The `mlm-calculus-r5` scout report labels its pages C01 to C13.

| Page | Report label | Title |
|---|---|---|
| 0080 | C01 | A derivative is the exchange rate between a small input change and a small output change |
| 0081 | C02 | The chain rule is the only differentiation rule that matters at scale |
| 0082 | C03 | Where the derivative does not exist, and why machine learning ships anyway |
| 0083 | C04 | Partial derivatives put every dial on its own axis, and the gradient collects them |
| 0084 | C05 | The gradient points uphill, and it is steepest only in the Euclidean sense |
| 0085 | C06 | The Jacobian is the chain rule when both ends are vectors |
| 0086 | C07 | Backpropagation is the chain rule run right to left on a computation graph |
| 0087 | C08 | A long chain of Jacobians: what backprop costs, and how the signal decays |
| 0088 | C09 | Curvature is the second derivative, and the Hessian holds it for every direction at once |
| 0089 | C10 | Taylor expansion: every loss is a quadratic if you stand close enough |
| 0090 | C12 | Integrals in machine learning: the area you report is a number you actually compute |
| 0091 | C13 | Six matrix-calculus identities, and the layout convention that breaks them |

`C11` is deliberately absent. It was a loss-surface page and it is **withdrawn to M06**,
whose saddle-points lesson declares the same three beats from the same primary source.
Its one unclaimed asset, filter normalisation and why an unnormalised loss-surface picture
is not evidence, is beat 8 of brief `0088`.

## Twelve pages where the roadmap planned eleven

The roadmap listed "Rules of differentiation" and "The chain rule" as separate pages. They
are one page here, `0081`, because the rules are fluency and the chain rule is the idea.
That frees a slot, and two pages the roadmap missed take it plus one more: `0082`, where
the derivative does not exist, and `0087`, what a long chain of Jacobians costs. Both carry
a misconception nothing else in the course corrects. The block's headroom absorbs the extra
page, so M06 is unaffected.

**The Jacobian also moves before backpropagation.** The roadmap had backpropagation at
position 6 and the Jacobian at 7, but backpropagation is a transposed-Jacobian product per
operation, so the old order asked the reader to use an object they met the following page.

## Boundaries this module holds

- Owns the derivative, the chain rule, and backpropagation as the chain rule. **M10 owns
  the softmax gradient**, so `0081` stops at the binary logit and cross-links.
- Owns the gradient and its picture. **M06 owns everything that descends along it.**
- Owns Taylor. M06 owns "gradient descent is the first-order model".
- **Owns integrals, and M07 depends on `0090`**: a density integrating to one is an integral.
- **Does not own the normal equations.** M03 derives them by projection, on purpose, so
  that module needs no calculus. `0091` reaches the same answer by calculus and says so.
- **Amendment, proposed rather than taken quietly.** The architecture gives
  "positive-definite Hessian implies a local minimum" to M06, but M05 precedes M06 and
  M06's saddle page opens by classifying critical points from eigenvalue signs. `0088`
  claims the **test**; M06 keeps the consequences and the prevalence argument.

## Datasets

M05 reuses `sensors.csv` for the regression pages and `sessions.csv` for the
mean-against-median page, and adds exactly one, `failures.csv`, for the two pages that need
a binary label with an informative score. `sessions.csv` has a boolean column, `returning`,
but fitting it by Newton's method reaches an area under the ROC curve of 0.507, so an ROC
lesson built on it would have no curve to integrate.
