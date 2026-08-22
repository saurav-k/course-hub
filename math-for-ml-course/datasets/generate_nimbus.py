"""Generate the Nimbus datasets used by modules M02 and M09.

Nimbus is a fictional SaaS product. Nothing here is real telemetry: every column
is drawn from a stated distribution with a fixed seed, so the files regenerate
byte-identically and every estimator in the course can be checked against a
parameter we actually know.

Run:
    python3 generate_nimbus.py            # writes the CSVs next to this file
    python3 generate_nimbus.py --truth    # also prints the ground truth table

Needs numpy and pandas only.

--------------------------------------------------------------------------
GROUND TRUTH - the parameters the course's estimators are trying to recover
--------------------------------------------------------------------------

nimbus-sessions.csv           25,000 rows
    page_views      Poisson(lambda = 7.4)
    latency_ms      Lognormal(mu = 4.30, sigma = 0.55) on the log scale,
                    with 1.5% of sessions multiplied by a cold-start factor
                    drawn from Uniform(8, 30). The contaminated column is
                    right-skewed and heavy-tailed on purpose.
    session_minutes Gamma(shape = 2.4, scale = 5.0)
    bytes_sent_kb   45.0 * session_minutes + Normal(0, 279.7), floored at 0.
                    Built to correlate with session_minutes at roughly r = 0.78,
                    so the correlation lesson has a real association to measure.
                    page_views is deliberately INDEPENDENT of both, because the
                    Poisson MLE lesson needs a clean lambda to recover.
    temp_c          Normal(21.0, 1.8). An interval scale: 0 is not "no heat"
                    and 30 is not "twice as hot as 15".
    converted       Bernoulli, rate by plan:
                        free 0.031, basic 0.058, pro 0.094, enterprise 0.141
    satisfaction    Ordinal 1..5, probabilities (0.06, 0.11, 0.24, 0.37, 0.22)

nimbus-population.csv         30,000 rows
    spend           Population mean and per-stratum means are printed by
                    --truth. Four strata of deliberately unequal size and
                    unequal spread, which is what makes stratification pay.
    cluster         600 clusters, spend correlated within a cluster.

nimbus-experiment.csv         24,000 rows, 12,000 per arm
    True conversion rate: control 0.0500, treatment 0.0560. That is a real
    12 per cent relative lift, and the assignment is clean: both arms carry
    the same device mix.

    The arm size under-powers the test on purpose. At 12,000 per arm the power
    to detect this effect at alpha = 0.05 two-sided is 0.546, so the experiment
    is close to a coin flip, and 21,885 per arm would be needed for 0.80.

    The stream offset for this file was CHOSEN, not accepted: offsets were
    searched for a realisation in which the underpowered test misses the real
    effect, because that is the case the lesson is about. It happens 45 per
    cent of the time at this power, so the file shows a common outcome rather
    than a rigged one, and saying so here is the price of choosing it.

    What the chosen realisation gives: 596/12,000 against 643/12,000, pooled
    p_hat = 0.05162, z = 1.371, two-sided p = 0.1703. Observed lift 0.392
    percentage points against a true 0.600.

    Three things are true at once, which is why the file exists: the effect is
    real, the test failed to find it, and the 95 per cent interval on the
    difference, [-0.168, +0.952] percentage points, still covers the true
    +0.600. A failed test is not an absent effect, and the failure was
    computable before a single user was assigned.

nimbus-experiment-srm.csv     24,000 rows
    The same product change, logged through a broken filter. The treatment
    effect is genuinely positive inside every device segment, and the pooled
    table reverses it, because the arms no longer share a device mix. This
    file exists to be caught, not to be trusted.

nimbus-adspend.csv            2,000 rows
    revenue_k = 12.5 + 3.20 * ad_spend_k + Normal(0, 8.0)

nimbus-features.csv           4,000 rows, 30 predictors
    Only x01, x02, x03, x04, x05 carry signal, with true coefficients
    (4.0, -2.5, 1.5, -1.0, 0.6). x06..x30 are pure noise with true
    coefficient 0. Noise standard deviation 3.0.

anscombe.csv                  44 rows
    Anscombe, F. J. (1973). "Graphs in Statistical Analysis."
    The American Statistician 27(1), 17-21. Transcribed from the paper.
"""

