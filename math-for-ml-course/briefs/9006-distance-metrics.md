# 9006 - Distance and similarity metrics, and the metric axioms

**Module** M10 - lesson 06  **Rung** working  **Class** core

## The single tight idea

"Similar" is not a fact about two vectors, it is a choice of function, and the three standard
choices disagree with each other on real data.

## Prerequisites

M03 for norms and the unit ball of each, and for the dot product, the angle and cosine similarity
as geometry. **M03 owns the norm axioms** (a property of one vector); **this page owns the metric
axioms** (a property of two points), which is an amendment to the spec's edge 5 that M03's brief
and this one agree on. M04 for eigenvalues and the eigendecomposition of a symmetric matrix. M08
for the covariance matrix and the multivariate Gaussian. 9003 for the four ways KL fails to be a
distance, which this page's table finally files.

## Beats, in order

1. **One-minute version.** Euclidean answers "how far apart", cosine answers "same direction",
   Mahalanobis answers "how far in units of the data's own spread". Scale decides between the first
   two; correlation decides whether you need the third.
2. **Orientation figure.** M03's norms and angles into "this page: which one, and when each lies"
   into 9007 (cosine in an embedding space), 9008 (kernels) and 9009 (what high dimension does to
   all three).
3. **The metric axioms**, which is what this page owns. A metric needs `d(x,y) = 0` if and only if
   `x = y`, symmetry, and the triangle inequality. Then immediately the table: Euclidean is a
   metric, standardised Euclidean is a metric, Mahalanobis is a metric, **cosine distance `1 - cos`
   is not**, and **KL is not** in three separate ways. This is the page that files 9003's four
   failures under a heading.
4. **Euclidean, and the units problem**, worked with real numbers below. One feature on a larger
   scale owns the distance. Standardisation is the answer and M02 owns the z-score.
5. **Cosine, and what dropping the magnitude buys and costs.** The exact relation
   `|x_hat - y_hat|^2 = 2(1 - cos theta)` for length-one vectors, so **after normalisation cosine
   and Euclidean give the same ranking**, which is why vector databases normalise on ingest. Page
   9007 develops the rest.
6. **Mahalanobis, built rather than quoted.** `D^2 = (x - mu)' Sigma^-1 (x - mu)`, PRML eq 2.44,
   which reduces to Euclidean when `Sigma = I`. Then the geometric reading: **it is Euclidean
   distance after each principal direction has been divided by its standard deviation.**
   **Named theorem, see proof.**
7. **Where it appears.** It is the exponent of the multivariate Gaussian, so a contour of constant
   density is a contour of constant Mahalanobis distance. Link back to M08.
8. **Trade-off, same section.** Mahalanobis needs `Sigma^-1`, which needs `n` comfortably larger
   than `d` and a well-conditioned covariance. In 768 dimensions with 500 samples the matrix is
   singular and the distance is undefined. Name shrinkage as the fix in one line, do not derive it,
   link to M04 on conditioning.

**Do not do here:** learned metrics, triplet loss, ANN index structures, the anisotropy material
(9007 owns it).

## The stated proofs (D4)

**Theorem (Mahalanobis is Euclidean after whitening).** Let `Sigma` be symmetric positive definite
with eigendecomposition `Sigma = sum_i lambda_i u_i u_i'`, the `u_i` orthonormal and every
`lambda_i > 0`. Define `y_i = u_i' (x - mu)`. Then
`(x - mu)' Sigma^-1 (x - mu) = sum_i y_i^2 / lambda_i`.

*Proof, in full.* The spectral theorem (M04 owns it; this page states it) gives the orthonormal
eigenbasis. Because the `u_i` are orthonormal, `Sigma^-1 = sum_i (1/lambda_i) u_i u_i'`: multiply
that candidate by `Sigma` and every cross term dies, since `u_i' u_j = 0` for `i != j`, leaving
`sum_i u_i u_i' = I`. Now substitute:

