"""M06 L07 - Adaptive learning rates: one step size per parameter.

COMPUTES IT TWICE: Adam's trajectory, once from Algorithm 1 written out line
by line exactly as the paper states it, and once vectorised over all
coordinates. They must agree to machine precision.

It then does three things the page needs:
  - runs the same problem with bias correction off, so you can see the first
    steps differ and the last steps do not,
  - reproduces Reddi, Kale and Kumar's counterexample, where Adam converges
    to the WORST point of a convex feasible set,
  - shows AdaGrad's effective rate decaying monotonically, which is what
    RMSProp's moving average was invented to repair.

    python3 0058-adaptive-learning-rates.py

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


ALPHA, BETA1, BETA2, EPS = 0.001, 0.9, 0.999, 1e-8


def gradient(design, target, theta):
    return design.T @ (sigmoid(design @ theta) - target) / len(target)


def adam_by_the_paper(design, target, steps, correct=True):
    """Algorithm 1 of Kingma and Ba, one coordinate at a time."""
    size = design.shape[1]
    theta = [0.0] * size
    first = [0.0] * size
    second = [0.0] * size
    for step in range(1, steps + 1):
        grad = gradient(design, target, np.array(theta))
        for index in range(size):
            g = float(grad[index])
            first[index] = BETA1 * first[index] + (1 - BETA1) * g
            second[index] = BETA2 * second[index] + (1 - BETA2) * g * g
            if correct:
                m_hat = first[index] / (1 - BETA1 ** step)
                v_hat = second[index] / (1 - BETA2 ** step)
            else:
                m_hat, v_hat = first[index], second[index]
            theta[index] -= ALPHA * m_hat / (np.sqrt(v_hat) + EPS)
    return np.array(theta)


def adam_vectorised(design, target, steps, correct=True):
    theta = np.zeros(design.shape[1])
    first = np.zeros_like(theta)
    second = np.zeros_like(theta)
    for step in range(1, steps + 1):
        grad = gradient(design, target, theta)
        first = BETA1 * first + (1 - BETA1) * grad
        second = BETA2 * second + (1 - BETA2) * grad ** 2
        if correct:
            m_hat = first / (1 - BETA1 ** step)
            v_hat = second / (1 - BETA2 ** step)
        else:
            m_hat, v_hat = first, second
        theta -= ALPHA * m_hat / (np.sqrt(v_hat) + EPS)
    return theta


def main() -> None:
    design, target = load(standardise=True)
    print("M06 L07 - Adam, two implementations and one counterexample")
    print()

    a = adam_by_the_paper(design, target, 60)
    b = adam_vectorised(design, target, 60)
    print(f"  Algorithm 1, coordinate by coordinate vs vectorised, 60 steps")
    print(f"    largest disagreement: {np.max(np.abs(a - b)):.3e}")
    print(f"    objective reached   : {mean_logistic_loss(design, target, a):.8f}")
    print()

    print("  Bias correction, on and off")
    for steps in (1, 5, 20, 100, 400):
        on = adam_vectorised(design, target, steps, correct=True)
        off = adam_vectorised(design, target, steps, correct=False)
        print(f"    after {steps:>4} steps   ||theta|| on = {np.linalg.norm(on):.6f}"
              f"   off = {np.linalg.norm(off):.6f}"
              f"   ratio = {np.linalg.norm(on) / max(np.linalg.norm(off), 1e-12):.3f}")
    print("    The correction matters early and washes out later, which is exactly")
    print("    what dividing by (1 - beta^t) is supposed to do.")
    print()

    print("  The inflation factor 1/(1 - beta2^t), beta2 = 0.999")
    for step in (1, 2, 10, 100, 1000, 5000):
        print(f"    t = {step:>5}   1 - beta1^t = {1 - BETA1 ** step:.6f}"
              f"   1 - beta2^t = {1 - BETA2 ** step:.6f}"
              f"   inflation = {1 / (1 - BETA2 ** step):>8.1f}x")
    print()

    print("  Reddi, Kale and Kumar (ICLR 2018): Adam on a convex problem")
    print("    f_t(x) = C*x when t mod 3 == 1, else -x.  F = [-1, 1].  C = 3.")
    print("    The optimum is x = -1. Watch where Adam goes.")
    C = 3.0
    beta2 = 1.0 / (1.0 + C * C)
    x, first, second = 0.0, 0.0, 0.0
    for step in range(1, 2_000_001):
        g = C if step % 3 == 1 else -1.0
        first = 0.0 * first + 1.0 * g          # beta1 = 0, as the paper sets it
        second = beta2 * second + (1 - beta2) * g * g
        x -= (0.1 / np.sqrt(step)) * first / (np.sqrt(second) + 1e-16)
        x = min(1.0, max(-1.0, x))
        if step in (3, 30, 300, 3_000, 30_000, 2_000_000):
            print(f"      t = {step:>9,}   x = {x:+.6f}")
    print(f"    beta2 = 1/(1 + C^2) = {beta2}")
    print("    Adam converges to +1: the WORST point of the feasible set.")
    print("    The one informative gradient C arrives every third step and is")
    print("    divided by a second moment it dominates, so it is scaled down by")
    print("    roughly C. The two misleading gradients are not.")
    print()

    print("  AdaGrad's effective rate can only fall")
    rng = np.random.default_rng(5)
    accumulator = 0.0
    print("    step    accumulated g^2    effective rate")
    for step in range(1, 10_001):
        g = rng.normal(0.0, 1.0)
        accumulator += g * g
        if step in (1, 10, 100, 1_000, 10_000):
            print(f"    {step:>5}    {accumulator:>15.2f}    {0.1 / np.sqrt(accumulator):.6f}")
    print("    A sum of squares never decreases, so this column never rises.")
    print("    RMSProp replaces the sum with a moving average, which can.")


if __name__ == "__main__":
    main()
