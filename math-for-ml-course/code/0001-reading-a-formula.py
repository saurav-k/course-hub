"""0001 - Reading a formula: indices, sigma, and pi.

A sigma is a for-loop with an accumulator. This program computes one quantity
three ways - an explicit double loop, a NumPy expression, and a Pandas
one-liner - and asserts all three agree, so that the notation, the loop and the
library are visibly the same thing.

Needs only numpy and pandas. Run it anywhere:

    python3 0001-reading-a-formula.py
"""

import numpy as np
import pandas as pd

LOCAL = "../datasets/tickets.csv"
REMOTE = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/tickets.csv"


def load() -> pd.DataFrame:
    """Relative path first so the repository works offline, URL so Colab works."""
    try:
        return pd.read_csv(LOCAL)
    except FileNotFoundError:
        return pd.read_csv(REMOTE)


def feature_matrix(frame: pd.DataFrame, vocab: list[str]) -> np.ndarray:
    """Rows are tickets and columns are features, which is this course's orientation."""
    index = {token: j for j, token in enumerate(vocab)}
    matrix = np.zeros((len(frame), len(vocab)))
    for i, tokens in enumerate(frame["tokens"]):
        for token in tokens.split():
            matrix[i, index[token]] += 1.0
    return matrix


def sum_of_squares_by_loop(matrix: np.ndarray) -> float:
    """The formula read literally: two nested loops and one running total."""
    total = 0.0
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            total += matrix[i, j] ** 2
    return total


def main() -> None:
    frame = load()
    batch = frame.head(32)
    vocab = sorted({t for tokens in frame["tokens"] for t in tokens.split()})
    matrix = feature_matrix(batch, vocab)

    m, d = matrix.shape
    print(f"minibatch: m = {m} tickets, d = {d} features")
    print(f"the double sum has m x d = {m * d} scalar terms")

    by_loop = sum_of_squares_by_loop(matrix)
    by_numpy = float((matrix ** 2).sum())
    by_pandas = float((pd.DataFrame(matrix) ** 2).to_numpy().sum())

    print(f"  explicit double loop : {by_loop:.4f}")
    print(f"  NumPy                : {by_numpy:.4f}")
    print(f"  Pandas               : {by_pandas:.4f}")
    assert np.isclose(by_loop, by_numpy), "the loop and NumPy disagree"
    assert np.isclose(by_loop, by_pandas), "the loop and Pandas disagree"

    # The index is bound: renaming it cannot change the number.
    renamed = sum(matrix[k, q] ** 2 for k in range(m) for q in range(d))
    assert np.isclose(by_loop, renamed), "renaming a bound index changed the answer"
    print("  renaming i to k and j to q: unchanged, because an index is bound")

    # The sample index and the feature index are different things.
    ticket_2 = matrix[1, :]
    feature_3 = matrix[:, 2]
    print(f"\nx^(2) is one ticket  : shape {ticket_2.shape}, a vector of {d} features")
    print(f"x_3  is one feature  : shape {feature_3.shape}, one number per ticket")
    assert ticket_2.shape != feature_3.shape or m == d

    # Empty sum is 0 and empty product is 1, which is why a model with no
    # features predicts the prior rather than zero.
    print(f"\nempty sum     = {float(np.sum(np.array([]))):.1f}")
    print(f"empty product = {float(np.prod(np.array([]))):.1f}")
    assert np.sum(np.array([])) == 0.0
    assert np.prod(np.array([])) == 1.0

    print("\nall assertions passed")


if __name__ == "__main__":
    main()
