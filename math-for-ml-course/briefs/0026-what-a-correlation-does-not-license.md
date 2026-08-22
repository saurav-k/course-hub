# 0026 Anscombe, and what a correlation does not license

| | |
|---|---|
| Module | M02 Data and summaries |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,000 to 1,200 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S02 and S13 |

## One tight idea

A correlation coefficient is a summary of a picture you have not looked at, and it licenses no claim about direction or cause.

## Prerequisites

`0025` for the coefficient itself, `0024` for shape.

## Downstream

M09's A/B testing page assumes this warning has landed. Every later page that reports an association relies on it.

## Boundaries: what this page must not teach

- **No probability anywhere in M02.** Every quantity is arithmetic on a column that already exists. M07 introduces random variables and M08 the expectation operator.
- Where a page wants to say "this estimates something", it says so in one sentence and forward-references M09 by module, never by number.
- **Not** causal inference as a field. No do-calculus, no instrumental variables, no potential outcomes. Name that the field exists and stop; a reader who wants it needs a different course.
- **Not** experimental design. `0027` owns sampling, and M09 owns what a randomised comparison buys.
- **Keep it concrete.** This page fails if it becomes philosophy. Every claim is shown on `sessions.csv`, which already carries a real association and a genuine null.

## Beats, in order

1. Anscombe's four datasets, shown before anything is said: same mean, same variance, same correlation, same fitted line, four completely different pictures.
2. The lesson stated plainly: the coefficient is a compression, and this is what it compressed away.
3. **Always plot before trusting a correlation.** State it as the habit and then spend the rest of the page on the second, harder failure.
4. Confounding: a third column driving both. Construct it on data the reader has, so the spurious association is one they can compute themselves.
5. Reverse causation: the arrow pointing the other way, and why the coefficient is symmetric and therefore cannot tell you which.
6. Selection: an association that exists only inside the rows you kept. This is the one that bites in machine learning, because a training set is always a selected set.
7. The one honest thing a correlation does license: a prediction, within the range and the population it was measured on. Say what that is worth and what it is not.
8. Close on the reading habit: when you see an association, ask what else could produce it before asking what it means.

## Figures

- **Orientation**, `flowchart`: *a coefficient (`0025`)* -> **THIS PAGE: three ways it misleads** -> *M09's experiments, every model you fit* -> *(dotted) M02*.
- **`svg.chart`**, required: Anscombe's four sets in a 2x2 grid inside one `<figure>`, one identical regression line drawn across all four. Reuse `0024`'s figure deliberately; a reader meeting it twice in two pages is being taught, not repeated at.
- **`svg.chart`**: the confounding picture. The spurious association drawn once for the whole data, then again split by the confounding column, showing the association vanish inside each group.

## Worked example

Build a confounder on `sessions.csv`: `device` drives both `session_seconds` and `spend`. Report the overall correlation, then the correlation within each device group. The drop between them is the confounding, quantified rather than described.

## Quiz seeds

1. **Misconception.** Two columns correlate at 0.9. Which claim is licensed? Distractors must include "one causes the other" and "they are linearly related in this sample" - the second being **correct** and the first the trap, with feedback saying exactly why the modest claim is the true one.
2. **Mechanism.** Which of confounding, reverse causation or selection is the one a training set always risks?

## Practice seed

**Stem.** Given a table where an association is strong overall and near zero inside every subgroup, name the phenomenon and say which column is responsible.
**Hint.** Compute the association separately inside each group before concluding anything about the whole.
**Solution path.** Overall correlation, then per-group correlations, then the identification of the grouping column as the confounder.
**`.p-check`.** If the association survives inside every subgroup at roughly its original strength, that grouping column is **not** the confounder and you are looking at the wrong one.

## Code and dataset

`code/0026-what-a-correlation-does-not-license.py` against `datasets/sessions.csv`. Computes the overall correlation between two columns, then the same correlation within each `device` group, and prints both. Also loads `datasets/anscombe.csv`, which #57 added as a committed dataset transcribed from the paper rather than the inline rows this brief originally assumed, and asserts all four sets share a mean, variance and correlation to the printed precision.

## Sources

- Anscombe, "Graphs in Statistical Analysis", *The American Statistician* 27(1), 1973, for the four datasets and their identical statistics.
