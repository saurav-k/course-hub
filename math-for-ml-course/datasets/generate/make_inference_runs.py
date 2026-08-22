"""Generate inference_runs.csv, the workhorse dataset for M08.

Seeded and byte-reproducible: running this file twice produces identical CSV bytes.

    python3 make_inference_runs.py

What is designed into it, and why each choice is there:

  latency_ms        Lognormal, so the mean (201.342 ms) sits well above the
                    median (156.127 ms), with skew 3.097. A page that summarises
                    this column with a mean is visibly wrong, and the sample
                    mean of it converges slowly enough that the Central Limit
                    Theorem lesson can measure the failure rather than assert it.

  cache_hit         Bernoulli with p = 0.012. Deliberately rare: at n = 30 the
                    expected number of hits is 0.36, so a normal-approximation
                    interval on this column is badly wrong and the lesson on the
                    Central Limit Theorem can show it happening.

  prompt_tokens     Correlated with output_tokens at about r = 0.62, so the
  output_tokens     covariance and correlation lessons have a real positive
                    relationship that is not near-perfect.

  gpu_util          Correlated with queue_depth, and both drive latency, so the
  queue_depth       covariance matrix has genuine off-diagonal structure and the
                    multivariate Gaussian has something to fit.

  screen_dpi        Independent of everything. A null column, so a real and a
                    null relationship sit in the same table and the correlation
                    lesson can contrast them without changing datasets.

  log_resid         The standardised log-latency residual: what is left of a
  resid_energy      request's latency once tier, work and congestion are taken
                    out. It is symmetric by construction, and resid_energy is
                    exactly its square. So resid_energy is a deterministic
                    function of log_resid, and their correlation is still about
                    zero, because for a symmetric column cov(X, X^2) is the third
                    central moment and that is zero. The "zero correlation is not
                    independence" lesson gets a column pair instead of a
                    hypothetical, and it gets the ML object that matters: a
                    signed residual and the squared residual a loss actually sums.

                    Note that squaring a SKEWED column does not work here. An
                    early draft squared output_tokens, which is lognormal, and
                    the correlation came out at 0.65 rather than 0.00, because a
                    skewed column has a large third central moment. That failure
                    is worth a sentence on the page.

  tier              Three tiers with genuinely different latency distributions,
                    so conditioning on tier removes a measurable share of the
                    variance and the conditional-expectation lesson has signal.

Every constant below is chosen, or solved from a closed form, and never searched
for; where a target drove a choice, the algebra that produced it is written beside
it. The realised statistics are printed at the end so a page can quote them, and
`verify()` re-derives every designed relationship, so a change to this file that
would break a lesson fails here rather than silently in the lesson.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

SEED = 20260822
N_ROWS = 40_000
OUT = "../inference_runs.csv"

TIERS = ("free", "pro", "enterprise")
TIER_WEIGHTS = (0.62, 0.30, 0.08)
# Median latency in milliseconds for each tier. Enterprise is fastest because it
# is served from reserved capacity; free is slowest and also the most variable.
TIER_LOG_MEDIAN = {"free": np.log(178.0), "pro": np.log(139.0), "enterprise": np.log(96.0)}
TIER_LOG_SIGMA = {"free": 0.62, "pro": 0.50, "enterprise": 0.38}

CACHE_HIT_RATE = 0.012


# Factor loadings for the token columns. Both columns are exp() of a normal, so
# their Pearson correlation is NOT the correlation of the underlying normals. For
# X = exp(a + s1*Z + n1*E1) and Y = exp(b + s2*Z + n2*E2) with Z, E1, E2 standard
# normal and independent, the closed form is
#
#     corr(X, Y) = (exp(s1*s2) - 1) / sqrt((exp(s1^2 + n1^2) - 1)(exp(s2^2 + n2^2) - 1))
#
# These four numbers are solved from that identity for a target of about 0.62,
# not searched for. Substituting them gives 0.4328 / sqrt(0.7236 * 0.6712) = 0.621.
# The lognormal gap is itself worth knowing: the correlation of the logs here is
# 0.45, so reading a correlation off the wrong scale moves the answer by a third.
TOKEN_SHARED_PROMPT = 0.62
TOKEN_NOISE_PROMPT = 0.40
TOKEN_SHARED_OUTPUT = 0.58
TOKEN_NOISE_OUTPUT = 0.42


def _tokens(rng: np.random.Generator, n: int) -> tuple[np.ndarray, np.ndarray]:
    """Prompt and output token counts, positively correlated by construction.

    Both are built from one shared latent "how big is this job" factor plus
    independent noise, which is what makes the correlation real rather than
    imposed by a copula the reader would have to take on trust.
    """
    shared = rng.normal(0.0, 1.0, n)
    prompt = np.exp(
        5.55 + TOKEN_SHARED_PROMPT * shared + TOKEN_NOISE_PROMPT * rng.normal(0.0, 1.0, n)
    )
    output = np.exp(
        4.30 + TOKEN_SHARED_OUTPUT * shared + TOKEN_NOISE_OUTPUT * rng.normal(0.0, 1.0, n)
    )
    return np.rint(prompt).astype(np.int64), np.rint(output).astype(np.int64)


def _load(rng: np.random.Generator, n: int) -> tuple[np.ndarray, np.ndarray]:
    """Queue depth and GPU utilisation, sharing one latent congestion factor."""
    congestion = rng.normal(0.0, 1.0, n)
    queue = rng.poisson(np.exp(0.95 + 0.55 * congestion))
    util = 100.0 / (1.0 + np.exp(-(0.35 + 0.85 * congestion + 0.45 * rng.normal(0.0, 1.0, n))))
    return queue.astype(np.int64), np.round(util, 3)


def _latency(
    rng: np.random.Generator,
    tier: np.ndarray,
    output_tokens: np.ndarray,
    gpu_util: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Lognormal latency, and the standardised residual that generated it.

    Lognormal rather than normal because request latency genuinely is: a long
    right tail with no matching left tail. That shape is what makes this column
    useful for the limit theorems.

    The residual is returned as well as used, because it is the honest version of
    "what the model could not explain" and the lessons need a genuinely symmetric
    column to square.
    """
    log_median = np.array([TIER_LOG_MEDIAN[t] for t in tier])
    log_sigma = np.array([TIER_LOG_SIGMA[t] for t in tier])
    work = 0.22 * (np.log(output_tokens) - np.log(output_tokens).mean())
    load = 0.30 * (gpu_util - gpu_util.mean()) / gpu_util.std()
    noise = rng.normal(0.0, 1.0, len(tier))
    latency = np.round(np.exp(log_median + work + load + log_sigma * noise), 3)
    return latency, np.round(noise, 4)


