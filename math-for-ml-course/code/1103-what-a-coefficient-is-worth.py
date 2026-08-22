"""M11 Capstone, part 3: standard errors, t-statistics and the two intervals.

Reproduces every number on lessons/1103-what-a-coefficient-is-worth.html: the eight-row
fit against the full fit, the null column through identical machinery, and the gap
between predicting an average and predicting one visitor.
Needs numpy and pandas only.

    python3 1103-what-a-coefficient-is-worth.py
"""

import math

import numpy as np
import pandas as pd

LOCAL = "../datasets/sessions.csv"
REMOTE = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/sessions.csv"
)

# the eight rows worked by hand on lessons/1102, kept here so the comparison runs
HAND_SECONDS = np.array([28, 46, 68, 85, 109, 204, 247, 332], float)
HAND_SPEND = np.array([57, 26, 33, 24, 98, 30, 66, 60], float)


def load() -> pd.DataFrame:
    try:
        return pd.read_csv(LOCAL)
    except (FileNotFoundError, OSError):
        return pd.read_csv(REMOTE)


def two_sided_p(t: float, degrees_of_freedom: int) -> float:
    """The two-sided tail of the t-distribution, via its normal limit.

    Honest about its own boundary: at the degrees of freedom this page uses the t and
    the normal agree to far more digits than are quoted, and below about 30 they do not.
    A small-sample p-value wants a real t-distribution rather than this.
    """
    if degrees_of_freedom < 30:
        return float("nan")
    return math.erfc(abs(t) / math.sqrt(2))


def fit_with_inference(x: np.ndarray, y: np.ndarray) -> dict:
    """Least squares plus everything module 9 attaches to it."""
    n = len(x)
    s_xx = float(((x - x.mean()) ** 2).sum())
    s_xy = float(((x - x.mean()) * (y - y.mean())).sum())
    slope = s_xy / s_xx
    intercept = float(y.mean() - slope * x.mean())

    residual = y - (intercept + slope * x)
    sse = float(residual @ residual)
    sigma_squared = sse / (n - 2)          # two parameters estimated, two degrees lost
    standard_error = math.sqrt(sigma_squared / s_xx)

    sst = float(((y - y.mean()) ** 2).sum())
    return {
        "n": n,
        "slope": slope,
        "intercept": intercept,
        "s_xx": s_xx,
        "sse": sse,
        "sigma": math.sqrt(sigma_squared),
        "sigma_squared": sigma_squared,
        "se": standard_error,
        "t": slope / standard_error,
        "r_squared": 1 - sse / sst,
        "mean_x": float(x.mean()),
    }


def report(label: str, fit: dict, critical: float) -> None:
    lo = fit["slope"] - critical * fit["se"]
    hi = fit["slope"] + critical * fit["se"]
    straddles = " and straddles zero" if lo < 0 < hi else ""
    print(f"{label}")
    print(f"  n {fit['n']:,}   slope {fit['slope']:.6f}   sigma-hat {fit['sigma']:.3f}")
    print(f"  S_xx {fit['s_xx']:,.1f}   SE {fit['se']:.6f}   t {fit['t']:.3f}")
    print(f"  interval [{lo:.6f}, {hi:.6f}]{straddles}")


def main() -> None:
    df = load()
    x = df["session_seconds"].to_numpy(float)
    y = df["spend"].to_numpy(float)
    brightness = df["screen_brightness"].to_numpy(float)

    hand = fit_with_inference(HAND_SECONDS, HAND_SPEND)
    full = fit_with_inference(x, y)
    null = fit_with_inference(brightness, y)

    # r squared and the squared correlation are the same thing in a one-predictor fit
    assert np.isclose(full["r_squared"], np.corrcoef(x, y)[0, 1] ** 2)

    print("The same slope, two sample sizes")
    print("=" * 64)
    report("eight rows, critical value 2.45 on 6 degrees of freedom", hand, 2.45)
    report("twenty thousand rows, critical value 1.96", full, 1.96)
    print(f"\n  slopes differ by {abs(hand['slope'] - full['slope']):.6f}")
    print(f"  standard errors differ by a factor of {hand['se'] / full['se']:.1f}")
    print(f"  row count differs by a factor of {full['n'] / hand['n']:.0f}, "
          f"whose square root is {math.sqrt(full['n'] / hand['n']):.1f}")
    print("  the rest of the gain is spread in the predictor, not count")

    print("\nThe same machinery, handed a column that carries nothing")
    print("=" * 64)
    report("screen brightness against spend", null, 1.96)
    print(f"  p {two_sided_p(null['t'], null['n'] - 2):.3f}")
    print(f"  for comparison, session length gives t {full['t']:.2f}")

    print("\nPredicting an average against predicting one visitor")
    print("=" * 64)
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
        print("  note: the lower end is negative and spend cannot be. The normal error")
        print("  model is symmetric and unbounded, and here that assumption is false.")

    print(f"\n  R-squared {full['r_squared']:.4f}: under a quarter of the variation.")
    print(f"  One more minute is worth {full['slope'] * 60:.2f} on a mean spend "
          f"of {y.mean():.2f}. Real, and small.")


if __name__ == "__main__":
    main()
