"""Lesson 0505 - the gradient is steepest, and only in one sense.

Implements the named result:

    among all unit vectors u,  u . grad f  is smallest at  u = -grad f / ||grad f||
    and its value there is  -||grad f||

which is Cauchy-Schwarz, and the program checks it by brute force: fifty
thousand random unit directions, none of which beats the negative gradient.

Then the part the result is usually quoted without. "Unit" was defined by the
Euclidean norm. Measure length with a different norm and a different direction
wins. The program computes the steepest direction under the norm defined by the
Hessian and reports the angle between the two, which is not small.

    python3 0505-the-gradient-points-uphill.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "sensors.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/sensors.csv"

# Predicting one sensor from the others is what a real monitoring system does,
# and it gives this module a design matrix whose columns are on wildly
# different scales: pressure runs in the hundreds, dust index around one. That
# disparity is the whole subject of lessons 0509 and 0510, so it is load
# bearing rather than incidental.
FEATURES = ["vibration_x", "vibration_y", "current_amp",
            "humidity_pct", "dust_index", "pressure_kpa"]
TARGET = "temp_c"


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)
SEED = 20260822


def design_matrix(frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    x = frame[FEATURES].to_numpy(dtype=float)
    return np.hstack([np.ones((len(frame), 1)), x]), frame[TARGET].to_numpy(dtype=float)


def gradient(theta: np.ndarray, x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return -2.0 / len(y) * (x.T @ (y - x @ theta))


def hessian(x: np.ndarray, n: int) -> np.ndarray:
    """For a squared-error loss the Hessian is constant: 2/n * X^T X."""
    return 2.0 / n * (x.T @ x)


def directional_derivative(grad: np.ndarray, u: np.ndarray) -> float:
    """The rate of change of f along the unit vector u. This is the chain rule
    applied to t -> f(x + t u) at t = 0, which collapses to a dot product."""
    return float(u @ grad)


def random_unit_vectors(count: int, dim: int, seed: int) -> np.ndarray:
    """Uniform on the sphere: normalise standard normals, which is the only
    way to do it that does not bunch the samples at the corners."""
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(count, dim))
    return raw / np.linalg.norm(raw, axis=1, keepdims=True)


def main() -> None:
    frame = load()
    x, y = design_matrix(frame)
    # Start from the intercept-only model: predict every reading's temperature
    # as the overall average and nothing else. It is the honest zero-knowledge
    # guess, and it is defined whatever the column count happens to be.
    theta = np.zeros(x.shape[1])
    theta[0] = float(y.mean())

    grad = gradient(theta, x, y)
    norm = float(np.linalg.norm(grad))
    steepest = -grad / norm
    print(f"loaded sensors.csv: {x.shape[0]} rows, {x.shape[1]} parameters")
    print(f"||grad f|| = {norm:,.4f}\n")

    print("named directions, and how fast the loss falls along each")
    def axis(name: str) -> np.ndarray:
        """The best downhill step that moves one named parameter and nothing else.

        Its sign is the sign that descends, which is the opposite of that
        parameter's gradient component. Picking the sign by hand instead would
        make the comparison meaningless: half the axes would point uphill and
        the table would be measuring the choice rather than the direction.
        """
        v = np.zeros(len(grad))
        j = (["intercept"] + FEATURES).index(name)
        v[j] = -np.sign(grad[j])
        return v

    named = {
        "-grad / ||grad||": steepest,
        "pressure only": axis("pressure_kpa"),
        "vibration_x only": axis("vibration_x"),
        "humidity only": axis("humidity_pct"),
        # Equal magnitude on every dial, each in its own descending sign.
        # This is not an arbitrary comparison: it is the normalised steepest
        # descent direction under the L-infinity norm, so the row quietly makes
        # the same point as the ellipse figure.
        "equal on every dial": -np.sign(grad) / np.sqrt(len(grad)),
    }
    for label, u in named.items():
        u = u / np.linalg.norm(u)
        dd = directional_derivative(grad, u)
        print(f"  {label:>20}  u.grad = {dd:14,.4f}   {100 * dd / -norm:7.2f}% of the best")

    print("\nbrute force: 50,000 random unit directions")
    sample = random_unit_vectors(50_000, len(grad), SEED)
    values = sample @ grad
    print(f"  most negative found : {values.min():,.4f}")
    print(f"  the bound says      : {-norm:,.4f}")
    print(f"  none beat the bound : {bool(values.min() >= -norm - 1e-9)}")
    print(f"  best random direction reaches {100 * values.min() / -norm:.2f}% of the best")

    print("\nsteepest under a different norm")
    h = hessian(x, len(y))
    # Steepest descent in the norm ||z||_P = sqrt(z^T P z) is -P^-1 grad.
    p_direction = -np.linalg.solve(h, grad)
    p_unit = p_direction / np.linalg.norm(p_direction)
    cos = float(np.clip(p_unit @ steepest, -1.0, 1.0))
    print(f"  angle to the Euclidean steepest direction: {np.degrees(np.arccos(cos)):.1f} degrees")
    print("  same point, same function, different answer, because 'unit' changed")


if __name__ == "__main__":
    main()
