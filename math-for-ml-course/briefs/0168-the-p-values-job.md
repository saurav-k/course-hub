# 0168 The p-value's job, and the four jobs it gets by mistake

| | |
|---|---|
| Module | M09 Estimation, testing, and inference |
| Rung | `pill med` |
| Class | core |
| Word budget | 1,100 to 1,400 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S11 |

## One tight idea

A p-value is a compatibility measure computed under a whole model, and almost every popular reading of it swaps a conditional round.

## Prerequisites

`0167` for the test that produces one. `0125` for Bayes' theorem, which is what the first misreading silently requires.

## Downstream

`0169` inherits the multiplicity problem as a stopping rule. `0173` supplies the machinery the first misreading actually needs.

## Boundaries: what this page must not teach

- **Not a second test.** No new statistic is derived here. The page is about reading the number `0167` already produced.
- **Not Bayes factors.** Name them once as an alternative and hand the school to `0173`.
- **Not research-integrity discourse.** The page stays technical: the failures are arithmetic and procedural, and it demonstrates them on data rather than deploring them.
- Name no person and no paper as a culprit. D16.

## Beats, in order

1. The definition, read slowly and clause by clause: the probability that the chosen test statistic would be at least as extreme as observed, **if every model assumption were correct, including the test hypothesis**. Every clause carries weight.
2. **Under `H0` a p-value is uniform.** Prove it, then read the consequence off immediately: `P(p <= 0.05) = 0.05` when nothing is going on. That *is* what the threshold means, and it makes everything below arithmetic rather than opinion.
3. The four misreadings, each with the correct account: it is not `P(H0 | data)`; `p > 0.05` is not evidence of no effect; it is not the probability the result was due to chance; it does not measure effect size.
4. **Multiplicity**, as a direct corollary of beat 2. Twenty independent tests at `alpha = 0.05` give at least one false positive with probability `1 - 0.95^20 = 0.6415`. Show the arithmetic and then show it happening on real slices.
5. Bonferroni: control the chance of *any* false positive by testing at `alpha/m`. Prove it from the union bound. Note that it gets conservative fast.
6. Benjamini-Hochberg: control the expected *proportion* of false positives among rejections. Give the step-up rule exactly, and show it rejecting more than Bonferroni on the same p-values.
7. **p-hacking without dishonesty.** Slice a dataset by a coin flip that changes nothing, report the best slice, and note that every individual test was computed correctly. The error is choosing what to report after looking.
8. Close constructively: report the effect size and its interval, and the p-value as one input among several.

## Named theorems and their stated proofs (D4)

**Theorem 1 (uniformity under the null).** If the test statistic `T` has a continuous distribution under `H0` with CDF `F`, and `P = 1 - F(T)`, then `P ~ Uniform(0,1)` under `H0`.
**Proof.** For `u` in `(0,1)`, `P(P <= u) = P(1 - F(T) <= u) = P(F(T) >= 1 - u)`. Since `F(T)` is the probability integral transform of `T` under its own distribution, `F(T) ~ Uniform(0,1)`, so that probability is `1 - (1 - u) = u`. A random variable whose CDF is the identity on `(0,1)` is uniform. []

**Corollary (family-wise error).** With `m` independent true nulls, `P(at least one p <= alpha) = 1 - (1 - alpha)^m`, which at `alpha = 0.05` and `m = 20` is `0.6415`.

**Theorem 2 (Bonferroni controls the family-wise error rate).** Testing each of `m` hypotheses at level `alpha/m` gives `P(any false positive) <= alpha`.
**Proof.** Let `m_0` be the number of true nulls. By the union bound, `P(any false positive) <= sum over true nulls of P(p_i <= alpha/m) = m_0 (alpha/m) <= alpha`, since `m_0 <= m`. No independence is needed, which is why Bonferroni is safe and blunt. []

**Benjamini-Hochberg, stated not proved.** Sort the p-values ascending, find the largest `i` with `p_(i) <= (i/m) q`, and reject the first `i`. Under independence this controls the false discovery rate at `q`. **The proof is not reproduced**, because the paper's own text could not be opened during this build and the course does not quote a proof it has not read. State the procedure, cite the paper, and say plainly that the control result is taken on citation.

