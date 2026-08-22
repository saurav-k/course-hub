"""The kernel trick, checked against the feature map it never builds.

Lesson: Kernels, and why a kernel matrix must be positive semi-definite.
Dataset: m10_signals.csv (12,000 rows) and a small ring problem generated here.

Runs on numpy and pandas and nothing else.

What it does:
  1. Builds the explicit degree-two feature map for two-dimensional inputs and
     shows phi(x).phi(z) equals (x.z + 1)^2 exactly, for random pairs.
  2. Counts how many multiplications each route costs as the input dimension
     grows, and prints the ratio.
  3. Builds a Gram matrix from real data and checks Mercer's condition the way
     you actually check it: the eigenvalues of the Gram matrix are all
     non-negative. Then breaks it, with a symmetric function that is not a
     kernel, and shows the negative eigenvalue.
  4. Solves a ring problem that no line separates, using kernel ridge
     regression written in six lines, and reports the accuracy against a linear
     model on the same data.
"""

from __future__ import annotations

import pathlib
from math import comb

import numpy as np
import pandas as pd

RAW = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/"


def load(name: str) -> pd.DataFrame:
    local = pathlib.Path(__file__).resolve().parent.parent / "datasets" / name
    return pd.read_csv(local if local.exists() else RAW + name)


def phi_degree_two(x: np.ndarray) -> np.ndarray:
    """The explicit feature map for k(x,z) = (x.z + 1)^2 in two dimensions.

    Six coordinates: the constant, the two linear terms scaled by sqrt(2), the
    two squares, and the cross term scaled by sqrt(2).
    """
    x1, x2 = x
    root2 = np.sqrt(2.0)
    return np.array([1.0, root2 * x1, root2 * x2, x1 * x1, root2 * x1 * x2, x2 * x2])


def polynomial_kernel(A: np.ndarray, B: np.ndarray, degree: int = 2, bias: float = 1.0) -> np.ndarray:
    return (A @ B.T + bias) ** degree


def rbf_kernel(A: np.ndarray, B: np.ndarray, gamma: float) -> np.ndarray:
    """exp(-gamma |x - z|^2), which is a function of the Euclidean distance."""
    sq = (A * A).sum(axis=1)[:, None] + (B * B).sum(axis=1)[None, :] - 2.0 * A @ B.T
    return np.exp(-gamma * np.maximum(sq, 0.0))


