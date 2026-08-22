# 9007 - Cosine similarity and where it is the wrong tool

**Module** M10 - lesson 07  **Rung** frontier  **Class** depth

## The single tight idea

An embedding space is not isotropic, so a cosine similarity has no absolute meaning, and every
score a retrieval system reports has to be read against that space's own baseline.

## Prerequisites

9006 (metric axioms, and the `|x_hat - y_hat|^2 = 2 - 2cos` relation). 9004 for pointwise mutual
information, which beat 7 needs. M03 for the dot product and the angle. M04 for SVD and low-rank
approximation.

## Beats, in order

1. **One-minute version.** Embeddings occupy a narrow cone, not a ball. A cosine of 0.59 can be
   below chance. One subtraction fixes most of it. And the classic word embedding turns out to be a
   factorised mutual-information matrix.
2. **Orientation figure.** A `mindmap` is allowed for an orientation figure and suits this page,
   because it is the one that indexes what the rest of the module built: "cosine (9006)",
   "PMI (9004)", "SVD (M04)", "concentration (9009)" as four branches into "reading a retrieval
   score honestly".
3. **What cosine is, and what it throws away.** The definition, then the ranking split: query
   `(1,1,0)`, `d1 = (10,10,0)` at cosine 1.0000 and Euclidean 12.7279, `d2 = (1,1,1)` at cosine
   0.8165 and Euclidean 1.0000. Opposite orders. Then the repair from 9006: normalise and the two
   orders become identical, every row, which the code file asserts.
4. **Anisotropy, measured.** If a space were isotropic the average cosine between two random rows
   would be zero. On the committed dataset it is **0.6399**. Ethayarajh 2019 measured roughly 0.6
   in GPT-2's layers 2 to 8 and near 1.0 in its last layer, so this is not an artefact of the toy.
   **Named effect, and see the proof section for why isotropy implies zero.**
5. **The reading that matters.** Same-topic pairs score 0.8677 and different-topic pairs score
   0.5943. Both *sound* like matches. Against a 0.6399 baseline the second is **below chance**.
   Ethayarajh's own instance: with a baseline of 0.99, a self-similarity of 0.95 means the
   representations are *well* contextualised.
6. **The fix, one subtraction.** Centre the space and renormalise. Measured: the baseline goes to
   0.0002, same-topic to 0.6341, different-topic to -0.1267, and the gap between the two
   populations goes from 0.2734 to 0.7608, a factor of 2.8.
7. **The loop this page closes, key callout.** Levy and Goldberg 2014 prove that skip-gram with
   negative sampling implicitly factorises the word-context matrix whose cells are
   `PMI(w,c) - log k`. So a word2vec vector is a low-rank factor of a pointwise-mutual-information
   matrix: 9004 defined PMI, M04 defined the factorisation, and they meet here.
8. **Three practical consequences**, one line each, each traceable to beat 4: normalise before
   indexing; centre before comparing; and never compare cosines across two models or two layers.
9. **Trade-off, same section.** Cosine measures whatever the training objective made "similar",
   which is co-occurrence, not truth and not relevance. The highest-scoring chunk can be the wrong
   chunk. Cross-link to `../../llm-papers-course/lessons/0031-rag.html`.

**Do not do here:** the curse of dimensionality (9009 owns it), ANN index structures, training
objectives for sentence encoders.

## The stated proof (D4)

**Proposition (why an isotropic space has a zero baseline).** If two vectors are drawn independently
and uniformly from the directions in `R^d`, then `E[cos theta] = 0`.

*Proof, in full.* Fix the first vector and call its direction `u`; by rotational symmetry nothing
depends on which direction that is. The second, `v`, is uniform on the sphere, and the sphere is
symmetric under the reflection `v -> -v`, which maps the uniform distribution to itself. Under that
map `cos theta = u . v` becomes `-u . v`. A random variable whose distribution is unchanged by
negation has expectation zero, provided the expectation exists, and here `|cos theta| <= 1` so it
does. **The step that does the real work** is the reflection symmetry: it is the whole argument,
and it is exactly the symmetry a real embedding space does not have, because every vector in it
carries a large component along one shared direction.

**Corollary the page must state.** A measured baseline of `b` instead of 0 means the excess over
chance for an observed score `s` is `s - b`, not `s`. On the committed data a raw score of 0.72
against a baseline of 0.6399 is an excess of 0.08, not 0.72: the reported number overstates the
match by roughly nine times.

**Honest boundary.** "Subtract the mean vector" is a first-order repair, not a theorem. It removes
the single dominant shared direction. It does not make the space isotropic, and the measured
post-centring baseline of 0.0002 on this dataset is that good only because the dataset was built
with exactly one cone. Real spaces have more structure than that, and the honest instruction is to
**measure your own baseline** rather than to assume centring fixed it.

## Planned figures

1. **Orientation, `mindmap`,** as beat 2. Mermaid takes mindmap branch colours from its own scale,
   which `hub.js` supplies from the `--branch-0..7` tokens, so check it in both modes.
2. **`svg.chart`, the cone.** A 2-D projection: an isotropic cloud on the left, an anisotropic cone
   on the right with the mean direction drawn, and the random-pair baseline printed under each,
   0.0000 against 0.6399.
