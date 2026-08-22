"""KL divergence: non-negative, asymmetric, and infinite on an unseen event.

Lesson: KL divergence.
Dataset: m10_classifier.csv (20,000 rows) and m10_signals.csv (12,000 rows).

Runs on numpy and pandas and nothing else.

What it does:
  1. Computes KL(p || q) from the definition and again as H(p,q) - H(p), and
     asserts the two agree. That subtraction IS the definition's meaning.
  2. Checks Gibbs' inequality, KL >= 0 with equality only when p = q, on ten
     thousand random pairs of distributions. Non-negativity is a theorem, so it
     is worth failing to break rather than believing.
  3. Measures the asymmetry on a real pair and reports both directions.
  4. Shows the infinity: one outcome the second distribution rules out.
  5. Fits a single-mode approximation to a two-mode target in each direction
     and shows the mean-seeking against mode-seeking split as numbers.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

RAW = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/"


def load(name: str) -> pd.DataFrame:
    local = pathlib.Path(__file__).resolve().parent.parent / "datasets" / name
    return pd.read_csv(local if local.exists() else RAW + name)


def kl_from_definition(p, q) -> float:
    """KL(p || q) = sum_i p_i log2(p_i / q_i), one term at a time.

    Returns infinity when q assigns zero to something p does not, which is the
    correct answer and not an error.
    """
    total = 0.0
    for pi, qi in zip(p, q):
        if pi > 0.0:
            if qi <= 0.0:
                return float("inf")
            total += pi * np.log2(pi / qi)
    return total


def entropy(p: np.ndarray) -> float:
    p = np.asarray(p, dtype=float)
    p = p[p > 0.0]
    return float(-(p * np.log2(p)).sum())


def cross_entropy(p: np.ndarray, q: np.ndarray) -> float:
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    keep = p > 0.0
    return float(-(p[keep] * np.log2(q[keep])).sum())


def main() -> None:
    clf = load("m10_classifier.csv")
    k = 5
    n = len(clf)
    logits = clf[[f"logit_{j}" for j in range(k)]].to_numpy()
    truth = clf["true_class"].to_numpy()
    shifted = logits - logits.max(axis=1, keepdims=True)
    probs = np.exp(shifted)
    probs /= probs.sum(axis=1, keepdims=True)

    p = np.bincount(truth, minlength=k) / n
    q = probs.mean(axis=0)

    # ---- 1. Two routes to the same number --------------------------------
    direct = kl_from_definition(p, q)
    subtracted = cross_entropy(p, q) - entropy(p)
    assert abs(direct - subtracted) < 1e-12
    print(f"m10_classifier.csv: {n} rows")
    print(f"\np = {np.round(p, 4)}   the true class shares")
    print(f"q = {np.round(q, 4)}   the model's average prediction")
    print(f"\nKL(p || q) from the definition        = {direct:.6f} bits")
    print(f"KL(p || q) as H(p,q) - H(p)           = {subtracted:.6f} bits")

    # ---- 2. Gibbs' inequality, tested rather than trusted ----------------
    rng = np.random.default_rng(0)
    smallest = float("inf")
    for _ in range(10000):
        a = rng.dirichlet(np.full(k, 0.7))
        b = rng.dirichlet(np.full(k, 0.7))
        value = kl_from_definition(a, b)
        assert value >= -1e-12, f"KL went negative: {value}"
        smallest = min(smallest, value)
    print(f"\nGibbs' inequality over 10,000 random pairs of distributions:")
    print(f"  smallest KL seen = {smallest:.6f} bits, and none was negative")
    same = kl_from_definition(p, p)
    assert abs(same) < 1e-12
    print(f"KL(p || p) = {same:.2e}, zero as the equality case requires")

    # ---- 3. The asymmetry -------------------------------------------------
    forward = kl_from_definition(p, q)
    reverse = kl_from_definition(q, p)
    print(f"\nKL(p || q) = {forward:.6f} bits")
    print(f"KL(q || p) = {reverse:.6f} bits")
    print(f"ratio      = {reverse / forward:.4f}. Same two distributions, two answers.")

    # ---- 4. The infinity --------------------------------------------------
    blocked = q.copy()
    blocked[4] = 0.0
    blocked /= blocked.sum()
    print(f"\nnow let the model rule class 4 out entirely, q4 = 0:")
    print(f"  KL(p || q) = {kl_from_definition(p, blocked)}   because p4 = {p[4]:.4f} > 0")
    print(f"  KL(q || p) = {kl_from_definition(blocked, p):.6f} bits, still finite")

    # ---- 5. Mean-seeking against mode-seeking, as numbers -----------------
    # A two-mode target on a grid, approximated by the best single Gaussian
    # under each direction of KL. Grid search, so there is no optimiser to
    # trust and every number is checkable.
    grid = np.linspace(-8.0, 8.0, 1601)
    target = (0.5 * np.exp(-0.5 * ((grid + 3.0) / 0.8) ** 2)
              + 0.5 * np.exp(-0.5 * ((grid - 3.0) / 0.8) ** 2))
    target /= target.sum()

    best = {"forward": (np.inf, None), "reverse": (np.inf, None)}
    for mu in np.linspace(-5.0, 5.0, 201):
        for sigma in np.linspace(0.3, 5.0, 95):
            model = np.exp(-0.5 * ((grid - mu) / sigma) ** 2)
            model /= model.sum()
            floor = 1e-300
            safe_model = np.maximum(model, floor)
            safe_target = np.maximum(target, floor)
            f = float((target * np.log2(safe_target / safe_model)).sum())
            r = float((model * np.log2(safe_model / safe_target)).sum())
            if f < best["forward"][0]:
                best["forward"] = (f, (mu, sigma))
            if r < best["reverse"][0]:
                best["reverse"] = (r, (mu, sigma))

    (f_val, (f_mu, f_sd)) = best["forward"]
    (r_val, (r_mu, r_sd)) = best["reverse"]
    print("\nfitting one Gaussian to a two-mode target, by grid search:")
    print(f"  minimising KL(target || model): mu = {f_mu:+.3f}  sigma = {f_sd:.3f}  KL = {f_val:.4f} bits")
    print(f"  minimising KL(model || target): mu = {r_mu:+.3f}  sigma = {r_sd:.3f}  KL = {r_val:.4f} bits")
    print(f"  the forward fit is {f_sd / r_sd:.1f}x wider and sits between the modes;")
    print("  the reverse fit sits on one of them. Same target, opposite answers.")

    # ---- 6. A KL on real columns -----------------------------------------
    signals = load("m10_signals.csv")
    churned = signals.loc[signals["churned"] == 1, "plan"].value_counts(normalize=True).sort_index()
    stayed = signals.loc[signals["churned"] == 0, "plan"].value_counts(normalize=True).sort_index()
    print(f"\nm10_signals.csv, plan mix among churners against stayers:")
    print(f"  churners {np.round(churned.to_numpy(), 4)}")
    print(f"  stayers  {np.round(stayed.to_numpy(), 4)}")
    print(f"  KL(churners || stayers) = {kl_from_definition(churned.to_numpy(), stayed.to_numpy()):.6f} bits")
    print(f"  KL(stayers || churners) = {kl_from_definition(stayed.to_numpy(), churned.to_numpy()):.6f} bits")


if __name__ == "__main__":
    main()