import argparse
import pathlib

import numpy as np
import pandas as pd

SEED = 20260822
HERE = pathlib.Path(__file__).resolve().parent

# Each dataset draws from its OWN stream, seeded from SEED by a fixed offset.
# That is deliberate: it means adding a column to one file, or changing the row
# count of one file, cannot silently move the numbers in any other file. A
# course quotes these numbers on its pages, so cross-contamination between
# datasets is a defect, not an inconvenience.
STREAM = {
    "sessions": 1, "sessions_bytes": 101, "population": 2, "experiment": 23,
    "experiment_srm": 4, "adspend": 5, "features": 6,
}


def stream(name: str) -> np.random.Generator:
    return np.random.default_rng(SEED + STREAM[name])

PLANS = ("free", "basic", "pro", "enterprise")
PLAN_WEIGHTS = (0.52, 0.27, 0.16, 0.05)
PLAN_CONVERSION = {"free": 0.031, "basic": 0.058, "pro": 0.094, "enterprise": 0.141}
REGIONS = ("us-east", "us-west", "eu-west", "ap-south", "sa-east")
REGION_WEIGHTS = (0.31, 0.19, 0.24, 0.18, 0.08)

POISSON_LAMBDA = 7.4
LOGNORMAL_MU = 4.30
LOGNORMAL_SIGMA = 0.55
COLD_START_RATE = 0.015
GAMMA_SHAPE, GAMMA_SCALE = 2.4, 5.0
TEMP_MEAN, TEMP_SD = 21.0, 1.8
# bytes_sent_kb is built to correlate with session_minutes at a chosen strength.
# Drawn from its own Generator so adding it left every other column untouched.
BYTES_PER_MINUTE = 45.0
BYTES_NOISE_SD = 279.7
SATISFACTION_P = (0.06, 0.11, 0.24, 0.37, 0.22)

STRATA = {
    #  name          size    mean spend   sd
    "smb": (16800, 240.0, 70.0),
    "mid": (8100, 610.0, 150.0),
    "large": (4200, 1480.0, 390.0),
    "strategic": (900, 4100.0, 1250.0),
}
N_CLUSTERS = 600

EXPERIMENT_N_PER_ARM = 12000
CONTROL_RATE = 0.0500
TREATMENT_RATE = 0.0560

ADSPEND_N = 2000
ADSPEND_INTERCEPT = 12.5
ADSPEND_SLOPE = 3.20
ADSPEND_NOISE_SD = 8.0

FEATURES_N = 4000
N_PREDICTORS = 30
TRUE_BETA = (4.0, -2.5, 1.5, -1.0, 0.6)
FEATURES_NOISE_SD = 3.0

ANSCOMBE = {
    "I": [(10, 8.04), (8, 6.95), (13, 7.58), (9, 8.81), (11, 8.33), (14, 9.96),
          (6, 7.24), (4, 4.26), (12, 10.84), (7, 4.82), (5, 5.68)],
    "II": [(10, 9.14), (8, 8.14), (13, 8.74), (9, 8.77), (11, 9.26), (14, 8.10),
           (6, 6.13), (4, 3.10), (12, 9.13), (7, 7.26), (5, 4.74)],
    "III": [(10, 7.46), (8, 6.77), (13, 12.74), (9, 7.11), (11, 7.81), (14, 8.84),
            (6, 6.08), (4, 5.39), (12, 8.15), (7, 6.42), (5, 5.73)],
    "IV": [(8, 6.58), (8, 5.76), (8, 7.71), (8, 8.84), (8, 8.47), (8, 7.04),
           (8, 5.25), (19, 12.50), (8, 5.56), (8, 7.91), (8, 6.89)],
}


