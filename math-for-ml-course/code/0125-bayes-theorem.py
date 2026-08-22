"""Lesson 0125 - Bayes' theorem, computed three ways that must agree.

Bayes reverses a conditional. This program computes the same posterior by three
independent routes and asserts all three land on the same number:

  1. The expanded formula: prior times likelihood, over the law of total
     probability in the denominator.
  2. The odds form: prior odds times the likelihood ratio, converted back to a
     probability. The evidence term cancels and never appears.
  3. Direct counting of the confusion table, which uses no theorem at all.

Route 3 is the control. If routes 1 and 2 agree with it, the algebra is right.

It then applies the same machinery to the abuse detector, computing precision
from Bayes and from a counted confusion matrix at two thresholds.

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


def posterior_expanded(prior: float, likelihood: float, likelihood_other: float) -> float:
    """P(E|A) = P(A|E)P(E) / [ P(A|E)P(E) + P(A|not E)P(not E) ].

    The denominator is the law of total probability over the two-part partition.
    """
    evidence = likelihood * prior + likelihood_other * (1.0 - prior)
    return likelihood * prior / evidence


def posterior_from_odds(prior: float, likelihood: float, likelihood_other: float) -> float:
    """Posterior odds = prior odds x likelihood ratio. No evidence term at all."""
    prior_odds = prior / (1.0 - prior)
    likelihood_ratio = likelihood / likelihood_other
    posterior_odds = prior_odds * likelihood_ratio
    return posterior_odds / (1.0 + posterior_odds)


def precision_from_bayes(prior: float, recall: float, false_positive_rate: float) -> float:
    """Precision IS a posterior: P(positive | flagged)."""
    return posterior_expanded(prior, recall, false_positive_rate)


def main() -> None:
    frame = load()
    verified = frame["verified_user"].to_numpy(dtype=bool)
    flagged = frame["flagged"].to_numpy(dtype=bool)
    unverified = ~verified

    prior = float(unverified.mean())
    likelihood = float(flagged[unverified].mean())
    likelihood_other = float(flagged[verified].mean())

    print("reversing P(flagged | unverified) into P(unverified | flagged)")
    print(f"    prior      P(unverified)             = {prior:.5f}")
    print(f"    likelihood P(flagged | unverified)   = {likelihood:.6f}")
    print(f"    the other  P(flagged | verified)     = {likelihood_other:.6f}")

    evidence = likelihood * prior + likelihood_other * (1.0 - prior)
    print(f"    evidence   P(flagged), by total prob = {evidence:.6f}")
    print(f"               P(flagged), counted       = {flagged.mean():.6f}")

    expanded = posterior_expanded(prior, likelihood, likelihood_other)
    odds = posterior_from_odds(prior, likelihood, likelihood_other)
    counted = float(unverified[flagged].mean())

    print(f"\n    1. expanded formula = {expanded:.6f}")
    print(f"    2. odds form        = {odds:.6f}")
    print(f"    3. counted directly = {counted:.6f}   "
          f"({int((unverified & flagged).sum())} of {int(flagged.sum())})")
    assert abs(expanded - counted) < 1e-9, "the expanded formula disagrees with the count"
    assert abs(odds - counted) < 1e-9, "the odds form disagrees with the count"

    prior_odds = prior / (1 - prior)
    ratio = likelihood / likelihood_other
    print(f"\n    odds form in full: {prior_odds:.4f} x {ratio:.2f} = "
          f"{prior_odds * ratio:.4f} posterior odds")
    print(f"    the prior said {prior:.2%}, the evidence moved it to {counted:.2%}")

    print("\nthe same theorem is precision, at two detector thresholds")
    score = frame["abuse_score"].to_numpy()
    base_rate = float(flagged.mean())
    clean = ~flagged
    for threshold in (0.5, 0.6):
        predicted = score >= threshold
        recall = float(predicted[flagged].mean())
        false_positive_rate = float(predicted[clean].mean())
        from_bayes = precision_from_bayes(base_rate, recall, false_positive_rate)
        from_counts = float(flagged[predicted].mean())
        print(f"    threshold {threshold}:  recall {recall:.4f}   FPR {false_positive_rate:.4f}")
        print(f"        precision from Bayes  = {from_bayes:.4f}")
        print(f"        precision from counts = {from_counts:.4f}   "
              f"({int((predicted & flagged).sum())} of {int(predicted.sum())} flags real)")
        assert abs(from_bayes - from_counts) < 1e-9, "precision disagrees with the count"


if __name__ == "__main__":
    main()
