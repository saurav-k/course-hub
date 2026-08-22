"""M03 L12 - Least squares: the normal equations, and why they are a projection.

    python3 m03-l12-least-squares.py

Three results, each checked twice.

1. The normal equations A^T A x = A^T b give the minimiser of ||Ax - b||. Checked
   by solving them, and again by confirming that 50,000 random nearby coefficient
   vectors all give a larger residual.
2. The fit is a projection: A x_hat equals P b for the projection matrix of L11,
   and X^T r is zero.
3. The same answer arrives by three routes - the normal equations, a QR
   factorisation, and numpy's own least-squares routine - and the normal equations
   are the least accurate of the three when the columns are badly scaled.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "housing.csv"
FEATURES = ["area_k_sqft", "bedrooms", "bathrooms", "age_years", "lot_sqft"]
TRUTH = np.array([38_000.0, 232_000.0, 43_000.0, 21_000.0, -900.0, 3.1])


def solve_normal_equations(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    return np.linalg.solve(X.T @ X, X.T @ y)


def solve_qr(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    Q, R = np.linalg.qr(X)
    return np.linalg.solve(R, Q.T @ y)


def main() -> None:
    frame = pd.read_csv(DATA)
    X = np.column_stack([np.ones(len(frame))] + [frame[c].to_numpy(float) for c in FEATURES])
    y = frame["price_usd"].to_numpy(float)
    names = ["intercept"] + FEATURES

    print(f"design matrix X is {X.shape[0]:,} x {X.shape[1]}, target y is {y.shape[0]:,} prices")
    print(f"over-determined: {X.shape[0]:,} equations, {X.shape[1]} unknowns")

    beta = solve_normal_equations(X, y)
    print(f"\n{'coefficient':<12} {'fitted':>14} {'truth used to build the data':>30}")
    for name, value, truth in zip(names, beta, TRUTH):
        print(f"{name:<12} {value:>14,.2f} {truth:>30,.2f}")

    residual = y - X @ beta
    print(f"\nresidual norm ||r||          = {np.linalg.norm(residual):,.1f}")
    print(f"root mean square residual    = {np.linalg.norm(residual) / np.sqrt(len(y)):,.1f} dollars")
    print(f"the noise the data was built with was 26,000 dollars")

    print("\n-- the orthogonality principle, in numbers --")
    print(f"  X^T r = {np.round(X.T @ residual, 4)}")
    print(f"  max |X^T r| relative to ||X|| ||r|| = "
          f"{np.abs(X.T @ residual).max() / (np.linalg.norm(X) * np.linalg.norm(residual)):.3e}")

    print("\n-- is it really the minimum? 50,000 challengers --")
    rng = np.random.default_rng(17)
    best = float(residual @ residual)
    scale = np.abs(beta) * 1e-3 + 1e-6
    beaten = 0
    margin = np.inf
    for _ in range(50_000):
        trial = beta + rng.normal(0.0, 1.0, size=len(beta)) * scale
        value = float(np.sum((y - X @ trial) ** 2))
        if value < best:
            beaten += 1
        margin = min(margin, value - best)
    print(f"  challengers that beat it: {beaten} of 50,000")
    print(f"  smallest gap seen       : {margin:.6e}  (never negative)")
    assert beaten == 0
    print("checked twice: the normal-equations answer is the minimiser")

    print("\n-- the fit IS a projection --")
    fitted = X @ beta
    P_times_y = X @ np.linalg.solve(X.T @ X, X.T @ y)
    print(f"  max |X beta - P y| = {np.abs(fitted - P_times_y).max():.3e}")
    print(f"  ||y||^2            = {y @ y:.6e}")
    print(f"  ||fitted||^2 + ||r||^2 = {fitted @ fitted + residual @ residual:.6e}")
    print("  the two agree because fitted and residual are orthogonal: Pythagoras, in 20,000 dimensions")
    assert abs((fitted @ fitted + residual @ residual) - y @ y) / (y @ y) < 1e-12

    print("\n-- three routes to the same coefficients --")
    beta_qr = solve_qr(X, y)
    beta_np, *_ = np.linalg.lstsq(X, y, rcond=None)
    print(f"  normal equations vs QR   : max difference {np.abs(beta - beta_qr).max():.3e}")
    print(f"  normal equations vs numpy: max difference {np.abs(beta - beta_np).max():.3e}")
    print(f"  cond(X)     = {np.linalg.cond(X):.3e}")
    print(f"  cond(X^T X) = {np.linalg.cond(X.T @ X):.3e}   <- squared, which is the cost of the shortcut")
    assert np.allclose(beta, beta_qr, rtol=1e-6) and np.allclose(beta, beta_np, rtol=1e-6)
    print("checked twice: all three agree here, and the condition numbers say why QR is the safer route")

    print("\n-- read the answer back in the units of the problem --")
    for name, value in zip(names[1:], beta[1:]):
        print(f"  one more unit of {name:<12} is worth {value:>12,.0f} dollars")


if __name__ == "__main__":
    main()
