# 0020 The measurement-scale ladder, and which summaries a column allows

| | |
|---|---|
| Module | M02 Data and summaries |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,000 to 1,200 prose words, excluding practice and quiz text |
| Source scout | `mlm-sfml-notes-r11` gap 3 |

## One tight idea

A column's measurement scale decides which summaries and which tests are even meaningful on it, and getting that wrong produces a number rather than an error.

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

1. Open on the failure: the mean of a postcode, the mean of a five-point satisfaction scale. Both compute. Neither means anything, and nothing in the tooling will tell you.
2. Nominal: labels with no order. Legal summaries are the mode and a frequency count, and nothing else.
3. Ordinal: order without spacing. The median becomes legal; the mean does not, because the gap between "agree" and "strongly agree" is not the gap between "neutral" and "agree".
4. Interval: equal spacing, arbitrary zero. The mean becomes legal, ratios do not. Twenty degrees is not twice ten.
5. Ratio: equal spacing and a true zero. Everything is legal, including ratios and the geometric mean.
6. The ladder as a table: for each scale, what is legal, what is not, and the one machine learning column that is usually mislabelled.
7. Where this bites in practice: a model given an ordinal column as if it were ratio has been told a false fact about the spacing, and it will use it.
8. Close on the reading habit: before summarising a column, name its scale out loud. It takes two seconds and it is the cheapest bug prevention in the module.

## Figures

- **Orientation**, `flowchart`: *a set of values (`0002`)* -> **THIS PAGE: which scale, and therefore which summaries are legal** -> *every later page in M02* -> *(dotted) M02*.
- **`svg.chart`**, required: the same five-point ordinal column summarised three ways, mode, median and mean, drawn on one axis so the reader sees the mean landing between categories where nothing exists.
- **`flowchart`**: the four-rung ladder as a decision tree, each rung adding one permitted operation.

## Worked example

Take `device` and `returning` from `sessions.csv` (nominal), a constructed five-point rating (ordinal), and `session_seconds` (ratio). For each, compute all three of mode, median and mean, and mark which are meaningful. The point lands when the reader sees a number computed successfully and still marked invalid.

## Quiz seeds

1. **Misconception.** Is a five-point Likert scale interval or ordinal? Distractors must include "interval, because the numbers are evenly spaced", which is true of the *encoding* and false of the *scale*, and the feedback must say exactly that.
2. **Mechanism.** Which scale is the lowest that permits a median?

## Practice seed

**Stem.** Six named columns. For each, give the scale and the highest-information legal summary.
**Hint.** Ask two questions in order: is there an order, and is there a true zero.
**Solution path.** The two questions partition the four scales; then read the legal summary off the ladder.
**`.p-check`.** If you marked a column as ratio, check that doubling its value doubles the thing it measures. Temperature in Celsius fails this and is the classic trap.

## Code and dataset

`code/0020-the-measurement-scale-ladder.py` against `datasets/sessions.csv`. Computes mean, median and mode for every column, then prints a table marking each as legal or not against a declared scale for that column. Nothing raises; that is the demonstration.

## Sources

- A primary source for the four-scale taxonomy, fetched and linked.
