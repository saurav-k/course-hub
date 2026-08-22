"""Generate lifecycle_states.csv, the Markov chain dataset for M08.

Seeded and byte-reproducible.

    python3 make_lifecycle_states.py

One row per user per week: 6,000 users observed for 40 weeks, so 240,000 rows.

What is designed into it:

  Four states, trial -> active -> dormant -> churned, with churned ABSORBING in
  the true generator, which is deliberate and is the lesson. A chain with an
  absorbing state is reducible, so it has no stationary distribution the chain
  reaches from anywhere: it converges to "everybody churned". The page uses that
  to show why irreducibility is a condition to CHECK rather than a formality,
  and then repairs it, exactly as PageRank's damping term repairs the web graph.

  The repair takes TWO edges, not one, and finding that out is the best thing in
  this dataset. See the comment on P_REPAIRED below.

  The transition probabilities are FIXED and known, so the lesson can estimate
  them from the data and compare against the truth. Estimating a transition
  matrix is just counting, and being able to check the count against the number
  that generated it is what makes the exercise land.

  The chain is homogeneous: the same matrix at every step. Real lifecycle data is
  not, and the page says so rather than pretending.

The true matrices are printed at the end so a page can quote them.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

SEED = 20260823
N_USERS = 6_000
N_WEEKS = 40
OUT = "../lifecycle_states.csv"

STATES = ("trial", "active", "dormant", "churned")

# The generating matrix. Rows are "from", columns are "to", and every row sums to
# one. Row 3 is the absorbing row: once churned, always churned.
P_TRUE = np.array(
    [
        [0.55, 0.30, 0.10, 0.05],  # from trial
        [0.00, 0.82, 0.13, 0.05],  # from active
        [0.00, 0.22, 0.60, 0.18],  # from dormant
        [0.00, 0.00, 0.00, 1.00],  # from churned, absorbing
    ]
)

# The repaired matrix the lesson moves to. Repairing this chain takes TWO edges,
# not one, and that is the point worth teaching.
#
# Adding only a churned -> active reactivation is NOT enough. It empties the
# absorbing state, but nothing anywhere transitions INTO trial, so trial stays
# unreachable from every other state and the chain stays reducible. The
# stationary distribution then puts exactly zero mass on trial, which is the
# symptom: a state the chain can never re-enter is transient, and a transient
# state gets no stationary mass.
#
# So the repair is a seat-replacement model, which is also the honest business
# model: a churned user either reactivates directly, or their seat is refilled by
# a new trial signup. Now trial <- churned <- dormant <- active <- trial closes
# the loop, every state reaches every other state, and the chain is irreducible.
# Every state also has a self-loop, so it is aperiodic. Both conditions are
# CHECKED in verify() rather than asserted in a comment.
RESEED_TO_TRIAL = 0.03
REACTIVATION = 0.01
P_REPAIRED = P_TRUE.copy()
P_REPAIRED[3] = [
    RESEED_TO_TRIAL,
    REACTIVATION,
    0.00,
    1.0 - RESEED_TO_TRIAL - REACTIVATION,
]


def is_irreducible(matrix: np.ndarray) -> bool:
    """True when every state reaches every other state in some number of steps.

    Reachability is a property of which entries are non-zero, not of their size,
    so this walks the zero pattern rather than multiplying probabilities, where
    repeated products would underflow towards zero and lie.
    """
    reachable = matrix > 0
    closure = reachable.copy()
    for _ in range(len(matrix)):
        closure |= closure @ reachable
    return bool(closure.all())


def is_aperiodic(matrix: np.ndarray) -> bool:
    """Sufficient condition: an irreducible chain with any self-loop is aperiodic."""
    return bool(np.any(np.diag(matrix) > 0))


def stationary(matrix: np.ndarray) -> np.ndarray:
    """The left eigenvector of `matrix` for eigenvalue 1, normalised to sum to 1."""
    values, vectors = np.linalg.eig(matrix.T)
    index = int(np.argmin(np.abs(values - 1.0)))
    vector = np.real(vectors[:, index])
    return vector / vector.sum()


def second_eigenvalue(matrix: np.ndarray) -> float:
    """The second-largest eigenvalue modulus, which sets the mixing rate."""
    moduli = np.sort(np.abs(np.linalg.eigvals(matrix)))
    return float(moduli[-2])


def build() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    # Everybody starts in trial, so the lesson can watch one starting vector move.
    current = np.zeros(N_USERS, dtype=np.int64)
    rows = []
    for week in range(N_WEEKS):
        rows.append(
            pd.DataFrame(
                {
                    "user_id": np.arange(1, N_USERS + 1, dtype=np.int64),
                    "week": np.full(N_USERS, week, dtype=np.int64),
                    "state": [STATES[i] for i in current],
                }
            )
        )
        draws = rng.random(N_USERS)
        cumulative = P_TRUE[current].cumsum(axis=1)
        current = (draws[:, None] > cumulative).sum(axis=1)
    return pd.concat(rows, ignore_index=True)


def estimate(frame: pd.DataFrame) -> np.ndarray:
    """Count transitions out of the observed data and normalise each row.

    This is the whole of transition-matrix estimation, and the lesson works it by
    hand on a small slice before running it here on all 234,000 transitions.
    """
    index = {name: i for i, name in enumerate(STATES)}
    ordered = frame.sort_values(["user_id", "week"])
    source = ordered["state"].to_numpy()[:-1]
    target = ordered["state"].to_numpy()[1:]
    same_user = ordered["user_id"].to_numpy()[:-1] == ordered["user_id"].to_numpy()[1:]

    counts = np.zeros((len(STATES), len(STATES)))
    for a, b in zip(source[same_user], target[same_user]):
        counts[index[a], index[b]] += 1
    totals = counts.sum(axis=1, keepdims=True)
    return np.divide(counts, totals, out=np.zeros_like(counts), where=totals > 0)


def verify(frame: pd.DataFrame) -> None:
    assert len(frame) == N_USERS * N_WEEKS, "row count changed"
    assert set(frame["state"].unique()) <= set(STATES), "unexpected state label"

    # Compare only the three transient rows. The churned row is absorbing, so it
    # reproduces exactly by construction and proves nothing about the estimator.
    estimated = estimate(frame)
    gap = float(np.abs(estimated[:3] - P_TRUE[:3]).max())
    assert gap < 0.02, f"estimated matrix drifted from the truth by {gap}"

    # The absorbing chain must genuinely absorb, or the lesson has no failure to show.
    final = frame[frame["week"] == N_WEEKS - 1]["state"].value_counts(normalize=True)
    assert final.get("churned", 0.0) > 0.75, "churn should dominate by week 40"

    # The absorbing chain is reducible, which is exactly what the lesson shows.
    assert not is_irreducible(P_TRUE), "P_TRUE should be reducible, that is the lesson"

    # The repaired chain must genuinely satisfy both conditions, and its
    # stationary distribution must put positive mass on EVERY state. That last
    # check is the one that caught the one-edge repair: with only a reactivation
    # edge, pi[trial] came out at exactly zero.
    assert is_irreducible(P_REPAIRED), "the repaired chain is still reducible"
    assert is_aperiodic(P_REPAIRED), "the repaired chain is not aperiodic"

    pi = stationary(P_REPAIRED)
    assert abs(pi.sum() - 1.0) < 1e-9, "pi is not a distribution"
    assert pi.min() > 1e-6, f"a transient state got no stationary mass: {pi}"
    assert np.allclose(pi @ P_REPAIRED, pi, atol=1e-12), "pi is not stationary"


def report(frame: pd.DataFrame) -> None:
    print(f"rows                {len(frame):,}  ({N_USERS:,} users x {N_WEEKS} weeks)")
    print(f"transitions         {(N_WEEKS - 1) * N_USERS:,}")
    print("\ntrue transition matrix P (rows sum to 1)")
    print(pd.DataFrame(P_TRUE, index=list(STATES), columns=list(STATES)).round(4))
    print("\nestimated from the data by counting")
    print(pd.DataFrame(estimate(frame), index=list(STATES), columns=list(STATES)).round(4))
    print("\nstate share by week, every fifth week")
    share = (
        frame[frame["week"] % 5 == 0]
        .groupby(["week", "state"])
        .size()
        .unstack(fill_value=0)
        .pipe(lambda d: d.div(d.sum(axis=1), axis=0))
        .reindex(columns=list(STATES))
    )
    print(share.round(4))
    print("\nrepaired transition matrix (two edges out of churned)")
    print(pd.DataFrame(P_REPAIRED, index=list(STATES), columns=list(STATES)).round(4))
    print(f"\nabsorbing chain  irreducible={is_irreducible(P_TRUE)}  "
          f"2nd eigenvalue modulus={second_eigenvalue(P_TRUE):.4f}")
    print(f"repaired chain   irreducible={is_irreducible(P_REPAIRED)}  "
          f"aperiodic={is_aperiodic(P_REPAIRED)}  "
          f"2nd eigenvalue modulus={second_eigenvalue(P_REPAIRED):.4f}")
    pi = stationary(P_REPAIRED)
    print("repaired chain, stationary distribution pi")
    for name, value in zip(STATES, pi):
        print(f"  {name:<9s} {value:.4f}")
    print(f"  check: pi @ P = {np.round(pi @ P_REPAIRED, 4)}")


if __name__ == "__main__":
    data = build()
    verify(data)
    data.to_csv(OUT, index=False, lineterminator="\n")
    report(data)
    print(f"\nwrote {OUT}")