```
(x - mu)' Sigma^-1 (x - mu) = (x - mu)' [ sum_i (1/lambda_i) u_i u_i' ] (x - mu)
                            = sum_i (1/lambda_i) (x - mu)' u_i * u_i' (x - mu)
                            = sum_i (1/lambda_i) y_i^2
```

**The step that does the real work** is the middle line, where the scalar `u_i' (x - mu)` is pulled
out of the matrix product twice. After that, the expression is a plain sum of squares with each
term divided by a variance, which is what "Euclidean distance in units of the spread" means. The
requirement that every `lambda_i > 0` is where positive definiteness is doing its job: a zero
eigenvalue means a direction with no spread, `Sigma` is singular, and the distance is undefined.

**Theorem (cosine distance is not a metric).** `1 - cos(x, y)` violates the triangle inequality.

*Proof, by counterexample, and the page prints the one its own code found.* Take
`a = (1, 0)`, `b = (1, 1)`, `c = (0, 1)`. Then `cos(a,b) = cos(b,c) = 1/sqrt(2) = 0.7071` and
`cos(a,c) = 0`. So `d(a,b) + d(b,c) = 2(1 - 0.7071) = 0.5858` while `d(a,c) = 1`. The direct route
is longer than the detour, so the inequality fails. The code file finds the same failure on real
rows of `m10_signals.csv`: rows 9804, 7919 and 1604, where `d(a,b) + d(b,c) = 0.801875` against
`d(a,c) = 0.851715`, a slack of `-0.0498`.

**And the repair.** `sqrt(2 - 2cos)` **is** a metric. For unit vectors,
`|x_hat - y_hat|^2 = x.x - 2 x.y + y.y = 2 - 2cos`, so this quantity is literally the Euclidean
distance between the two normalised vectors, and Euclidean distance satisfies all three axioms.
**The step that does the real work** is recognising that the square root is not cosmetic: `1 - cos`
is the *square* of a distance, and squaring a metric generally destroys the triangle inequality.

## Planned figures

1. **Orientation, `flowchart LR`,** as beat 2.
2. **`svg.chart`, one scatter, three verdicts.** A query point and three candidates in 2-D, with a
   small table under it giving the rank each metric assigns. The ranks disagree.
3. **`svg.chart`, the Mahalanobis ellipse.** The real covariance of `tenure_months` and
   `monthly_spend` (correlation 0.8458), its 1-, 2- and 3-Mahalanobis contours, and two points at
   **identical** Euclidean distance from the centre, one along the ridge and one across it, with
   `D = 1.561` and `D = 5.403` printed on them.
4. **`flowchart LR`, the decision.** "Are the features on comparable scales?" then "Does magnitude
   carry meaning?" then "Are the features correlated?", ending at Euclidean, cosine, standardised
   Euclidean, Mahalanobis.
5. **`svg.chart`, the axiom table as a figure**, or a plain table if that reads better: four
   candidate functions against three axioms, with the failing cell marked in `alarm`.

## The worked example, with its numbers

Units, worked in eight parts. Derived.

Two columns: annual income in rupees and age in years. Customer A `(1,200,000, 30)`,
B `(1,200,050, 65)`, C `(1,900,000, 31)`.

1. `d(A,B) = sqrt(50^2 + 35^2) = sqrt(3725) = 61.0`.
2. `d(A,C) = sqrt(700000^2 + 1^2) = 700,000.0`.
3. B is nearer than C by four orders of magnitude. A `k`-NN model sees only income.
4. Standardise with column standard deviations of 400,000 rupees and 12 years.
   A becomes `(3.0, 2.5)`, B becomes `(3.000125, 5.4167)`, C becomes `(4.75, 2.5833)`.
5. `d(A,B) = 2.9167`.
6. `d(A,C) = sqrt(1.75^2 + 0.0833^2) = 1.7520`. **C is now nearer and the ranking has flipped.**
7. **Sanity check.** In standardised units no single-column gap should exceed a few, because a
   z-score of 5 is already extreme. A gap of 2.92 is large but plausible; a gap of 700,000 tells
   you immediately that you forgot to standardise.
