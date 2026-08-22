# 0027 Survey sampling designs, and which question each one answers

| | |
|---|---|
| Module | M02 Data and summaries |
| Rung | `pill easy` |
| Class | depth |
| Word budget | 1,000 to 1,200 prose words, excluding practice and quiz text |
| Source scout | `mlm-sfml-notes-r11` gap 4 |

## One tight idea

How you choose the rows decides which population your summary describes, and no amount of arithmetic afterwards can repair a badly chosen sample.

## Prerequisites

`0002` for partitions, `0022` for the summaries these designs are computed on.

## Downstream

M08 owns sampling **from a distribution**, which is a different act wearing the same word, and its brief must say so. M09's cross-validation borrows stratification directly.

## Boundaries: what this page must not teach

- **No probability anywhere in M02.** Every quantity is arithmetic on a column that already exists. M07 introduces random variables and M08 the expectation operator.
- Where a page wants to say "this estimates something", it says so in one sentence and forward-references M09 by module, never by number.
- **Not** sampling from a distribution. **This is the word collision the course has to survive**: M08's "sampling" means drawing from a known law, this page's means choosing rows from a real population. Both briefs say so explicitly.
- **Not** the standard error or any sampling distribution. M08 owns both, and this page must not compute how wrong a sample is - only how it was chosen.
- **The only `depth` page in M02**, because a reader can skip it and still read the rest of the course.

## Beats, in order

1. The question every design answers: which population does this sample let me describe?
2. Simple random: every row equally likely. The baseline, and the thing every other design is compared against.
3. Stratified: partition first, then sample inside each part. Point at `0002`: the strata are a partition, and that word carries the guarantee.
4. Why stratification helps: it removes the luck of the draw across groups. **Stratified k-fold cross-validation is the same idea**, and saying so converts an ML habit into a statistical fact.
5. Cluster: sample whole groups. Cheap, and it buys that cheapness with rows that resemble each other.
6. Systematic: every k-th row, and the one way it fails badly, which is when the data has a period that matches k.
7. Convenience: whoever was easiest to reach. Name it plainly as the design most real datasets actually have, including most machine learning benchmarks.
8. Close on the honest reading: a summary describes the population your design actually sampled, which is often narrower than the one you meant.

## Figures

- **Orientation**, `flowchart`: *a population and a partition (`0002`)* -> **THIS PAGE: which rows you chose, and therefore who your answer is about** -> *M09's cross-validation, M08's sampling from a law* -> *(dotted) M02*.
- **`svg.chart`**, required: one population of dots coloured by group, drawn five times in a small-multiples row inside one `<figure>`, with the selected rows highlighted under each design. The cluster panel visibly misses two groups entirely, which is the argument.
- **`flowchart`**: the five designs as a decision tree keyed on what you can afford and what you know about the groups.

## Worked example

A 60-row population with three groups of unequal size. Draw 12 rows by simple random and by stratified sampling, and report the group proportions in each sample against the population. Stratification matches by construction; the simple random draw is off by a visible margin, and that margin is the page's point.

## Quiz seeds

1. **Misconception.** Cluster sampling gives you the same information per row as simple random. Distractors should include "yes, if the clusters are chosen at random", which is a true statement about *unbiasedness* answering a question about *information*.
2. **Mechanism.** Which design is stratified k-fold cross-validation an instance of?

## Practice seed

**Stem.** A population of 1,000 rows with three groups in a 70/20/10 split. You may sample 100. Give the stratified allocation, and say what a simple random draw risks for the smallest group.
**Hint.** Stratified allocation is proportional unless you have a reason to over-sample.
**Solution path.** 70/20/10 becomes 70/20/10 of 100; then the observation that a random draw can easily return very few of the 10 per cent group.
**`.p-check`.** Your allocation must sum to exactly 100 and each group must get at least one row. If any group gets zero, the design has silently become a two-group study.

## Code and dataset

`code/0027-survey-sampling-designs.py` against `datasets/sessions.csv`, using `device` as the strata. Draws 500 rows simple-random and 500 stratified, 200 times each with a seed, and reports the spread of the `mobile` proportion under both. The stratified spread is near zero by construction and the random one is not; the printed numbers are what the page quotes.

## Sources

- A primary source for the sampling-design taxonomy.
- A library's stratified k-fold documentation, for the cross-link in beat 4.