def build_sessions(rng: np.random.Generator, n: int = 25000) -> pd.DataFrame:
    """One row per user session, carrying one column of every measurement scale."""
    plan = rng.choice(PLANS, size=n, p=PLAN_WEIGHTS)
    latency = rng.lognormal(LOGNORMAL_MU, LOGNORMAL_SIGMA, size=n)
    cold = rng.random(n) < COLD_START_RATE
    latency[cold] *= rng.uniform(8.0, 30.0, size=int(cold.sum()))
    rate = np.array([PLAN_CONVERSION[p] for p in plan])
    minutes = np.round(rng.gamma(GAMMA_SHAPE, GAMMA_SCALE, size=n), 2)
    # Its own stream, so this column can be added without shifting any other.
    extra = stream("sessions_bytes")
    payload = BYTES_PER_MINUTE * minutes + extra.normal(0.0, BYTES_NOISE_SD, size=n)
    return pd.DataFrame({
        "session_id": [f"NM-{i:06d}" for i in range(1, n + 1)],
        "region": rng.choice(REGIONS, size=n, p=REGION_WEIGHTS),
        "plan": plan,
        "satisfaction": rng.choice([1, 2, 3, 4, 5], size=n, p=SATISFACTION_P),
        "temp_c": np.round(rng.normal(TEMP_MEAN, TEMP_SD, size=n), 2),
        "latency_ms": np.round(latency, 1),
        "page_views": rng.poisson(POISSON_LAMBDA, size=n),
        "session_minutes": minutes,
        "bytes_sent_kb": np.round(np.maximum(payload, 0.0), 2),
        "converted": (rng.random(n) < rate).astype(int),
    })


def build_population(rng: np.random.Generator) -> pd.DataFrame:
    """A sampling frame with real strata, so stratified beats simple random."""
    frames = []
    for name, (size, mean, sd) in STRATA.items():
        cluster = rng.integers(0, N_CLUSTERS, size=size)
        # A cluster-level offset is what makes cluster sampling lose precision.
        offset = rng.normal(0.0, sd * 0.45, size=N_CLUSTERS)[cluster]
        spend = rng.normal(mean, sd * 0.9, size=size) + offset
        frames.append(pd.DataFrame({
            "stratum": name,
            "cluster": cluster,
            "spend": np.round(np.maximum(spend, 0.0), 2),
        }))
    out = pd.concat(frames, ignore_index=True)
    out = out.sample(frac=1.0, random_state=7).reset_index(drop=True)
    out.insert(0, "unit_id", [f"U-{i:06d}" for i in range(1, len(out) + 1)])
    return out


def build_experiment(rng: np.random.Generator) -> pd.DataFrame:
    """A clean A/B log: same device mix in both arms, one honest difference."""
    n = EXPERIMENT_N_PER_ARM
    variant = np.repeat(["control", "treatment"], n)
    device = rng.choice(["mobile", "desktop"], size=2 * n, p=(0.62, 0.38))
    day = rng.integers(1, 15, size=2 * n)
    rate = np.where(variant == "control", CONTROL_RATE, TREATMENT_RATE)
    order = rng.permutation(2 * n)
    return pd.DataFrame({
        "user_id": [f"E-{i:06d}" for i in range(1, 2 * n + 1)],
        "variant": variant,
        "device": device,
        "day": day,
        "converted": (rng.random(2 * n) < rate).astype(int),
    }).iloc[order].reset_index(drop=True)


def build_experiment_srm(rng: np.random.Generator) -> pd.DataFrame:
    """The same change, logged through a broken filter.

    Treatment wins inside mobile and inside desktop. It loses when pooled,
    because the arms no longer share a device mix. The mix is the bug.
    """
    blocks = [
        # variant,     device,    n,     rate
        ("control", "mobile", 3000, 0.040),
        ("control", "desktop", 9000, 0.150),
        ("treatment", "mobile", 10400, 0.048),
        ("treatment", "desktop", 1600, 0.160),
    ]
    frames = []
    for variant, device, n, rate in blocks:
        frames.append(pd.DataFrame({
            "variant": variant,
            "device": device,
            "day": rng.integers(1, 15, size=n),
            "converted": (rng.random(n) < rate).astype(int),
        }))
    out = pd.concat(frames, ignore_index=True)
    out = out.sample(frac=1.0, random_state=11).reset_index(drop=True)
    out.insert(0, "user_id", [f"S-{i:06d}" for i in range(1, len(out) + 1)])
    return out


