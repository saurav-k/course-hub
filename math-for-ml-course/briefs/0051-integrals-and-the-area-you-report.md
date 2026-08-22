# 0051 - Integrals in machine learning: the area you report is a number you actually compute

> Number claimed under #42 from the roadmap count in `../index.html`. Report label C12.

| | |
|---|---|
| Module | M05 Calculus |
| Rung | working (`pill med`) |
| Label | `core` |
| Prerequisites | 0041. M01: set notation and summation. |
| Enables | **M07, as a hard scheduling edge** (a density integrating to one is an integral, and a CDF is an integral), and M08's expectation |

## The single tight idea

An integral is an accumulation, the most-reported number in applied machine learning is
one, and it also has a meaning that has nothing to do with area.

## Beats, in order

1. **Accumulation before notation.** Chop the region into rectangles, add them, shrink
   the width. That limit is the definite integral. No `int` sign until the reader has
   added rectangles.
2. **The fundamental theorem, in one sentence and one picture.** Differentiation and
   integration undo each other. This is why the exponential tail M07 will meet collapses
   to a single term.
3. **The trapezoid rule, because that is what actually runs.** Trapezoids beat rectangles
   because they average across each interval, and a block of tied scores makes a sloped
   segment that a rectangle systematically mis-measures.
4. **The ROC curve, built from scratch.** Sort by score, sweep the threshold, plot the
   true-positive rate against the false-positive rate.
5. **Worked: the area, by the trapezoid rule, on twenty thousand real predictions.**
6. **The reframing, boxed as `.card.callout.key`.** That same area is the probability that
   a randomly chosen positive outranks a randomly chosen negative. Compute it the second
   way on the same data and get the same number.
7. **Preview and hand-off.** Expectation is an integral against a density. One figure,
   then M07 takes the density and M08 takes the expectation.

## Named theorems and their stated proofs

**Theorem 1 (the fundamental theorem of calculus, both parts).**

> Let `f` be continuous on `[a, b]`.
> **(i)** The function `F(x) = int_a^x f(t) dt` is differentiable on `(a,b)` with
> `F'(x) = f(x)`.
> **(ii)** If `G` is any antiderivative of `f` on `[a,b]`, then
> `int_a^b f(t) dt = G(b) - G(a)`.
>
> *Proof of (i).* For `h != 0`,
> `(F(x+h) - F(x)) / h = (1/h) int_x^{x+h} f(t) dt`.
> By the mean value theorem for integrals, which holds because `f` is continuous on the
> closed interval between `x` and `x+h`, there is a point `c_h` in that interval with
> `int_x^{x+h} f(t) dt = f(c_h) h`. So the quotient equals `f(c_h)`. As `h -> 0`, `c_h`
> is squeezed onto `x`, and `f` is continuous at `x`, so `f(c_h) -> f(x)`. Hence
> `F'(x) = f(x)`.
> *Proof of (ii).* By (i), `F` is an antiderivative of `f`. Any two antiderivatives differ
> by a constant, because their difference has zero derivative on an interval and is
> therefore constant by the mean value theorem. So `G = F + C` for some constant `C`, and
> `G(b) - G(a) = (F(b) + C) - (F(a) + C) = F(b) - F(a) = int_a^b f - 0`. **QED**

**Theorem 2 (the area under the ROC curve is a ranking probability).** This is the page's
reframing beat and it is the reason the page exists, so it gets the full argument.

