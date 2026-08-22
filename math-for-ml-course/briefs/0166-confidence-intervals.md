# 0166 Confidence intervals: what the ninety-five per cent is attached to

| | |
|---|---|
| Module | M09 Estimation, testing, and inference |
| Rung | `pill med` |
| Class | core |
| Word budget | 1,100 to 1,400 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S09 |

## One tight idea

The ninety-five per cent is a property of the procedure across repetitions, not of the one interval on your screen.

## Prerequisites

`0160` for the standard error. M08 for the Central Limit Theorem, quoted here and proved there.

## Downstream

`0167` turns the same machinery into a test. `0169` reports one. `0173` puts the credible interval beside it and shows what the difference costs.

## Boundaries: what this page must not teach

- **Not hypothesis testing.** `0167` owns it. This page ends by showing that comparing two intervals by eye is the wrong tool and naming the right one.
- **Not credible intervals.** `0173` owns them, and the comparison lands much harder once the reader has felt this page's frustration.
- **Not the bootstrap.** One sentence as the onward road for statistics with no closed form.
- Do not present the Wald interval as the interval. It is one procedure with known failures, and the page shows them.

## Beats, in order

1. Build it before interpreting it: standardise, read `1.96` off the standard normal, un-standardise. Three steps the reader can already do.
2. The substitution nobody announces: the formula wants the unknown `p`, so `p_hat` goes in its place. Name it, and name what it costs, which is that the coverage becomes approximate.
3. **The interpretation, and this is the page.** Before you look, the interval is random and covers with probability 0.95. After you look, it is a fixed pair of numbers and the parameter is a fixed number: it either covers or it does not. The 95 per cent describes the rule.
4. Draw twenty intervals from twenty repeats with the truth as a vertical line and one of them missing. A reader who has seen this picture does not make the mistake again.
5. **Coverage is not automatic.** Measure it: at small `n` and small `p` the Wald interval falls short of its nominal level, and at zero successes it returns `[0, 0]`, which is perfect certainty from no evidence. A `.callout.warn` carries this.
6. `z` against `t`: with `sigma` unknown and `n` small the multiplier comes from `t`, and at `n = 5` the normal interval is 42 per cent too narrow. Give the table, because "compare two models over ten seeds" is the `n = 10` row.
7. **The overlap trap**, which sets up the next page. Two overlapping intervals do not establish the absence of a difference, because the right comparison uses the standard error of the difference. State the asymmetry: non-overlap does imply significance, the converse fails.

## Named theorem and its stated proof (D4)

**Theorem (asymptotic coverage of the Wald interval).** If `p_hat` is the sample proportion from `n` independent Bernoulli(`p`) draws, then `P(p in [p_hat - z se, p_hat + z se]) -> 1 - alpha` as `n` grows, where `se = sqrt(p_hat(1-p_hat)/n)` and `z` is the `1 - alpha/2` standard normal quantile.

**Proof.** By `0160`, `E[p_hat] = p` and `Var(p_hat) = p(1-p)/n`. By the Central Limit Theorem, `Z = (p_hat - p)/sqrt(p(1-p)/n)` converges in distribution to a standard normal, so `P(|Z| <= z) -> 1 - alpha`. Rearranging the event `|p_hat - p| <= z sqrt(p(1-p)/n)` for `p` gives an interval centred at `p_hat`. Replacing `p` by `p_hat` inside the standard error is justified because `p_hat -> p` in probability, and Slutsky's theorem then preserves the limiting distribution. []

**The honest boundary.** Every step of that is asymptotic, and the substitution is what makes the coverage approximate rather than exact. The measured coverage on this page falls below 0.95 at small `n`, which is not a bug in the arithmetic: it is the theorem's "as `n` grows" being cashed at an `n` that has not grown. Say this rather than presenting the interval as a guarantee.

## Figures

- **Orientation**, `flowchart`: *the standard error (`0160`)* -> **THIS PAGE: an interval, and what the 95 per cent attaches to** -> *`0167` testing, `0173` credible intervals*.
- **`svg.chart`**, required: twenty horizontal interval bars from twenty simulated repeats against a vertical true-value line, the one that misses drawn in the alarm colour. Kills: the Fundamental Confidence Fallacy, in one picture.
- **`svg.chart`**: the standard normal density with the central 95 per cent shaded and `+/-1.96` on the axis.
- **`svg.chart`**: `t` densities at df 4, 9 and 49 overlaid on the standard normal, their critical values marked, converging.

## Worked example

`sessions.csv`'s `returning` column as the population, resampled: twenty intervals printed with the misses flagged, then a measured-coverage table at `n = 50, 200, 800, 3200` showing the shortfall. Then the `z`-against-`t` multiplier table. Close on `experiment.csv`: control `596/12,000` gives `[4.578%, 5.355%]` and treatment `643/12,000` gives `[4.955%, 5.761%]`. They overlap, and the page states plainly that this is not a verdict and hands the reader to `0167`.

## Quiz seeds

1. **Misconception.** You compute one 95 per cent interval. What is the probability it contains the true value? Answer: either zero or one hundred per cent. Distractors "exactly 95 per cent" and "about 95 per cent" are the two ways people state the fallacy and both must appear.
2. **Mechanism.** Comparing two models over 10 seeds, which multiplier? Answer: 2.262 from the `t` table. Distractor 1.960 must be present, with feedback that it makes the interval about 15 per cent too narrow.

## Practice seed

**Stem.** ResNet-50 has 5.25 per cent top-5 error on ImageNet's 50,000 validation images; ResNet-101 has 4.60 per cent. Compute each standard error and each 95 per cent Wald interval, say whether they overlap, and state exactly what may and may not be concluded.
**Hint.** Treat each image as a Bernoulli trial and use `sqrt(p(1-p)/n)`.
**Solution path.** `sqrt(0.0525 x 0.9475/50000) = 0.000997`, so `[5.05%, 5.45%]`; `sqrt(0.046 x 0.954/50000) = 0.000937`, so `[4.42%, 4.78%]`. They do not overlap.
**`.p-check`.** Non-overlap does imply a significant difference at this level, so the conclusion is available here. The reverse inference is not: had they overlapped, that would have established nothing. If you concluded "no difference" from an overlap on some other pair, that is the error this page exists to prevent.

## Code and dataset

`code/0166-confidence-intervals.py` against `datasets/sessions.csv` and `datasets/experiment.csv`, already on main from #57. Reference it; do not rewrite it.

## Sources

- Greenland et al. (2016), *European Journal of Epidemiology* 31, 337-350, misinterpretations 19 and 21, for what the 95 per cent attaches to and for the overlap asymmetry. `https://pmc.ncbi.nlm.nih.gov/articles/PMC4877414/`
- Morey, Hoekstra, Rouder, Lee and Wagenmakers (2016), *Psychonomic Bulletin & Review* 23, 103-123, for the Fundamental Confidence Fallacy by name. `https://pmc.ncbi.nlm.nih.gov/articles/PMC4742505/`
