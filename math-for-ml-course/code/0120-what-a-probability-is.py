"""Lesson M07-01 - a probability estimated from data, computed two ways.

A frequentist probability is a rate over repetitions. This program estimates one
- the rate at which requests are served from cache - and shows it settling as
the number of repetitions grows, which is the claim the page makes in words.

It computes the running estimate twice:

  1. From the definition, one row at a time: keep a count of hits and a count of
     trials, and divide. This is what the page does by hand on ten rows.
  2. Vectorised with a cumulative sum over all 25,000 rows.

The two are the same arithmetic. The first shows it; the second scales. The
program asserts they agree on the overlap.

Needs only numpy and pandas. Runs in a codebase, in Jupyter, or in Colab.
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "requests.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/requests.csv"
)


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def running_rate_from_the_definition(outcomes: np.ndarray) -> np.ndarray:
    """Count the successes, count the trials, divide. One row at a time.

    This is the loop the page works by hand. It is deliberately not vectorised,
    because the point is to show that a probability estimate is nothing but a
    running count over a running total.
    """
    estimates = np.empty(len(outcomes), dtype=float)
    successes = 0
    for trial, outcome in enumerate(outcomes, start=1):
        successes += int(outcome)
        estimates[trial - 1] = successes / trial
    return estimates


def running_rate_vectorised(outcomes: np.ndarray) -> np.ndarray:
    """The same estimate, computed for every prefix at once."""
    trials = np.arange(1, len(outcomes) + 1)
    return np.cumsum(outcomes) / trials


def largest_step(estimates: np.ndarray, lo: int, hi: int) -> float:
    """Biggest jump between consecutive estimates in the window [lo, hi)."""
    window = estimates[lo:hi]
    return float(np.max(np.abs(np.diff(window))))


def main() -> None:
    frame = load()
    cache_hit = frame["cache_hit"].to_numpy(dtype=bool)

    # The loop runs over the first 200 rows only; it is O(n) either way, but the
    # page only needs the early rows, where the estimate is still moving.
    by_definition = running_rate_from_the_definition(cache_hit[:200])
    vectorised = running_rate_vectorised(cache_hit)

    assert np.allclose(by_definition, vectorised[:200]), "the two routes disagree"
    print("definition and vectorised agree on the first 200 rows")

    print("\nthe estimate settling:")
    for n in (10, 100, 1_000, 25_000):
        print(f"  after {n:>6,} requests   P(cache_hit) = {vectorised[n - 1]:.4f}")

    print("\nlargest single-step change, by decade:")
    for lo, hi in ((1, 10), (10, 100), (100, 1_000), (1_000, 25_000)):
        print(f"  rows {lo:>6,} to {hi:>6,}   {largest_step(vectorised, lo, hi):.4f}")

    print(
        "\nThe estimate is a random variable too. Ten rows is not a probability,"
        "\nit is a noisy guess at one, and how noisy is what Module 09 measures."
    )


if __name__ == "__main__":
    main()
