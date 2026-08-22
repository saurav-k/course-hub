# 0008 - Counting what you cannot enumerate

| | |
|---|---|
| Module | M01 Foundations |
| Rung | foundation (`pill easy`) |
| Partition | core |
| Prose budget | 1,300 to 1,500 words |
| Prerequisites | `0002` (Cartesian product, power set), `0001` (`Prod`) |
| Needed by | M07 (the binomial distribution), M08 (sampling) |
| Code | `code/0008-counting-what-you-cannot-enumerate.py` |
| Dataset | `datasets/tickets.csv` |
| Named theorems | **`C(n,k) = n!/(k!(n-k)!)`, Pascal's rule, and `Sum_k C(n,k) = 2^n`.** All three proved (D4). |

## Boundary and absorption

M07 owns the binomial **distribution**; this page owns the **coefficient** in front of it.
M08 owns sampling with and without replacement as a probabilistic act.
This page carries the counting half of the absorbed lecture on counting and sampling, at full depth. Survey design is not mathematics and is not here.

## The one idea

Three questions decide every counting problem: does order matter, is repetition allowed, and how many are you choosing.

## Beats, in order

1. The multiplication rule, with a hyperparameter grid as its first example so the reader counts something they have actually run.
2. Ordered without repetition: `n!` for all of them, `n!/(n-k)!` for `k` of them.
3. Factorial growth against exponential growth, shown on a chart. `pedagogy.md` requires a quantitative figure for a growth claim.
4. Unordered without repetition: **`C(n,k)`, derived rather than asserted**.
5. The decision table: order against repetition, four cells, one formula per cell. Name the fourth even though machine learning rarely uses it, so the table is honest.
6. **Pascal's rule** and **`Sum_k C(n,k) = 2^n`**, both proved, closing the loop back to `0002`'s power set.
7. `2^n` is the number that makes things impossible, and it is the same number in three places: dropout's thinned networks, SHAP's coalitions, exhaustive feature selection. Use the dropout sentence verbatim, because it carries `2^n` and `O(n^2)` in one line and previews `0009`.
8. Where the factorials go when you are not counting: SHAP's attribution weight is built out of nothing else.

## The proofs (D4)

**The binomial coefficient.** The number of `k`-element subsets of an `n`-element set is `C(n,k) = n! / (k! (n-k)!)`.
*Proof by overcounting, which is the honest way round.* First count **ordered** selections of `k` distinct items: `n` choices, then `n-1`, down to `n-k+1`, giving `n!/(n-k)!` by the multiplication rule. Now every **unordered** `k`-subset was produced exactly `k!` times, once for each of the `k!` orderings of its own elements. Dividing a count by the constant number of times each object was counted gives the number of objects, so the subsets number `n!/((n-k)! k!)`.
**The step that does the real work** is that the overcount is the *same* for every subset. If different subsets were produced different numbers of times you could not divide by a single constant, and that is exactly what goes wrong when repetition is allowed.

**Pascal's rule.** `C(n,k) = C(n-1, k-1) + C(n-1, k)` for `0 < k < n`.
*Proof by a bijection, not by algebra.* Fix one particular element `x` of the `n`-set. Every `k`-subset either contains `x` or does not, and never both, so the two cases partition the collection. Those containing `x` are determined by choosing the remaining `k-1` elements from the other `n-1`, giving `C(n-1,k-1)`. Those not containing `x` are a choice of `k` from the other `n-1`, giving `C(n-1,k)`. Adding two disjoint counts gives the total.
**The step that does the real work** is choosing an element to condition on, which turns one hard count into two easy ones.

**The subset sum.** `Sum_{k=0}^{n} C(n,k) = 2^n`.
*Proof by counting one set two ways.* The left side counts every subset of an `n`-set by first grouping them by size. The right side counts the same subsets by walking the `n` elements and making an independent in-or-out choice at each, which is the multiplication rule with `2` repeated `n` times. Two correct counts of one collection must agree.
**The step that does the real work** is that both sides count the **same** collection. Double counting is the whole technique, and it is worth naming, because the reader will meet it again.

**Honest boundary.** These are the finite, no-repetition cases. Counting multisets and counting under symmetry are real subjects this course does not need and does not enter.

## Figures (4, at least one `svg.chart`)