def main() -> None:
    rng = np.random.default_rng(17)

    # ---- 1. The identity, on numbers -------------------------------------
    print("k(x, z) = (x.z + 1)^2 against phi(x).phi(z), on ten random pairs:")
    worst = 0.0
    for _ in range(10):
        x = rng.normal(size=2)
        z = rng.normal(size=2)
        direct = float((x @ z + 1.0) ** 2)
        explicit = float(phi_degree_two(x) @ phi_degree_two(z))
        worst = max(worst, abs(direct - explicit))
    print(f"  largest disagreement = {worst:.3e}")
    assert worst < 1e-9
    x = np.array([2.0, 1.0])
    z = np.array([1.0, 3.0])
    print(f"  worked: x = {x}, z = {z}")
    print(f"    x.z = {x @ z:.0f}, so k = ({x @ z:.0f} + 1)^2 = {(x @ z + 1) ** 2:.0f}")
    print(f"    phi(x) = {np.round(phi_degree_two(x), 4)}")
    print(f"    phi(z) = {np.round(phi_degree_two(z), 4)}")
    print(f"    phi(x).phi(z) = {phi_degree_two(x) @ phi_degree_two(z):.0f}")

    # ---- 2. What the trick saves -----------------------------------------
    print("\nmultiplications for one similarity, kernel route against explicit route:")
    print("  input dim   degree   monomials C(n+d, d)   kernel cost   ratio")
    for n_in, degree in ((2, 2), (256, 2), (256, 3), (256, 4), (256, 7)):
        monomials = comb(n_in + degree, degree)
        kernel_cost = n_in + degree - 1
        print(f"  {n_in:>9}   {degree:>6}   {monomials:>19,}   {kernel_cost:>11}   "
              f"{monomials / kernel_cost:>10,.0f}x")
    print("  The kernel column does not grow with the degree. That is the trick.")

    # ---- 3. Mercer's condition, as an eigenvalue test --------------------
    signals = load("m10_signals.csv")
    X = signals[["tenure_months", "monthly_spend", "sessions_week"]].to_numpy(dtype=float)
    X = (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)
    sample = X[rng.choice(len(X), size=400, replace=False)]

    print(f"\nGram matrices on 400 standardised rows of m10_signals.csv:")
    for name, K in (("linear", sample @ sample.T),
                    ("polynomial degree 2", polynomial_kernel(sample, sample)),
                    ("RBF gamma = 0.5", rbf_kernel(sample, sample, 0.5))):
        eig = np.linalg.eigvalsh((K + K.T) / 2.0)
        print(f"  {name:<22} symmetric {np.allclose(K, K.T)}   "
              f"smallest eigenvalue {eig.min():+.3e}   valid {eig.min() > -1e-8}")
        assert eig.min() > -1e-8, f"{name} is not positive semi-definite"

    # A symmetric similarity that is not a kernel. tanh is a common one and it
    # is not positive semi-definite for most parameter settings.
    bad = np.tanh(0.5 * sample @ sample.T + 1.0)
    eig = np.linalg.eigvalsh((bad + bad.T) / 2.0)
    print(f"  {'tanh(0.5 x.z + 1)':<22} symmetric {np.allclose(bad, bad.T)}   "
          f"smallest eigenvalue {eig.min():+.3e}   valid {eig.min() > -1e-8}")
    assert eig.min() < -1e-8, "the counterexample stopped being a counterexample"
    print("  Symmetric is not enough. Positive semi-definite is the condition, and")
    print("  the eigenvalues of the Gram matrix are how you check it on real data.")

    # ---- 4. A problem no line separates -----------------------------------
    n = 800
    angle = rng.uniform(0.0, 2.0 * np.pi, n)
    radius = np.where(rng.random(n) < 0.5, 1.0, 2.6) + rng.normal(0.0, 0.22, n)
    P = np.column_stack([radius * np.cos(angle), radius * np.sin(angle)])
    label = np.where(radius < 1.8, -1.0, 1.0)
    split = 600
    train, test = P[:split], P[split:]
    y_train, y_test = label[:split], label[split:]

    # Linear ridge regression in the input space.
    A = np.column_stack([train, np.ones(split)])
    w = np.linalg.solve(A.T @ A + 1e-6 * np.eye(3), A.T @ y_train)
    linear_pred = np.sign(np.column_stack([test, np.ones(len(test))]) @ w)

    # Kernel ridge regression. Same algebra, one substitution.
    gamma = 0.5
    lam = 1e-3
    K = rbf_kernel(train, train, gamma)
    alpha = np.linalg.solve(K + lam * np.eye(split), y_train)
    kernel_pred = np.sign(rbf_kernel(test, train, gamma) @ alpha)

    print(f"\na ring inside a ring, {split} training and {len(test)} test points:")
    print(f"  linear ridge in the input space : accuracy {(linear_pred == y_test).mean():.4f}")
    print(f"  kernel ridge with an RBF kernel : accuracy {(kernel_pred == y_test).mean():.4f}")
    print(f"  The second model never built a feature vector. It solved a "
          f"{split} by {split} system instead.")
    assert (kernel_pred == y_test).mean() > 0.95
    assert (linear_pred == y_test).mean() < 0.7

    print(f"\n  and the cost the trick charges instead: the Gram matrix is "
          f"{split} by {split} = {split * split:,} entries.")
    print(f"  At 1,000,000 training points that would be 10^12 entries, which is")
    print(f"  why kernel methods trade a dimension problem for a sample-size problem.")


if __name__ == "__main__":
    main()
