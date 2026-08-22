"""M06 L09 - Saddle points and plateaus.

COMPUTES IT TWICE: the character of a critical point, once from the
eigenvalue signs of the analytic Hessian and once by sampling the objective
on a small sphere around the point and asking whether some directions rise
and some fall. They must agree.

The sampling route is what you can do when you cannot form a Hessian, which
is the real case. Seeing it agree where both are available is what earns it
your trust where only one is.

It also runs the page's central surprise: from the same start near a saddle,
gradient descent leaves and Newton arrives.

    python3 0060-saddle-points-and-plateaus.py

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


def classify_by_eigenvalues(hessian_matrix, tolerance=1e-9):
    eigenvalues = np.linalg.eigvalsh(hessian_matrix)
    positive = int(np.sum(eigenvalues > tolerance))
    negative = int(np.sum(eigenvalues < -tolerance))
    if negative == 0 and positive > 0:
        return "minimum", eigenvalues
    if positive == 0 and negative > 0:
        return "maximum", eigenvalues
    return "saddle", eigenvalues


def classify_by_sampling(objective, point, radius=1e-3, draws=4_000, rng=None):
    rng = rng or np.random.default_rng(0)
    here = objective(point)
    rose = fell = 0
    for _ in range(draws):
        direction = rng.normal(0.0, 1.0, len(point))
        direction /= np.linalg.norm(direction)
        difference = objective(point + radius * direction) - here
        if difference > 1e-12:
            rose += 1
        elif difference < -1e-12:
            fell += 1
    if fell == 0:
        return "minimum", rose, fell
    if rose == 0:
        return "maximum", rose, fell
    return "saddle", rose, fell


def main() -> None:
    rng = np.random.default_rng(31)
    print("M06 L09 - what a zero gradient actually is, in high dimensions")
    print()

    print("  Two routes to the character of a critical point")
    cases = {
        "f(x,y) = x^2 + y^2      (a bowl)":
            (lambda p: float(p[0] ** 2 + p[1] ** 2), np.array([2.0, 2.0])),
        "f(x,y) = x^2 - y^2      (a saddle)":
            (lambda p: float(p[0] ** 2 - p[1] ** 2), np.array([2.0, -2.0])),
        "f(x,y) = -x^2 - y^2     (a dome)":
            (lambda p: float(-p[0] ** 2 - p[1] ** 2), np.array([-2.0, -2.0])),
    }
    for label, (objective, curvature) in cases.items():
        matrix = np.diag(curvature)
        by_eigen, eigenvalues = classify_by_eigenvalues(matrix)
        by_sample, rose, fell = classify_by_sampling(objective, np.zeros(2), rng=rng)
        agree = "agree" if by_eigen == by_sample else "DISAGREE"
        # Both bowl and dome were mis-specified when this was first written,
        # and this line is what caught it. Keep the check: a consistency test
        # you never see fail is a test you have no reason to believe.
        print(f"    {label}")
        print(f"      eigenvalues {np.array2string(eigenvalues, precision=1)}"
              f"  ->  {by_eigen}")
        print(f"      sampling: {rose} rose, {fell} fell  ->  {by_sample}   [{agree}]")
    print()

    print("  The surprise: from the same start near the saddle f(x,y) = x^2 - y^2")
    start = np.array([0.01, 0.01])
    curvature = np.array([2.0, -2.0])          # the Hessian, constant here
    print("    step   gradient descent |x|      Newton |x|")
    gd_point, newton_point = start.copy(), start.copy()
    for step in range(1, 41):
        gd_point = gd_point - 0.1 * (curvature * gd_point)
        newton_point = newton_point - np.linalg.solve(np.diag(curvature),
                                                      curvature * newton_point)
        if step in (1, 5, 10, 20, 40):
            print(f"    {step:>4}   {np.linalg.norm(gd_point):>20.6e}"
                  f"   {np.linalg.norm(newton_point):>13.6e}")
    print("    Gradient descent leaves along the negative-curvature direction.")
    print("    Newton divides by the negative eigenvalue, which flips the step,")
    print("    so it walks INTO the saddle. The exact second-order step is a trap")
    print("    exactly where the landscape is hardest.")
    print()

    print("  Why saddles dominate: the coin-flip model, ratio = 2^n - 2")
    print("    (an idealisation - real Hessian spectra are not independent flips)")
    for dimension in (1, 2, 10, 50, 200):
        ratio = 2.0 ** dimension - 2.0
        print(f"    n = {dimension:>4}   P(all positive) = {2.0 ** -dimension:.3e}"
              f"   saddles per minimum = {ratio:.3e}")
    print()

    print("  The diagnostic: three flat losses, three different causes")
    design, target = load(standardise=True)

    def gradient(theta):
        return design.T @ (sigmoid(design @ theta) - target) / len(target)

    print("     run                          gradient norm      diagnosis")
    theta = np.zeros(design.shape[1])
    for _ in range(5_000):
        theta -= 1.0 * gradient(theta)
    print(f"    converged (5,000 steps)      {np.linalg.norm(gradient(theta)):.3e}"
          f"        at a critical point")
    theta_slow = np.zeros(design.shape[1])
    for _ in range(20):
        theta_slow -= 1e-4 * gradient(theta_slow)
    print(f"    step far too small (20)      {np.linalg.norm(gradient(theta_slow)):.3e}"
          f"        NOT a critical point")
    theta_bad = np.zeros(design.shape[1])
    for _ in range(60):
        theta_bad -= 40.0 * gradient(theta_bad)
    norm = np.linalg.norm(gradient(theta_bad))
    print(f"    step past the ceiling (60)   {norm:.3e}        diverging")
    print()
    print("    The loss curve looks flat in the first two and saturated in the")
    print("    third. One logged quantity separates all three, and it is not")
    print("    the loss.")


if __name__ == "__main__":
    main()
