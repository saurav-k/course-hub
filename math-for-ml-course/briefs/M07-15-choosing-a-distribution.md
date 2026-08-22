# M07-15 - Choosing a distribution: what each one assumes, and where it breaks

**Class:** core. **Rung:** working.

## The single tight idea

You choose a distribution by answering three questions about the quantity, not by looking at a histogram, and every choice is an assumption that can be wrong in a way that changes the answer.

## Prerequisites

Every page of M07. This is the module's closing page and it assumes all of it.

| Page | What it supplies |
|---|---|
| M07-10 | Bernoulli, binomial, categorical |
| M07-11 | uniform |
| M07-12 | geometric |
| M07-13 | Poisson, exponential |
| M07-14 | normal |

## Beats, in order

1. **Question 1: what is the support?** Binary; one of `k`; a count in `{0, 1, 2, ...}`; a non-negative duration; a bounded interval; all of the reals. This alone eliminates most of the list, and it is the question people skip.
2. **Question 2: what is the generating mechanism?** One trial; `n` independent trials; trials until the first success; events arriving at a constant rate; the gap between such events; a sum of many small independent contributions.
3. **Question 3: what do you actually know?** A rate; a mean; a range and nothing else; only a variance. The honest answer is sometimes "less than the distribution I was about to choose requires".
4. **The table.** All eight distributions on one screen: support, parameters, mean, variance, the mechanism that produces it, the ML home, and **the assumption that breaks it**. This is the page a reader returns to, so it must be complete and it must print.
5. **The eight assumptions, each stated as a failure.** Bernoulli: nothing, it is just a label. Binomial: needs independence and a constant `p`, and sampling without replacement breaks the first. Categorical: needs the states exhaustive and mutually exclusive, which multi-label problems are not. Uniform: claims the endpoints are as likely as the middle. Geometric and exponential: claim no memory, so wrong for anything that ages or warms up. Poisson: claims a constant rate and independent increments, so wrong for bursty or self-exciting traffic, and its mean-equals-variance is the check. Normal: claims light tails, and real serving metrics do not have them.
6. **The worked failure**, below: the same ten rows, two defensible summaries, opposite decisions.
7. **Fitting is not choosing.** Once the family is picked, estimating its parameters is M09's subject, and doing it well does not rescue a wrong family. One sentence and a link.
8. **What to do when you are unsure.** Pick the simplest family the support allows, state the assumption in the same paragraph as the answer, and compute what the answer would have been under the next-simplest family. If the two agree, the choice did not matter. **If they disagree, you have found the real result**, which is that the answer depends on an assumption rather than on the data.

## Proof

No new theorem. The page's one derivation is the median-to-rate relation for an exponential, worth three lines because it is the cheapest demonstration that two defensible summaries of the same data pin down two different members of one family.

For an exponential, `P(X > t) = e^(-lambda t)`. The median `m` is by definition the value with half the mass above it, so `e^(-lambda m) = 0.5`. Taking logs, `-lambda m = ln(0.5) = -ln 2`, so **`lambda = ln(2) / m`**. Fitting instead through the mean uses `lambda = 1/mean`, and unless the data happen to satisfy `mean = m / ln 2` those two rates differ.

## Planned figures

1. **Orientation, `mindmap`.** The module's own map, which is exactly what `widgets.md` names a mindmap for: a root with branches for `binary`, `one of k`, `counts`, `waits`, `bounded` and `all reals`, each carrying its distributions. This is the page's slice of the graph, drawn as a taxonomy rather than a chain, because the page indexes rather than develops.
2. **`flowchart TD` - the decision procedure.** Support, then mechanism, then distribution, with all eight leaves and the breaking assumption on each leaf edge.
3. **`svg.chart` - eight shapes, one convention.** A small-multiples row: eight thumbnails on a shared axis convention, each drawn at a stated parameter, each captioned with its one-word mechanism. The shape-recognition figure the reader keeps.
4. **`svg.chart` - two families, one dataset, three tails.** The observed one-second count histogram as `m-stat` bars, with the fitted Poisson as `s-prob` marks and the fitted normal as an `s-alarm` curve drawn continuous and visibly spilling below zero. The region beyond 6 is shaded and three numbers are printed in it: normal 0.30 percent, Poisson 0.93 percent, observed 1.15 percent.

## The worked example, eight parts