- **F1 orientation, `flowchart LR`.** "Sets and the power set (0002)" to "THIS PAGE: three questions decide the count" to "the binomial distribution (M07), sampling (M08)".
- **F2 `flowchart TD`.** The decision tree: "Does order matter?" then "Is repetition allowed?", four leaves, one formula in each. The page's spine.
- **F3 inline `svg.chart`.** Growth on a log-y axis for `n` from 1 to 20: `n`, `n^2`, `2^n`, `n!`, with the crossing of `n!` over `2^n` marked. Kills: that factorial and exponential are "both just fast".
- **F4 inline `svg.chart`.** Pascal's triangle, rows 0 to 6, drawn as numbers, with each row's sum annotated on the right as `2^n`, and one cell highlighted with the two cells above it that produced it. Kills: that `C(n,k)` is unrelated to the power set, and it draws Pascal's rule rather than stating it.

## Worked example (eight parts)

SHAP's exact Shapley value for feature `i` sums over **every subset** of the other features, with weight `card(S)! (card(F) - card(S) - 1)! / card(F)!`.
With 15 features: `2^15 = 32,768` coalitions, so at 1 ms per model evaluation one explanation costs 33 seconds, and 20 features costs 17.5 minutes.
Subsets of the other 14 of size 7 number `C(14,7) = 3,432`, each weighted `7! x 7! / 15! = 1.9425e-5`, so that layer contributes `3,432 x 1.9425e-5 = 0.06667`.

That last number is `1/15` exactly, and it is `1/15` for **every** size from 0 to 14, because `C(14,s) x s!(14-s)!/15!` collapses to `14!/15!`.
Fifteen layers each contributing `1/15`, summing to exactly 1, which is what a weighted average must do.

- **Sanity check.** The fifteen contributions sum to 1. If they do not, the weight or the subset count is wrong.
- **What changes if** one more feature is added: the coalition count doubles to 65,536 and the per-layer share becomes `1/16`.

## Code

`code/0008-counting-what-you-cannot-enumerate.py`.
Against `tickets.csv`: takes the top-12 tokens as a feature set and **enumerates all `2^12` subsets explicitly**, asserting the enumerated count equals `2^12` and equals `Sum_k C(12,k)`, which is the third theorem checked by brute force rather than believed.
Then verifies Pascal's rule across a triangle computed two ways, verifies `C(n,k) = C(n,n-k)`, and computes the SHAP layer weights for `card(F) = 15`, asserting every layer sums to `1/15` and the total to 1.
Finally it times the growth of `2^n` to show where enumeration stops being possible.

## Quizzes

- **Q1** (misconception): the dropout paper says a net with `n` units is a collection of how many thinned networks?
  `2 to the n, one per subset` / `n squared, one per unit pair` / `n factorial, one per ordering` / `n choose 2, one per pairing`
  Feedback: option 2 is the paper's **parameter** count, `O(n^2)`, in the very same sentence, which makes it the strongest distractor; options 3 and 4 count orderings and pairs, and dropout picks a subset, where order is irrelevant.
- **Q2** (misconception): how many ways can you choose 3 validation folds from 10 when order does not matter?
  `10! divided by 7!, which is 720` / `10 to the 3rd power, giving 1000` / `3 to the 10th power, a big number` / `10! divided by 3!7!, giving 120`
  Feedback: option 1 is the **ordered** count and is exactly `3! = 6` times too big, which is the overcount this page's first proof divides out; option 2 allows repetition and order; option 3 has `n` and `k` swapped.

## Practice

(a) A grid of 4 learning rates, 3 depths and 2 optimisers, with 5-fold cross-validation. How many model fits?
(b) Instead you try **every subset** of 12 candidate features. How many fits, and at 2 seconds each, how long?
(c) How many of those subsets use exactly 5 features?
(d) Check that the counts by size add up to the total in (b).

- **Hint.** (a) is the multiplication rule; (b) is the power set; (d) is this page's third theorem.
- **Solution.** (a) `4 x 3 x 2 x 5 = 120`. (b) `2^12 = 4,096` fits, `8,192` seconds, about **2.3 hours**. (c) `C(12,5) = 12!/(5! 7!) = 792`. (d) `Sum_{k=0}^{12} C(12,k) = 4,096`, matching (b) exactly.
- **`.p-check`.** (c) must be smaller than (b), and by a lot: one size cannot outnumber all thirteen sizes together.

## Primary sources to go deeper

Srivastava et al., *Dropout: A Simple Way to Prevent Neural Networks from Overfitting*, JMLR 15 (2014), section 2.
Lundberg and Lee, *A Unified Approach to Interpreting Model Predictions*, equation 4.
