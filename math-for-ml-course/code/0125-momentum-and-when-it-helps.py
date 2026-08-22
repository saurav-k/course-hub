"""M06 L06 - Momentum: when averaging past gradients actually helps.

COMPUTES IT TWICE: the iterations needed to reach a fixed objective gap,
once for plain gradient descent and once for momentum, at the same step size
from the same start. The ratio is what turns "momentum helps" into a number.

It also checks the terminal-velocity formula directly, by feeding a constant
gradient and comparing the converged velocity against -eta*g/(1 - alpha).

    python3 0125-momentum-and-when-it-helps.py

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


def gradient(design, target, theta):
    return design.T @ (sigmoid(design @ theta) - target) / len(target)


def plain(design, target, rate, target_gap, floor, cap=20_000):
    theta = np.zeros(design.shape[1])
    for step in range(1, cap + 1):
        theta -= rate * gradient(design, target, theta)
        if mean_logistic_loss(design, target, theta) - floor < target_gap:
            return step
    return None


def with_momentum(design, target, rate, alpha, target_gap, floor,
                  nesterov=False, cap=20_000):
    theta = np.zeros(design.shape[1])
    velocity = np.zeros_like(theta)
    for step in range(1, cap + 1):
        point = theta + alpha * velocity if nesterov else theta
        velocity = alpha * velocity - rate * gradient(design, target, point)
        theta = theta + velocity
        if mean_logistic_loss(design, target, theta) - floor < target_gap:
            return step
    return None


def main() -> None:
    design, target = load(standardise=True)
    print("M06 L06 - what momentum actually buys, counted in iterations")
    print()

    # Part 1: the terminal velocity formula, checked directly.
    print("  Terminal velocity under a constant gradient g = 1.0, eta = 0.1")
    print("    alpha    converged v     -eta*g/(1-alpha)    1/(1-alpha)")
    for alpha in (0.0, 0.5, 0.9, 0.99):
        velocity = 0.0
        for _ in range(20_000):
            velocity = alpha * velocity - 0.1 * 1.0
        predicted = -0.1 * 1.0 / (1.0 - alpha)
        print(f"     {alpha:<6}  {velocity:12.6f}    {predicted:12.6f}"
              f"     {1 / (1 - alpha):9.1f}x")
    print()

    # Part 2: the hand-worked two-coordinate example from the page.
    print("  The page's worked example: eta = 0.1, alpha = 0.9")
    for label, gradients in (("oscillating (+1,-1,+1,-1)", [1.0, -1.0, 1.0, -1.0]),
                             ("consistent  (+0.2 each)  ", [0.2, 0.2, 0.2, 0.2])):
        velocity, path = 0.0, []
        for g in gradients:
            velocity = 0.9 * velocity - 0.1 * g
            path.append(velocity)
        print(f"    {label}: " + ", ".join(f"{v:+.4f}" for v in path))
    print("    One cancels itself. The other accumulates. Same size gradients.")
    print()

    # Part 3: momentum's benefit depends on the condition number, so measure
    # it against the condition number rather than asserting it once.
    print("  Iterations to reach a 1e-8 gap on f(x) = 0.5*(x1^2 + g*x2^2),")
    print("  at eta = 1/lambda_max, from x0 = (g, 1). kappa = g.")
    print()
    print("    kappa      plain GD    momentum(0.9)   Nesterov(0.9)   speed-up")
    for gamma in (2.0, 10.0, 50.0, 200.0, 1000.0):
        curvature = np.array([1.0, gamma])
        rate = 1.0 / max(curvature)
        start = np.array([gamma, 1.0])

        def run(alpha, nesterov):
            x = start.copy()
            velocity = np.zeros(2)
            for step in range(1, 200_001):
                point = x + alpha * velocity if nesterov else x
                velocity = alpha * velocity - rate * (curvature * point)
                x = x + velocity
                if 0.5 * float(curvature @ (x ** 2)) < 1e-8:
                    return step
            return None

        plain_steps = run(0.0, False)
        momentum_steps = run(0.9, False)
        nesterov_steps = run(0.9, True)
        ratio = (f"{plain_steps / momentum_steps:.1f}x"
                 if plain_steps and momentum_steps else "n/a")
        print(f"    {gamma:>7.0f}    {str(plain_steps):>9}    {str(momentum_steps):>12}"
              f"   {str(nesterov_steps):>13}   {ratio:>8}")
    print()
    print("  The speed-up grows with the condition number, which is the claim:")
    print("  momentum is a cure for a stretched bowl, not a general accelerant.")
    print()

    # Part 4: and on the real, well-conditioned credit problem it barely helps.
    theta = np.zeros(design.shape[1])
    for _ in range(5_000):
        theta -= 1.0 * gradient(design, target, theta)
    floor = mean_logistic_loss(design, target, theta)
    print(f"  Now the real credit problem, where kappa is only 26.5.")
    print(f"  full-batch optimum objective: {floor:.8f}")
    print()
    print("   target gap    plain GD    momentum(0.9)   Nesterov(0.9)")
    for gap in (1e-3, 1e-4, 1e-5):
        a = plain(design, target, 1.0, gap, floor)
        b = with_momentum(design, target, 1.0, 0.9, gap, floor)
        c = with_momentum(design, target, 1.0, 0.9, gap, floor, nesterov=True)
        print(f"    {gap:.0e}    {str(a):>9}    {str(b):>12}   {str(c):>13}")
    print()
    print("  Momentum is not reliably ahead here, and at some targets it is behind.")
    print("  That is not a bug in the run. A well-conditioned problem has little")
    print("  zigzag to cancel, so there is little for averaging to recover, and")
    print("  the extra effective step size can overshoot. Nesterov, which")
    print("  evaluates after the jump, is the more stable of the two throughout.")
    print()
    print("  Report this honestly on the page. An optimizer that helps on every")
    print("  problem does not exist, and a course that implies one is teaching")
    print("  the reader to stop measuring.")


if __name__ == "__main__":
    main()
