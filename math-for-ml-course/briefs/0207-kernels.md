# 0207 - Kernels, and why a kernel matrix must be positive semi-definite

**Module** M10 - lesson 08  **Rung** frontier  **Class** depth

## The single tight idea

If an algorithm touches its inputs only through dot products you can swap in a different dot
product and get a non-linear method for free, without ever visiting the bigger space.

## Prerequisites

0205 (distances, and the RBF kernel is a function of one). M03 for the dot product. **M04 owns
positive semi-definiteness and the eigenvalue test**; this page uses it and does not re-derive it.
0208 is *not* a prerequisite, but the page should note it comes next and that adding dimensions on
purpose is about to look strange.

## Beats, in order

1. **One-minute version.** `k(x, x') = phi(x) . phi(x')`. You never compute `phi`. The condition on
   `k` is that its Gram matrix is positive semi-definite. The feature space can be
   infinite-dimensional at finite cost.
2. **Orientation figure.** M03's dot product into "this page: a dot product in a space you do not
   visit" into the SVM, kernel PCA and Gaussian processes, with M04's positive semi-definiteness on
   a dotted edge.
3. **Mental model before any formula.** Two rings that no line separates in 2-D, lifted by one
   extra coordinate, separated by a plane, and the plane's shadow back in 2-D is a circle. Draw it
   before the algebra.
4. **Mechanism, checked by hand.** `k(x,z) = (x.z + 1)^2` on two-dimensional inputs equals
   `phi(x) . phi(z)` with `phi(x) = (1, sqrt2 x1, sqrt2 x2, x1^2, sqrt2 x1 x2, x2^2)`. Both routes
   worked with numbers, below. This one small check is the whole idea.
5. **The trick, stated as the condition it is.** PRML chapter 6: if an algorithm is written so that
   the input enters only through scalar products, you can replace that scalar product with any
   kernel. Say which algorithms qualify and which do not.
6. **Which functions are legal.** Mercer's condition, and what it becomes on a finite sample:
   **the Gram matrix `K_ij = k(x_i, x_j)` is positive semi-definite.** That is M04's eigenvalue
   test applied to a matrix of similarities. Key callout, because the reader will not see it coming.
   **Named theorem, see proof.**
7. **The catalogue, three entries with what each assumes.** Linear `x.x'`. Polynomial
   `(x.x' + 1)^d`, Cortes and Vapnik eq 37. RBF `exp(-gamma |x - x'|^2)`, whose feature space is
   infinite-dimensional and whose ancestor is the potential function `exp(-|u - v|)` of Aizerman,
   Braverman and Rozonoer 1964 (Cortes and Vapnik eq 36). Note that the RBF is a function of
   `|x - x'|`, so **it is 0205's Euclidean distance wearing a different hat** and everything 0208
   is about to say applies to it.
8. **Trade-off, in the same section.** The Gram matrix is `n` by `n`. At a million training points
   that is `10^12` entries. Kernel methods trade a dimension problem for a sample-size problem,
   which is the honest reason deep networks displaced them and the reason random-feature
   approximations exist.

**Do not do here:** the SVM dual and its optimisation (M06 owns constrained optimisation; state the
decision function, do not derive the quadratic program), Gaussian processes, random features beyond
one naming sentence.

## The stated proof (D4)

**Theorem.** If `k(x, z) = phi(x) . phi(z)` for some feature map `phi`, then for any finite set of
points `x_1, ..., x_n` the Gram matrix `K` with `K_ij = k(x_i, x_j)` is symmetric and positive
semi-definite.

*Proof, in full.* Symmetry is immediate, because the dot product is symmetric:
`K_ij = phi(x_i) . phi(x_j) = phi(x_j) . phi(x_i) = K_ji`. For positive semi-definiteness, take any
real vector `c` and compute the quadratic form:

