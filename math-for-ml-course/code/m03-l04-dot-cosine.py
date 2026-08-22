"""M03 L04 - The dot product, the angle, and cosine similarity.

    python3 m03-l04-dot-cosine.py

Two results, each checked twice.

1. The Cauchy-Schwarz inequality, |a.b| <= ||a|| ||b||, checked on every pair in a
   sample and again by confirming that the ratio it bounds never leaves [-1, 1],
   which is what makes the arccos in the angle definition well defined.
2. That the raw dot product is not a similarity. The same retrieval is run twice
   over 8,000 documents, once ranked by dot product and once by cosine, and the
   two rankings are scored against the topic labels.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "documents.csv"


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def main() -> None:
    frame = pd.read_csv(DATA)
    terms = [c for c in frame.columns if c not in ("doc_id", "topic")]
    counts = frame[terms].to_numpy(dtype=float)
    topic = frame["topic"].to_numpy()
    doc_id = frame["doc_id"].to_numpy()
    lengths = counts.sum(axis=1)
    norms = np.linalg.norm(counts, axis=1)

    print(f"{counts.shape[0]:,} documents over a {counts.shape[1]}-word vocabulary")
    print(f"document length: min {lengths.min():.0f}, median {np.median(lengths):.0f}, max {lengths.max():.0f}")

    print("\n-- Cauchy-Schwarz, on 20,000 random pairs --")
    rng = np.random.default_rng(5)
    pairs = rng.integers(0, len(counts), size=(20_000, 2))
    a = counts[pairs[:, 0]]
    b = counts[pairs[:, 1]]
    dots = np.einsum("ij,ij->i", a, b)
    bound = norms[pairs[:, 0]] * norms[pairs[:, 1]]
    violations = int(np.sum(np.abs(dots) > bound + 1e-8))
    ratio = dots / bound
    print(f"|a.b| <= ||a|| ||b|| violated in {violations} of 20,000 pairs")
    print(f"the ratio a.b / (||a|| ||b||) stays in [{ratio.min():.6f}, {ratio.max():.6f}]")
    assert violations == 0 and ratio.min() >= -1 - 1e-9 and ratio.max() <= 1 + 1e-9
    print("checked twice: the bound holds, and the ratio it bounds is a valid cosine")

    print("\n-- the same identity in three dimensions, by hand --")
    d1 = np.array([10.0, 6.0, 4.0])
    d2 = 10.0 * d1
    d3 = np.array([2.0, 1.0, 20.0])
    for name, u, v in (("d1,d2", d1, d2), ("d1,d3", d1, d3), ("d2,d3", d2, d3)):
        c = cosine(u, v)
        print(f"  {name}: dot = {u @ v:8.1f}   cos = {c:.4f}   angle = {np.degrees(np.arccos(c)):.2f} deg")

    print("\n-- retrieval, ranked twice over the whole corpus --")
    query = 2570
    print(f"query document {doc_id[query]}: topic {topic[query]}, {lengths[query]:.0f} words")
    dot_scores = counts @ counts[query]
    cos_scores = dot_scores / (norms * norms[query])
    dot_order = np.argsort(-dot_scores)[1:51]
    cos_order = np.argsort(-cos_scores)[1:51]

    print("  nearest by raw dot product:")
    for i in dot_order[:3]:
        print(f"    {doc_id[i]}  topic {topic[i]:<16} {lengths[i]:>5.0f} words")
    print("  nearest by cosine:")
    for i in cos_order[:3]:
        print(f"    {doc_id[i]}  topic {topic[i]:<16} {lengths[i]:>5.0f} words")

    print(f"  top-50 same-topic share: dot {np.mean(topic[dot_order] == topic[query]):.0%}"
          f"   cosine {np.mean(topic[cos_order] == topic[query]):.0%}")

    print("\n-- over 500 random queries, top 10 --")
    sample = rng.choice(len(counts), 500, replace=False)
    dot_hits, cos_hits = [], []
    for q in sample:
        s = counts @ counts[q]
        dot_hits.append(np.mean(topic[np.argsort(-s)[1:11]] == topic[q]))
        cos_hits.append(np.mean(topic[np.argsort(-(s / (norms * norms[q])))[1:11]] == topic[q]))
    print(f"  dot product: {np.mean(dot_hits):.1%} of the top 10 share the query's topic")
    print(f"  cosine     : {np.mean(cos_hits):.1%}")

    print("\n-- normalise once, and the two agree --")
    unit = counts / norms[:, None]
    by_cosine = np.argsort(-(unit @ unit[query]))[1:21]
    by_distance = np.argsort(np.linalg.norm(unit - unit[query], axis=1))[1:21]
    assert np.array_equal(by_cosine, by_distance)
    print("on unit vectors the cosine ranking and the Euclidean ranking are identical,")
    print("because ||u - v||^2 = 2 - 2(u.v) when both have norm 1")
    u, v = unit[query], unit[dot_order[0]]
    print(f"  check: ||u-v||^2 = {np.linalg.norm(u - v) ** 2:.8f}   2 - 2(u.v) = {2 - 2 * (u @ v):.8f}")


if __name__ == "__main__":
    main()
