# 0024 Shape is the part the summary throws away

| | |
|---|---|
| Module | M02 Data and summaries |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,200 to 1,400 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S02 |

## One tight idea

Two datasets can agree on every number so far and still be nothing alike, so shape needs a vocabulary of its own.

## Prerequisites

`0022` for mean and variance, `0023` for quantiles, `0004` for reading a curve's shape.

## Downstream

M07's named distributions are shapes before they are formulas. M08's Central Limit Theorem is a statement about a shape appearing.

## Boundaries: what this page must not teach

- **No probability anywhere in M02.** Every quantity on this page is arithmetic on a column that already exists. There are no random variables, no expectation operator and no population parameters. M07 introduces the first and M08 the rest.
- Where a page wants to say "this estimates something", it says so in one sentence and forward-references M09 by module, never by number.
- **Not** any named distribution. "Normal" may be used as an adjective for a shape; **M07 owns the Normal distribution** and this page must not define it.
- **Not** Chebyshev's proof. The bound may be **quoted with its numbers** to contrast with the empirical rule; **M08 owns the statement and the proof**.
- **Not** correlation. `0025` owns it.

## Beats, in order

1. Open with four datasets that share their mean, variance and correlation and look nothing alike. This is the page's thesis delivered before any vocabulary.
2. Skewness in words first: which tail is longer. Then the standardised third moment, with the sign convention stated because it is the half people get backwards.
3. Right-skew as the default in the wild: latencies, incomes, session lengths. Tie it back to the mean-median gap `0022` already showed.
4. Kurtosis, **defined as tail extremity and explicitly not as peakedness**. This misconception needs a `.callout.warn` of its own, because the word is taught wrongly in a great many places.
5. Excess kurtosis and why the 3 is subtracted, so a Normal-shaped column reads zero.
6. Modality: unimodal, bimodal, and why a bimodal column usually means two populations were mixed and should not have been.
7. The trade-off, in the same section: a bound that holds for every shape is loose, and a rule that is tight needs an assumption. Show both at k = 2 on the same data, at least 75 per cent against about 95 per cent, and name what the second one is assuming.
8. Close on the habit: every summary in `0022` and `0023` is a lossy compression, and the shape is the part that was lost.

## Figures

- **Orientation**, `flowchart`: *centre and spread (`0022`, `0023`)* -> **THIS PAGE: what those numbers threw away** -> *M07's distributions, M08's CLT* -> *(dotted) M02*.
- **`svg.chart`**, required: four scatter plots in a 2x2 grid inside one `<figure>`, identical summary statistics, one regression line drawn identically across all four. One figure, the whole page.
- **`svg.chart`**: three densities on one axis, left-skewed, symmetric and right-skewed, with mean and median marked on each so the reader can read skew off the gap between them.

## Worked example

Two eight-value columns constructed to share a mean and a standard deviation exactly, one symmetric and one right-skewed. Compute both summaries to show they match, then compute the skewness of each and plot both, so the reader watches identical numbers describe different data.

## Quiz seeds

1. **Misconception.** High kurtosis means what? Distractors must include "a sharper peak", which is the textbook-wrong answer this page exists to correct, with feedback naming tail extremity as the real definition.
2. **Mechanism.** Mean well above median: which way is the column skewed?

## Practice seed

**Stem.** Two columns with identical mean and standard deviation are given. Compute the skewness of each and say which you would model with a symmetric assumption.
**Hint.** Compute the mean-median gap first; it tells you the sign before any third moment does.
**Solution path.** The gap, then the standardised third moment, then the modelling call.
**`.p-check`.** A right-skewed column has mean above median and positive skewness. If your two signals disagree, one of the two calculations is wrong.

## Code and dataset

`code/0024-shape-is-what-the-summary-throws-away.py` against `datasets/sessions.csv`. Computes skewness and excess kurtosis from their definitions with explicit moment sums and again with `pandas`, and asserts agreement. Then reports the mean, median and skewness of `session_seconds` so the page quotes real numbers rather than invented ones.

## Sources

- A primary source defining kurtosis as tail behaviour, quoted, since correcting the misconception requires the authority.
- Anscombe's 1973 paper for the four datasets.
