# 0107 - KL divergence

**Module** M10 - lesson 03  **Rung** working  **Class** core

## The single tight idea

Subtract the floor from the bill and what is left measures only the model's error - and that
number is directional, so the direction you pick decides what your fitted model looks like.

## Prerequisites

0105 (entropy), 0106 (cross-entropy). M05 for convexity as a picture; this page uses Jensen's
inequality and states it rather than proving it, because M06 owns convexity.

## Beats, in order

1. **One-minute version.** `KL(p||q) = H(p,q) - H(p)`. Zero only when `p = q`. Never negative.
   Not symmetric. Infinite when `q` rules out something `p` allows.
2. **Orientation figure.** 0106's "what you pay" minus 0105's "what you must pay" into "this page:
   the excess", into 0108 (mutual information) and the KL term in an RLHF objective.
3. **Mechanism by subtraction, not by definition.** Write `H(p,q)`, write `H(p)`, subtract, and the
   log ratio falls out. Deriving it this way means the reader never has to accept a new formula.
4. **Non-negativity, picture first.** The chord-above-the-curve figure for `-log`, then the algebra.
   **Named theorem: Gibbs' inequality.** This is the module's central proof; see below.
5. **Why "distance" is the wrong word**, as four separate failures, one line each: not symmetric;
   fails the triangle inequality; infinite on a single ruled-out outcome; and the units are bits,
   not length. Page 0110 owns the metric axioms and this page hands it the four failures.
6. **The asymmetry with its consequence.** Forward `KL(p||q)` punishes `q` for being small where
   `p` is large, so it is mean-seeking and smears across modes. Reverse `KL(q||p)` punishes `q` for
   being large where `p` is small, so it is mode-seeking and picks one. Numbers below.
7. **Where each direction is used, named.** Maximum likelihood is forward KL against the empirical
   distribution (M09 owns the derivation). Variational inference minimises reverse KL. The RLHF and
   DPO penalty is a KL to a reference policy; cross-link out to
   `../../llm-papers-course/lessons/0025-dpo.html`.
8. **Trade-off, same section.** Because it is not a metric you cannot use it as an index key,
   cluster with it naively, or average it. Name Jensen-Shannon divergence as the symmetric repair
   in one sentence and say its square root is a metric.

**Do not do here:** Wasserstein, `f`-divergences in general, variational inference.

## The stated proof (D4)