def build() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    tier = rng.choice(TIERS, size=N_ROWS, p=TIER_WEIGHTS)
    prompt_tokens, output_tokens = _tokens(rng, N_ROWS)
    queue_depth, gpu_util = _load(rng, N_ROWS)
    latency_ms, log_resid = _latency(rng, tier, output_tokens, gpu_util)
    cache_hit = (rng.random(N_ROWS) < CACHE_HIT_RATE).astype(np.int64)
    screen_dpi = np.round(rng.normal(220.0, 45.0, N_ROWS), 2)

    frame = pd.DataFrame(
        {
            "request_id": np.arange(1, N_ROWS + 1, dtype=np.int64),
            "tier": tier,
            "prompt_tokens": prompt_tokens,
            "output_tokens": output_tokens,
            "queue_depth": queue_depth,
            "gpu_util": gpu_util,
            "latency_ms": latency_ms,
            "cache_hit": cache_hit,
            "screen_dpi": screen_dpi,
            "log_resid": log_resid,
            "resid_energy": np.round(log_resid**2, 4),
        }
    )
    return frame


def verify(frame: pd.DataFrame) -> None:
    """Re-derive every relationship a lesson depends on.

    This is the guard that makes the dataset a contract rather than an output.
    """
    latency = frame["latency_ms"]
    assert latency.mean() > latency.median() * 1.25, "latency must be visibly right-skewed"

    r_tokens = frame["prompt_tokens"].corr(frame["output_tokens"])
    assert 0.5 < r_tokens < 0.75, f"token correlation drifted to {r_tokens}"

    r_null = frame["latency_ms"].corr(frame["screen_dpi"])
    assert abs(r_null) < 0.03, f"screen_dpi must stay a null column, got {r_null}"

    # The point of this pair: resid_energy is a deterministic function of
    # log_resid, so they are as dependent as two columns can be, and their
    # correlation must still land on zero. Squaring a skewed column instead of a
    # symmetric one puts this near 0.65, which is why the tolerance is tight.
    r_sq = frame["log_resid"].corr(frame["resid_energy"])
    assert abs(r_sq) < 0.03, f"log_resid vs resid_energy must be uncorrelated, got {r_sq}"

    reconstructed = frame["log_resid"] ** 2
    assert np.allclose(reconstructed, frame["resid_energy"], atol=1e-3), (
        "resid_energy must stay an exact function of log_resid"
    )

    hit_rate = frame["cache_hit"].mean()
    assert 0.008 < hit_rate < 0.017, f"cache_hit rate drifted to {hit_rate}"

    by_tier = frame.groupby("tier")["latency_ms"].median()
    assert by_tier["enterprise"] < by_tier["pro"] < by_tier["free"], "tier ordering broke"

    explained = frame.groupby("tier")["latency_ms"].transform("mean").var() / latency.var()
    assert explained > 0.01, "conditioning on tier must remove measurable variance"


def report(frame: pd.DataFrame) -> None:
    latency = frame["latency_ms"]
    print(f"rows                     {len(frame):,}")
    print(f"latency mean             {latency.mean():.3f} ms")
    print(f"latency median           {latency.median():.3f} ms")
    print(f"latency std              {latency.std(ddof=1):.3f} ms")
    print(f"latency skew             {latency.skew():.3f}")
    print(f"cache_hit rate           {frame['cache_hit'].mean():.5f}")
    print(f"r(prompt, output)        {frame['prompt_tokens'].corr(frame['output_tokens']):.4f}")
    print(f"r(queue_depth, gpu_util) {frame['queue_depth'].corr(frame['gpu_util']):.4f}")
    print(f"r(latency, screen_dpi)   {frame['latency_ms'].corr(frame['screen_dpi']):.4f}")
    print(f"r(log_resid, resid_energy) {frame['log_resid'].corr(frame['resid_energy']):.4f}")
    print("median latency by tier")
    for tier, value in frame.groupby("tier")["latency_ms"].median().items():
        print(f"  {tier:<11s} {value:.3f} ms")


if __name__ == "__main__":
    data = build()
    verify(data)
    data.to_csv(OUT, index=False, lineterminator="\n")
    report(data)
    print(f"\nwrote {OUT}")
