"""Mutual information: three formulas, one number, and the thing correlation misses.

Lesson: Mutual information.
Dataset: m10_signals.csv (12,000 rows).

Runs on numpy and pandas and nothing else.

What it does:
  1. Computes I(X;Y) three ways - as a KL between the joint and the product of
     the marginals, as H(Y) - H(Y|X), and as H(X) + H(Y) - H(X,Y) - and asserts
     all three agree. Shannon writes the same three identities on page 21 of the
     1948 paper.
  2. Computes pointwise mutual information per cell, and shows it can be
     negative while the expectation cannot.
  3. Builds Y = X^2 with X symmetric about zero, measures a Pearson correlation
     of essentially zero, and measures a large mutual information on the same
     data. That is the whole reason this quantity exists.
  4. Shows the estimation bias: a column independent of the label by
     construction still measures a positive mutual information, and the
     measured value grows with the number of distinct values.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

RAW = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/"


def load(name: str) -> pd.DataFrame:
    local = pathlib.Path(__file__).resolve().parent.parent / "datasets" / name
    return pd.read_csv(local if local.exists() else RAW + name)


def entropy(p) -> float:
    p = np.asarray(p, dtype=float)
    p = p[p > 0.0]
    return float(-(p * np.log2(p)).sum())


def joint_table(x: pd.Series, y: pd.Series) -> np.ndarray:
    """The joint distribution of two columns, as a table of probabilities."""
    counts = pd.crosstab(x, y).to_numpy(dtype=float)
    return counts / counts.sum()


def mi_as_kl(joint: np.ndarray) -> float:
    """I(X;Y) = KL(p(x,y) || p(x)p(y)), one cell at a time."""
    px = joint.sum(axis=1)
    py = joint.sum(axis=0)
    total = 0.0
    for i in range(joint.shape[0]):
        for j in range(joint.shape[1]):
            if joint[i, j] > 0.0:
                total += joint[i, j] * np.log2(joint[i, j] / (px[i] * py[j]))
    return total


def mi_as_entropy_drop(joint: np.ndarray) -> float:
    """I(X;Y) = H(Y) - H(Y|X)."""
    px = joint.sum(axis=1)
    py = joint.sum(axis=0)
    conditional = 0.0
    for i in range(joint.shape[0]):
        if px[i] > 0.0:
            conditional += px[i] * entropy(joint[i, :] / px[i])
    return entropy(py) - conditional


def mi_as_three_entropies(joint: np.ndarray) -> float:
    """I(X;Y) = H(X) + H(Y) - H(X,Y)."""
    return entropy(joint.sum(axis=1)) + entropy(joint.sum(axis=0)) - entropy(joint.ravel())


def main() -> None:
    signals = load("m10_signals.csv")
    n = len(signals)
    print(f"m10_signals.csv: {n} rows")

    print("\ncolumn          values      I(X;churned) bits    H(churned|X) bits")
    for column in ["plan", "support_tier", "theme"]:
        joint = joint_table(signals[column], signals["churned"])
        a = mi_as_kl(joint)
        b = mi_as_entropy_drop(joint)
        c = mi_as_three_entropies(joint)
        assert abs(a - b) < 1e-12 and abs(a - c) < 1e-12, "the three formulas disagree"
        h_y = entropy(joint.sum(axis=0))
        print(f"  {column:<14} {signals[column].nunique():>4}          {a:.6f}             {h_y - a:.6f}")

    h_label = entropy(signals["churned"].value_counts(normalize=True).to_numpy())
    print(f"\nH(churned) = {h_label:.6f} bits, so plan removes "
          f"{100 * mi_as_kl(joint_table(signals['plan'], signals['churned'])) / h_label:.2f} per cent of it")

    # ---- 2. Pointwise mutual information ---------------------------------
    joint = joint_table(signals["plan"], signals["churned"])
    px = joint.sum(axis=1)
    py = joint.sum(axis=0)
    levels = sorted(signals["plan"].unique())
    print("\npointwise mutual information, per cell, in bits:")
    print("  plan          churned=0   churned=1")
    for i, level in enumerate(levels):
        row = [np.log2(joint[i, j] / (px[i] * py[j])) for j in range(2)]
        print(f"  {level:<12} {row[0]:+9.4f}  {row[1]:+9.4f}")
    print("  PMI is signed. The expectation of it over the joint, which is I(X;Y), is not.")

    # ---- 3. Zero correlation, large mutual information -------------------
    rng = np.random.default_rng(11)
    x = rng.choice([-2.0, -1.0, 1.0, 2.0], size=40000)
    y = x ** 2
    correlation = float(np.corrcoef(x, y)[0, 1])
    frame = pd.DataFrame({"x": x, "y": y})
    quadratic = joint_table(frame["x"], frame["y"])
    print(f"\nY = X^2 with X symmetric about zero, {len(x)} samples:")
    print(f"  Pearson correlation      = {correlation:+.6f}")
    print(f"  I(X;Y)                   = {mi_as_kl(quadratic):.6f} bits")
    print(f"  H(Y)                     = {entropy(quadratic.sum(axis=0)):.6f} bits")
    print("  Y is a deterministic function of X, so H(Y|X) = 0 and I(X;Y) = H(Y) exactly.")
    assert abs(correlation) < 0.02
    assert mi_as_kl(quadratic) > 0.9

    # ---- 4. The estimation bias -------------------------------------------
    # theme is independent of churned by construction, so the population value
    # of I is exactly zero. The sample value is not, and it grows with the
    # number of distinct values, because more cells means more room for noise.
    print("\nestimation bias: mutual information with a column that is independent by construction")
    print("  distinct values    measured I(X;churned) bits")
    label = signals["churned"].to_numpy()
    for cardinality in (2, 4, 16, 64, 256, 2048, 12000):
        fake = rng.integers(0, cardinality, size=n)
        table = joint_table(pd.Series(fake), pd.Series(label))
        print(f"  {cardinality:>10}         {mi_as_kl(table):.6f}")
    print("  The true value is zero in every row. A plug-in estimate is biased upward,")
    print("  and the bias grows with the number of cells you spread the data over.")


if __name__ == "__main__":
    main()
