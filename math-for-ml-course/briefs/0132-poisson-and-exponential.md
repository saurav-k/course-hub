# M07-13 - Counting and gaps: Poisson and exponential are one process

**Class:** depth. **Rung:** working.

## The single tight idea

If events land independently at a constant average rate, the count in a window is Poisson and the gap between events is exponential: two distributions, one process, each the other's shadow.

## Prerequisites

| Page | What it supplies |
|---|---|
| M07-12 | memorylessness in discrete time, and waiting |
| M07-10 | the binomial, which the Poisson is a limit of |
| M07-09 | PDF and CDF |
| M05, integrals | integrating an exponential, and improper integrals |
| M01, e and logs | `e`, and the limit that defines it |

## Beats, in order

1. **Poisson(lambda).** `P(X = k) = lambda^k e^(-lambda) / k!` for `k >= 0`. Mean `lambda`, variance `lambda`, as table entries with a forward link to M08. **The mean equalling the variance is a diagnostic**: real count data that is over-dispersed is not Poisson, and this file's counts give 2.2967 against 2.3388, which is close enough to be consistent and not so close as to look staged.
2. **Poisson as the binomial limit.** Proved below. Then show it, rather than asserting it: the module's own minibatch numbers agree to four decimal places at `n = 256`.
3. **The Poisson process.** Two conditions: independent increments, and the count in `[s, t]` distributed as `Poi(lambda(t - s))`. Lambda is now a rate per unit time.
4. **Exponential(lambda).** `f(t) = lambda e^(-lambda t)` for `t >= 0`, CDF `1 - e^(-lambda t)`, tail `e^(-lambda t)`, mean `1/lambda`.
5. **The duality, which is the page.** A counting process is Poisson **if and only if** its inter-arrival times are independent and exponential with the same rate. Proved in one direction below.
6. **Memorylessness in continuous time**, proved below. Equivalent to a constant failure rate, which is why the exponential is the no-wear-out model and exactly why it is wrong for anything that ages.
7. **Two lambda traps, both real.** First, `lambda` is a rate per unit time in a process and a mean count in a window, and `Poi(lambda(t-s))` is what reconciles them. Second, `numpy.random.exponential` and `scipy.stats.expon` take **scale**, which is `1/lambda`, not `lambda`. Fit `lambda = 2.3` and sample with `exponential(2.3)` and every number is out by a factor of 5.3.
8. **The machine-learning section.** Request arrivals at an inference endpoint, which is the worked example. Count regression on event data. Time to failure of a node. And in generative modelling, the LDA paper's generative process opens "Choose N ~ Poisson(xi)" for document length, with the authors' own honest caveat that "the Poisson assumption is not critical to anything that follows" - a good model of how to state an assumption you have not earned.

## Proof

**Named theorem 1: the Poisson is the limit of the binomial.**
Fix `lambda > 0`. Let `X_n` be binomial with `n` trials and `p = lambda / n`. Then `P(X_n = k)` tends to `lambda^k e^(-lambda) / k!` as `n` grows, for each fixed `k`.

*Assumed, in words:* many trials, each individually rare, with the product of the two held fixed.

*Shape:* write the binomial PMF out, split it into three factors, and show each converges separately.

*Steps.* The binomial PMF at `k` is `[n(n-1)...(n-k+1) / k!] (lambda/n)^k (1 - lambda/n)^(n-k)`. Regroup as three pieces:
`[n(n-1)...(n-k+1) / n^k]` times `[lambda^k / k!]` times `[(1 - lambda/n)^n]` times `[(1 - lambda/n)^(-k)]`.
The first bracket is a product of `k` factors each tending to 1, so it tends to 1. The second does not depend on `n`. The fourth tends to 1 because `k` is fixed and `lambda/n` tends to 0. **The third bracket is the one that does the real work, and it tends to `e^(-lambda)`** - it is the defining limit of the exponential function, taken from M01. Multiplying the four limits gives the Poisson PMF.

*Honest boundary.* This is convergence for each fixed `k`, which is what the page needs and what the approximation is used for. Uniformity of the approximation over all `k` at once is a stronger statement and this course does not prove it.

**Named theorem 2: a Poisson process has exponential inter-arrival times.**
If `N` is a Poisson process with rate `lambda`, the time `T` to the first arrival is `Exponential(lambda)`.

*Steps.* `T > t` says exactly that no arrival has happened by time `t`, which is the event `{N_t = 0}`. By the definition of a Poisson process `N_t` is `Poi(lambda t)`, so `P(N_t = 0) = e^(-lambda t) (lambda t)^0 / 0! = e^(-lambda t)`. So `P(T > t) = e^(-lambda t)`, and therefore `P(T <= t) = 1 - e^(-lambda t)`, which is the exponential CDF. Independence of the successive gaps follows from independent increments.

**The step that does the real work is the translation `{T > t} = {N_t = 0}`**, which turns a question about a waiting time into a question about a count. That single sentence is the whole duality, and everything else on this page follows from it.

*The converse* - that exponential independent gaps produce a Poisson process - is also true and is what Hajek's Proposition 3.5.2 states as an equivalence. The page states it and does not prove it, naming the extra work required.

**Named theorem 3: memorylessness of the exponential.** `P(T > s + t | T > s) = P(T > t)`.

*Steps.* By the definition of conditional probability, and because `T > s+t` contains `T > s`, the left side is `P(T > s+t) / P(T > s)`, which is `e^(-lambda(s+t)) / e^(-lambda s) = e^(-lambda t)`.

