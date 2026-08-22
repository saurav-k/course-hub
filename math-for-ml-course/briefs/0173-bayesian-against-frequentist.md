# 0173 Bayesian against frequentist

| | |
|---|---|
| Module | M09 Estimation, testing, and inference |
| Rung | `pill hard` |
| Class | core |
| Word budget | 1,100 to 1,400 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S17 |

## One tight idea

The two schools disagree about what is random, and almost every confusion in this module is a sentence from one being read in the other's grammar.

## Prerequisites

`0125` for Bayes' theorem, `0165` for MAP, `0166` for the confidence interval, `0168` for what a p-value is not.

## Downstream

The last page of M09. It closes the module and hands the reader to M10 and to the capstone.

## Boundaries: what this page must not teach

- **Not a computational course.** No MCMC, no variational inference. Sampling appears only as the way the page gets posterior quantiles without scipy.
- **Not conjugate-prior tables.** One conjugate pair, derived, because it is the one the module's running example needs.
- **Not advocacy.** The page does not pick a winner. It says what each grammar licenses and where they meet.
- Name no camp and no person. D16.

## Beats, in order

1. State the disagreement precisely and early, because it is the whole page: **frequentist**, the parameter is a fixed unknown and the data is random, so probability attaches to procedures; **Bayesian**, the data is what it is and the parameter carries a distribution, so probability attaches to the parameter.
2. Reread `0166`'s confidence interval in that light. The 95 per cent was always about the rule, and now the reader can see which grammar forced that.
3. **The credible interval**, and the sentence it is allowed to say: there is a 95 per cent probability that `p` lies here, given the model and the prior. That is the sentence everyone wanted on `0166`, and it costs a prior.
4. Conjugacy, derived once: a Beta prior and a Bernoulli likelihood give a Beta posterior. Two lines of algebra and the reader can compute a posterior by hand.
5. **The prior as a count.** The posterior mean is a weighted average of the prior mean and the sample proportion, and the prior acts exactly like `a + b` extra observations. That is the honest way to describe a prior's strength: not "belief" in the abstract, but a number of imaginary rows.
6. **Where they meet.** MAP with a flat prior is the MLE, and with plenty of data the likelihood dominates so the two intervals nearly coincide. The disagreement is loudest exactly where the data is thinnest, which is where it matters most.
7. **Two honest limits, both ways.** A flat prior is a choice and is not preserved under reparameterisation: uniform on `p` is not uniform on log-odds. And neither framework checks your model: model checking sits outside both formalisms and is usually what decides whether the number meant anything.
8. Close by placing the module's own objects on the map: p-value and confidence interval on one side, MAP and credible interval on the other, MLE on the seam.

## Named theorems and their stated proofs (D4)

**Theorem 1 (Beta-Bernoulli conjugacy).** If `p ~ Beta(a, b)` a priori and `k` successes are observed in `n` independent trials, then `p | data ~ Beta(a + k, b + n - k)`.
**Proof.** The posterior is proportional to likelihood times prior: `p^k (1-p)^(n-k) . p^(a-1) (1-p)^(b-1) = p^(a+k-1) (1-p)^(b+n-k-1)`, which is the `Beta(a + k, b + n - k)` kernel. A density is determined by its kernel together with the requirement that it integrate to one, so that is the posterior. []

**Corollary (the prior is a count).** The posterior mean is `(a + k)/(a + b + n)`, which is the weighted average of the prior mean `a/(a+b)` and the sample proportion `k/n` with weights `a + b` and `n`. So a prior's strength is measurable in observations.

**Theorem 2 (MAP under a flat prior is the MLE).** If `p(theta)` is constant on the parameter space then `argmax [log L(theta) + log p(theta)] = argmax log L(theta)`.
**Proof.** `log p(theta)` is an additive constant in `theta`, and adding a constant cannot move a maximum. []

