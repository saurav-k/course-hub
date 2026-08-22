# 0021 Seeing one column: frequency tables, class intervals and histograms

| | |
|---|---|
| Module | M02 Data and summaries |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,000 to 1,200 prose words, excluding practice and quiz text |
| Source scout | `mlm-sfml-notes-r11` gap 2 |

## One tight idea

A histogram is a frequency table with a choice of bin width baked into it, and that choice can change what you conclude.

## Prerequisites

`0020` for the scale, since a histogram of a nominal column is a bar chart and the difference matters.

## Downstream

`0022` and `0024`: every claim about centre, spread and shape is read off this picture first.

## Boundaries: what this page must not teach

- **No probability anywhere in M02.** Every quantity on this page is arithmetic on a column that already exists. There are no random variables, no expectation operator and no population parameters. M07 introduces the first and M08 the rest, and M02 sits before both on purpose so that a reader meets a histogram long before they meet the Central Limit Theorem.
- Where a page wants to say "this estimates something", it says so in one sentence and forward-references M09 by module, never by number.
- **Not** density estimation. Kernel density is a different tool and belongs nowhere in this course.
- **Not** the probability density function. M07 owns that, and this page must not blur a count into a density.

## Beats, in order

1. A frequency table for a column with few distinct values, built by hand.
2. Relative frequency, and why it is what lets two differently sized samples be compared.
3. Class intervals: what to do when there are too many distinct values to tabulate. Equal width, and the boundary convention, which must be stated because half-open intervals are the source of every off-by-one in a bin count.
4. The histogram as that table drawn. Area, not height, is the quantity, which is why unequal bins mislead.
5. **Bin width changes the story.** Show the same column at three widths: one that hides the second mode, one that shows it, one that is pure noise. This is the page's whole reason to exist.
6. Cumulative frequency, and reading a quantile straight off it. This is the bridge to `0023`.
7. The bar chart against the histogram: gaps between bars mean categories, touching bars mean a continuous axis, and a chart that gets this wrong lies about the data's type.
8. Close on the habit: plot the column before summarising it, every time.

## Figures

- **Orientation**, `flowchart`: *a column and its scale (`0020`)* -> **THIS PAGE: see the whole column before summarising it** -> *`0022` centre and spread, `0024` shape* -> *(dotted) M02*.
- **`svg.chart`**, required: `session_seconds` at three bin widths, small multiples in one `<figure>`, with the same underlying data. The lognormal shape means a wide bin genuinely hides structure a narrow one shows.
- **`svg.chart`**: the cumulative frequency curve for the same column, with the median read off it by a dotted construction line.

## Worked example

Twenty values by hand into five equal-width classes. Build the frequency table, the relative frequency column, and the cumulative column, then read the median off the cumulative column and check it against the sorted list.

## Quiz seeds

1. **Misconception.** What does a histogram's bar height represent when bins are unequal? Distractors must include "the count in that bin", which is true for equal bins and is exactly the belief that misleads on unequal ones.
2. **Mechanism.** Bars touching against bars separated: what does the difference say about the column?

## Practice seed

**Stem.** Given a 20-value column, build a frequency table with 4 classes and then with 8, and say which conclusion changes.
**Hint.** Look for whether a second cluster appears or disappears.
**Solution path.** Two tables, two sketches, then a sentence naming the structure that only one width reveals.
**`.p-check`.** The relative frequencies must sum to 1 and the final cumulative frequency must equal the row count. If either fails, a boundary value went into two bins or none.

## Code and dataset

`code/0021-frequency-tables-and-histograms.py` against `datasets/sessions.csv`. Bins `session_seconds` two ways, once with an explicit loop over boundaries and once with `pandas.cut`, and asserts the counts agree. Then prints the counts at three bin widths so the page can quote them.

## Sources

- A primary source for the histogram's area-not-height convention.
