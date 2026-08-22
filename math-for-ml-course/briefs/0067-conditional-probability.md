# M07-04 - Conditional probability

**Class:** core. **Rung:** foundation.

## The single tight idea

Conditioning does not change the world; it shrinks the sample space to the part where the condition holds and renormalises what is left.

## Prerequisites

| Page | What it supplies |
|---|---|
| M07-02 | events, the axioms |
| M07-03 | counting outcomes to get a probability |

## Beats, in order

1. **The definition.** `P(B | A) = P(AB) / P(A)` when `P(A) > 0`, and **undefined** when `P(A) = 0`. Hajek's engineering framing is the one to use: a routine handed `P(AB) = 0` and `P(A) = 0` "shouldn't simply return the value zero. Rather, your routine should generate an error message". A reader who has written a division guard already understands this.
2. **The picture, before the algebra.** Same numerator, smaller denominator. The bar is not division of the world, it is a change of what counts as everything.
3. **It can go up, down, or nowhere.** Show all three on `requests.csv`: `P(flagged)` is 0.003960 overall, `P(flagged | unverified)` is 0.010694, `P(flagged | verified)` is 0.001085, and `P(cache_hit | verified)` is 0.24893 against an unconditional 0.24928. Conditioning raised one, lowered another, and left a third alone.
4. **A conditional probability is a probability.** It satisfies all three axioms on the restricted space, so everything from M07-02 still works after you condition. One sentence, and it saves the reader re-learning the subject.
5. **The multiplication rule and the chain rule.** Rearranged, the definition is `P(AB) = P(A) P(B | A)`. Extended, it is the chain rule.
6. **The machine-learning section.** Every supervised model estimates a conditional. A decision-tree leaf is one by construction: the count of a class in the leaf over the count in the leaf. And the chain rule is not an analogy for an autoregressive language model, it is the definition of one: the model computes each factor and the joint is their product. Link out to `llm-papers-course` for the mechanism.
7. **Set up the next two pages.** `P(A | B)` and `P(B | A)` are different numbers. Show it now with the module's own data: `P(flagged | unverified) = 0.0107` while `P(unverified | flagged) = 0.8081`, a factor of 75. Do not explain it yet - M07-06 does.

## Proof

**Named theorem: the chain rule of conditional probability.**
`P(A1 A2 ... An) = P(A1) P(A2 | A1) P(A3 | A1 A2) ... P(An | A1 ... A(n-1))`.

*Assumed, in words:* every conditioning event has positive probability, so every factor is defined.

*Shape:* it is the definition of conditional probability applied `n - 1` times, and nothing else. The only care needed is bookkeeping about what is on the right of the bar.

*Steps.* For two events the definition rearranges directly to `P(A1 A2) = P(A1) P(A2 | A1)`. For three, apply that to the pair `(A1 A2)` and `A3`: `P(A1 A2 A3) = P(A1 A2) P(A3 | A1 A2)`, then substitute the two-event result for `P(A1 A2)`. Induction repeats the same substitution.

**The step that does the real work is treating `A1 A2` as a single event.** That is the whole trick: the two-event rule was never about two events, it was about one event and one more, and the chain rule is that observation used repeatedly.

*Honest note.* This says nothing about independence and needs none. The factorisation is always true. What independence later buys is that the conditions can be dropped, which is a different and much stronger claim.

## Planned figures

1. **Orientation, `flowchart LR`.** `M07-02 axioms` and `M07-03 counting` feed `THIS PAGE - conditioning`, which enables `independence`, `Bayes` and `every P(y given x) model`.
2. **`svg.chart` - the shrinking denominator.** Two panels of the same 25,000-row block. Left: all rows, the unverified band shaded `f-prob` and the flagged rows marked `m-alarm`, with `99 / 25,000` printed. Right: only the 7,481 unverified rows kept, `80` marked, with `80 / 7,481` printed. Same marks, different ground.
3. **`sequenceDiagram` - the chain rule as decoding.** A model emitting three tokens: `P(w1)`, then `P(w2 | w1)`, then `P(w3 | w1, w2)`, with a `Note over` saying the joint is the product. No semicolons in the note text.

## The worked example, eight parts

1. **Setting.** `requests.csv`. `A` is "the user is not verified", `B` is "the request is flagged".
2. **Symbolic.** `P(B | A) = P(AB) / P(A)`, gloss naming each piece as a proportion of the full 25,000.
3. **Picture first.** Figure 2 above.
4. **`ol.worked`.** `P(A) = 7,481 / 25,000 = 0.29924`. `P(AB) = 80 / 25,000 = 0.00320`. Divide: `0.00320 / 0.29924 = 0.010694`. Then the shortcut that shows what conditioning is: `80 / 7,481` is the same number in one step, because the 25,000 cancels.
5. **`keynum`.** All counts read from the file; every result derived here and plain.
6. **Sanity check.** The answer must exceed the unconditional 0.003960, because unverified users are the risky ones, and it must stay below 1.
7. **What changes if.** Condition on `verified` instead and the answer falls to 0.001085. The two conditionals sit either side of the unconditional rate, and they must, because the unconditional rate is their weighted average.
8. **Interpretation.** The 25,000 cancelling is the whole lesson: conditioning is not a new measurement, it is the old one read over a smaller population.

## Code and dataset

`code/0067-conditional-probability.py` against `datasets/requests.csv`.

Computes `P(flagged | not verified)` twice: once from the definition as a ratio of two proportions over the full frame, and once by filtering to the unverified rows and taking the mean, asserting they agree to 12 places. Then verifies the law of total probability numerically by recovering `P(flagged)` from the two conditionals and their weights. Then demonstrates the chain rule on three columns, computing the three-way joint directly and as a product of conditionals and asserting equality.

## Quiz seeds

1. **Misconception.** `P(flagged | unverified)` is 0.0107 and `P(unverified | flagged)` is 0.8081. What explains the gap? *Correct:* they are ratios over different denominators, one over unverified users and one over flagged requests. *Distractors:* one of them is miscalculated; the events are not independent; flagging is not deterministic. Each distractor is true or plausible and answers a different question.
2. What should a routine return for `P(B | A)` when `P(A) = 0`? *Correct:* an error, because the quantity is undefined.

## Practice seed

**Stem.** In `requests.csv` there are 6,232 cache hits and 17,519 verified users, and 4,361 rows are both. Find `P(cache_hit | verified_user)` and `P(verified_user | cache_hit)`. Then say why they differ even though the numerator is the same number.
**Hint.** Write both as a count over a count. The numerator is 4,361 in both cases. Look only at what changes.
**Solution.** `4,361 / 17,519 = 0.24893`; `4,361 / 6,232 = 0.69978`. They differ because the denominators differ: the same overlap is a small slice of a big group and a big slice of a small one.
**`.p-check`.** Both lie between 0 and 1, and each must be at least the joint proportion 0.1744, because a conditional divides by something no larger than 1.

## Sources

- Hajek, ECE 313, section 2.3, including Example 2.3.1.
- Goodfellow, Bengio, Courville, *Deep Learning*, ch 3.5 and eq 3.6.