**The honest boundary.** Theorem 2 is where the two schools touch, and it is often over-read as showing they agree. They agree on a *point*, under a flat prior, with plenty of data. They do not agree on what that point means, and the page's whole job is that they never did.

## Figures

- **Orientation**, `quadrantChart`: the module's own objects placed on *is the parameter random* against *does it require a prior*: p-value, confidence interval, MLE, MAP, posterior, credible interval. Kills: the two schools as attitudes rather than as claims about what is random.
- **`svg.chart`**, required: a 95 per cent confidence interval and a 95 per cent credible interval for the same data drawn one above the other, near-identical, annotated with the two different sentences each is allowed to say. Kills: "they always disagree", and sets up the point that the sentences differ even when the numbers do not.
- **`svg.chart`**: posterior densities under a flat, a weak and a strong prior at `n = 10` and again at `n = 1000`, converging in the second panel. Kills: "the prior's influence is permanent".
- **`svg.chart`**: two "uninformative" priors, uniform on `p` and uniform on log-odds transformed back to `p`, plotted together and visibly different. Kills: "flat means no assumption".

## Worked example

`experiment.csv`'s control arm, `596` conversions in `12,000`, done both ways. The Wald interval from `0166`, then a `Beta(1,1)` prior giving a `Beta(597, 11405)` posterior, with its 95 per cent credible interval taken by sampling. The two agree to within a small fraction of a percentage point, and the page says exactly why: a flat prior and 12,000 observations. Then a table of four priors, from flat to a firm and deliberately wrong one, with each one's implied extra-observation count beside the posterior mean it produces, so the reader can watch a prior worth 400 imaginary rows barely move an answer built on 12,000 real ones.

Then the divergence: at `0` successes in `40`, the Wald interval collapses to `[0, 0]` while the Bayesian interval stays open and says the rate is somewhere below about 9 per cent. The schools agree when data is plentiful and disagree exactly where the answer is hard.

## Quiz seeds

1. **Misconception.** What is random in the frequentist picture? Answer: the data, not the parameter. Distractor "the unknown parameter" describes the Bayesian picture and is where the module's confusions come from.
2. **Mechanism.** When do the two intervals nearly coincide? Answer: with a flat prior and plenty of data. Distractors: whenever the prior is strong, which is when they diverge; whenever the sample is small, likewise.

## Practice seed

**Stem.** 300 conversions in 1,000. Compute the 95 per cent Wald interval. Then with a `Beta(1,1)` prior, name the posterior and state its mean. Its 95 per cent credible interval is `[27.24%, 32.91%]`. Compare, and explain both the closeness and the difference in what the two sentences claim.
**Hint.** The posterior parameters are the prior's plus the successes and the failures.
**Solution path.** `se = sqrt(0.3 x 0.7/1000) = 0.01449`, so `0.30 +/- 0.0284 = [27.16%, 32.84%]`. The posterior is `Beta(301, 701)` with mean `301/1002 = 30.04%`. The intervals agree to within about 0.08 percentage points because the prior is flat and 1,000 observations swamp it. The claims differ entirely: the credible interval says `p` is in that range with probability 0.95 given the model and the prior; the confidence interval says the procedure that produced it covers `p` 95 per cent of the time.
**`.p-check`.** The posterior mean must sit between the prior mean of 0.5 and the sample proportion of 0.30, and much closer to the second. If it landed outside that range, the successes and failures were swapped in the update.

## Code and dataset

`code/0173-bayesian-against-frequentist.py` against `datasets/experiment.csv` and `datasets/sessions.csv`. **The program exists on main but under the wrong number**: #57 landed it as `code/0171-bayesian-against-frequentist.py`, before the roadmap order was known. The crew writing this page renames it to `0173-bayesian-against-frequentist.py`; `0171` belongs to cross-validation. No content change is needed and no page has ever been published under either number, so no public URL moves.

## Sources

- Gelman and Shalizi (2013), *British Journal of Mathematical and Statistical Psychology* 66, 8-38, for model checking sitting outside the Bayesian updating formalism.