1. **Setting.** Capacity planning on the module's own file. Bin the 25,000 arrivals into 10,884 one-second windows and ask: if we provision for 6 concurrent requests a second, what overflow rate do we promise the service review?
2. **Symbolic.** Two candidate models side by side. Normal: `N(mu, sigma^2)` with `mu = 2.2967` and `sigma = 1.5293`. Poisson: `P(N = k) = lambda^k e^(-lambda) / k!` with `lambda = 2.2967`. Gloss naming `mu`, `sigma` and `lambda`, and saying that the Poisson has **one** parameter where the normal has two, because its mean and variance are the same number.
3. **Picture first.** Figure 4 above.
4. **`ol.worked`.** Question 1, support. Counts are non-negative integers. The normal is continuous and unbounded below, and at these parameters it puts `Phi((0 - 2.2967)/1.5293) = Phi(-1.5018) = 0.0666` - **6.66 percent of its mass on a negative number of requests.** That alone should end it, and usually nobody checks. Question 2, mechanism. Independent arrivals at a constant rate is exactly the Poisson process from M07-13. Question 3, the diagnostic. A Poisson forces variance to equal mean; observed variance is 2.3388 against a mean of 2.2967, a ratio of 1.018. Now price the decision both ways. Normal: `P(N > 6) = 1 - Phi((6.5 - 2.2967)/1.5293) = 0.0030`. Poisson: `1 - 0.9907 = 0.0093`. Observed in the file: 125 seconds of 10,884, which is `0.0115`.
5. **`keynum`.** `2.326` for the 99th percentile of the standard normal is a quoted constant; every fitted parameter, tail and count is derived here.
6. **Sanity check.** The two models must agree roughly on the middle and disagree in the tail, because that is what a family choice controls. They do: both put the 99th percentile at 6, and their overflow probabilities differ by a factor of three.
7. **What changes if.** Nothing about the decision - both families say provision 6. **What changes is the promise.** A team using the normal signs up to 0.30 percent overflow; the truth is 1.15 percent, which is **3.8 times worse** and breaches a 1 percent objective the normal said was comfortably met.
8. **Interpretation.** The family choice did not move the capacity number here, and it moved the number that goes in the service objective by nearly a factor of four. **A model can be wrong in a way that never shows up in the decision it was built for and shows up badly in the commitment made alongside it.** The Poisson was identifiable in advance from question 1, before any fitting.

## Code and dataset

`code/M07-15-choosing-a-distribution.py` against `datasets/requests.csv`.

Rather than a single result, this program is the module's diagnostic kit, and its docstring says so. For each of five columns it prints the three questions answered: the observed support, a mechanism guess, and what is known. Then it runs the checks that distinguish the families: mean against variance for the count column, which is the Poisson diagnostic; the ratio of mean to standard deviation for `retries`, which distinguishes geometric from Poisson; the band occupancies for `latency_ms`, which is the normal check that fails; and the memorylessness ratio for the gaps, which is the exponential check that passes. Each check is computed from the definition and printed with the value the family predicts beside it, and the program asserts nothing, because the point is that the reader reads the comparison and decides.

It also fits both candidate families to the one-second counts, prints the two overflow estimates against the observed 0.0115, and prints the normal's mass below zero, so the support argument is generated rather than typed.

## Quiz seeds

1. **Misconception.** You have count data with mean 12 and variance 47. Is the Poisson a reasonable model? *Correct:* no, a Poisson forces the variance to equal the mean, and 47 is nearly four times 12. *Distractors:* yes, counts are always Poisson; yes, provided the counts are non-negative integers; it cannot be judged without knowing the window.
2. A quantity is a non-negative duration and all you know is its mean. Which family does the procedure reach for, and what does that choice assume? *Correct:* the exponential, which assumes a constant hazard, so nothing that ages.

## Practice seed

**Stem.** For each of these, name the family and the one assumption that would break it: (a) whether a request is cached; (b) how many of 512 rows in a batch are flagged; (c) the seconds between two arrivals; (d) which of three routes a request takes; (e) the number of attempts before an upstream call succeeds.
**Hint.** Answer question 1 first for all five. Two of them share a support and are told apart only by question 2.
**Solution.** (a) Bernoulli; breaks if "cached" is not really binary, for example a partial cache hit. (b) Binomial; breaks if the rows are not independent or the flag rate varies across the batch. (c) Exponential; breaks if arrivals are bursty, so the rate is not constant. (d) Categorical; breaks if the routes are not exhaustive, for example when a request can be re-routed and counted twice. (e) Geometric; breaks if retries are not independent, which is exactly what a backoff policy or a cold cache makes them.
**`.p-check`.** Items (b) and (e) are both counts of trials and get different answers, which is the check that you used question 2 and not just question 1. If you gave them the same family, you stopped after the support.

## Sources

- Hajek, ECE 313, appendix 6.3, the two distribution tables.
- Goodfellow, Bengio, Courville, *Deep Learning*, ch 3.9.
- For a second, fully independent worked case of the same failure - one where the family choice does flip the decision - the sibling course develops a credit example in full at `statistical-foundations-ml-course/lessons/0004-from-baseline-to-risk-the-exponential-model.html`. Link to it one way from the "go deeper" section; that course is a separate live course and nothing here edits it.
