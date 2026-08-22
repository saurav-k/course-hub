"""0409 - Low-rank approximation and Eckart-Young.

Measures the truncation error two ways at every k: by building A_k explicitly
and measuring the residual, and by reading it off the discarded spectrum alone.
The theorem says these must be equal. They are, to twelve decimals.

Needs numpy and pandas only:  python3 0409-low-rank-approximation.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd

LOCAL = "../datasets/spectra.csv"
REMOTE = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/spectra.csv"
)


def load_channels() -> np.ndarray:
    """Read the dataset from beside the course checkout, else over the network.

    Rows are samples and columns are features, the course convention (D7).
    """
    try:
        frame = pd.read_csv(LOCAL)
    except (FileNotFoundError, OSError):
        frame = pd.read_csv(REMOTE)
    return frame.drop(columns="sample_id").to_numpy(dtype=float)


def centred(values: np.ndarray) -> np.ndarray:
    """Subtract the per-column mean. Covariance is defined on deviations."""
    return values - values.mean(axis=0)

def truncate(left: np.ndarray, singular: np.ndarray, right: np.ndarray, k: int) -> np.ndarray:
    """A_k as the sum of the first k rank-one pieces sigma_i u_i v_i^T."""
    return (left[:, :k] * singular[:k]) @ right[:k]


def main() -> None:
    data = centred(load_channels())
    rows, cols = data.shape
    left, singular, right = np.linalg.svd(data, full_matrices=False)

    print(f"centred data matrix: {rows} x {cols} = {rows * cols:,} numbers")
    print("singular values, first eight:")
    print("  " + "  ".join(f"{s:8.4f}" for s in singular[:8]))

    print("\n  k | measured ||A-Ak||_F | sqrt(tail sq) | measured ||A-Ak||_2 |  sigma_k+1")
    print("  " + "-" * 76)
    for k in range(1, 9):
        approximation = truncate(left, singular, right, k)
        residual = data - approximation

        measured_frobenius = float(np.linalg.norm(residual, "fro"))
        theory_frobenius = float(np.sqrt((singular[k:] ** 2).sum()))
        measured_spectral = float(np.linalg.norm(residual, 2))
        theory_spectral = float(singular[k])

        print(f"  {k} | {measured_frobenius:19.12f} | {theory_frobenius:13.6f} | "
              f"{measured_spectral:19.12f} | {theory_spectral:11.6f}")

        assert np.isclose(measured_frobenius, theory_frobenius, rtol=1e-10), "Frobenius identity failed"
        assert np.isclose(measured_spectral, theory_spectral, rtol=1e-10), "spectral identity failed"

    print("\nboth identities hold at every k: the error IS the discarded spectrum")

    total = float((singular ** 2).sum())
    print("\n  k | energy kept | numbers stored |  vs full  | ratio")
    print("  " + "-" * 58)
    for k in (1, 2, 3, 4, 5, 6):
        kept = float((singular[:k] ** 2).sum()) / total
        stored = k * (rows + cols + 1)
        print(f"  {k} | {kept * 100:10.4f}% | {stored:14,} | {rows * cols:9,} | "
              f"{rows * cols / stored:5.2f}x")

    # The elbow at four is not discovered, it was built in. Say so, and show the
    # numerical signature of it: the discarded values are a flat noise floor.
    floor = singular[4:]
    print(f"\nsigma_5 .. sigma_24: mean {floor.mean():.4f}, "
          f"standard deviation {floor.std():.4f}")
    print(f"cliff ratio sigma_4 / sigma_5 = {singular[3] / singular[4]:.4f}")
    print("A flat tail is the signature of independent noise, and it is why the")
    print("elbow sits at four. This dataset was GENERATED with four components,")
    print("so the elbow is designed in, not evidence about the world.")

    # What this program has not shown.
    print("\nNOT shown here: that any of this survives missing entries. Eckart-Young")
    print("assumes a fully observed matrix. Filling blanks in does not recover it.")


if __name__ == "__main__":
    main()
