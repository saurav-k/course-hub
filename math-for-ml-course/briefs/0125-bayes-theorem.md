# M07-06 - Bayes' theorem

**Class:** core. **Rung:** working.

## The single tight idea

Bayes' theorem is two lines of algebra from the definition of conditional probability, and it is the only route from "how the detector behaves given abuse" to "is this request abuse".

## Prerequisites

| Page | What it supplies |
|---|---|
| M07-04 | conditional probability, the multiplication rule |
| M07-02 | partitions |

## Beats, in order

1. **Name the asymmetry first, with the module's own numbers.** `P(flagged | unverified)` is 0.010694 and `P(unverified | flagged)` is 0.8081. Same two events, factor of 75. The failure to notice has a name: the confusion of the inverse.
2. **Derive it.** `P(AB)` equals both `P(A|B)P(B)` and `P(B|A)P(A)`, so set them equal and divide. Two lines and no new ideas. Proof below.
3. **The denominator is the law of total probability**, not a mysterious normaliser. Proof below.
4. **Name the four terms once and use them forever.** Prior, likelihood, evidence, posterior, each in words and each pointed at a piece of the worked example.
5. **The odds form.** Posterior odds equals prior odds times the likelihood ratio. One multiplication, and the evidence term cancels. On the module's data the prior odds of unverified are `0.29924 / 0.70076 = 0.4270`, the likelihood ratio is `0.010694 / 0.001085 = 9.86`, and the product `4.2105` is posterior odds, which converts back to `0.8081`. **The same answer with no denominator.**
6. **Sequential updating.** Yesterday's posterior is today's prior; with conditionally independent evidence the likelihood ratios multiply. This is why practitioners use the odds form.
7. **The machine-learning section.** Precision is a posterior. Compute it for the module's detector at threshold 0.5 from prior and likelihoods, and check it against a direct count of the confusion matrix; they agree to four decimals. Then name the maximum-likelihood and maximum-a-posteriori decision rules in one sentence each and hand inference to M09.
8. **Honest limit callout.** Bayes returns a posterior only if you supply a prior. Where the prior is genuinely unknown the theorem does not rescue you, and calling a uniform prior "no assumption" is itself an assumption - which M07-03 already showed costs 79 percent on this very dataset.

## Proof

**Named theorem 1: the law of total probability.**
If `E1 ... Ek` partition `Omega` and each has positive probability, then `P(A) = P(A|E1)P(E1) + ... + P(A|Ek)P(Ek)`.

*Assumed:* the `Ei` are mutually exclusive and their union is `Omega`.

*Shape:* cut `A` along the partition, add the pieces with axiom 2, then rewrite each piece with the multiplication rule.

*Steps.* Because the `Ei` cover `Omega` and do not overlap, the sets `AE1 ... AEk` are mutually exclusive and their union is `A`. Axiom 2 gives `P(A) = P(AE1) + ... + P(AEk)`. The multiplication rule rewrites each term as `P(A|Ei)P(Ei)`.

**The step that does the real work is that `AE1 ... AEk` are disjoint,** which is inherited from the partition and is the only reason axiom 2 applies.

**Named theorem 2: Bayes' theorem.**
`P(Ei | A) = P(A | Ei) P(Ei) / P(A)`, and expanded, over the partition in the denominator.

*Assumed:* `P(A) > 0` and `P(Ei) > 0`.

*Steps.* By definition `P(Ei|A) = P(A Ei) / P(A)`. By the multiplication rule the numerator is `P(A|Ei)P(Ei)`. Substitute. For the expanded form, replace `P(A)` using theorem 1.

**The step that does the real work is writing the joint two ways.** `P(A Ei)` does not care which event you condition on, and that symmetry is the entire content of the theorem; everything else is division.

*Honest note.* The theorem is arithmetic and cannot be wrong. Every disagreement about a Bayesian answer is a disagreement about the prior, never about this.

## Planned figures

