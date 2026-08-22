"""0005 - argmax, argmin, and what training actually is.

max returns a value and argmax returns a place, and the two have different
types. This program shows that on real logits, then checks the theorem this
lesson proves - softmax is shift invariant - at the scale of 9,000 rows, and
shows the naive softmax failing where the stabilised one does not.

Needs only numpy and pandas.
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "tickets.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/tickets.csv"
CLASSES = ["urgent", "normal", "spam"]


def load() -> pd.DataFrame:
    """Relative to this file so the repository works offline, URL so Colab works."""
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def softmax_naive(z: np.ndarray) -> np.ndarray:
    """Straight from the formula, with nothing done about the exponentials."""
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def softmax_stable(z: np.ndarray) -> np.ndarray:
    """The same function, with the shift the theorem says costs nothing."""
    shifted = z - z.max(axis=-1, keepdims=True)
    e = np.exp(shifted)
    return e / e.sum(axis=-1, keepdims=True)


def main() -> None:
    frame = load()
    logits = frame[["logit_urgent", "logit_normal", "logit_spam"]].to_numpy()
    print(f"logits: {logits.shape[0]:,} rows x {logits.shape[1]} classes")

    # ---- max is a value, argmax is a place -------------------------------
    row = logits[0]
    print(f"\none row: {np.round(row, 4).tolist()}")
    print(f"  max    = {row.max():.4f}          a score, a float")
    print(f"  argmax = {row.argmax()}  -> '{CLASSES[row.argmax()]}'   a class, an index")
    assert isinstance(float(row.max()), float)
    assert isinstance(int(row.argmax()), int)
    print(f"  the two answer different questions and have different types")

    # ---- argmin is argmax with a sign flip -------------------------------
    assert row.argmin() == (-row).argmax(), "argmin should be argmax of the negation"
    print(f"  argmin = {row.argmin()}, which is argmax of the negated row: the sign flip")

    # ---- ties: argmax is a set, and the library picks one -----------------
    tied = np.array([2.0, 2.0, 1.0])
    every = np.flatnonzero(tied == tied.max())
    print(f"\n  on {tied.tolist()} the argmax SET is {every.tolist()}")
    print(f"  numpy returns {tied.argmax()}, which is a convention and not the mathematics")
    assert len(every) == 2 and tied.argmax() == every[0]

    # ---- shift invariance, the theorem, checked on every row -------------
    print("\nshift invariance, checked on all rows")
    baseline = softmax_stable(logits)
    for shift in (-800.0, -5.0, 5.0, 800.0):
        shifted = softmax_stable(logits + shift)
        assert np.allclose(baseline, shifted), f"shift of {shift} changed the output"
    print("  softmax(z + c) == softmax(z) for c in -800, -5, 5, 800")

    # ---- and where the naive version dies --------------------------------
    with np.errstate(over="ignore", invalid="ignore"):
        naive_big = softmax_naive(logits + 800.0)
        naive_small = softmax_naive(logits - 800.0)
    print(f"\n  naive softmax after +800: {np.isnan(naive_big).all(axis=1).sum():,} of "
          f"{len(logits):,} rows are entirely nan")
    print(f"  naive softmax after -800: {np.isnan(naive_small).all(axis=1).sum():,} rows are entirely nan")
    print(f"  stable softmax after +800: {np.isfinite(softmax_stable(logits + 800.0)).all()} finite everywhere")
    assert np.isnan(naive_big).all(), "expected the naive version to overflow"
    assert np.isnan(naive_small).all(), "expected the naive version to underflow"
    assert np.isfinite(softmax_stable(logits + 800.0)).all()

    # ---- temperature changes confidence, never the prediction ------------
    print("\ntemperature")
    reference = logits.argmax(axis=1)
    for temperature in (0.5, 1.0, 2.0, 10.0):
        probabilities = softmax_stable(logits / temperature)
        assert np.array_equal(probabilities.argmax(axis=1), reference), (
            f"temperature {temperature} moved a prediction"
        )
        print(f"  T = {temperature:>4}: mean top probability {probabilities.max(axis=1).mean():.4f}, "
              f"argmax unchanged on all {len(logits):,} rows")

    print(f"\n  softmax rows sum to 1: max deviation {np.abs(baseline.sum(axis=1) - 1).max():.2e}")
    assert np.allclose(baseline.sum(axis=1), 1.0)

    print("\nall assertions passed")


if __name__ == "__main__":
    main()
