# M07-03 - Equally likely outcomes, and when that assumption is wrong

**Class:** core. **Rung:** foundation.

## The single tight idea

Counting outcomes and dividing is a probability model, not a definition, and it is only correct when something makes the outcomes genuinely symmetric.

## Prerequisites

| Page | What it supplies |
|---|---|
| M07-02 | the axioms, events, partitions |
| M01, counting | permutations, combinations, the multiplication principle |

## Beats, in order

1. **The formula, and the assumption hiding inside it.** When `Omega` is finite and every outcome is equally likely, `P(A) = |A| / |Omega|`. Every symbol named. The assumption is the second clause, and it is an input, not a fact.
2. **Where the symmetry comes from when it is real.** A fair die, a shuffled deck, a hash bucket, `random_state` in a train/test split. In each case a physical or algorithmic mechanism makes the outcomes interchangeable.
3. **Counting, borrowed from M01 and used here.** One sentence and a link for the combination; the page uses `C(n, k)` and does not re-derive it.
4. **With and without replacement.** Drawing a minibatch without replacement makes the draws dependent; with replacement makes them independent. This is the setup M07-10 needs when it names the binomial's two assumptions.
5. **The counterexample the module's own data supplies.** Assume the three routes are equally likely and every one of them is wrong: chat is 0.5972 against an assumed 0.3333, an error of 79 percent; rerank is 0.0996, an error of 70 percent. **Equally likely was not a neutral starting point, it was a false claim.**
6. **The trap, named.** "I have no information, so I will assume uniform" is a statement about the modeller and a claim about the world, and those are different things. A uniform prior is an assumption like any other, and this page's job is to make the reader feel that before M07-06 lets them choose one.
7. **The honest boundary.** Choosing a distribution when you genuinely know little is a real subject with real answers, and it is M10's, through maximum entropy. Name it and link.

## Proof

No named theorem. The counting formula is a modelling assumption plus arithmetic, and the page says so rather than dressing it as a result.

## Planned figures

1. **Orientation, `flowchart LR`.** `M07-02 the axioms` and `M01 counting` feed `THIS PAGE - equally likely, and when it is wrong`, which enables `the uniform distribution` and `every distribution that is not uniform`.
2. **`svg.chart` - assumed against actual.** Three paired bars for the routes: the assumed 0.3333 in `m-noise` beside the actual 0.5972, 0.3032, 0.0996 in `m-stat`, with the error printed over each pair. The figure is the argument.
3. **`flowchart TD` - is equally likely safe here?** A decision path: is `Omega` finite? Is there a mechanism forcing symmetry - a shuffle, a fair device, a hash? If yes, count. If no, the counts must be estimated, and that is M09.

## The worked example, eight parts

1. **Setting.** Draw one request at random from the 25,000 in `requests.csv`. Here the outcomes genuinely are equally likely, because the draw is what makes them so.
2. **Symbolic.** `P(A) = |A| / |Omega|`, gloss naming `|A|` as the count of rows where `A` holds and `|Omega|` as 25,000.
3. **Picture first.** Figure 2 above.
4. **`ol.worked`.** `P(rerank)` = 2,490 / 25,000 = 0.0996. Then the trap: `P(rerank)` if the three routes were assumed equally likely = 1/3 = 0.3333. The two differ by a factor of 3.3.
5. **`keynum`.** Counts are read from the file; both results are derived here and are plain.
6. **Sanity check.** The three route probabilities must sum to 1 under either model. They do - which is exactly why summing to 1 does not tell you the model is right.
7. **What changes if.** Draw two requests without replacement. `P(both rerank)` is `(2490/25000) x (2489/24999)` = 0.009917, not `0.0996` squared = 0.009920. The gap is tiny here and it is not zero, and it is the whole difference between the binomial and the hypergeometric.
8. **Interpretation.** The draw was uniform. The routes were not. Uniformity is a property of the sampling mechanism, never of the thing sampled.

## Code and dataset

`code/0122-equally-likely-outcomes.py` against `datasets/requests.csv`.

Computes `P(route = rerank)` twice: once by counting matching rows and dividing, and once with `value_counts(normalize=True)`, asserting they agree. Then draws 200,000 random rows with `default_rng`, confirms the empirical draw frequency matches the row proportions, and prints the assumed-uniform answer beside the true one so the 3.3-times error is on screen. Also computes with-and-without-replacement pair probabilities and prints the difference.

## Quiz seeds

1. **Misconception.** A colleague says "we have no information about which route a request will take, so each is equally likely". What is wrong? *Correct:* it is a claim about the routes, and the data says chat is six times rerank. *Distractors:* nothing, it is the correct default; the routes are not mutually exclusive; you need more than three outcomes for it to apply.
2. Drawing a minibatch **without** replacement makes the draws what? *Correct:* dependent, because each draw changes what is left.

## Practice seed

**Stem.** A hash function spreads 25,000 requests over 8 shards. Assuming it spreads them uniformly, what is the probability a given request lands in shard 3, and what is the expected number of requests there? Then name one real thing that would break the assumption.
**Hint.** The first two are one division and one multiplication. For the third, ask what the hash is computed from.
**Solution.** `1/8 = 0.125`; `25,000 / 8 = 3,125`. Breaks if the hash key is not uniformly distributed, for example hashing on `route` when 60 percent of traffic is chat, which sends 60 percent of requests to one shard.
**`.p-check`.** The eight shard probabilities must sum to 1, and 8 x 3,125 must be 25,000. If a shard count does not divide evenly the model is still fine; the counts are just not all equal.

## Sources

- Hajek, ECE 313, sections 1.3 and 1.4, calculating the size of sets and experiments with equally likely outcomes.
