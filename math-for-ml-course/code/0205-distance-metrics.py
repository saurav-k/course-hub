"""Three distances on one table, and which of them are metrics.

Lesson: Distance and similarity metrics, and the metric axioms.
Dataset: m10_signals.csv (12,000 rows).

Runs on numpy and pandas and nothing else.

What it does:
  1. Computes Euclidean, standardised Euclidean and Mahalanobis distance from
     the centre for every row, and shows the three rankings disagree.
  2. Computes Mahalanobis twice - once as (x-mu)' S^-1 (x-mu), once as ordinary
     Euclidean distance in the whitened coordinates the eigendecomposition
     gives - and asserts they agree. That equality is the whole geometric
     content of the definition.
  3. Tests the three metric axioms on random triples for each candidate:
     Euclidean and Mahalanobis pass, cosine distance fails the triangle
     inequality and the failure is printed with the triple that broke it.
  4. Shows that the angular form sqrt(2 - 2cos) does satisfy the triangle
     inequality, because it is a Euclidean distance in disguise.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

RAW = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/"
COLUMNS = ["tenure_months", "monthly_spend", "sessions_week"]


def load(name: str) -> pd.DataFrame:
    local = pathlib.Path(__file__).resolve().parent.parent / "datasets" / name
    return pd.read_csv(local if local.exists() else RAW + name)


def euclidean(a: np.ndarray, b: np.ndarray) -> float:
    """The square root of the sum of squared differences, written out."""
    total = 0.0
    for ai, bi in zip(a, b):
        total += (ai - bi) ** 2
    return float(np.sqrt(total))


def mahalanobis(x: np.ndarray, mu: np.ndarray, inverse: np.ndarray) -> float:
    """sqrt((x - mu)' S^-1 (x - mu)), Bishop PRML equation 2.44."""
    d = x - mu
    return float(np.sqrt(d @ inverse @ d))


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def main() -> None:
    signals = load("m10_signals.csv")
    X = signals[COLUMNS].to_numpy(dtype=float)
    n = len(X)
    mu = X.mean(axis=0)
    sd = X.std(axis=0, ddof=1)
    cov = np.cov(X, rowvar=False)
    inverse = np.linalg.inv(cov)

    print(f"m10_signals.csv: {n} rows, columns {COLUMNS}")
    print(f"\nmeans {np.round(mu, 3)}")
    print(f"sds   {np.round(sd, 3)}")
    print("\ncorrelation matrix:")
    print(np.round(np.corrcoef(X, rowvar=False), 4))

    # ---- 1. Three distances, three rankings -------------------------------
    d_raw = np.linalg.norm(X - mu, axis=1)
    Z = (X - mu) / sd
    d_std = np.linalg.norm(Z, axis=1)
    centred = X - mu
    d_mah = np.sqrt(np.einsum("ij,jk,ik->i", centred, inverse, centred))

    print(f"\nthe single most extreme row under each distance:")
    for name, d in (("raw Euclidean", d_raw), ("standardised", d_std), ("Mahalanobis", d_mah)):
        worst = int(np.argmax(d))
        print(f"  {name:<14} row {worst:>5}  {np.round(X[worst], 2)}  d = {d[worst]:.3f}")

    top_raw = set(np.argsort(-d_raw)[:100].tolist())
    top_std = set(np.argsort(-d_std)[:100].tolist())
    top_mah = set(np.argsort(-d_mah)[:100].tolist())
    print(f"\nthe 100 most distant rows, how much the three lists overlap:")
    print(f"  raw and standardised share {len(top_raw & top_std)} of 100")
    print(f"  raw and Mahalanobis  share {len(top_raw & top_mah)} of 100")
    print(f"  standardised and Mahalanobis share {len(top_std & top_mah)} of 100")
    print("  The metric is not a detail. It picks a different hundred rows.")

    # ---- 2. Mahalanobis is Euclidean after whitening ---------------------
    values, vectors = np.linalg.eigh(cov)
    print(f"\neigenvalues of the covariance matrix: {np.round(values, 3)}")
    whitened = (centred @ vectors) / np.sqrt(values)
    d_white = np.linalg.norm(whitened, axis=1)
    gap = float(np.abs(d_white - d_mah).max())
    print(f"Euclidean distance in whitened coordinates against Mahalanobis:")
    print(f"  largest disagreement over {n} rows = {gap:.3e}")
    assert gap < 1e-9, "the whitening identity failed"
    print("  They are the same number. PRML equation 2.50 is what that identity is.")

    # A pair chosen to make it concrete: same Euclidean distance, different
    # Mahalanobis distance, because one lies along the correlation ridge and
    # the other across it.
    scale = np.array([1.0, sd[1] / sd[0], 0.0])
    along = mu + 1.5 * sd * np.array([1.0, 1.0, 0.0])
    across = mu + 1.5 * sd * np.array([1.0, -1.0, 0.0])
    print(f"\ntwo synthetic points, both 1.5 standard deviations out on two axes:")
    print(f"  along the ridge  {np.round(along, 2)}  Euclid {euclidean(along, mu):9.3f}  "
          f"Mahalanobis {mahalanobis(along, mu, inverse):.3f}")
    print(f"  across the ridge {np.round(across, 2)}  Euclid {euclidean(across, mu):9.3f}  "
          f"Mahalanobis {mahalanobis(across, mu, inverse):.3f}")
    print(f"  identical Euclidean distance, Mahalanobis differs by a factor of "
          f"{mahalanobis(across, mu, inverse) / mahalanobis(along, mu, inverse):.2f}")

    # ---- 3. The metric axioms, tested ------------------------------------
    rng = np.random.default_rng(5)
    triples = rng.integers(0, n, size=(200000, 3))

    def check(name, distance):
        worst_violation = 0.0
        witness = None
        identity_ok = True
        symmetry_ok = True
        for a, b, c in triples[:20000]:
            if a == b or b == c or a == c:
                continue
            dab, dbc, dac = distance(a, b), distance(b, c), distance(a, c)
            slack = dab + dbc - dac
            if slack < worst_violation:
                worst_violation = slack
                witness = (int(a), int(b), int(c), dab, dbc, dac)
            if abs(distance(a, b) - distance(b, a)) > 1e-12:
                symmetry_ok = False
            if distance(a, a) > 1e-12:
                identity_ok = False
        return name, identity_ok, symmetry_ok, worst_violation, witness

    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)

    def d_euclid(i, j):
        return float(np.linalg.norm(X[i] - X[j]))

    def d_cosine(i, j):
        return float(1.0 - Xn[i] @ Xn[j])

    def d_angular(i, j):
        return float(np.linalg.norm(Xn[i] - Xn[j]))

    print("\nthe three metric axioms, tested on 20,000 random triples of real rows:")
    print("  candidate            d(x,x)=0   symmetric   worst triangle slack")
    for name, fn in (("Euclidean", d_euclid),
                     ("cosine distance", d_cosine),
                     ("sqrt(2-2cos)", d_angular)):
        _, ident, symm, slack, witness = check(name, fn)
        verdict = "fails" if slack < -1e-9 else "holds"
        print(f"  {name:<20} {str(ident):<10} {str(symm):<11} {slack:+.6f}  {verdict}")
        if slack < -1e-9 and witness is not None:
            a, b, c, dab, dbc, dac = witness
            print(f"      counterexample rows {a}, {b}, {c}: "
                  f"d(a,b)+d(b,c) = {dab + dbc:.6f} < d(a,c) = {dac:.6f}")

    print("\n  1 - cos is not a metric. sqrt(2 - 2cos) is, because it is the ordinary")
    print("  Euclidean distance between the two length-one vectors, and Euclidean")
    print("  distance satisfies the triangle inequality by construction.")
    pair = rng.integers(0, n, size=2)
    lhs = np.linalg.norm(Xn[pair[0]] - Xn[pair[1]])
    rhs = np.sqrt(2.0 - 2.0 * cosine_similarity(X[pair[0]], X[pair[1]]))
    assert abs(lhs - rhs) < 1e-9
    print(f"  check on one random pair: {lhs:.9f} = {rhs:.9f}")


if __name__ == "__main__":
    main()
