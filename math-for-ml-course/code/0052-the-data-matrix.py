"""Lesson 52 - the data matrix, and how a thing with no numbers becomes a vector.

Three results, each checked twice.

1. The Gram matrix of a centred, scaled data matrix IS the correlation matrix.
   Computed as Z^T Z / (n - 1) and again with pandas' own .corr().
2. A one-hot vector times a matrix selects one row. Computed as a matrix product
   and again as an index, with the flop counts for both.
3. The analogy caveat, measured rather than asserted: word vectors are built from
   the corpus, the offset a* - a + b is scored against every word, and the top hit
   is reported both with the three input words allowed and with them excluded.

Needs only numpy and pandas. Runs in a codebase, in Jupyter, or in Colab.
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "sensors.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/sensors.csv"

SENSORS = [
    "vibration_x", "vibration_y", "acoustic_db", "current_amp",
    "humidity_pct", "dust_index", "temp_c", "pressure_kpa",
]


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


DOCUMENTS_LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "documents.csv"
DOCUMENTS_URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/documents.csv"
)


def load_documents() -> pd.DataFrame:
    return pd.read_csv(DOCUMENTS_LOCAL) if DOCUMENTS_LOCAL.exists() else pd.read_csv(DOCUMENTS_URL)


def main() -> None:
    frame = load()
    X = frame[SENSORS].to_numpy(dtype=float)
    n, d = X.shape
    print(f"X is (n_samples, n_features) = {X.shape}: rows are readings, columns are sensors")
    print(f"  row 0    is one reading: {np.round(X[0], 3)}")
    print(f"  column 0 is one sensor : first three are {np.round(X[:3, 0], 3)}")

    print("\n-- centre, scale, and the Gram matrix becomes the correlation matrix --")
    Z = (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)
    G = Z.T @ Z / (n - 1)
    R = frame[SENSORS].corr().to_numpy()
    print(f"  Z^T Z / (n-1) is {G.shape}, symmetric to {np.abs(G - G.T).max():.3e}")
    print(f"  max |Z^T Z/(n-1) - pandas .corr()| = {np.abs(G - R).max():.3e}")
    assert np.allclose(G, R)
    print("checked twice: one matrix product reproduces every pairwise correlation")
    print(f"  correlation(vibration_x, vibration_y) = {G[0, 1]:.4f}")
    print(f"  cost of X^T X: about {2 * n * d * d:,} flops, and it is symmetric so half is enough")

    print("\n-- a batched linear layer is one matrix product --")
    W = np.random.default_rng(0).normal(0.0, 0.1, size=(3, d))
    print(f"  X {X.shape} @ W.T {W.T.shape} -> {(X @ W.T).shape}, "
          f"which is {n * 3:,} dot products of length {d}")

    print("\n-- categorical data has no distance until you give it one --")
    machines = sorted(frame["machine"].unique())
    onehot = np.eye(len(machines))
    pairwise = {round(float(np.linalg.norm(onehot[i] - onehot[j])), 6)
                for i in range(len(machines)) for j in range(i + 1, len(machines))}
    print(f"  {len(machines)} machines {machines}, one-hot")
    print(f"  every pairwise distance is the same: {sorted(pairwise)}  (which is sqrt 2)")

    print("\n-- one-hot times a matrix is a row lookup --")
    E = np.random.default_rng(1).normal(0.0, 0.02, size=(200, 8))
    index = 137
    e = np.zeros(200)
    e[index] = 1.0
    assert np.array_equal(e @ E, E[index])
    print(f"  e_{index} @ E equals E[{index}] exactly: True")
    vocabulary, d_model = 37_000, 512
    print(f"  at a real size, {vocabulary:,} by {d_model}:")
    print(f"    the one-hot basis written out: {vocabulary * vocabulary:,} numbers")
    print(f"    the embedding matrix E       : {vocabulary * d_model:,} numbers "
          f"({vocabulary / d_model:.0f}x smaller)")
    print(f"    the product costs about {2 * vocabulary * d_model:,} flops per token")
    print("    the lookup costs nothing, which is why every library does the lookup")

    print("\n-- a count-based embedding, built from the corpus --")
    docs = load_documents()
    topics = sorted(docs["topic"].unique())
    terms = [c for c in docs.columns if c not in ("doc_id", "topic")]
    counts = docs[terms].to_numpy(dtype=float)
    profile = np.zeros((len(terms), len(topics)))
    for t, topic in enumerate(topics):
        profile[:, t] = counts[docs["topic"].to_numpy() == topic].sum(axis=0)
    profile = profile / profile.sum(axis=1, keepdims=True)
    unit = profile / np.linalg.norm(profile, axis=1, keepdims=True)
    print(f"  every one of the {len(terms)} words is now a point in R^{len(topics)}")
    print(f"  the four axes are {topics}")
    for word in ("gradient", "flour", "telescope", "the"):
        print(f"    {word:<10} {np.round(profile[terms.index(word)], 3)}")
    print("  'the' sits near the middle because every topic uses it, which is the")
    print("  distributional idea: a word is described by the company it keeps")

    print("\n-- the analogy, measured rather than asserted --")
    def offset_scores(a: str, a_star: str, b: str) -> np.ndarray:
        v = unit[terms.index(a_star)] - unit[terms.index(a)] + unit[terms.index(b)]
        return unit @ (v / np.linalg.norm(v))

    a, a_star, b = "model", "gradient", "flour"
    order = np.argsort(-offset_scores(a, a_star, b))
    inputs = {a, a_star, b}
    print(f"  '{a}' is to '{a_star}' as '{b}' is to ...?")
    print(f"    top four, inputs allowed : {[terms[i] for i in order[:4]]}")
    print(f"    top four, inputs excluded: {[terms[i] for i in order if terms[i] not in inputs][:4]}")

    print("\n  across 3,000 random word triples from this corpus:")
    rng = np.random.default_rng(0)
    hits = trials = small_hits = small_trials = 0
    for _ in range(3_000):
        i, j, k = rng.choice(len(terms), 3, replace=False)
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
    print(f"    the top hit IS one of the three input words {hits}/{trials} = {hits / trials:.1%} of the time")
    print(f"    when the offset a* - a is small, that rises to "
          f"{small_hits}/{small_trials} = {small_hits / small_trials:.1%}")
    print("  checked twice: the same count restricted to a small offset isolates the reason.")
    print("  This is why the published method excludes a, a* and b before reporting an answer.")


if __name__ == "__main__":
    main()
