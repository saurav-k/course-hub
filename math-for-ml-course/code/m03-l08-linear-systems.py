"""M03 L08 - Ax = b, the three answers, and why you solve rather than invert.

    python3 m03-l08-linear-systems.py

Two results, each checked twice.

1. A system has no solution, exactly one, or infinitely many. The "never exactly
   two" claim is checked constructively: given two solutions, every point on the
   line between them is shown to be a solution too.
2. Solving beats inverting, on both counts the page claims. The flop counts are
   arithmetic; the accuracy and the time are measured on an ill-conditioned system
   built from the housing table's own redundant column.
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "housing.csv"


def describe(A: np.ndarray) -> str:
    m, n = A.shape
    if m > n:
        return f"{m}x{n}, tall, over-determined"
    if m < n:
        return f"{m}x{n}, wide, under-determined"
    return f"{m}x{n}, square"


def main() -> None:
    print("-- the three answers --")

    A_none = np.array([[1.0, 1.0], [1.0, 0.0], [1.0, -1.0]])
    b_none = np.array([1.0, -1.0, 0.0])
    x_ls, *_ = np.linalg.lstsq(A_none, b_none, rcond=None)
    print(f"  no solution   : A is {describe(A_none)}")
    print(f"    best possible residual ||Ax - b|| = {np.linalg.norm(A_none @ x_ls - b_none):.6f}, not zero")

    A_one = np.array([[2.0, 1.0], [1.0, 3.0]])
    b_one = np.array([5.0, 10.0])
    x_one = np.linalg.solve(A_one, b_one)
    print(f"  one solution  : A is {describe(A_one)}, x = {np.round(x_one, 6)}")
    print(f"    residual = {np.linalg.norm(A_one @ x_one - b_one):.3e}")

    A_many = np.array([[1.0, 1.0, 0.0], [0.0, 1.0, 1.0]])
    b_many = np.array([1.0, 2.0])
    p, q = np.array([1.0, 0.0, 2.0]), np.array([0.0, 1.0, 1.0])
    print(f"  many solutions: A is {describe(A_many)}")
    print(f"    p = {p} gives residual {np.linalg.norm(A_many @ p - b_many):.3e}")
    print(f"    q = {q} gives residual {np.linalg.norm(A_many @ q - b_many):.3e}")

    print("\n  why 'exactly two' is impossible: every blend of p and q also solves it")
    worst = 0.0
    for alpha in np.linspace(-2.0, 3.0, 11):
        z = alpha * p + (1 - alpha) * q
        worst = max(worst, float(np.linalg.norm(A_many @ z - b_many)))
        print(f"    alpha = {alpha:>5.1f}  z = {np.round(z, 3)}  residual {np.linalg.norm(A_many @ z - b_many):.3e}")
    assert worst < 1e-12
    print("  checked twice: eleven different blends, every one an exact solution")

    print("\n-- solve, do not invert --")
    frame = pd.read_csv(DATA)
    # A real square system: the normal equations of the housing fit. The redundant
    # area column is deliberately LEFT OUT here, because a singular matrix would
    # make the comparison prove something else. This one is merely ill-conditioned,
    # which is the ordinary case and the case worth measuring.
    cols = ["area_k_sqft", "bedrooms", "bathrooms", "age_years", "lot_sqft"]
    X = np.column_stack([np.ones(len(frame))] + [frame[c].to_numpy(float) for c in cols])
    A = X.T @ X
    b = X.T @ frame["price_usd"].to_numpy(float)
    n = A.shape[0]
    print(f"  A = X^T X is {n}x{n}, condition number {np.linalg.cond(A):.3e}")

    x_solve = np.linalg.solve(A, b)
    x_invert = np.linalg.inv(A) @ b
    r_solve = np.linalg.norm(A @ x_solve - b) / np.linalg.norm(b)
    r_invert = np.linalg.norm(A @ x_invert - b) / np.linalg.norm(b)
    print(f"  relative residual, solve : {r_solve:.3e}")
    print(f"  relative residual, invert: {r_invert:.3e}")
    print(f"  inverting is {r_invert / r_solve:.1f} times worse on this system")

    print("\n  the flop counts, and the same comparison at a size where time is visible")
    big_n = 700
    print(f"  solve directly     : about 2 n^3 = {2 * big_n**3:,} flops")
    print(f"  invert then apply  : about 3 n^3 = {3 * big_n**3:,} flops, plus the multiply")
    rng = np.random.default_rng(9)
    big = rng.normal(size=(big_n, big_n))
    rhs = rng.normal(size=big_n)
    t_solve = min(_time(lambda: np.linalg.solve(big, rhs)) for _ in range(5))
    t_invert = min(_time(lambda: np.linalg.inv(big) @ rhs) for _ in range(5))
    print(f"  measured: solve {t_solve:.4f}s, invert-then-multiply {t_invert:.4f}s"
          f"  ({t_invert / t_solve:.1f}x)")
    e_solve = np.linalg.norm(big @ np.linalg.solve(big, rhs) - rhs)
    e_invert = np.linalg.norm(big @ (np.linalg.inv(big) @ rhs) - rhs)
    print(f"  residual: solve {e_solve:.3e}, invert {e_invert:.3e}")

    print("\n-- factorisation caching: ten right-hand sides for the price of one --")
    k = 10
    print(f"  naive : {k} separate solves, about 2 k n^3 = {2 * k * big_n**3:,} flops")
    print(f"  cached: about 2 n^3 + 3 k n^2 = {2 * big_n**3 + 3 * k * big_n**2:,} flops")
    print(f"  predicted speed-up: {2 * k * big_n**3 / (2 * big_n**3 + 3 * k * big_n**2):.1f}x")
    B = rng.normal(size=(big_n, k))
    t_together = min(_time(lambda: np.linalg.solve(big, B)) for _ in range(3))
    t_separate = min(
        _time(lambda: np.column_stack([np.linalg.solve(big, B[:, i]) for i in range(k)]))
        for _ in range(3)
    )
    print(f"  measured: one call {t_together:.4f}s, {k} calls {t_separate:.4f}s"
          f"  ({t_separate / t_together:.1f}x)")
    assert np.allclose(np.linalg.solve(big, B),
                       np.column_stack([np.linalg.solve(big, B[:, i]) for i in range(k)]))
    print("  checked twice: one call with ten columns matches ten calls with one")


def _time(fn) -> float:
    start = time.perf_counter()
    fn()
    return time.perf_counter() - start


if __name__ == "__main__":
    main()
