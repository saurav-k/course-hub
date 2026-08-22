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

No new theorem. The page's one derivation is the median-to-rate relation it reuses, and it is worth showing because it takes three lines and is the hinge of the worked example.

For an exponential, `P(X > t) = e^(-lambda t)`. The median `m` is by definition the value with half the mass above it, so `e^(-lambda m) = 0.5`. Taking logs, `-lambda m = ln(0.5) = -ln 2`, so **`lambda = ln(2) / m`**. That the mean is instead `1/lambda` is the whole of the worked example: the two summaries pin down different rates.

## Planned figures

1. **Orientation, `mindmap`.** The module's own map, which is exactly what `widgets.md` names a mindmap for: a root with branches for `binary`, `one of k`, `counts`, `waits`, `bounded` and `all reals`, each carrying its distributions. This is the page's slice of the graph, drawn as a taxonomy rather than a chain, because the page indexes rather than develops.
2. **`flowchart TD` - the decision procedure.** Support, then mechanism, then distribution, with all eight leaves and the breaking assumption on each leaf edge.
3. **`svg.chart` - eight shapes, one convention.** A small-multiples row: eight thumbnails on a shared axis convention, each drawn at a stated parameter, each captioned with its one-word mechanism. The shape-recognition figure the reader keeps.
4. **`svg.chart` - the decision that flipped.** One exponential density fitted through the median and a second fitted through the mean, drawn on the same axes, with the region beyond 2,000 shaded on each and the two tail areas printed: 3.5 percent and 19.5 percent, against a `ref` line at the 5 percent policy threshold. One dataset, two curves, opposite sides of the line.

## The worked example, eight parts

1. **Setting.** Ten days of one user's daily spend, median Rs 415 and mean Rs 1,225 - the case the predecessor course built, reused here because it is the best worked modelling failure available and this module absorbs that course's probability content.
2. **Symbolic.** `f(x) = lambda e^(-lambda x)` with the gloss naming `x` as a day's spend in rupees and `lambda` as a rate per rupee, plus `P(X > t) = e^(-lambda t)`.
3. **Picture first.** Figure 4 above.
4. **`ol.worked`.** Fit through the median: `lambda = ln(2) / 415 = 0.693 / 415 = 0.001670`. Tail: `0.001670 x 2,000 = 3.3405`, so `P(X > 2,000) = e^(-3.3405) = 0.0354`, that is **3.5 percent, below the 5 percent policy line, approved**. Now fit through the mean, because for an exponential the mean is `1/lambda`: `lambda = 1 / 1,225 = 0.000816`. Tail: `0.000816 x 2,000 = 1.633`, so `P(X > 2,000) = e^(-1.633) = 0.1954`, that is **19.5 percent, refused**.
5. **`keynum`.** The median 415 and the mean 1,225 are quoted from the source case; both rates and both tails are derived here.
6. **Sanity check.** The mean-fitted rate must be the smaller of the two, because the mean of this sample exceeds its median, and a smaller rate means a fatter tail. It is, and the fatter tail is what refuses the loan.
7. **What changes if.** Apply question 1 honestly. An exponential puts its mode at zero and says days get steadily rarer as they get larger. The observed days bunch around Rs 400 with **nothing at all below Rs 350**. The support is right and the shape is wrong, so the family was chosen for tractability rather than for fit - which is a legitimate reason, and a different one.
8. **Interpretation.** Ten rows cannot identify a distribution family. The number that decided this loan was not in the data; it was in the choice of curve, and the honest deliverable is both answers with the assumption named, not one answer with the assumption hidden.

## Code and dataset

`code/M07-15-choosing-a-distribution.py` against `datasets/requests.csv`.

Rather than a single result, this program is the module's diagnostic kit, and its docstring says so. For each of five columns it prints the three questions answered: the observed support, a mechanism guess, and what is known. Then it runs the checks that distinguish the families: mean against variance for the count column, which is the Poisson diagnostic; the ratio of mean to standard deviation for `retries`, which distinguishes geometric from Poisson; the band occupancies for `latency_ms`, which is the normal check that fails; and the memorylessness ratio for the gaps, which is the exponential check that passes. Each check is computed from the definition and printed with the value the family predicts beside it, and the program asserts nothing, because the point is that the reader reads the comparison and decides.

It also reproduces the credit worked example end to end from the two summary numbers, printing 0.0354 and 0.1954, so the reader can change the median and see the decision flip.

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
- The credit case reuses the worked figures from `statistical-foundations-ml-course/lessons/0004-from-baseline-to-risk-the-exponential-model.html`, whose probability content this module absorbs. Both tail figures were recomputed here and match that page exactly.
