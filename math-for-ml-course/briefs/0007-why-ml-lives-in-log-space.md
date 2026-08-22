# 0007 - Why machine learning lives in log space

| | |
|---|---|
| Module | M01 Foundations |
| Rung | foundation (`pill easy`) |
| Partition | core |
| Prose budget | 1,400 to 1,600 words (the densest page in the module) |
| Prerequisites | `0006` (the product rule), `0005` (argmax), `0004` (the monotone theorem) |
| Needed by | M07, M09 (MLE), M10 (log-sum-exp, cross-entropy) |
| Code | `code/0007-why-ml-lives-in-log-space.py` |
| Dataset | `datasets/tickets.csv` |
| Named theorem | **legality of the log-likelihood swap**, as a corollary of `0004`. Proved (D4). |

## Boundary

M07 owns probability itself; this page uses probabilities only as numbers between 0 and 1.
**M10 owns the log-sum-exp identity.** This page may name a `logsumexp` routine and point at one; it does not derive the identity.

## The one idea

Log space is where a product of ten thousand probabilities is still a number your computer can hold, and where the answer you wanted does not change.

## Beats, in order

1. Open with the failure, not the fix. A long support ticket, each token with a small probability under a class model. The product is `0.0` in float64 and the classifier now cannot tell the two classes apart, because both scored zero.
2. Why: float64 underflows to zero below an exponent of about `-746` and `exp` overflows above `709.78`. Cite Deep Learning Book section 4.1 and show the two thresholds as this course's own arithmetic.
3. The fix is one rule from `0006`. `log` turns `Prod` into `Sum`, and a sum of a few hundred numbers near `-9` is an entirely ordinary number.
4. Why the swap is **legal**, which is a different question from why it is necessary. State the corollary and prove it in one line from `0004`.
5. Make the two-reason structure explicit in a `.callout.key`. Legality is monotonicity. Necessity is floating point. A reader who merges them cannot say what breaks when only one holds.
6. Show it in real code, not pseudocode: scikit-learn's `_joint_log_likelihood` is documented as returning "log P(c) + log P(x given c)", and `predict_log_proba` normalises it with `logsumexp`. The library does exactly what this page teaches.
7. The one place a naive log still fails. Deep Learning Book section 4.1: computing `log(softmax(x))` by running softmax first "could erroneously obtain minus infinity". This is why PyTorch's `CrossEntropyLoss` takes raw logits and is "equivalent to applying LogSoftmax on an input, followed by NLLLoss", and why calling softmax yourself first is a bug.
8. Hand off cleanly: the log-sum-exp identity and everything information-theoretic is M10's.

## The proof (D4)

**Corollary (legality of the log-likelihood swap).** For a likelihood `L(theta) > 0`, `argmax_theta L(theta) = argmax_theta ln L(theta)`.

*Proof.* `ln` is strictly increasing on `(0, infinity)`: if `0 < a < b` then `ln b - ln a = ln(b/a)` by the quotient rule of `0006`, and `b/a > 1` gives `ln(b/a) > 0`. So `ln` satisfies the hypothesis of the monotone-transform theorem of `0004` with `g = ln`, and the conclusion `argmax f = argmax(g . f)` applies directly with `f = L`.

**The step that does the real work** is not in this proof at all: it is `0004`'s converse direction, which is where strictness was needed. This page's contribution is only to check the hypothesis, and saying so out loud is the point. A reader who can see that a two-line corollary is standing on a page-old theorem has learned how mathematics is actually assembled.

**Honest boundary, and it matters.** The corollary says the **location** of the maximum is preserved. It says nothing about the value: `ln L` is not `L`, and a likelihood ratio is not a log-likelihood ratio. It also says nothing about whether either quantity is computable, which is the entirely separate floating-point problem this page opened with. Legality without necessity would leave you free to work in log space; necessity without legality would leave you obliged to and wrong to. You need both, and they come from different places.

## Figures (4, at least one `svg.chart`)