1. **Orientation, `flowchart LR`.** `M07-04 conditioning` and `M07-02 partitions` feed `THIS PAGE - Bayes`, which enables `the base-rate trap`, `naive Bayes` and `M09 inference`.
2. **`flowchart LR` - the machine.** `prior` and `likelihood` into `multiply`, into `unnormalised`, into `divide by the evidence`, into `posterior`, with the evidence node exploded into the total-probability sum over the two-part partition.
3. **`svg.chart` - the two-way slab.** A unit rectangle split vertically by the prior into a 0.2992 unverified column and a 0.7008 verified column, then each split horizontally by its flag rate. The two flagged slivers are `m-alarm`; the posterior is visibly the left sliver as a share of both slivers, 80 against 99. This one figure carries the whole page.
4. **`svg.chart` - the odds form.** A single horizontal log-odds axis with the prior odds 0.4270 marked, an arrow labelled "x 9.86" and the posterior odds 4.2105 marked. Multiplication as a shift along a line.

## The worked example, eight parts

1. **Setting.** `requests.csv`. Reverse `P(flagged | unverified)` into `P(unverified | flagged)`.
2. **Symbolic.** Bayes in the expanded form, gloss naming prior, likelihood, evidence, posterior against the four numbers about to be used.
3. **Picture first.** Figure 3 above.
4. **`ol.worked`.** Prior `P(unverified) = 7,481 / 25,000 = 0.29924`. Likelihoods `0.010694` and `0.001085`. Evidence by total probability: `0.010694 x 0.29924 + 0.001085 x 0.70076 = 0.003200 + 0.000760 = 0.003960`, which is the observed flag rate exactly. Posterior `0.010694 x 0.29924 / 0.003960 = 0.8081`. Then check it against the direct count: `80 / 99 = 0.8081`.
5. **`keynum`.** Counts read from the file; every quotient derived here and plain.
6. **Sanity check.** The evidence recovered from the two conditionals must equal the flag rate you can count directly. It does, to six decimals, and if it did not the arithmetic would be wrong.
7. **What changes if.** Suppose verification were dropped so everyone is unverified. The prior goes to 1, the posterior goes to 1, and the detector learns nothing from the column - a feature with no variation carries no evidence.
8. **Interpretation.** The prior said 30 percent, the evidence said 81 percent, and the whole move was one multiplication by the likelihood ratio 9.86.

## Code and dataset

`code/0125-bayes-theorem.py` against `datasets/requests.csv`.

Computes the posterior three ways and asserts all three agree: from the expanded Bayes formula; from the odds form as prior odds times likelihood ratio converted back; and by direct counting of the confusion table. Then computes the detector's precision at thresholds 0.5 and 0.6 from Bayes and from the counted confusion matrix, asserting agreement, and prints the pair so the page can quote 0.2395 and 0.6033.

## Quiz seeds

1. **Misconception.** A detector fires on 92 percent of abusive requests. A request just fired. What is the chance it is abusive? *Correct:* not determined - you also need the base rate and the false-positive rate. *Distractors:* 92 percent; 8 percent; slightly under 92 percent. Feedback: 92 percent is the likelihood and answers the reverse question.
2. In `P(E|A) = P(A|E)P(E) / P(A)`, which term is the evidence? *Correct:* the denominator, which the law of total probability expands.

## Practice seed

**Stem.** Prior odds that a request is unverified are 0.4270 to 1. A second, conditionally independent signal fires with likelihood ratio 3.0. Starting from the flag evidence already applied, what are the posterior odds and the posterior probability?
**Hint.** In odds form, independent evidence multiplies. You do not need the evidence term at all.
**Solution.** `0.4270 x 9.86 x 3.0 = 12.632` posterior odds; as a probability `12.632 / (1 + 12.632) = 0.9266`.
**`.p-check`.** Adding evidence that points the same way must raise the posterior, so the answer must exceed 0.8081, and it must stay below 1.

## Sources

- Hajek, ECE 313, section 2.10, eqs 2.16 and 2.17, and Example 2.10.3.
- Goodfellow, Bengio, Courville, *Deep Learning*, ch 3.5.
