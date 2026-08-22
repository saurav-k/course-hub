# M07-07 - The base-rate trap, worked

**Class:** core. **Rung:** working.

## The single tight idea

When the positive class is rare the posterior is dominated by the prior, so a detector's accuracy on positives tells you almost nothing about what a positive prediction means.

## Prerequisites

| Page | What it supplies |
|---|---|
| M07-06 | Bayes' theorem and the odds form |
| M07-04 | conditional probability |

## Beats, in order

1. **Ask before telling.** Open with the classic screening question in a callout, and invite the reader to answer before reading on: a condition affects 1 in 1,000, a test has a 5 percent false-positive rate and catches essentially every real case. Someone tests positive. What is the chance they have it?
2. **Work it in probabilities.** `0.001 / (0.001 + 0.05 x 0.999) = 0.0196`, so about 2 percent.
3. **Work the identical problem in natural frequencies.** Of 100,000 people, 100 have it and all test positive; of the remaining 99,900, some 4,995 test positive anyway; so 100 of 5,095 positives are real, which is 1.96 percent. Same arithmetic, no fractions.
4. **What the research found, naming no person (D16).** A 1978 study put that question to 60 clinicians and students at a teaching hospital: the most common answer was 95 percent, given by 27 of the 60, and only 11 gave 2 percent. A later study of 48 physicians across four diagnostic problems found the Bayesian answer given in 10 percent of cases when the numbers came as probabilities and 46 percent when the same numbers came as natural frequencies. **The format, not the mathematics, is what moved the answers.** Report the finding; name no individual, and do not frame it as a story about people being foolish. The lesson is that the presentation defeats trained readers, and here is the presentation that does not.
5. **A second data point.** A mammography problem with a 1 percent base rate, 79 percent sensitivity and a 9.6 percent false-positive rate gives 7.67 percent, and in the reported study 95 of 100 physicians estimated between 70 and 80 percent.
6. **The transfer, which is why this page is in a maths-for-ML course.** Precision is the posterior. On `requests.csv` the abuse rate is 99 in 25,000, or 0.003960. At threshold 0.5 the detector has recall 0.9192 and a false-positive rate of 0.0116, and its precision is **0.2395**: of 380 flags, 91 are real and 289 are not. Three flags in four are wrong, from a detector that catches 92 percent of real abuse.
7. **The fix is not recall.** Raising the threshold to 0.6 drops recall to 0.7374 and lifts precision to 0.6033. Show the trade as a number, not as a slogan.
8. **The control that ends the argument.** Always predicting "clean" on this file scores **99.604 percent accuracy** and catches nothing. Accuracy on an imbalanced file is not a weak metric, it is a meaningless one.
9. **What to report instead.** Precision at a stated recall, on the real base rate, with the false-positive count in absolute terms, because a reviewer's time is spent per false positive and not per percentage point.

## Proof

No new theorem. The page applies M07-06's Bayes' theorem, and says so rather than restating it.

An observation worth stating and justifying in one line, because it is the page's whole claim: holding recall and false-positive rate fixed, precision is increasing in the prior, and as the prior goes to zero precision goes to zero. From the Bayes expression, dividing top and bottom by the prior gives `precision = recall / (recall + FPR x (1 - prior) / prior)`, and the second term in the denominator grows without bound as the prior shrinks.

## Planned figures

1. **Orientation, `flowchart LR`.** `M07-06 Bayes` feeds `THIS PAGE - the base-rate trap`, which enables `M09 evaluation` and `every rare-class problem you will ship`.
2. **`svg.chart` - the natural-frequency block.** 25,000 requests as a block; 99 abusive picked out in `m-alarm`; the 380 flags pulled out beside it at readable scale as 91 `m-alarm` against 289 `m-noise`. The count, not the rate, is what lands.
3. **`svg.chart` - precision against base rate.** Recall fixed at 0.9192 and FPR at 0.0116, log x-axis from 0.001 to 0.5, curve through 7.35, 23.95, 44.44, 80.65, 95.19 and 98.75 percent, with a `ref` line at the file's own 0.003960. The detector never changes; only the prior does.
4. **`svg.chart` - the threshold trade.** Recall and precision as two `s-` curves against threshold from 0.3 to 0.7, crossing between 0.5 and 0.6, with the two quoted operating points marked in `gold`.

