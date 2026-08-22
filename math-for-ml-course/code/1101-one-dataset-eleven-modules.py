"""M11 Capstone, part 1: the summaries this course already computed for sessions.csv.

Reproduces every number stated on lessons/1101-one-dataset-eleven-modules.html.
Needs numpy and pandas only. Runs unchanged in a codebase, in Jupyter and in Colab.

    python3 1101-one-dataset-eleven-modules.py

Each quantity is computed twice, once from the definition and once the library way,
and the two are asserted equal. The point is to see the arithmetic, not to call an API.
"""

import numpy as np
import pandas as pd

LOCAL = "../datasets/sessions.csv"
REMOTE = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/sessions.csv"
)


def load() -> pd.DataFrame:
    """Read the committed dataset from disk, falling back to the published copy."""
    try:
        return pd.read_csv(LOCAL)
    except (FileNotFoundError, OSError):
        return pd.read_csv(REMOTE)


def mean_from_definition(values: np.ndarray) -> float:
    """Sum every value and divide by the count, which is all a mean is."""
    total = 0.0
    for v in values:
        total += float(v)
    return total / len(values)


def median_from_definition(values: np.ndarray) -> float:
    """Sort, then take the middle value, or the average of the middle pair."""
    ordered = np.sort(values)
    n = len(ordered)
    middle = n // 2
    if n % 2 == 1:
        return float(ordered[middle])
    return (float(ordered[middle - 1]) + float(ordered[middle])) / 2.0


def correlation_from_definition(a: np.ndarray, b: np.ndarray) -> float:
    """Centre both columns, then divide their cross product by the two spreads."""
    da = a - mean_from_definition(a)
    db = b - mean_from_definition(b)
    return float((da * db).sum() / np.sqrt((da**2).sum() * (db**2).sum()))


def main() -> None:
    df = load()
    seconds = df["session_seconds"].to_numpy(float)
    spend = df["spend"].to_numpy(float)
    brightness = df["screen_brightness"].to_numpy(float)

    mean = mean_from_definition(seconds)
    median = median_from_definition(seconds)
    r_real = correlation_from_definition(seconds, spend)
    r_null = correlation_from_definition(brightness, spend)

    # the same four quantities, the library way
    assert np.isclose(mean, seconds.mean())
    assert np.isclose(median, np.median(seconds))
    assert np.isclose(r_real, np.corrcoef(seconds, spend)[0, 1])
    assert np.isclose(r_null, np.corrcoef(brightness, spend)[0, 1])

    print(f"rows                          {len(df):,}")
    print(f"mean session length           {mean:.1f} s")
    print(f"median session length         {median:.1f} s")
    print(f"mean / median                 {mean / median:.2f}")
    print(f"lower quartile                {np.percentile(seconds, 25):.1f} s")
    print(f"upper quartile                {np.percentile(seconds, 75):.1f} s")
    print(f"sessions past 600 s           {(seconds > 600).sum():,}")
    print()
    print(f"corr(session length, spend)   {r_real:.3f}   a real association")
    print(f"corr(brightness, spend)       {r_null:.3f}   a null one")
    print()
    print("Both correlations came out of identical arithmetic on identically shaped")
    print("columns. Nothing in the formula knew which column mattered.")


if __name__ == "__main__":
    main()
