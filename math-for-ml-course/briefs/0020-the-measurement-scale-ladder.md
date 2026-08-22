# 0020 The measurement-scale ladder, and which summaries a column allows

| | |
|---|---|
| Module | M02 Data and summaries |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,000 to 1,200 prose words, excluding practice and quiz text |
| Source scout | `mlm-sfml-notes-r11` gap 3 |
| Dataset | **`population.csv`**, not `sessions.csv`. See the dataset note below. |

## One tight idea

A column's measurement scale decides which summaries are meaningful on it, and the test is not a rule to memorise: **apply the transformation that scale allows, and see whether your conclusion survives.**

## Prerequisites

`0002` for sets, `0003` for functions.

## Downstream

Everything else in M02: the scale decides whether a mean, a median or only a mode is legal. M09's test-selection page rests on it.

## Boundaries: what this page must not teach

- **No probability anywhere in M02.** Every quantity on this page is arithmetic on a column that already exists. There are no random variables, no expectation operator and no population parameters. M07 introduces the first and M08 the rest, and M02 sits before both on purpose so that a reader meets a histogram long before they meet the Central Limit Theorem.
- Where a page wants to say "this estimates something", it says so in one sentence and forward-references M09 by module, never by number.
- **Not** feature encoding. One-hot and ordinal encoding are ML techniques; this page owns only the property of the column that makes an encoding right or wrong.
- **Not** the tests themselves. Name which family each scale admits and hand every test to M09.

## Beats, in order

1. Open on the failure: the mean of a region code, the mean of a five-point satisfaction score. Both compute. Neither means anything, and nothing in the tooling will tell you.
2. **The test, stated once and used four times.** Each rung is defined by the transformations that leave its meaning intact. Apply one of those transformations and see whether your conclusion moves. If it moves, the statistic was never meaningful on that scale. Everything below is that one test, run four times.
3. Nominal: labels only, meaningful under **any one-to-one relabelling**. Legal summaries are the mode and a frequency count. Relabel `region` two ways and watch the "mean region" give two different answers while the mode does not move.
4. Ordinal: ordered labels, meaningful under **any order-preserving transformation**. The median becomes legal. Respace `satisfaction`'s top category from 5 to 10, which preserves the order, and watch the median hold while the mean moves a long way. **Reporting a mean rating is a choice to assume interval spacing, and it should be a stated choice rather than a habit.**
5. Interval: differences are meaningful, the zero is a convention, meaningful under `x -> a.x + b` with positive `a`. Convert `office_temp_c` to Fahrenheit: the mean converts correctly, a difference converts correctly, and **a ratio does not**. Two legitimate conversions give two different ratios, so the ratio was meaningless.
6. Ratio: a true zero, meaningful only under `x -> a.x`. Convert `spend` from pounds to pence and the ratio is bit-for-bit identical, because the scale factor cancels. "The tail is 14.5 times the median" is a sentence that means something.
7. The ladder as a table: for each rung, the transformations it allows, what is legal, and what is not.
8. Where this bites: a model given an ordinal column as if it were ratio has been told a false fact about the spacing, and it will use it.
9. Close on the reading habit: before summarising a column, name its scale. It takes two seconds and it is the cheapest bug prevention in the module.

## Figures

- **Orientation**, `flowchart`: *a set of values (`0002`)* -> **THIS PAGE: which scale, and therefore which summaries survive** -> *every later page in M02* -> *(dotted) M02*.
- **`svg.chart`**, required: `satisfaction` before and after the respacing, with median and mean marked on both. The median sits on the same tick twice; the mean walks from 3.58 to 4.68. One figure, the whole ordinal argument.
- **`svg.chart`**: the interval failure. `office_temp_c`'s p01 and p99 drawn on a Celsius axis and a Fahrenheit axis, with the two ratios (1.49 and 1.24) annotated, so the reader sees one quantity give two answers.
- **`flowchart`**: the four-rung ladder as a decision tree, each rung labelled with the transformation it allows rather than with the statistics it permits, because the transformation is what generates the rest.

## Worked example

One column per rung from `population.csv`, and the same test applied to each by hand on a small slice: `region` (nominal), `satisfaction` (ordinal), `office_temp_c` (interval), `spend` (ratio).

For each, compute the summary, apply the transformation the rung allows, and recompute. Tabulate what moved. The point lands when the reader sees a number compute successfully, survive nothing, and still be marked invalid.

Numbers the page quotes, all produced by the program: mean region 2.0881 under one encoding and 1.9119 under another; satisfaction median 4.0 both times while the mean goes 3.5782 to 4.6847; the temperature ratio 1.4941 in Celsius against 1.2405 in Fahrenheit; the spend ratio 14.4574 in pounds and 14.4574 in pence.

## Quiz seeds

1. **Misconception.** Is a five-point satisfaction score interval or ordinal? Distractors must include "interval, because the numbers are evenly spaced", which is true of the *encoding* and false of the *scale*, and the feedback must say exactly that.
2. **Mechanism.** Temperature in Celsius: which of mean, difference, ratio, median fails to survive conversion to Fahrenheit?

## Practice seed

**Stem.** A room is 10 C and another is 20 C. Is the second twice as warm? Convert both to Fahrenheit and answer again. Then do the same for two spends of 10 and 20 pounds, converted to pence.
**Hint.** Do not argue about it. Convert, recompute the ratio, and compare the two answers.
**Solution path.** 10 and 20 C are 50 and 68 F, so the ratio goes from 2.0 to 1.36; the conversion was legitimate, so the ratio was meaningless. 10 and 20 pounds are 1000 and 2000 pence, ratio 2.0 both times, because a ratio scale allows only multiplication and it cancels.
**`.p-check`.** If your two ratios agree, the scale has a true zero. If they disagree, it does not, and no amount of care in the arithmetic will fix that.

## Code and dataset

**`code/0020-the-measurement-scale-ladder.py` against `datasets/population.csv`.** Already written and landed in #57.

**Dataset note, and why it is not `sessions.csv`.** This brief originally named `sessions.csv`, which predates the dataset ruling and cannot carry this page: it has **no interval column at all**, and the ordinal column would have had to be constructed on the spot. `population.csv` was generated for exactly this lesson and carries one column of every rung, with `office_temp_c` being the interval column nothing else in the course has. The page uses `population.csv` and this brief is corrected to match.

The program runs the transformation test on each of the four columns and prints both conclusions, before and after, which is the only way to show that a statistic was never meaningful rather than merely inconvenient.

## Sources

- **Stevens, S. S., "On the Theory of Scales of Measurement", *Science* 103 (1946), 677-680.** The primary source for the ladder, and specifically for the framing this page uses: a scale is defined by the transformations that leave it invariant, and a statistic is meaningful on that scale only if it survives them. Cite this rather than a summary of it.