8. **What changes if** the two columns had been income in rupees and income in lakhs? Then they are
   the same column twice and standardising makes them identical, so the distance doubles a single
   signal. Standardisation fixes *scale*; it does not fix *redundancy*, and that is what
   Mahalanobis is for.

Second part, Mahalanobis on the committed data (derived, from the code file): the covariance of the
three continuous columns has eigenvalues `[12.338, 21.991, 43699.414]`. Two synthetic points both
1.5 standard deviations out on two axes sit at **identical** Euclidean distance 313.645 from the
centre, and at Mahalanobis distance **1.561** along the correlation ridge against **5.403** across
it, a factor of 3.46.

## Quiz seeds

- **Q1.** Query `(1,1,0)`, documents `d1 = (10,10,0)` and `d2 = (1,1,1)`. Which document is nearer?
  **Answer: it depends on the metric, and the two standard ones disagree.** Distractors: `d1`;
  `d2`; they are equidistant.
- **Q2 (misconception).** Cosine distance, `1 - cos`, is not a metric. Which property does it fail?
  **Answer: the triangle inequality.** Distractors: symmetry; `d(x,x) = 0`; non-negativity. All
  three distractors are properties it *does* satisfy, which is what makes them good.

## Practice seed

**Stem.** Using the covariance eigenvalues above, take a point that lies purely along the largest
eigendirection at Euclidean distance 100 from the mean, and another purely along the smallest, also
at Euclidean distance 100. (a) Compute both Mahalanobis distances. (b) Say which point an outlier
detector built on Mahalanobis distance would flag, and which one a detector built on Euclidean
distance would flag. (c) Say which is right, and what "right" depends on.

**Hint.** Along a single eigendirection the theorem collapses to `D = |y| / sqrt(lambda)`.

**Solution.** (a) Largest eigenvalue 43699.414, so `sqrt(lambda) = 209.05` and `D = 100/209.05 =
0.478`. Smallest 12.338, so `sqrt(lambda) = 3.513` and `D = 100/3.513 = 28.47`. (b) Mahalanobis
flags the second, by a factor of sixty. Euclidean flags neither over the other; they are the same
distance. (c) Mahalanobis is right if you believe the training covariance describes normal
behaviour, because a point 28 standard deviations out along a narrow direction is far stranger than
one half a standard deviation out along a wide one. It is wrong if the covariance was estimated
from contaminated data, because then the outliers helped define what "normal spread" means.

**`.p-check`.** The two Mahalanobis answers must differ by exactly the ratio of the square roots of
the two eigenvalues, `sqrt(43699.414 / 12.338) = 59.5`. If your ratio is 3543 you divided by the
eigenvalues instead of their square roots.

## Code and dataset plan

`code/9006-distance-metrics.py` against `m10_signals.csv`. Computes all three distances for every
row and shows the top-100 lists overlap by only 30 of 100 between raw and Mahalanobis; **verifies
the whitening theorem to 5.2e-13 over 12,000 rows**; and **tests the three metric axioms on 20,000
random triples**, finding a real triangle-inequality violation for cosine distance and none for
Euclidean or `sqrt(2-2cos)`.

## Sources, primary only

- Bishop, *PRML* (2006) eq 2.44 and eq 2.50, for the definition and the eigen reading.
- Aggarwal, Hinneburg and Keim, ICDT 2001, section 1, for the `L_k` family. Used mainly on 9009.
- **Note for the writer.** Mahalanobis' own 1936 note in *PINSA* is a scan with no text layer at
  `insa.nic.in/writereaddata/UpLoadedFiles/PINSA/Vol02_1936_1_Art05.pdf`. Cite PRML for the
  definition and do not claim the original. Record it in `RESOURCES.md` under `## Gaps`.

## Primary source to go deeper

Bishop, *PRML*, section 2.3. The Mahalanobis distance and the Gaussian are one object there, which
is the right way to meet it.
