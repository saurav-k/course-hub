"""Lesson 0089 - the Taylor model, the largest safe step, and conditioning.

Implements three named results.

1.  Taylor's theorem to first and second order, with the error measured rather
    than asserted: halving the distance should divide the first-order error by
    four and the second-order error by eight.

2.  The step that minimises the second-order model,

        eps* = g^T g / (g^T H g),   worst case  1 / lambda_max

    checked against a scan of the true loss along the descent ray.

3.  The condition number of the Hessian, before and after standardising the
    columns, and what it does to the largest tolerable step. This is the
    lesson's punchline: feature scaling is a curvature fix.

    python3 0089-taylor-and-the-quadratic-model.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

SENSORS = Path(__file__).resolve().parent.parent / "datasets" / "sensors.csv"
FAILURES = Path(__file__).resolve().parent.parent / "datasets" / "failures.csv"
SENSORS_URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/sensors.csv"
FAILURES_URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/failures.csv"

FEATURES = ["vibration_x", "vibration_y", "current_amp",
            "humidity_pct", "dust_index", "pressure_kpa"]
TARGET = "temp_c"


def read(local: Path, url: str) -> pd.DataFrame:
    return pd.read_csv(local) if local.exists() else pd.read_csv(url)


def build(standardise: bool) -> tuple[np.ndarray, np.ndarray]:
    frame = read(SENSORS, SENSORS_URL)
    x = frame[FEATURES].to_numpy(dtype=float)
    if standardise:
        x = (x - x.mean(axis=0)) / x.std(axis=0)
    y = frame[TARGET].to_numpy(dtype=float)
    return np.hstack([np.ones((len(frame), 1)), x]), y


def loss(theta: np.ndarray, x: np.ndarray, y: np.ndarray) -> float:
    r = y - x @ theta
    return float(r @ r / len(y))


def gradient(theta: np.ndarray, x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return -2.0 / len(y) * (x.T @ (y - x @ theta))


def hessian(x: np.ndarray, n: int) -> np.ndarray:
    return 2.0 / n * (x.T @ x)


def taylor1(theta: np.ndarray, step: np.ndarray, f0: float, g: np.ndarray) -> float:
    return f0 + g @ step


def taylor2(theta: np.ndarray, step: np.ndarray, f0: float, g: np.ndarray, h: np.ndarray) -> float:
    return f0 + g @ step + 0.5 * step @ h @ step


def main() -> None:
    x, y = build(standardise=False)
    n = len(y)
    # Start from the intercept-only model: predict every reading's temperature
    # as the overall average and nothing else. It is the honest zero-knowledge
    # guess, and it is defined whatever the column count happens to be.
    theta = np.zeros(x.shape[1])
    theta[0] = float(y.mean())
    f0 = loss(theta, x, y)
    g = gradient(theta, x, y)
    h = hessian(x, n)

    print(f"loaded sensors.csv: {n} rows\n")

    print("1a. a squared-error loss is exactly quadratic, so the second-order")
    print("    Taylor model is not an approximation of it - it IS it")
    direction = -g / np.linalg.norm(g)
    print(f"    {'distance':>10} {'1st order err':>16} {'2nd order err':>16}")
    for k in range(2, 7):
        d = 10.0**-k
        step = d * direction
        true = loss(theta + step, x, y)
        print(f"    {d:10.0e} {abs(taylor1(theta, step, f0, g) - true):16.3e} "
              f"{abs(taylor2(theta, step, f0, g, h) - true):16.3e}")
    print("    the second column falls like the distance squared. The third does not")
    print("    fall at all: it is already at the floating-point floor, because the")
    print("    third derivative of a quadratic is zero and there is no error to shrink.")

    print("\n1b. the error rates, on a loss that is not quadratic")
    print("    logistic regression on the failures table, two parameters")
    scores = read(FAILURES, FAILURES_URL)
    sx = np.column_stack([
        np.ones(len(scores)),
        np.log(scores["hours_since_service"].to_numpy(dtype=float)),
    ])
    sy = scores["failed"].to_numpy(dtype=float)

    def log_loss(t: np.ndarray) -> float:
        z = sx @ t
        return float(np.mean(np.maximum(z, 0) - z * sy + np.log1p(np.exp(-np.abs(z)))))

    def log_grad(t: np.ndarray) -> np.ndarray:
        z = sx @ t
        p = np.where(z >= 0, 1 / (1 + np.exp(-z)), np.exp(z) / (1 + np.exp(z)))
        return sx.T @ (p - sy) / len(sy)

    def log_hess(t: np.ndarray) -> np.ndarray:
        z = sx @ t
        p = np.where(z >= 0, 1 / (1 + np.exp(-z)), np.exp(z) / (1 + np.exp(z)))
        w = p * (1 - p)
        return (sx * w[:, None]).T @ sx / len(sy)

    t0 = np.array([0.3, 0.7])
    lf0, lg, lh = log_loss(t0), log_grad(t0), log_hess(t0)
    ldir = -lg / np.linalg.norm(lg)
    print(f"    {'distance':>10} {'1st order err':>16} {'ratio':>8} {'2nd order err':>16} {'ratio':>8}")
    prev1 = prev2 = None
    for k in range(0, 5):
        d = 10.0**-k
        step = d * ldir
        true = log_loss(t0 + step)
        e1 = abs(lf0 + lg @ step - true)
        e2 = abs(lf0 + lg @ step + 0.5 * step @ lh @ step - true)
        r1 = f"{prev1 / e1:8.1f}" if prev1 else f"{'':>8}"
        r2 = f"{prev2 / e2:8.1f}" if prev2 else f"{'':>8}"
        print(f"    {d:10.0e} {e1:16.3e} {r1} {e2:16.3e} {r2}")
        prev1, prev2 = e1, e2
    print("    now the rates show: 100x per decade for first order, 1000x for second,")
    print("    which is the distance squared and the distance cubed.")

    print("\n2. the step the quadratic model says is best")
    gg = float(g @ g)
    ghg = float(g @ h @ g)
    eps_star = gg / ghg
    lam = np.linalg.eigvalsh(h)
    print(f"   g^T g          = {gg:.6e}")
    print(f"   g^T H g        = {ghg:.6e}")
    print(f"   eps*           = {eps_star:.6e}")
    print(f"   1 / lambda_max = {1.0 / lam[-1]:.6e}")
    print(f"   they nearly agree because g is almost parallel to the top eigenvector:")
    top = np.linalg.eigh(h)[1][:, -1]
    cos = abs(float(g @ top / np.linalg.norm(g)))
    print(f"   |cos angle(g, v_max)| = {cos:.6f}")

    print(f"\n   scanning the true loss along -g")
    print(f"   {'eps':>12} {'true loss':>18} {'model':>18}")
    for mult in (0.25, 0.5, 1.0, 2.0, 3.0):
        eps = mult * eps_star
        step = -eps * g
        print(f"   {eps:12.3e} {loss(theta + step, x, y):18.6f} "
              f"{taylor2(theta, step, f0, g, h):18.6f}   ({mult:g} x eps*)")
    print(f"   the loss at eps = 0 is {f0:.6f}")
    print("   at 2 x eps* the model is back where it started, and past that it climbs")

    print("\n3. the same problem with standardised columns")
    xs, ys = build(standardise=True)
    hs = hessian(xs, len(ys))
    lam_s = np.linalg.eigvalsh(hs)
    print(f"   {'':>14} {'lambda_min':>16} {'lambda_max':>16} {'kappa':>16} {'1/lambda_max':>16}")
    print(f"   {'raw':>14} {lam[0]:16.6e} {lam[-1]:16.6e} {lam[-1] / lam[0]:16,.1f} {1 / lam[-1]:16.3e}")
    print(f"   {'standardised':>14} {lam_s[0]:16.6e} {lam_s[-1]:16.6e} "
          f"{lam_s[-1] / lam_s[0]:16,.1f} {1 / lam_s[-1]:16.3e}")
    print(f"   condition number falls by a factor of {(lam[-1] / lam[0]) / (lam_s[-1] / lam_s[0]):,.0f}")
    print(f"   the largest tolerable step rises by a factor of {(1 / lam_s[-1]) / (1 / lam[-1]):,.0f}")
    print("   nothing about the data changed. Only the units did.")


if __name__ == "__main__":
    main()
