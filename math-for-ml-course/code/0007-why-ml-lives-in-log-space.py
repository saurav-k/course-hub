"""0007 - Why machine learning lives in log space.

Fits a Laplace-smoothed naive Bayes on the training tickets and scores the test
tickets twice, naively and in log space, so the failure is measured rather than
described.

Two populations matter and they fail differently:

  * both class scores underflow to 0.0, so the classifier cannot decide at all;
  * exactly one underflows, so the decision is forced by a floating-point
    artefact rather than by evidence. That is the silent failure, and on this
    data it is several times more common than the loud one.

Needs only numpy and pandas.
"""

import numpy as np
import pandas as pd

LOCAL = "../datasets/tickets.csv"
REMOTE = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/tickets.csv"
CLASSES = ["urgent", "normal"]


def load() -> pd.DataFrame:
    try:
        return pd.read_csv(LOCAL)
    except FileNotFoundError:
        return pd.read_csv(REMOTE)


def fit(train: pd.DataFrame, vocab: list[str]) -> tuple[dict, dict]:
    """Laplace-smoothed token probabilities and class priors."""
    index = {token: j for j, token in enumerate(vocab)}
    counts = {c: np.ones(len(vocab)) for c in CLASSES}
    for tokens, label in zip(train["tokens"], train["label"]):
        for token in tokens.split():
            counts[label][index[token]] += 1.0
    probabilities = {c: counts[c] / counts[c].sum() for c in CLASSES}
    priors = {c: float((train["label"] == c).mean()) for c in CLASSES}
    return probabilities, priors


def main() -> None:
    frame = load()
    train = frame[frame.row_split == "train"]
    test = frame[frame.row_split == "test"]
    vocab = sorted({t for tokens in frame["tokens"] for t in tokens.split()})
    index = {token: j for j, token in enumerate(vocab)}
    probabilities, priors = fit(train, vocab)

    print(f"fitted on {len(train):,} tickets, vocabulary of {len(vocab)} tokens")
    smallest = min(p.min() for p in probabilities.values())
    print(f"smallest per-token probability: {smallest:.6f}")
    print(f"float64 underflows to zero below an exponent of about -746")
    print(f"so a ticket of about {int(-745 / np.log(smallest))} such tokens is already at the floor\n")

    both_zero = one_zero = 0
    naive_correct = log_correct = 0
    shortest_underflow = None
    longest_survivor = 0

    for tokens, truth, n_tokens in zip(test["tokens"], test["label"], test["n_tokens"]):
        ids = [index[t] for t in tokens.split() if t in index]

        naive = {c: priors[c] * float(np.prod(probabilities[c][ids])) for c in CLASSES}
        logs = {c: float(np.log(priors[c]) + np.log(probabilities[c][ids]).sum()) for c in CLASSES}

        zeros = sum(1 for c in CLASSES if naive[c] == 0.0)
        if zeros == 2:
            both_zero += 1
        elif zeros == 1:
            one_zero += 1

        if zeros:
            shortest_underflow = n_tokens if shortest_underflow is None else min(shortest_underflow, n_tokens)
        else:
            longest_survivor = max(longest_survivor, n_tokens)

        # A tie in the naive path is undecidable; call it wrong rather than guess.
        naive_pick = max(CLASSES, key=lambda c: naive[c]) if naive[CLASSES[0]] != naive[CLASSES[1]] else None
        log_pick = max(CLASSES, key=lambda c: logs[c])
        naive_correct += int(naive_pick == truth)
        log_correct += int(log_pick == truth)

        assert np.isfinite(logs[CLASSES[0]]) and np.isfinite(logs[CLASSES[1]]), (
            "a log-space score was not finite"
        )

    n = len(test)
    print(f"scored {n:,} held-out tickets\n")
    print(f"  both class scores underflow to 0.0   : {both_zero:>4}  ({both_zero / n:.2%})")
    print(f"    the classifier cannot decide at all - a loud failure")
    print(f"  exactly one underflows               : {one_zero:>4}  ({one_zero / n:.2%})")
    print(f"    the decision is forced by an artefact - a SILENT failure")
    print(f"  affected in total                    : {both_zero + one_zero:>4}  ({(both_zero + one_zero) / n:.2%})")
    print(f"\n  shortest ticket that underflows: {shortest_underflow} tokens")
    print(f"  longest ticket that survives   : {longest_survivor} tokens")
    print(f"  so the cliff is not a single length: it depends on which tokens are in the ticket")

    print(f"\n  accuracy, naive product : {naive_correct / n:.4f}")
    print(f"  accuracy, log space     : {log_correct / n:.4f}")
    assert both_zero + one_zero > 0, "expected some underflow on this dataset"
    assert log_correct >= naive_correct, "log space should never be worse"
    assert one_zero > both_zero, "on this data the silent failure is the common one"

    # The two paths agree exactly where the naive one has not broken.
    print("\n  where the naive product survives, the two paths agree exactly:")
    agreed = checked = 0
    for tokens in test["tokens"].head(400):
        ids = [index[t] for t in tokens.split() if t in index]
        naive = {c: priors[c] * float(np.prod(probabilities[c][ids])) for c in CLASSES}
        if min(naive.values()) == 0.0:
            continue
        logs = {c: float(np.log(priors[c]) + np.log(probabilities[c][ids]).sum()) for c in CLASSES}
        checked += 1
        agreed += int(max(CLASSES, key=lambda c: naive[c]) == max(CLASSES, key=lambda c: logs[c]))
    print(f"    {agreed} of {checked} checked, which is the monotonicity argument holding in practice")
    assert agreed == checked, "the two paths disagreed where both were computable"

    print("\n  NOTE: the two class vocabularies barely overlap by construction, so this")
    print("  accuracy is a property of the generator and not evidence about real classifiers.")
    print("\nall assertions passed")


if __name__ == "__main__":
    main()