**Theorem (Gibbs' inequality).** For distributions `p` and `q` over the same finite alphabet,
`KL(p || q) >= 0`, with equality if and only if `p_i = q_i` for every `i`.

*Proof, in full.* Work in nats; the base only scales the answer. Write

```
-KL(p || q) = sum_i p_i ln (q_i / p_i)
```

restricting the sum to the `i` with `p_i > 0`, which the `0 log 0 = 0` convention licenses. The
function `ln` is **concave**, so Jensen's inequality lets the expectation move inside:

```
sum_i p_i ln (q_i / p_i)  <=  ln ( sum_i p_i * (q_i / p_i) )
                          =   ln ( sum_i q_i )
                          <=  ln 1  =  0
```

so `-KL <= 0`, that is `KL >= 0`.

**The step that does the real work** is the first inequality, and it is worth naming precisely why
it is the whole proof: Jensen turns "the average of a log" into "the log of an average", and the
average of `q_i / p_i` under `p` is just `sum q_i`, which the normalisation pins at 1. Every other
line is arithmetic.

**The equality case.** `ln` is *strictly* concave, so Jensen is an equality only when the quantity
inside is constant across every outcome `p` gives positive weight, that is `q_i / p_i = c` for all
such `i`. Summing, `c sum p_i = sum q_i` over that support, so `c <= 1`; and the second inequality
above is an equality only when `sum q_i = 1` over that same support, forcing `c = 1` and `q = p`.
So equality holds exactly when the two distributions agree.

**Honest boundary.** The proof above assumes a finite alphabet. For continuous distributions the
same argument runs with integrals and the same conclusion holds, but "equality" weakens to
"equal almost everywhere", and this course does not develop the measure theory that makes that
phrase precise.

## Planned figures

1. **Orientation, `flowchart LR`,** as beat 2.
2. **`svg.chart`, the asymmetry, drawn as it behaves.** A bimodal `p` as a filled `f-prob` curve
   with two fitted single Gaussians overlaid: the forward-KL fit (`s-stat`) straddling both modes
   at `mu = 0.000, sigma = 3.250`, the reverse-KL fit (`s-alarm`) sitting on one at
   `mu = +3.000, sigma = 0.800`. Both numbers come from the code file's grid search. The single
   most useful figure in the module.
3. **`svg.chart`, the convexity picture.** `-ln x` with a chord above it. That is the whole proof.
4. **`flowchart LR`, the metric checklist.** Four boxes for four properties, ticks and crosses for
   KL beside Euclidean distance. Kills "KL is a distance".

## The worked example, with its numbers

Both directions on the same pair, eight parts, derived.

1. `p = [0.9, 0.05, 0.05]`, `q = [0.34, 0.33, 0.33]`.
2. `H(p) = 0.5690` bits.
3. `H(p, q) = 1.5607` bits.
4. `KL(p || q) = 1.5607 - 0.5690 = 0.9917` bits.
5. Swap them: `KL(q || p) = 1.3193` bits.
6. Same two distributions, two answers, **33 per cent apart**. Not rounding.
7. **Sanity check.** Both must be non-negative and both must be zero when the arguments match:
   `KL(p || p) = 0.0000`. If either came out negative, a probability did not sum to one.
8. **What changes if** the model rules an outcome out? Set `q_3 = 0` while `p_3 = 0.05`. Then
   `KL(p || q) = infinity`, while `KL(q || p)` stays finite. One unseen event in one direction
   destroys the whole quantity, which is why a language model must never emit an exact zero and
   why smoothing exists.

## Quiz seeds

- **Q1 (misconception, M2 "KL is a distance").** `KL(p||q) = 0.99` bits. What is `KL(q||p)`?
  **Answer: it cannot be determined from this.** Distractors: `0.99`; `-0.99`; `1/0.99`. All three
  encode the same wrong belief in three different disguises.
- **Q2.** You fit one Gaussian `q` to a two-mode `p` by minimising `KL(q||p)`. What does the fit
  look like? **Answer: it sits on one mode and ignores the other.** Distractors: it straddles both
  (true of the *other* direction, which makes it the strongest distractor); it sits in the valley
  between them; it matches the overall mean and variance.

## Practice seed

**Stem.** `p = [0.5, 0.5]` and `q = [0.99, 0.01]` over two outcomes. (a) Compute both divergences
in bits. (b) Now set `q = [1.0, 0.0]` and compute both again. (c) In one sentence, say why a
language model must never output an exact zero.

**Hint.** In (a) one of the two terms is negative. That is allowed; only the total is constrained.

**Solution.** (a) `KL(p||q) = 0.5 log2(0.5/0.99) + 0.5 log2(0.5/0.01) = -0.4928 + 2.8219 = 2.3291`
bits. `KL(q||p) = 0.99 log2(1.98) + 0.01 log2(0.02) = 0.9757 - 0.0564 = 0.9193` bits. A factor of
2.53. (b) `KL(p||q) = infinity`, because `p_2 = 0.5 > 0` while `q_2 = 0`. `KL(q||p) = 1 * log2 2 = 1`
bit, finite. (c) A single token the model rules out entirely makes the forward KL, and therefore
the cross-entropy loss, infinite the moment that token occurs.

**`.p-check`.** Both answers in (a) must be positive even though one term inside each is negative.
If you got a negative total, check that both vectors sum to exactly 1.

## Code and dataset plan

`code/0107-kl-divergence.py` against `m10_classifier.csv` and `m10_signals.csv`. Computes KL from
the definition and again as `H(p,q) - H(p)`; **tests Gibbs' inequality over 10,000 random Dirichlet
pairs** and reports the smallest value seen (0.006997 bits, never negative); measures the asymmetry
(0.060771 against 0.071421 bits, ratio 1.1753); demonstrates the infinity; and **grid-searches the
best single Gaussian under each direction of KL** against a two-mode target, returning
`mu = 0.000, sigma = 3.250` forward and `mu = +3.000, sigma = 0.800` reverse. No optimiser to
trust; every number checkable.

## Sources, primary only

- Bishop, *PRML* (2006) eq 1.113 to 1.118: the definition, the convexity argument, Jensen, and the
  equality case.
- Goodfellow, Bengio and Courville, *Deep Learning* (2016) section 3.13 eq 3.50, and figure 3.6 for
  the two fitted directions. https://www.deeplearningbook.org/contents/prob.html
- Kullback and Leibler, *On Information and Sufficiency*, Annals of Mathematical Statistics 22(1)
  (1951), for the original. **Note for the writer:** the Project Euclid PDF returned an HTML
  interstitial when I tried it; cite it, and if it cannot be fetched at writing time, say in
  `RESOURCES.md` under `## Gaps` that the definition is taken from Bishop and Goodfellow rather
  than the 1951 paper.

## Primary source to go deeper

Bishop, *PRML*, section 1.6.1. Five pages, and it carries the proof above in its own notation.
