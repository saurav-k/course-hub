"""Lesson 0126 - precision against threshold, and precision against base rate.

Precision is a posterior, so it depends on three things: recall, the false
positive rate, and the base rate. Only the first two belong to the detector.

This program sweeps the detector threshold and, at every step, computes
precision twice - once by counting the confusion matrix and once from Bayes
using the measured recall, false positive rate and prior - and asserts they
agree. That is the whole claim of the page, checked at nine operating points
instead of the two the page works by hand.

It then holds the detector fixed and moves the base rate instead, by
subsampling the clean rows, so the reader can watch precision travel from 7
percent to 99 percent without the model changing at all.

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


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def precision_by_counting(positive: np.ndarray, predicted: np.ndarray) -> float:
    """Of the rows we flagged, what share were really positive."""
    flagged = int(predicted.sum())
    if flagged == 0:
        return float("nan")
    return float((predicted & positive).sum() / flagged)


def precision_from_bayes(prior: float, recall: float, false_positive_rate: float) -> float:
    """The same number as a posterior, from the three inputs Bayes needs."""
    numerator = recall * prior
    return float(numerator / (numerator + false_positive_rate * (1.0 - prior)))


def main() -> None:
    frame = load()
    positive = frame["flagged"].to_numpy(dtype=bool)
    score = frame["abuse_score"].to_numpy()
    negative = ~positive
    prior = float(positive.mean())

    print(f"base rate: {int(positive.sum())} abusive of {len(frame):,} "
          f"= {prior:.6f}")
    print(f"'always predict clean' accuracy = {1 - prior:.6f}, catching nothing\n")

    print("  thresh  recall     FPR   precision(count)  precision(Bayes)  alerts  real")
    for threshold in np.arange(0.30, 0.75, 0.05):
        predicted = score >= threshold
        recall = float(predicted[positive].mean())
        false_positive_rate = float(predicted[negative].mean())
        counted = precision_by_counting(positive, predicted)
        bayes = precision_from_bayes(prior, recall, false_positive_rate)
        assert abs(counted - bayes) < 1e-9, "precision disagrees with the count"
        print(
            f"    {threshold:.2f}  {recall:.4f}  {false_positive_rate:.4f}"
            f"        {counted:.4f}            {bayes:.4f}"
            f"   {int(predicted.sum()):5d}  {int((predicted & positive).sum()):4d}"
        )
    print("\n  the two precision columns agree at every threshold, so precision")
    print("  really is Bayes applied to a confusion matrix\n")

    # Hold the detector fixed at 0.5 and move only the prior, by keeping all the
    # abusive rows and subsampling the clean ones.
    predicted_at_half = score >= 0.5
    recall = float(predicted_at_half[positive].mean())
    false_positive_rate = float(predicted_at_half[negative].mean())
    print(f"detector fixed at threshold 0.50: recall {recall:.4f}, FPR {false_positive_rate:.4f}")
    print("  now move ONLY the base rate:\n")
    print("     base rate   precision   (the detector never changes)")
    for target in (0.001, prior, 0.01, 0.05, 0.20, 0.50):
        print(f"      {target:8.5f}    {precision_from_bayes(target, recall, false_positive_rate):.4f}")

    # And confirm that by actually resampling rather than only by formula.
    rng = np.random.default_rng(SEED)
    clean_index = np.flatnonzero(negative)
    positive_index = np.flatnonzero(positive)
    keep_clean = rng.choice(clean_index, size=len(positive_index) * 9, replace=False)
    subset = np.concatenate([positive_index, keep_clean])
    resampled_positive = positive[subset]
    resampled_predicted = predicted_at_half[subset]
    resampled_prior = float(resampled_positive.mean())
    resampled_precision = precision_by_counting(resampled_positive, resampled_predicted)

    # Bayes is exact, but it is only as good as the three numbers fed to it. The
    # 891 clean rows that survived the subsample have their own false positive
    # rate, and it is not the full population's. Use the subset's own inputs and
    # the identity closes exactly; use the full population's and it does not.
    resampled_recall = float(resampled_predicted[resampled_positive].mean())
    resampled_fpr = float(resampled_predicted[~resampled_positive].mean())

    print(f"\n  resampled to a base rate of {resampled_prior:.4f}, keeping every abusive")
    print(f"  row and 9 clean rows per abusive row:")
    print(f"      precision by counting                  = {resampled_precision:.4f}")
    print(f"      precision from Bayes, subset's own FPR = "
          f"{precision_from_bayes(resampled_prior, resampled_recall, resampled_fpr):.4f}")
    print(f"      precision from Bayes, full-file FPR    = "
          f"{precision_from_bayes(resampled_prior, recall, false_positive_rate):.4f}")
    assert abs(
        resampled_precision
        - precision_from_bayes(resampled_prior, resampled_recall, resampled_fpr)
    ) < 1e-9, "Bayes should close exactly on the subset's own inputs"
    print(f"\n  the subset's FPR is {resampled_fpr:.4f} against the full file's "
          f"{false_positive_rate:.4f}.")
    print("  Bayes is exact arithmetic on three inputs, and an estimated input")
    print("  moves the answer. That gap is estimation error, not a flaw in the theorem.")


if __name__ == "__main__":
    main()
