# 0007 Why machine learning lives in log space

| | |
|---|---|
| Module | M01 Foundations |
| Rung | `pill easy` |
| Class | core |
| Word budget | 1,400 to 1,600 prose words, excluding practice and quiz text |
| Source scout | `mlm-foundations-r2` L7 |

## One tight idea

Log space is where a product of ten thousand probabilities is still a number your computer can hold, and where the answer you wanted does not change.

## Prerequisites

`0006` for the product rule, `0005` for argmax, `0004` for monotonicity.

## Downstream

M07, M09 (maximum likelihood), M10 (log-sum-exp, cross-entropy).

## Boundaries: what this page must not teach

- **Not** probability. This page uses probabilities only as numbers between 0 and 1; M07 owns what they are.
- **Not** the log-sum-exp identity. It may say the identity exists and why, and point at a routine that implements it. **M10 derives it.**
- **Not** cross-entropy. M10 owns it, M09 owns its equivalence with likelihood.
- This is the densest page in M01 and the one most likely to need splitting. If it passes 1,600 prose words, split at beat 6.

## Beats, in order

1. Open with the failure, not the fix. A 200-word document, each word with probability 1e-4 under a naive model. The product is exactly `0.0` in float64, and the classifier can no longer tell one class from another because both score zero.
2. Why: the exponent range of a float64. Show the two thresholds as this course's own arithmetic, with the underflow and overflow limits computed rather than quoted.
3. The fix is one rule from `0006`: the log turns a product into a sum. Compute the same document's log-score and show it is an entirely ordinary number.
4. Why the swap is **legal**, which is a different question from why it is necessary. The log is strictly increasing, so by `0004` the argmax is untouched.
5. Make the two-reason structure explicit and put it in a `.callout.key`. **Legality is monotonicity. Necessity is floating point.** A reader who merges them cannot say what breaks when only one holds.
6. Show it in real library code rather than pseudocode: a naive Bayes implementation returning a log joint likelihood and normalising with a log-sum-exp routine. The library is doing exactly what this page teaches.
7. The one place a naive log still fails: taking a softmax first and a log second can produce minus infinity, which is why a fused cross-entropy takes raw logits and why calling softmax yourself first is a bug.
8. Hand off cleanly: the log-sum-exp identity and everything information-theoretic is M10's.

## Stated proof (D4)

No new theorem is proved here. The legality argument **is** `0004`'s monotone-argmax theorem, and this page must **cite it by number rather than restate it**. Say in one line which theorem is doing the work and where it was proved. A reader who cannot name the theorem behind a step they just accepted has been shown a trick rather than an argument.

## Figures

- **Orientation**, `flowchart`: *the product rule (`0006`) and monotonicity (`0004`)* -> **THIS PAGE: why every likelihood in the field is logged** -> *M09's log-likelihood, M10's cross-entropy* -> *(dotted) M01*.
- **`svg.chart`**, required: the running product against the running log-sum for the same 200 factors, on two panels in one `<figure>`. The first hits the floor and flatlines at zero; the second descends steadily. This is the page in one picture.
- **`svg.chart`**: the float64 exponent range as a number line with the underflow and overflow thresholds marked, and the 200-word document's product and log-product plotted on it.

## Worked example

200 words, each at probability 1e-4. Show the product underflowing to exactly zero, then the log-sum arriving at an ordinary negative number. Then take two documents with genuinely different scores and show that in the product both are zero and indistinguishable, while in log space they are cleanly ordered. **That indistinguishability is the bug**, and it is what makes this worth a page.

## Quiz seeds

1. **Misconception.** Why do we take logs of a likelihood? Distractors must include "because it makes the optimum easier to find" and "because it makes the numbers smaller" - both true-sounding, and both answering a different question than "what breaks without it".
2. **Mechanism.** Which is the legality argument and which is the necessity argument? Four options pairing monotonicity and floating point in both orders.

## Practice seed

**Stem.** A 50-token sequence, each token at probability 0.002. Compute the log-probability. Then say what the raw product would be in float64, and why comparing two such sequences by their raw products fails.
**Hint.** You never need the product itself. Take the log of the expression before evaluating anything.
**Solution path.** `50 x ln(0.002)`; then the raw product's exponent against the float64 floor; then the indistinguishability argument.
**`.p-check`.** A log-probability is always negative, and more tokens must make it more negative. If yours got closer to zero as the sequence grew, a sign is wrong.

## Code and dataset

`code/0007-why-ml-lives-in-log-space.py`, self-contained with NumPy. Scores two synthetic documents both ways: the naive product, which returns `0.0` for both and reports them as tied, and the log-sum, which orders them correctly. Asserts the naive comparison fails and the log comparison succeeds. **The failing assertion is the teaching**, so it is written as an explicit check rather than left implicit.

## Sources

- Goodfellow, Bengio and Courville, *Deep Learning*, section 4.1, on underflow, overflow and the log-softmax trap.
- A named library's naive Bayes log-likelihood implementation, linked.
- A named framework's fused cross-entropy documentation, for the raw-logits requirement.

## As built

Written by `mlm-foundations-r2` alongside this brief; where the shipped page departs from the plan above, this is what it does and why.

The brief's "indistinguishability is the bug" is the page's centre, and it is now **measured rather than asserted**: on 721 held-out tickets, 8 have both class scores underflow and cannot be decided, and 26 have exactly one underflow, so the decision is forced by a floating-point artefact and looks confident. The silent failure is more than three times the loud one, and the same model loses 1.11 points of accuracy to arithmetic alone.
The two failure modes are drawn as a `sequenceDiagram` using two real rows, tickets 731 and 359, rather than as a float64 number line.
