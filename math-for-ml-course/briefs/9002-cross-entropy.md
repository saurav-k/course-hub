# 9002 - Cross-entropy, and why it is the loss

**Module** M10 - lesson 02  **Rung** working  **Class** core

## The single tight idea

The classification loss you already use is the average code length you pay when you compress
reality with your model's beliefs.

## Prerequisites

- 9001 (entropy, and the code reading of it).
- **M09 owns the equivalence** "minimising cross-entropy is maximising likelihood" and derives it
  for the Gaussian and the Bernoulli. This page restates the one-line result with a link and
  **does not re-derive it**. That boundary is the spec's ownership table, edge 23.

## Beats, in order

1. **One-minute version.** `H(p,q) = -sum p log q`. It is what you pay; `H(p)` is what you must
   pay; the gap is the model's fault. The binary case is the log loss M09 already derived.
2. **Orientation figure.** M09's negative log-likelihood into "this page: the same number read as
   bits per symbol" into 9003 (the gap), 9011 (perplexity) and 9005 (the machinery), with 9001
   attached by a dotted edge as the floor.
3. **Mental model: two codebooks.** Reality emits symbols with frequencies `p`. You built your
   code table from `q`. Every symbol costs `-log q` bits instead of the `-log p` it could have.
   Both trees drawn over one alphabet, both average lengths printed.
4. **Mechanism.** `H(p,q) = -sum_i p_i log2 q_i`, every symbol glossed. Then show that a one-hot
   label collapses the sum to a single term, `-log q_(true class)`, and that this collapse is why
   the loss looks so small in code.
5. **The bridge, stated not derived.** One `.math` block, one sentence, one link: M09 showed the
   negative log-likelihood is the objective; this sum **is** that objective averaged over the
   training set, with the empirical distribution as `p`.
6. **The misnomer, key callout, from the source.** *Deep Learning* section 5.5: calling only the
   Bernoulli-or-softmax NLL "cross-entropy" is a misnomer, and mean squared error is the
   cross-entropy between the empirical distribution and a Gaussian model. This retro-labels M09's
   result and unifies two losses the reader has always seen as unrelated.
7. **Cross-entropy is a compression rate, with the number.** Brown et al. 1992 measured 1.75 bits
   per character for printed English as the cross-entropy of the Brown Corpus under a word-trigram
   model. `H(P) <= H(P,M)` always, so any model's measured cross-entropy is an upper bound on the
   true entropy and better models give tighter bounds. **Named theorem, see proof section.**
8. **Trade-off, same section.** Cross-entropy is unbounded above. One confident wrong prediction at
   `q = 1e-9` contributes 29.9 bits and can dominate a batch. Name label smoothing and gradient
   clipping as the two answers, one line, link to M06.

**Do not do here:** softmax mechanics (9005), KL as a named quantity (9003), perplexity (9011),
the MLE derivation (M09 owns it).

## The stated proofs (D4)

**Theorem (the decomposition).** `H(p, q) = H(p) + KL(p || q)`.

*Proof, in full.* Add and subtract `log2 p_i` inside the sum:

```
H(p, q) = -sum_i p_i log2 q_i
        = -sum_i p_i log2 p_i  +  sum_i p_i log2 p_i - sum_i p_i log2 q_i
        =  H(p)                +  sum_i p_i log2 (p_i / q_i)
        =  H(p) + KL(p || q)
```

**The step that does the real work** is the second line, and it does no work at all: it adds zero.
That is the point worth making to the reader. The decomposition is not a discovery about the world,
it is bookkeeping, and everything interesting is in what the two pieces *mean*.

**Corollary (Gibbs, applied).** `H(p, q) >= H(p)`, with equality only when `q = p`. Immediate from
the decomposition plus `KL >= 0`, which page 9003 proves. So a model can never beat the floor, and
the amount by which it misses is exactly the KL. That corollary is what licenses Brown et al.'s
1.75 bits as an **upper bound** on the entropy of English rather than an estimate of it.

## Planned figures

1. **Orientation, `flowchart LR`,** as beat 2.
2. **`flowchart TB`, two codebooks over one alphabet.** Left the code built from `p`, right the
   code built from `q` applied to symbols arriving at rate `p`. Kills "cross-entropy is an
   arbitrary formula".
3. **`svg.chart`, the loss curve.** `-log2 q` against `q` on (0, 1], with the asymptote at zero and
   the value 0 at `q = 1`. Mark `q = 0.5` at 1 bit and `q = 1e-9` at 29.9 bits. Kills "why does one
   bad prediction wreck my batch loss".
4. **`quadrantChart`, four losses.** Axes "assumes Gaussian noise / assumes categorical" against
   "is a cross-entropy / is not". Points: MSE, binary log loss, softmax cross-entropy, hinge loss.
   Three of the four are cross-entropies, which is the misnomer made visual. Keep point labels
   under 26 characters.
5. **`svg.chart`, the reliability curve**, measured by the code file: mean confidence against
   accuracy in eight bins, with the diagonal drawn. It crosses.

