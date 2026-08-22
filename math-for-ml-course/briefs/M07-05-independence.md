# M07-05 - Independence, and conditional independence

**Class:** core. **Rung:** foundation.

## The single tight idea

Independence is one equation, `P(AB) = P(A)P(B)`; your story about the setup is a hypothesis that the equation holds, and "mutually exclusive" is its opposite rather than its cousin.

## Prerequisites

| Page | What it supplies |
|---|---|
| M07-04 | conditional probability, the multiplication rule |
| M07-02 | mutually exclusive, the axioms |

## Beats, in order

1. **The definition.** `A` is independent of `B` if `P(AB) = P(A)P(B)`. Symmetric in `A` and `B`, and it works even when `P(A) = 0`, which the `P(B|A) = P(B)` form does not.
2. **The reading that makes it mean something.** When `P(A) > 0` it is equivalent to `P(B|A) = P(B)`: learning `A` moves nothing.
3. **Mutually exclusive is not independent.** Proof below. This is the misconception the page exists to kill.
4. **Pairwise is not mutual.** The two-coin counterexample, worked. Then the general definition: `n` events are independent when the product rule holds for **every** subset of size 2 or more, not merely for the pairs.
5. **Conditional independence.** `P(AB | C) = P(A | C) P(B | C)` for every value of `C`. It neither implies nor is implied by independence, and the page states that plainly rather than letting the reader assume a relationship.
6. **The machine-learning section.** Naive Bayes assumes the features are conditionally independent given the class. In text that is nearly always false. The classifier is often useful anyway, because correlated evidence is multiplied rather than pooled, which wrecks the probabilities while frequently leaving the `argmax` right. Teach both halves; a course that teaches only "it works anyway" produces engineers who trust naive Bayes probabilities.
7. **Independence is what i.i.d. means**, and i.i.d. is what makes a train/test split mean anything. One sentence, forward link to M09.

## Proof

**Named result: two mutually exclusive events with positive probability are dependent.**

*Assumed:* `AB` is empty, `P(A) > 0` and `P(B) > 0`.

*Shape:* one line from each definition, then compare.

*Steps.* `AB` empty gives `P(AB) = P(empty) = 0` by property p.6. But `P(A)P(B)` is a product of two positive numbers, so it is positive. `0` is not positive, so `P(AB)` is not `P(A)P(B)`, and the events are not independent.

**The step that does the real work is noticing the two definitions talk about the same quantity, `P(AB)`,** and force it to two different values. And the direction matters: they are not merely dependent, they are as dependent as two events can be, because `P(B | A) = 0` - learning `A` tells you `B` certainly did not happen.

**Second, a disproof: pairwise independence does not imply independence.**
Flip two fair coins, so `Omega = {HH, HT, TH, TT}` with each outcome at 0.25. Let `A` be "first is heads", `B` be "second is heads", `C` be "the two faces match". Each has probability 0.5. Each pairwise intersection is a single outcome, so each is 0.25, which equals `0.5 x 0.5`: all three pairs are independent. But `ABC = {HH}`, so `P(ABC) = 0.25` while `P(A)P(B)P(C) = 0.125`. And `P(A | BC) = 1`. A single counterexample is a complete disproof, and this is why the definition for three events needs a fourth equation.

## Planned figures

1. **Orientation, `flowchart LR`.** `M07-04 conditioning` feeds `THIS PAGE - independence`, which enables `the binomial`, `the geometric`, `i.i.d. data` and `naive Bayes`.
2. **`svg.chart` - the four-cell disproof.** The two-coin sample space as four equal cells. Three overlay strips show `A`, `B` and `C` each covering two cells, each pair sharing exactly one, and all three sharing the single cell `HH`, with `0.25` printed against the `0.125` the product rule demands.
3. **`svg.chart` - one dependent pair and one independent pair, from the same file.** Two grouped bar pairs. Left: `P(cache_hit AND verified)` at 0.174440 beside the product 0.174685, visually identical, labelled independent. Right: `P(flagged AND verified)` at 0.000760 beside the product 0.002775, visibly different, labelled dependent. One dataset, both answers, no ambiguity about what the test looks like when it passes.
4. **`flowchart TD` - the decision path.** Do `A` and `B` share an outcome? No: mutually exclusive, therefore dependent unless one has probability zero. Yes: test the product rule, which may hold or not.

## The worked example, eight parts

1. **Setting.** `requests.csv`, two pairs of columns.
2. **Symbolic.** `P(AB) = P(A)P(B)` with the gloss naming each side as a proportion of the 25,000 rows.
3. **Picture first.** Figure 3 above.
4. **`ol.worked`.** Pair one: `P(cache_hit) = 0.24928`, `P(verified) = 0.70076`, product `0.174685`, observed joint `4,361 / 25,000 = 0.174440`, difference `0.000245`. Pair two: `P(flagged) = 0.003960`, product with `P(verified)` `= 0.002775`, observed joint `19 / 25,000 = 0.000760`, difference `0.002015`, which is 8 times the first difference on a quantity 200 times smaller.
5. **`keynum`.** Counts read from the file; every product and difference derived here.
6. **Sanity check.** A joint can never exceed either marginal. `0.174440` is below both `0.24928` and `0.70076`, and `0.000760` is below both.
7. **What changes if.** Compare the two differences as ratios instead of gaps: pair one is off by 0.14 percent of the product, pair two by 73 percent. On rare events the absolute gap is useless and only the ratio reads.
8. **Interpretation.** Neither difference is exactly zero, and the first one never will be on finite data. Deciding how close is close enough is a hypothesis test, and it is M09's.

## Code and dataset

`code/M07-05-independence.py` against `datasets/requests.csv`.

For each of the two pairs, computes the joint twice: once as `P(A) * P(B)` from the two marginals, and once by counting rows where both hold. Prints both with their absolute and relative gap, and asserts the independent pair agrees to within 0.001 while the dependent pair does not. Then builds the two-coin counterexample as an explicit four-row frame and checks all four independence equations, printing which three pass and which one fails.

## Quiz seeds

1. **Misconception.** Two events each have probability 0.4 and cannot both occur. Are they independent? *Correct:* no, and they are maximally dependent. *Distractors:* yes, because neither affects the other; yes, because they are disjoint; it cannot be determined from what is given.
2. Three events are pairwise independent. What else must hold for them to be independent? *Correct:* the product rule for all three at once.

## Practice seed

**Stem.** In `requests.csv`, `P(verified) = 0.70076` and `P(retries = 1) = 0.8480`, and 14,817 rows have both. Test whether the two are independent, and state your conclusion as a comparison of two numbers rather than as a yes or no.
**Hint.** You need the product of the marginals and the observed joint. Compare them as a ratio, not only as a gap.
**Solution.** Product `0.70076 x 0.8480 = 0.594244`; observed `14,817 / 25,000 = 0.592680`; gap `0.001564`, which is 0.26 percent of the product. Consistent with independence, and the generator did draw them independently.
**`.p-check`.** The joint must be below both marginals, and for an independent pair the gap should be of the order of sampling noise, roughly `1/sqrt(25,000)` = 0.006 at worst. A gap of 0.0016 is comfortably inside that, which is the point: independence on finite data never shows up as an exact zero.

## Sources

- Hajek, ECE 313, section 2.4.1: Definitions 2.4.1, 2.4.4, 2.4.6, 2.4.7 and Example 2.4.5.
- Goodfellow, Bengio, Courville, *Deep Learning*, ch 3.7, eqs 3.7 and 3.8.
- Manning, Raghavan and Schutze, *Introduction to Information Retrieval*, ch 13, for the naive Bayes assumption.
