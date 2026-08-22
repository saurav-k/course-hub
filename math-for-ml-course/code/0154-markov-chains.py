"""Markov chains: estimating one, running it, and the two conditions.

Lesson: Markov chains.

    python3 0815-markov-chains.py

Uses lifecycle_states.csv: 6,000 users over 40 weeks, generated from a known
transition matrix, so the estimate can be checked against the truth.

What it checks twice:

  1. Estimating P is counting. The estimate from 234,000 observed transitions
     against the matrix that generated them.
  2. The n-step distribution by repeated matrix multiplication, against the
     state shares actually observed in the data at that week. Theory and
     measurement, side by side.
  3. The stationary distribution three ways: by iterating, by solving the linear
     system, and as a left eigenvector for eigenvalue 1.
  4. The two conditions, CHECKED. The generating chain is reducible, so it has no
     stationary distribution it reaches from anywhere. The repaired chain is
     irreducible and aperiodic, and the mixing rate is read off the second
     eigenvalue.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "lifecycle_states.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/lifecycle_states.csv"
)
STATES = ("trial", "active", "dormant", "churned")

P_TRUE = np.array(
    [
        [0.55, 0.30, 0.10, 0.05],
        [0.00, 0.82, 0.13, 0.05],
        [0.00, 0.22, 0.60, 0.18],
        [0.00, 0.00, 0.00, 1.00],
    ]
)
P_REPAIRED = P_TRUE.copy()
P_REPAIRED[3] = [0.03, 0.01, 0.00, 0.96]


def load() -> pd.DataFrame:
    """Read the committed dataset, falling back to the published URL.

    The path is resolved from this file rather than the working directory, so the
    program runs from anywhere. The URL fallback is what lets it be pasted into
    Colab or a notebook with no checkout at all.
    """
    return pd.read_csv(DATA) if DATA.exists() else pd.read_csv(URL)


def estimate(frame: pd.DataFrame) -> np.ndarray:
    """Count every transition and normalise each row. That is the whole estimator."""
    index = {name: i for i, name in enumerate(STATES)}
    ordered = frame.sort_values(["user_id", "week"])
    users = ordered["user_id"].to_numpy()
    codes = np.array([index[s] for s in ordered["state"].to_numpy()])
    same = users[:-1] == users[1:]
    counts = np.zeros((4, 4))
    np.add.at(counts, (codes[:-1][same], codes[1:][same]), 1)
    totals = counts.sum(axis=1, keepdims=True)
    return np.divide(counts, totals, out=np.zeros_like(counts), where=totals > 0)


def is_irreducible(matrix: np.ndarray) -> bool:
    reach = matrix > 0
    closure = reach.copy()
    for _ in range(len(matrix)):
        closure |= closure @ reach
    return bool(closure.all())


def main() -> None:
    frame = load()
    print(f"rows {len(frame):,}   users {frame['user_id'].nunique():,}   "
          f"weeks {frame['week'].nunique()}\n")

    print("1. Estimating the transition matrix is counting")
    estimated = estimate(frame)
    print("   estimated from 234,000 observed transitions")
    print(pd.DataFrame(estimated, index=list(STATES), columns=list(STATES)).round(4))
    print(f"\n   largest gap to the generating matrix: "
          f"{np.abs(estimated[:3] - P_TRUE[:3]).max():.4f}")
    assert np.allclose(estimated[:3], P_TRUE[:3], atol=0.02)
    print("   Every row sums to 1:", np.round(estimated.sum(axis=1), 10))

    print("\n2. The n-step distribution: theory against the data")
    print("   v_0 P^t predicted, against the state shares actually observed.")
    v0 = np.array([1.0, 0.0, 0.0, 0.0])
    observed = (
        frame.groupby(["week", "state"]).size().unstack(fill_value=0).reindex(columns=list(STATES))
    )
    observed = observed.div(observed.sum(axis=1), axis=0)
    print(f"\n   {'week':>5}  {'predicted (trial/active/dormant/churned)':<44}{'observed':<44}")
    for week in (1, 2, 5, 10, 20):
        predicted = v0 @ np.linalg.matrix_power(P_TRUE, week)
        actual = observed.loc[week].to_numpy()
        print(f"   {week:>5}  {np.array2string(np.round(predicted, 4), precision=4):<44}"
              f"{np.array2string(np.round(actual, 4), precision=4):<44}")
        assert np.abs(predicted - actual).max() < 0.02
    print("\n   One matrix power is the entire future. Nothing was simulated to get")
    print("   the left column, and nothing was assumed to get the right one.")

    print("\n3. The stationary distribution, three ways (on the repaired chain)")
    iterated = np.array([0.25, 0.25, 0.25, 0.25])
    for _ in range(5_000):
        iterated = iterated @ P_REPAIRED
    # Solve (P^T - I) pi = 0 with the constraint that pi sums to 1.
    system = np.vstack([P_REPAIRED.T - np.eye(4), np.ones(4)])
    target = np.array([0.0, 0.0, 0.0, 0.0, 1.0])
    solved, *_ = np.linalg.lstsq(system, target, rcond=None)
    values, vectors = np.linalg.eig(P_REPAIRED.T)
    which = int(np.argmin(np.abs(values - 1.0)))
    eigen = np.real(vectors[:, which])
    eigen = eigen / eigen.sum()
    table = pd.DataFrame(
        {"by iterating": iterated, "by solving": solved, "by eigenvector": eigen},
        index=list(STATES),
    )
    print(table.round(6))
    assert np.allclose(iterated, solved, atol=1e-8) and np.allclose(iterated, eigen, atol=1e-8)
    print(f"\n   check pi @ P = {np.round(iterated @ P_REPAIRED, 6)}")
    assert np.allclose(iterated @ P_REPAIRED, iterated)
    print("   Unchanged by another step, which is what stationary means. Note that")
    print("   users keep moving between states forever; it is the DISTRIBUTION that")
    print("   stopped moving, not anybody's trajectory.")

    print("\n4. The two conditions, checked rather than assumed")
    for name, matrix in (("generating chain", P_TRUE), ("repaired chain", P_REPAIRED)):
        irreducible = is_irreducible(matrix)
        aperiodic = bool(np.any(np.diag(matrix) > 0))
        moduli = np.sort(np.abs(np.linalg.eigvals(matrix)))
        print(f"   {name:<18} irreducible={str(irreducible):<6} "
              f"aperiodic={str(aperiodic):<6} |lambda_2|={moduli[-2]:.4f}")
    print("\n   The generating chain is REDUCIBLE, because churned is absorbing and")
    print("   nothing leaves it. Its long-run answer is 'everybody churned', which")
    print("   is a limit but not a useful stationary distribution.")
    print("   Repairing it took TWO edges, not one. A churned-to-active edge alone")
    print("   still leaves trial unreachable from everywhere, so trial stays")
    print("   transient and gets exactly zero stationary mass. Adding a")
    print("   churned-to-trial edge as well closes the loop.")
    print("\n   That is exactly what PageRank's damping term does: a raw web graph")
    print("   has dangling pages and disconnected components, so the teleport is")
    print("   not a hack, it is what makes the theorem apply at all.")

    gap = np.sort(np.abs(np.linalg.eigvals(P_REPAIRED)))[-2]
    print(f"\n   Mixing: |lambda_2| = {gap:.4f}, so the distance to pi falls by about")
    print(f"   {(1 - gap) * 100:.0f} percent per step. After t steps it is roughly {gap:.3f}^t:")
    start = np.array([1.0, 0.0, 0.0, 0.0])
    print(f"   {'t':>5}{'distance to pi':>18}{'|lambda_2|^t':>16}")
    current = start.copy()
    for t in range(0, 121, 20):
        current = start @ np.linalg.matrix_power(P_REPAIRED, t)
        print(f"   {t:>5}{np.abs(current - iterated).sum():>18.6f}{gap**t:>16.6f}")


if __name__ == "__main__":
    main()