```
c' K c = sum_i sum_j c_i c_j  phi(x_i) . phi(x_j)
       = ( sum_i c_i phi(x_i) ) . ( sum_j c_j phi(x_j) )
       = | sum_i c_i phi(x_i) |^2
       >= 0
```

**The step that does the real work** is the second line, where bilinearity lets the two sums move
inside the dot product. Once they are inside, the expression is a vector dotted with itself, and a
squared length cannot be negative. There is nothing else in the proof, which is why the condition
is so easy to check and so easy to state.

**Why it matters operationally.** A symmetric similarity function that a practitioner invents is
usually *not* a kernel, and the failure is not cosmetic: it means no feature space exists, the
optimisation problem is no longer convex, and a solver may return something meaningless without
complaining. The code file demonstrates this with `tanh(0.5 x.z + 1)`, which is symmetric and has
a smallest Gram eigenvalue of **-42.66** on 400 real rows.

**Honest boundary: the converse.** Mercer's theorem gives the other direction, that a continuous
symmetric function satisfying `integral integral K(u,v) g(u) g(v) du dv > 0` for every
square-integrable `g` **is** a dot product in some feature space. That direction needs the spectral
theory of integral operators, which is beyond this course. The page states it, attributes it to
Cortes and Vapnik section 4, and says plainly that the reader is being given the statement and not
the argument. The direction proved above is the one an engineer uses, because it is the one that
turns "is my similarity legal" into "run an eigenvalue check".

## Planned figures

1. **Orientation, `flowchart LR`,** as beat 2.
2. **`svg.chart`, the lift.** Two panels in one `viewBox`: concentric rings in 2-D that no line
   separates, and the same points plotted against `x1^2 + x2^2`, separated by a horizontal line.
3. **`flowchart LR`, the two routes to the same number.** Top: `x, z` -> `phi(x), phi(z)` in 6-D ->
   dot product -> `k`. Bottom: `x, z` -> `(x.z + 1)^2` -> the same `k`. Both arrive at one node.
   Kills "the kernel trick is an approximation".
4. **`svg.chart`, the Cortes and Vapnik table as a chart.** Polynomial degree against USPS raw
   error on the left axis (12.0, 4.7, 4.4, 4.3, 4.3, 4.2, 4.3) and feature-space dimensionality on
   a log right axis (256 up to about `10^16`). Error flattens while dimension explodes.
5. **`svg.chart`, the Gram spectrum.** Sorted eigenvalues of four Gram matrices on the same 400
   rows: linear, polynomial, RBF and the `tanh` counterexample, with zero as a `ref` line. Only one
   curve crosses it.

## The worked example, with its numbers

The identity by hand, then the economics. Eight parts.

1. `x = (2, 1)`, `z = (1, 3)`.
2. `x . z = 2 + 3 = 5`, so `k = (5 + 1)^2 = 36`. Two multiplications and an add.
3. The long way: `phi(x) = (1, 2.8284, 1.4142, 4, 2.8284, 1)`.
4. `phi(z) = (1, 1.4142, 4.2426, 1, 4.2426, 9)`.
5. `phi(x) . phi(z) = 1 + 4 + 6 + 4 + 12 + 9 = 36`. **The same number**, six multiplications in a
   bigger space.
6. **Sanity check.** `(x.z + 1)^2` is a square, so it cannot be negative. If your explicit route
   gave a negative answer you dropped a `sqrt2` and broke the correspondence.
7. **What changes if** the inputs are 256-dimensional? The degree-2 feature space has
   `C(258, 2) = 33,153` coordinates. The kernel is still one dot product and one square: 257
   multiplications against 33,153, a factor of 129. At degree 4 it is 186,043,585 against 259, a
   factor of 718,315, and the kernel column has not moved.
