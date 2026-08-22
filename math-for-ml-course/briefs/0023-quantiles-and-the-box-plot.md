# 0023 Quantiles, percentiles, the IQR and the box plot

| | |
|---|---|
| Module | M02 Data and summaries |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,000 to 1,200 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S02 |

## One tight idea

A quantile answers "what value is this fraction of the way through the sorted data", and it survives skew and outliers because it answers only to rank.

## Prerequisites

`0021` for the cumulative frequency curve, `0022` for the median, which is the 50th percentile under another name.

## Downstream

`0024` needs the five-number summary. M09's confidence intervals are read as quantiles. `production-systems-course` writes latency budgets in this vocabulary.

## Boundaries: what this page must not teach

- **No probability anywhere in M02.** Every quantity on this page is arithmetic on a column that already exists. There are no random variables, no expectation operator and no population parameters. M07 introduces the first and M08 the rest.
- Where a page wants to say "this estimates something", it says so in one sentence and forward-references M09 by module, never by number.
- **Not** the quantile function of a distribution. M07 owns that; this page is quantiles of a column you have.
- **Not** the several interpolation conventions in full. Name that they exist, show the one this course uses, and move on. A survey of nine methods is a reference-sheet job, not a lesson.

## Beats, in order

1. The median as the 50th percentile, which the reader already has from `0022`. Generalise it: sort, then step a fraction of the way along.
2. Quartiles Q1, Q2, Q3, and the interquartile range as a spread measure that answers only to rank.
3. The interpolation problem, honestly: when the fraction lands between two values, something must be chosen. State the convention this course uses and note in one line that libraries differ.
4. The five-number summary, and the box plot as its drawing.
5. The whisker rule and what a point beyond it does and does not mean. **It flags a value as far from the middle. It does not say the value is wrong**, and treating the two as the same is how real data gets deleted.
6. p95 and p99: the vocabulary a latency budget is written in, and why a mean latency is close to useless for one.
7. The trade-off in the same section: quantiles are robust and they are also blind to magnitude. Move the largest value ten times further out and the p95 barely stirs, which is a strength when it is contamination and a weakness when it is signal.

## Figures

- **Orientation**, `flowchart`: *the cumulative curve (`0021`) and the median (`0022`)* -> **THIS PAGE: any fraction of the way through, not just the half** -> *`0024` shape, M09 intervals* -> *(dotted) M02*.
- **`svg.chart`**, required: a box plot of `session_seconds` drawn directly above the histogram of the same column on a shared x-axis, so the reader sees which features of the shape the box keeps and which it discards.
- **`svg.chart`**: the cumulative curve with Q1, Q2 and Q3 read off it by three dotted construction lines.

## Worked example

Eleven sorted values, chosen so Q1 and Q3 land exactly on data points and the median is unambiguous. Compute the five-number summary and the IQR by hand. Then a twelve-value version where Q1 falls between two points, so the interpolation choice has to be made explicitly rather than hidden.

## Quiz seeds

1. **Misconception.** A point beyond the whisker is what? Distractors must include "an error to remove", which is the belief this page exists to break, and the feedback must say what the whisker rule actually asserts.
2. **Mechanism.** Why does a latency budget use p99 rather than the mean?

## Practice seed

**Stem.** Given eleven response times, give the five-number summary and the IQR. Then multiply the largest by 20 and report which of the five numbers changed.
**Hint.** Sort first. Every quantile is a position before it is a value.
**Solution path.** Sort, position, read; then observe only the maximum moves.
**`.p-check`.** Q1 <= Q2 <= Q3 always, and the IQR is never negative. If your Q1 exceeds your median, the sort was skipped.

## Code and dataset

`code/0023-quantiles-and-the-box-plot.py` against `datasets/sessions.csv`. Computes p50, p95 and p99 of `session_seconds` by explicit sort-and-index and by `numpy.percentile`, asserts agreement within the interpolation convention, and prints the mean beside p99 so the page can quote how far apart they are.

## Sources

- A primary source for the box plot and the whisker convention.
- A library's percentile documentation, for the interpolation methods.
