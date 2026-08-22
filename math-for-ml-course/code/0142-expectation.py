"""Expectation, and the linearity that survives dependence.

Lesson: Expectation, and the properties that hold even under dependence.

    python3 0803-expectation.py

What it checks twice:

  1. E[X] as a weighted sum over the distinct values, against the plain mean of
     the raw column. The first is the definition, the second is what a library
     gives you, and they are the same number.
  2. Linearity E[aX + bY] = aE[X] + bE[Y] on two columns that are strongly
     DEPENDENT (r = 0.62). Route one builds the combined column and averages it.
     Route two never forms the combination and adds the two expectations. They
     agree, which is the whole point: linearity did not ask about dependence.
  3. E[XY] = E[X]E[Y] under independence, and its failure under dependence. The
     same identity is tried on an independent pair and a dependent pair, so the
     reader sees which one breaks.
  4. The bootstrap out-of-bag fraction, (1 - 1/n)^n -> 1/e, derived by linearity
     over n dependent indicators and then measured by simulation.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "inference_runs.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/inference_runs.csv"
)


def load() -> pd.DataFrame:
    """Read the committed dataset, falling back to the published URL.

    The path is resolved from this file rather than the working directory, so the
    program runs from anywhere. The URL fallback is what lets it be pasted into
    Colab or a notebook with no checkout at all.
    """
    return pd.read_csv(DATA) if DATA.exists() else pd.read_csv(URL)


def expectation_from_pmf(column: pd.Series) -> float:
    """E[X] = sum over distinct values of value times its probability.

    This is the definition applied literally: build the PMF, then take the
    weighted sum. It is slower than .mean() and it is the thing .mean() means.
    """
    pmf = column.value_counts(normalize=True)
    return float((pmf.index.to_numpy() * pmf.to_numpy()).sum())


def main() -> None:
    frame = load()
    print(f"rows {len(frame):,}\n")

    print("1. Expectation two ways, on queue_depth")
    by_pmf = expectation_from_pmf(frame["queue_depth"])
    by_mean = float(frame["queue_depth"].mean())
    print(f"   weighted sum over the PMF   {by_pmf:.10f}")
    print(f"   plain mean of the column    {by_mean:.10f}")
    assert np.isclose(by_pmf, by_mean), "the definition and the mean disagree"
    print("   the definition and the shortcut are the same number\n")

    print("2. Linearity, on a DEPENDENT pair")
    x = frame["prompt_tokens"].astype(float)
    y = frame["output_tokens"].astype(float)
    r = float(x.corr(y))
    a, b = 3.0, -2.0
    combined = float((a * x + b * y).mean())
    separate = a * float(x.mean()) + b * float(y.mean())
    print(f"   correlation between the two columns   r = {r:.4f}  (far from independent)")
    print(f"   E[{a}X + {b}Y] by building the column   {combined:.6f}")
    print(f"   {a}E[X] + {b}E[Y], never combining      {separate:.6f}")
    assert np.isclose(combined, separate), "linearity failed, which cannot happen"
    print("   equal. Linearity never asked whether the columns were independent.\n")

    print("3. E[XY] = E[X]E[Y] holds only under independence")
    for label, left, right in (
        ("independent  (latency, screen_dpi)", frame["latency_ms"], frame["screen_dpi"]),
        ("dependent    (prompt, output)     ", x, y),
    ):
        product = float((left * right).mean())
        separate_product = float(left.mean()) * float(right.mean())
        gap = abs(product - separate_product) / separate_product
        print(
            f"   {label}  E[XY]={product:>14,.2f}  "
            f"E[X]E[Y]={separate_product:>14,.2f}  relative gap {gap:>7.4f}"
        )
    print("   The first pair agrees to a fraction of a percent. The second does not.\n")

    print("4. Out-of-bag fraction: linearity over n DEPENDENT indicators")
    print("   Derived: P(item j missed by all n draws) = (1 - 1/n)^n, then sum by linearity.")
    rng = np.random.default_rng(20260824)
    for n in (10, 100, 1_000, 10_000):
        derived = (1.0 - 1.0 / n) ** n
        trials = 2_000 if n <= 1_000 else 300
        measured = float(
            np.mean([len(np.unique(rng.integers(0, n, n))) / n for _ in range(trials)])
        )
        print(
            f"   n={n:>6,}   derived {derived:.6f}   "
            f"measured left out {1 - measured:.6f}   ({trials} resamples)"
        )
    print(f"   limit 1/e = {1 / np.e:.6f}")
    print(
        "\n   The derivation never wrote down the joint distribution of the n\n"
        "   indicators, which is just as well: they are dependent, and that joint\n"
        "   is the thing linearity let us skip."
    )


if __name__ == "__main__":
    main()
