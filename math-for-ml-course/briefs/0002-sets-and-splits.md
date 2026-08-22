# 0002 - Sets, and why most data bugs are set bugs

| | |
|---|---|
| Module | M01 Foundations |
| Rung | foundation (`pill easy`) |
| Partition | core |
| Prose budget | 1,100 to 1,300 words |
| Prerequisites | `0001` (cardinality, and set-builder read as a filter) |
| Needed by | M07 (sample spaces and events are sets), M09 (the train/test partition), M10 (set similarity) |
| Code | `code/0002-sets-and-splits.py` |
| Dataset | `datasets/tickets.csv` |
| Named theorems | **De Morgan's laws** and **inclusion-exclusion for two sets**. Both proved (D4). |

## The one idea

A dataset is a set, a split is a partition, and leakage is a non-empty intersection.

## Beats, in order

1. What a set is: unordered, no duplicates. Contrast with a list using the ticket data: the **vocabulary** is a set, the **token stream** is not, and confusing them is a real bug.
2. Membership, subset, the empty set, and cardinality.
3. Set-builder notation read aloud as a filter: "the x in R^d such that ...".
4. Union, intersection, difference, complement, with one ML reading each, not four abstract diagrams.
5. Disjoint, and **partition**. Train/validation/test is a partition, and that one word carries the whole contract: covers everything, overlaps nothing.
6. **Inclusion-exclusion for two sets**, stated and proved. Then leakage is the partition failing: quote scikit-learn's definition, "information that would not be available at prediction time is used when building the model", and show the fit-scaler-before-split bug as a set statement.
7. **De Morgan's laws**, stated and proved, in the only form the reader needs: "not (A or B)" is "not A and not B". One example of a row filter negated wrongly.
8. Intersection over union as a pure set formula, using PASCAL VOC's actual detection criterion. The page's payoff: a headline vision metric is two set operations and a division.
9. Cartesian product, a hyperparameter grid as its first example, then the power set and `2^d` stated and handed forward to `0008`. Do not derive `2^d` here.

## The proofs (D4)

**Inclusion-exclusion for two finite sets.** `card(A union B) = card(A) + card(B) - card(A intersection B)`.
*Proof.* Every element of `A union B` lies in exactly one of three disjoint pieces: `A` only, `B` only, or both. Counting `card(A) + card(B)` counts the first piece once, the second once, and the third **twice**, because it belongs to `A` and to `B`. Subtracting `card(A intersection B)` removes exactly one of those two counts. **The step that does the work** is the observation that the three pieces are disjoint, which is what lets the counts be added at all.

**De Morgan's laws.** `complement(A union B) = complement(A) intersection complement(B)`, and `complement(A intersection B) = complement(A) union complement(B)`.
*Proof of the first, by double inclusion.* If `x` is in `complement(A union B)` then `x` is not in `A union B`, so `x` is in neither `A` nor `B`, so `x` is in `complement(A)` and in `complement(B)`. Every step reverses, which gives the other inclusion and hence equality. **The step that does the work** is "not in a union means in neither", which is the definition of union read backwards.

## Figures (4, at least one `svg.chart`)

- **F1 orientation, `flowchart LR`.** "You can read an index" to "THIS PAGE: a dataset is a set" to "splits, leakage, sample spaces (M07), similarity (M10)".
- **F2 inline `svg.chart`.** Two overlapping rectangles to scale: predicted box and ground-truth box, intersection filled `f-prob`, union outlined, with 11,200 and 19,800 and `IoU = 0.566` annotated and a `ref` line at the 0.5 threshold. Kills: "IoU is overlap over the ground-truth area".
- **F3 `flowchart TB`.** Tickets splitting into three disjoint blocks, plus a second edge showing a statistic fitted on all rows feeding the training block: the leakage path drawn as a path. Kills: that leakage means copying rows.
- **F4 inline `svg.chart`.** Two overlapping regions drawn four times in one figure, with union, intersection, difference and symmetric difference each shaded in turn and the cardinality of each written underneath. Kills: which operation is which, and it makes inclusion-exclusion visible: the two shaded areas overlap, so adding them double-counts the middle.

## Worked example (eight parts)

Predicted box `(50, 60, 150, 200)`, ground truth `(70, 50, 170, 220)`, in pixels.
Areas 14,000 and 17,000; overlap `80 x 140 = 11,200`; union `14,000 + 17,000 - 11,200 = 19,800`; **IoU 0.566**, which clears PASCAL VOC's stated 0.5 threshold.
The union line is inclusion-exclusion in its simplest form: you subtract the intersection because otherwise you counted it twice.

- **Sanity check.** IoU lies in `[0, 1]` by construction, and the boxes visibly overlap by more than half, so 0.57 is plausible and 0.9 is not.
- **What changes if** the predicted box shifts 30 px right: the intersection shrinks, the union grows, and IoU falls through 0.5 into a miss.

## Code

`code/0002-sets-and-splits.py`.
Against `tickets.csv`: builds the customer sets on each side of `row_split`, **verifies inclusion-exclusion numerically** (`card(A) + card(B) - card(A and B)` equals `card(A or B)`), **verifies both De Morgan laws** on the token vocabularies, and then audits the split, reporting how many test customers also appear in train.
Closes by computing IoU from the definition and asserting it matches a vectorised NumPy version.

## Quizzes

- **Q1** (misconception): the overlap of a predicted and a true box is 11,200 px squared. What do you divide by for IoU?
  `The area of the ground-truth box alone` / `The area of the predicted box alone` / `The area covered by either box` / `The sum of both boxes' areas`
  Feedback: option 1 gives a recall-like quantity and is the most common wrong version; option 2 a precision-like one; option 4 double-counts the overlap, and subtracting it once is exactly what makes it a union.
- **Q2** (misconception): a statistic is fitted on all rows, then the rows are split. The row sets are still disjoint. What went wrong?
  `Nothing, since the row sets are disjoint` / `A statistic crossed the partition line` / `The test set became a training subset` / `The split ratio is now miscalculated`
  Feedback: option 1 is the misconception, since leakage is about information and not rows; option 3 is false, the rows never moved; option 4 is unaffected.

## Practice

(a) Predicted box `(0, 0, 100, 100)`, ground truth `(50, 50, 150, 150)`. Compute IoU and say whether VOC counts it as a detection.
(b) `tickets.csv` is split by **row**. The row sets are disjoint. Why is an evaluation on it still optimistic, and what is the fix?

- **Hint.** For (b), ask what unit the model could memorise instead of the label, then ask whether the split separated that unit.
- **Solution.** (a) intersection `50 x 50 = 2,500`; each box 10,000; union `10,000 + 10,000 - 2,500 = 17,500`; IoU `= 0.143`, below 0.5, so a miss. (b) the partition is correct at the level of tickets and wrong at the level of customers: the same customer appears on both sides, so the model can recognise the customer rather than the urgency. As sets, `train intersection test` is empty in tickets and very much non-empty in customers. The fix is to partition by the leakage unit, which is the customer.
- **`.p-check`.** IoU must lie in `[0, 1]`; and in (b), if your answer does not name a unit other than the row, it has not found the bug.

## Primary sources to go deeper

scikit-learn, Common pitfalls and recommended practices, section on data leakage, `https://scikit-learn.org/stable/common_pitfalls.html`.
Everingham et al., *The PASCAL Visual Object Classes (VOC) Challenge*, IJCV 2010, equation 3.
