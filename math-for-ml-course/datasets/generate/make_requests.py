"""Generate requests.csv - an inference-endpoint request log, built for Module 07.

WHAT IS DESIGNED INTO IT, AND WHY

Module 07 teaches probability, and the two shared datasets cannot carry it:
neither has arrival times, neither has counts in a window, and neither has a
class rare enough for a base rate to bite. This one has all three, in one
schema, so a reader learns the columns once and then meets them on thirteen
pages.

Every property below is deliberate. The numbers are invented. No page cites
this file as evidence about the real world.

  arrival_s        Arrivals are a Poisson process at RATE = 2.3 per second, so
                   the gaps between them are Exponential(2.3) and the count in
                   any one-second window is Poisson(2.3). One column, two
                   distributions, which is the whole of the Poisson/exponential
                   lesson. Memorylessness is checkable directly from the gaps.

  retries          Attempts until the upstream call succeeded, Geometric(0.85)
                   on the trials-until-success convention: support starts at 1,
                   mean 1/p. A reader who assumes the failures-before-success
                   convention gets a mean that is off by exactly one, which is
                   the misconception the geometric page tests.

  route            Categorical over three states with UNEQUAL probabilities
                   (chat 0.60, embed 0.30, rerank 0.10). Equal probabilities
                   would let a reader confuse "categorical" with "uniform".

  cache_hit        Bernoulli(0.25), generated INDEPENDENTLY of verified_user.

  flagged          Bernoulli whose parameter DEPENDS on verified_user:
                   P(flagged | not verified) = 0.0120
                   P(flagged | verified)     = 0.0010
                   So the file carries a genuine dependence and a genuine
                   independence side by side, and the independence page can
                   test both with the same two lines of code. Exactly the
                   trick sessions.csv plays with a real and a null correlation.

                   The marginal rate lands near 0.4%, rare enough that a
                   detector with excellent recall still has poor precision,
                   which is the base-rate lesson computed on our own data.

  abuse_score      The detector's score in [0, 1]. Flagged rows score higher,
                   but the two distributions OVERLAP, so no threshold separates
                   them and every threshold trades recall against false
                   positives. Thresholding this column is how the Bayes page
                   gets a real precision number instead of an assumed one.

  latency_ms       97% Normal(180, 28) and 3% from a heavy right tail. The bulk
                   is close enough to Gaussian that standardising works and the
                   68-95-99.7 check nearly holds; the tail is fat enough that
                   the check visibly fails in the third band. The Gaussian page
                   needs both halves: the default is useful, and real serving
                   latency is not normal.

REPRODUCIBILITY

Seeded with SEED. Re-running must leave `git status` clean.
Needs only numpy and pandas.
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260822
N_ROWS = 25_000

RATE_PER_SECOND = 2.3
RETRY_SUCCESS_P = 0.85

ROUTES = ("chat", "embed", "rerank")
ROUTE_P = (0.60, 0.30, 0.10)

VERIFIED_P = 0.70
CACHE_HIT_P = 0.25

FLAG_P_UNVERIFIED = 0.0120
FLAG_P_VERIFIED = 0.0010

LATENCY_MEAN = 180.0
LATENCY_SD = 28.0
TAIL_SHARE = 0.03

OUT = Path(__file__).resolve().parent.parent / "requests.csv"


def build() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)

    # Arrivals: exponential gaps accumulate into a Poisson process.
    gaps = rng.exponential(scale=1.0 / RATE_PER_SECOND, size=N_ROWS)
    arrival_s = np.cumsum(gaps)

    route = rng.choice(ROUTES, size=N_ROWS, p=ROUTE_P)
    verified = rng.random(N_ROWS) < VERIFIED_P

    # Independent of `verified` by construction: its own draw, no shared input.
    cache_hit = rng.random(N_ROWS) < CACHE_HIT_P

    # Dependent on `verified` by construction: the parameter is chosen per row.
    flag_p = np.where(verified, FLAG_P_VERIFIED, FLAG_P_UNVERIFIED)
    flagged = rng.random(N_ROWS) < flag_p

    # Overlapping score distributions, so no threshold separates the classes.
    score = np.where(
        flagged,
        rng.beta(5.0, 2.0, size=N_ROWS),
        rng.beta(1.6, 8.0, size=N_ROWS),
    )

    retries = rng.geometric(RETRY_SUCCESS_P, size=N_ROWS)

    # Gaussian bulk with a heavy right tail mixed in.
    bulk = rng.normal(LATENCY_MEAN, LATENCY_SD, size=N_ROWS)
    tail = LATENCY_MEAN + rng.lognormal(mean=4.4, sigma=0.75, size=N_ROWS)
    is_tail = rng.random(N_ROWS) < TAIL_SHARE
    latency_ms = np.where(is_tail, tail, bulk)

    return pd.DataFrame(
        {
            "request_id": np.arange(1, N_ROWS + 1),
            "arrival_s": np.round(arrival_s, 4),
            "route": route,
            "verified_user": verified,
            "cache_hit": cache_hit,
            "retries": retries,
            "abuse_score": np.round(score, 4),
            "flagged": flagged,
            "latency_ms": np.round(latency_ms, 2),
        }
    )


def main() -> None:
    frame = build()
    frame.to_csv(OUT, index=False, lineterminator="\n")
    print(f"wrote {OUT} - {len(frame):,} rows, {OUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
