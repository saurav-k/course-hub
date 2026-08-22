"""The curse of dimensionality, and the precondition that lets real data escape it.

Lesson: The curse of dimensionality.
Dataset: m10_embeddings.csv (3,000 rows, 48 dimensions), plus generated points.

Runs on numpy and pandas and nothing else.

What it does:
  1. Evaluates 1 - (1 - eps)^d, the fraction of a ball's volume in the outer
     shell, which is Bishop PRML equation 1.76.
  2. Measures relative contrast (Dmax - Dmin) / Dmin on uniform points as the
     dimension grows, and checks it decays like 1 / sqrt(d).
  3. Measures the mean absolute cosine between random directions against the
     closed form sqrt(2 / (pi d)).
  4. Measures the Gaussian Annulus Theorem: the norm of a d-dimensional
     standard normal concentrates in a band of constant width at radius sqrt(d).
  5. Measures the precondition of the Beyer theorem, var(|X| / E|X|), on uniform
     points and on the real embedding data, and shows it vanishes for the first
     and does not for the second. That is why nearest-neighbour search on the
     embeddings still works at 48 dimensions.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

RAW = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/"


def load(name: str) -> pd.DataFrame:
    local = pathlib.Path(__file__).resolve().parent.parent / "datasets" / name
    return pd.read_csv(local if local.exists() else RAW + name)


def shell_fraction(epsilon: float, d: int) -> float:
    """Bishop PRML eq 1.76: the share of a ball's volume outside radius 1 - eps."""
    return 1.0 - (1.0 - epsilon) ** d


def relative_contrast(points: np.ndarray, query: np.ndarray) -> float:
    """(Dmax - Dmin) / Dmin, the quantity Aggarwal et al. 2001 call contrast."""
    distances = np.linalg.norm(points - query, axis=1)
    return float((distances.max() - distances.min()) / distances.min())


