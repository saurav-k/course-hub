"""Joint and marginal distributions, on 40,000 inference requests.

Lesson: Joint distributions, and what a marginal is.

Run it:

    python3 0801-joint-and-marginal.py

Needs numpy and pandas and nothing else.

What it shows, and what it checks twice:

  1. A joint PMF over two columns is a table of counts divided by the total, and
     its cells sum to 1.
  2. A marginal is that table summed along one axis. The check: the marginal
     computed from the joint must equal the marginal computed directly from the
     raw column, without ever forming the joint. Two routes, one answer.
  3. Independence is factorisation. The program measures how far the joint is
     from the product of its marginals, on a pair that IS nearly independent and
     on a pair that is not, so the reader sees the number separate them.
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


def latency_band(frame: pd.DataFrame) -> pd.Series:
    """Bucket latency into three named bands at fixed millisecond cut points.

    Fixed cuts rather than quantiles, so the bands mean the same thing on a
    bigger extract of the same data and the reader can reason about them.
    """
    return pd.cut(
        frame["latency_ms"],
        bins=[0.0, 120.0, 260.0, np.inf],
        labels=["fast", "normal", "slow"],
        right=False,
    )


def joint_pmf(left: pd.Series, right: pd.Series) -> pd.DataFrame:
    """The joint probability mass function of two categorical columns."""
    counts = pd.crosstab(left, right)
    return counts / counts.to_numpy().sum()


def total_variation(joint: pd.DataFrame) -> float:
    """Half the summed absolute gap between the joint and its own marginals' product.

    Zero exactly when the two columns are independent. It is a distance, so it
    answers "how far from independent" rather than only "independent or not".
    """
    row = joint.sum(axis=1).to_numpy()[:, None]
    column = joint.sum(axis=0).to_numpy()[None, :]
    return float(0.5 * np.abs(joint.to_numpy() - row * column).sum())


def main() -> None:
    frame = load()
    frame["latency_band"] = latency_band(frame)
    print(f"rows {len(frame):,}\n")

    joint = joint_pmf(frame["tier"], frame["latency_band"])
    print("Joint PMF  P(tier, latency_band)")
    print(joint.round(4))
    print(f"\ncells sum to {joint.to_numpy().sum():.10f}\n")

    # Route one: marginalise the joint by summing away the other variable.
    from_joint = joint.sum(axis=1)
    # Route two: count the raw column directly, never forming the joint at all.
    from_raw = frame["tier"].value_counts(normalize=True).reindex(from_joint.index)

    print("Marginal P(tier), by two independent routes")
    comparison = pd.DataFrame({"summed from joint": from_joint, "counted directly": from_raw})
    print(comparison.round(6))
    assert np.allclose(from_joint, from_raw), "the two routes disagree"
    print("\nboth routes agree to machine precision\n")

    print("Distance from independence, on two pairs of columns")
    frame["dpi_band"] = pd.qcut(frame["screen_dpi"], 3, labels=["low", "mid", "high"])
    dependent = total_variation(joint_pmf(frame["tier"], frame["latency_band"]))
    null = total_variation(joint_pmf(frame["dpi_band"], frame["latency_band"]))
    print(f"  tier      against latency_band   {dependent:.4f}   <- genuinely dependent")
    print(f"  dpi_band  against latency_band   {null:.4f}   <- independent by construction")
    print(
        "\nThe second number is not exactly zero and never will be: it is an\n"
        "estimate from 40,000 rows, so sampling noise keeps it a little above 0."
    )

    # The cost of a full joint, which is why independence assumptions exist.
    print("\nFree numbers needed for a full joint over d binary features")
    for d in (5, 10, 20, 50):
        print(f"  d={d:<3d} full joint {2**d - 1:>20,}   assuming independence {d:>4,}")


if __name__ == "__main__":
    main()
