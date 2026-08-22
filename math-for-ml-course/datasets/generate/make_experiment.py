"""Generate experiment.csv: a randomised A/B log that is under-powered on purpose.

The dataset behind the hypothesis-testing, p-value, A/B and Bayesian pages of
M09. Every number in it is invented, and it is built so the reader can check an
answer against a truth we actually know:

  - The true conversion rates are 0.0500 for control and 0.0560 for treatment.
    That is a real 12 per cent relative lift, so there IS an effect to find.
  - The arms are 12,000 each, which gives power 0.546 to detect that effect at
    alpha = 0.05 two-sided. Detecting it reliably would need 21,885 per arm.
    The under-powering is the lesson, not an accident.
  - The seed offset was CHOSEN rather than accepted. Offsets were searched for a
    realisation in which the under-powered test MISSES the real effect, because
    that is the case the page is about. It happens 45 per cent of the time at
    this power, so the file shows a common outcome, and disclosing the search
    here is the price of having run it.
  - What the chosen realisation gives: 596/12,000 against 643/12,000, pooled
    p_hat = 0.05162, z = 1.3711, two-sided p = 0.1703. Observed lift 0.392
    percentage points against a true 0.600.
  - Three things are therefore true at once, which is the whole point: the
    effect is real, the test failed to find it, and the 95 per cent interval on
    the difference, [-0.168, +0.952] percentage points, still covers the true
    +0.600. A failed test is not an absent effect.
  - `device` is assigned independently of `variant`, so the arms share a device
    mix. A reader can check that, and checking it is the sample-ratio-mismatch
    habit the A/B page teaches.
  - `day` runs 1 to 14 so the peeking simulation has a time axis to walk.

Run: python3 make_experiment.py
Writes ../experiment.csv. Seeded, so it writes the same file every time.
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260845          # 20260822 + 23, the searched offset
ROWS_PER_ARM = 12_000
CONTROL_RATE = 0.0500
TREATMENT_RATE = 0.0560
OUT = Path(__file__).resolve().parent.parent / "experiment.csv"


def build(rows_per_arm: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = 2 * rows_per_arm
    variant = np.repeat(["control", "treatment"], rows_per_arm)
    device = rng.choice(["mobile", "desktop"], size=n, p=(0.62, 0.38))
    day = rng.integers(1, 15, size=n)
    rate = np.where(variant == "control", CONTROL_RATE, TREATMENT_RATE)
    order = rng.permutation(n)
    frame = pd.DataFrame({
        "user_id": np.arange(1, n + 1),
        "variant": variant,
        "device": device,
        "day": day,
        "converted": (rng.random(n) < rate).astype(int),
    })
    return frame.iloc[order].reset_index(drop=True)


def main() -> None:
    frame = build(ROWS_PER_ARM, SEED)
    frame.to_csv(OUT, index=False)
    print(f"wrote {OUT}  {len(frame):,} rows  {OUT.stat().st_size / 1e3:.0f} KB")
    table = frame.groupby("variant").converted.agg(["sum", "count", "mean"])
    for variant, row in table.iterrows():
        print(f"  {variant:<10} {int(row['sum']):>5}/{int(row['count']):,} = {row['mean']:.5f}")


if __name__ == "__main__":
    main()
