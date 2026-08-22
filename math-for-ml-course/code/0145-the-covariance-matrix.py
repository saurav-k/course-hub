"""The covariance matrix, and why its eigenvectors are the shape of the data.

Lesson: The covariance matrix (0083).

    python3 0806-covariance-matrix.py

What it checks twice:

  1. Sigma built entry by entry from pairwise covariances, against the one-line
     matrix form (1/(n-1)) Xc^T Xc on the centred data matrix. Same matrix.
  2. Positive semi-definiteness, checked the way the proof reads: z^T Sigma z is
     the variance of the projected data z^T x, for a thousand random z. Never
     negative, and equal to the directly measured projection variance.
  3. trace(Sigma) equals the sum of the eigenvalues, so total variance is
     conserved and the eigendecomposition only decides how it is split.
  4. The standardisation trap: eigenvalues of the covariance matrix against
     eigenvalues of the correlation matrix, on the same columns.
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
COLUMNS = ["prompt_tokens", "output_tokens", "queue_depth", "gpu_util", "latency_ms"]


def load() -> pd.DataFrame:
    """Read the committed dataset, falling back to the published URL.

    The path is resolved from this file rather than the working directory, so the
    program runs from anywhere. The URL fallback is what lets it be pasted into
    Colab or a notebook with no checkout at all.
    """
    return pd.read_csv(DATA) if DATA.exists() else pd.read_csv(URL)


def main() -> None:
    frame = load()
    matrix = frame[COLUMNS].to_numpy(dtype=float)
    n, d = matrix.shape
    print(f"data matrix: {n:,} rows x {d} columns\n")

    print("1. Sigma two ways")
    entrywise = np.empty((d, d))
    for i in range(d):
        for j in range(d):
            a, b = matrix[:, i], matrix[:, j]
            entrywise[i, j] = ((a - a.mean()) * (b - b.mean())).sum() / (n - 1)
    centred = matrix - matrix.mean(axis=0)
    matrix_form = centred.T @ centred / (n - 1)
    print("   entry by entry, one covariance at a time:")
    print(pd.DataFrame(entrywise, index=COLUMNS, columns=COLUMNS).round(3))
    assert np.allclose(entrywise, matrix_form), "the two constructions disagree"
    assert np.allclose(entrywise, np.cov(matrix, rowvar=False, ddof=1))
    print("\n   (1/(n-1)) Xc^T Xc gives the identical matrix, as does numpy.cov.")
    print("   The diagonal is the variances; everything off it is a covariance.")

    print("\n2. Positive semi-definiteness, checked as the proof reads")
    print("   The claim is z^T Sigma z = Var(z^T x), so it cannot be negative.")
    rng = np.random.default_rng(20260826)
    worst = np.inf
    largest_gap = 0.0
    for _ in range(1_000):
        z = rng.normal(size=d)
        quadratic_form = float(z @ matrix_form @ z)
        projected_variance = float(np.var(centred @ z, ddof=1))
        worst = min(worst, quadratic_form)
        largest_gap = max(largest_gap, abs(quadratic_form - projected_variance))
    print(f"   smallest z^T Sigma z over 1,000 random directions   {worst:,.4f}")
    print(f"   largest gap to the measured projection variance     {largest_gap:.2e}")
    assert worst >= 0.0 and largest_gap < 1e-6
    print("   Never negative, and always exactly the projected variance. The")
    print("   quadratic form is not LIKE a variance, it IS one.")
    eigenvalues = np.linalg.eigvalsh(matrix_form)
    print(f"   smallest eigenvalue                                 {eigenvalues.min():,.6f}")
    print("   (Non-negative eigenvalues say the same thing, one direction at a time.)")

    print("\n3. Total variance is conserved")
    values, vectors = np.linalg.eigh(matrix_form)
    order = np.argsort(values)[::-1]
    values, vectors = values[order], vectors[:, order]
    print(f"   trace(Sigma)              {np.trace(matrix_form):,.6f}")
    print(f"   sum of the eigenvalues    {values.sum():,.6f}")
    assert np.isclose(np.trace(matrix_form), values.sum())
    print("   Identical. Rotating to the eigenvector basis moves variance between")
    print("   directions and never creates or destroys any.")

    print("\n4. The standardisation trap: same columns, two answers")
    correlation = np.corrcoef(matrix, rowvar=False)
    from_cov = np.sort(np.linalg.eigvalsh(matrix_form))[::-1]
    from_corr = np.sort(np.linalg.eigvalsh(correlation))[::-1]
    table = pd.DataFrame(
        {
            "on covariance": from_cov / from_cov.sum(),
            "on correlation": from_corr / from_corr.sum(),
        },
        index=[f"PC{i + 1}" for i in range(d)],
    )
    print((table * 100).round(2).to_string(float_format=lambda v: f"{v:6.2f}%"))
    print("\n   Column variances, which is where the disagreement comes from:")
    for name, variance in zip(COLUMNS, np.diag(matrix_form)):
        print(f"     {name:<16}{variance:>16,.3f}")
    print(
        f"\n   PC1 carries {table.iloc[0, 0]:.1%} on the covariance matrix and only "
        f"{table.iloc[0, 1]:.1%}\n"
        "   on the correlation matrix. The covariance answer is dominated by\n"
        "   whichever column happens to have the largest raw variance, and here\n"
        "   that is a units accident rather than a fact about the data.\n"
        "   Neither answer is wrong and neither is the default. Columns in mixed\n"
        "   units need the correlation matrix; the choice has to be made on purpose."
    )


if __name__ == "__main__":
    main()