def build_adspend(rng: np.random.Generator) -> pd.DataFrame:
    """One predictor, one response, a known line and known noise."""
    spend = rng.uniform(2.0, 60.0, size=ADSPEND_N)
    revenue = ADSPEND_INTERCEPT + ADSPEND_SLOPE * spend
    revenue = revenue + rng.normal(0.0, ADSPEND_NOISE_SD, size=ADSPEND_N)
    return pd.DataFrame({
        "week": np.arange(1, ADSPEND_N + 1),
        "ad_spend_k": np.round(spend, 3),
        "revenue_k": np.round(revenue, 3),
    })


def build_features(rng: np.random.Generator) -> pd.DataFrame:
    """Five predictors that matter and twenty-five that do not."""
    x = rng.normal(0.0, 1.0, size=(FEATURES_N, N_PREDICTORS))
    beta = np.zeros(N_PREDICTORS)
    beta[:len(TRUE_BETA)] = TRUE_BETA
    y = x @ beta + rng.normal(0.0, FEATURES_NOISE_SD, size=FEATURES_N)
    cols = {f"x{j + 1:02d}": np.round(x[:, j], 4) for j in range(N_PREDICTORS)}
    return pd.DataFrame({"y": np.round(y, 4), **cols})


def build_anscombe() -> pd.DataFrame:
    rows = [{"dataset": name, "x": float(px), "y": float(py)}
            for name, pts in ANSCOMBE.items() for px, py in pts]
    return pd.DataFrame(rows)


def print_truth(frames: dict[str, pd.DataFrame]) -> None:
    """Print the realised numbers a page may quote, next to the parameters."""
    sessions = frames["nimbus-sessions"]
    print("\n== nimbus-sessions ==")
    print(f"  rows                     {len(sessions):,}")
    print(f"  page_views  true lambda  {POISSON_LAMBDA}   sample mean {sessions.page_views.mean():.4f}")
    print(f"  latency_ms  mean         {sessions.latency_ms.mean():.1f} ms")
    print(f"  latency_ms  median       {sessions.latency_ms.median():.1f} ms")
    print(f"  latency_ms  p95 / p99    {sessions.latency_ms.quantile(0.95):.1f} / {sessions.latency_ms.quantile(0.99):.1f} ms")
    print(f"  overall conversion       {sessions.converted.mean():.5f}")
    r_bm = sessions.bytes_sent_kb.corr(sessions.session_minutes)
    r_pm = sessions.page_views.corr(sessions.session_minutes)
    print(f"  r(bytes_sent_kb, session_minutes) {r_bm:.5f}   built to be near 0.78")
    print(f"  r(page_views,   session_minutes) {r_pm:.5f}   built to be independent")

    pop = frames["nimbus-population"]
    print("\n== nimbus-population ==")
    print(f"  rows                     {len(pop):,}")
    print(f"  POPULATION MEAN spend    {pop.spend.mean():.4f}")
    print(f"  population sd            {pop.spend.std(ddof=0):.4f}")
    for name, grp in pop.groupby("stratum", observed=True):
        print(f"    {name:<10} n={len(grp):>6,}  mean={grp.spend.mean():>9.2f}  sd={grp.spend.std(ddof=1):>8.2f}")

    exp = frames["nimbus-experiment"]
    print("\n== nimbus-experiment (clean) ==")
    tab = exp.groupby("variant", observed=True).converted.agg(["sum", "count", "mean"])
    for variant, row in tab.iterrows():
        print(f"  {variant:<10} {int(row['sum']):>5} / {int(row['count']):>6}  =  {row['mean']:.5f}")
    print("  device mix by arm:")
    mix = pd.crosstab(exp.variant, exp.device, normalize="index")
    for variant, row in mix.iterrows():
        print(f"    {variant:<10} " + "  ".join(f"{d} {v:.4f}" for d, v in row.items()))
    print(f"  {two_proportion_z(exp)}")

    srm = frames["nimbus-experiment-srm"]
    print("\n== nimbus-experiment-srm (the trap) ==")
    seg = srm.groupby(["device", "variant"], observed=True).converted.agg(["sum", "count", "mean"])
    for (device, variant), row in seg.iterrows():
        print(f"  {device:<8} {variant:<10} {int(row['sum']):>5} / {int(row['count']):>6}  =  {row['mean']:.5f}")
    pooled = srm.groupby("variant", observed=True).converted.agg(["sum", "count", "mean"])
    print("  pooled:")
    for variant, row in pooled.iterrows():
        print(f"    {variant:<10} {int(row['sum']):>5} / {int(row['count']):>6}  =  {row['mean']:.5f}")

    ads = frames["nimbus-adspend"]
    sxx = ((ads.ad_spend_k - ads.ad_spend_k.mean()) ** 2).sum()
    sxy = ((ads.ad_spend_k - ads.ad_spend_k.mean()) * (ads.revenue_k - ads.revenue_k.mean())).sum()
    slope = sxy / sxx
    intercept = ads.revenue_k.mean() - slope * ads.ad_spend_k.mean()
    print("\n== nimbus-adspend ==")
    print(f"  true      revenue_k = {ADSPEND_INTERCEPT} + {ADSPEND_SLOPE} * ad_spend_k,  sigma = {ADSPEND_NOISE_SD}")
    print(f"  recovered revenue_k = {intercept:.4f} + {slope:.4f} * ad_spend_k")

    print("\n== nimbus-features ==")
    print(f"  rows {FEATURES_N:,}  predictors {N_PREDICTORS}  informative {len(TRUE_BETA)}")
    print(f"  true beta x01..x05 = {TRUE_BETA}, x06..x30 = 0, noise sd = {FEATURES_NOISE_SD}")


