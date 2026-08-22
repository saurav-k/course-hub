"""Conditional distributions, and why conditioning is not intervening.

Lesson: Conditional distributions, PMF and PDF.

    python3 0802-conditional-distributions.py

What it checks twice:

  1. A conditional PMF is a slice of the joint divided by that slice's own total.
     Route one slices the joint. Route two filters the raw rows and counts. Same
     answer, and the second route is the one that shows what conditioning IS.
  2. Every conditional distribution sums to 1. Checked for every slice, not one.
  3. Bayes' theorem reverses a conditional. The program computes P(tier | slow)
     from P(slow | tier) and the marginals, and separately by direct counting,
     and the two agree. That is Bayes verified rather than quoted.
  4. A conditional DENSITY is a slice of a joint density. The program does the
     continuous case by narrow binning, which is what a density is a limit of.
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
    return pd.cut(
        frame["latency_ms"],
        bins=[0.0, 120.0, 260.0, np.inf],
        labels=["fast", "normal", "slow"],
        right=False,
    )


def main() -> None:
    frame = load()
    frame["latency_band"] = latency_band(frame)

    counts = pd.crosstab(frame["tier"], frame["latency_band"])
    joint = counts / counts.to_numpy().sum()

    # Route one: divide each row of the joint by that row's own total.
    from_joint = joint.div(joint.sum(axis=1), axis=0)
    # Route two: filter the raw rows to one tier and count. This is what the
    # division above is DOING, and seeing them agree is the point.
    from_filter = pd.DataFrame(
        {
            band: {
                tier: (
                    (frame.loc[frame["tier"] == tier, "latency_band"] == band).sum()
                    / (frame["tier"] == tier).sum()
                )
                for tier in counts.index
            }
            for band in counts.columns
        }
    )[list(counts.columns)]

    print("P(latency_band | tier), by slicing the joint")
    print(from_joint.round(4))
    assert np.allclose(from_joint.to_numpy(), from_filter.loc[from_joint.index].to_numpy())
    print("\nfiltering the raw rows gives the same table to machine precision")

    row_sums = from_joint.sum(axis=1)
    print("\nevery conditional sums to 1:", np.round(row_sums.to_numpy(), 10))
    assert np.allclose(row_sums, 1.0)

    print("\nCompare against the unconditional distribution")
    marginal = frame["latency_band"].value_counts(normalize=True).reindex(counts.columns)
    print(pd.concat([marginal.rename("P(band)"), from_joint.T], axis=1).round(4))
    print(
        "\nP(slow) overall is "
        f"{marginal['slow']:.4f}, but P(slow | enterprise) is "
        f"{from_joint.loc['enterprise', 'slow']:.4f} and P(slow | free) is "
        f"{from_joint.loc['free', 'slow']:.4f}.\n"
        "Knowing the tier changes the answer by a factor of "
        f"{from_joint.loc['free', 'slow'] / from_joint.loc['enterprise', 'slow']:.1f}. "
        "That is what a feature is."
    )

    # Bayes, computed two ways.
    print("\nBayes: reversing the conditional")
    p_slow_given_tier = from_joint["slow"]
    p_tier = frame["tier"].value_counts(normalize=True).reindex(from_joint.index)
    numerator = p_slow_given_tier * p_tier
    by_bayes = numerator / numerator.sum()
    by_counting = (
        frame.loc[frame["latency_band"] == "slow", "tier"]
        .value_counts(normalize=True)
        .reindex(from_joint.index)
    )
    print(pd.DataFrame({"by Bayes": by_bayes, "by counting": by_counting}).round(6))
    assert np.allclose(by_bayes, by_counting), "Bayes disagreed with direct counting"
    print("agree to machine precision\n")

    # The continuous case: a conditional density is a slice of a joint density.
    print("Conditional density of latency given tier, by narrow binning")
    edges = np.linspace(0.0, 600.0, 61)
    width = edges[1] - edges[0]
    table = {}
    beyond = {}
    for tier in from_joint.index:
        values = frame.loc[frame["tier"] == tier, "latency_ms"]
        counts_in_bins, _ = np.histogram(values, bins=edges)
        # Divide by ALL of this tier's rows, not only the ones inside the range.
        # numpy's density=True would divide by the in-range count instead, which
        # renormalises the tail away and always reports an area of exactly 1.
        table[tier] = counts_in_bins / (len(values) * width)
        beyond[tier] = float((values >= edges[-1]).mean())
    densities = pd.DataFrame(table, index=np.round(edges[:-1] + width / 2, 1))
    print(densities.iloc[6:14].round(6))

    areas = densities.sum() * width
    print("\narea under each conditional density, over 0 to 600 ms only:")
    summary = pd.DataFrame(
        {"area in range": areas, "mass beyond 600 ms": pd.Series(beyond)}
    )
    summary["total"] = summary.sum(axis=1)
    print(summary.round(4).to_string())
    assert np.allclose(summary["total"], 1.0, atol=1e-9), "the two pieces must make 1"
    print(
        "\nEach area falls short of 1 by exactly the mass past 600 ms, and the two\n"
        "columns add back to 1. A density integrates to 1 over its WHOLE support,\n"
        "and free tier keeps "
        f"{beyond['free'] * 100:.2f} percent of its mass out there against "
        f"enterprise's {beyond['enterprise'] * 100:.2f} percent.\n"
        "That gap is the heavy tail, measured rather than described."
    )


if __name__ == "__main__":
    main()
