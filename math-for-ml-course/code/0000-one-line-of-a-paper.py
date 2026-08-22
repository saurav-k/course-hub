"""Lesson 00 - the softmax in the attention line, computed two ways.

Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V   (Vaswani et al. 2017, section 3.2.1)

This program does the softmax part on a real 12,000 x 8 matrix, so the reader can
see the same arithmetic they did by hand on four numbers run at a scale where
doing it by hand is impossible.

It computes the softmax twice:

  1. Straight from the definition: exp of each score, divided by the row's sum.
  2. The way every library actually does it: subtract each row's maximum first.

Those two are algebraically identical - subtracting a constant c from every score
multiplies the top and the bottom by exp(-c), which cancels - and they are NOT
identical in floating point. The second one is what survives large scores. The
program asserts they agree where both are finite, then shows the first one
failing on scores ten times bigger.

Needs only numpy and pandas. Runs in a codebase, in Jupyter, or in Colab.
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "sensors.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/sensors.csv"

SENSORS = [
    "vibration_x", "vibration_y", "acoustic_db", "current_amp",
    "humidity_pct", "dust_index", "temp_c", "pressure_kpa",
]


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def softmax_from_the_definition(scores: np.ndarray) -> np.ndarray:
    """exp of each score over the row's total. Exactly what the formula says."""
    weights = np.exp(scores)
    return weights / weights.sum(axis=1, keepdims=True)


def softmax_the_way_libraries_do_it(scores: np.ndarray) -> np.ndarray:
    """The same function, shifted by each row's maximum before the exp.

    Subtracting a constant from every score in a row multiplies numerator and
    denominator by the same factor, so the answer is unchanged on paper. In
    floating point it is the difference between an answer and an overflow.
    """
    shifted = scores - scores.max(axis=1, keepdims=True)
    weights = np.exp(shifted)
    return weights / weights.sum(axis=1, keepdims=True)


def main() -> None:
    frame = load()
    raw = frame[SENSORS].to_numpy(dtype=float)

    # Put every column on the same footing first. `pressure_kpa` is in the
    # hundreds and `vibration_x` is near zero, and a softmax over those raw
    # numbers is a one-hot: pressure wins every row and the other seven get
    # weights near 1e-200. Standardising is what makes the eight comparable,
    # and it is the same problem the attention line solves by dividing by the
    # square root of the key dimension. M02 and M03 build this properly.
    scores = (raw - raw.mean(axis=0)) / raw.std(axis=0, ddof=1)
    print(f"score matrix: {scores.shape[0]:,} rows x {scores.shape[1]} columns, standardised")

    plain = softmax_from_the_definition(scores)
    stable = softmax_the_way_libraries_do_it(scores)

    print(f"largest disagreement between the two: {np.abs(plain - stable).max():.3e}")
    assert np.allclose(plain, stable), "the two softmaxes must agree at this scale"

    row_totals = stable.sum(axis=1)
    print(f"every row sums to 1: min {row_totals.min():.12f}, max {row_totals.max():.12f}")
    print(f"largest single weight anywhere: {stable.max():.4f}")
    print(f"smallest single weight anywhere: {stable.min():.3e}")

    # Now the reason the shift exists. Large scores are not unusual - they are
    # what un-scaled dot products produce, and preventing them is exactly why the
    # attention line divides by the square root of the key dimension.
    big = scores * 300.0
    with np.errstate(over="ignore", invalid="ignore"):
        broken = softmax_from_the_definition(big)
    survived = softmax_the_way_libraries_do_it(big)

    bad_rows = int(np.isnan(broken).any(axis=1).sum())
    print(f"\nat 300 times the scale:")
    print(f"  from the definition: {bad_rows:,} of {len(big):,} rows came back as nan")
    print(f"  shifted first:       {int(np.isnan(survived).any(axis=1).sum()):,} rows nan, "
          f"row sums still {survived.sum(axis=1).min():.12f} to {survived.sum(axis=1).max():.12f}")


if __name__ == "__main__":
    main()
