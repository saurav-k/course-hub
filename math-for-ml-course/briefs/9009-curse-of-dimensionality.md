# 9009 - The curse of dimensionality

**Module** M10 - lesson 09  **Rung** frontier  **Class** depth

## The single tight idea

In high dimensions all pairwise distances converge, so "nearest" stops meaning anything - and the
theorem that says so has a hypothesis that real data usually violates, which is why your vector
database works.

## Prerequisites

9006 (distances). 9007 (what an embedding space actually looks like). M03 for norms. **M08 owns
concentration and tail bounds**, and this page consumes them: every theorem quoted here is a tail
bound applied to a norm. This is the heaviest incoming edge in M10.

## Beats, in order

1. **One-minute version.** Volume moves to the surface. Points concentrate on a thin shell. Random
   directions become orthogonal. Relative contrast decays like `1/sqrt(d)`. And none of it stops
   embedding search from working, for two reasons this page names.
2. **Orientation figure.** 9006's three distance functions into "this page: what happens to all of
   them as `d` grows" into 9008 (which adds dimensions on purpose) and 9007 (which searches in
   forty-eight of them anyway).
3. **Three facts with three pictures, each derived rather than asserted.**
   - **Volume goes to the shell.** `vol((1-eps)A) = (1-eps)^d vol(A)` for any body, so the fraction
     outside the shrunken copy is `1 - (1-eps)^d`. **Named theorem, see proof.**
   - **Points concentrate on a thin annulus.** The Gaussian Annulus Theorem: for a `d`-dimensional
     spherical Gaussian with unit variance per coordinate, all but at most `3 e^{-c beta^2}` of the
     mass lies in `sqrt(d) - beta <= |x| <= sqrt(d) + beta`. Stated, not proved; boundary below.
   - **Random directions are almost orthogonal.** Blum, Hopcroft and Kannan Theorem 2.8: for `n`
     points from the unit ball, with probability `1 - O(1/n)` every pair has
     `|x_i . x_j| <= sqrt(6 ln n) / sqrt(d - 1)`.
4. **The consequence for nearest-neighbour search, stated as the theorem actually reads.** Aggarwal,
   Hinneburg and Keim Theorem 1, their restatement of Beyer et al.: **IF**
   `var(|X_d| / E|X_d|) -> 0` **THEN** `(Dmax - Dmin) / Dmin -> 0` in probability. The `if` is doing
   all the work and this page must print it.
5. **The norm result most treatments skip.** `Dmax - Dmin` grows like `d^{1/k - 1/2}` for the `L_k`
   norm, so it grows for `L1`, is constant for `L2`, and shrinks for `L3` and above. Relative
   contrast degrades like `1/sqrt(d)` for every norm, with a constant `sqrt(1/(2k+1))` that favours
   smaller `k`. The paper's own conclusion: `L1` is preferable in high dimensions, then `L2`, then
   `L3`. Counter-intuitive, in the title of the paper, and it changes a default in real code.
6. **The honest half, and it is why this page is `frontier`.** PRML section 1.4, in Bishop's own
   words: "real data will often be confined to a region of the space having lower effective
   dimensionality" and "real data will typically exhibit some smoothness properties". The
   hypothesis in beat 4 fails whenever the coordinates are strongly dependent, which for a trained
   embedding they always are. **The curse applies to the ambient dimension; real data lives on a
   much lower-dimensional surface inside it.** Measured on the committed data below.
7. **The other meaning of the phrase, disambiguated.** `llm-evolution-course` lesson 0018 uses
   "curse of dimensionality" in Bengio's 2003 sense: the number of possible `n`-grams grows
   exponentially so no corpus covers it. That is **statistical sparsity**, not **geometric
   concentration**. Both are correct and they are different claims with different fixes. Name both,
   link across, say which one this page is about. Nobody else in the hub will do this.
8. **Trade-off, same section.** The fix for the geometric curse is to reduce the dimension (M04's
   PCA and SVD). The fix for the statistical curse is to share parameters across similar inputs,
   which is what an embedding does.

**Do not do here:** ANN algorithms, HNSW, locality-sensitive hashing beyond one naming sentence.

## The stated proofs (D4)

**Theorem (volume concentrates near the surface).** For any measurable body `A` in `R^d` and any
`0 < eps < 1`, `vol((1 - eps)A) = (1 - eps)^d vol(A)`, so the share of `A`'s volume lying outside
the shrunken copy is `1 - (1 - eps)^d >= 1 - e^{-eps d}`.

