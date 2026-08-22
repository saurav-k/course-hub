"""0003 - A model is a function, and depth is composition.

Builds a 45-32-16-3 forward pass over tickets.csv with NumPy only, printing the
shape after every layer so the contract f : A -> B is visible at run time,
counting parameters from the shapes alone, and showing which functions have an
inverse and which do not.

Needs only numpy and pandas.
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "tickets.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/tickets.csv"
WIDTHS = [45, 32, 16, 3]


def load() -> pd.DataFrame:
    """Relative to this file so the repository works offline, URL so Colab works."""
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def feature_matrix(frame: pd.DataFrame, vocab: list[str]) -> np.ndarray:
    index = {token: j for j, token in enumerate(vocab)}
    matrix = np.zeros((len(frame), len(vocab)))
    for i, tokens in enumerate(frame["tokens"]):
        for token in tokens.split():
            matrix[i, index[token]] += 1.0
    return matrix


def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(0.0, x)


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def logit(p: np.ndarray) -> np.ndarray:
    """The inverse of sigmoid, defined only on the open interval (0, 1)."""
    return np.log(p / (1.0 - p))


def main() -> None:
    frame = load().head(256)
    vocab = sorted({t for tokens in load()["tokens"] for t in tokens.split()})
    x = feature_matrix(frame, vocab)
    assert x.shape[1] == WIDTHS[0], "the data does not match the declared domain"

    rng = np.random.default_rng(3)
    layers = [
        (rng.normal(0, 0.1, (WIDTHS[i], WIDTHS[i + 1])), np.zeros(WIDTHS[i + 1]))
        for i in range(len(WIDTHS) - 1)
    ]

    print(f"f : R^{WIDTHS[0]} -> R^{WIDTHS[-1]}, composed of {len(layers)} layers\n")
    activation = x
    print(f"  input               shape {activation.shape}")
    for n, (weight, bias) in enumerate(layers, start=1):
        before = activation.shape[1]
        assert before == weight.shape[0], (
            f"layer f{n} declares domain R^{weight.shape[0]} and was handed R^{before}"
        )
        activation = activation @ weight + bias
        if n < len(layers):
            activation = relu(activation)
        print(f"  after f{n} : R^{weight.shape[0]} -> R^{weight.shape[1]}   shape {activation.shape}")

    assert activation.shape[1] == WIDTHS[-1], "the composition missed its codomain"
    print(f"\n  the codomain of each layer is the domain of the next: that is what composes means")

    # Parameters are a fact about the shapes alone, before any training.
    counts = [w.size + b.size for w, b in layers]
    for n, (count, (w, _)) in enumerate(zip(counts, layers), start=1):
        print(f"  f{n}: {w.shape[0]} x {w.shape[1]} + {w.shape[1]} = {count:,} parameters")
    print(f"  total: {sum(counts):,}")
    assert sum(counts) == sum(WIDTHS[i] * WIDTHS[i + 1] + WIDTHS[i + 1] for i in range(len(WIDTHS) - 1))

    # Composition does not commute: the reversed chain is not even defined.
    first, second = layers[0][0], layers[1][0]
    try:
        _ = np.zeros((1, second.shape[1])) @ first
        raise AssertionError("the reversed composition should not have been defined")
    except ValueError:
        print("\n  f1 . f2 is undefined: composition does not commute")

    # Inverses: sigmoid and logit round-trip, ReLU cannot.
    sample = np.array([-3.0, -0.5, 0.0, 0.5, 3.0])
    round_trip = logit(sigmoid(sample))
    print(f"\n  logit(sigmoid(x)) recovers x: max error {np.abs(round_trip - sample).max():.2e}")
    assert np.allclose(round_trip, sample), "sigmoid and logit are not inverses"

    # The image is the OPEN interval (0, 1), so mathematically sigmoid never
    # reaches either end. Floating point disagrees, and the gap between those
    # two facts is where log(1 - yhat) turns into -inf in a real training run.
    print(f"\n  sigmoid(1.0)  = {sigmoid(np.array([1.0]))[0]:.12f}   strictly inside (0, 1)")
    assert 0.0 < sigmoid(np.array([1.0]))[0] < 1.0

    for dtype, name in ((np.float64, "float64"), (np.float32, "float32")):
        low, high = 0.0, 100.0
        for _ in range(200):
            mid = (low + high) / 2
            value = dtype(1) / (dtype(1) + np.exp(-dtype(mid)))
            if value >= dtype(1.0):
                high = mid
            else:
                low = mid
        print(f"  in {name}, sigmoid rounds to exactly 1.0 from x = {high:.3f} upward")
    assert sigmoid(np.array([37.0]))[0] == 1.0, "expected float64 to round here"
    print("  so the mathematics says never and the arithmetic says from about 36.7")
    print("  knowing which of those two facts you are looking at is the whole skill")

    collided = relu(np.array([-3.0, -1.0, -0.25]))
    print(f"  relu maps -3, -1 and -0.25 all to {collided.tolist()}: not one-to-one, so no inverse")
    assert len(set(collided.tolist())) == 1

    print("\nall assertions passed")


if __name__ == "__main__":
    main()
