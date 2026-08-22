# 0105 - Entropy: how surprised you should expect to be

**Module** M10 Information, similarity, and dimension - lesson 01
**Rung** working  **Class** core  **Number** PROVISIONAL, see `briefs/README.md`

## The single tight idea

Entropy is the average of `-log p`, which is the average number of yes/no questions you must
ask to learn the outcome, and every other quantity in this module is that one number rearranged.

## Prerequisites

- M01, logs and exponentials, and specifically that `log` turns a product into a sum. M01 owns
  the arithmetic case for log space; this page owns the information reading.
- M07, PMF over a discrete random variable.
- M08, expectation as a weighted average. It is the only operation on this page.

## Beats, in order

1. **One-minute version.** Surprise is `-log p`. Entropy is its expectation. Base 2 gives bits.
   A certainty scores zero and the uniform distribution scores the maximum, `log n`.
2. **Orientation figure**, before any section. Where M10 sits: probability gave you
   distributions and statistics gave you likelihoods, this page gives one number that scores a
   distribution, and that number becomes every loss, split criterion and model metric that follows.
3. **Mental model before any formula: a code.** You must send one symbol from an alphabet down a
   wire. Frequent symbols get short codes. The average code length is the quantity. Draw the code
   tree first.
4. **Mechanism.** `I(x) = -log2 p(x)`, then `H(p) = E[-log2 p(x)] = -sum p_i log2 p_i`. Gloss
   every symbol. State the `0 log 0 = 0` convention and say it is licensed by
   `lim x log x = 0 as x -> 0`, not chosen for convenience.
5. **Why `-log` and nothing else.** Shannon's three requirements, in his words: `H` continuous in
   the `p_i`; for equally likely outcomes `H` increasing in `n`; and the grouping property, that a
   choice broken into two successive choices must give the weighted sum. **Named theorem: Shannon's
   Theorem 2.** See the proof section.
6. **Units.** Base 2 is bits, base `e` is nats, `1 nat = 1.4427 bits`. The word "bit" is Tukey's,
   per Shannon's own footnote. State the course convention once: teach in bits, quote a training
   loss in nats, always label which.
7. **Two properties, picture first.** `H = 0` exactly when one outcome is certain. `H` is maximal
   at `log2 n` for the uniform distribution. **Named theorem: the maximum-entropy bound.**
8. **Trade-off, in the same section.** Entropy is a property of a distribution, not of a sample.
   Estimating it from counts is biased downward, and the bias grows with the number of categories.
   One line, forward-link to page 0108, which measures the bias.
9. **Warning callout, one only.** Differential entropy is not the limit of discrete entropy. The
   `ln D` term is dropped, so the continuous version can be negative: a Gaussian's is
   `0.5(1 + ln 2*pi*sigma^2)`, below zero whenever `sigma^2 < 1/(2*pi*e)`.

**Do not do here:** cross-entropy, KL, any loss function, coding theorems, continuous entropy
beyond the warning.

## The stated proofs (D4)

**Theorem (maximum entropy).** Over an alphabet of `n` symbols, `H(p) <= log2 n`, with equality
only for the uniform distribution.

*Proof, in full.* Compare `p` with the uniform `u_i = 1/n`.

```
log2 n - H(p) = sum_i p_i log2 n + sum_i p_i log2 p_i      (since sum p_i = 1)
              = sum_i p_i log2 (n p_i)
              = sum_i p_i log2 (p_i / u_i)
```

That last expression is `KL(p || u)`, which page 0107 proves is non-negative and zero only when
`p = u`. So `log2 n - H(p) >= 0`. **The step that does the real work** is the first line: writing
the constant `log2 n` as `sum_i p_i log2 n`, which is legal only because the probabilities sum to
one, turns a comparison of two numbers into a single sum over outcomes. Everything after that is
the definition of KL. *Forward reference is deliberate and stated on the page: this page uses a
result page 0107 proves, and 0107 does not use this one, so there is no circle.*

**Theorem 2 (Shannon 1948).** The only `H` satisfying the three requirements in beat 5 is
`H = -K sum p_i log p_i` for a positive constant `K`.

*The shape of the argument.* Write `A(n) = H(1/n, ..., 1/n)`. The grouping requirement applied to
a choice among `s^m` equally likely options, decomposed into `m` successive choices among `s`,
forces `A(s^m) = m A(s)`. A function on the integers satisfying that, and increasing in `n`, must
be `A(n) = K log n`: squeeze `s^m` between two powers of another base `t` and let `m` grow.
Continuity then carries the result from equal probabilities to rational ones and from rational
ones to all. **The step that does the real work** is `A(s^m) = m A(s)`, which is where the
grouping axiom turns into a functional equation. **Honest boundary:** Shannon puts the full
argument in his Appendix 2 and this course does not reproduce it. Shannon himself writes that the
theorem "and the assumptions required for its proof, are in no way necessary for the present
theory... The real justification of these definitions, however, will reside in their
implications." Quote that. It is the right note for an engineering course.

## Planned figures

1. **Orientation, `flowchart LR`.** Four nodes: "M07 gave you distributions" and "M09 gave you
   likelihoods" into "THIS PAGE: one number that scores a distribution" into "every loss, split
   and metric in M10". Kills: "why is there an information theory module in a maths course".
2. **`svg.chart`, the binary entropy curve.** `H(p)` against `p` on 0 to 1, peaking at 1 bit at
   `p = 0.5`, both ends pinned to zero, `p = 0.1` marked at 0.4690 bits. Kills "entropy is disorder":
   the reader sees certainty at *either* end costs nothing.