**The honest boundary.** Theorem 1 assumes a continuous test statistic. For a discrete one, a proportion with small counts for instance, the p-value is not exactly uniform, it is stochastically larger than uniform, and the test is conservative. That is worth one sentence because it explains why exact tests on small counts reject less often than their nominal level suggests.

## Figures

- **Orientation**, `mindmap`: root *the p-value's one correct reading*, four branches, one per misreading, each leaf naming what that number actually is a statement about.
- **`svg.chart`**, required: the histogram of 40,000 p-values from tests where nothing is going on, visibly flat, with the `[0, 0.05]` bucket shaded and labelled with its share. Kills: "a small p-value is rare", which it is not when the null is true.
- **`svg.chart`**: `1 - 0.95^m` against `m`, rising to 0.64 at 20, with `alpha = 0.05` drawn as a flat reference line.
- **`svg.chart`**: sorted p-values as dots against rank, with Bonferroni's horizontal line and BH's sloped `(i/m)q` line drawn across them, and the rejected points marked under each.

## Worked example

Two halves. First, 40,000 two-proportion tests where both arms have the same true rate: the p-values fall in the expected proportions in every bucket, and `0.05` of them land at or below 0.05 by construction. Then the same p-values blocked into families of 1, 5, 10, 20 and 40 with the analytic and measured family-wise rates side by side.

Second, on `population.csv`: assign a coin-flip label that changes nothing, binarise spend at its median, and test the twenty `region` by `stratum` slices. Report how many came in at or below 0.05 uncorrected, and then under Bonferroni and BH, both of which should reject nothing because the label was a coin flip. Close with a constructed set of twenty p-values, five of them genuinely small, where Bonferroni rejects three and BH rejects five: that gap is the power BH buys by letting its threshold rise with rank.

## Quiz seeds

1. **Misconception.** `p = 0.03`. What is the probability the null is true? Answer: the p-value does not say. Distractors "three per cent" and "ninety-seven per cent" swap the conditional in opposite directions and both must appear.
2. **Mechanism.** Twenty independent guardrail metrics at `alpha = 0.05` on a null experiment. How often does at least one look significant? Answer: about sixty-four per cent. Distractor "five per cent" is the per-metric rate and is exactly the confusion.

## Practice seed

**Stem.** Five p-values: `0.008, 0.021, 0.033, 0.041, 0.180`. Which survive Bonferroni at family-wise 0.05? Apply Benjamini-Hochberg at `q = 0.05` and say which survive. Then explain in one sentence what each procedure controls.
**Hint.** For BH compute `(i/m) x q` at each rank and find the **largest** `i` whose p-value is at or below its threshold.
**Solution path.** Bonferroni threshold `0.05/5 = 0.01`, so only `0.008` survives. BH thresholds are `0.010, 0.020, 0.030, 0.040, 0.050`; comparing in order, only rank 1 passes, so `i = 1` and only `0.008` is rejected. Bonferroni controls the probability of any false positive; BH controls the expected proportion of false positives among the rejections.
**`.p-check`.** BH is usually the more permissive of the two and here it is not. That is not an error: BH is more permissive when the p-values are small *relative to their ranks*, and these are not. Change `0.021` to `0.015` and BH rejects two while Bonferroni still rejects one.

## Code and dataset

`code/0168-the-p-values-job.py` against `datasets/population.csv`, already on main from #57. Reference it; do not rewrite it.

## Sources

- Wasserstein and Lazar (2016), the ASA Statement on Statistical Significance and P-Values, for the definition and the six principles. `https://www.amstat.org/asa/files/pdfs/P-ValueStatement.pdf`
- Greenland et al. (2016), *European Journal of Epidemiology* 31, 337-350, for the numbered misinterpretations. `https://pmc.ncbi.nlm.nih.gov/articles/PMC4877414/`
- Benjamini and Hochberg (1995), *JRSS-B* 57(1), 289-300, cited for the step-up procedure. The control theorem is taken on citation and not reproduced.
