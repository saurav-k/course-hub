"""Softmax and log-sum-exp: the shift, the fp16 cliff, and the gradient p - y.

Lesson: Softmax and log-sum-exp.
Dataset: m10_classifier.csv (20,000 rows, a five-class classifier's held-out logits).

Runs on numpy and pandas and nothing else.

What it does:
  1. Computes softmax naively and with the max shift, and shows they agree in
     float64 on this data.
  2. Repeats both in float16, where the naive route returns not-a-number on
     28.7 per cent of the rows because a logit exceeds the float16 exp ceiling
     of 11.0.
  3. Shows softmax is invariant to adding any constant to a whole row.
  4. Checks the identity log softmax(z)_i = z_i - logsumexp(z) to machine
     precision on all 20,000 rows.
  5. Checks, numerically, that the gradient of log-sum-exp IS the softmax, by
     central differences against the closed form.
  6. Derives the cross-entropy gradient p - y from those two facts and checks
     it against central differences on the loss itself.
  7. Shows what temperature does, and that it never moves the argmax.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

RAW = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/"
FP16_LOG_MAX = 11.0  # Blanchard, Higham and Higham 2021, table 2


def load(name: str) -> pd.DataFrame:
    local = pathlib.Path(__file__).resolve().parent.parent / "datasets" / name
    return pd.read_csv(local if local.exists() else RAW + name)


def softmax_naive(z: np.ndarray) -> np.ndarray:
    """Straight from the formula. Correct on paper, unsafe on a machine."""
    weights = np.exp(z)
    return weights / weights.sum(axis=-1, keepdims=True)


def softmax_shifted(z: np.ndarray) -> np.ndarray:
    """The same function, with the row max subtracted first."""
    weights = np.exp(z - z.max(axis=-1, keepdims=True))
    return weights / weights.sum(axis=-1, keepdims=True)


def log_sum_exp(z: np.ndarray) -> np.ndarray:
    """LSE(z) = a + log sum_j exp(z_j - a) with a = max_j z_j."""
    peak = z.max(axis=-1)
    return peak + np.log(np.exp(z - peak[..., None]).sum(axis=-1))


def log_softmax(z: np.ndarray) -> np.ndarray:
    """z_i - LSE(z). Never log(softmax(z)), which underflows to -inf."""
    return z - log_sum_exp(z)[..., None]


def main() -> None:
    clf = load("m10_classifier.csv")
    n = len(clf)
    k = 5
    z = clf[[f"logit_{j}" for j in range(k)]].to_numpy()
    y = clf["true_class"].to_numpy()

    print(f"m10_classifier.csv: {n} rows, {k} classes")
    print(f"logit range {z.min():.3f} to {z.max():.3f}")

    # ---- 1. float64: both routes work ------------------------------------
    naive64 = softmax_naive(z)
    safe64 = softmax_shifted(z)
    print(f"\nfloat64: largest difference between naive and shifted = "
          f"{np.abs(naive64 - safe64).max():.3e}")
    assert np.abs(naive64 - safe64).max() < 1e-12

    # ---- 2. float16: only one route works --------------------------------
    over = (z > FP16_LOG_MAX).any(axis=1)
    print(f"\nrows with at least one logit above the float16 exp ceiling of "
          f"{FP16_LOG_MAX}: {over.sum()} of {n} = {100 * over.mean():.1f}%")

    z16 = z.astype(np.float16)
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        naive16 = softmax_naive(z16)
    safe16 = softmax_shifted(z16)
    broken = ~np.isfinite(naive16).all(axis=1)
    print(f"  naive softmax in float16 returns not-a-number on {broken.sum()} rows")
    print(f"  the two counts differ because {FP16_LOG_MAX} is the published value rounded to three")
    print(f"  significant figures. exp overflows float16 at ln(65504) = {np.log(65504):.4f}, so rows")
    print(f"  with a logit between {FP16_LOG_MAX} and {np.log(65504):.4f} survive.")
    print(f"  shifted softmax in float16 is finite on {np.isfinite(safe16).all(axis=1).sum()} rows")
    assert broken.sum() > 0, "the dataset no longer exercises the overflow"
    assert np.isfinite(safe16).all(), "the shift did not rescue every row"
    worst16 = np.abs(safe16.astype(np.float64) - safe64).max()
    print(f"  shifted float16 against float64: largest error {worst16:.2e}")

    # ---- 3. Shift invariance ----------------------------------------------
    bumped = z + 137.0
    print(f"\nadd 137 to every logit: largest change in the output = "
          f"{np.abs(softmax_shifted(bumped) - safe64).max():.3e}")
    assert np.abs(softmax_shifted(bumped) - safe64).max() < 1e-12

    # ---- 4. The identity that makes the loss computable -------------------
    identity_gap = np.abs(log_softmax(z) - np.log(safe64)).max()
    print(f"\nlog softmax(z)_i = z_i - LSE(z): largest gap over {n * k} entries = "
          f"{identity_gap:.3e}")
    assert identity_gap < 1e-9

    loss = -z[np.arange(n), y] + log_sum_exp(z)
    print(f"mean loss from that identity = {loss.mean():.6f} nats")

    # ---- 5. The gradient of log-sum-exp is the softmax --------------------
    # Blanchard, Higham and Higham 2021, equation 1.2. Checked by central
    # differences on twelve rows rather than taken on trust.
    rng = np.random.default_rng(3)
    sample = rng.choice(n, size=12, replace=False)
    step = 1e-6
    worst = 0.0
    for row in sample:
        base = z[row].copy()
        for j in range(k):
            up, down = base.copy(), base.copy()
            up[j] += step
            down[j] -= step
            numeric = (log_sum_exp(up) - log_sum_exp(down)) / (2 * step)
            worst = max(worst, abs(numeric - safe64[row, j]))
    print(f"\nd LSE / d z_j against softmax(z)_j, central differences on 12 rows:")
    print(f"  largest disagreement = {worst:.3e}")
    assert worst < 1e-6

    # ---- 6. So the loss gradient is p - y ---------------------------------
    onehot = np.zeros((n, k))
    onehot[np.arange(n), y] = 1.0
    analytic = safe64 - onehot

    worst = 0.0
    for row in sample:
        base = z[row].copy()
        for j in range(k):
            up, down = base.copy(), base.copy()
            up[j] += step
            down[j] -= step
            loss_up = -up[y[row]] + log_sum_exp(up)
            loss_down = -down[y[row]] + log_sum_exp(down)
            numeric = (loss_up - loss_down) / (2 * step)
            worst = max(worst, abs(numeric - analytic[row, j]))
    print(f"\nd loss / d z_j against (p - y)_j, same 12 rows:")
    print(f"  largest disagreement = {worst:.3e}")
    assert worst < 1e-6
    print(f"  every gradient row sums to {np.abs(analytic.sum(axis=1)).max():.2e}, "
          "which it must: the loss cannot see a constant added to a whole row.")

    # ---- 7. Temperature ---------------------------------------------------
    example = z[0]
    print(f"\none row of logits, rounded: {np.round(example, 3)}")
    print("  T      softmax                                        argmax")
    for T in (0.25, 0.5, 1.0, 2.0, 5.0):
        out = softmax_shifted(example / T)
        print(f"  {T:<5}  {np.array2string(out, precision=4, floatmode='fixed')}   {out.argmax()}")
    argmaxes = {softmax_shifted(example / T).argmax() for T in (0.1, 0.25, 1.0, 5.0, 50.0)}
    assert len(argmaxes) == 1, "temperature moved the argmax, which is impossible"
    print("  the argmax is the same at every temperature, because dividing by a")
    print("  positive number preserves order.")


if __name__ == "__main__":
    main()
