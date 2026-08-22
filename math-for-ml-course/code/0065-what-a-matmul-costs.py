"""Lesson 65 - what a matrix multiply costs.

The result this checks twice is the 2mnp flop count: once as arithmetic from the
shapes, and once as measured wall-clock time, which scales the same way even
though the constant belongs entirely to the machine.

It also settles the ordering question. (AB)C and A(BC) return the same matrix and
cost wildly different amounts.

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


def flops_matmul(m: int, p: int, n: int) -> int:
    """About 2mnp: mn output entries, each an inner product of length p."""
    return 2 * m * n * p


def timed(fn, repeats: int = 3) -> float:
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - start)
    return best


def main() -> None:
    X = load()[SENSORS].to_numpy(dtype=float)
    print(f"the data matrix is {X.shape[0]:,} by {X.shape[1]}")

    print("\n-- predicted flops against measured time --")
    rng = np.random.default_rng(1)
    print(f"{'shape':>22} {'flops':>16} {'seconds':>10} {'Gflop/s':>9}")
    previous = None
    for n in (128, 256, 512, 1024):
        A = rng.normal(size=(n, n))
        B = rng.normal(size=(n, n))
        f = flops_matmul(n, n, n)
        seconds = timed(lambda: A @ B)
        line = f"{f'{n}x{n} @ {n}x{n}':>22} {f:>16,} {seconds:>10.5f} {f / seconds / 1e9:>9.1f}"
        if previous is not None:
            line += f"   flops x{f / previous[0]:.0f}, time x{seconds / previous[1]:.1f}"
        print(line)
        previous = (f, seconds)
    print("doubling n multiplies the flop count by 8. The measured time follows once")
    print("the matrices are big enough for the arithmetic to dominate the overheads.")

    print("\n-- the ordering result: same answer, different bill --")
    d, r = 4096, 4
    x = rng.normal(size=(1, d))
    B_lora = rng.normal(size=(d, r))
    A_lora = rng.normal(size=(r, d))
    first = flops_matmul(d, r, d) + flops_matmul(1, d, d)
    second = flops_matmul(1, d, r) + flops_matmul(1, r, d)
    print(f"  form (B A) then x @ it : {first:>15,} flops")
    print(f"  (x @ B) then @ A       : {second:>15,} flops")
    print(f"  ratio                  : {first / second:>15,.0f}x")
    slow = timed(lambda: x @ (B_lora @ A_lora))
    fast = timed(lambda: (x @ B_lora) @ A_lora)
    print(f"  measured: {slow:.5f}s against {fast:.5f}s, a factor of {slow / fast:.0f}")
    assert np.allclose(x @ (B_lora @ A_lora), (x @ B_lora) @ A_lora, atol=1e-8)
    print("checked twice: associativity gives the identical answer both ways")

    print("\n-- where a Transformer block's matmul flops go --")
    d_model, n_ctx = 12_288, 2_048
    d_ff = 4 * d_model
    rows = [
        ("Q, K, V, O projections", 4 * flops_matmul(n_ctx, d_model, d_model)),
        ("Q K^T scores", flops_matmul(n_ctx, d_model, n_ctx)),
        ("scores @ V", flops_matmul(n_ctx, n_ctx, d_model)),
        ("MLP up", flops_matmul(n_ctx, d_model, d_ff)),
        ("MLP down", flops_matmul(n_ctx, d_ff, d_model)),
    ]
    total = sum(f for _, f in rows)
    for label, f in rows:
        print(f"  {label:<24} {f / 1e12:>7.3f} Tflop  {100 * f / total:>5.1f}%")
    attention = rows[1][1] + rows[2][1]
    print(f"  {'TOTAL':<24} {total / 1e12:>7.3f} Tflop")
    print(f"  attention is {100 * attention / total:.1f}% of the block at {n_ctx:,} tokens")
    print(f"  the two halves are equal when n = 6d = {6 * d_model:,} tokens")

    print("\n-- the Gram matrix is symmetric, so it costs about half --")
    n, k = X.shape
    print(f"  X^T X as a general product: about {flops_matmul(k, n, k):,} flops")
    print(f"  exploiting symmetry       : about {flops_matmul(k, n, k) // 2:,} flops")
    G = X.T @ X
    assert np.allclose(G, np.triu(G) + np.triu(G, 1).T)
    print("  checked twice: the upper half plus its mirror rebuilds the whole Gram matrix")


if __name__ == "__main__":
    main()