8. **Quoted, Cortes and Vapnik 1995, table 2.** US Postal Service digits, 16x16 pixels, 7,300
   training and 2,000 test patterns, input dimension 256. Degree 1: 12.0 per cent error, 200
   support vectors, feature space 256. Degree 2: 4.7 per cent, 127 support vectors, feature space
   about 33,000. Degree 4: 4.3 per cent, 165 support vectors, feature space about `10^9`.
   A classifier described by 165 vectors, implicitly living in a space nobody built.

**A discrepancy the page must own.** The paper's "about 33,000" for degree 2 matches `C(258,2) =
33,153` exactly. Its `10^9` for degree 4 does not match `C(260,4) = 186,043,585`, and its `10^16`
for degree 7 does not match `C(263,7) = 1.59 x 10^13`. Quote their figures as theirs, show the
`C(n+d, d)` arithmetic as separately derived, and do not present the two as the same claim.

## Quiz seeds

- **Q1 (misconception, M10).** What does the kernel trick let you avoid? **Answer: ever computing
  the feature vector `phi(x)`.** Distractors: computing the dot product; storing the training data;
  solving an optimisation problem.
- **Q2.** Which condition must `k(x, x')` satisfy to be a valid kernel? **Answer: its Gram matrix
  must be positive semi-definite for every finite sample.** Distractors: it must be symmetric and
  that is sufficient; it must be bounded by 1; it must decrease with distance.

## Practice seed

**Stem.** Inputs are two-dimensional. `x = (3, 1)`, `z = (2, 2)`. (a) Compute `k = (x.z + 1)^2`
directly. (b) Write out `phi(x)` and `phi(z)` and verify the same number. (c) Someone proposes
`s(x, z) = 1 / (1 + |x - z|)` as a similarity. Say what you would run to decide whether it is a
valid kernel, and what result would rule it out.

**Hint.** For (b), the six coordinates are the constant, the two linear terms scaled by `sqrt2`,
the two squares, and the cross term scaled by `sqrt2`.

**Solution.** (a) `x.z = 6 + 2 = 8`, so `k = 81`. (b) `phi(x) = (1, 4.2426, 1.4142, 9, 4.2426, 1)`;
`phi(z) = (1, 2.8284, 2.8284, 4, 5.6569, 4)`; the dot product is
`1 + 12 + 4 + 36 + 24 + 4 = 81`. (c) Build the Gram matrix on a few hundred of your own rows and
compute its eigenvalues with `numpy.linalg.eigvalsh`. Any eigenvalue meaningfully below zero rules
it out: no feature space exists, so the substitution is not licensed. A single tiny negative value
of order `1e-13` is rounding, not a verdict.

**`.p-check`.** Both routes in (a) and (b) must give the *same integer*. If they differ, you almost
certainly wrote `x1 x2` where the map needs `sqrt2 x1 x2`, and the cross term will be out by a
factor of two.

## Code and dataset plan

`code/0207-kernels.py` against `m10_signals.csv` plus a ring problem generated in the file. Verifies
the identity on ten random pairs to 8.9e-16; prints the multiplication-count table; **checks
Mercer's condition as an eigenvalue test** on linear, polynomial and RBF Gram matrices and on the
`tanh` counterexample; and solves the ring problem twice, linear ridge at 0.6650 accuracy against
kernel ridge at 1.0000, both in six lines.

## Sources, primary only

- Cortes and Vapnik, *Support-Vector Networks*, Machine Learning 20 (1995), section 4 and table 2.
  https://link.springer.com/content/pdf/10.1007/BF00994018.pdf
- Bishop, *PRML* (2006) eq 6.1 and the "kernel trick, also known as kernel substitution" paragraph
  in the chapter 6 introduction.
- **Note for the writer.** Boser, Guyon and Vapnik 1992 is the usual first citation and three
  mirrors returned 404 or HTML. Cortes and Vapnik 1995 covers the same material and was obtained;
  cite it and record the gap in `RESOURCES.md`.

## Primary source to go deeper

Cortes and Vapnik 1995, section 4. Three pages, and table 2 is the whole economic argument.
