"""Lesson 0501 - the derivative is a limit, and what a machine does to it.

Implements: the definition of the derivative as a limit of difference
quotients, and the two ways to evaluate it numerically.

The result the lesson states, and this program checks:

    forward difference   error falls like h        (first order)
    central difference   error falls like h^2      (second order)

and then both stop falling, because subtracting two nearly equal floats loses
significant digits faster than a smaller h gains them. The error curve is a V,
not a slope, and the bottom of the V is where a gradient check should sit.

Runs on numpy alone. No dataset: this lesson's object is a function, not a
table. The dataset arrives in lesson 2.

    python3 0501-derivative-as-a-limit.py
"""

from __future__ import annotations

import numpy as np


def f(x: float) -> float:
    """The function under test. Nothing special about it: it is smooth, it is
    not a polynomial, and its exact derivative is short enough to check."""
    return float(np.sin(x) * np.exp(x / 3.0))


def f_prime_exact(x: float) -> float:
    """d/dx [sin(x) e^(x/3)] by the product rule."""
    return float(np.cos(x) * np.exp(x / 3.0) + np.sin(x) * np.exp(x / 3.0) / 3.0)


def forward_difference(fn, x: float, h: float) -> float:
    """(f(x+h) - f(x)) / h. The difference quotient exactly as the definition
    of the derivative writes it, stopped before the limit."""
    return (fn(x + h) - fn(x)) / h


def central_difference(fn, x: float, h: float) -> float:
    """(f(x+h) - f(x-h)) / 2h. Straddles x instead of stepping off it, which
    cancels the leading error term."""
    return (fn(x + h) - fn(x - h)) / (2.0 * h)


def error_table(x: float, powers: range) -> list[tuple[float, float, float]]:
    exact = f_prime_exact(x)
    rows = []
    for k in powers:
        h = 10.0**-k
        rows.append(
            (
                h,
                abs(forward_difference(f, x, h) - exact),
                abs(central_difference(f, x, h) - exact),
            )
        )
    return rows


def main() -> None:
    x = 1.2
    exact = f_prime_exact(x)
    print(f"exact f'({x}) = {exact:.12f}\n")

    rows = error_table(x, range(1, 13))
    print(f"{'h':>10} {'forward error':>16} {'central error':>16}")
    for h, fwd, ctr in rows:
        print(f"{h:10.0e} {fwd:16.3e} {ctr:16.3e}")

    best_fwd = min(rows, key=lambda r: r[1])
    best_ctr = min(rows, key=lambda r: r[2])
    print(f"\nforward difference is best at h = {best_fwd[0]:.0e}, error {best_fwd[1]:.3e}")
    print(f"central difference is best at h = {best_ctr[0]:.0e}, error {best_ctr[2]:.3e}")

    # The order of accuracy, read off the table rather than asserted. Halving
    # the exponent of h should divide the forward error by 10 and the central
    # error by 100, while truncation error still dominates.
    h1, fwd1, ctr1 = rows[1]   # h = 1e-2
    h2, fwd2, ctr2 = rows[2]   # h = 1e-3
    print(f"\nmeasured order, {h1:.0e} -> {h2:.0e}:")
    print(f"  forward error ratio {fwd1 / fwd2:8.2f}   (first order predicts 10)")
    print(f"  central error ratio {ctr1 / ctr2:8.2f}   (second order predicts 100)")


if __name__ == "__main__":
    main()