3. **`svg.chart`, three overlapping histograms** of cosine score: all pairs, same-topic pairs,
   different-topic pairs, with the baseline as a `ref` line. The different-topic distribution
   sitting just below the baseline is the whole page in one figure.
4. **`svg.chart`, before and after centring**, the same three histograms after the subtraction, so
   the 0.2734-to-0.7608 gap is visible rather than asserted.
5. **`flowchart LR`, the factorisation loop.** Corpus co-occurrence counts -> PMI matrix (9004) ->
   shifted by `-log k` -> low-rank factorisation (M04 SVD) -> the word vectors you use.

## The worked example, with its numbers

Reading a score against its baseline, eight parts.

1. A retrieval system reports a cosine of 0.72 between a query and a chunk.
2. Measure the baseline: sample 200,000 random pairs from the same space. Here it is **0.6399**.
3. Excess over chance: `0.72 - 0.6399 = 0.0801`.
4. For scale, a same-topic pair in this space averages 0.8677, an excess of 0.2278.
5. So the reported 0.72 is about **35 per cent of the way** from chance to a genuine topical match,
   not 72 per cent of the way to perfect.
6. **Sanity check.** The baseline must lie strictly between -1 and 1, and if it comes out near zero
   your space is already close to isotropic and the correction is not needed. A baseline above 0.9
   means almost all of every score is the cone.
7. **What changes if** you centre first? The baseline becomes 0.0002, the same-topic mean becomes
   0.6341 and the different-topic mean becomes -0.1267. The same 0.72 raw score would have to be
   recomputed on the centred vectors; the point is that after centring the number can be read at
   face value, and before it cannot.
8. **The threshold consequence, measured.** A fixed cut at 0.75 on raw scores keeps 18.1 per cent of
   all pairs, of which 92.3 per cent are same-topic against 16.7 per cent in the population. The
   same cut on centred scores keeps 0.9 per cent of pairs, of which **100 per cent** are same-topic.
   The threshold did not change. The space did.

**Quoted, for the loop.** Levy and Goldberg 2014 trained on English Wikipedia, 1.5 billion tokens,
a 189,533-word vocabulary and a window of two tokens each side, and showed SGNS implicitly
factorises `PMI(w,c) - log k`. With `k = 5` negative samples that shift is `log 5 = 1.609` nats
subtracted from every cell.

## Quiz seeds

- **Q1 (misconception, M9).** A retrieval system reports a cosine of 0.65 between a query and a
  chunk. What do you need before you can call that a good match? **Answer: the average cosine
  between two random vectors in that same space.** Distractors: the length of the query; how many
  chunks were searched; the model's training loss.
- **Q2.** Levy and Goldberg 2014 showed that skip-gram with negative sampling implicitly factorises
  which matrix? **Answer: the word-context PMI matrix shifted by `-log k`.** Distractors: the raw
  co-occurrence count matrix; the TF-IDF matrix; the term-document matrix.

## Practice seed

**Stem.** You compare two sentence encoders. Encoder X gives your query-document pair a cosine of
0.81; encoder Y gives 0.55. You sample 10,000 random pairs from each: X's mean is 0.78, Y's is 0.11.
(a) Compute the excess over baseline for each. (b) Say which encoder discriminates better and by
how much. (c) Name the two things that go wrong if you set a shared similarity threshold across
both models.

**Hint.** Do not compare 0.81 with 0.55. Compare each with its own space.

**Solution.** (a) X: `0.81 - 0.78 = 0.03`. Y: `0.55 - 0.11 = 0.44`. (b) Y, by roughly fifteen times
on the excess, despite reporting a much lower raw number. Almost all of X's 0.81 is the cone.
(c) First, the absolute value of a cosine has no cross-model meaning, so "above 0.75" is not one
rule but two different rules. Second, applied to both spaces it retrieves nearly everything in X's
and nearly nothing in Y's, so the same configuration silently becomes a no-op filter on one model
and an over-aggressive one on the other.

**`.p-check`.** Both excesses must be smaller than the raw scores, and both must be below 1. If an
excess came out negative, the pair scored below chance, which is a real and reportable result.

## Code and dataset plan

`code/9007-cosine-similarity.py` against `m10_embeddings.csv`. Cosine from the definition against
the unit-row dot product; the 200,000-pair baseline; the same-topic and different-topic means;
centring and the recomputation; the ranking-split example; and the threshold experiment. Asserts
that once rows are normalised the cosine order and the Euclidean order are **identical for every
row**, and checks `|u - v|^2 = 2 - 2cos` to 1e-12.

## Sources, primary only

- Ethayarajh, *How Contextual are Contextualized Word Representations?*, EMNLP 2019, sections 3.4
  and 4.1. https://aclanthology.org/D19-1006.pdf **Note for the writer:** the GPT-2 per-layer
  figures are in prose and in figure 1; there is no table. Any chart is a qualitative redraw and
  the figcaption must say so.
- Levy and Goldberg, *Neural Word Embedding as Implicit Matrix Factorization*, NeurIPS 2014,
  abstract and section 5.
  https://proceedings.neurips.cc/paper_files/paper/2014/file/b78666971ceae55a8e87efb7cbfd9ad4-Paper.pdf
- Bishop, *PRML* (2006) for Cauchy-Schwarz bounding the cosine into `[-1, 1]`.

## Primary source to go deeper

Ethayarajh 2019. Eleven pages, and it is the paper that makes a cosine score readable.
