# M07-10 - Bernoulli, binomial, and categorical

**Class:** core. **Rung:** working.

## The single tight idea

One trial, `n` trials, one of `k` outcomes: three distributions that are the same idea at three widths, and between them they are the output layer of almost every classifier you will ship.

## Prerequisites

| Page | What it supplies |
|---|---|
| M07-09 | PMF and CDF |
| M07-05 | independence, which the binomial requires |
| M01, the binomial coefficient | `C(n, k)`. M01 owns it; this page uses it and does not re-derive it. |

## Beats, in order

1. **Bernoulli(p).** A single trial with two outcomes. `P(X = 1) = p`, `P(X = 0) = 1 - p`, compactly `p^x (1-p)^(1-x)`. Mean `p`, variance `p(1-p)`, maximal at `p = 0.5`: **a fair coin is the hardest coin to predict.** Note that M08 owns mean and variance as operators; here they are entries in a table with a forward link.
2. **Binomial(n, p).** The number of ones in `n` independent Bernoulli trials at the same `p`. PMF derived below. **Name the two assumptions loudly**: independent, and `p` constant across trials. Almost every misuse breaks one.
3. **Where the coefficient comes from.** One sentence, one link to M01.
4. **The shape surprises people.** At `p = 0.5` it is a symmetric hump; at `p = 0.004` it is a decaying staircase with its mode at zero. Draw both.
5. **Categorical, also called multinoulli.** `k` states, a parameter vector summing to 1, exactly one state occurs. Reproduce DLB's own footnote, because the naming genuinely trips people: "Many texts use the term multinomial to refer to multinoulli distributions without clarifying that they are referring only to the n = 1 case."
6. **The family in one picture.** Sum `n` Bernoullis and get a binomial; widen a Bernoulli to `k` states and get a categorical; count `n` categorical draws and get a multinomial, which the page names and does not teach.
7. **The machine-learning section, which is why this page is core.** A sigmoid head produces the parameter of a Bernoulli - DLB says exactly that. A softmax head produces the parameter vector of a categorical. A dropout mask is one Bernoulli per unit. A class prior is Bernoulli or categorical. The count of positives in a minibatch is binomial.
8. **The convention trap, which costs real experiments.** In the dropout paper `p` is the probability of **keeping** a unit, and its experiments use `p = 0.5` for hidden units and `p = 0.8` for input units. `torch.nn.Dropout(p)` documents `p` as the "probability of an element to be zeroed". So the paper's input setting is `nn.Dropout(0.2)`, not `0.8`. Teach the misconception; name no person.

## Proof

**Named theorem: the binomial PMF.** For `n` independent trials each succeeding with probability `p`, the number of successes `X` satisfies `P(X = k) = C(n, k) p^k (1-p)^(n-k)` for `0 <= k <= n`.

*Assumed, in words:* the trials are independent, and every trial has the same success probability.

*Shape:* price one particular arrangement, then count how many arrangements there are, then add them up.

*Steps.* Fix one specific sequence of outcomes with `k` successes and `n - k` failures, say `1101...`. Because the trials are independent, the probability of that exact sequence is the product of the individual probabilities, which is `p^k (1-p)^(n-k)`. **Crucially that value does not depend on which positions the successes occupied**, only on how many there were. The event `{X = k}` is the union of all such sequences, they are mutually exclusive, and there are `C(n, k)` of them. Axiom 2 adds them, giving `C(n, k)` copies of the same number.

**The step that does the real work is independence**, used exactly once, to multiply the per-trial probabilities into a per-sequence probability. Drop it and the product is wrong and nothing else survives.

**That it sums to one** follows from the binomial theorem: `sum over k of C(n,k) p^k (1-p)^(n-k)` is the expansion of `(p + (1-p))^n = 1^n = 1`. Worth showing, because it is the check that no arrangement was counted twice or missed.

## Planned figures

