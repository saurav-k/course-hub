"""Generate population.csv: a survey frame with real strata, and one column of every measurement scale.

The dataset behind two M02 pages, and it carries two unrelated jobs because
each alone would not justify a file.

JOB ONE - survey sampling designs. The lesson is that stratified sampling beats
simple random by exactly the between-stratum variance, and that cluster
sampling usually loses. Neither claim is demonstrable without strata and
clusters, so:

  - Four strata of deliberately unequal size AND unequal spread, with means
    running from about 240 to about 4,100. That spread is what makes
    stratification pay: the between-stratum share of total variance is about
    87 per cent, and that number predicts the measured variance ratio of about
    0.13 against simple random sampling.
  - 600 clusters with a cluster-level offset added to `spend`, so units inside
    a cluster resemble one another. That similarity is precisely why cluster
    sampling is less precise per unit, and without it the lesson has no effect
    to measure.

JOB TWO - the measurement-scale ladder. The lesson is that each rung licenses
different operations, and it is demonstrated by applying the transformation a
rung allows and watching a conclusion survive or break. That needs one column
of each rung, and an INTERVAL column is the one nothing else in the course has:

  - `region` is NOMINAL. Labels only, and any relabelling is allowed, which is
    what makes a "mean region" give two different answers.
  - `satisfaction` is ORDINAL, 1 to 5. Order is meaningful, spacing is not,
    which is what makes a mean rating a stated assumption rather than a fact.
  - `office_temp_c` is INTERVAL. Differences mean something and the zero is a
    convention, so a ratio of two temperatures reads differently in Celsius and
    in Fahrenheit. That failure is the point of the column.
  - `spend` is RATIO. A true zero, so ratios survive and "twice as much" means
    something.

Every number is invented. Nothing here is a claim about the world.

Run: python3 make_population.py
Writes ../population.csv. Seeded, so it writes the same file every time.
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260824
N_CLUSTERS = 600
OUT = Path(__file__).resolve().parent.parent / "population.csv"

#  name          size    mean spend   sd
STRATA = {
    "smb": (16_800, 240.0, 70.0),
    "mid": (8_100, 610.0, 150.0),
    "large": (4_200, 1_480.0, 390.0),
    "strategic": (900, 4_100.0, 1_250.0),
}
REGIONS = ("us-east", "us-west", "eu-west", "ap-south", "sa-east")
REGION_WEIGHTS = (0.31, 0.19, 0.24, 0.18, 0.08)
SATISFACTION_P = (0.06, 0.11, 0.24, 0.37, 0.22)
TEMP_MEAN, TEMP_SD = 21.0, 1.8


def build(seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
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
    n = len(out)
    out["region"] = rng.choice(REGIONS, size=n, p=REGION_WEIGHTS)
    out["satisfaction"] = rng.choice([1, 2, 3, 4, 5], size=n, p=SATISFACTION_P)
    out["office_temp_c"] = np.round(rng.normal(TEMP_MEAN, TEMP_SD, size=n), 2)
    out = out.sample(frac=1.0, random_state=7).reset_index(drop=True)
    out.insert(0, "unit_id", np.arange(1, n + 1))
    return out[["unit_id", "region", "stratum", "cluster", "satisfaction",
                "office_temp_c", "spend"]]


def main() -> None:
    frame = build(SEED)
    frame.to_csv(OUT, index=False)
    print(f"wrote {OUT}  {len(frame):,} rows  {OUT.stat().st_size / 1e3:.0f} KB")
    print(f"  POPULATION MEAN spend = {frame.spend.mean():.4f}")
    within = 0.0
    between = 0.0
    mu = frame.spend.mean()
    for name, grp in frame.groupby("stratum"):
        w = len(grp) / len(frame)
        within += w * grp.spend.var(ddof=0)
        between += w * (grp.spend.mean() - mu) ** 2
        print(f"    {name:<10} n={len(grp):>6,}  mean={grp.spend.mean():>9.2f}  sd={grp.spend.std(ddof=1):>8.2f}")
    print(f"  within {within:,.1f} + between {between:,.1f} = {within + between:,.1f}"
          f"  (population variance {frame.spend.var(ddof=0):,.1f})")
    print(f"  between-stratum share {between / (within + between):.1%}")


if __name__ == "__main__":
    main()
