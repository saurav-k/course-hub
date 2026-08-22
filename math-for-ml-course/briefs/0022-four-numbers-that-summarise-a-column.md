# 0022 Four numbers that summarise a column, and when each one lies

| | |
|---|---|
| Module | M02 Data and summaries |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,100 to 1,300 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S01 |

## One tight idea

The centre and the spread are two separate questions, and the right answer to each depends on the shape of the data rather than on habit.

## Prerequisites

`0020` for which summaries are legal, `0021` for the picture, `0001` for summation notation.

## Downstream

`0023`, `0024`, `0025`, and every page in M09.

## Boundaries: what this page must not teach

- **No probability anywhere in M02.** Every quantity on this page is arithmetic on a column that already exists. There are no random variables, no expectation operator and no population parameters. M07 introduces the first and M08 the rest, and M02 sits before both on purpose so that a reader meets a histogram long before they meet the Central Limit Theorem.
- Where a page wants to say "this estimates something", it says so in one sentence and forward-references M09 by module, never by number.
- **Not** the word *unbiased*. The `n-1` is explained here as "one number was already spent estimating the mean"; **M09 owns the word and the proof**, and this page forward-references it in one line.
- **Not** quantiles or skew. `0023` and `0024` own them.

## Beats, in order

1. Mean, median and mode defined in words and then in symbols, using `0001`'s sigma so the notation is a re-reading rather than a new thing.
2. Deviations from the mean sum to zero. Show it on five numbers, and use it to motivate why a spread measure must square or take absolute values rather than just average the deviations.
3. Sample variance and standard deviation. The standard deviation is in the column's own units and the variance is not, which is why one goes on a chart and the other goes in an algebra step.
4. The `n-1`: state it as "the correction exists because one number was already spent estimating the mean", show the arithmetic difference on a small `n`, and forward-reference M09 for the word and the proof.
5. The trade-off, in the same section as the technique: the mean uses every value and therefore answers to every value; the median answers only to rank. One outlier moves one and not the other.
6. Which to reach for, as a decision rather than a rule: symmetric and clean, use the mean; skewed or contaminated, use the median; and always look at the picture from `0021` first.
7. The `ddof` trap: one library defaults to the population divisor and another to the sample divisor, so the same column gives two different standard deviations depending on which you called.

## Stated proof (D4)

**Deviations from the mean sum to zero.** Two lines, and it is what motivates squaring, so proving it is cheaper than asserting it.

The sum of `(x_i - xbar)` splits into `Sum x_i - n xbar`. By the definition of the mean, `Sum x_i = n xbar`, so the difference is zero. **The step that does the work** is substituting the definition of the mean into its own deviation sum, and it is worth naming because the result then looks inevitable rather than surprising.

Do **not** prove the `n-1` correction here. That needs the expectation operator and belongs to M09; say so in one line.

## Figures

- **Orientation**, `flowchart`: *a column you have looked at (`0021`)* -> **THIS PAGE: two questions, where is it and how spread out** -> *`0023` quantiles, `0025` two columns at once* -> *(dotted) M02*.
- **`svg.chart`**, required: `session_seconds` with mean and median both marked. The lognormal shape puts them at 171.7 and 98.9, so the gap is large and visible, and the figure argues the page's thesis without a word.
- **`svg.chart`**: the balance-beam picture, blocks on a plank with the fulcrum at the mean, showing one far-out value moving the balance point while the middle value stays put.

## Worked example

Ten values from `sessions.csv`. Compute mean, median, variance and standard deviation by hand, showing the deviation column and its zero sum. Then replace the largest value with one ten times bigger and recompute all four, tabulating which moved and by how much.

## Quiz seeds

1. **Misconception.** Why divide by `n-1` rather than `n`? Distractors should include "because the sample is smaller than the population", a true-sounding statement that explains nothing.
2. **Mechanism.** One value in a 1,000-row column is multiplied by 100. Which of mean, median, variance, mode moves most?

## Practice seed

**Stem.** Ten values given. Compute all four summaries. Then add one outlier and recompute, and say which summary you would report to a stakeholder and why.
**Hint.** Compute the deviation column first; it is needed for the variance and it checks the mean.
**Solution path.** Mean, then deviations (which must sum to zero), then squared deviations over `n-1`, then the root; median by sorting.
**`.p-check`.** Your deviations must sum to zero and your standard deviation must be smaller than the range. If the deviations do not sum to zero, the mean is wrong and everything after it is too.

## Code and dataset

`code/0022-four-numbers-that-summarise-a-column.py` against `datasets/sessions.csv`. Computes variance from the definition with an explicit loop and with `numpy.var(ddof=1)`, asserts they agree, and then prints `numpy.var` at both `ddof` settings side by side so the trap is a number rather than a warning.

## Sources

- A primary source for the definitions of mean, median, variance and standard deviation.
- The two library documentation pages whose `ddof` defaults differ, both linked.