> Let a scoring classifier assign scores to `P` positive and `N` negative instances. Let
> `S+` be the score of a uniformly random positive and `S-` of an independent uniformly
> random negative. Then the area under the ROC curve, computed by the trapezoid rule over
> the empirical curve, equals
>
>   `Pr(S+ > S-) + (1/2) Pr(S+ = S-)`.
>
> *Proof.* Sweep the threshold from above every score downwards. At threshold `t` the
> curve sits at `(FPR(t), TPR(t))` where `TPR(t) = (1/P) #{positives with score >= t}` and
> `FPR(t) = (1/N) #{negatives with score >= t}`. Consider what happens as the threshold
> passes one distinct score value `s`, admitting `p` positives and `q` negatives that are
> tied at `s`. The curve moves right by `q/N` and up by `p/P`, and the trapezoid over that
> step contributes
>
>   `(q/N) * [ TPR_before + (p/P)/2 ]`
>
> where `TPR_before` is the fraction of positives already admitted, that is those with
> score strictly greater than `s`. Multiply through by `P N`:
>
>   `q * #{positives with score > s}  +  (1/2) p q`.
>
> Summing over all distinct score values `s`, the first term counts every ordered pair
> (positive, negative) in which the negative has score exactly `s` and the positive
> strictly beats it, so over the whole sweep it counts every strictly-winning pair exactly
> once. The second term counts half of every tied pair exactly once. Dividing back by
> `P N`, the total is
>
>   `#{pairs with S+ > S-}/(P N)  +  (1/2) #{pairs with S+ = S-}/(P N)`,
>
> which is the stated probability, since the pair is drawn uniformly from the `P N`
> pairs. **QED**
>
> The identity is due to Bamber (1975) and is the form Hanley and McNeil (1982) made
> standard in the medical literature; Fawcett (2006) states it as "the AUC of a classifier
> is equivalent to the probability that the classifier will rank a randomly chosen
> positive instance higher than a randomly chosen negative instance", and notes it is
> equivalent to the Wilcoxon test of ranks.

## Figures

1. **Orientation, `flowchart LR`.** "The derivative (0041)" into "THIS PAGE: its inverse,
   and the areas machine learning reports" into "densities (M07)" and "expectation (M08)".
2. **`svg.chart`.** Rectangles under a curve at three widths converging on the smooth
   area, with the running total printed for each.
   *Kills:* "an integral is an antiderivative". It is an accumulation, and the
   antiderivative is how you evaluate it.
3. **`svg.chart`, quantitative, real data.** The ROC curve of the score table with the
   trapezoids drawn under it. *Kills:* "AUC is computed by an opaque library call".
4. **`svg.chart`, quantitative, same data.** A grid of positive-negative pairs, shaded
   where the positive outranks the negative, annotated with the same number the integral
   gave. *Kills:* "the area and the ranking probability are two separate facts".
5. **`flowchart LR`.** Derivative and integral as inverse arrows, with three destinations
   hanging off the integral: area under a curve, expectation, and the normalising constant
   of a density. Hands off explicitly to M07 and M08.

## Worked example, in eight parts

1. **Setting.** Twenty thousand held-out predictions from a binary classifier. The team
   reports an AUC. What number is that, and what does it mean?
2. **Symbolic.** `.math` for the trapezoid rule
   `int ~= sum (x_{i+1} - x_i)(y_i + y_{i+1})/2`, with a `.gloss` naming every symbol and
   saying which axis is which.
3. **Picture.** Figure 3, the curve with its trapezoids, before any arithmetic.
4. **`ol.worked`.** Sort by descending score. Sweep, consuming ties as a block. Accumulate
   trapezoids. Then count ranked pairs directly and divide.
5. **`.keynum`** on nothing: derived here from the committed dataset.
6. **Sanity check.** The area must lie in `[0, 1]`, and a classifier no better than
   guessing gives `0.5`, so anything below `0.5` means the scores are inverted rather than
   uninformative. And the two routes must agree exactly, not approximately: they are the
   same sum rearranged.
7. **What changes if** the class balance changes? Nothing. Both the true-positive rate and
   the false-positive rate are ratios within a single column of the confusion matrix, so
   neither depends on the mix. That is why AUC survives a change in prevalence when
   accuracy and precision do not.
8. **In words.** An AUC of `0.857` says that if you pick one positive and one negative at
   random, the model scores the positive higher about 86 times in 100. It says nothing
   about any particular threshold.

