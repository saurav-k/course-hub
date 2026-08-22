# 0002 Sets, and why most data bugs are set bugs

| | |
|---|---|
| Module | M01 Foundations |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,100 to 1,300 prose words, excluding practice and quiz text |
| Source scout | `mlm-foundations-r2` L2 |

## One tight idea

A dataset is a set, a split is a partition, and leakage is a non-empty intersection.

## Prerequisites

`0001` for set-builder notation read as a filter, and for cardinality.

## Downstream

M07 needs sample spaces and events, which are sets. M09 needs the train/test partition, for cross-validation. M10 needs set-style similarity.

## Boundaries: what this page must not teach

- **Not** the geometry of `{x : ||x|| <= 1}`. M03 owns norm balls; this page owns only the notation that describes one.
- **Not** probability. A sample space is a set and M07 owns everything that follows from that.
- **Not** counting. `2^d` is stated here and derived in `0008`.

## Beats, in order

1. What a set is: unordered, no duplicates. Contrast with a list using a tokenizer, where the **vocabulary** is a set and the **token stream** is not, and confusing them is a real bug.
2. Membership, subset, the empty set, and cardinality.
3. Set-builder notation read aloud as a filter: "the x in R^d such that ...".
4. Union, intersection, difference, complement, with one machine learning reading each rather than four abstract Venn diagrams.
5. Disjoint, and **partition**. Train, validation and test is a partition, and that one word carries the whole contract: covers everything, overlaps nothing.
6. Leakage is the partition failing. Show the fit-the-scaler-before-the-split bug written as a set statement.
7. Intersection over union as a pure set formula. The payoff: a headline computer-vision metric is two set operations and a division.
8. De Morgan, in the only form the reader needs, with one example of a row filter negated wrongly.
9. Inclusion-exclusion for two sets, which is the union line of the IoU just computed. Name it, because `0008` uses the idea again.
10. Cartesian product, with a hyperparameter grid as its first example.
11. Power set and `2^d`, stated and handed forward to `0008`. Do not derive it here.

## Stated proof (D4)

One named result: **inclusion-exclusion for two sets**. It is one line and it must be argued rather than asserted: every element of the union is counted once by `|A| + |B|` unless it lies in both, in which case it is counted twice, so subtracting `|A and B|` corrects exactly the double-counted elements. Name the step that does the work: the case split on whether an element is in the intersection.

## Figures

- **Orientation**, `flowchart`: *a dataset is a pile of rows* -> **THIS PAGE: it is a set, and a split is a partition** -> *leakage becomes a thing you can check* -> *(dotted) M01*.
- **`svg.chart`**, required: two overlapping regions drawn to scale for a real IoU, with the intersection and union areas labelled with their actual values, so the metric is a picture before it is a formula.
- **`flowchart`**: the train/validation/test partition, with a red edge showing the one arrow that must not exist.

## Worked example

A predicted box and a ground-truth box with integer corners chosen so the intersection and union are whole numbers. Compute IoU by hand, then show the union computed the wrong way (adding the two areas) and how much the metric inflates.

## Quiz seeds

1. **Misconception.** A reader scales features before splitting. What has gone wrong, stated as a set fact? Distractors include "nothing, scaling is deterministic" (true of the function, wrong about the information) and "the test set is too small".
2. **Mechanism.** Which of four operations makes a train/test division a partition rather than merely two sets?

## Practice seed

**Stem.** Given two boxes with named corners, compute IoU. Then a second pair whose union you must get from inclusion-exclusion rather than by counting.
**Hint.** The union is not the sum of the two areas.
**Solution path.** Intersection by overlap on each axis, then union by inclusion-exclusion, then the ratio.
**`.p-check`.** IoU is always between 0 and 1. A value above 1 means the union was computed as a sum.

## Code and dataset

`code/0002-sets-and-splits.py` against `datasets/sessions.csv`. Splits `session_id` into train and test with a seed, then asserts three set facts: the two are disjoint, their union is the whole, and a deliberately leaked split fails the same assertion. The assertion failing is the teaching.

## Sources

- scikit-learn's own definition of data leakage, quoted and linked.
- The PASCAL VOC detection criterion for the IoU threshold.
