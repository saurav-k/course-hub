"""M06 L08 - Newton's method, and why nobody runs it at scale.

COMPUTES IT TWICE: the optimum of the logistic objective, once by Newton's
method (which for logistic regression is iteratively reweighted least
squares) and once by gradient descent run to convergence. They must agree to
several decimals while the iteration counts differ by orders of magnitude.

It also demonstrates the two theorems the page proves:
  - Newton is exact on a quadratic in one step, from any start.
  - Newton is affine invariant: rescale a feature column by a million and
    its iteration count does not move, while gradient descent's does.

    python3 m06-08-newton.py

Needs numpy and pandas. Dataset: ../datasets/m06-credit.csv
"""

import numpy as np

from m06_common import load, mean_logistic_loss, sigmoid


def gradient(design, target, theta):
    return design.T @ (sigmoid(design @ theta) - target) / len(target)


def hessian(design, theta):
    probability = sigmoid(design @ theta)
    weights = probability * (1.0 - probability)
    return (design * weights[:, None]).T @ design / len(design)


# Tolerances are loose enough to run in seconds on a laptop and tight enough
# that the iteration-count contrast is unambiguous. Tighten them if you want
# to watch Newton's quadratic convergence do its last two digits.
def newton(design, target, tolerance=1e-8, cap=100):
    theta = np.zeros(design.shape[1])
    for step in range(1, cap + 1):
        grad = gradient(design, target, theta)
        if np.linalg.norm(grad) < tolerance:
            return theta, step
        # solve, never invert: same answer, better conditioned, and it is
        # what any real implementation does.
        theta = theta - np.linalg.solve(hessian(design, theta), grad)
    return theta, cap


def descend(design, target, rate, tolerance=1e-8, cap=40_000):
    theta = np.zeros(design.shape[1])
    for step in range(1, cap + 1):
        grad = gradient(design, target, theta)
        if np.linalg.norm(grad) < tolerance:
            return theta, step
        theta = theta - rate * grad
    return theta, cap


def main() -> None:
    print("M06 L08 - the second-order step, and what it costs")
    print()

    print("  Theorem 1: Newton is exact on a quadratic, in one step, from anywhere.")
    rng = np.random.default_rng(17)
    size = 6
    root = rng.normal(0.0, 1.0, (size, size))
    matrix = root @ root.T + size * np.eye(size)      # symmetric positive definite
    vector = rng.normal(0.0, 1.0, size)
    truth = np.linalg.solve(matrix, vector)
    for trial in range(3):
        start = rng.normal(0.0, 50.0, size)
        step = start - np.linalg.solve(matrix, matrix @ start - vector)
        print(f"    start norm {np.linalg.norm(start):8.3f}"
              f"   after ONE Newton step, distance to optimum:"
              f" {np.linalg.norm(step - truth):.3e}")
    print()

    design, target = load(standardise=True)
    print("  Two routes to the same optimum on the credit objective")
    theta_newton, newton_steps = newton(design, target)
    theta_gd, gd_steps = descend(design, target, 1.0, cap=40_000)
    print(f"    Newton           : {newton_steps:>7} iterations"
          f"   objective {mean_logistic_loss(design, target, theta_newton):.10f}")
    print(f"    gradient descent : {gd_steps:>7} iterations"
          f"   objective {mean_logistic_loss(design, target, theta_gd):.10f}")
    print(f"    largest coefficient disagreement: "
          f"{np.max(np.abs(theta_newton - theta_gd)):.3e}")
    print(f"    iteration ratio  : {gd_steps / newton_steps:.0f}x")
    print()

    print("  Theorem 2: affine invariance. Rescale one column and re-run.")
    print("    scaling      Newton steps    GD steps (eta = 1/L, recomputed)")
    for scale in (1.0, 1e2, 1e4):
        scaled = design.copy()
        scaled[:, 3] *= scale
        _, n_steps = newton(scaled, target)
        largest = np.linalg.eigvalsh(hessian(scaled, np.zeros(scaled.shape[1])))[-1]
        _, g_steps = descend(scaled, target, 1.0 / largest, tolerance=1e-6,
                             cap=30_000)
        capped = " (capped)" if g_steps >= 30_000 else ""
        print(f"    {scale:>9.0e}    {n_steps:>12}    {g_steps:>12}{capped}")
    print("    Newton does not notice. Gradient descent does. That is the whole")
    print("    of L04, made irrelevant by a method nobody can afford.")
    print()

    print("  And the reason nobody can afford it")
    print("    model                              k        Hessian entries"
          "      bytes at 2/entry")
    for label, k in (("logistic regression, 12 features", 13),
                     ("a small network", 10_000),
                     ("a mid-size network", 10_000_000),
                     ("GPT-3 scale (175B params)", 175_000_000_000)):
        entries = float(k) ** 2
        print(f"    {label:<34} {k:>13,}    {entries:>14.3e}   {2 * entries:>14.3e}")
    print()
    largest_fitting = int(np.sqrt(80e9 / 2))
    print(f"    Largest k whose Hessian fits one 80 GB accelerator: {largest_fitting:,}")
    print(f"    GPT-3's Hessian at 2 bytes an entry: "
          f"{2 * (175e9 ** 2) / 1e21:.1f} zettabytes")
    print("    Assumptions, stated: bfloat16, and the textbook k^3 bound for the")
    print("    solve. Storage is only half the bill - the solve is the other half,")
    print("    and it is redone every iteration because the parameters moved.")


if __name__ == "__main__":
    main()
