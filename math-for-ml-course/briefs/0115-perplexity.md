# 0115 - Perplexity

**Module** M10 - lesson 11, the last page of the module  **Rung** working  **Class** core

## The single tight idea

Perplexity is the effective number of equally likely options the model is choosing among, which
makes it readable across models and meaningless across tokenizers.

## Prerequisites

0105 (entropy), 0106 (cross-entropy). Nothing else; this page is deliberately the easy landing
after four hard ones.

## Beats, in order

1. **One-minute version.** `PPL = exp(mean NLL)`. It is one over the geometric mean of the
   probabilities the model gave the things that actually happened. A uniform model over `V` symbols
   scores exactly `V`. And comparing two models with different tokenizers is not a comparison.
2. **Orientation figure.** 0106's cross-entropy in bits into "this page: exponentiate to get a
   count of options" into reading a scaling-law plot, with 0105 dotted in as the floor.
3. **Mental model: a fair die.** A model with perplexity 7 is on average as uncertain as someone
   rolling a fair seven-sided die. Draw the ladder: 1 is certainty, `V` is total ignorance.
4. **Mechanism, both readings, shown to be the same number.** `PPL = exp(-(1/N) sum log q(x_i))`
   and `PPL = (prod q(x_i))^{-1/N}`. **Named theorem, see proof.** The second is the geometric-mean
   reading and it is the one that makes the metric intuitive.
5. **The anchor.** A GPT-2 tokenizer has 50,257 tokens, so a uniform model scores 50,257 and a
   cross-entropy of `log2 50257 = 15.6170` bits or `10.8249` nats. Every real number a reader meets
   is measured against that ceiling.
6. **Where the number comes from, measured.** Perplexity is a geometric mean, so the smallest
   probabilities dominate it. On the committed data the worst 1 per cent of symbols carry 10.4 per
   cent of the total loss, and dropping them moves perplexity from 2.1293 to 1.9821 while accuracy
   moves from 0.7924 to 0.8004. Accuracy cannot tell a near miss from a catastrophe.
7. **The trap, and it is the reason this page exists.** Perplexity is per token and tokens differ.
   Brown et al. saw it in 1992 and wrote it down: restricting the model to the test sample's
   vocabulary "would be noticeably lower" but "could not be trumpeted as upper bounds to the entropy
   of English". The modern fix is bits per UTF-8 byte, and The Pile defines it:
   `BPB = (L_T/L_B) * loss / ln 2` with `L_T/L_B = 0.29335` GPT-2 tokens per byte, "preferred over
   bits per character or perplexity ... due to its invariance to different tokenization schemes".
   **One warning callout**, with the retokenisation experiment below.
8. **Two smaller traps, one line each.** Perplexity depends on whether documents are concatenated
   or scored independently, and on the context length used. The Pile section 3.2 says which it chose
   and why.
9. **Trade-off, same section.** Perplexity measures calibrated next-token probability and nothing
   else. A model can improve on perplexity and get worse at a task. Cross-link out to
   `../../llm-papers-course/lessons/0005-scaling-laws.html`, where perplexity is the `y` axis, and
   `../../llm-evolution-course/lessons/0028-gpt-2-and-the-bet-on-scale.html` for it in context.
10. **Module close.** This is the last page of M10, so the pager "next" points at `../index.html`
    titled "Course map". One paragraph of reprise: every quantity in this module was `-log p`
    averaged in a different way.

**Do not do here:** scaling laws, benchmark design, evaluation methodology.

## The stated proof (D4)

**Theorem (the three readings are one number).** For probabilities `q_1, ..., q_N` assigned to the
`N` symbols that actually occurred,

```
exp( -(1/N) sum_i ln q_i )  =  ( prod_i q_i )^{-1/N}  =  2^( (1/N) sum_i log2 (1/q_i) )
```

*Proof, in full.* Take the middle expression and push it through `exp(ln(.))`, which is the identity
on positive numbers:

