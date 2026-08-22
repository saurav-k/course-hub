# M07-02 - The axioms, and what a probability is a probability of

**Class:** core. **Rung:** foundation.

## The single tight idea

Everything in probability is derived from three rules about a set of outcomes, so the whole subject is only as good as the set you wrote down.

## Prerequisites

| Page | What it supplies |
|---|---|
| M07-01 | what a probability is |
| M01, sets | union, intersection, complement, the empty set, partition |

## Beats, in order

1. **The sample space.** `Omega` is the set of possible outcomes; an outcome is one element; **an event is a subset of `Omega`**. Build it on `route`: `Omega = {chat, embed, rerank}` and "not chat" is the subset `{embed, rerank}`.
2. **The event algebra in words before symbols.** `A union B` is "or", `AB` is "and", `A` complement is "not". Two events are **mutually exclusive** when `AB` is empty. A set of mutually exclusive events covering `Omega` is a **partition**.
3. **The three axioms**, stated as Hajek states them: `P(A) >= 0`; `P(A union B) = P(A) + P(B)` for mutually exclusive `A` and `B`, extending to a countable list; `P(Omega) = 1`.
4. **The consequences, each derived in one line.** `P(A complement) = 1 - P(A)`, `P(empty) = 0`, `P(A) <= 1`, `A` inside `B` implies `P(A) <= P(B)`, and **inclusion-exclusion**.
5. **The machine-learning section.** A classifier's label set is a sample space. A softmax output satisfies the axioms by construction: every entry is positive because `exp` is, and they sum to one because of the denominator. A multi-label sigmoid head does not: three sigmoid outputs of 0.9, 0.8 and 0.7 sum to 2.4, so axiom 3 fails. They are three Bernoullis on three sample spaces, and reading them as one distribution over labels is a real bug whose symptom is that `argmax` still works while every probability is wrong.
6. **The honest boundary.** Hajek also states three *event* axioms about which subsets may be events. Say in two sentences that they exist, that they matter only when `Omega` is uncountable, and that this is an engineering course. Do not develop them.

## Proof

**Named theorem: inclusion-exclusion.** `P(A union B) = P(A) + P(B) - P(AB)`.

*Assumed, in words:* only the three axioms, and that `A` and `B` are events.

*Shape of the argument:* axiom 2 only applies to pieces that do not overlap, so cut `A union B` into pieces that do not overlap, add them with axiom 2, then reassemble.

*Steps.* `A union B` is the union of three mutually exclusive sets: `A` without `B`, `B` without `A`, and `AB`. Axiom 2 gives `P(A union B) = P(A B-complement) + P(A-complement B) + P(AB)`. Now add and subtract `P(AB)` and regroup: `(P(A B-complement) + P(AB)) + (P(A-complement B) + P(AB)) - P(AB)`. Each bracket is itself an application of axiom 2, to `A` and to `B`. So the expression is `P(A) + P(B) - P(AB)`.

**The step that does the real work is the cut into three disjoint pieces.** Everything after it is arithmetic. The reason the theorem needs proving at all is that axiom 2 is silent about overlapping events, and the minus sign is the price of that silence.

*Also proved on this page, in one line each:* the complement rule, from `A` and `A` complement being a partition; and `P(empty) = 0` from the complement rule applied to `Omega`.

## Planned figures

1. **Orientation, `flowchart LR`.** `M07-01 what a probability is` and `M01 sets` feed `THIS PAGE - the three axioms`, which enables `conditioning`, `independence` and `every result in the module`.
2. **`svg.chart` - the Karnaugh partition.** A rectangle for `Omega` cut into the four cells `AB`, `A B-complement`, `A-complement B`, `A-complement B-complement`, with `A union B` outlined and `AB` hatched to show it sitting inside both outlines. This is the proof above, drawn.
3. **`svg.chart` - is it a distribution?** Two stacked bars. Left: the three `route` proportions 0.5972, 0.3032, 0.0996 stacked to exactly 1.0000, labelled "a probability measure". Right: three sigmoid outputs 0.9, 0.8, 0.7 stacked past a `ref` line at 1.0 to 2.4, labelled "three Bernoullis, not one distribution".

## The worked example, eight parts

1. **Setting.** The `route` column of `requests.csv`. Three outcomes, real counts: chat 14,930, embed 7,580, rerank 2,490.
2. **Symbolic.** `P(A) = |A| / |Omega|` will come on M07-03; here the probabilities are the observed proportions, and the `.gloss` says so.
3. **Picture first.** Figure 3 above.
4. **`ol.worked`.** Check axiom 1 on all three. Check axiom 3 by summing. Compute `P(not chat)` twice: once by adding embed and rerank, once by the complement rule, and get the same number both ways.
5. **`keynum`.** Counts read from the file are plain; they are derived here.
6. **Sanity check.** The three proportions must sum to 1.0000 exactly, because each was divided by the same total.
7. **What changes if.** Add a fourth route with zero traffic. The sample space grows, every probability is unchanged, and `P` of the new event is 0, which is allowed: axiom 1 says non-negative, not positive.
8. **Interpretation.** "Not chat" needed no new data. That is what an axiom buys: a number you did not have to measure.

## Code and dataset

`code/0065-the-axioms.py` against `datasets/requests.csv`.

Computes `P(A union B)` for `A = verified_user` and `B = cache_hit` twice: once by inclusion-exclusion from the three separate probabilities, and once by directly counting rows where either holds. Asserts they agree to 12 decimal places. Then checks the three axioms on the `route` distribution and prints each check. Then demonstrates the failure: sums three independent sigmoid-style columns and shows the total exceeding 1.

## Quiz seeds

1. **Misconception.** A multi-label head emits 0.9, 0.8 and 0.7 for three tags. Which axiom fails if you read those as a distribution over tags? *Correct:* the one saying the whole sample space has probability 1. *Distractors:* the non-negativity axiom; the additivity axiom; none, the head is fine. Feedback: non-negativity holds, additivity is not even in play because the tags are not mutually exclusive, and "fine" is true of the head and false of the reading.
2. `P(A) = 0.30`, `P(B) = 0.55`, `P(AB) = 0.22`. What is `P(A union B)`? *Correct:* 0.63.

## Practice seed

**Stem.** In `requests.csv`, `P(verified_user) = 0.7008` and `P(cache_hit) = 0.2493`, and 4,361 rows have both. Find `P(verified or cached)` and `P(neither)`. Then say which axiom you used for the second one.
**Hint.** The second number is the complement of the first. You do not need to count anything again.
**Solution.** `ol.worked`: 0.174440 as the joint proportion; 0.7008 + 0.2493 - 0.17444 = 0.7756; 1 - 0.7756 = 0.2244; the complement rule, which comes from axioms 2 and 3.
**`.p-check`.** Both answers sit between 0 and 1, and the first must be at least as large as 0.7008, because "verified or cached" contains "verified".

## Sources

- Hajek, ECE 313, section 1.2, the event and probability axioms and properties p.4 to p.8.
- Goodfellow, Bengio, Courville, *Deep Learning*, ch 3.3.1.
