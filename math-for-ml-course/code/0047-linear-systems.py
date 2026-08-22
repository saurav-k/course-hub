"""Lesson 47 - Ax = b, the three answers, and why you solve rather than invert.

Two results, each checked twice.

1. A system has no solution, exactly one, or infinitely many. The "never exactly
   two" claim is checked constructively: given two solutions, every point on the
   line between them is shown to be a solution too.
2. Solving beats inverting on both counts. The flop counts are arithmetic; the
   accuracy and the time are measured on the normal equations of a real fit and
   on a 700 by 700 system.

Needs only numpy and pandas. Runs in a codebase, in Jupyter, or in Colab.
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "sensors.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/sensors.csv"

SENSORS = [
    "vibration_x", "vibration_y", "acoustic_db", "current_amp",
    "humidity_pct", "dust_index", "temp_c", "pressure_kpa",
]


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


import time


def describe(A: np.ndarray) -> str:
    m, n = A.shape
    if m > n:
        return f"{m}x{n}, tall, over-determined"
    if m < n:
        return f"{m}x{n}, wide, under-determined"
    return f"{m}x{n}, square"


def elapsed(fn) -> float:
    start = time.perf_counter()
    fn()
    return time.perf_counter() - start


def main() -> None:
    print("-- the three answers --")
    A_none = np.array([[1.0, 1.0], [1.0, 0.0], [1.0, -1.0]])
    b_none = np.array([1.0, -1.0, 0.0])
    x_ls, *_ = np.linalg.lstsq(A_none, b_none, rcond=None)
    print(f"  no solution   : A is {describe(A_none)}")
    print(f"    the best any x can do is ||Ax - b|| = {np.linalg.norm(A_none @ x_ls - b_none):.6f}, not zero")

    A_one = np.array([[2.0, 1.0], [1.0, 3.0]])
    b_one = np.array([5.0, 10.0])
    x_one = np.linalg.solve(A_one, b_one)
    print(f"  one solution  : A is {describe(A_one)}, x = {np.round(x_one, 6)}, "
          f"residual {np.linalg.norm(A_one @ x_one - b_one):.3e}")

    A_many = np.array([[1.0, 1.0, 0.0], [0.0, 1.0, 1.0]])
    b_many = np.array([1.0, 2.0])
    p, q = np.array([1.0, 0.0, 2.0]), np.array([0.0, 1.0, 1.0])
    print(f"  many solutions: A is {describe(A_many)}")
    print("\n  why 'exactly two' is impossible: every blend of two solutions solves it too")
    worst = 0.0
    for alpha in np.linspace(-2.0, 3.0, 11):
        z = alpha * p + (1 - alpha) * q
        worst = max(worst, float(np.linalg.norm(A_many @ z - b_many)))
        print(f"    alpha {alpha:>5.1f}  z = {np.round(z, 3)}  residual {np.linalg.norm(A_many @ z - b_many):.3e}")
    assert worst < 1e-12
    print("  checked twice: eleven different blends, every one an exact solution")

    print("\n-- solve, do not invert --")
    frame = load()
    # A real square system: the normal equations of the fit lesson 51 works out.
    # The target is built from a stated rule so the system is genuine rather than
    # circular - regressing a sensor on a design that already contains it would
    # fit exactly and prove nothing.
    X = np.column_stack([np.ones(len(frame))] + [frame[s].to_numpy(float) for s in SENSORS])
    truth = np.array([12.5, 3.2, -1.8, 0.9, 2.4, -0.6, 1.1, 0.35, 0.07])
    y = X @ truth + np.random.default_rng(20260822).normal(0.0, 2.0, len(frame))
    A = X.T @ X
    b = X.T @ y
    n = A.shape[0]
    print(f"  A = X^T X is {n}x{n}, condition number {np.linalg.cond(A):.3e}")
    x_solve = np.linalg.solve(A, b)
    x_invert = np.linalg.inv(A) @ b
    r_solve = np.linalg.norm(A @ x_solve - b) / np.linalg.norm(b)
    r_invert = np.linalg.norm(A @ x_invert - b) / np.linalg.norm(b)
    print(f"  relative residual, solve : {r_solve:.3e}")
    print(f"  relative residual, invert: {r_invert:.3e}")
    print(f"  inverting is {r_invert / r_solve:.0f} times worse on this system")

    big_n = 700
    print(f"\n  at a size where the time is visible, {big_n} by {big_n}:")
    print(f"    solve directly    : about 2 n^3 = {2 * big_n ** 3:,} flops")
    print(f"    invert then apply : about 3 n^3 = {3 * big_n ** 3:,} flops, plus the multiply")
    rng = np.random.default_rng(9)
    big, rhs = rng.normal(size=(big_n, big_n)), rng.normal(size=big_n)
    t_solve = min(elapsed(lambda: np.linalg.solve(big, rhs)) for _ in range(5))
    t_invert = min(elapsed(lambda: np.linalg.inv(big) @ rhs) for _ in range(5))
    print(f"    measured: solve {t_solve:.4f}s, invert-then-multiply {t_invert:.4f}s ({t_invert / t_solve:.1f}x)")

    print("\n-- factorisation caching: ten right-hand sides for the price of one --")
    k = 10
    print(f"  naive : {k} separate solves, about 2 k n^3 = {2 * k * big_n ** 3:,} flops")
    print(f"  cached: about 2 n^3 + 3 k n^2 = {2 * big_n ** 3 + 3 * k * big_n ** 2:,} flops")
    print(f"  predicted speed-up: {2 * k * big_n ** 3 / (2 * big_n ** 3 + 3 * k * big_n ** 2):.1f}x")
    B = rng.normal(size=(big_n, k))
    t_together = min(elapsed(lambda: np.linalg.solve(big, B)) for _ in range(3))
    t_separate = min(elapsed(lambda: np.column_stack([np.linalg.solve(big, B[:, i]) for i in range(k)]))
                     for _ in range(3))
    print(f"  measured: one call {t_together:.4f}s, {k} calls {t_separate:.4f}s ({t_separate / t_together:.1f}x)")
    assert np.allclose(np.linalg.solve(big, B),
                       np.column_stack([np.linalg.solve(big, B[:, i]) for i in range(k)]))
    print("  checked twice: one call with ten columns matches ten calls with one")


if __name__ == "__main__":
    main()
