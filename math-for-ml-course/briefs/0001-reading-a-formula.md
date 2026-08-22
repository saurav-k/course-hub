# 0001 Reading a formula: indices, sigma, and pi

| | |
|---|---|
| Module | M01 Foundations |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,000 to 1,200 prose words, excluding practice and quiz text |
| Source scout | `mlm-foundations-r2` L1 |

## One tight idea

Every formula in a machine learning paper is a loop with an accumulator, and the index tells you what it loops over.

## Prerequisites

**None.** This is the first content page after lesson zero (`0000`). It may assume the reader can program and nothing else.

## Downstream

Everything. M02 needs index notation for a column, M03 needs it for the data matrix, M07 needs the sum for expectations, M10 needs the product for likelihoods.

## Boundaries: what this page must not teach

- **Not** what a variable is. The reader programs for a living.
- **Not** matrix notation. M03 owns that; this page stays with scalars and one index.
- **Not** the derivative, even though the gradient formula in beat 7 contains one. Name it as "the thing M05 builds" and move on.

## Beats, in order

1. Name the reader's real problem in one paragraph: the difficulty is not the mathematics, it is that the notation compresses a loop into three characters and nobody says so out loud.
2. A variable, an index, and the two places an index can sit. `x^(i)` in parenthesised superscript is the **i-th example**; `x_j` in subscript is the **j-th feature**. This is the field's own convention, not a house one.
3. Sigma as a for-loop with a running total. Give the three parts explicitly: where the index starts, where it stops, what is accumulated.
4. The index is a **bound** variable, so summing over `i` and summing over `k` give the same number. This is the single fact that unlocks reading an unfamiliar paper.
5. Pi is the same loop with a running product. State the empty sum as 0 and the empty product as 1 here; both are load-bearing later.
6. Double sums as nested loops, and the trap: in a double sum the two indices are independent, and a reader who ties them together computes a trace instead of a full sum.
7. Read one real formula end to end, naming every symbol in words before using it.
8. Close on the habit: when a formula stops you, write down what the index ranges over before anything else.

## Figures

- **Orientation**, `flowchart`, 4 nodes: *you can already write a loop* -> **THIS PAGE: the same loop, written in three characters** -> *every formula in the course* -> *(dotted) M01 Foundations*.
- **`svg.chart`**, required: the same accumulation drawn twice side by side, a for-loop's running total as a step plot against the sigma that denotes it, so the reader sees one object and two notations.
- **`flowchart`**: the anatomy of a sum, with the start, the stop and the body called out as three labelled parts.

## Worked example

Ten daily spend values from `sessions.csv`, taken as the first ten rows so the reader can check them against the file. Write the mean twice: once as a sentence, once as the sigma formula, and show they are the same arithmetic. Then rename the index and show the number does not move.

## Quiz seeds

1. **Misconception.** `Sum_{i=1}^{n} a_i` against `Sum_{k=1}^{n} a_k`: same number, or different? Distractors should include "different, because the index letter changes which values are picked up", which is a true-sounding statement about a different thing (a *free* variable).
2. **Mechanism.** In a double sum over `i` and `j`, what does tying the indices together compute instead? One option is the correct full sum, one is the trace, one is a row sum, one is a column sum.

## Practice seed

**Stem.** Given a five-row table of `pages_viewed`, write the total as a sum, then write the mean, then rewrite both with the index renamed.
**Hint.** Start by writing the loop in Python, then translate it one part at a time.
**Solution path.** The three parts of the sigma, filled in from the loop; the division by `n`; the rename, showing the number is unchanged.
**`.p-check`.** The mean must land between the smallest and largest value in the column. If it does not, the sum is wrong, not the division.

## Code and dataset

`code/0001-reading-a-formula.py` against `datasets/sessions.csv`. Computes a column mean twice: once with an explicit Python loop and an accumulator, once with `frame['spend'].mean()`, and asserts they agree. The point is that the reader watches the sigma and the loop produce the same float.

## Sources

- Goodfellow, Bengio and Courville, *Deep Learning*, the notation table, for `x^(i)` against `x_j`.
- Any source used for the real formula in beat 7 must be fetched and linked on the page.

## As built

Written by `mlm-foundations-r2` alongside this brief; where the shipped page departs from the plan above, this is what it does and why.

The worked example uses **`tickets.csv`**, not `sessions.csv`: M01 has its own dataset, and the reason it exists is recorded in `datasets/README.md`.
The required `svg.chart` became **two**: the data matrix drawn as a grid with one row and one column shaded, which is what kills the superscript-against-subscript error, and a second showing a double sum's every cell against a single sum's diagonal. The accumulation is unrolled as a `sequenceDiagram` instead of a step plot, because the confusion it kills is about *order*, not magnitude.
Five figures rather than three. The page names no theorem and says so in the teacher note.
