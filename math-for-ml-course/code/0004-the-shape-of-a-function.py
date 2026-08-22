"""0004 - The shape of a function, and what a monotone change preserves.

The theorem this lesson proves says a strictly increasing transform moves every
number and no ordering. This program checks that on 1,308 real held-out rows:
AUC is unchanged to machine precision, accuracy at a fixed cutoff is not, and
transporting the cutoff through the same transform recovers it exactly.

AUC is computed twice, once from the rank definition and once by counting
concordant pairs, and the two are asserted equal.

Needs only numpy and pandas.
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "tickets.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/tickets.csv"


def load() -> pd.DataFrame:
    """Relative to this file so the repository works offline, URL so Colab works."""
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def auc_by_ranks(labels: np.ndarray, scores: np.ndarray) -> float:
    """The Mann-Whitney form: mean rank of the positives, shifted and scaled.

    Tied scores must share the AVERAGE of the ranks they span. Handing them
    ordinal ranks instead silently breaks the tie in whatever order the sort
    happened to produce, and the answer stops matching the pair-counting
    definition below - which is how this was caught.
    """
    order = np.argsort(scores, kind="mergesort")
    ranks = np.empty(len(scores), dtype=float)
    ranks[order] = np.arange(1, len(scores) + 1, dtype=float)

    ordered = scores[order]
    start = 0
    for stop in range(1, len(ordered) + 1):
        if stop == len(ordered) or ordered[stop] != ordered[start]:
            if stop - start > 1:                       # a run of tied scores
                ranks[order[start:stop]] = ranks[order[start:stop]].mean()
            start = stop

    n_pos = int(labels.sum())
    n_neg = len(labels) - n_pos
    return (ranks[labels == 1].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)


def auc_by_pairs(labels: np.ndarray, scores: np.ndarray) -> float:
    """The definition read literally: the share of positive-negative pairs
    the model puts the right way round. Quadratic, so only for a check."""
    positives = scores[labels == 1]
    negatives = scores[labels == 0]
    wins = (positives[:, None] > negatives[None, :]).sum()
    ties = (positives[:, None] == negatives[None, :]).sum()
    return (wins + 0.5 * ties) / (len(positives) * len(negatives))


def accuracy_at(labels: np.ndarray, scores: np.ndarray, cutoff: float) -> float:
    return float(((scores > cutoff).astype(int) == labels).mean())


def main() -> None:
    frame = load()
    held_out = frame[frame.row_split == "test"]
    labels = (held_out.label == "urgent").to_numpy().astype(int)
    scores = held_out.score_urgent.to_numpy()
    print(f"held-out rows: {len(labels)}, of which {labels.sum()} urgent")

    by_ranks = auc_by_ranks(labels, scores)
    by_pairs = auc_by_pairs(labels, scores)
    print(f"\nAUC from ranks           = {by_ranks:.6f}")
    print(f"AUC by counting pairs    = {by_pairs:.6f}")
    assert np.isclose(by_ranks, by_pairs, rtol=0, atol=1e-12), (
        "the two AUC definitions disagree - check the tie handling"
    )

    cutoff = 0.5
    before_auc = by_ranks
    before_acc = accuracy_at(labels, scores, cutoff)

    # g(s) = s^2 is strictly increasing on [0, 1].
    transformed = scores ** 2
    after_auc = auc_by_ranks(labels, transformed)
    after_acc = accuracy_at(labels, transformed, cutoff)

    print(f"\n                       before      after g(s) = s^2")
    print(f"  AUC                  {before_auc:.6f}    {after_auc:.6f}")
    print(f"  accuracy at {cutoff}      {before_acc:.6f}    {after_acc:.6f}")

    assert before_auc == after_auc, "a strictly increasing map must not move AUC"
    assert not np.isclose(before_acc, after_acc), (
        "expected accuracy at a FIXED cutoff to move; the dataset may have changed"
    )

    # The order really is untouched, checked directly rather than inferred.
    assert np.array_equal(np.argsort(scores, kind="mergesort"),
                          np.argsort(transformed, kind="mergesort")), "the order moved"
    print("\n  the ranking is identical, element for element")

    # The defect was the fixed cutoff, not the transform: transport it.
    transported = cutoff ** 2
    recovered = accuracy_at(labels, transformed, transported)
    print(f"  transporting the cutoff to g({cutoff}) = {transported} gives accuracy {recovered:.6f}")
    assert np.isclose(recovered, before_acc), "transporting the cutoff should recover the accuracy"

    # Clipping is non-decreasing and NOT strictly increasing, which is exactly
    # where the theorem's converse fails.
    clipped = np.minimum(scores, 0.6)
    moved = int((np.argmax(scores) != np.argmax(clipped)))
    tied = int((clipped == 0.6).sum())
    print(f"\n  clipping at 0.6 creates {tied} ties, and argmax {'moved' if moved else 'happened not to move'}")
    assert tied > 1, "clipping should create ties"

    print("\nall assertions passed")


if __name__ == "__main__":
    main()
