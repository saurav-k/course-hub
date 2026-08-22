"""Shared loading helpers for the M06 Optimization programs.

Every program in this module is meant to be runnable on its own, so each one
imports only this file and nothing else of ours. Copy the two files together
into a notebook directory, or paste this file's two functions into your own
script - they are short on purpose.

Needs numpy and pandas only.
"""

from pathlib import Path

import numpy as np
import pandas as pd

# The dataset ships beside the course. From code/ that is ../datasets/.
# Replace with the published URL to run this in Colab without the repo.
DATA = Path(__file__).resolve().parent.parent / "datasets" / "m06-credit.csv"

FEATURES = [
    "income_inr",
    "age_years",
    "utilisation_ratio",
    "enquiries_6m",
    "tenure_months",
    "emi_to_income",
    "late_payments_12m",
    "card_count",
    "noise_1",
    "noise_2",
    "noise_3",
    "noise_4",
]


def load(standardise: bool = True, add_intercept: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """Return the design matrix and the binary target.

    standardise: centre each feature and divide by its standard deviation.
        M06 L04 is the lesson about why this matters, and it is the one
        place in the module you should pass False.
    add_intercept: prepend a column of ones.
    """
    frame = pd.read_csv(DATA)
    matrix = frame[FEATURES].to_numpy(dtype=float)
    if standardise:
        matrix = (matrix - matrix.mean(axis=0)) / matrix.std(axis=0)
    if add_intercept:
        matrix = np.column_stack([np.ones(len(matrix)), matrix])
    return matrix, frame["default"].to_numpy(dtype=float)


def load_regression(standardise: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """Return the design matrix and the continuous credit-limit target."""
    frame = pd.read_csv(DATA)
    matrix = frame[FEATURES].to_numpy(dtype=float)
    if standardise:
        matrix = (matrix - matrix.mean(axis=0)) / matrix.std(axis=0)
    target = frame["credit_limit_inr"].to_numpy(dtype=float)
    return matrix, target - target.mean()


def sigmoid(z: np.ndarray) -> np.ndarray:
    """Logistic function, written so it does not overflow on large |z|."""
    out = np.empty_like(z, dtype=float)
    positive = z >= 0
    out[positive] = 1.0 / (1.0 + np.exp(-z[positive]))
    exp_z = np.exp(z[~positive])
    out[~positive] = exp_z / (1.0 + exp_z)
    return out


def mean_logistic_loss(design: np.ndarray, target: np.ndarray,
                       theta: np.ndarray) -> float:
    """Mean logistic loss, written so it cannot overflow or take log(0).

    The obvious form, -mean(y*log(p) + (1-y)*log(1-p)), is exact arithmetic
    and a numerical trap: once |z| passes about 37 the sigmoid rounds to
    exactly 0 or 1, log(0) is -inf, and the objective becomes inf or nan.
    Worse, a nan then compares False against everything, so a test written
    on top of it reports success by silently comparing nothing.

    The identity below has no such point. For a logit z and label y,
        -y*log(p) - (1-y)*log(1-p)  =  log(1 + exp(z)) - y*z
    and numpy.logaddexp(0, z) computes log(1 + exp(z)) stably for any z.
    """
    logit = design @ theta
    return float(np.mean(np.logaddexp(0.0, logit) - target * logit))