def two_proportion_z(exp: pd.DataFrame) -> str:
    """The pooled two-proportion z test, so the seed can be judged on its output."""
    tab = exp.groupby("variant", observed=True).converted.agg(["sum", "count"])
    x_c, n_c = int(tab.loc["control", "sum"]), int(tab.loc["control", "count"])
    x_t, n_t = int(tab.loc["treatment", "sum"]), int(tab.loc["treatment", "count"])
    p_pool = (x_c + x_t) / (n_c + n_t)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_c + 1 / n_t))
    z = (x_t / n_t - x_c / n_c) / se
    p = 2 * (1 - normal_cdf(abs(z)))
    return f"pooled p_hat={p_pool:.5f}  SE={se:.6f}  z={z:.4f}  two-sided p={p:.4f}"


def normal_cdf(z: float) -> float:
    """Standard normal CDF via the error function, so numpy alone is enough."""
    return 0.5 * (1.0 + np.vectorize(_erf)(z / np.sqrt(2.0)))


def _erf(x: float) -> float:
    import math
    return math.erf(x)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the Nimbus datasets.")
    parser.add_argument("--truth", action="store_true", help="print the ground truth")
    parser.add_argument("--out", default=str(HERE), help="output directory")
    args = parser.parse_args()

    frames = {
        "nimbus-sessions": build_sessions(stream("sessions")),
        "nimbus-population": build_population(stream("population")),
        "nimbus-experiment": build_experiment(stream("experiment")),
        "nimbus-experiment-srm": build_experiment_srm(stream("experiment_srm")),
        "nimbus-adspend": build_adspend(stream("adspend")),
        "nimbus-features": build_features(stream("features")),
        "anscombe": build_anscombe(),
    }

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, frame in frames.items():
        path = out / f"{name}.csv"
        frame.to_csv(path, index=False)
        print(f"wrote {path.name:<28} {len(frame):>7,} rows  {path.stat().st_size / 1e6:>6.2f} MB")

    if args.truth:
        print_truth(frames)


if __name__ == "__main__":
    main()
