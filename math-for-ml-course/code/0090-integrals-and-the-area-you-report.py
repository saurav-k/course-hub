"""Lesson 0090 - the area under a curve, computed two ways that must agree.

Implements two named results.

1.  The trapezoid rule for a definite integral, applied to the ROC curve. This
    is what a library means when it reports an area: sort by score, sweep the
    threshold, accumulate trapezoids.

2.  The identity of Bamber (1975) and Hanley and McNeil (1982),

        AUC = P(a random positive scores above a random negative)

    which says the area is a statement about ranking and has nothing to do
    with geometry. The program computes it by counting ranked pairs, with ties
    counted as one half, and the two answers agree to fourteen decimal places.

    Twenty thousand rows is 3,401 x 16,599 = 56,453,199 pairs. Counting them
    directly is possible here and is deliberately included, because seeing the
    brute-force count agree with the rank-sum shortcut is the point.

    python3 0090-integrals-and-the-area-you-report.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "failures.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/failures.csv"


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def sigmoid(z: np.ndarray) -> np.ndarray:
    out = np.empty_like(z, dtype=float)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    e = np.exp(z[~pos])
    out[~pos] = e / (1.0 + e)
    return out


def fitted_scores(frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Fit a logistic model by Newton's method and return (label, score).

    The dataset ships features and a label, not scores. Scores are what a model
    produces, so the program produces them, in ten lines and no library. A
    reader who has read lesson 0081 has already seen this fit.
    """
    y = frame["failed"].to_numpy(dtype=float)
    raw = np.column_stack([
        np.ones(len(frame)),
        np.log(frame["hours_since_service"].to_numpy(dtype=float)),
        frame["load_pct"].to_numpy(dtype=float) ** 2,
        np.log(frame["vibration_mm_s"].to_numpy(dtype=float)),
        frame["coolant_c"].to_numpy(dtype=float),
    ])
    centre, scale = raw.mean(axis=0), raw.std(axis=0)
    centre[0], scale[0] = 0.0, 1.0
    x = (raw - centre) / scale

    w = np.zeros(x.shape[1])
    for _ in range(50):
        p = sigmoid(x @ w)
        weights = np.clip(p * (1.0 - p), 1e-12, None)
        w -= np.linalg.solve(
            (x * weights[:, None]).T @ x / len(y) + 1e-10 * np.eye(len(w)),
            x.T @ (p - y) / len(y),
        )
    return y, sigmoid(x @ w)


