# 0027 Survey sampling designs, and which question each one answers

| | |
|---|---|
| Module | M02 Data and summaries |
| Rung | `pill easy` |
| Class | depth |
| Word budget | 1,000 to 1,200 prose words, excluding practice and quiz text |
| Source scout | `mlm-sfml-notes-r11` gap 4 |
| Dataset | **`population.csv`**, not `sessions.csv`. See the dataset note below. |

## One tight idea

How you choose the rows decides how precise your answer is, and stratifying removes exactly the between-stratum variance from the error, which on this population is 87 per cent of it.

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

1. The question every design answers: which population does this sample let me describe, and how precise is the answer.
2. Simple random: every unit equally likely. The baseline, and unbiased for the population mean, which is the theorem below.
3. Stratified: partition first, then sample inside each part. Point at `0002`: the strata are a partition, and that word carries the guarantee that every unit belongs to exactly one.
4. **Why stratification helps, quantitatively rather than as a slogan.** Total variance splits into a within-stratum part and a between-stratum part. Stratified sampling removes the between part from the error, because it fixes how many units come from each stratum instead of leaving it to the draw. On `population.csv` the between part is **87.4 per cent** of the total, which predicts the measured variance ratio of about **0.13**, and the page shows both numbers side by side.
5. **Stratified k-fold cross-validation is the same idea**, and saying so converts an ML habit into a statistical fact. M09 uses it.
6. Cluster: sample whole groups. Cheap, and it buys that cheapness with units that resemble one another, so **each extra unit inside a chosen cluster tells you less than a fresh independent unit would**. On this population cluster sampling is measurably worse than simple random, and the page reports by how much.
7. Systematic: every k-th unit, and the one way it fails badly, which is when the data has a period matching k.
8. Convenience: whoever was easiest to reach. Name it plainly as the design most real datasets actually have, including most machine learning benchmarks.
9. Close on the honest reading: a summary describes the population your design actually sampled, which is often narrower than the one you meant, and no arithmetic afterwards repairs it.

## Stated proof (D4)

Two named results, and the page owes both.

**1. Simple random sampling is unbiased for the population mean.** Each unit's probability of appearing in a sample of size `n` drawn without replacement from `N` units is `n/N`, the same for every unit. The sample mean is therefore an average in which every population unit carries equal weight in expectation, so its expectation is the population mean. **The step that does the work** is that the inclusion probability is identical across units; it is what equal weighting in the estimator has to match.

**2. Stratified sampling has lower variance than simple random of the same size.** Write the population variance as within-stratum plus between-stratum. Simple random sampling pays for both, because the number of units it happens to draw from each stratum varies from sample to sample. Proportionally allocated stratified sampling fixes those counts, so the between-stratum term never enters the sampling error at all, leaving only the within part.

**The step that does the work** is that fixing the allocation removes a source of randomness rather than averaging over it. **State the boundary honestly**: this is why cluster sampling does *not* get the same benefit. It also fixes something, but what it fixes is which whole groups are in, and units inside a group resemble one another, so it *adds* a source of variation instead of removing one.

## Figures

- **Orientation**, `flowchart`: *a population and a partition (`0002`)* -> **THIS PAGE: which rows you chose, and therefore who your answer is about** -> *M09's cross-validation, M08's sampling from a law* -> *(dotted) M02*.
- **`svg.chart`**, required: the sampling distribution of the estimated mean under all three designs, drawn as three overlaid densities from the program's repeated draws. All three centre on the same population mean, and the stratified one is visibly narrower while the cluster one is visibly wider. **Unbiasedness and precision are different properties and this figure shows both at once.**
- **`svg.chart`**: the variance decomposition as a single stacked bar, within against between, annotated with 79,955 and 552,775 and the 87.4 per cent share. This is the number that predicts the variance ratio, so it earns its own figure.
- **`flowchart`**: the five designs as a decision tree keyed on what you can afford and what you know about the groups.

## Worked example

A 12-unit toy population in three strata of 6, 4 and 2, with deliberately different means. Small enough to enumerate by hand.

Compute the population mean; then the within-stratum and between-stratum variance components and check they sum to the total; then a proportionally allocated stratified sample of 6 and note that its stratum counts are fixed at 3, 2 and 1 in every draw, while a simple random sample of 6 can return anywhere from 0 to 2 units of the smallest stratum. **The fixed counts are the whole mechanism**, and on twelve units the reader can see it rather than take it.

Then quote the same three quantities computed by the program on all 30,000 units: within 79,955.05, between 552,775.08, total 632,730.14, and the between share 87.4 per cent.

## Quiz seeds

1. **Misconception.** Cluster sampling gives you the same information per unit as simple random. Distractors must include "yes, if the clusters are chosen at random", which is a true statement about **unbiasedness** answering a question about **precision**, and the feedback must name that swap explicitly.
2. **Mechanism.** Stratification removes which part of the variance from the sampling error: the within-stratum part, the between-stratum part, both, or neither?

## Practice seed

**Stem.** A population of 1,000 units in three strata, 70/20/10, with stratum means 100, 400 and 900. You may sample 100. Give the proportional allocation. Then compute the between-stratum variance component, and say what fraction of the total it would be if the within-stratum variance were 2,500 in every stratum.
**Hint.** The allocation is proportional. For the components, the between part is the spread of the stratum means around the overall mean, weighted by stratum size.
**Solution path.** 70/20/10 of 100; the overall mean as the weighted average of 100, 400 and 900; the between component from the weighted squared deviations; the within component as the weighted average of 2,500, which is 2,500; then the share.
**`.p-check`.** Your allocation must sum to exactly 100 and no stratum may get zero. The between share must land between 0 and 1: if it exceeds 1 you have divided by the within part instead of the total.

## Code and dataset

**`code/0027-survey-sampling-designs.py` against `datasets/population.csv`.** Already written and landed in #57, and it is correct: its printed decomposition (within 79,955.05, between 552,775.08, total 632,730.14, share 87.4 per cent) reconciles exactly with the population variance, and its measured variance ratio matches what that share predicts.

**Dataset note, and why it is not `sessions.csv`.** This brief originally named `sessions.csv` with `device` as the strata, which predates the dataset ruling and cannot carry this page. `sessions.csv` has **no real strata and no clusters**: `device` groups barely differ in mean, so stratification would remove almost nothing and the page's central claim would have no effect to measure. `population.csv` was generated for this lesson with four strata of unequal size *and* unequal spread, and 600 clusters carrying a cluster-level offset, precisely so that stratification visibly wins and clustering visibly loses. The page uses `population.csv` and this brief is corrected to match.

## Sources

- A primary source for the sampling-design taxonomy and for the stratified variance result, fetched and linked. Cochran's *Sampling Techniques* is the standard reference for the decomposition in the stated proof.
- A library's stratified k-fold documentation, for the cross-link in beat 5.
