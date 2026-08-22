# M05 Calculus briefs

Twelve briefs, one per planned page, written from `mlm-calculus-r5`'s scout report
and reconciled against `mlm-audit-r1`'s architecture.

## Numbers, from the definitive block table

The block table on issue #42 is the single source of truth. **M05's block is `0080-0099`,
twenty slots**, and these twelve pages take `0080` to `0091`. Eight slots of headroom
remain, which is what the sparse scheme is for.

**A warning for the next crew that reads that comment.** Its prose says "module N starts
at `N x 20`", and that sentence does not match its own table: the table gives M01
`0001-0019`, which would be `N x 20 = 20` under the prose. The blocks are twenty wide
counting from zero, so module N starts at `(N - 1) x 20`, and M01 begins at `0001` only
because `0000` is lesson zero. **Read the table rows, not the sentence.** These briefs were
renamed twice before that was spotted, first to `0041-0052` from a roadmap count and then
to `0100-0111` from the sentence, which is M06's block.

**M05 writes twelve pages where the roadmap planned eleven**, which the block absorbs
without touching M06. The reasons are in the roadmap commit: the rules of differentiation
fold into the chain-rule page, and two pages the roadmap missed are added.

| Number | Report label | Page |
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

`C11` in the report is deliberately absent. It was a loss-surface page and it is
withdrawn to `mlm-optim-r6` L09, which declares the same beats from the same source.
Its one unclaimed asset, filter normalisation, is beat 8 of brief 0088.

## Module boundaries, from `mlm-audit-r1` section 4.4

- Owns the derivative, the chain rule, and backpropagation as the chain rule (edge 11).
  M10 owns the softmax gradient. 0081 stops at the binary logit.
- Owns the gradient and its picture (edge 12). M06 owns everything that descends along it.
- Owns Taylor (edge 13). M06 owns "gradient descent is the first-order model".
- Owns integrals (edge 14). **M07 depends on 0090**: a density integrating to one is an integral.
- Does not own the normal equations (edge 31). M03 derives them by projection.
  0091 reaches the same answer by calculus and says so explicitly.
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

---

# M10 Information, similarity, and dimension briefs

One brief per planned page, per issue #42. Briefs are markdown and live here rather than as stub
pages, because `validate_site.py` requires every `lessons/*.html` to be a registered card and to
appear in `outline.js`, and `widgets.md` requires a planned page to be plain text in a `.roadmap`
and never a link. Together those mean a planned page can have **no file at all**. The deploy
excludes `*.md` and the validator ignores it, and **no page ever links a brief**.

## The numbers

M10's block is **0180 to 0199**, read off the block **table** on issue #42. The prose above that
table says "module N starts at `N x 20`" and that phrase is one module out: the table's own first
row gives M01 the block `0001-0019`, so a module occupies `(N-1) x 20 + 1` upward and M11, not M10,
is the one that starts at 0200. **The rows are the authority.** This module briefly used 0105-0115
and then 0200-0210 before that was settled; both are gone.

Eleven of the twenty slots are used, 0180 to 0190, leaving nine spare. That headroom also settles a
question this module had raised: the course map's roadmap lists M10 as ten pages because it merged
"Information gain" and "Perplexity" onto one line, while issue #53, the spec for this module's
scope, lists them as two of eleven lessons. They are two ideas with two theorems, two worked
examples and two datasets' worth of results, so this module ships eleven, inside its own block,
costing no other crew a number.

| Real | Slug | Class |
|---|---|---|
| 0180 | entropy | core |
| 0181 | cross-entropy | core |
| 0182 | kl-divergence | core |
| 0183 | mutual-information | core |
| 0184 | softmax-log-sum-exp | core |
| 0185 | distance-metrics | core |
| 0186 | cosine-similarity | depth |
| 0187 | kernels | depth |
| 0188 | curse-of-dimensionality | depth |
| 0189 | information-gain | depth |
| 0190 | perplexity | core |

Teaching order is file order, and file order is a topological order of the prerequisite graph:
0180 -> 0181 -> 0182 -> 0183 -> 0189, with 0184 needing 0181, 0190 needing 0180 and 0181, and the
geometry arc 0185 -> 0186 -> 0187 -> 0188 needing only 0185 from inside this module. No page needs
a page that comes after it.

## What every M10 page owes

The house contract in `references/page-contracts.md`, plus this course's delta: an orientation
figure that is this page's slice of the prerequisite graph; at least one hand-authored `svg.chart`;
every symbol named in words; one worked example in eight parts with a sanity check and a
"what changes if" line; **a stated proof for every named theorem (D4)**; a runnable NumPy/Pandas
program against a committed dataset; two quizzes of which at least one tests a misconception; and
at least one practice problem with a hint, a hidden solution and a `.p-check` line.

## `statistical-foundations-ml-course` is frozen

Per captain update 3. This module creates, modifies, renames and deletes **nothing** under that
folder. One-way links out to its pages are allowed and one is planned, from 0183 to its
`lessons/0007-leading-indicators-and-correlation.html`, because that page teaches correlation as a
diagnostic and 0183 is where the reader learns what correlation cannot see. No reverse link, because
that would edit a frozen file.