- **F1 orientation, `flowchart LR`.** "Log rules (0006) and monotonicity (0004)" to "THIS PAGE: work in log space" to "MLE (M09), cross-entropy and log-sum-exp (M10)".
- **F2 inline `svg.chart`, the page's centrepiece.** Two series against the number of tokens multiplied. The running **product** on a log-y axis falls linearly and then hits a `ref` line marked "float64 floor" and drops to zero. The running **log-sum** falls linearly forever. Kills: that underflow is a rare edge case; the cliff arrives at a document length the dataset actually contains.
- **F3 `sequenceDiagram`.** Two paths side by side: the naive multiply returning `0.0` for both classes and a tie the classifier cannot break, against the log path returning two distinct finite numbers. **No semicolon anywhere in the message text.**
- **F4 `flowchart LR`.** Two independent inputs converging: "log is strictly increasing" to "the swap is **legal**", and "float64 underflows" to "the swap is **necessary**", both arriving at "work in log space".

## Worked example (eight parts)

A 200-token ticket, each token about `1e-4` under the class model.
Naive: `(1e-4)^200 = 0.0`. In log space: `200 x ln(1e-4) = -1842.07`, an ordinary number.
Then open the library: scikit-learn's `GaussianNB._joint_log_likelihood` is `log(prior) - 0.5 * sum(log(2 pi var)) - 0.5 * sum((x - mean)^2 / var)`, and every `+` in it is a `x` that a log turned into a `+`.

- **Sanity check.** The log score must be negative, since every probability is below 1, and `-1842` is about `200 x -9.2`.
- **What changes if** the ticket is 3 tokens instead of 200: the naive product is about `3.0e-7` and survives, which is exactly why a short example hides the bug.

## Code

`code/0007-why-ml-lives-in-log-space.py`.
Fits a Laplace-smoothed naive Bayes on the `train` rows of `tickets.csv` and scores the `test` rows **twice**, naively and in log space.
It reports the three populations that matter and asserts the log path has no non-finite value:

- documents where **both** class scores underflow to `0.0`, so the classifier cannot decide at all;
- documents where **exactly one** underflows, so the decision is forced by a floating-point artefact rather than by evidence, which is the silent and more common failure;
- the accuracy of the log-space classifier, and the token counts of the shortest document that underflows and the longest that survives, which shows the cliff is not a single length.

## Quizzes

- **Q1** (misconception): why is maximising the log-likelihood instead of the likelihood **legal**?
  `Because logs prevent underflow` / `Because log is strictly increasing` / `Because the product becomes a sum` / `Because the values are unchanged`
  Feedback: options 1 and 3 are both true and are reasons it is **useful**, not reasons it is **allowed**; keeping the two apart is the point of this page. Option 4 is false, the values change a great deal and only the location of the maximum does not.
- **Q2** (misconception): you call `softmax`, then take `log` of the result. What can go wrong?
  `Nothing, the two are inverses` / `The exponentials always overflow` / `The output stops summing to one` / `A tiny probability logs to minus infinity`
  Feedback: option 1 is false, they are not inverses; option 2 says "always", and a stabilised softmax overflows never; option 3 is false, softmax always sums to one. Option 4 is the Deep Learning Book's "one small problem" and is why PyTorch ships `LogSoftmax`.

## Practice

Priors `P(urgent) = 0.3`, `P(normal) = 0.7`. A three-token ticket with `P(token given urgent) = 0.01, 0.02, 0.005` and `P(token given normal) = 0.001, 0.004, 0.002`.
(a) Compute the joint log likelihood of each class. (b) Which wins, and by how much on the log scale? (c) Turn the two log scores into posterior probabilities. (d) The naive products here are `3.0e-7` and `5.6e-9`, both representable. So why bother with logs?

- **Hint.** For (c), you cannot exponentiate and divide without losing the point; subtract the larger log score from both before exponentiating.
- **Solution.** (a) add the log prior to the three log likelihoods: urgent gives `-1.204 - 4.605 - 3.912 - 5.298 = -15.019`; normal gives `-0.357 - 6.908 - 5.521 - 6.215 = -19.001`. (b) urgent, by `3.981` on the log scale, a factor of `e^3.981 = 53.6` in probability. (c) `logsumexp = -15.019 + ln(1 + e^-3.981) = -15.001`; subtracting and exponentiating gives `0.982` and `0.018`. (d) because three tokens is not a ticket. At 200 tokens the same arithmetic underflows to `0.0` and both classes tie at zero. This small case exists so you can check the log answer against a product you can still see.
- **`.p-check`.** The two posteriors must sum to 1, and the winner on the log scale must be the winner after exponentiating: if it flipped, you subtracted in the wrong direction.

## Primary sources to go deeper

Goodfellow, Bengio and Courville, *Deep Learning*, section 4.1, `https://www.deeplearningbook.org/contents/numerical.html`.
