"""M05 lesson 13 - six matrix-calculus identities, each checked numerically.

Implements the six identities the rest of this course leans on, and verifies
every one against a finite-difference derivative rather than asserting it:

    1.  d(a^T x) / dx            = a
    2.  d(x^T A x) / dx          = (A + A^T) x        = 2 A x for symmetric A
    3.  d(||x||^2) / dx          = 2 x
    4.  d(A x) / dx              = A                  (a Jacobian)
    5.  d(||y - X b||^2) / db    = -2 X^T (y - X b)
    6.  d tr(A X) / dX           = A^T

Then the payoff: identity 5 set to zero gives the normal equations, which the
linear algebra module reached by dropping a perpendicular. Two disjoint routes,
one answer, checked against each other on eight thousand real rows.

Layout convention, held everywhere in this course: a gradient has the shape of
the thing you differentiate by. d(scalar)/dx for a column x is a column.

    python3 m05_13_matrix_calculus.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "datasets" / "m05-housing.csv"
FEATURES = ["area_sqft", "bedrooms", "age_years", "lot_sqft"]
TARGET = "price_k"
SEED = 20260822


def numeric_gradient(fn, x: np.ndarray, h: float = 1e-6) -> np.ndarray:
    """Central difference in every entry of x, returned with the shape of x."""
    grad = np.zeros_like(x, dtype=float)
    it = np.nditer(x, flags=["multi_index"])
    while not it.finished:
        idx = it.multi_index
        original = x[idx]
        x[idx] = original + h
        up = fn(x)
        x[idx] = original - h
        down = fn(x)
        x[idx] = original
        grad[idx] = (up - down) / (2.0 * h)
        it.iternext()
    return grad


def numeric_jacobian(fn, x: np.ndarray, h: float = 1e-6) -> np.ndarray:
    base = fn(x)
    out = np.zeros((len(base), len(x)))
    for j in range(len(x)):
        up, down = x.copy(), x.copy()
        up[j] += h
        down[j] -= h
        out[:, j] = (fn(up) - fn(down)) / (2.0 * h)
    return out


def report(name: str, analytic: np.ndarray, numeric: np.ndarray) -> None:
    gap = float(np.abs(analytic - numeric).max())
    shape = "x".join(str(d) for d in analytic.shape)
    print(f"  {name:<34} shape {shape:<8} largest gap {gap:.3e}")


def main() -> None:
    rng = np.random.default_rng(SEED)
    n = 5
    x = rng.normal(size=n)
    a_vec = rng.normal(size=n)
    a_mat = rng.normal(size=(n, n))
    a_sym = a_mat + a_mat.T

    print("the six identities, analytic against central difference\n")
    report("1. d(a^T x)/dx = a", a_vec, numeric_gradient(lambda v: float(a_vec @ v), x.copy()))
    report(
        "2. d(x^T A x)/dx = (A + A^T)x",
        (a_mat + a_mat.T) @ x,
        numeric_gradient(lambda v: float(v @ a_mat @ v), x.copy()),
    )
    report(
        "   symmetric A: 2 A x",
        2 * a_sym @ x,
        numeric_gradient(lambda v: float(v @ a_sym @ v), x.copy()),
    )
    report("3. d(||x||^2)/dx = 2x", 2 * x, numeric_gradient(lambda v: float(v @ v), x.copy()))
    report("4. d(A x)/dx = A", a_mat, numeric_jacobian(lambda v: a_mat @ v, x.copy()))

    m = 7
    x_mat = rng.normal(size=(m, n))
    y_vec = rng.normal(size=m)
    b = rng.normal(size=n)
    report(
        "5. d(||y - Xb||^2)/db",
        -2.0 * x_mat.T @ (y_vec - x_mat @ b),
        numeric_gradient(lambda v: float((y_vec - x_mat @ v) @ (y_vec - x_mat @ v)), b.copy()),
    )

    big = rng.normal(size=(n, n))
    report(
        "6. d tr(A X)/dX = A^T",
        a_mat.T,
        numeric_gradient(lambda v: float(np.trace(a_mat @ v)), big.copy()),
    )

    print("\nthe payoff: identity 5, set to zero, is the normal equations")
    frame = pd.read_csv(DATA)
    xd = np.hstack([np.ones((len(frame), 1)), frame[FEATURES].to_numpy(dtype=float)])
    yd = frame[TARGET].to_numpy(dtype=float)

    # Route one: calculus. Set -2 X^T (y - X b) = 0, so X^T X b = X^T y.
    by_calculus = np.linalg.solve(xd.T @ xd, xd.T @ yd)

    # Route two: geometry, with no derivative anywhere. Project y onto the
    # column space of X. numpy's lstsq solves the least-squares problem
    # directly, by QR, which is the orthogonality argument made numerical.
    by_projection, *_ = np.linalg.lstsq(xd, yd, rcond=None)

    names = ["intercept", *FEATURES]
    print(f"  {'parameter':>12} {'by calculus':>16} {'by projection':>16} {'gap':>12}")
    for name, c, p in zip(names, by_calculus, by_projection):
        print(f"  {name:>12} {c:16.8f} {p:16.8f} {abs(c - p):12.2e}")

    residual = yd - xd @ by_calculus
    print(f"\n  the residual is perpendicular to every column of X:")
    print(f"    max |X^T r| = {np.abs(xd.T @ residual).max():.3e}")
    print("  which is the geometric statement the calculus route never mentions")

    print("\n  ridge: add lambda ||b||^2 and identity 3 adds 2 lambda b")
    for lam in (0.0, 1.0, 100.0, 10000.0):
        ridge = np.linalg.solve(xd.T @ xd + lam * np.eye(xd.shape[1]), xd.T @ yd)
        eig = np.linalg.eigvalsh(2.0 / len(yd) * (xd.T @ xd) + 2 * lam / len(yd) * np.eye(xd.shape[1]))
        print(f"    lambda {lam:8.0f}: ||b|| = {np.linalg.norm(ridge):10.4f}   "
              f"kappa = {eig[-1] / eig[0]:16,.1f}")
    print("    every eigenvalue rises by the same amount, so the smallest one")
    print("    moves furthest in relative terms. That is why ridge conditions the problem.")


if __name__ == "__main__":
    main()
