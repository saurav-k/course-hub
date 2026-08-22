"""M06 L02 - Convexity, and the one guarantee it buys.

COMPUTES IT TWICE: convexity of the logistic objective, once by sampling
random chords and testing the defining inequality on every one, and once by
taking the smallest eigenvalue of the analytic Hessian.

Those two are not the same kind of evidence, and the program says so.
Sampling can only ever FAIL TO FIND a counterexample. An eigenvalue is a
proof at the point where it was taken. Knowing which of your checks is which
is a habit worth more than either check.

    python3 0121-convexity-and-the-one-guarantee-it-buys.py

Needs numpy and pandas. Dataset: ../datasets/m06-credit.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

# Self-contained on purpose: this file needs only numpy and pandas, so it
# runs unchanged in a repo checkout, in Jupyter, or pasted straight into
# Google Colab. The dataset loads locally if it is beside the code and
# falls back to the published copy if it is not.
LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "m06-credit.csv" \
    if "__file__" in dir() else Path("m06-credit.csv")
URL = ("https://saurav-k.github.io/course-hub/math-for-ml-course/"
       "datasets/m06-credit.csv")

FEATURES = [
    "income_inr", "age_years", "utilisation_ratio", "enquiries_6m",
    "tenure_months", "emi_to_income", "late_payments_12m", "card_count",
    "noise_1", "noise_2", "noise_3", "noise_4",
]


def read_frame() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def sigmoid(z: np.ndarray) -> np.ndarray:
    """Logistic function, written so it does not overflow on large |z|."""
    out = np.empty_like(z, dtype=float)
    positive = z >= 0
    out[positive] = 1.0 / (1.0 + np.exp(-z[positive]))
    exp_z = np.exp(z[~positive])
    out[~positive] = exp_z / (1.0 + exp_z)
    return out


def mean_logistic_loss(design, target, theta) -> float:
    """Mean logistic loss, written so it cannot overflow or take log(0).

    The obvious form, -mean(y*log(p) + (1-y)*log(1-p)), is exact arithmetic
    and a numerical trap: once |z| passes about 37 the sigmoid rounds to
    exactly 0 or 1 and log(0) is -inf. Worse, the resulting nan compares
    False against everything, so a test built on it reports success by
    silently comparing nothing. The identity
        -y*log(p) - (1-y)*log(1-p)  =  log(1 + exp(z)) - y*z
    has no such point, and np.logaddexp(0, z) computes it stably.
    """
    logit = design @ theta
    return float(np.mean(np.logaddexp(0.0, logit) - target * logit))


def load(standardise: bool = True, add_intercept: bool = True):
    """Design matrix (n rows by d columns, one row per sample) and the target."""
    frame = read_frame()
    matrix = frame[FEATURES].to_numpy(dtype=float)
    if standardise:
        matrix = (matrix - matrix.mean(axis=0)) / matrix.std(axis=0)
    if add_intercept:
        matrix = np.column_stack([np.ones(len(matrix)), matrix])
    return matrix, frame["default"].to_numpy(dtype=float)


def load_regression(standardise: bool = True):
    """Design matrix and the continuous credit-limit target, centred."""
    frame = read_frame()
    matrix = frame[FEATURES].to_numpy(dtype=float)
    if standardise:
        matrix = (matrix - matrix.mean(axis=0)) / matrix.std(axis=0)
    target = frame["credit_limit_inr"].to_numpy(dtype=float)
    return matrix, target - target.mean()


def logistic_objective(design: np.ndarray, target: np.ndarray, theta: np.ndarray) -> float:
    """Stable mean logistic loss - see m06_common.mean_logistic_loss.

    The naive form saturates for the large random thetas this program
    samples, and a nan silently passes every comparison in the chord test.
    """
    return mean_logistic_loss(design, target, theta)


def logistic_hessian(design: np.ndarray, theta: np.ndarray) -> np.ndarray:
    probability = sigmoid(design @ theta)
    weights = probability * (1.0 - probability)
    return (design * weights[:, None]).T @ design / len(design)


def product_objective(point: np.ndarray) -> float:
    """f(a, b) = (a*b - 1)^2. The shape of every matrix-factorisation model."""
    return float((point[0] * point[1] - 1.0) ** 2)


def chord_test(evaluate, sampler, trials: int, rng) -> tuple[int, float]:
    """Count chord violations. Returns (violations, worst gap seen)."""
    violations = 0
    worst = 0.0
    for _ in range(trials):
        left, right = sampler(rng), sampler(rng)
        weight = rng.uniform(0.0, 1.0)
        midpoint = weight * left + (1.0 - weight) * right
        chord = weight * evaluate(left) + (1.0 - weight) * evaluate(right)
        gap = evaluate(midpoint) - chord          # convex means gap <= 0
        if not np.isfinite(gap):
            raise FloatingPointError(
                "non-finite chord gap - the objective overflowed, so this "
                "test would report success without having tested anything")
        if gap > 1e-9:
            violations += 1
            worst = max(worst, gap)
    return violations, worst


def main() -> None:
    design, target = load()
    rng = np.random.default_rng(11)
    dimension = design.shape[1]

    print("M06 L02 - is the logistic objective convex? Two kinds of evidence.")
    print(f"rows: {len(target):,}   parameters: {dimension}")
    print()

    print("Route 1: sample 5,000 chords and test f(mid) <= chord.")
    violations, worst = chord_test(
        lambda theta: logistic_objective(design, target, theta),
        lambda r: r.normal(0.0, 1.5, dimension),
        5_000, rng)
    print(f"  violations: {violations} of 5,000   worst gap: {worst:.3e}")
    print("  A clean run here is FAILURE TO FIND a counterexample.")
    print("  It is not a proof, and no number of samples would make it one.")
    print()

    print("Route 2: the smallest eigenvalue of the analytic Hessian.")
    for label, theta in (("theta = 0", np.zeros(dimension)),
                         ("a random theta", rng.normal(0.0, 0.5, dimension))):
        eigenvalues = np.linalg.eigvalsh(logistic_hessian(design, theta))
        print(f"  at {label:<16} smallest = {eigenvalues[0]:.6e}"
              f"   largest = {eigenvalues[-1]:.6e}"
              f"   {'positive definite' if eigenvalues[0] > 0 else 'NOT positive definite'}")
    print("  A positive semi-definite Hessian at a point IS a proof of convexity there.")
    print()

    print("Now the counterexample: f(a, b) = (a*b - 1)^2.")
    violations, worst = chord_test(
        product_objective, lambda r: r.normal(0.0, 1.5, 2), 5_000, rng)
    print(f"  violations: {violations} of 5,000   worst gap: {worst:.4f}")
    left, right = np.array([1.0, 1.0]), np.array([-1.0, -1.0])
    midpoint = 0.5 * (left + right)
    print(f"  the hand-picked pair from the page:")
    print(f"    f(1, 1)    = {product_objective(left):.1f}")
    print(f"    f(-1, -1)  = {product_objective(right):.1f}")
    print(f"    average    = {0.5 * (product_objective(left) + product_objective(right)):.1f}")
    print(f"    f(midpoint)= {product_objective(midpoint):.1f}   <- above the chord")
    print()
    print("One counterexample settles it. Five thousand clean samples do not.")
    print("That asymmetry is the whole difference between the two routes.")


if __name__ == "__main__":
    main()