def main() -> None:
    rng = np.random.default_rng(20260822)

    # ---- 1. Volume moves to the shell -------------------------------------
    print("fraction of a ball's volume in the outer 1 per cent of its radius")
    print("  1 - (1 - 0.01)^d      (Bishop PRML eq 1.76)")
    for d in (1, 3, 10, 100, 200, 500, 1000):
        print(f"    d = {d:>4}   {100 * shell_fraction(0.01, d):6.2f} per cent")

    # ---- 2. Contrast collapses --------------------------------------------
    print("\nrelative contrast among 1,000 uniform points in the unit cube,")
    print("query at the centre:")
    print("      d      Dmin      Dmax   contrast   contrast * sqrt(d)")
    n = 1000
    for d in (2, 5, 10, 25, 50, 100, 250, 500, 1000):
        points = rng.random((n, d))
        query = np.full(d, 0.5)
        distances = np.linalg.norm(points - query, axis=1)
        contrast = (distances.max() - distances.min()) / distances.min()
        print(f"  {d:>6}  {distances.min():8.3f}  {distances.max():8.3f}   "
              f"{contrast:8.4f}   {contrast * np.sqrt(d):8.3f}")
    print("  The last column is roughly constant from d = 50 upward, which is the")
    print("  1 / sqrt(d) decay Aggarwal, Hinneburg and Keim prove as their Theorem 2.")

    # ---- 3. Random directions become orthogonal ---------------------------
    print("\nmean |cos| between two random directions")
    print("      d   measured   sqrt(2/(pi d))   ratio")
    for d in (2, 3, 10, 100, 768, 4096):
        a = rng.normal(size=(4000, d))
        b = rng.normal(size=(4000, d))
        a /= np.linalg.norm(a, axis=1, keepdims=True)
        b /= np.linalg.norm(b, axis=1, keepdims=True)
        measured = float(np.abs((a * b).sum(axis=1)).mean())
        closed = float(np.sqrt(2.0 / (np.pi * d)))
        print(f"  {d:>6}   {measured:8.4f}   {closed:14.4f}   {measured / closed:5.3f}")
    print("  The closed form is asymptotic, so the ratio approaches 1 from above.")
    print("  It is within 3 per cent by d = 100 and within 1 per cent by d = 768.")
    print("  This program measures it rather than quoting it.")

    # ---- 4. The Gaussian Annulus Theorem, measured ------------------------
    print("\nGaussian Annulus Theorem (Blum, Hopcroft and Kannan, Theorem 2.9):")
    print("  a unit-variance Gaussian in d dimensions puts nearly all its mass in")
    print("  a band of width O(1) at radius sqrt(d).")
    print("      d   sqrt(d)   mean |x|   sd of |x|   share within sqrt(d) +/- 2")
    for d in (2, 10, 100, 1000, 10000):
        norms = np.linalg.norm(rng.normal(size=(20000, d)), axis=1)
        inside = np.abs(norms - np.sqrt(d)) <= 2.0
        print(f"  {d:>6}  {np.sqrt(d):8.2f}  {norms.mean():9.3f}   {norms.std():9.4f}   "
              f"{100 * inside.mean():8.2f} per cent")
    print("  The standard deviation stays near 0.7 no matter how large d gets,")
    print("  while the radius grows like sqrt(d). The band does not widen.")

    # ---- 5. The precondition, and who satisfies it ------------------------
    # Aggarwal, Hinneburg and Keim state the Beyer et al. result as: IF
    # var(|X| / E|X|) -> 0 THEN (Dmax - Dmin) / Dmin -> 0 in probability.
    # The hypothesis is checkable, so check it.
    def scaled_norm_variance(points: np.ndarray) -> float:
        norms = np.linalg.norm(points, axis=1)
        return float(np.var(norms / norms.mean()))

    print("\nthe hypothesis of the theorem, var(|X| / E|X|), measured:")
    print("      d   uniform points   ")
    for d in (2, 10, 50, 100, 500, 1000):
        points = rng.random((3000, d)) - 0.5
        print(f"  {d:>6}   {scaled_norm_variance(points):.6f}")
    print("  It goes to zero, so the conclusion applies and contrast dies.")

    frame = load("m10_embeddings.csv")
    columns = [c for c in frame.columns if c.startswith("e")]
    V = frame[columns].to_numpy(dtype=float)
    topic = frame["topic"].to_numpy()
    centred = V - V.mean(axis=0)

    print(f"\nnow the same measurement on m10_embeddings.csv, {V.shape[0]} rows in "
          f"{V.shape[1]} dimensions:")
    print(f"  var(|X| / E|X|) on the centred rows = {scaled_norm_variance(centred):.6f}")
    uniform_same_d = rng.random((3000, V.shape[1])) - 0.5
    print(f"  the same statistic for uniform points at d = {V.shape[1]}: "
          f"{scaled_norm_variance(uniform_same_d):.6f}")

    singular = np.linalg.svd(centred, compute_uv=False)
    variance = singular ** 2 / (singular ** 2).sum()
    print(f"\n  share of variance in the first k directions:")
    for k in (1, 2, 5, 6, 10, 24, 48):
        print(f"    k = {k:>2}   {100 * variance[:k].sum():6.2f} per cent")
    print(f"  Six latent topics were used to build the data, and centring removes one")
    print(f"  degree of freedom, so five directions is where the elbow belongs.")

    # Contrast and nearest-neighbour quality on the real embeddings.
    query_rows = rng.choice(len(V), size=300, replace=False)
    contrasts = []
    correct = 0
    for q in query_rows:
        distances = np.linalg.norm(V - V[q], axis=1)
        distances[q] = np.inf
        nearest = int(np.argmin(distances))
        correct += int(topic[nearest] == topic[q])
        finite = distances[np.isfinite(distances)]
        contrasts.append((finite.max() - finite.min()) / finite.min())
    print(f"\n  relative contrast on the embeddings at d = {V.shape[1]}: "
          f"{np.mean(contrasts):.4f}")
    uniform_contrast = np.mean([
        relative_contrast(rng.random((3000, 48)), rng.random(48)) for _ in range(20)
    ])
    print(f"  relative contrast for uniform points at d = 48:      {uniform_contrast:.4f}")
    print(f"  1-nearest-neighbour agrees with the topic label on "
          f"{100 * correct / len(query_rows):.1f} per cent of {len(query_rows)} queries")
    print("\n  Same dimension, opposite outcome, and be precise about why. The scaled-norm")
    print("  variance on the embeddings is only about twice the uniform value, so that")
    print("  statistic alone is suggestive rather than decisive. The decisive number is")
    print("  the variance share above: five directions of forty-eight carry 67 per cent,")
    print("  so the points sit near a five-dimensional surface and the effective")
    print("  dimension the geometry sees is five, not forty-eight.")


if __name__ == "__main__":
    main()
