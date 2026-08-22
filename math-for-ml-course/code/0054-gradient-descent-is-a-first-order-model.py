"""M06 L03 - Gradient descent is a first-order model, taken one step at a time.

COMPUTES IT TWICE: the descent direction, once as the analytic gradient and
once by central finite differences on every coordinate. They must agree to
about 1e-7.

A gradient check is the single most useful habit this module can hand you,
and running it here - before any optimizer exists - is the right place for it.
Every optimizer in the rest of M06 trusts this gradient. If it is wrong,
nothing downstream can be right, and nothing downstream will tell you.

    python3 0054-gradient-descent-is-a-first-order-model.py

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


def objective(design: np.ndarray, target: np.ndarray, theta: np.ndarray) -> float:
    """Stable mean logistic loss - see m06_common.mean_logistic_loss."""
    return mean_logistic_loss(design, target, theta)


def analytic_gradient(design: np.ndarray, target: np.ndarray, theta: np.ndarray) -> np.ndarray:
    return design.T @ (sigmoid(design @ theta) - target) / len(target)


def numeric_gradient(design: np.ndarray, target: np.ndarray,
                     theta: np.ndarray, step: float = 1e-6) -> np.ndarray:
    """Central differences. Two objective evaluations per parameter."""
    gradient = np.zeros_like(theta)
    for index in range(len(theta)):
        forward, backward = theta.copy(), theta.copy()
        forward[index] += step
        backward[index] -= step
        gradient[index] = (objective(design, target, forward)
                           - objective(design, target, backward)) / (2.0 * step)
    return gradient


def main() -> None:
    design, target = load()
    rng = np.random.default_rng(3)
    theta = rng.normal(0.0, 0.3, design.shape[1])

    print("M06 L03 - the gradient check, then the descent")
    print()
    exact = analytic_gradient(design, target, theta)
    approx = numeric_gradient(design, target, theta)
    relative = np.abs(exact - approx) / np.maximum(np.abs(exact), 1e-12)
    print("  coordinate       analytic        numeric      relative error")
    for index in range(len(theta)):
        print(f"    {index:>3}        {exact[index]:> .8f}   {approx[index]:> .8f}"
              f"      {relative[index]:.2e}")
    print(f"  worst relative error: {relative.max():.3e}")
    print("  Anything above about 1e-5 means the analytic gradient is wrong.")
    print()

    # The hand-worked example from the page, at full precision.
    print("The page's hand-worked example: J(w) = (w - 3)^2, w0 = 0")
    for learning_rate in (0.1, 0.6, 1.0):
        weight = 0.0
        path = [weight]
        for _ in range(5):
            weight = weight - learning_rate * 2.0 * (weight - 3.0)
            path.append(weight)
        factor = 1.0 - 2.0 * learning_rate
        print(f"  eta = {learning_rate:<4} factor (1 - 2*eta) = {factor:>5.1f}   "
              + ", ".join(f"{value:.4f}" for value in path))
    print("  At eta = 1.0 the factor is exactly -1, so it alternates forever.")
    print("  It neither converges nor diverges. L04 is the page about that edge.")
    print()

    # The real descent, and the rate.
    print("Full-batch gradient descent on the credit objective")
    theta = np.zeros(design.shape[1])
    learning_rate = 1.0
    best = None
    for iteration in range(1, 3001):
        theta -= learning_rate * analytic_gradient(design, target, theta)
        if iteration in (1, 10, 100, 1000, 3000):
            value = objective(design, target, theta)
            print(f"  step {iteration:>5}   objective = {value:.8f}")
            best = value
    print()
    print(f"  final objective: {best:.8f}")
    print("  Notice how much of the fall happened in the first ten steps,")
    print("  and how little in the last two thousand. That is O(1/t).")


if __name__ == "__main__":
    main()
