"""Cosine similarity against its own baseline, on an anisotropic embedding space.

Lesson: Cosine similarity and where it is the wrong tool.
Dataset: m10_embeddings.csv (3,000 rows, 48 dimensions, 6 latent topics).

Runs on numpy and pandas and nothing else.

What it does:
  1. Computes cosine similarity from the definition and again as a dot product
     of length-one rows, and asserts they agree.
  2. Measures the random-pair baseline. If the space were isotropic the baseline
     would be zero. It is not, and the number it actually is tells you how to
     read every score the system reports.
  3. Compares a same-topic pair, a different-topic pair and the baseline, and
     shows that a score which reads as a strong match is at or below chance.
  4. Subtracts the mean vector and repeats. One subtraction turns a 0.27 gap
     into a 0.76 gap.
  5. Shows the ranking split between cosine and Euclidean, and that the two
     agree exactly once the rows are normalised.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

RAW = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/"


def load(name: str) -> pd.DataFrame:
    local = pathlib.Path(__file__).resolve().parent.parent / "datasets" / name
    return pd.read_csv(local if local.exists() else RAW + name)


def cosine_from_definition(a, b) -> float:
    """a.b / (|a| |b|), written as three loops so nothing is hidden."""
    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0
    for ai, bi in zip(a, b):
        dot += ai * bi
        norm_a += ai * ai
        norm_b += bi * bi
    return float(dot / (np.sqrt(norm_a) * np.sqrt(norm_b)))


def unit_rows(matrix: np.ndarray) -> np.ndarray:
    return matrix / np.linalg.norm(matrix, axis=1, keepdims=True)


def main() -> None:
    frame = load("m10_embeddings.csv")
    columns = [c for c in frame.columns if c.startswith("e")]
    V = frame[columns].to_numpy(dtype=float)
    topic = frame["topic"].to_numpy()
    n, d = V.shape
    print(f"m10_embeddings.csv: {n} rows, {d} dimensions, {frame['topic'].nunique()} topics")

    # ---- 1. Two routes to one number --------------------------------------
    U = unit_rows(V)
    slow = cosine_from_definition(V[0], V[1])
    fast = float(U[0] @ U[1])
    assert abs(slow - fast) < 1e-12
    print(f"\ncosine(row 0, row 1): definition {slow:.9f}, unit-row dot product {fast:.9f}")

    # ---- 2. The baseline ---------------------------------------------------
    rng = np.random.default_rng(1)
    i = rng.integers(0, n, 200000)
    j = rng.integers(0, n, 200000)
    keep = i != j
    i, j = i[keep], j[keep]
    scores = (U[i] * U[j]).sum(axis=1)
    same = topic[i] == topic[j]

    print(f"\nrandom-pair cosine over {len(i)} pairs:")
    print(f"  mean   {scores.mean():.4f}      <- this is the chance level, not zero")
    print(f"  sd     {scores.std():.4f}")
    print(f"  range  {scores.min():.4f} to {scores.max():.4f}")
    print(f"  an isotropic space would give a mean of 0.0000")

    # ---- 3. The reading that matters ---------------------------------------
    print(f"\n  same-topic pairs      {scores[same].mean():.4f}   "
          f"excess over chance {scores[same].mean() - scores.mean():+.4f}")
    print(f"  different-topic pairs {scores[~same].mean():.4f}   "
          f"excess over chance {scores[~same].mean() - scores.mean():+.4f}")
    print(f"\n  A different-topic pair scores {scores[~same].mean():.4f}. Reported as a percentage")
    print(f"  match that reads as {100 * scores[~same].mean():.0f} per cent, and it is below chance.")

    # ---- 4. One subtraction ------------------------------------------------
    centred = unit_rows(V - V.mean(axis=0))
    centred_scores = (centred[i] * centred[j]).sum(axis=1)
    print(f"\nafter subtracting the mean vector and renormalising:")
    print(f"  baseline              {centred_scores.mean():+.4f}")
    print(f"  same-topic pairs      {centred_scores[same].mean():+.4f}")
    print(f"  different-topic pairs {centred_scores[~same].mean():+.4f}")
    raw_gap = scores[same].mean() - scores[~same].mean()
    new_gap = centred_scores[same].mean() - centred_scores[~same].mean()
    print(f"  the gap between the two populations goes from {raw_gap:.4f} to {new_gap:.4f}, "
          f"a factor of {new_gap / raw_gap:.1f}")
    print(f"  mean vector length before centring: {np.linalg.norm(V.mean(axis=0)):.4f} "
          f"of a maximum of 1.0")

    # ---- 5. Cosine against Euclidean ---------------------------------------
    query = 0
    cos_rank = np.argsort(-(U @ U[query]))
    euc_rank = np.argsort(np.linalg.norm(V - V[query], axis=1))
    unit_euc_rank = np.argsort(np.linalg.norm(U - U[query], axis=1))
    print(f"\ntop 5 neighbours of row {query}:")
    print(f"  by cosine            {cos_rank[1:6].tolist()}")
    print(f"  by Euclidean on raw  {euc_rank[1:6].tolist()}")
    print(f"  by Euclidean on unit {unit_euc_rank[1:6].tolist()}")
    print("  All three agree here only because every row of this dataset already has")
    print("  length one. On data where the lengths differ the first two split:")
    q = np.array([1.0, 1.0, 0.0])
    d1 = np.array([10.0, 10.0, 0.0])
    d2 = np.array([1.0, 1.0, 1.0])
    for name, doc in (("d1 = (10,10,0)", d1), ("d2 = (1,1,1)", d2)):
        print(f"    {name}  Euclidean {np.linalg.norm(q - doc):7.4f}   "
              f"cosine {cosine_from_definition(q, doc):.4f}")
    print("    Euclidean ranks d2 first, cosine ranks d1 first. Opposite answers.")
    assert (cos_rank == unit_euc_rank).all(), "normalised, the two orders must be identical"
    print("  Once the rows are length one the two orders are identical, every row,")
    print("  because |x - y|^2 = 2 - 2 cos when both have length one.")

    lhs = float(np.linalg.norm(U[0] - U[1]) ** 2)
    rhs = float(2.0 - 2.0 * (U[0] @ U[1]))
    assert abs(lhs - rhs) < 1e-12
    print(f"  check: {lhs:.9f} = {rhs:.9f}")

    # ---- 6. What the raw scores would have told you ------------------------
    threshold = 0.75
    flagged = scores > threshold
    print(f"\na fixed threshold of {threshold} on the raw scores:")
    print(f"  keeps {100 * flagged.mean():.1f} per cent of all pairs")
    print(f"  of which {100 * same[flagged].mean():.1f} per cent are same-topic, "
          f"against {100 * same.mean():.1f} per cent in the population")
    flagged_c = centred_scores > threshold
    print(f"the same threshold on the centred scores:")
    print(f"  keeps {100 * flagged_c.mean():.1f} per cent of all pairs")
    print(f"  of which {100 * same[flagged_c].mean():.1f} per cent are same-topic")


if __name__ == "__main__":
    main()