*Proof, in full.* Partition `A` into infinitesimal cubes. Shrinking `A` by the factor `(1 - eps)`
shrinks each of a cube's `d` sides by that factor, so each cube's volume shrinks by `(1 - eps)^d`.
Volume is additive over the partition, so the whole body's volume shrinks by the same factor. The
share outside is therefore `1 - (1 - eps)^d`, and `1 - x <= e^{-x}` gives the bound.

**The step that does the real work** is "each of a cube's `d` sides", and it is worth pausing the
reader on it. Nothing here is about spheres, or about probability, or about data. It is about the
exponent `d` in a product of `d` side lengths, and that exponent is why the effect is violent
rather than gradual: at `eps = 0.01`, the outer one per cent of the radius holds 2.97 per cent of
the volume at `d = 3`, 63.40 per cent at `d = 100`, and 99.34 per cent at `d = 500`.

**Corollary (the intuition that has to go).** A `d`-dimensional ball is not "like a 3-D ball but
bigger". Almost all of it is skin.

**Theorem 2.9 (Gaussian Annulus), stated.** As in beat 3. **Honest boundary:** the proof needs a
tail inequality for sums of independent bounded-moment random variables, which is M08's material,
and Blum, Hopcroft and Kannan prove it in their appendix. This course states the result and gives
the one-line intuition instead: `E[|x|^2] = sum_i E[x_i^2] = d`, so the mean squared distance from
the centre is exactly `d` and the radius is `sqrt(d)`. What the theorem adds is that the *spread*
around that radius does not grow with `d`. The code file measures precisely that: the standard
deviation of `|x|` stays near 0.70 from `d = 10` to `d = 10,000` while the radius grows from 3.16
to 100.

**Theorem 1 (Beyer et al., as Aggarwal, Hinneburg and Keim restate it), stated with its hypothesis.**
**Honest boundary, and the page must say this plainly:** the 1999 original is a scan with no text
layer and I could not read it directly; this course quotes the restatement in Aggarwal, Hinneburg
and Keim, ICDT 2001, section 2, and attributes it that way. That is a second-hand citation and
labelling it is the point.

## Planned figures

1. **Orientation, `flowchart LR`,** as beat 2.
2. **`svg.chart`, volume in the shell.** `1 - (1-eps)^d` against `eps` for `d = 1, 2, 5, 20, 200`.
   PRML figure 1.22 redrawn from the formula, so it is derived rather than copied.
3. **`svg.chart`, the contrast collapse**, from this page's own simulation: relative contrast
   against `d` on a log-x axis with a `1/sqrt(d)` reference curve. Label it derived and print the code.
4. **`svg.chart`, near-orthogonality.** Mean `|cos|` between two random directions against `d`,
   measured, with `sqrt(2/(pi d))` overlaid, marking `d = 768` at 0.0290.
5. **`quadrantChart`, when the curse bites.** Axes "coordinates independent / strongly dependent"
   against "ambient dimension low / high". Points: tabular data at d=8; one-hot text features; a
   Gaussian cloud at d=1000; a trained embedding. Only one quadrant is dangerous. Keep every point
   label under 26 characters.

## The worked example, with its numbers

Two simulations the reader can run, then the counterweight. Eight parts, all derived, code shown.

1. 1,000 uniform points in the unit cube, query at the centre. At `d = 2`: `Dmin = 0.017`,
   `Dmax = 0.692`, contrast **40.42**.
2. At `d = 10`: `Dmin = 0.432`, `Dmax = 1.263`, contrast **1.9229**.
3. At `d = 100`: `Dmin = 2.474`, `Dmax = 3.299`, contrast **0.3336**.
4. At `d = 1000`: `Dmin = 8.708`, `Dmax = 9.597`, contrast **0.1021**. The farthest of a thousand
   points is ten per cent farther away than the nearest.
5. **Sanity check on the rate.** Multiply each contrast by `sqrt(d)`: 57.2, 11.4, 6.08, 3.85, 3.56,
   3.34, 3.41, 3.03, 3.23 for `d = 2` to `1000`. From `d = 50` upward the product sits near 3.0 to
   3.6 and stops trending, while the contrast itself has fallen by a factor of five. That is the
   `1/sqrt(d)` decay, measured rather than quoted. Below `d = 25` the product is still falling
   fast, so the asymptotic rate is not yet in force and the page should say so.
6. Second simulation, mean `|cos theta|` between two random Gaussian directions: 0.5059 at `d = 3`,
   0.0820 at `d = 100`, 0.0290 at `d = 768`, 0.0124 at `d = 4096`, against `sqrt(2/(pi d))` of
   0.4607, 0.0798, 0.0288 and 0.0125. Within 3 per cent by `d = 100`.