```
( prod_i q_i )^{-1/N} = exp( ln ( prod_i q_i )^{-1/N} )
                      = exp( -(1/N) ln prod_i q_i )
                      = exp( -(1/N) sum_i ln q_i )
```

using `ln(ab) = ln a + ln b`, which is the single property of logarithms M01 established. For the
third expression, change base: `exp(x) = 2^{x / ln 2}` and `log2 y = ln y / ln 2`, so
`exp(-(1/N) sum ln q_i) = 2^{-(1/N) sum log2 q_i} = 2^{(1/N) sum log2 (1/q_i)}`.

**The step that does the real work** is `ln(prod) = sum(ln)`, and it is worth telling the reader
why it is not merely convenient: the product of twenty thousand numbers below one underflows
float64 long before you finish multiplying it. The geometric-mean reading is the *meaning* and the
log-space computation is the only way to obtain it. The code file computes it in log space for
exactly that reason.

**Corollary (the anchors).** A uniform model over `V` symbols assigns `q_i = 1/V` to every symbol,
so the geometric mean is `1/V` and `PPL = V`. A perfect model assigns 1 to every symbol, the
geometric mean is 1, and `PPL = 1`. So perplexity always lies in `[1, V]` for a model that never
assigns zero, and it reads directly as "how many options, effectively".

**Corollary (why the trap is a theorem and not an accident).** Group the `N` symbols into `N/2`
adjacent pairs and treat each pair as one token. The model's beliefs about the underlying sequence
have not changed at all: the probability of a pair is the product of its two probabilities, so the
total log-likelihood is identical. But `PPL` divides by the token count, which has halved, so the
exponent doubles and **the new perplexity is the square of the old one**. The code file measures
2.1293 becoming 4.5339, and `2.1293^2 = 4.5339`. Bits per symbol does not move, to nine decimal
places. Nothing about the model changed; only the unit did.

## Planned figures

1. **Orientation, `flowchart LR`,** as beat 2.
2. **`svg.chart`, the ladder.** One log axis from 1 to 50,257 with marks at a perfect model, the
   committed model at 2.13 on a five-symbol alphabet, a word-trigram model on English, and uniform
   over the GPT-2 vocabulary. Only anchors with a source get a `keynum`.
3. **`flowchart LR`, the same number four ways.** mean NLL in nats -> bits per token -> perplexity
   -> bits per byte, with the conversion written on each edge (`/ ln 2`, `exp`, `* L_T/L_B`).
   Kills "these are four different metrics".
4. **`svg.chart`, the retokenisation trap.** Two grouped bars: per-token perplexity under the fine
   and coarse tokenisations (2.1293 against 4.5339) beside bits per symbol under both (1.0904 and
   1.0904). One pair moves, one does not.
5. **`svg.chart`, the loss concentration.** Cumulative share of total loss against the sorted
   percentile of symbols, showing the worst 1 per cent carrying 10.4 per cent and the worst 5 per
   cent carrying 33.5 per cent, with the diagonal drawn for reference.

## The worked example, with its numbers

A four-token sentence and a retokenisation. Eight parts, derived.

1. A model assigns `[0.40, 0.20, 0.10, 0.05]` to the four tokens that occurred.
2. `sum ln q = -0.9163 - 1.6094 - 2.3026 - 2.9957 = -7.8240`; mean NLL `= 1.9560` nats.
3. `PPL = e^{1.9560} = 7.0711`.
4. The other reading: geometric mean `= (0.40 * 0.20 * 0.10 * 0.05)^{1/4} = (0.0004)^{0.25} =
   0.1414`, and `1 / 0.1414 = 7.0711`. **Same number, two routes.**
5. In bits: `1.9560 / ln 2 = 2.8219` bits per token, and `2^{2.8219} = 7.0711`. Three routes now.
6. **Sanity check.** `PPL` must lie between 1 and the alphabet size, and it must be larger than
   `1/max(q_i) = 2.5` and smaller than `1/min(q_i) = 20`, because a geometric mean lies between the
   extremes it averages. 7.07 sits inside.
