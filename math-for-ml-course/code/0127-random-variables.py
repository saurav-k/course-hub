"""Lesson 0127 - a random variable is a function, applied two ways.

X is the number of abusive requests in a minibatch of 256. That is a function
from batches to whole numbers, and this program builds it twice:

  1. With an explicit loop over the 97 batches that counts one row at a time,
     so the function is visibly being applied to each outcome.
  2. Vectorised, by reshaping the flag column and summing along an axis.

The two arrays must be identical, element for element, not merely equal in
distribution. That assertion is the point: the vectorised form is not a
different calculation, it is the same function computed faster.

It then demonstrates the preimage. For each value k, the set of batches with
X = k is a subset of the sample space, which is what makes P(X = k) meaningful
at all, and the program prints those batch indices and checks each really does
contain k flagged rows.

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

BATCH = 256


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def apply_the_function_one_batch_at_a_time(flags: np.ndarray, batch: int) -> np.ndarray:
    """X(omega) for each batch omega, counted row by row.

    This is the function being applied: for each outcome in the sample space,
    look at what it contains and return a number.
    """
    n_batches = len(flags) // batch
    values = np.empty(n_batches, dtype=int)
    for index in range(n_batches):
        rows = flags[index * batch:(index + 1) * batch]
        total = 0
        for row in rows:
            total += int(row)
        values[index] = total
    return values


def apply_the_function_vectorised(flags: np.ndarray, batch: int) -> np.ndarray:
    """The same function, computed for every outcome at once."""
    n_batches = len(flags) // batch
    return flags[: n_batches * batch].reshape(n_batches, batch).sum(axis=1)


def main() -> None:
    frame = load()
    flags = frame["flagged"].to_numpy(dtype=bool)

    by_loop = apply_the_function_one_batch_at_a_time(flags, BATCH)
    vectorised = apply_the_function_vectorised(flags, BATCH)
    assert np.array_equal(by_loop, vectorised), "the two routes disagree batch by batch"
    print(f"the function agrees on all {len(by_loop)} batches, element for element")

    dropped = len(flags) - len(by_loop) * BATCH
    print(f"\nsample space: {len(by_loop)} batches of {BATCH} rows "
          f"({dropped} rows dropped so every batch is the same size)")
    print(f"total flags inside the batches: {int(by_loop.sum())}, "
          f"and in the dropped tail: {int(flags[len(by_loop) * BATCH:].sum())}")

    print("\nthe distribution X induces on the whole numbers:")
    counts = np.bincount(by_loop)
    for value, count in enumerate(counts):
        if count:
            print(f"    X = {value}:  {count:3d} batches   "
                  f"proportion {count / len(by_loop):.4f}")
    print(f"    mean of X = {by_loop.sum()} / {len(by_loop)} = {by_loop.mean():.4f}")

    print("\nthe preimage: {X = 3} is a SET OF BATCHES, which is why it has a probability")
    preimage = np.flatnonzero(by_loop == 3)
    print(f"    batches with X = 3: {preimage.tolist()}")
    for index in preimage:
        rows = flags[index * BATCH:(index + 1) * BATCH]
        assert int(rows.sum()) == 3, "a batch in the preimage does not contain 3"
    print("    each one really does contain exactly 3 flagged requests")

    print("\nchange the function, not the world: batches of 1024")
    bigger = apply_the_function_vectorised(flags, 1024)
    print(f"    {len(bigger)} batches, P(X = 0) = {float(np.mean(bigger == 0)):.4f}, "
          f"mean {bigger.mean():.4f}")
    print("    the same 99 flags, a different function, a different distribution")


if __name__ == "__main__":
    main()
