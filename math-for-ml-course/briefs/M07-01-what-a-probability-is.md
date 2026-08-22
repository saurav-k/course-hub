# M07-01 - What a probability is, and the two ways to read one

**Class:** core. **Rung:** foundation.

## The single tight idea

A probability is a number that obeys the same three rules whichever story you tell about where it came from, and the only thing your problem decides is which story it can support.

## Prerequisites

| Page | What it supplies |
|---|---|
| Lesson 00 | the course's promise, and the softmax as a thing that outputs numbers summing to one |
| M01, set notation | the idea of a set and of membership |
| M01, functions | a rule that takes an input and returns an output |

Nothing in M07 precedes this page. It is the module's on-ramp.

## Beats, in order

1. **Two sentences that both say 70 percent.** "This route serves a cached response 70 percent of the time" and "I am 70 percent sure this particular request is abusive". The first has a long run you can count. The second does not: this request happens once.
2. **The frequentist reading.** A probability is the rate at which something occurs over repetitions. It is checkable, and checking it needs repetitions that actually happened.
3. **The Bayesian reading.** A probability is a degree of belief. Goodfellow, Bengio and Courville put it exactly: probability represents "a degree of belief, with 1 indicating absolute certainty".
4. **The point of the page: the mathematics does not care.** The same axioms govern both. DLB, section 3.1: "the only way to satisfy those properties is to treat Bayesian probabilities as behaving exactly the same as frequentist probabilities". So everything in the next fourteen pages is neutral between the two readings, and a reader never has to pick a side to do the work.
5. **Where it bites in machine learning.** A model that outputs 0.7 has produced a number. Whether that number is a rate is an empirical question about the model, not a fact about the arithmetic. Name calibration in one sentence and hand it to M09.
6. **The honest boundary.** Hajek's own stance, quoted: the notes "do not present or advocate any one comprehensive philosophy for the meaning and application of probability theory, but present the widely used axiomatic framework". This course does the same.

## Proof

No named theorem on this page. Nothing to prove.

## Planned figures

1. **Orientation, `flowchart LR`.** This page's slice of the prerequisite graph: `Lesson 00` and `M01 sets and functions` feed `THIS PAGE - what a probability is`, which enables `the axioms`, `conditioning` and `every distribution in the module`.
2. **`svg.chart` - the running rate.** Proportion of `cache_hit` over the first 1 to 2,000 rows of `requests.csv`, an `s-stat` trace, wandering hard for the first hundred rows and settling onto a `ref` line at the final 0.2493. Kills "a probability is visible in a small sample": the first fifty points are the whole argument.
3. **`quadrantChart` - which reading a question needs.** Five questions placed by repeatable-against-one-off and rate-claim-against-belief-claim: a cache hit on this route, this request being abusive, next quarter's traffic, the flagged rate in a finished log, this model beating the last one. Labels under 26 characters.

## The worked example, eight parts

1. **Setting.** The `cache_hit` column of `requests.csv`, first ten rows only, small enough to count by hand.
2. **Symbolic.** `P(A) = (number of times A happened) / (number of trials)`, with a `.gloss` naming `A` as an event, and the ratio as an estimate of a rate rather than the rate itself.
3. **Picture first.** Figure 2 goes above this.
4. **`ol.worked`.** Count the hits in the first ten rows. Divide by ten. Then the same over the first 100, then the first 2,000, then all 25,000, showing the estimate settling: the running value moves by tenths early and by thousandths late: 0.4000, then 0.2900, then 0.2530, then 0.2493.
5. **`keynum`.** The final 0.2493 is derived here, so plain. The designed 0.25 in the generator docstring is quoted, so `.keynum`.
6. **Sanity check.** The answer must lie between 0 and 1, and it must move less as `n` grows. If a later estimate jumps more than an earlier one, the arithmetic is wrong.
7. **What changes if.** Take the last ten rows instead of the first ten. The ten-row estimate changes a lot and the 25,000-row estimate does not move at all.
8. **Interpretation.** A rate estimated from ten rows is not a probability, it is a noisy guess at one. How noisy is exactly what M09 measures.

## Code and dataset

`code/M07-01-what-a-probability-is.py` against `datasets/requests.csv`.

Computes the running proportion of `cache_hit` two ways: once from the definition as a cumulative count divided by a cumulative trial number, in a loop over the first 200 rows so the reader sees the arithmetic; and once vectorised with `np.cumsum` over all 25,000. Asserts the two agree on the overlap. Prints the estimate at n = 10, 100, 1000, 25000 and the largest step between consecutive estimates in each decade, which is the convergence the page claims.

## Quiz seeds

1. **Misconception.** A model outputs 0.7 on one image. What would you have to collect to check whether that 0.7 is a rate? *Correct:* many examples the model scored near 0.7, and their true labels. *Distractors:* the model's training loss; the model's architecture; a second model's opinion. Feedback names each as a true thing answering a different question.
2. "There is a 60 percent chance the new checkpoint wins next month." Which reading does the sentence need, and why? *Correct:* Bayesian, because next month happens once.

## Practice seed

**Stem.** Using only the first twenty rows of `requests.csv`, estimate `P(verified_user)`. Then say, in one sentence, what would have to be true for that estimate to be a good guess at the rate over all 25,000 rows.
**Hint.** Count the `True` values and divide. The second half is not arithmetic - ask what the twenty rows would have to be a fair sample of.
**Solution.** `ol.worked`: count, divide, compare against the full-column 0.7008.
**`.p-check`.** The answer is between 0 and 1 and should land near 0.7. It is 0.80, which is a tenth above the full-column 0.7008 - and a twenty-row estimate can only ever move in steps of 0.05, so it could not have landed closer than 0.70 even if the sample had been perfect.

## Sources

- Goodfellow, Bengio, Courville, *Deep Learning*, ch 3.1. <https://www.deeplearningbook.org/contents/prob.html>
- Hajek, *Probability with Engineering Applications*, ECE 313, section 1.2. <https://courses.grainger.illinois.edu/ece313/fa2020/probabilityAug21.pdf>
