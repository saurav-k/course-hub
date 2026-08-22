# 0203 - Mutual information

**Module** M10 - lesson 04  **Rung** working  **Class** core

## The single tight idea

Mutual information is the KL divergence between "the world where these two columns are related"
and "the world where they are not", so a zero really does mean independent - which is more than a
correlation of zero can say.

## Prerequisites

0202 (KL). M07 for independence and joint distributions. M08 for covariance and correlation, so
the contrast in beat 5 lands.

## Beats, in order

1. **One-minute version.** `I(X;Y) = KL(p(x,y) || p(x)p(y))`. It equals `H(Y) - H(Y|X)`. It is zero
   if and only if the two are independent. Correlation zero does not say that.
2. **Orientation figure.** 0202's "KL between any two distributions" into "this page: KL between
   the joint and the product of the marginals" into 0209 (a decision tree split) and 0206 (the PMI
   matrix behind word embeddings).
3. **Mental model: the two-circle overlap.** `H(X)`, `H(Y)`, overlap `I(X;Y)`, union `H(X,Y)`.
   Draw it, then immediately say what the picture does not survive: the analogous three-variable
   region can be negative, so the diagram is a mnemonic and not a proof.
4. **Mechanism, three forms.** `I = H(X) - H(X|Y) = H(Y) - H(Y|X) = H(X) + H(Y) - H(X,Y)`. Shannon
   writes the same three identities for his "rate of transmission" on page 21 of the 1948 paper, so
   these are his, not a modern repackaging. **Named theorem, see proof.**
5. **Non-negativity comes free**, because it is a KL: 0202 already proved it. **One-way cross-link,
   allowed by captain update 3 and genuinely useful here:**
   `../../statistical-foundations-ml-course/lessons/0007-leading-indicators-and-correlation.html`
   teaches correlation as a diagnostic and its traps; this page is where the reader learns what
   correlation cannot see at all. Link out to it, never edit it: that course is frozen. And `I = 0` exactly
   when `p(x,y) = p(x)p(y)`, which is the definition of independence. Say plainly: **this is the
   thing correlation cannot do.** `Y = X^2` with `X` symmetric about zero is the standing
   counterexample and the worked example below.
6. **Pointwise mutual information**, `PMI(x,y) = log2 (p(x,y) / (p(x)p(y)))`, with the note that
   PMI can be negative while its expectation under the joint cannot. Page 0206 needs this definition.
7. **Trade-off, same section, and it is severe.** Mutual information is hard to estimate.
   McAllester and Stratos prove that any distribution-free high-confidence lower bound from `N`
   samples cannot exceed `2 ln N + 5`. With `N = 128` that ceiling is about 14.7 nats however much
   information is really there. One warning callout, because readers meet MINE and InfoNCE and
   assume the estimates are measurements.

**Do not do here:** the information bottleneck, MIC, continuous estimators beyond naming them.

## The stated proofs (D4)

**Theorem (the three forms agree).** `I(X;Y) = KL(p(x,y) || p(x)p(y)) = H(Y) - H(Y|X)
= H(X) + H(Y) - H(X,Y)`.

*Proof, in full.* Start from the KL form and split the logarithm:

```
KL(p(x,y) || p(x)p(y)) = sum_{x,y} p(x,y) log2 ( p(x,y) / (p(x) p(y)) )
                       = sum_{x,y} p(x,y) log2 p(x,y)
                         - sum_{x,y} p(x,y) log2 p(x)
                         - sum_{x,y} p(x,y) log2 p(y)
                       = -H(X,Y) + H(X) + H(Y)
```

The second and third sums collapse because summing `p(x,y)` over `y` gives `p(x)`, so
`sum_{x,y} p(x,y) log2 p(x) = sum_x p(x) log2 p(x) = -H(X)`, and symmetrically for `y`. That gives
the third form. For the second, substitute the chain rule `H(X,Y) = H(X) + H(Y|X)`, which page 0200
established as Shannon's property 5:

```
H(X) + H(Y) - H(X,Y) = H(X) + H(Y) - H(X) - H(Y|X) = H(Y) - H(Y|X)
```

**The step that does the real work** is the marginalisation in the middle: `log2 p(x)` does not
depend on `y`, so summing the joint over `y` turns a double sum into a single one. That one move
is what makes three apparently different quantities the same number.

**Corollary.** `I(X;Y) >= 0`, with equality if and only if `X` and `Y` are independent. It is a KL,
so Gibbs from 0202 applies directly, and the equality case of Gibbs says `p(x,y) = p(x)p(y)`
everywhere, which is exactly independence. **Consequence worth stating on the page:**
`H(Y|X) <= H(Y)`. Conditioning never increases entropy on average. Shannon states it as
"the uncertainty of `y` is never increased by knowledge of `x`".

## Planned figures

1. **Orientation, `flowchart LR`,** as beat 2.
2. **`svg.chart`, the two overlapping circles**, hand-drawn because Mermaid cannot: `H(X)`, `H(Y)`,
   `H(X|Y)`, `H(Y|X)`, `I(X;Y)` and `H(X,Y)` all labelled on one figure.
