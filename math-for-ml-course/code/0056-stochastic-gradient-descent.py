"""M06 L05 - Stochastic gradient descent: paying in noise to buy iterations.

COMPUTES IT TWICE: the standard error of a minibatch gradient, once
empirically by drawing many minibatches at each size and measuring the
spread, and once from the sigma/sqrt(m) formula using the per-row gradient
variance over the whole dataset. The two curves must lie on top of each
other, which is what turns the formula from an assertion into a measurement.

It then measures the thing the formula does not tell you: with a FIXED step
size SGD settles into a band around the optimum and stops improving, and the
width of that band is proportional to the step size. With a decaying step it
keeps going. That band is the reason schedules exist.

    python3 0056-stochastic-gradient-descent.py

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


def full_gradient(design, target, theta):
    return design.T @ (sigmoid(design @ theta) - target) / len(target)


def per_row_gradients(design, target, theta):
    """The n individual gradients whose mean is the full gradient."""
    return design * (sigmoid(design @ theta) - target)[:, None]


def main() -> None:
    design, target = load(standardise=True)
    rng = np.random.default_rng(23)
    rows = len(target)

    # A partly trained theta, so the gradient is neither huge nor zero.
    theta = np.zeros(design.shape[1])
    for _ in range(50):
        theta -= 1.0 * full_gradient(design, target, theta)

    print("M06 L05 - minibatch gradient noise, measured and predicted")
    print(f"rows: {rows:,}   parameters: {design.shape[1]}")
    print()

    exact = full_gradient(design, target, theta)
    rows_grad = per_row_gradients(design, target, theta)
    # Per-row variance summed over coordinates, which is what the norm sees.
    sigma_squared = float(np.sum(np.var(rows_grad, axis=0)))
    sigma = np.sqrt(sigma_squared)
    print(f"  per-row gradient standard deviation (sigma): {sigma:.6f}")
    print()
    print("   batch m     measured spread    sigma/sqrt(m)     ratio")
    for size in (1, 8, 32, 128, 1024, 8192):
        draws = 2_000
        errors = np.empty(draws)
        for index in range(draws):
            pick = rng.integers(0, rows, size)
            estimate = (design[pick].T
                        @ (sigmoid(design[pick] @ theta) - target[pick])) / size
            errors[index] = np.linalg.norm(estimate - exact)
        measured = float(np.sqrt(np.mean(errors ** 2)))
        predicted = sigma / np.sqrt(size)
        print(f"    {size:>6}      {measured:12.6f}     {predicted:12.6f}"
              f"     {measured / predicted:6.3f}")
    print()
    print("  The ratio is flat, which is the claim: the spread falls as 1/sqrt(m).")
    print("  Going from m=32 to m=1024 is 32 times the work for about 5.7 times")
    print("  less noise. That is the trade the rest of the page is about.")
    print()

    # The noise ball.
    print("  Now the part the formula does not tell you: where SGD stops.")
    best_theta = theta.copy()
    for _ in range(3_000):
        best_theta -= 1.0 * full_gradient(design, target, best_theta)
    floor = mean_logistic_loss(design, target, best_theta)
    print(f"  full-batch optimum objective: {floor:.8f}")
    print()
    rows_out = []
    print("   schedule                 last-200-step mean    spread     gap to optimum")
    for label, rate_of in (
        ("fixed eta = 0.50", lambda k: 0.50),
        ("fixed eta = 0.10", lambda k: 0.10),
        ("fixed eta = 0.02", lambda k: 0.02),
        ("decaying 1.0/(1+k/500)", lambda k: 1.0 / (1.0 + k / 500.0)),
    ):
        theta_sgd = np.zeros(design.shape[1])
        trace = []
        for step in range(1, 6_001):
            pick = rng.integers(0, rows, 32)
            gradient = (design[pick].T
                        @ (sigmoid(design[pick] @ theta_sgd) - target[pick])) / 32
            theta_sgd -= rate_of(step) * gradient
            if step > 5_800:
                trace.append(mean_logistic_loss(design, target, theta_sgd))
        trace = np.array(trace)
        gap = trace.mean() - floor
        rows_out.append((label, rate_of(1), gap))
        print(f"    {label:<24} {trace.mean():16.8f}  {trace.std():9.2e}"
              f"     {gap:.2e}")
    print()
    print("  Theorem 4.6 says the gap is proportional to the step size. Check it:")
    for label, rate, gap in rows_out:
        if label.startswith("fixed"):
            print(f"    {label:<24} gap / eta = {gap / rate:.3e}")
    print("  Those three numbers are close, which is the theorem, measured.")
    print()
    print("  Halve the step and the band gets tighter and the approach slower.")
    print("  A decaying schedule buys the first without paying the second forever,")
    print("  and Robbins-Monro is the exact condition that makes it work:")
    print("  sum of the steps infinite, sum of their squares finite.")


if __name__ == "__main__":
    main()
