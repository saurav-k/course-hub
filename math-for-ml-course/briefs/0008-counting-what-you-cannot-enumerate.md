# 0008 Counting what you cannot enumerate

| | |
|---|---|
| Module | M01 Foundations |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,300 to 1,500 prose words, excluding practice and quiz text |
| Source scout | `mlm-foundations-r2` L8 |

## One tight idea

Three questions decide every counting problem: does order matter, is repetition allowed, and how many are you choosing.

## Prerequisites

`0002` for the Cartesian product and the power set, `0001` for the product notation.

## Downstream

M07 owns the binomial **distribution**; this page owns the **coefficient** in front of it. M08 owns sampling with and without replacement as a probabilistic act.

## Boundaries: what this page must not teach

- **Not** probability. Nothing here divides by a sample space size; M07 does that.
- **Not** sampling as a statistical design. M02 owns survey designs, M08 owns sampling from a distribution. This page is pure counting.
- **Not** the binomial distribution.

## Beats, in order

1. The multiplication rule, with a hyperparameter grid as its first example, so the reader counts something they have actually run.
2. Ordered without repetition: `n!` for all of them, `n!/(n-k)!` for `k` of them.
3. Factorial growth against exponential growth, drawn. `pedagogy.md` requires a quantitative figure for a growth claim and this is it.
4. Unordered without repetition: the binomial coefficient. **Derive the division by `k!` rather than asserting it**: you counted every subset `k!` times, once per ordering.
5. The decision table: order against repetition, four cells, one formula per cell. Say which three machine learning uses and name the fourth so the table is honest.
6. Three properties worth holding: symmetry, Pascal's rule, and that the row sums to `2^n`, which closes the loop back to `0002`'s power set.
7. `2^n` is the number that makes things impossible, and it is the same number in three different places: dropout's thinned networks, coalition-based attribution, exhaustive feature selection.
8. Where the factorials go when you are not counting: a coalition attribution weight built out of nothing but factorials.

## Stated proof (D4)

**The binomial coefficient.** Required by D4 and it is the page's best moment, so it must not be asserted.

There are `n!/(n-k)!` ordered ways to pick `k` from `n`. Every unordered subset of size `k` is produced exactly `k!` times by that count, once for each ordering of its members. Dividing by `k!` therefore counts each subset once.

**The step that does the work** is "exactly `k!` times", and it is worth one sentence of its own: it holds because the `k` chosen items are distinct, so all `k!` orderings are different ordered picks. **State where it fails**: with repetition allowed the chosen items need not be distinct, the orderings collide, and the division is wrong. That is why the fourth cell of the table has a different formula.

## Figures

- **Orientation**, `flowchart`: *sets and the Cartesian product (`0002`)* -> **THIS PAGE: three questions that decide every count** -> *M07's binomial distribution, M08's sampling* -> *(dotted) M01*.
- **`svg.chart`**, required: `n!`, `2^n` and `n^2` on one log-y axis for n up to about 20, so the reader sees factorial outrunning exponential and both outrunning polynomial. The log axis is `0006`'s skill being used.
- **`flowchart`**: the three-question decision tree, ending in the four formulas.

## Worked example

A grid of 3 learning rates, 4 batch sizes and 2 optimisers: 24 runs by the multiplication rule. Then: how many ways to pick 3 of 10 features, ordered and unordered, showing the `3! = 6` collapse explicitly by listing one subset's six orderings.

## Quiz seeds

1. **Misconception.** Choosing 3 features from 10: ordered or unordered? Distractors should include a correct permutation count offered for a combination question, which is a right answer to a different question.
2. **Mechanism.** Why is there a `k!` in the denominator? Options must include "because order does not matter" (vague but popular) and the precise "because each subset was counted once per ordering".

## Practice seed

**Stem.** A model has 12 candidate features. How many subsets of exactly 4? How many subsets in total? Which of those two numbers is the reason exhaustive feature selection is not done?
**Hint.** The second question is `0002`'s power set, not a new formula.
**Solution path.** The binomial coefficient for the first; `2^12` for the second; then the observation that the total, not the layer, is what explodes.
**`.p-check`.** The number of 4-subsets must be smaller than the total number of subsets, and the symmetry property says choosing 4 of 12 equals choosing 8 of 12. Check both before trusting the arithmetic.

## Code and dataset

`code/0008-counting-what-you-cannot-enumerate.py` with NumPy and `math`. Computes the binomial coefficient two ways, from factorials and by the multiplicative recurrence, asserts they agree, and shows the factorial route overflowing for large `n` where the recurrence survives. Then verifies that the row of coefficients sums to `2^n` for several `n`.

## Sources

- A primary source for the dropout `2^n` claim, quoted with its own wording.
- A primary source for the coalition attribution weight.
