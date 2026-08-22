"""M06 L04 - The learning rate is bounded by curvature.

COMPUTES IT TWICE: the largest learning rate that converges, once
analytically as 2/lambda_max from the Hessian's eigenvalues, and once
empirically by running gradient descent at a ladder of step sizes and
finding the largest that survives.

The empirical route is the one you actually have on a real model, where
forming a Hessian is out of the question.

AND THE TWO DO NOT ALWAYS AGREE, WHICH IS THE POINT OF PART TWO.
On least squares the Hessian is constant, 2/L is exact, and the two routes
land on the same number. On logistic regression the Hessian is not constant:
its weights are p*(1-p), which shrink towards zero as the model grows
confident. So curvature FALLS as the iterate moves, the bound computed at
the start is conservative, and the empirical answer is larger.

A threshold derived on a quadratic is exact on a quadratic and a guide
everywhere else. Knowing which of those you are holding is the lesson.

    python3 0055-the-learning-rate-is-bounded-by-curvature.py

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


LADDER = (0.25, 0.5, 0.9, 0.99, 1.01, 1.1, 1.5, 2.0, 4.0)


def least_squares_hessian(design: np.ndarray) -> np.ndarray:
    """Constant everywhere: the objective is exactly quadratic."""
    return design.T @ design / len(design)


def logistic_hessian(design: np.ndarray, theta: np.ndarray) -> np.ndarray:
    """Depends on theta. The weights p*(1-p) are at most 1/4 and shrink."""
    probability = sigmoid(design @ theta)
    weights = probability * (1.0 - probability)
    return (design * weights[:, None]).T @ design / len(design)


def run(design, target, gradient_of, loss_of, learning_rate, steps=400):
    """Return the final loss, or inf if it blew up."""
    theta = np.zeros(design.shape[1])
    for _ in range(steps):
        theta = theta - learning_rate * gradient_of(design, target, theta)
        if not np.all(np.isfinite(theta)) or np.max(np.abs(theta)) > 1e12:
            return np.inf
    value = loss_of(design, target, theta)
    return value if np.isfinite(value) else np.inf


def ladder_report(design, target, gradient_of, loss_of, largest_eigenvalue):
    start = loss_of(design, target, np.zeros(design.shape[1]))
    ceiling = 2.0 / largest_eigenvalue
    best = None
    for factor in LADDER:
        rate = ceiling * factor
        final = run(design, target, gradient_of, loss_of, rate)
        ok = np.isfinite(final) and final < start
        if ok:
            best = rate
        shown = f"{final:.6f}" if np.isfinite(final) else "diverged"
        print(f"      eta = {rate:.4e}  ({factor:>4.2f} x 2/L)"
              f"   final loss {shown:>12}   {'ok' if ok else 'FAILS'}")
    return ceiling, best


def ls_gradient(design, target, theta):
    return design.T @ (design @ theta - target) / len(target)


def ls_loss(design, target, theta):
    residual = design @ theta - target
    return float(0.5 * np.mean(residual ** 2))


def lr_gradient(design, target, theta):
    return design.T @ (sigmoid(design @ theta) - target) / len(target)


def main() -> None:
    print("M06 L04 - the step-size ceiling, analytically and empirically")
    print()

    print("PART 1. Least squares: the Hessian is constant, so 2/L is exact.")
    print("    (The target is a rupee credit limit, so the loss is in rupees")
    print("     squared and the raw numbers are large. Only the ratios matter.)")
    design, target = load_regression(standardise=True)
    design = np.column_stack([np.ones(len(design)), design])
    eigenvalues = np.linalg.eigvalsh(least_squares_hessian(design))
    print(f"    Hessian eigenvalues : {eigenvalues[0]:.4e} .. {eigenvalues[-1]:.4e}")
    print(f"    condition number    : {eigenvalues[-1] / eigenvalues[0]:.4e}")
    ceiling, best = ladder_report(design, target, ls_gradient, ls_loss, eigenvalues[-1])
    print(f"    analytic 2/L        : {ceiling:.4e}")
    print(f"    largest empirical   : {best:.4e}")
    print(f"    ratio               : {best / ceiling:.3f}   <- the two routes agree")
    print()

    print("PART 2. Logistic regression: the Hessian shrinks as confidence grows.")
    design, target = load(standardise=True)
    theta_zero = np.zeros(design.shape[1])
    eigenvalues = np.linalg.eigvalsh(logistic_hessian(design, theta_zero))
    print(f"    Hessian eigenvalues at theta = 0 : {eigenvalues[0]:.4e} .. {eigenvalues[-1]:.4e}")
    ceiling, best = ladder_report(design, target, lr_gradient, mean_logistic_loss,
                                  eigenvalues[-1])
    print(f"    analytic 2/L at the start : {ceiling:.4e}")
    print(f"    largest empirical         : {best:.4e}")
    print(f"    ratio                     : {best / ceiling:.3f}   <- conservative, not wrong")
    print()
    # Show WHY: measure the curvature at the answer.
    theta = np.zeros(design.shape[1])
    for _ in range(2000):
        theta -= 1.0 * lr_gradient(design, target, theta)
    at_optimum = np.linalg.eigvalsh(logistic_hessian(design, theta))[-1]
    print(f"    largest eigenvalue at theta = 0        : {eigenvalues[-1]:.4e}")
    print(f"    largest eigenvalue at the optimum      : {at_optimum:.4e}")
    print(f"    curvature fell by a factor of          : {eigenvalues[-1] / at_optimum:.3f}")
    print("    The bound moved while we were walking towards it. That is why")
    print("    the start-of-run estimate is safe rather than tight.")
    print()

    print("PART 3. What standardising the features bought.")
    raw, target = load(standardise=False)
    std, _ = load(standardise=True)
    raw_ev = np.linalg.eigvalsh(logistic_hessian(raw, np.zeros(raw.shape[1])))
    std_ev = np.linalg.eigvalsh(logistic_hessian(std, np.zeros(std.shape[1])))
    raw_kappa, std_kappa = raw_ev[-1] / raw_ev[0], std_ev[-1] / std_ev[0]
    print(f"    condition number : {raw_kappa:.4e}  ->  {std_kappa:.4e}"
          f"   ({raw_kappa / std_kappa:.3e} x better)")
    print(f"    2/L at the start : {2 / raw_ev[-1]:.4e}  ->  {2 / std_ev[-1]:.4e}"
          f"   ({(2 / std_ev[-1]) / (2 / raw_ev[-1]):.3e} x larger)")
    print()

    print("PART 4. Boyd's exact quadratic, f(x) = 0.5*(x1^2 + gamma*x2^2).")
    print("    contraction per step under exact line search is ((g-1)/(g+1))^2")
    for gamma in (1.0, 3.0, 10.0, 100.0):
        ratio = ((gamma - 1.0) / (gamma + 1.0)) ** 2
        steps = "1 (exact)" if ratio == 0 else f"{np.log(1e-6) / np.log(ratio):.1f}"
        print(f"      gamma = {gamma:>6}   kappa = {max(gamma, 1 / gamma):>6.1f}"
              f"   contraction = {ratio:.4f}   steps to 1e-6: {steps}")


if __name__ == "__main__":
    main()