## The worked example, eight parts

1. **Setting.** `requests.csv`, the abuse detector at threshold 0.5.
2. **Symbolic.** Precision as Bayes, gloss naming recall as `P(flag | abuse)`, FPR as `P(flag | clean)`, prior as `P(abuse)`, precision as `P(abuse | flag)`.
3. **Picture first.** Figure 2 above.
4. **`ol.worked`.** Prior `99 / 25,000 = 0.003960`. True positives `91`, false negatives `8`, so recall `91 / 99 = 0.9192`. False positives `289` out of `24,901` clean, so FPR `0.0116`. Bayes: `0.9192 x 0.003960 / (0.9192 x 0.003960 + 0.0116 x 0.996040) = 0.2395`. Direct count: `91 / 380 = 0.2395`.
5. **`keynum`.** Counts read from the file. The two 0.2395 values are both derived here, by different routes, which is the check.
6. **Sanity check.** Precision must lie between 0 and 1 and, for a rare positive class with a non-trivial false-positive rate, must be far below recall. If precision came out near recall, the prior was applied wrongly.
7. **What changes if.** Ten times the abuse, prior 0.0396: precision rises from 0.2395 to 0.7656 with the detector untouched. **The single biggest driver of precision is not the model.**
8. **Interpretation.** 289 false alarms at, say, 90 seconds of review each is more than seven hours of work to surface 91 real cases. That is the number a decision gets made on, and it is invisible in "92 percent recall".

## Code and dataset

`code/0070-the-base-rate-trap.py` against `datasets/requests.csv`.

Sweeps the threshold from 0.3 to 0.75 and, at each step, computes precision twice: once by counting the confusion matrix and once from Bayes using the measured recall, FPR and prior, asserting agreement. Prints the table the page quotes. Then holds recall and FPR fixed at the 0.5-threshold values and sweeps the prior by resampling the clean rows, showing precision moving from 7 percent to 99 percent with the detector unchanged.

## Quiz seeds

1. **Misconception.** A detector holds recall at 0.92 and FPR at 0.012. The abuse rate rises from 0.4 percent to 4 percent. What happened to precision? *Correct:* it rose from 23.95 to 76.56 percent, and the detector did not change. *Distractors:* nothing, precision depends only on the model; it fell, because there is more abuse to miss; it cannot be known without retraining.
2. What accuracy does "always predict clean" achieve on this file? *Correct:* 99.604 percent, catching nothing.

## Practice seed

**Stem.** At threshold 0.6 the detector has recall 0.7374 and FPR 0.0019 on the same file. Compute its precision, the absolute number of false alarms, and say which of the two thresholds you would ship if a reviewer takes 90 seconds per alert and a missed abuse costs 20 minutes of incident time.
**Hint.** Precision needs the same three inputs as before. For the decision, put both options into the same unit: minutes.
**Solution.** `0.7374 x 0.003960 / (0.7374 x 0.003960 + 0.0019 x 0.996040) = 0.6033`; false alarms `0.0019 x 24,901 = 48`. Threshold 0.5: 380 alerts is 570 minutes of review, and 8 missed abuses is 160 minutes, so 730. Threshold 0.6: 121 alerts is 182 minutes, and 26 missed is 520 minutes, so 702. **Threshold 0.6 wins, narrowly**, and the answer flips if a missed abuse costs 30 minutes rather than 20.
**`.p-check`.** Precision at 0.6 must exceed precision at 0.5, because a higher threshold discards more clean rows than abusive ones. If it did not, the counts were swapped.

## Sources

- Hoffrage and Gigerenzer, "How to Improve the Diagnostic Inferences of Medical Experts", in Kurz-Milcke and Gigerenzer (eds), *Experts in Science and Society*, Kluwer 2004, pp 249-268. It quotes the 1978 screening question verbatim at its p 999 citation and reports the 48-physician result.
- Hajek, ECE 313, section 2.10, for the Bayes machinery being applied.