## The worked example, with its numbers

A real three-class prediction, worked in eight parts. Derived; arithmetic shown in full.

1. A classifier outputs logits `[2.0, 1.0, 0.1]`.
2. Softmax gives `q = [0.6590, 0.2424, 0.0986]`.
3. The true label is class 0, so `p = [1, 0, 0]`.
4. `H(p, q) = -(1 * ln 0.6590) = 0.4170` nats `= 0.6016` bits.
5. Had the truth been class 2: `-ln 0.0986 = 2.3170` nats, **5.6 times larger from the same prediction**.
6. **Sanity check.** The loss must lie between 0 and `+inf` and must fall as `q_true` rises. At
   `q_true = 1` it is 0; at `q_true = 1/3`, the uninformed answer for three classes, it is
   `ln 3 = 1.0986` nats. Our 0.4170 sits below that, so the model beat a coin toss.
7. **What changes if** the label were soft, say `p = [0.8, 0.2, 0]`? The sum no longer collapses:
   `-(0.8 ln 0.6590 + 0.2 ln 0.2424) = 0.3336 + 0.2836 = 0.6172` nats. Label smoothing is exactly
   this, and it costs you something even when you are right, which is the point of it.
8. **Quoted, for the compression reading.** Brown et al. 1992: 1.75 bits per character for printed
   English, over an alphabet of 95 printable ASCII characters, from a word-trigram model built on
   583 million words and tested on the 5.96-million-character Brown Corpus. A uniform model over 95
   characters costs `log2 95 = 6.57` bits, so the model captures about 73 per cent of the redundancy.

## Quiz seeds

- **Q1.** A three-class model outputs `[0.7, 0.2, 0.1]` and the true class is the second. What is
  the loss in nats? **Answer: `-ln 0.2 = 1.609`.** Distractors: `-ln 0.7 = 0.357` (scored the
  argmax, not the label); `0.8` (used `1 - p`); `1.030` (averaged all three terms as if the label
  were uniform).
- **Q2 (misconception, M3 the misnomer).** According to *Deep Learning* section 5.5, mean squared
  error is which of these? **Answer: the cross-entropy between the empirical distribution and a
  Gaussian model.** Distractors: not a cross-entropy at all; a cross-entropy only for targets in
  `[0,1]`; the same thing as KL divergence.

## Practice seed

**Stem.** Two models score the same four-example test set. Model A gives the true class the
probabilities `[0.9, 0.9, 0.9, 0.1]`. Model B gives `[0.7, 0.7, 0.7, 0.6]`. (a) Which has the better
accuracy at a 0.5 threshold? (b) Which has the lower mean cross-entropy? (c) Which would you ship,
and why do the two metrics disagree?

**Hint.** Compute the loss on the fourth example on its own before you average anything.

**Solution.** (a) A is right on three of four; B on four of four. B wins on accuracy.
(b) A: `-(3 ln 0.9 + ln 0.1)/4 = (0.3162 + 2.3026)/4 = 0.6547` nats.
B: `-(3 ln 0.7 + ln 0.6)/4 = (1.0700 + 0.5108)/4 = 0.3952` nats. B wins here too, but not for the
reason accuracy gives. (c) A's single confident error costs 2.3026 nats on its own, **88 per cent of
A's total loss**. Accuracy charges a flat 1 for the same error. Ship B, and note the answer would
flip if that fourth example turned out to be mislabelled in the test set, because cross-entropy
punishes confident disagreement with a label far harder than accuracy does.

**`.p-check`.** Both mean losses must be positive and below `ln 4 = 1.386`, the loss of a model
that guesses uniformly over four options. If either is above that, you summed instead of averaging.

## Code and dataset plan

`code/9002-cross-entropy.py` against `datasets/m10_classifier.csv`. Computes the loss the long way
(`-sum p log q` over all five classes) and the framework way (`-z_true + logsumexp(z)`) and asserts
they agree to 3.6e-15 over 20,000 rows; verifies `H(p,q) = H(p) + KL` on the label marginal; then
reports accuracy 0.7924 against mean loss 0.7558 nats, mean loss 0.2874 on correct rows and 2.5435
on wrong ones, a worst row at 26.2117 nats which is 88 times the median, the worst 1 per cent of
rows carrying 10.4 per cent of the total loss, and the eight-bin reliability curve.

## Sources, primary only

- Goodfellow, Bengio and Courville, *Deep Learning* (2016) section 5.5, eq 5.56-5.61, and the
  misnomer paragraph. https://www.deeplearningbook.org/contents/ml.html
- Brown, Della Pietra, Della Pietra, Mercer and Lai, *An Estimate of an Upper Bound for the Entropy
  of English*, Computational Linguistics 18:1 (1992), sections 2.1 and 2.2.
  https://aclanthology.org/J92-1002.pdf
- Bishop, *PRML* (2006) eq 1.113 and the surrounding paragraph.

## Primary source to go deeper

Brown et al. 1992. Six pages, and it is the clearest statement anywhere that a cross-entropy is a
file size.