7. **What changes if** you pair adjacent tokens? Measured on the committed data: per-token
   perplexity goes from 2.1293 to 4.5339, exactly the square, while bits per **symbol** stays at
   1.0904 to nine decimal places. Nothing about the model changed.
8. **The conversion, quoted.** The Pile: `BPB = (L_T/L_B) * loss / ln 2` with `L_T/L_B = 0.29335`.
   A loss of 2.0 nats per token becomes `0.29335 * 2.0 / 0.6931 = 0.8464` bits per byte. Two models
   with different vocabularies can be compared on that and cannot be compared on step 3.

## Quiz seeds

- **Q1 (misconception, M8).** Model A has perplexity 18 with a 32,000-token vocabulary; model B has
  perplexity 22 with a 50,257-token vocabulary, on the same text. Which is better? **Answer: you
  cannot tell from these numbers.** Distractors: A; B; A, because lower is always better.
- **Q2.** A model has perplexity 1.0 on a test set. What does that mean? **Answer: it assigned
  probability 1 to every token that occurred.** Distractors: it is as uncertain as a fair coin; it
  never made an argmax mistake; the test set had one token type.

## Practice seed

**Stem.** A model scores a five-token sentence with probabilities `[0.5, 0.25, 0.5, 0.125, 0.5]`.
(a) Compute the mean negative log-likelihood in nats and in bits. (b) Compute the perplexity two
ways and check they agree. (c) The corpus has 0.25 tokens per UTF-8 byte under this tokenizer.
Convert to bits per byte and say why you would report that number instead.

**Hint.** Every probability here is a power of one half, so the bits answer is exact and you can do
(a) without a calculator.

**Solution.** (a) The five probabilities are `2^-1, 2^-2, 2^-1, 2^-3, 2^-1`, so the bits are
`1, 2, 1, 3, 1` and the mean is exactly **1.6 bits**, which is `1.6 * ln 2 = 1.1090` nats.
(b) `PPL = 2^{1.6} = 3.0314`, and the geometric mean is `(0.5*0.25*0.5*0.125*0.5)^{1/5} =
(2^{-8})^{1/5} = 2^{-1.6} = 0.32988`, whose reciprocal is **3.0314**. They agree.
(c) `BPB = 0.25 * 1.6 = 0.400` bits per byte. Report it because it is invariant to the tokenizer,
which is why The Pile adopted it, and because a per-token number cannot be compared with any model
that segments text differently.

**`.p-check`.** Your perplexity must lie between 2 and 8, because the smallest probability is 0.125
and the largest is 0.5, and a geometric mean lies between the extremes. If you got something
outside that range you averaged the probabilities instead of their logs.

## Code and dataset plan

`code/0115-perplexity.py` against `m10_classifier.csv` read as a next-symbol predictor. Computes
perplexity three ways and asserts they agree to 1e-9; checks both anchors; reports the loss
concentration; and **performs the retokenisation experiment**, pairing adjacent symbols so the
model's beliefs are unchanged and only the unit moves, then prints The Pile's conversion.

## Sources, primary only

- Brown, Della Pietra, Della Pietra, Mercer and Lai, Computational Linguistics 18:1 (1992),
  section 2.2, for the vocabulary-restriction warning. https://aclanthology.org/J92-1002.pdf
- Gao et al., *The Pile*, arXiv:2101.00027, section 3.1, for the BPB definition and the 0.29335
  constant. https://arxiv.org/pdf/2101.00027
- Goodfellow, Bengio and Courville, *Deep Learning* (2016) section 3.13, for the entropy the
  exponent is taken of.

## Primary source to go deeper

Gao et al., *The Pile*, section 3.1. Two paragraphs, and they settle a question that has confused
model comparisons for a decade.