1. **Orientation, `flowchart LR`.** `M07-09 PMF` and `M07-05 independence` feed `THIS PAGE - the Bernoulli family`, which enables `the geometric`, `the Poisson` and `every classification head`.
2. **`flowchart LR` - the family.** `Bernoulli` to `Binomial` on "sum n of them"; `Bernoulli` to `Categorical` on "widen to k states"; `Categorical` to `Multinomial - named only` on "count n draws".
3. **`svg.chart` - two binomials, one axis.** Series one, `n = 256, p = 0.00396`, bars at 0.3621, 0.3686, 0.1868, 0.0629. Series two, `n = 256, p = 0.5`, a symmetric hump drawn at reduced vertical scale with its peak marked at 128. Same `n`, unrecognisably different shapes.
4. **`svg.chart` - theory against the file.** The four binomial bars overlaid with the observed proportions from the 97 real batches: 0.3814, 0.3505, 0.1649, 0.0722. Close, and visibly not identical, which is what 97 samples looks like.

## The worked example, eight parts

1. **Setting.** `requests.csv`, minibatches of 256, `X` = flagged requests in a batch. `p = 99 / 25,000 = 0.00396`.
2. **Symbolic.** The binomial PMF, gloss naming `n` as the batch size, `k` as the count asked about, `p` as the per-row flag probability, and `C(n,k)` as the number of ways to choose which rows are flagged.
3. **Picture first.** Figure 3 above.
4. **`ol.worked`.** `P(X = 0) = C(256,0) p^0 (1-p)^256 = (0.99604)^256 = 0.3621`. So **64 percent of batches contain at least one flag and 36 percent contain none.** Then `P(X = 1) = 256 x 0.00396 x (0.99604)^255 = 0.3686`. Expected count `256 x 0.00396 = 1.0138`.
5. **`keynum`.** `99` and `25,000` are read from the file; every power and product is derived here.
6. **Sanity check.** The four probabilities 0.3621, 0.3686, 0.1868, 0.0629 already total 0.9804, so the remaining mass above `k = 3` must be about 0.02. It is, and if the four had totalled more than 1 the arithmetic would be wrong.
7. **What changes if.** Batch of 1,024: `P(X = 0)` falls to 0.0172 and the expected count rises to 4.055. Quadrupling the batch quadrupled the expectation and cut the empty-batch rate twenty-one fold, because that rate is exponential in `n`.
8. **Interpretation.** Just over a third of gradient steps at batch 256 carry no information at all about the class you care about. That is arithmetic about the class prior, not a fault in the optimiser, and it is why people oversample.

## Code and dataset

`code/0129-bernoulli-binomial-categorical.py` against `datasets/requests.csv`.

Computes the binomial PMF twice: once from the definition with an explicit factorial-based `C(n,k)` written out, and once with a vectorised recurrence that avoids overflow, asserting agreement. Then chops the flag column into 97 real batches of 256 and prints the observed proportions beside the theoretical ones, so the reader sees theory and sample side by side rather than only theory. Also fits and prints the three-state categorical over `route` and asserts the three probabilities sum to 1.

## Quiz seeds

1. **Misconception.** The dropout paper reports `p = 0.8` for input units. What does `nn.Dropout(0.8)` do? *Correct:* drops 80 percent, which is the opposite of the paper's intent. *Distractors:* keeps 80 percent, matching the paper; drops 20 percent, matching the paper; nothing, `p` only affects evaluation.
2. Which binomial assumption fails when a sampler draws a minibatch **without** replacement? *Correct:* independence across trials.

## Practice seed

**Stem.** At batch size 512 on the same file, find the probability a batch contains no flagged request, and the expected number of flags. Then say roughly how large the batch must be for the empty-batch probability to fall below 5 percent.
**Hint.** The first is one power. For the third, take logs of `(1 - p)^n = 0.05`.
**Solution.** `(0.99604)^512 = 0.1311`; `512 x 0.00396 = 2.028`. For the threshold, `n = ln(0.05) / ln(0.99604) = -2.9957 / -0.003968 = 755`, so about 760 rows.
**`.p-check`.** The 512 answer must sit between the 256 answer of 0.3621 and the 1,024 answer of 0.0172, and it must be close to the square root of 0.3621, which is 0.6018 squared - it is: `0.3621 x 0.3621 = 0.1311` exactly, because doubling the batch squares the empty probability.

## Sources

- Hajek, ECE 313, sections 2.4.3, 2.4.4 and appendix 6.3.1.
- Goodfellow, Bengio, Courville, *Deep Learning*, ch 3.9.1 and 3.9.2, and the sigmoid remark in ch 3.10.
- Srivastava et al., "Dropout", JMLR 15 (2014), section 4.
