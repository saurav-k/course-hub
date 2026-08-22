"""M03 L13 - The data matrix, and how a thing with no numbers becomes a vector.

    python3 m03-l13-data-matrix.py

Three results, each checked twice.

1. The Gram matrix of a centred, scaled data matrix is the correlation matrix.
   Computed as X^T X / (n - 1) and again with pandas' own .corr().
2. A one-hot vector times a matrix selects one row. Computed as a matrix product
   and again as an index, with the flop counts for both.
3. The analogy caveat. Word vectors are built from the corpus, the offset
   a* - a + b is computed, and its nearest neighbour is reported twice: once with
   the three input words allowed, and once with them excluded.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HOUSING = Path(__file__).resolve().parent.parent / "datasets" / "housing.csv"
DOCUMENTS = Path(__file__).resolve().parent.parent / "datasets" / "documents.csv"
FEATURES = ["area_k_sqft", "bedrooms", "bathrooms", "age_years", "lot_sqft"]


def main() -> None:
    frame = pd.read_csv(HOUSING)
    X = frame[FEATURES].to_numpy(dtype=float)
    n, d = X.shape
    print(f"X is (n_samples, n_features) = {X.shape}: rows are houses, columns are measurements")
    print(f"  row 0    is one house       : {np.round(X[0], 2)}")
    print(f"  column 0 is one measurement : first three are {np.round(X[:3, 0], 3)}")

    print("\n-- centre, scale, and the Gram matrix becomes the correlation matrix --")
    Z = (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)
    G = Z.T @ Z / (n - 1)
    R = frame[FEATURES].corr().to_numpy()
    print(f"  Z^T Z / (n-1) is {G.shape}, symmetric to {np.abs(G - G.T).max():.3e}")
    print(f"  max |Z^T Z/(n-1) - pandas .corr()| = {np.abs(G - R).max():.3e}")
    assert np.allclose(G, R)
    print("checked twice: one matrix product reproduces every pairwise correlation")
    print(f"  correlation(area_k_sqft, bedrooms) = {G[0, 1]:.4f}")
    print(f"  cost of X^T X: about {2 * n * d * d:,} flops, and it is symmetric so about half is needed")

    print("\n-- a batched linear layer is one matrix product --")
    W = np.random.default_rng(0).normal(0.0, 0.1, size=(3, d))
    out = X @ W.T
    print(f"  X {X.shape} @ W.T {W.T.shape} -> {out.shape}, which is {n * 3:,} dot products of length {d}")

    print("\n-- categorical data has no distance until you give it one --")
    docs = pd.read_csv(DOCUMENTS)
    topics = sorted(docs["topic"].unique())
    onehot = np.eye(len(topics))
    print(f"  {len(topics)} topics, one-hot: every pair is the same distance apart")
    dists = {
        f"{topics[i]} to {topics[j]}": float(np.linalg.norm(onehot[i] - onehot[j]))
        for i in range(len(topics))
        for j in range(i + 1, len(topics))
    }
    print(f"  all pairwise distances: {sorted(set(round(v, 6) for v in dists.values()))}  (sqrt 2)")

    print("\n-- one-hot times a matrix is a row lookup --")
    vocabulary = 37_000
    d_model = 512
    E = np.random.default_rng(1).normal(0.0, 0.02, size=(200, 8))
    index = 137
    e = np.zeros(200)
    e[index] = 1.0
    by_product = e @ E
    by_index = E[index]
    assert np.array_equal(by_product, by_index)
    print(f"  e_{index} @ E equals E[{index}] exactly: {np.array_equal(by_product, by_index)}")
    print(f"  at a real size, {vocabulary:,} by {d_model}:")
    print(f"    the one-hot basis written out : {vocabulary * vocabulary:,} numbers")
    print(f"    the embedding matrix E        : {vocabulary * d_model:,} numbers"
          f"  ({vocabulary * vocabulary / (vocabulary * d_model):.0f}x smaller)")
    print(f"    the product costs about {2 * vocabulary * d_model:,} flops per token")
    print(f"    the lookup costs 0, which is why every library does the lookup")

    print("\n-- a count-based embedding, built from this corpus --")
    terms = [c for c in docs.columns if c not in ("doc_id", "topic")]
    counts = docs[terms].to_numpy(dtype=float)
    profile = np.zeros((len(terms), len(topics)))
    for t, topic in enumerate(topics):
        profile[:, t] = counts[docs["topic"].to_numpy() == topic].sum(axis=0)
    profile = profile / profile.sum(axis=1, keepdims=True)
    unit = profile / np.linalg.norm(profile, axis=1, keepdims=True)
    print(f"  every one of the {len(terms)} words is now a point in R^{len(topics)}")
    for word in ("gradient", "flour", "telescope", "the"):
        i = terms.index(word)
        print(f"    {word:<10} {np.round(profile[i], 3)}")
    print("  'the' sits near the middle because every topic uses it, which is the whole")
    print("  distributional idea: a word is described by the company it keeps")

    print("\n-- the analogy, measured rather than asserted --")
    # The offset method: given a is to a* as b is to ?, score every word against
    # a* - a + b. The question this measures is what the top hit turns out to BE.
    def offset_scores(a: str, a_star: str, b: str) -> np.ndarray:
        v = unit[terms.index(a_star)] - unit[terms.index(a)] + unit[terms.index(b)]
        return unit @ (v / np.linalg.norm(v))

    a, a_star, b = "model", "gradient", "flour"
    scores = offset_scores(a, a_star, b)
    order = np.argsort(-scores)
    inputs = {a, a_star, b}
    print(f"  '{a}' is to '{a_star}' as '{b}' is to ...?")
    print(f"    top four, inputs allowed : {[terms[i] for i in order[:4]]}")
    print(f"    top four, inputs excluded: {[terms[i] for i in order if terms[i] not in inputs][:4]}")
    ranks = {w: int(np.where(order == terms.index(w))[0][0]) + 1 for w in inputs}
    print(f"    where the input words themselves rank: {ranks}")
    print(f"    note that all eight cooking words tie at cosine {scores[order[0]]:.4f}: this space has")
    print(f"    only {len(topics)} dimensions, so words of one topic are one point")

    print("\n  across 3,000 random word triples from this corpus:")
    rng2 = np.random.default_rng(0)
    hits = trials = 0
    small_hits = small_trials = 0
    for _ in range(3_000):
        i, j, k = rng2.choice(len(terms), 3, replace=False)
        v = unit[j] - unit[i] + unit[k]
        if np.linalg.norm(v) < 1e-9:
            continue
        top = int(np.argmax(unit @ (v / np.linalg.norm(v))))
        trials += 1
        hit = top in (i, j, k)
        hits += hit
        if np.linalg.norm(unit[j] - unit[i]) <= 0.35:
            small_trials += 1
            small_hits += hit
    print(f"    the top hit IS one of the three input words in {hits}/{trials} = {hits / trials:.1%}")
    print(f"    when the offset a* - a is small, that rises to"
          f" {small_hits}/{small_trials} = {small_hits / small_trials:.1%}")
    print("  checked twice: the same count, restricted to the case where the offset is small,")
    print("  isolates the reason. This is why the published method excludes a, a* and b")
    print("  from the search before reporting an answer.")


if __name__ == "__main__":
    main()
