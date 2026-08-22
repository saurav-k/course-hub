"""M06 L01 - Learning is an optimization problem.

The objective an L2-regularised logistic regression actually minimises,
evaluated at two candidate parameter vectors.

COMPUTES IT TWICE: once with an explicit Python loop over rows, which is what
the page teaches, and once as a vectorised NumPy expression, which is what a
codebase runs. They must agree to machine precision. If they ever disagree,
the loop is right and the vector form has a broadcasting bug.

    python3 0100-learning-is-an-optimization-problem.py

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


def objective_by_loop(design: np.ndarray, target: np.ndarray,
                      theta: np.ndarray, inverse_strength: float) -> float:
    """Mean logistic loss plus the L2 penalty, one row at a time."""
    total = 0.0
    for row, label in zip(design, target):
        logit = float(np.dot(theta, row))
        probability = float(sigmoid(np.array([logit]))[0])
        total += -(label * np.log(probability) + (1.0 - label) * np.log(1.0 - probability))
    mean_loss = total / len(target)
    # The intercept is conventionally left unpenalised, so theta[0] is skipped.
    penalty = float(np.dot(theta[1:], theta[1:])) / (2.0 * inverse_strength)
    return mean_loss + penalty


def objective_vectorised(design: np.ndarray, target: np.ndarray,
                         theta: np.ndarray, inverse_strength: float) -> float:
    """The same number, computed on the whole matrix at once."""
    mean_loss = mean_logistic_loss(design, target, theta)
    penalty = float(theta[1:] @ theta[1:]) / (2.0 * inverse_strength)
    return float(mean_loss + penalty)


def main() -> None:
    design, target = load()

    # Two candidates built to sit on opposite sides of the trade the penalty
    # makes. B is fitted: forty plain gradient steps, so it fits the data
    # better and its weights are correspondingly larger. A is B shrunk
    # towards zero, so it fits worse and costs almost no penalty.
    # Neither is the optimum. The point is that the objective's preference
    # between them depends on C, and the page works out why.
    theta_b = np.zeros(design.shape[1])
    for _ in range(40):
        residual = sigmoid(design @ theta_b) - target
        theta_b -= 0.5 * (design.T @ residual) / len(target)
    theta_a = 0.25 * theta_b

    print("M06 L01 - the objective, two candidates, two ways of computing it")
    print(f"rows: {len(target):,}   parameters: {design.shape[1]}")
    print()

    for name, theta in (("A", theta_a), ("B", theta_b)):
        for inverse_strength in (1.0, 0.01):
            loop = objective_by_loop(design, target, theta, inverse_strength)
            vector = objective_vectorised(design, target, theta, inverse_strength)
            mean_loss = mean_logistic_loss(design, target, theta)
            penalty = float(theta[1:] @ theta[1:]) / (2.0 * inverse_strength)
            print(f"  candidate {name}, C = {inverse_strength}")
            print(f"    mean logistic loss : {mean_loss:.8f}")
            print(f"    L2 penalty         : {penalty:.8f}")
            print(f"    objective (loop)   : {loop:.8f}")
            print(f"    objective (vector) : {vector:.8f}")
            print(f"    agree to           : {abs(loop - vector):.3e}")
    print()

    # The beat the page turns on: which candidate wins depends on C.
    print("which candidate does the objective prefer?")
    previous = None
    for inverse_strength in (100.0, 10.0, 1.0, 0.1, 0.01, 0.001):
        value_a = objective_vectorised(design, target, theta_a, inverse_strength)
        value_b = objective_vectorised(design, target, theta_b, inverse_strength)
        winner = "A" if value_a < value_b else "B"
        flip = "   <-- the ranking flips here" if previous and previous != winner else ""
        print(f"  C = {inverse_strength:<8} A = {value_a:>10.6f}   B = {value_b:>10.6f}"
              f"   -> {winner}{flip}")
        previous = winner
    print()
    print("B fits better, so the likelihood term alone always prefers B.")
    print("A costs less penalty. C decides which of the two the objective believes,")
    print("and somewhere between those rows the answer changes. That is the whole")
    print("reason the second term is in the objective at all.")


if __name__ == "__main__":
    main()
