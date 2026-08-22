"""M11 capstone, part 3: standard errors, t-statistics and the two intervals.

Every number on lessons/0202-what-a-coefficient-is-worth.html comes from this program:
the eight-row fit against the full fit, the null column through identical machinery,
and the gap between predicting an average and predicting one visitor.

Needs numpy and pandas only. Runs unchanged in a codebase, in Jupyter and in Colab.

    python3 0202-what-a-coefficient-is-worth.py
"""

import math
from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "sessions.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/sessions.csv"
)

# the eight rows worked by hand on the page, kept here so the comparison runs
HAND_SECONDS = np.array([36, 72, 76, 112, 114, 162, 166, 248], float)
HAND_SPEND = np.array([11, 19, 17, 17, 24, 26, 14, 22], float)


def two_sided_p(t: float, degrees_of_freedom: int) -> float:
    """The two-sided tail of the t-distribution, through its normal limit.

    Honest about its own boundary: at 19,998 degrees of freedom the t and the normal
    agree to far more digits than this page quotes. Below about 30 they do not, and a
    small-sample p-value wants a real t-distribution rather than this shortcut.
    """
    if degrees_of_freedom < 30:
        return float("nan")
    return math.erfc(abs(t) / math.sqrt(2))


def fit_with_inference(x: np.ndarray, y: np.ndarray) -> dict:
    """Least squares from the centred sums, plus everything module 9 attaches to it."""
    n = len(x)
    s_xx = float(((x - x.mean()) ** 2).sum())
    s_xy = float(((x - x.mean()) * (y - y.mean())).sum())
    slope = s_xy / s_xx
    intercept = float(y.mean() - slope * x.mean())

    residual = y - (intercept + slope * x)
    sse = float(residual @ residual)
    sigma_squared = sse / (n - 2)      # two parameters estimated, two degrees lost
    standard_error = math.sqrt(sigma_squared / s_xx)
    sst = float(((y - y.mean()) ** 2).sum())

    # the same slope the library way, from the design matrix
    design = np.column_stack([np.ones(n), x])
    library = np.linalg.solve(design.T @ design, design.T @ y)
    assert np.isclose(slope, library[1]), "centred sums and the solve must agree"
    assert np.isclose(intercept, library[0])

    return {
        "n": n, "slope": slope, "intercept": intercept, "s_xx": s_xx, "sse": sse,
        "sigma": math.sqrt(sigma_squared), "sigma_squared": sigma_squared,
        "se": standard_error, "t": slope / standard_error,
        "r_squared": 1 - sse / sst, "mean_x": float(x.mean()),
    }


def report(label: str, fit: dict, critical: float) -> None:
    lo = fit["slope"] - critical * fit["se"]
    hi = fit["slope"] + critical * fit["se"]
    verdict = " and straddles zero" if lo < 0 < hi else " and excludes zero"
    print(f"{label}")
    print(f"  n {fit['n']:,}   slope {fit['slope']:.6f}   sigma-hat {fit['sigma']:.3f}")
    print(f"  S_xx {fit['s_xx']:,.1f}   SE {fit['se']:.6f}   t {fit['t']:.3f}")
    print(f"  interval [{lo:.6f}, {hi:.6f}]{verdict}")


def main() -> None:
    frame = pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)
    x = frame["session_seconds"].to_numpy(float)
    y = frame["spend"].to_numpy(float)
    brightness = frame["screen_brightness"].to_numpy(float)

    hand = fit_with_inference(HAND_SECONDS, HAND_SPEND)
    full = fit_with_inference(x, y)
    null = fit_with_inference(brightness, y)

    # in a one-predictor fit R squared is the squared correlation, exactly
    assert np.isclose(full["r_squared"], np.corrcoef(x, y)[0, 1] ** 2)

    print("The same slope, two sample sizes")
    print("=" * 66)
    report("eight rows, critical value 2.45 on 6 degrees of freedom", hand, 2.45)
    report("twenty thousand rows, critical value 1.96", full, 1.96)
    print(f"\n  slopes differ by {abs(hand['slope'] - full['slope']):.6f}")
    print(f"  standard errors differ by a factor of {hand['se'] / full['se']:.1f}")
    print(f"  row counts differ by a factor of {full['n'] / hand['n']:.0f}, "
          f"whose square root is {math.sqrt(full['n'] / hand['n']):.1f}")

    print("\nThe same machinery, handed a column that carries nothing")
    print("=" * 66)
    report("screen brightness against spend", null, 1.96)
    print(f"  p {two_sided_p(null['t'], null['n'] - 2):.3f}"
          f"   against t {full['t']:.2f} for session length")

    print("\nPredicting an average against predicting one visitor")
    print("=" * 66)
    x0 = 300.0
    point = full["intercept"] + full["slope"] * x0
    leverage = 1 / full["n"] + (x0 - full["mean_x"]) ** 2 / full["s_xx"]
    se_mean = math.sqrt(full["sigma_squared"] * leverage)
    se_one = math.sqrt(full["sigma_squared"] * (1 + leverage))
    print(f"  at {x0:.0f} s the fitted spend is {point:.3f}")
    print(f"  mean:        [{point - 1.96 * se_mean:8.3f}, {point + 1.96 * se_mean:8.3f}]"
          f"   width {2 * 1.96 * se_mean:.3f}")
    print(f"  one visitor: [{point - 1.96 * se_one:8.3f}, {point + 1.96 * se_one:8.3f}]"
          f"   width {2 * 1.96 * se_one:.3f}")
    print(f"  a factor of {se_one / se_mean:.0f}")
    if point - 1.96 * se_one < 0:
        print("  the lower end is negative and spend cannot be: the normal error model")
        print("  is symmetric and unbounded, and here that assumption is false.")

    print("\nWhat the fit does not establish")
    print("=" * 66)
    print(f"  R-squared {full['r_squared']:.4f}")
    print(f"  one more minute is worth {full['slope'] * 60:.2f} "
          f"on a mean spend of {y.mean():.2f}")
    print(f"  {(y == 0).mean():.1%} of sessions spend nothing at all, so a straight line")
    print("  through this column is a summary of a shape it does not match.")


if __name__ == "__main__":
    main()
