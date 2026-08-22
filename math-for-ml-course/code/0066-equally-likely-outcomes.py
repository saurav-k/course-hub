"""Lesson M07-03 - equally likely outcomes, and the cost of assuming it wrongly.

Counting outcomes and dividing is a probability MODEL, not a definition. It is
correct only when something makes the outcomes genuinely symmetric.

This program shows both halves of that.

Where the assumption holds: drawing one row at random from the log really does
make all 25,000 rows equally likely, because the draw is what makes them so. The
program computes P(route = rerank) from the definition and again with pandas,
asserts they agree, then draws 200,000 random rows and confirms the empirical
frequency matches.

Where it fails: assuming the three ROUTES are equally likely is a claim about
the routes, and the file says it is wrong by up to 79 percent.

It closes with the with-and-without-replacement pair probabilities, which is the
difference between a binomial and a hypergeometric and is worth seeing as a
number before Lesson 10 names it.

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

SEED = 20260822
DRAWS = 200_000


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def probability_by_counting(frame: pd.DataFrame, route: str) -> float:
    """|A| / |Omega|, written out. Count the matching rows, divide by the total."""
    matching = int((frame["route"] == route).sum())
    total = len(frame)
    return matching / total


def probability_the_pandas_way(frame: pd.DataFrame, route: str) -> float:
    """The same number, from the library."""
    return float(frame["route"].value_counts(normalize=True)[route])


def main() -> None:
    frame = load()
    rng = np.random.default_rng(SEED)

    print("where the assumption HOLDS: a uniform draw over 25,000 rows")
    by_hand = probability_by_counting(frame, "rerank")
    by_library = probability_the_pandas_way(frame, "rerank")
    print(f"    counted   |A| / |Omega| = {by_hand:.6f}")
    print(f"    pandas    value_counts  = {by_library:.6f}")
    assert abs(by_hand - by_library) < 1e-12, "the two routes disagree"

    picks = rng.integers(0, len(frame), size=DRAWS)
    empirical = float((frame["route"].to_numpy()[picks] == "rerank").mean())
    print(f"    {DRAWS:,} actual random draws     = {empirical:.6f}")
    print("    the draw is uniform, so counting rows is the right model")

    print("\nwhere the assumption FAILS: the three routes are not equally likely")
    assumed = 1 / 3
    for route, actual in frame["route"].value_counts(normalize=True).items():
        error = abs(actual - assumed) / assumed
        print(
            f"    {route:<7} assumed {assumed:.4f}   actual {actual:.4f}   "
            f"off by {error * 100:5.1f}%"
        )
    print("    'no information, so assume uniform' was a claim, and it was wrong")

    print("\nwith and without replacement, two rerank requests")
    n_rerank = int((frame["route"] == "rerank").sum())
    total = len(frame)
    with_replacement = (n_rerank / total) ** 2
    without_replacement = (n_rerank / total) * ((n_rerank - 1) / (total - 1))
    print(f"    with replacement    {with_replacement:.6f}   the draws are independent")
    print(f"    without replacement {without_replacement:.6f}   the first draw changes the second")
    print(f"    difference          {with_replacement - without_replacement:.8f}")
    print("    tiny here because 25,000 is large. It is the binomial/hypergeometric gap.")


if __name__ == "__main__":
    main()