3. **`flowchart TB`, the code tree.** Four symbols at 1/2, 1/4, 1/8, 1/8 with codes 0, 10, 110, 111
   and each leaf labelled by its length. Average length 1.75 bits; `H` is 1.75 bits. Kills
   "entropy is an abstraction with no operational meaning".
4. **`svg.chart`, three distributions over eight bins**, side by side with `H` under each: a spike,
   a mild spread, uniform. Kills "higher entropy means more possible values".

## The worked example, with its numbers

**Shannon's own noisy channel**, quoted from page 21 of the 1948 paper, worked in eight parts.

A binary source sends 1,000 symbols per second at `p(0) = p(1) = 0.5`, so it produces 1,000 bits
per second. Noise flips one symbol in a hundred. The intuitive answer, 990 bits per second, is wrong.

1. The equivocation is the entropy of the error pattern: `H(0.01)`.
2. `-0.01 log2 0.01 = 0.01 * 6.6439 = 0.0664` bits.
3. `-0.99 log2 0.99 = 0.99 * 0.0145 = 0.0144` bits.
4. `H(0.01) = 0.0808` bits per symbol.
5. Over 1,000 symbols: 80.8, so the rate is `1000 - 81 = 919` bits per second (Shannon prints 919).
6. **Sanity check.** At a 50 per cent error rate the equivocation is exactly 1 bit per symbol and
   the rate is zero, which is right: the output is then independent of the input.
7. **What changes if** the error rate falls to 0.1 per cent? `H(0.001) = 0.0114` bits, so the rate
   is 989 bits per second. Ten times fewer errors buys back only about nine tenths of the loss,
   because `-p log p` does not scale linearly in `p`.
8. **Derived against quoted.** 919 is Shannon's. `0.08079` is this page's recomputation and agrees.

Second, smaller, derived: a 90/10 class imbalance has entropy 0.4690 bits against 1 bit for a
balanced set, so a majority-class classifier has "explained" more than half the label entropy
before it has learned anything.

## Quiz seeds

Exactly four options each, matched to within 12 characters, `.q-fb` explaining every wrong option.
Answer indices assigned at module integration.

- **Q1 (misconception, M1 "entropy is disorder").** A dataset has two equally likely classes. Add a
  third, also equally likely. What happens to the entropy?
  **Answer: it rises from 1 bit to log2(3) = 1.585 bits.**
  Distractors: it stays at 1 because the classes are still balanced (confuses balance with count);
  it falls because there is more structure (the disorder metaphor, doing its damage); it rises to
  2 bits (thinks entropy counts classes rather than logs them).
- **Q2.** Which of four distributions over four outcomes has the highest entropy?
  **Answer: the uniform one.** Distractors: a spike, a near-spike, a two-way split. The reader has
  to compare rather than pattern-match on "looks spread out".

## Practice seed

**Stem.** A fraud model's training set is 998 legitimate and 2 fraudulent transactions per thousand.
(a) Compute the label entropy in bits. (b) A colleague says the model "explains 99.8 per cent of
the labels". Say what their number measures and what yours measures.

**Hint.** Both terms matter. The rare class has a tiny `p` and an enormous `-log p`; work out which
one wins before you decide the answer is near zero.

**Solution.** (a) `-0.998 log2 0.998 = 0.998 * 0.00289 = 0.00288`;
`-0.002 log2 0.002 = 0.002 * 8.9658 = 0.01793`; total **0.0208 bits**. Note the rare class supplies
86 per cent of it. (b) Their 99.8 per cent is the accuracy of a constant predictor. Your 0.0208
bits is all the uncertainty there ever was to remove. A model that removes none of it still scores
99.8 per cent, which is why the metric and the loss disagree, and it is the same point M06 makes
about accuracy having no usable gradient.

**`.p-check`.** Your answer must be between 0 and 1 bit, because there are two classes. If you got
something above 1 you summed the surprises instead of averaging them.

## Code and dataset plan

`code/0105-entropy.py` against `datasets/m10_signals.csv` and `datasets/m10_classifier.csv`.
Computes `H` with a Python loop and again vectorised and asserts they agree; checks `H = 0` for a
certainty and `H = log2(k)` for the uniform at `k = 2, 3, 5, 8`; **checks the grouping axiom
numerically** on the `plan` column, which is the axiom that forces the `-log` form; then scales to
the entropy of 20,000 predicted distributions and asserts none exceeds `log2 5`.
Measured output the page quotes: `H(plan) = 1.4416` bits against a ceiling of 1.5850;
`H(churned) = 0.8902` bits; grouping axiom agrees to 1e-12; mean row entropy 1.0688 bits.

## Sources, primary only

- Shannon, *A Mathematical Theory of Communication*, BSTJ 27 (1948), section 6, pages 10-11:
  the three requirements, Theorem 2, properties 1 and 2, "bits" from Tukey, and the 919 bits/second
  channel on page 21. https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf
- Goodfellow, Bengio and Courville, *Deep Learning* (2016) section 3.13, for self-information,
  the nats convention and the `0 log 0` convention. https://www.deeplearningbook.org/contents/prob.html
- Bishop, *Pattern Recognition and Machine Learning* (2006) eq 1.102-1.104 and 1.110, for the
  differential-entropy warning.

## Primary source to go deeper

Shannon 1948, section 6. It is nine pages, it is readable, and the reader has now met every idea in it.
