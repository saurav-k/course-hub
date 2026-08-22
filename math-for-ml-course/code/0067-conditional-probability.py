"""Lesson 0067 - conditional probability, the law of total probability, the chain rule.

Conditioning shrinks the sample space and renormalises. This program computes the
same conditional probability two ways to show that literally:

  1. From the definition: P(AB) / P(A), both measured over all 25,000 rows.
  2. By filtering to the rows where A holds and taking the mean there.

Route 2 is route 1 with the 25,000 cancelled top and bottom, which is what
"conditioning is the old measurement over a smaller population" means.

It then verifies the law of total probability numerically by recovering the
unconditional flag rate from the two conditionals and their weights, and checks
the chain rule on a three-way joint.

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


def conditional_from_the_definition(b: np.ndarray, a: np.ndarray) -> float:
    """P(B | A) = P(AB) / P(A), with both measured over the whole sample space."""
    p_joint = (a & b).mean()
    p_given = a.mean()
    if p_given == 0.0:
        raise ZeroDivisionError("conditioning on an event of probability zero")
    return float(p_joint / p_given)


def conditional_by_restricting(b: np.ndarray, a: np.ndarray) -> float:
    """The same number, by throwing away every row where A is false."""
    restricted = b[a]
    if restricted.size == 0:
        raise ZeroDivisionError("conditioning on an event of probability zero")
    return float(restricted.mean())


def main() -> None:
    frame = load()
    flagged = frame["flagged"].to_numpy(dtype=bool)
    verified = frame["verified_user"].to_numpy(dtype=bool)
    unverified = ~verified

    print("P(flagged | not verified), two ways")
    definition = conditional_from_the_definition(flagged, unverified)
    restricted = conditional_by_restricting(flagged, unverified)
    print(f"    P(AB)              = {(unverified & flagged).mean():.8f}")
    print(f"    P(A)               = {unverified.mean():.8f}")
    print(f"    definition, AB / A = {definition:.8f}")
    print(f"    restricted mean    = {restricted:.8f}")
    assert abs(definition - restricted) < 1e-12, "the two routes disagree"
    print(f"    counts: {int((unverified & flagged).sum())} flagged "
          f"of {int(unverified.sum())} unverified - the 25,000 cancelled")

    print("\nconditioning can move a probability up, down, or not at all")
    print(f"    P(flagged)                 = {flagged.mean():.6f}")
    print(f"    P(flagged | not verified)  = {definition:.6f}   up")
    print(f"    P(flagged | verified)      = {conditional_by_restricting(flagged, verified):.6f}   down")
    cached = frame["cache_hit"].to_numpy(dtype=bool)
    print(f"    P(cached)                  = {cached.mean():.6f}")
    print(f"    P(cached | verified)       = {conditional_by_restricting(cached, verified):.6f}   barely moved")

    print("\nthe law of total probability recovers the unconditional rate")
    recovered = (
        conditional_by_restricting(flagged, unverified) * unverified.mean()
        + conditional_by_restricting(flagged, verified) * verified.mean()
    )
    print(f"    P(f|~v)P(~v) + P(f|v)P(v) = {recovered:.8f}")
    print(f"    P(flagged) counted directly = {flagged.mean():.8f}")
    assert abs(recovered - flagged.mean()) < 1e-12, "total probability does not close"

    print("\nthe chain rule on a three-way joint")
    a, b, c = verified, cached, (frame["retries"].to_numpy() == 1)
    direct = (a & b & c).mean()
    chained = a.mean() * conditional_by_restricting(b, a) * conditional_by_restricting(c, a & b)
    print(f"    P(A,B,C) counted directly           = {direct:.8f}")
    print(f"    P(A) P(B|A) P(C|A,B)                = {chained:.8f}")
    assert abs(direct - chained) < 1e-12, "the chain rule does not close"
    print("    the factorisation is always true, and it needs no independence")


if __name__ == "__main__":
    main()
