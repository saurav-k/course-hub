"""Lesson 63 - the dot product, the angle, and cosine similarity.

Two results, each checked twice.

1. Cauchy-Schwarz, |a.b| <= ||a|| ||b||, checked on 20,000 random pairs and again
   by confirming the ratio it bounds never leaves [-1, 1], which is what makes the
   arccos in the angle definition well defined.
2. That a raw dot product is not a similarity. The same retrieval runs twice over
   8,000 documents, ranked by dot product and by cosine, and both are scored
   against the topic labels.

Needs only numpy and pandas. Runs in a codebase, in Jupyter, or in Colab.
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "documents.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/documents.csv"

SENSORS = [
    "vibration_x", "vibration_y", "acoustic_db", "current_amp",
    "humidity_pct", "dust_index", "temp_c", "pressure_kpa",
]


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def main() -> None:
    frame = load()
    terms = [c for c in frame.columns if c not in ("doc_id", "topic")]
    counts = frame[terms].to_numpy(dtype=float)
    topic = frame["topic"].to_numpy()
    doc_id = frame["doc_id"].to_numpy()
    lengths = counts.sum(axis=1)
    norms = np.linalg.norm(counts, axis=1)

    print(f"{counts.shape[0]:,} documents over a {counts.shape[1]}-word vocabulary")
    print(f"length: min {lengths.min():.0f}, median {np.median(lengths):.0f}, max {lengths.max():.0f}")

    print("\n-- Cauchy-Schwarz, on 20,000 random pairs --")
    rng = np.random.default_rng(5)
    pairs = rng.integers(0, len(counts), size=(20_000, 2))
    dots = np.einsum("ij,ij->i", counts[pairs[:, 0]], counts[pairs[:, 1]])
    bound = norms[pairs[:, 0]] * norms[pairs[:, 1]]
    ratio = dots / bound
    print(f"|a.b| <= ||a|| ||b|| violated in {int(np.sum(np.abs(dots) > bound + 1e-8))} of 20,000")
    print(f"the ratio stays in [{ratio.min():.6f}, {ratio.max():.6f}]")
    assert ratio.min() >= -1 - 1e-9 and ratio.max() <= 1 + 1e-9
    print("checked twice: the bound holds, and the ratio it bounds is a valid cosine")

    print("\n-- the same thing in three dimensions, by hand --")
    d1 = np.array([10.0, 6.0, 4.0])
    d2 = 10.0 * d1
    d3 = np.array([2.0, 1.0, 20.0])
    for name, u, w in (("d1,d2", d1, d2), ("d1,d3", d1, d3), ("d2,d3", d2, d3)):
        c = cosine(u, w)
        print(f"  {name}: dot = {u @ w:8.1f}   cos = {c:.4f}   angle = {np.degrees(np.arccos(c)):.2f} deg")

    print("\n-- retrieval, ranked twice over the whole corpus --")
    query = int(np.where(doc_id == "d02546")[0][0])
    print(f"query {doc_id[query]}: topic {topic[query]}, {lengths[query]:.0f} words")
    dot_scores = counts @ counts[query]
    cos_scores = dot_scores / (norms * norms[query])
    dot_order = np.argsort(-dot_scores)[1:51]
    cos_order = np.argsort(-cos_scores)[1:51]

    print("  nearest by raw dot product:")
    for i in dot_order[:3]:
        print(f"    {doc_id[i]}  {topic[i]:<17}{lengths[i]:>6.0f} words")
    print("  nearest by cosine:")
    for i in cos_order[:3]:
        print(f"    {doc_id[i]}  {topic[i]:<17}{lengths[i]:>6.0f} words")
    print(f"  top-50 same topic: dot {np.mean(topic[dot_order] == topic[query]):.0%}"
          f"   cosine {np.mean(topic[cos_order] == topic[query]):.0%}")

    print("\n-- over 500 random queries, top 10 --")
    sample = rng.choice(len(counts), 500, replace=False)
    dot_hits = [np.mean(topic[np.argsort(-(counts @ counts[q]))[1:11]] == topic[q]) for q in sample]
    cos_hits = [
        np.mean(topic[np.argsort(-((counts @ counts[q]) / (norms * norms[q])))[1:11]] == topic[q])
        for q in sample
    ]
    print(f"  dot product: {np.mean(dot_hits):.1%}")
    print(f"  cosine     : {np.mean(cos_hits):.1%}")

    print("\n-- normalise once, and the two rankings coincide --")
    unit = counts / norms[:, None]
    by_cosine = np.argsort(-(unit @ unit[query]))[1:21]
    by_distance = np.argsort(np.linalg.norm(unit - unit[query], axis=1))[1:21]
    assert np.array_equal(by_cosine, by_distance)
    u, w = unit[query], unit[dot_order[0]]
    print(f"  ||u-v||^2 = {np.linalg.norm(u - w) ** 2:.8f}   2 - 2(u.v) = {2 - 2 * (u @ w):.8f}")
    print("  checked twice: on unit vectors the cosine order and the Euclidean order are one order")


if __name__ == "__main__":
    main()
