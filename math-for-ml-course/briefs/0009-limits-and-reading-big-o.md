# 0009 Sequences, limits, and how to read a Big-O claim

| | |
|---|---|
| Module | M01 Foundations |
| Rung | `pill easy` |
| Class | depth |
| Word budget | 1,200 to 1,400 prose words, excluding practice and quiz text |
| Source scout | `mlm-foundations-r2` L9 |

## One tight idea

A limit says where a sequence is heading and an asymptotic bound says how fast a cost grows, and neither is a statement about any particular n.

## Prerequisites

`0006` for the growth ladder, `0008` for factorials.

## Downstream

M05 owns the derivative as a limit and needs this intuition. M08 owns convergence in probability, the law of large numbers and the Central Limit Theorem.

## Boundaries: what this page must not teach

- **Not** the derivative. M05 owns it; this page owns only the idea of approaching.
- **Not** convergence in probability. M08 owns it, and this page must say explicitly that a sequence of numbers and a sequence of random variables converge in different senses, then stop.
- **Not** epsilon-delta. This is a foundation page for an engineer, not an analysis course.
- **The only `depth` page in M01.** A reader can skip it and still read the rest of the course; everything else in M01 is consumed by a later module.

## Beats, in order

1. A sequence as a function on the positive integers, which is the definition that makes the rest easy.
2. A limit in words: the sequence gets and stays arbitrarily close. Emphasise **stays**, because that is the half that rules out oscillation.
3. Three sequences: one convergent, one divergent, one oscillating. One picture each, no formalism.
4. The two limits the reader will meet everywhere, stated and not derived: a decaying learning rate going to zero, and a standard error going to zero like one over the square root of n. Hand the second to M08.
5. Big-O as a statement about growth **rate**, not about time. Say plainly that it deliberately discards constants, and that this is why the asymptotically better algorithm can be slower at every size you actually run.
6. The growth ladder, read off the chart: constant, logarithmic, linear, linearithmic, quadratic, exponential, factorial.
7. An asymptotic bound never settles a race alone, because **which variable is growing** decides the winner. Compare two costs that cross, and give the crossing point.
8. The reading habit: when you meet a complexity claim, ask what is growing and what is being held fixed.

## Figures

- **Orientation**, `flowchart`: *logs and factorials (`0006`, `0008`)* -> **THIS PAGE: where a sequence heads, and how fast a cost grows** -> *M05's derivative, M08's law of large numbers* -> *(dotted) M01*.
- **`svg.chart`**, required: the growth ladder, seven curves on one log-y axis, with the crossing points between the two closest pairs marked. This is the page's reference figure and readers will come back to it.
- **`svg.chart`**: two real costs that cross, plotted against the variable that is growing, with the crossover annotated with its actual value. This is the figure that makes beat 7 land rather than be asserted.

## Worked example

Two costs of the form `a n^2 d` and `b n d^2`. Set them equal, solve for the crossing, and put in real numbers so the reader gets a specific size at which the answer flips. Then change one constant and show the crossing move, which is the whole point about discarded constants.

## Quiz seeds

1. **Misconception.** An `O(n log n)` algorithm always beats an `O(n^2)` one. Distractors should include "true for large enough n", which is the correct statement and therefore the strongest wrong answer to "always" - the feedback must say precisely why the qualifier matters.
2. **Mechanism.** In a two-variable cost, what decides which term dominates?

## Practice seed

**Stem.** Given two costs and their constants, find the size at which they cross. Then say which you would ship for inputs an order of magnitude below that.
**Hint.** Set the two expressions equal and solve. The constants do not cancel, and that is the point.
**Solution path.** Equate, solve, substitute, then read the inequality on either side of the crossing.
**`.p-check`.** Below the crossing the asymptotically worse algorithm must win, and above it the better one. If your inequality points the same way on both sides, the algebra flipped a sign.

## Code and dataset

`code/0009-limits-and-reading-big-o.py` with NumPy. Times nothing; it evaluates both cost expressions across a range of sizes and reports the crossing found numerically, then compares it with the crossing solved algebraically and asserts they agree. Timing would make the page about one machine, and the point is the shape.

## Sources

- Knuth on the one-way meaning of the equals sign in an asymptotic statement, quoted.
- A named source for the two costs compared in the worked example.

## As built

Written by `mlm-foundations-r2` alongside this brief; where the shipped page departs from the plan above, this is what it does and why.

The p-series test is proved by grouping, with an explicit honest boundary: that is the engineering proof for the two cases the course needs, and the general statement needs the integral test from M05.
`O`, `Omega` and `Theta` are drawn as **nested sets of functions** so that Knuth's one-way equality reads as set inclusion, which pays `0002` back. The attention-against-recurrence crossover is drawn at `n = d = 512` and the page states plainly that a complexity class alone is never a verdict.
