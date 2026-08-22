"""Lesson M07-02 - the three axioms, checked, and inclusion-exclusion two ways.

The axioms are three lines and everything else in probability is derived from
them. This program does two things with that.

First it checks the axioms on a real distribution: the three-state `route`
column. Non-negativity, additivity over mutually exclusive events, and total
mass one. All three are arithmetic a reader can follow.

Second it computes P(A or B) twice:

  1. From inclusion-exclusion, using the three separate probabilities.
  2. By directly counting the rows where either event holds.

Those agree because the axioms force them to, and the assertion is the proof
running on 25,000 rows rather than on a Karnaugh map.

It closes by showing the failure the page warns about: three independent
sigmoid-style scores summing past 1, which is not a distribution over labels.

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


def union_by_inclusion_exclusion(a: np.ndarray, b: np.ndarray) -> float:
    """P(A or B) = P(A) + P(B) - P(A and B). The theorem, spelled out."""
    p_a = a.mean()
    p_b = b.mean()
    p_both = (a & b).mean()
    return float(p_a + p_b - p_both)


def union_by_counting(a: np.ndarray, b: np.ndarray) -> float:
    """P(A or B), by counting the rows where either holds. No theorem used."""
    return float((a | b).mean())


def check_the_axioms(masses: np.ndarray) -> None:
    """The three probability axioms, as three assertions."""
    assert (masses >= 0).all(), "axiom 1 fails: a probability went negative"
    assert abs(masses.sum() - 1.0) < 1e-12, "axiom 3 fails: the total is not 1"
    print("  axiom 1, every probability is non-negative:  ok")
    print(f"  axiom 3, the total is one:                   ok ({masses.sum():.12f})")


def main() -> None:
    frame = load()

    print("the three route outcomes as a probability measure:")
    counts = frame["route"].value_counts()
    masses = (counts / len(frame)).to_numpy()
    for name, mass in zip(counts.index, masses):
        print(f"    P({name:<7}) = {int(counts[name]):>6,} / 25,000 = {mass:.4f}")
    check_the_axioms(masses)

    # Axiom 2 needs mutually exclusive events, and distinct routes are exactly that.
    chat = (frame["route"] == "chat").to_numpy()
    embed = (frame["route"] == "embed").to_numpy()
    print(
        f"  axiom 2, additivity over disjoint events:    "
        f"{chat.mean():.4f} + {embed.mean():.4f} = {chat.mean() + embed.mean():.4f}"
        f"  and directly {(chat | embed).mean():.4f}"
    )

    print("\ninclusion-exclusion, where the events DO overlap:")
    verified = frame["verified_user"].to_numpy(dtype=bool)
    cached = frame["cache_hit"].to_numpy(dtype=bool)
    theorem = union_by_inclusion_exclusion(verified, cached)
    counted = union_by_counting(verified, cached)
    print(f"    P(verified)            = {verified.mean():.5f}")
    print(f"    P(cached)              = {cached.mean():.5f}")
    print(f"    P(both)                = {(verified & cached).mean():.5f}")
    print(f"    P(either), theorem     = {theorem:.6f}")
    print(f"    P(either), by counting = {counted:.6f}")
    assert abs(theorem - counted) < 1e-12, "inclusion-exclusion disagrees with the count"
    print("    the two agree, which is what the minus sign is for")

    naive = verified.mean() + cached.mean()
    print(f"    without the minus sign you would get {naive:.6f}, too big by "
          f"{naive - counted:.6f}, which is exactly P(both)")

    print("\nthe failure: three sigmoid scores are not a distribution over labels")
    scores = np.array([0.9, 0.8, 0.7])
    print(f"    scores {scores.tolist()} sum to {scores.sum():.1f}")
    print("    axiom 3 fails. These are three Bernoullis on three sample spaces,")
    print("    not one distribution over three labels.")


if __name__ == "__main__":
    main()