## Quiz seeds

**Q1, misconception.** A classifier's AUC is `0.857`. What does that mean?
*Answer:* pick one positive and one negative at random; the probability the positive
scores higher is `0.857`.
*Distractors:* "85.7 per cent of predictions are correct" is accuracy; "the model is right
85.7 per cent of the time above the threshold" invents a threshold AUC does not have;
"85.7 per cent of the area lies above the diagonal" misreads the geometry.

**Q2.** Why does the AUC algorithm add trapezoids rather than rectangles?
*Answer:* a trapezoid averages the two endpoint heights, which is exactly right on the
sloped segment a block of tied scores produces.
*Distractors:* "rectangles are harder to compute" is false; "trapezoids are exact for any
curve" is false; "the ROC curve is always a straight line" is false.

## Practice seed

**Stem.** Using this twenty-instance published test set
(`p .9, p .8, n .7, p .6, p .55, p .54, n .53, n .52, p .51, n .505, p .4, n .39, p .38,
n .37, n .36, n .35, p .34, n .33, p .30, n .1`): sweep the threshold and list the ROC
points, sum the trapezoids, then count the positive-negative pairs where the positive
scores higher and divide by 100. Say what it means that the two agree.

**Hint.** Ten positives and ten negatives, so a hundred pairs. Count the pairs directly:
for each positive, how many negatives does it beat?

**Solution.** Both routes give `0.68`. They agree because the area and the ranking
probability are the same quantity, which is the Wilcoxon rank statistic, so an AUC is a
statement about ranking and not about any particular threshold.

**`.p-check`.** The pair count must be a whole number out of 100 before you divide, and
`68` is. A fractional count before dividing means a tie was mishandled; there are no ties
in this table, so there should be no halves.

**Attribution note for the writer.** The twenty-row table is Fawcett (2006) Figure 3.
**The paper prints the table and the curve but does not print the area.** Both `0.68`
figures are derived, so they are plain text on the page and never `.keynum`, and the page
must say they were computed here.

## Code and dataset

`../code/m05_12_auc_two_ways.py` against `../datasets/m05-scores.csv` (20,000 rows).
It builds the ROC curve, integrates it by the trapezoid rule, computes the same number by
the Mann-Whitney rank sum, and then counts every pair by brute force as a third check.

Verified output to quote: 6,175 positives and 13,825 negatives, which is `85,369,375`
pairs; the ROC curve has `19,798` points; and the three routes give
**`0.85650938055948` each, with a largest gap of `0.000e+00`**. Coarsening the curve to
eleven points gives `0.8521946365`, an error of `4.31e-03`, and the error falls
monotonically as points are added. Left rectangles give `0.8565091170` and right
rectangles `0.8565096441`, and their average is the trapezoid answer exactly.

Three independent routes agreeing to fourteen decimals is the strongest evidence this
module produces, and the page should say so plainly.

## Sources

- Fawcett, "An introduction to ROC analysis", *Pattern Recognition Letters* 27:861-874,
  2006. Section 7 for the AUC, for the statement that it equals the ranking probability
  and is equivalent to the Wilcoxon test of ranks, and for the trapezoid algorithm;
  section 4.2 for insensitivity to class skew and for why metrics using both columns of
  the confusion matrix are not. DOI `10.1016/j.patrec.2005.10.010`.
- Hanley and McNeil, "The meaning and use of the area under a receiver operating
  characteristic (ROC) curve", *Radiology* 143:29-36, 1982, DOI
  `10.1148/radiology.143.1.7063747`. **Bibliographic record confirmed through Crossref;
  the full text is behind a paywall and was not read.** Cite it as the origin of the
  identity, on Fawcett's attribution, and do not quote it.
- Deisenroth, Faisal and Ong, *Mathematics for Machine Learning*, section 6.7 for the
  change of variables that M08 will need. `https://mml-book.github.io/book/mml-book.pdf`
