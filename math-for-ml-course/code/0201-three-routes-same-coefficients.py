"""M11 Capstone, part 2: the same fit by normal equations and by gradient descent.

Reproduces every number on lessons/0201-three-routes-same-coefficients.html, including
the divergence of descent on raw columns and the condition numbers that predict it.
Needs numpy and pandas only.

    python3 0201-three-routes-same-coefficients.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "sessions.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/sessions.csv"
)


def load() -> pd.DataFrame:
    """The committed dataset, with a URL fallback so pasting into Colab works."""
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def fit_by_normal_equations(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Solve X'X b = X'y directly. This is module 3's route."""
    design = np.column_stack([np.ones(len(x)), x])
    intercept, slope = np.linalg.solve(design.T @ design, design.T @ y)
    return float(intercept), float(slope)


def fit_by_two_sums(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """The same answer from the centred sums, which is what you do by hand."""
    s_xy = ((x - x.mean()) * (y - y.mean())).sum()
    s_xx = ((x - x.mean()) ** 2).sum()
    slope = float(s_xy / s_xx)
    return float(y.mean() - slope * x.mean()), slope


def fit_by_descent(
    x: np.ndarray, y: np.ndarray, step: float = 0.1, iterations: int = 60
) -> tuple[float, float, list[tuple[int, float]]]:
    """Walk downhill on standardised columns. This is module 6's route.

    Standardising is not cosmetic here: see condition_numbers() below.
    """
    x_mean, x_sd = x.mean(), x.std()
    y_mean, y_sd = y.mean(), y.std()
    design = np.column_stack([np.ones(len(x)), (x - x_mean) / x_sd])
    target = (y - y_mean) / y_sd

    weights = np.zeros(2)
    path = [(0, 0.0)]
    for step_number in range(1, iterations + 1):
        gradient = (2.0 / len(x)) * (design.T @ (design @ weights - target))
        weights = weights - step * gradient
        path.append((step_number, float(weights[1])))

    slope = float(weights[1]) * y_sd / x_sd
    return float(y_mean - slope * x_mean), slope, path


def condition_numbers(x: np.ndarray) -> None:
    """Why the raw columns need a step size ten thousand times smaller."""
    for label, column in [("raw", x), ("standardised", (x - x.mean()) / x.std())]:
        design = np.column_stack([np.ones(len(x)), column])
        hessian = (2.0 / len(x)) * (design.T @ design)
        low, high = np.linalg.eigvalsh(hessian)
        print(
            f"  {label:13s} eigenvalues {low:.4e} and {high:.4e}, "
            f"condition {high / low:.4e}, largest safe step {2 / high:.4e}"
        )


def show_divergence(x: np.ndarray, y: np.ndarray, step: float = 0.1) -> None:
    """Run five steps on the RAW columns at the step size that worked standardised.

    Nothing raises. The loss simply stops meaning anything, which is why this is
    usually misdiagnosed as bad data rather than as a step size far too large.
    """
    design = np.column_stack([np.ones(len(x)), x])
    weights = np.zeros(2)
    for step_number in range(1, 6):
        gradient = (2.0 / len(x)) * (design.T @ (design @ weights - y))
        weights = weights - step * gradient
        loss = float(np.mean((design @ weights - y) ** 2))
        print(f"  iteration {step_number}   mean squared error {loss:.3e}")


def main() -> None:
    df = load()
    x = df["session_seconds"].to_numpy(float)
    y = df["spend"].to_numpy(float)

    b0_solve, b1_solve = fit_by_normal_equations(x, y)
    b0_sums, b1_sums = fit_by_two_sums(x, y)
    b0_desc, b1_desc, path = fit_by_descent(x, y)

    # the matrix solve and the hand method are the same equation
    assert np.isclose(b1_solve, b1_sums), "the two closed forms must agree exactly"
    assert np.isclose(b0_solve, b0_sums)
    # descent lands on it too, to the precision 60 iterations buys
    assert abs(b1_desc - b1_solve) < 1e-6, "descent must reach the same minimiser"
    # 60 iterations leaves about 9e-8; 80 closes it to 1e-9. Neither is a disagreement.

    print("Route A, normal equations")
    print(f"  intercept {b0_solve:.6f}   slope {b1_solve:.6f}")
    print("Route B, gradient descent on standardised columns")
    print(f"  intercept {b0_desc:.6f}   slope {b1_desc:.6f}")
    print(f"  slopes differ by {abs(b1_desc - b1_solve):.2e}")
    print()

    print("the descent path, standardised slope against iteration")
    for step_number, value in path:
        if step_number in (0, 1, 2, 3, 5, 10, 20, 40, 60):
            print(f"  iteration {step_number:3d}   {value:.6f}")
    print()

    print("why standardising was not cosmetic")
    condition_numbers(x)
    print()

    print("the same step size on the raw columns, five iterations")
    show_divergence(x, y)
    print()

    # run it longer and the last digits close too
    _, b1_long, _ = fit_by_descent(x, y, iterations=80)
    print(f"at 80 iterations descent gives {b1_long:.8f} "
          f"against {b1_solve:.8f}, a gap of {abs(b1_long - b1_solve):.1e}")
    print()

    # the residual is perpendicular to both columns: module 3's projection picture
    design = np.column_stack([np.ones(len(x)), x])
    residual = y - design @ np.array([b0_solve, b1_solve])
    print("the projection check, residual against each column")
    print(f"  residual . ones  {residual @ design[:, 0]:.3e}")
    print(f"  residual . x     {residual @ design[:, 1]:.3e}")
    print()
    print(f"one more minute is worth {b1_solve * 60:.4f} on average.")
    print("Part 3 asks how much that number is worth.")


if __name__ == "__main__":
    main()
