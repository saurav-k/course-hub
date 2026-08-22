"""Cross-entropy, computed twice, and the accuracy that disagrees with it.

Lesson: Cross-entropy, and why it is the loss.
Dataset: m10_classifier.csv (20,000 rows, a five-class classifier's held-out logits).

Runs on numpy and pandas and nothing else.

What it does:
  1. Computes the per-row loss straight from the definition, -sum p*log q over
     all five classes, with the one-hot label as p.
  2. Computes it the way a framework does, -z_true + logsumexp(z), and asserts
     the two agree to floating-point tolerance. Those are the same number by an
     identity, not by approximation.
  3. Shows that H(p, q) = H(p) + KL(p || q) on the label marginal.
  4. Measures accuracy and mean cross-entropy on the same 20,000 rows and shows
     where they disagree, which is the whole reason the loss is not the metric.
  5. Reports the reliability curve, measured rather than assumed.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

RAW = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/"


def load(name: str) -> pd.DataFrame:
    local = pathlib.Path(__file__).resolve().parent.parent / "datasets" / name
    return pd.read_csv(local if local.exists() else RAW + name)


def softmax(logits: np.ndarray) -> np.ndarray:
    """Row-wise softmax, shifted by the row max so exp never overflows."""
    shifted = logits - logits.max(axis=1, keepdims=True)
    weights = np.exp(shifted)
    return weights / weights.sum(axis=1, keepdims=True)


def log_sum_exp(logits: np.ndarray) -> np.ndarray:
    """log sum_j exp(z_j), one value per row, computed the safe way."""
    peak = logits.max(axis=1)
    return peak + np.log(np.exp(logits - peak[:, None]).sum(axis=1))


def cross_entropy_from_definition(p: np.ndarray, q: np.ndarray) -> float:
    """H(p, q) = -sum_i p_i log2(q_i), for one pair of distributions."""
    total = 0.0
    for pi, qi in zip(p, q):
        if pi > 0.0:
            total += pi * np.log2(qi)
    return -total


def main() -> None:
    clf = load("m10_classifier.csv")
    n = len(clf)
    k = 5
    logits = clf[[f"logit_{j}" for j in range(k)]].to_numpy()
    truth = clf["true_class"].to_numpy()

    probs = softmax(logits)

    # ---- 1. The definition, on every row ---------------------------------
    # The label is one-hot, so the sum over five classes collapses to one term.
    # Doing it the long way first shows why.
    onehot = np.zeros((n, k))
    onehot[np.arange(n), truth] = 1.0
    slow = -(np.where(onehot > 0, onehot * np.log(probs), 0.0)).sum(axis=1)

    # ---- 2. The way a framework does it ----------------------------------
    fast = -logits[np.arange(n), truth] + log_sum_exp(logits)

    gap = np.abs(slow - fast).max()
    assert gap < 1e-9, f"the two routes disagree by {gap}"

    print(f"m10_classifier.csv: {n} rows, {k} classes")
    print(f"\nroute 1, -sum p log q over all {k} classes : mean {slow.mean():.6f} nats")
    print(f"route 2, -z_true + logsumexp(z)           : mean {fast.mean():.6f} nats")
    print(f"largest disagreement over {n} rows     : {gap:.3e}")

    loss_nats = float(fast.mean())
    print(f"\nmean cross-entropy = {loss_nats:.4f} nats = {loss_nats / np.log(2):.4f} bits")

    # ---- 3. H(p, q) = H(p) + KL(p || q) on the marginals -----------------
    p_true = np.bincount(truth, minlength=k) / n
    q_model = probs.mean(axis=0)
    h_true = float(-(p_true * np.log2(p_true)).sum())
    h_cross = cross_entropy_from_definition(p_true, q_model)
    kl = float((p_true * np.log2(p_true / q_model)).sum())
    print(f"\non the label marginal:")
    print(f"  p (true share)      = {np.round(p_true, 4)}")
    print(f"  q (mean prediction) = {np.round(q_model, 4)}")
    print(f"  H(p)                = {h_true:.6f} bits   the floor")
    print(f"  H(p, q)             = {h_cross:.6f} bits   what you pay")
    print(f"  KL(p || q)          = {kl:.6f} bits   the excess")
    assert abs(h_cross - (h_true + kl)) < 1e-12
    print(f"  H(p) + KL           = {h_true + kl:.6f} bits, equal to H(p, q)")

    # ---- 4. Accuracy against loss ----------------------------------------
    predicted = probs.argmax(axis=1)
    correct = predicted == truth
    print(f"\naccuracy            = {correct.mean():.4f}")
    print(f"mean loss on correct rows = {fast[correct].mean():.4f} nats")
    print(f"mean loss on wrong rows   = {fast[~correct].mean():.4f} nats")
    print(f"worst single row          = {fast.max():.4f} nats "
          f"({fast.max() / np.median(fast):.0f}x the median of {np.median(fast):.4f})")
    worst = np.argsort(fast)[-int(0.01 * n):]
    print(f"the worst 1% of rows carry {100 * fast[worst].sum() / fast.sum():.1f}% of the total loss")

    # ---- 5. Reliability, measured ----------------------------------------
    confidence = probs.max(axis=1)
    print("\nreliability curve (confidence bin -> mean confidence, accuracy, rows)")
    for lo in np.arange(0.2, 1.0, 0.1):
        inside = (confidence >= lo) & (confidence < lo + 0.1)
        if inside.sum() > 50:
            print(f"  {lo:.1f}-{lo + 0.1:.1f}   {confidence[inside].mean():.4f}   "
                  f"{correct[inside].mean():.4f}   {inside.sum():6d}")
    print(f"\nmean confidence {confidence.mean():.4f} against accuracy {correct.mean():.4f}: "
          "the average hides a curve that crosses.")


if __name__ == "__main__":
    main()