**The step that does the real work is that the exponential turns a subtraction in the exponent into a division**, which is the only property used. Hajek notes the converse too: any non-negative random variable with this property is exponential.

## Planned figures

1. **Orientation, `flowchart LR`.** `M07-12 waiting` and `M07-10 the binomial` feed `THIS PAGE - one process, two distributions`, which enables `load modelling`, `count regression` and `time-to-failure`.
2. **`svg.chart` - the keystone.** A horizontal timeline strip carrying real arrival ticks from the first 20 seconds of `requests.csv`. Above it, per-second counts as `m-prob` bars, captioned Poisson. Below it, the same gaps as an `m-stat` histogram, captioned exponential. **One dataset, two readings**, and the figure is the argument for the whole page.
3. **`svg.chart` - the limit, measured.** Binomial(256, 0.00396) bars overlaid with Poisson(1.0138) dots at `k` = 0 to 3: 0.36212 against 0.36285, 0.36856 against 0.36784, 0.18683 against 0.18645, 0.06289 against 0.06301. The approximation is invisible at this scale, and the page says by how much rather than that it is good.
4. **`svg.chart` - counts against theory.** The 10,884 one-second windows of the real file as `m-stat` bars at `k` = 0 to 8, with `Poi(2.2967)` drawn over them as `s-prob` marks: 0.1016 against 0.1006, 0.2296 against 0.2310, 0.2705 against 0.2653, and so on.
5. **`sequenceDiagram` - independent increments.** Three clients and an endpoint over one window, with a `Note over` stating that the next gap does not consult the last. No semicolons anywhere in the note text.

## The worked example, eight parts

1. **Setting.** The `arrival_s` column of `requests.csv`: 25,000 requests over 10,884.5 seconds, generated as a Poisson process at 2.3 per second.
2. **Symbolic.** The Poisson PMF and the exponential tail together, with one gloss naming `lambda` twice - once as a rate per second and once as the mean count in a one-second window - because that double meaning is the trap.
3. **Picture first.** Figure 2 above.
4. **`ol.worked`.** Estimate the rate two ways. From the gaps: mean gap `0.43538` s, so `lambda = 1 / 0.43538 = 2.2969` per second. From the counts: `25,000 / 10,884` windows `= 2.2967` per second. **The same number from a duration and from a count.** Then `P(N = 0` in one second`) = e^(-2.2967) = 0.1006`, against an observed 0.1016. Then `P(gap > 1 s) = e^(-2.2969) = 0.1006`, against an observed 0.09928.
5. **`keynum`.** `2.3` is quoted from the generator's docstring; both estimates and every exponential are derived here.
6. **Sanity check.** The two rate estimates must agree, because they are the same parameter measured through two different windows onto the same process. They agree to three decimals. If they disagreed, the arrivals would not be a Poisson process.
7. **What changes if.** Widen the window to five seconds. The count becomes `Poi(11.48)`, `P(N = 0)` collapses from 0.1006 to 0.00001, and the distribution becomes almost symmetric. **The Poisson changes shape with the window, and the exponential gaps do not change at all.**
8. **Interpretation.** At 2.3 per second the mean says one replica at 200 ms is enough. But `P(N >= 5)` in a second is 0.0834 by theory and 0.0858 in the file, so about one second in twelve carries a burst one replica cannot clear. Size for the tail of the count distribution, never for its mean.

## Code and dataset

`code/0132-poisson-and-exponential.py` against `datasets/requests.csv`.

Estimates the rate twice, from the mean gap and from the count per window, and asserts the two agree to two decimals. Computes the Poisson PMF from the definition with an explicit factorial and again by a stable recurrence, asserting agreement. Bins the arrivals into one-second windows and prints the empirical count distribution beside the theoretical one. Then tests memorylessness on the real gaps by conditioning and prints the pairs the page quotes. Finally it demonstrates the scale trap: samples with `rng.exponential(scale=1/lam)` and with `rng.exponential(scale=lam)` and prints both sample means so the factor of 5.3 is on screen.

## Quiz seeds

1. **Misconception.** You fitted `lambda = 2.3` arrivals per second and want samples of the gaps. What do you pass to `numpy.random.exponential`? *Correct:* 0.435, the scale, because the argument is a mean and not a rate. *Distractors:* 2.3, the rate you fitted; 1.0, then multiply after; 5.29, the rate squared.
2. Requests arrive as a Poisson process at 2.3 per second. What is the distribution of the gap between consecutive arrivals? *Correct:* exponential with the same rate, mean 0.435 seconds.

## Practice seed

**Stem.** A GPU node fails on average once every 90 days, modelled as a Poisson process. Find the probability it survives 30 days, the probability of two or more failures in a 180-day period, and the probability it survives a further 30 days given it has already run 60.
**Hint.** The first and third are exponential tail questions, the second is a Poisson count question. Choose the window before you choose the distribution.
**Solution.** Rate `1/90` per day. Survive 30 days: `e^(-30/90) = e^(-0.3333) = 0.7165`. In 180 days the count is `Poi(2)`, so `P(N >= 2) = 1 - e^(-2)(1 + 2) = 1 - 0.4060 = 0.5940`. Survive a further 30 given 60 already: `0.7165` again, by memorylessness.
**`.p-check`.** The first and third answers must be identical, and if they are not you have used the elapsed 60 days somewhere, which is exactly what memorylessness forbids.

## Sources

- Hajek, ECE 313, sections 2.7, 3.4, 3.5.2 including Definition 3.5.1 and Proposition 3.5.2, and appendix 6.3.
- Blei, Ng and Jordan, "Latent Dirichlet Allocation", JMLR 3 (2003), section 3. <https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf>