3. **`svg.chart`, the counterexample.** A scatter of `Y = X^2` with `X` symmetric about zero, with
   `corr = +0.0004` and `I(X;Y) = 1.0000 bits` printed on the figure. Highest-value figure on the page.
4. **`svg.chart`, the estimation ceiling.** `2 ln N + 5` against `N` on a log axis with a `ref`
   line at a true MI, showing where the certifiable bound crosses it.
5. **`svg.chart`, the plug-in bias**, from the code file: measured `I` against the number of
   distinct values of a column that is independent by construction, rising from 0.000005 bits at
   two values to 0.574493 bits at twelve thousand.

## The worked example, with its numbers

A 2x2 contingency table, eight parts, derived.

1. 100 rows. `(F=0,Y=0) = 40`, `(0,1) = 10`, `(1,0) = 20`, `(1,1) = 30`.
2. Marginals: `p(F) = [0.5, 0.5]`, `p(Y) = [0.6, 0.4]`.
3. `H(Y) = -0.6 log2 0.6 - 0.4 log2 0.4 = 0.9710` bits.
4. `H(Y|F) = 0.5 H(0.8) + 0.5 H(0.6) = 0.5(0.7219) + 0.5(0.9710) = 0.8464` bits.
5. `I(F;Y) = 0.9710 - 0.8464 = 0.1245` bits. Knowing the feature removes **12.8 per cent** of the
   label uncertainty.
6. One PMI cell: `log2(0.30 / (0.5 * 0.4)) = log2 1.5 = +0.585` bits. That pair co-occurs more than
   chance.
7. **Sanity check.** `I` cannot exceed `min(H(F), H(Y)) = min(1.0000, 0.9710)`. 0.1245 is well
   under. If you got a number above either marginal entropy, a cell probability is wrong.
8. **The counterexample, and what changes.** `X` uniform on `{-2,-1,1,2}`, `Y = X^2`. Pearson
   correlation is `+0.0004`, indistinguishable from zero. But `Y` is a deterministic function of
   `X`, so `H(Y|X) = 0` and `I(X;Y) = H(Y) = 1.0000` bit exactly. Zero correlation, one full bit of
   dependence. **What changes if** you square `X` before correlating? The correlation becomes 1.
   Correlation measures a *linear* relation between the columns you hand it; mutual information
   measures dependence of any shape.

## Quiz seeds

- **Q1 (misconception).** `corr(X,Y) = 0`. Which of these follows? **Answer: nothing about
  independence follows.** Distractors: they are independent; `I(X;Y) = 0`; `H(X|Y) = H(X)`. The
  last two are the same wrong claim wearing information-theory clothes, which is the point.
- **Q2.** `I(X;Y) = H(Y) - H(Y|X)`. If `X` determines `Y` exactly, what is `I(X;Y)`?
  **Answer: `H(Y)`.** Distractors: 1 bit; `H(X)`; zero.

## Practice seed

**Stem.** A 100-row table: feature `F` is 1 for 50 rows; label `Y` is 1 for 40 rows; of the 50 rows
with `F = 1`, thirty have `Y = 1`. (a) Fill in the 2x2 table. (b) Compute `H(Y)`, `H(Y|F)` and
`I(F;Y)` in bits. (c) A second feature `G` is a random 100-value identifier. Say what `I(G;Y)`
computes to on this sample and what it is in the population, and why the two differ.

**Hint.** For (c), work out how many rows share any given value of `G`.

**Solution.** (a) `(1,1)=30, (1,0)=20, (0,1)=10, (0,0)=40`. (b) as the worked example: 0.9710,
0.8464, **0.1245** bits. (c) Each value of `G` appears once, so knowing `G` determines the row and
therefore `Y`: `H(Y|G) = 0` and `I(G;Y) = H(Y) = 0.9710` bits, the maximum possible. In the
population it is exactly zero. The gap is plug-in estimation bias, it grows with the number of
distinct values, and page 0209 shows the same effect wrecking a decision tree.

**`.p-check`.** `I(F;Y)` must be at most `min(H(F), H(Y))`. Here that is 0.9710, so anything above
that is arithmetic gone wrong, not a discovery.

## Code and dataset plan

`code/0203-mutual-information.py` against `m10_signals.csv`. Computes `I` all three ways and
asserts they agree to 1e-12 on every column; prints the PMI table; builds `Y = X^2` on 40,000
samples and reports correlation `+0.000387` beside `I = 0.999993` bits; and sweeps the plug-in bias
from 2 to 12,000 distinct values on a column independent by construction. Measured: `plan` 0.056819
bits, `support_tier` 0.005494, `theme` 0.000011 (true value exactly zero).

## Sources, primary only

- Shannon 1948, page 21: `R = H(x) - H_y(x) = H(y) - H_x(y) = H(x) + H(y) - H(x,y)`, and the
  "never increased by knowledge" statement in section 6, property 6.
- Bishop, *PRML* (2006) eq 1.120 and 1.121.
- McAllester and Stratos, *Formal Limitations on the Measurement of Mutual Information*, AISTATS
  2020, Theorem 1.1. https://arxiv.org/pdf/1811.04251

## Primary source to go deeper

McAllester and Stratos 2020. It is the paper that stops a reader trusting a large MI estimate.
