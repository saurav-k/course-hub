"""Lesson 0508 - what a long chain of Jacobians costs, and how it decays.

Implements two named results.

1.  The cost of a Jacobian by mode (Griewank and Walther, quoted by Baydin et
    al. 2018). For f: R^n -> R^m,

        forward mode   n . c . ops(f)
        reverse mode   m . c . ops(f)          c < 6, typically 2 to 3

    so with one scalar loss and n parameters, reverse mode wins by a factor of
    n. The program measures the ratio directly by running both modes on the
    same function and counting wall-clock, rather than quoting the bound.

2.  The vanishing and exploding gradient condition (Pascanu, Mikolov and
    Bengio 2013). A gradient reaching back k steps carries a product of k
    Jacobians, and with |sigma'| <= gamma it is sufficient for the largest
    eigenvalue of the recurrent matrix to satisfy lambda_1 < 1/gamma for the
    long-term contribution to vanish. The program builds recurrent matrices at
    chosen spectral radii and measures the decay.

    python3 0508-a-long-chain-of-jacobians.py
"""

from __future__ import annotations

import time

import numpy as np

SEED = 20260822


def chain(x: np.ndarray, weights: list[np.ndarray]) -> float:
    """A deep scalar-valued function: repeated tanh layers, then a sum."""
    v = x
    for w in weights:
        v = np.tanh(w @ v)
    return float(v.sum())


def forward_mode_gradient(x: np.ndarray, weights: list[np.ndarray]) -> np.ndarray:
    """One sweep per input. Each sweep carries a tangent vector forward.

    This is the honest cost of forward mode for a scalar output: n sweeps, and
    the program pays every one of them.
    """
    n = len(x)
    out = np.empty(n)
    for j in range(n):
        v, dv = x, np.eye(n)[j]
        for w in weights:
            pre = w @ v
            v = np.tanh(pre)
            dv = (1.0 - v**2) * (w @ dv)
        out[j] = dv.sum()
    return out


def reverse_mode_gradient(x: np.ndarray, weights: list[np.ndarray]) -> np.ndarray:
    """One sweep, total. Forward once keeping the activations, then backward
    once carrying an adjoint."""
    activations = [x]
    v = x
    for w in weights:
        v = np.tanh(w @ v)
        activations.append(v)
    adjoint = np.ones_like(v)
    for w, out in zip(reversed(weights), reversed(activations[1:])):
        adjoint = w.T @ (adjoint * (1.0 - out**2))
    return adjoint


def matrix_with_spectral_radius(dim: int, radius: float, rng: np.random.Generator) -> np.ndarray:
    """A random square matrix rescaled so its largest eigenvalue modulus is
    exactly the radius asked for."""
    m = rng.normal(size=(dim, dim))
    current = np.abs(np.linalg.eigvals(m)).max()
    return m * (radius / current)


def main() -> None:
    rng = np.random.default_rng(SEED)

    print("1. forward mode against reverse mode, measured")
    dim, depth = 60, 12
    weights = [matrix_with_spectral_radius(dim, 0.95, rng) for _ in range(depth)]
    x = rng.normal(size=dim)

    g_rev = reverse_mode_gradient(x, weights)
    g_fwd = forward_mode_gradient(x, weights)
    print(f"   function R^{dim} -> R, {depth} layers")
    print(f"   the two modes agree to {np.abs(g_fwd - g_rev).max():.3e}")

    start = time.perf_counter()
    for _ in range(5):
        reverse_mode_gradient(x, weights)
    rev_s = (time.perf_counter() - start) / 5
    start = time.perf_counter()
    for _ in range(5):
        forward_mode_gradient(x, weights)
    fwd_s = (time.perf_counter() - start) / 5
    print(f"   reverse mode : {rev_s * 1e3:8.3f} ms")
    print(f"   forward mode : {fwd_s * 1e3:8.3f} ms")
    print(f"   ratio        : {fwd_s / rev_s:8.1f} x   (the bound predicts about n = {dim})")

    print("\n2. the product of Jacobians decays or explodes geometrically")
    print(f"   {'spectral radius':>16} {'30 layers':>14} {'100 layers':>14}")
    for radius in (0.90, 0.99, 1.00, 1.01, 1.10):
        print(f"   {radius:16.2f} {radius**30:14.4g} {radius**100:14.4g}")

    print("\n   the same thing measured on real Jacobian products, dim 60")
    for radius in (0.90, 1.00, 1.10):
        mats = [matrix_with_spectral_radius(60, radius, rng) for _ in range(30)]
        v = rng.normal(size=60)
        v = v / np.linalg.norm(v)
        for m in mats:
            v = m.T @ v
        print(f"   radius {radius:.2f}: a unit gradient arrives with norm "
              f"{np.linalg.norm(v):.4g}")
    print("   note the radius 1.00 row: a typical direction still shrinks.")
    print("   The spectral radius bounds the LARGEST growth any direction can see,")
    print("   which is why Pascanu et al. state lambda_1 < 1/gamma as SUFFICIENT for")
    print("   vanishing and lambda_1 > 1/gamma as only NECESSARY for exploding.")

    print("\n   the activation only sets the bound, per Pascanu et al. 2013")
    print("     tanh    : |sigma'| <= 1,    so vanishing is sufficient when lambda_1 < 1")
    print("     sigmoid : |sigma'| <= 0.25, so vanishing is sufficient when lambda_1 < 4")


if __name__ == "__main__":
    main()
