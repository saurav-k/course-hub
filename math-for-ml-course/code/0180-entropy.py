"""Shannon entropy, computed twice and checked against its own theorem.

Lesson: Entropy - how surprised you should expect to be.
Dataset: m10_signals.csv (12,000 rows) and m10_classifier.csv (20,000 rows).

Runs on numpy and pandas and nothing else. Works from a clone, from Jupyter, or
pasted into Colab.

What it does:
  1. Computes H(p) = -sum p*log2(p) straight from the definition, with a Python
     loop, so you can see the arithmetic.
  2. Computes it again vectorised with numpy, and asserts the two agree.
  3. Checks the two properties Shannon proves in section 6 of the 1948 paper:
     H = 0 exactly when one outcome is certain, and H is maximised at log2(n)
     for the uniform distribution.
  4. Checks the grouping axiom (Shannon's requirement 3) on the plan column,
     which is the axiom that forces the -log form.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

RAW = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/"


def load(name: str) -> pd.DataFrame:
    local = pathlib.Path(__file__).resolve().parent.parent / "datasets" / name
    return pd.read_csv(local if local.exists() else RAW + name)


# --------------------------------------------------------------------------
# The definition, written out
# --------------------------------------------------------------------------

def entropy_from_definition(probabilities) -> float:
    """H(p) = -sum_i p_i log2(p_i), one term at a time.

    The 0*log(0) = 0 convention is applied by skipping zero-probability
    outcomes, which is what the limit x*log(x) -> 0 as x -> 0 licenses.
    """
    total = 0.0
    for p in probabilities:
        if p > 0.0:
            total += p * np.log2(p)
    return -total if total != 0.0 else 0.0


def entropy_vectorised(probabilities: np.ndarray) -> float:
    p = np.asarray(probabilities, dtype=float)
    p = p[p > 0.0]
    total = float((p * np.log2(p)).sum())
    return -total if total != 0.0 else 0.0


def surprise(p: float) -> float:
    """The information content of one outcome, in bits."""
    return float(-np.log2(p))


def main() -> None:
    signals = load("m10_signals.csv")
    n = len(signals)

    # ---- 1. The entropy of a real column --------------------------------
    shares = signals["plan"].value_counts(normalize=True).sort_index()
    slow = entropy_from_definition(shares.to_numpy())
    fast = entropy_vectorised(shares.to_numpy())
    assert abs(slow - fast) < 1e-12, "the loop and the vector disagree"

    print(f"m10_signals.csv: {n} rows")
    print("\nplan: share and surprise")
    for value, share in shares.items():
        print(f"  {value:<12} p = {share:.4f}   surprise = {surprise(share):.4f} bits")
    print(f"  H(plan)             = {fast:.4f} bits")
    print(f"  log2(3), the ceiling = {np.log2(3):.4f} bits")

    # ---- 2. The label column --------------------------------------------
    label = signals["churned"].value_counts(normalize=True).sort_index().to_numpy()
    h_label = entropy_vectorised(label)
    print(f"\nchurned: p = {np.round(label, 4)}")
    print(f"  H(churned)          = {h_label:.4f} bits")

    # ---- 3. Shannon's two properties, checked ----------------------------
    certain = np.array([1.0, 0.0, 0.0])
    assert entropy_vectorised(certain) == 0.0
    print(f"\nH of a certainty     = {entropy_vectorised(certain):.4f} bits   (Shannon 1948, property 1)")

    for k in (2, 3, 5, 8):
        uniform = np.full(k, 1.0 / k)
        h = entropy_vectorised(uniform)
        assert abs(h - np.log2(k)) < 1e-12
        print(f"H of uniform over {k}  = {h:.4f} bits = log2({k})   (property 2)")

    # A non-uniform distribution over the same support must score lower.
    skewed = np.array([0.90, 0.05, 0.03, 0.02])
    assert entropy_vectorised(skewed) < entropy_vectorised(np.full(4, 0.25))
    print(f"H([.90 .05 .03 .02]) = {entropy_vectorised(skewed):.4f} bits < "
          f"{entropy_vectorised(np.full(4, 0.25)):.4f} bits, the uniform ceiling")

    # ---- 4. The grouping axiom -------------------------------------------
    # Shannon's third requirement: splitting a choice into two successive
    # choices must give the same total, weighted by how often the second
    # choice happens. This is the axiom that forces the -log form, so it is
    # worth checking rather than believing.
    #
    # Group plan into {basic} against {pro, enterprise}, then resolve the
    # second group.
    p = shares.to_dict()
    p_basic = p["basic"]
    p_rest = p["pro"] + p["enterprise"]
    outer = entropy_vectorised([p_basic, p_rest])
    inner = entropy_vectorised([p["pro"] / p_rest, p["enterprise"] / p_rest])
    grouped = outer + p_rest * inner
    print(f"\ngrouping axiom (Shannon 1948, requirement 3):")
    print(f"  H(basic, rest)                     = {outer:.6f}")
    print(f"  H(pro|rest, enterprise|rest)       = {inner:.6f}")
    print(f"  H(outer) + P(rest) * H(inner)      = {grouped:.6f}")
    print(f"  H(plan) computed directly          = {fast:.6f}")
    assert abs(grouped - fast) < 1e-12, "the grouping axiom does not hold"
    print("  they agree to 1e-12")

    # ---- 5. Scale up: entropy of 20,000 predicted distributions ----------
    clf = load("m10_classifier.csv")
    logits = clf[[f"logit_{j}" for j in range(5)]].to_numpy()
    shift = logits.max(axis=1, keepdims=True)
    probs = np.exp(logits - shift)
    probs /= probs.sum(axis=1, keepdims=True)
    per_row = -(np.where(probs > 0, probs * np.log2(probs), 0.0)).sum(axis=1)
    print(f"\nm10_classifier.csv: entropy of each row's predicted distribution")
    print(f"  rows                = {len(clf)}")
    print(f"  mean H              = {per_row.mean():.4f} bits")
    print(f"  median H            = {np.median(per_row):.4f} bits")
    print(f"  min / max H         = {per_row.min():.4f} / {per_row.max():.4f} bits")
    print(f"  ceiling log2(5)     = {np.log2(5):.4f} bits")
    assert per_row.max() <= np.log2(5) + 1e-9, "a distribution beat the uniform ceiling"
    print("  no row exceeds the ceiling, as property 2 requires")


if __name__ == "__main__":
    main()
