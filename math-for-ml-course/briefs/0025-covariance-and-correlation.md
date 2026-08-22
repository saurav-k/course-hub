# 0025 Covariance and correlation, and why the units do not matter

| | |
|---|---|
| Module | M02 Data and summaries |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,200 to 1,400 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S13 |

## One tight idea

Covariance measures whether two columns move together in their own units, and dividing by both spreads removes the units and leaves a number between -1 and 1.

## Prerequisites

`0022` for the mean and standard deviation, `0024` for shape.

## Downstream

M04's covariance matrix and PCA. M08's population covariance. `0026` is this page's warning label and must be read with it.

## Boundaries: what this page must not teach

- **No probability anywhere in M02.** Every quantity on this page is arithmetic on a column that already exists. There are no random variables, no expectation operator and no population parameters. M07 introduces the first and M08 the rest.
- Where a page wants to say "this estimates something", it says so in one sentence and forward-references M09 by module, never by number.
- **Not** the covariance **matrix**. M04 owns it as a linear-algebra object and M08 as a statistical one. This page is two columns and one number.
- **Not** causation. `0026` owns it, and this page must **end** by pointing there rather than hedging in the middle.
- **Not** Spearman or Kendall in full. Name that rank correlations exist and what they buy, in two sentences.

## Beats, in order

1. Two columns and one question: when one is above its mean, is the other? Build the product-of-deviations table before naming anything.
2. Covariance as the average of that product. Positive, negative and near-zero, one picture each.
3. The problem with covariance: it carries the units of both columns multiplied together, so its magnitude is uninterpretable and changing from seconds to minutes changes it.
4. The fix: divide by both standard deviations. The units cancel, and this is the whole derivation of the correlation coefficient rather than a definition to memorise.
5. The range is -1 to 1, and what each end means geometrically: all the points on one straight line.
6. **Correlation measures linear association only.** Show a strong non-linear relationship with a correlation near zero, so the word "linear" is a fact the reader has seen rather than a caveat they read past.
7. Rank correlation in two sentences: replace values with ranks and the same formula measures monotone association instead, which is what `0004`'s monotonicity buys here.
8. Close by handing straight to `0026`: this number says nothing about direction or cause, and the next page is why.

## Stated proof (D4)

**Correlation is unit-free.** Required by D4, and it is the page's central claim rather than an aside.

Rescale a column by a positive constant `a`. Every deviation scales by `a`, so the covariance scales by `a`, and that column's standard deviation also scales by `a`. In the ratio the two factors of `a` cancel, so the correlation is unchanged.

**The step that does the work** is that the deviation, not the value, is what enters both the numerator and the denominator. **State the boundary**: the constant must be positive, because a negative one flips the sign of the covariance and therefore of the correlation, which is correct behaviour rather than a failure of the argument.

## Figures

- **Orientation**, `flowchart`: *one column at a time (`0022`, `0024`)* -> **THIS PAGE: two columns, and whether they move together** -> *`0026`'s warning, M04's covariance matrix* -> *(dotted) M02*.
- **`svg.chart`**, required: two scatter plots side by side in one `<figure>`, `session_seconds` against `spend` at r = 0.487 and `screen_brightness` against `spend` at r = 0.002, both drawn from `sessions.csv`. A real association and a genuine null, on the same data, at the same scale.
- **`svg.chart`**: a diverging scale from -1 to +1 with both values marked, plus a third marker for a strong non-linear relationship whose correlation is near zero.

## Worked example

Six paired values. Build the deviation table for both columns, then the product column, then the covariance, then divide by the two standard deviations. Then convert one column from seconds to minutes and recompute both: the covariance changes by exactly 60 and the correlation does not move at all.

## Quiz seeds

1. **Misconception.** A correlation of 0 means the two columns are unrelated. Distractors must include "yes, zero covariance means independent", which is a true statement about a different (and stronger) property, with feedback naming the non-linear counterexample.
2. **Mechanism.** Converting a column from seconds to minutes: which of covariance, correlation, both or neither changes?

## Practice seed

**Stem.** Six paired readings. Compute the covariance and the correlation. Then rescale one column by 100 and report both again.
**Hint.** Build the two deviation columns first; every quantity on this page is made from them.
**Solution path.** Deviations, products, covariance; the two standard deviations; the ratio; then the rescale and the cancellation.
**`.p-check`.** The correlation must lie in [-1, 1] and must be unchanged by the rescale. If it moved, a standard deviation was not rescaled alongside the covariance.

## Code and dataset

`code/0025-covariance-and-correlation.py` against `datasets/sessions.csv`. Computes the correlation from the definition with explicit deviation sums and again with `numpy.corrcoef`, asserts they agree, then rescales a column and asserts the correlation is bit-for-bit unchanged while the covariance is not. Prints the r = 0.487 and r = 0.002 the page quotes.

## Sources

- A primary source for Pearson's correlation coefficient and its bounds.