def roc_points(label: np.ndarray, score: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """The ROC curve, one point per distinct threshold.

    Sort by descending score and sweep. At each distinct score the point is
    (false positives so far / all negatives, true positives so far / all
    positives). Ties must be consumed as a block, or the curve gains staircase
    corners that are not there.
    """
    order = np.argsort(-score, kind="mergesort")
    y = label[order]
    s = score[order]

    positives = float(y.sum())
    negatives = float(len(y) - positives)

    tp = np.cumsum(y)
    fp = np.cumsum(1.0 - y)

    # Keep only the last index of each run of equal scores.
    last_of_run = np.r_[np.flatnonzero(np.diff(s)), len(s) - 1]
    return np.r_[0.0, fp[last_of_run] / negatives], np.r_[0.0, tp[last_of_run] / positives]


def auc_trapezoid(fpr: np.ndarray, tpr: np.ndarray) -> float:
    """The definite integral of the ROC curve, by the trapezoid rule.

    A trapezoid rather than a rectangle because a block of tied scores produces
    a sloped segment, and a rectangle would systematically mis-measure it.
    """
    return float(np.sum(np.diff(fpr) * (tpr[:-1] + tpr[1:]) / 2.0))


def auc_by_ranks(label: np.ndarray, score: np.ndarray) -> float:
    """The same number as a probability, via the Mann-Whitney rank sum.

    Average ranks handle ties, which is what makes this exactly equal to
    counting a tie as half a win.
    """
    order = np.argsort(score, kind="mergesort")
    ranks = np.empty(len(score), dtype=float)
    sorted_scores = score[order]
    i = 0
    while i < len(sorted_scores):
        j = i
        while j + 1 < len(sorted_scores) and sorted_scores[j + 1] == sorted_scores[i]:
            j += 1
        ranks[order[i : j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1

    positives = label == 1
    n_pos = int(positives.sum())
    n_neg = len(label) - n_pos
    rank_sum = float(ranks[positives].sum())
    return (rank_sum - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def auc_by_brute_force(label: np.ndarray, score: np.ndarray) -> float:
    """Every positive against every negative, ties worth one half.

    Chunked so the pair matrix never has to exist all at once.
    """
    pos = np.sort(score[label == 1])
    neg = np.sort(score[label == 0])
    wins = 0.0
    for start in range(0, len(pos), 512):
        block = pos[start : start + 512][:, None]
        wins += float(np.sum(block > neg[None, :]))
        wins += 0.5 * float(np.sum(block == neg[None, :]))
    return wins / (len(pos) * len(neg))


def main() -> None:
    frame = load()
    label, score = fitted_scores(frame)
    label = label.astype(int)
    n_pos = int(label.sum())
    n_neg = len(label) - n_pos
    print(f"loaded failures.csv: {len(frame)} rows, {n_pos} positive, {n_neg} negative")
    print(f"that is {n_pos * n_neg:,} positive-negative pairs\n")

    fpr, tpr = roc_points(label, score)
    print(f"the ROC curve has {len(fpr)} points")

    area = auc_trapezoid(fpr, tpr)
    ranks = auc_by_ranks(label, score)
    brute = auc_by_brute_force(label, score)

    print(f"\n  1. trapezoid rule, an integral   : {area:.14f}")
    print(f"  2. Mann-Whitney rank sum         : {ranks:.14f}")
    print(f"  3. counting all {n_pos * n_neg:,} pairs : {brute:.14f}")
    print(f"\n  largest gap between the three: {max(abs(area - ranks), abs(ranks - brute)):.3e}")

    print("\nthe trapezoid rule converging, on a coarsened curve")
    print("  keeping every k-th threshold and re-integrating:")
    for k in (2048, 512, 128, 32, 8, 1):
        idx = np.unique(np.r_[0, np.arange(0, len(fpr), k), len(fpr) - 1])
        coarse = auc_trapezoid(fpr[idx], tpr[idx])
        print(f"    every {k:5d}th point ({len(idx):5d} points): {coarse:.10f}  "
              f"error {abs(coarse - area):.2e}")

    print("\nrectangles instead of trapezoids, and when the choice matters")
    left = float(np.sum(np.diff(fpr) * tpr[:-1]))
    right = float(np.sum(np.diff(fpr) * tpr[1:]))
    print(f"  left rectangles  : {left:.10f}   error {abs(left - area):.2e}")
    print(f"  right rectangles : {right:.10f}   error {abs(right - area):.2e}")
    print("  All three agree exactly, and that is not luck: the fitted scores are")
    print("  all distinct, so every step of the sweep moves either right or up and")
    print("  never both. With no sloped segment there is nothing for a rectangle to")
    print("  get wrong.")

    print("\n  Now round the scores to two decimals, which creates ties:")
    tied = np.round(score, 2)
    f2, t2 = roc_points(label, tied)
    a2 = auc_trapezoid(f2, t2)
    l2 = float(np.sum(np.diff(f2) * t2[:-1]))
    r2 = float(np.sum(np.diff(f2) * t2[1:]))
    print(f"    {len(f2)} curve points instead of {len(fpr)}")
    print(f"    trapezoid        : {a2:.10f}")
    print(f"    left rectangles  : {l2:.10f}   error {abs(l2 - a2):.2e}")
    print(f"    right rectangles : {r2:.10f}   error {abs(r2 - a2):.2e}")
    print(f"    and the rank-sum answer is still {auc_by_ranks(label, tied):.10f}")
    print("    The trapezoid tracks the rank sum through the ties. The rectangles")
    print("    bracket it, one low and one high. THAT is why the rule is a trapezoid.")


if __name__ == "__main__":
    main()
