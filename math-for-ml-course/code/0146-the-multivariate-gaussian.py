"""The multivariate Gaussian: density, Mahalanobis distance, whitening.

Lesson: The multivariate Gaussian.

    python3 0807-multivariate-gaussian.py

What it checks twice:

  1. The density evaluated from the formula, against the same density built as a
     product of independent standard normals after whitening. If x = mu + Bz is
     right, those two must agree, and the Jacobian factor det(B) is what makes
     them agree.
  2. Mahalanobis distance from Sigma^-1, against Euclidean distance in the
     whitened coordinates. Same number, two descriptions.
  3. Whitening: B^-1 (x - mu) must have mean 0 and covariance I, measured.
  4. Where Euclidean and Mahalanobis DISAGREE about which point is stranger,
     found in the real data rather than constructed.

The columns are logged first, because latency and token counts are lognormal and
the Gaussian is a claim about the log scale here. Fitting a Gaussian to the raw
columns would be the error the page warns about.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "inference_runs.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/inference_runs.csv"
)
COLUMNS = ["prompt_tokens", "output_tokens", "latency_ms"]


def load() -> pd.DataFrame:
    """Read the committed dataset, falling back to the published URL.

    The path is resolved from this file rather than the working directory, so the
    program runs from anywhere. The URL fallback is what lets it be pasted into
    Colab or a notebook with no checkout at all.
    """
    return pd.read_csv(DATA) if DATA.exists() else pd.read_csv(URL)


def log_density(x: np.ndarray, mu: np.ndarray, sigma: np.ndarray) -> np.ndarray:
    """log p(x; mu, Sigma), computed from the definition.

    In logs because the density of a 3-dimensional Gaussian underflows to zero in
    the tails, and a page that prints 0.0 for a rare point has taught nothing.
    """
    d = len(mu)
    delta = x - mu
    inverse = np.linalg.inv(sigma)
    sign, logdet = np.linalg.slogdet(sigma)
    assert sign > 0, "Sigma must be positive definite"
    quadratic = np.einsum("ij,jk,ik->i", delta, inverse, delta)
    return -0.5 * (d * np.log(2 * np.pi) + logdet + quadratic)


def main() -> None:
    frame = load()
    logged = np.log(frame[COLUMNS].to_numpy(dtype=float))
    n, d = logged.shape
    mu = logged.mean(axis=0)
    sigma = np.cov(logged, rowvar=False, ddof=1)
    print(f"fitted to log({', '.join(COLUMNS)}) on {n:,} rows\n")
    print("mu     ", np.round(mu, 4))
    print("Sigma\n", pd.DataFrame(sigma, index=COLUMNS, columns=COLUMNS).round(5))
    print(f"\ndet(Sigma) = {np.linalg.det(sigma):.8f}")

    # Cholesky gives the B with B B^T = Sigma. Any such B works; this one is
    # triangular, which makes the inverse cheap and the whitening explicit.
    B = np.linalg.cholesky(sigma)
    assert np.allclose(B @ B.T, sigma), "Cholesky factor is wrong"
    print("\nB from the Cholesky factorisation, so that B B^T = Sigma:")
    print(np.round(B, 5))

    print("\n1. The density two ways, on ten real rows")
    sample = logged[:10]
    direct = log_density(sample, mu, sigma)
    # Route two: whiten, evaluate a product of independent standard normals, then
    # correct by the Jacobian of the linear map, which is 1/|det B|.
    whitened = np.linalg.solve(B, (sample - mu).T).T
    standard = -0.5 * (d * np.log(2 * np.pi) + (whitened**2).sum(axis=1))
    via_whitening = standard - np.log(np.abs(np.linalg.det(B)))
    print(f"   {'from the formula':>20}{'via whitening':>18}{'gap':>12}")
    for a, b in zip(direct, via_whitening):
        print(f"   {a:>20.10f}{b:>18.10f}{abs(a - b):>12.2e}")
    assert np.allclose(direct, via_whitening), "the two routes disagree"
    print("   Identical. x = mu + Bz is not an analogy, it is the density's shape.")

    print("\n2. Mahalanobis distance two ways")
    all_whitened = np.linalg.solve(B, (logged - mu).T).T
    from_inverse = np.sqrt(
        np.einsum("ij,jk,ik->i", logged - mu, np.linalg.inv(sigma), logged - mu)
    )
    from_whitened = np.linalg.norm(all_whitened, axis=1)
    assert np.allclose(from_inverse, from_whitened)
    print(f"   largest gap over all {n:,} rows   {np.abs(from_inverse - from_whitened).max():.2e}")
    print("   Mahalanobis distance is plain Euclidean distance, measured after")
    print("   the covariance has been divided out.")

    print("\n3. Whitening does what it claims")
    print(f"   mean of the whitened data   {np.round(all_whitened.mean(axis=0), 10)}")
    print("   covariance of the whitened data")
    print(np.round(np.cov(all_whitened, rowvar=False, ddof=1), 10))
    assert np.allclose(np.cov(all_whitened, rowvar=False, ddof=1), np.eye(d), atol=1e-9)
    print("   Mean zero and covariance the identity, to ten decimal places.")

    print("\n4. Where the two distances disagree")
    euclidean = np.linalg.norm(logged - mu, axis=1)
    e_rank = euclidean.argsort().argsort()
    m_rank = from_inverse.argsort().argsort()
    disagreement = m_rank - e_rank
    worst = int(np.argmax(disagreement))
    tame = int(np.argmin(disagreement))
    print(f"   {'':<6}{'euclidean':>12}{'e-rank':>9}{'mahalanobis':>14}{'m-rank':>9}")
    for label, index in (("row A", worst), ("row B", tame)):
        print(
            f"   {label:<6}{euclidean[index]:>12.4f}{e_rank[index]:>9,}"
            f"{from_inverse[index]:>14.4f}{m_rank[index]:>9,}"
        )
    print(
        f"\n   Row A is only the {e_rank[worst]:,}th most distant point by Euclidean\n"
        f"   distance but the {m_rank[worst]:,}th by Mahalanobis, and row B moves the\n"
        "   other way. Euclidean distance treats every direction as equal. The\n"
        "   covariance matrix knows the cloud is long in some directions and thin\n"
        "   in others, and a point that is ordinary along the long axis can be\n"
        "   extraordinary across the thin one."
    )


if __name__ == "__main__":
    main()
