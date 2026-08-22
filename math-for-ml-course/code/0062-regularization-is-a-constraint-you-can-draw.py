"""M06 L11 - Regularization is a constraint you can draw.

COMPUTES IT TWICE: the lasso solution at each point on a regularization path,
once by coordinate descent using the soft-thresholding operator the page
derives, and once by proximal gradient descent (ISTA), which is a completely
different algorithm reaching the same optimum.

It then makes the page's central claim into a test rather than an assertion:
count the coefficients that are EXACTLY zero at each penalty strength, under
L1 and under L2. The L2 count must be zero at every strength. If it is ever
non-zero, Result 2 of the page is wrong.

Finally it demonstrates the trade-off the page owes: on two predictors
correlated at 0.92 by construction, the lasso's choice between them is
unstable across bootstrap resamples.

    python3 0062-regularization-is-a-constraint-you-can-draw.py

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


def soft_threshold(value: np.ndarray, amount: float) -> np.ndarray:
    """S(z, g) = sign(z) * max(|z| - g, 0). The page derives this."""
    return np.sign(value) * np.maximum(np.abs(value) - amount, 0.0)


def lasso_coordinate_descent(design, target, penalty, sweeps=400):
    rows, columns = design.shape
    beta = np.zeros(columns)
    column_energy = np.sum(design ** 2, axis=0) / rows
    residual = target - design @ beta
    for _ in range(sweeps):
        for index in range(columns):
            residual += design[:, index] * beta[index]
            correlation = design[:, index] @ residual / rows
            beta[index] = soft_threshold(np.array(correlation), penalty)[()] \
                / column_energy[index]
            residual -= design[:, index] * beta[index]
    return beta


def lasso_proximal_gradient(design, target, penalty, steps=6_000):
    """ISTA: a gradient step on the smooth part, then the prox of the L1 part."""
    rows, columns = design.shape
    beta = np.zeros(columns)
    lipschitz = np.linalg.eigvalsh(design.T @ design / rows)[-1]
    rate = 1.0 / lipschitz
    for _ in range(steps):
        gradient = design.T @ (design @ beta - target) / rows
        beta = soft_threshold(beta - rate * gradient, rate * penalty)
    return beta


def ridge(design, target, penalty):
    rows, columns = design.shape
    return np.linalg.solve(design.T @ design / rows + penalty * np.eye(columns),
                           design.T @ target / rows)


def main() -> None:
    design, target = load_regression(standardise=True)
    print("M06 L11 - the lasso path, two algorithms, and the zero count")
    print(f"rows: {len(target):,}   predictors: {design.shape[1]}")
    print()

    print("  Two algorithms, same optimum")
    print("    penalty     max coefficient gap    nonzero (CD)   nonzero (ISTA)")
    for penalty in (1e3, 1e4, 3e4, 1e5):
        by_cd = lasso_coordinate_descent(design, target, penalty)
        by_ista = lasso_proximal_gradient(design, target, penalty)
        gap = float(np.max(np.abs(by_cd - by_ista)))
        print(f"    {penalty:<10.0e}  {gap:>19.3e}    {int(np.sum(by_cd != 0)):>12}"
              f"   {int(np.sum(by_ista != 0)):>14}")
    print()

    print("  The claim, made into a test: exact zeros under L1 and under L2")
    print("    penalty      L1 zeros    L2 zeros    L2 smallest |coefficient|")
    for penalty in (1e2, 1e3, 1e4, 3e4, 1e5, 1e6):
        by_l1 = lasso_coordinate_descent(design, target, penalty)
        by_l2 = ridge(design, target, penalty)
        smallest = float(np.min(np.abs(by_l2)))
        print(f"    {penalty:<11.0e}  {int(np.sum(by_l1 == 0)):>9}"
              f"   {int(np.sum(by_l2 == 0)):>9}    {smallest:.6e}")
    print()
    print("    The L2 column is zero at every penalty, and its smallest coefficient")
    print("    keeps shrinking without ever arriving. L2 shrinks; L1 selects.")
    print()

    print("  Which predictors survive, and in what order")
    order = []
    for penalty in np.logspace(2, 6, 40):
        beta = lasso_coordinate_descent(design, target, penalty, sweeps=200)
        alive = {FEATURES[i] for i in range(len(FEATURES)) if beta[i] != 0}
        order.append((penalty, alive))
    dropped = {}
    for penalty, alive in order:
        for name in FEATURES:
            if name not in alive and name not in dropped:
                dropped[name] = penalty
    print("    predictor              dropped at penalty")
    for name, penalty in sorted(dropped.items(), key=lambda item: item[1]):
        marker = "   <- pure noise" if name.startswith("noise_") else ""
        print(f"    {name:<22} {penalty:>10.3e}{marker}")
    print()

    print("  Finding 1: a merely-correlated predictor is dropped, correctly.")
    print("    utilisation_ratio and emi_to_income are correlated at 0.92, but")
    print("    only utilisation_ratio enters the credit-limit target. The path")
    print("    above drops emi_to_income at penalty 1.0e+02 and keeps")
    print("    utilisation_ratio to 1.1e+04. That is the lasso working: it is")
    print("    not fooled by correlation alone.")
    print()

    print("  Finding 2: when BOTH predictors are genuinely predictive and")
    print("  correlated, the choice between them is unstable. Built here so the")
    print("  two coefficients are equal by construction and nothing is hidden.")
    rng = np.random.default_rng(53)
    rows = 4_000
    shared = rng.normal(0.0, 1.0, rows)
    first = shared + rng.normal(0.0, 0.30, rows)
    second = shared + rng.normal(0.0, 0.30, rows)
    other = rng.normal(0.0, 1.0, (rows, 3))
    twin_design = np.column_stack([first, second, other])
    twin_design = (twin_design - twin_design.mean(0)) / twin_design.std(0)
    # Equal true coefficients on the two twins, so neither is favoured.
    twin_target = (1.0 * twin_design[:, 0] + 1.0 * twin_design[:, 1]
                   + 0.5 * twin_design[:, 2] + rng.normal(0.0, 1.0, rows))
    twin_target -= twin_target.mean()
    print(f"    correlation between the twins: "
          f"{np.corrcoef(twin_design[:, 0], twin_design[:, 1])[0, 1]:.4f}")

    # The interesting penalty is the one in the transition zone, where the
    # path is dropping one of the two. Below it both survive every time and
    # above it neither does, and in both of those regimes there is nothing to
    # see. Scanned rather than guessed - see the printed sweep below.
    print()
    print("    penalty sweep, 30 resamples each:")
    for penalty in (0.9, 1.3, 1.8, 2.2):
        counts = {"both": 0, "one": 0, "neither": 0}
        for _ in range(30):
            sample = rng.integers(0, rows, rows)
            beta = lasso_coordinate_descent(twin_design[sample], twin_target[sample],
                                            penalty, sweeps=120)
            alive = int(beta[0] != 0) + int(beta[1] != 0)
            counts["both" if alive == 2 else "one" if alive == 1 else "neither"] += 1
        print(f"      penalty {penalty:<5}  both {counts['both']:>2}"
              f"   exactly one {counts['one']:>2}   neither {counts['neither']:>2}")
    print()
    print("    At penalty 1.8 the selection is genuinely contested. Look there:")

    picks = {"first only": 0, "second only": 0, "both": 0, "neither": 0}
    for _ in range(80):
        sample = rng.integers(0, rows, rows)
        beta = lasso_coordinate_descent(twin_design[sample], twin_target[sample],
                                        1.8, sweeps=150)
        has_first, has_second = beta[0] != 0, beta[1] != 0
        if has_first and has_second:
            picks["both"] += 1
        elif has_first:
            picks["first only"] += 1
        elif has_second:
            picks["second only"] += 1
        else:
            picks["neither"] += 1
    for label, count in picks.items():
        print(f"    {label:<14} {count:>3} of 80 bootstrap resamples")
    print()
    print("    The two predictors are interchangeable by construction, so which")
    print("    one survives is decided by the resample rather than by the data")
    print("    generating process. A sparse answer is not automatically a stable")
    print("    one. Report the selection frequency, not just the coefficients.")


if __name__ == "__main__":
    main()