7. **The counterweight, and this is what stops the page being alarmist.** Run the same contrast
   measurement on `m10_embeddings.csv`, which is 48-dimensional: contrast **1.9656**, against
   **0.8229** for uniform points at the same `d = 48`. Nearest-neighbour agrees with the topic
   label on **100 per cent** of 300 queries. Same dimension, opposite outcome.
8. **What changes, and be precise about why.** The scaled-norm variance on the embeddings is 0.0084
   against 0.0045 for uniform points at `d = 48` - only about twice, so that statistic alone is
   suggestive rather than decisive. The decisive number is the spectrum: **five directions of
   forty-eight carry 67.10 per cent of the variance**, because the data was built from six latent
   topics and centring removes one degree of freedom. The effective dimension the geometry sees is
   five, not forty-eight, and that is the whole escape.

## Quiz seeds

- **Q1 (misconception, M5).** Which condition must hold for the "all distances converge" theorem to
  apply? **Answer: the variance of the norm divided by its expectation must tend to zero.**
  Distractors: the dimension must exceed 20; the data must be uniformly distributed; the metric
  must be Euclidean. All three are things people believe and none is the hypothesis.
- **Q2 (misconception, M6).** In high dimensions, which `L_k` norm keeps the most contrast?
  **Answer: `L1`, the Manhattan norm.** Distractors: `L2`, because it is the natural one; `L_inf`,
  because it ignores the small coordinates; they are all equally bad.

## Practice seed

**Stem.** (a) Using `1 - (1 - eps)^d`, compute the share of a ball's volume in the outer 1 per cent
of its radius for `d = 3`, `d = 100` and `d = 500`. (b) A team stores 768-dimensional sentence
embeddings and finds brute-force nearest-neighbour search still returns useful results. Reconcile
that with (a), naming the specific assumption that fails.

**Hint.** For (b), re-read the hypothesis of the theorem in beat 4 before you reach for an
explanation about `d` being not large enough.

**Solution.** (a) `1 - 0.99^3 = 1 - 0.970299 = 2.97` per cent; `1 - 0.99^100 = 1 - 0.366032 = 63.40`
per cent; `1 - 0.99^500 = 1 - 0.006570 = 99.34` per cent. (b) The volume result describes the
*ambient* space, and the convergence theorem needs `var(|X| / E|X|) -> 0`, which needs the
coordinates to be close to independent. A trained embedding's 768 coordinates are strongly
dependent, so the points sit near a much lower-dimensional surface and the variance does not vanish.
PRML section 1.4 names both escapes: lower effective dimensionality, and local smoothness.

**Marking note for the writer to put in the feedback:** an answer of "because 768 is not big enough"
is wrong and the `.q-fb` must say so. The threshold is not a dimension count.

**`.p-check`.** All three answers in (a) must be between 0 and 100 per cent and must increase with
`d`. If your `d = 500` figure came out smaller than your `d = 100` figure you raised `0.01` to the
power `d` instead of `0.99`.

## Code and dataset plan

`code/9009-curse-of-dimensionality.py` against `m10_embeddings.csv` plus generated points. Evaluates
the shell fraction; measures contrast against `d` and checks the `1/sqrt(d)` rate; measures mean
`|cos|` against the closed form; **measures the Gaussian Annulus Theorem directly**, reporting that
the standard deviation of `|x|` stays near 0.70 from `d = 10` to `d = 10,000`; and **measures the
hypothesis of Theorem 1** on uniform points and on the real embeddings, with the spectrum that
explains the difference.

## Sources, primary only

- Blum, Hopcroft and Kannan, *Foundations of Data Science*, chapter 2, sections 2.3 and 2.4,
  Theorems 2.7, 2.8 and 2.9. https://www.cs.cornell.edu/jeh/book.pdf
- Bishop, *PRML* (2006) section 1.4, eq 1.76, and the two escape clauses.
- Aggarwal, Hinneburg and Keim, *On the Surprising Behavior of Distance Metrics in High Dimensional
  Space*, ICDT 2001, section 2, Theorem 1 and Theorems 2-3. https://bib.dbvis.de/uploadedFiles/155.pdf
- Cross-link, one way and no edit: `../../llm-evolution-course/lessons/0018-meaning-as-a-direction-in-space.html`
  for the statistical sense of the phrase.

## Primary source to go deeper

Blum, Hopcroft and Kannan, chapter 2. Thirty pages, it proves everything this page states, and it
is free.
