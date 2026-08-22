"""Generate m05-spend.csv, the heavy-tailed spend table for M05.

Five thousand daily card spends with a long right tail. The lesson on points
where the derivative does not exist uses it to show two things at once: that
setting a derivative to zero picks out the mean, and that the same move is
unavailable for the absolute loss, whose minimiser is the median and whose
minimising set is an interval rather than a point.

A long tail is what makes the two answers differ enough to argue about, so the
bulk is lognormal and a small fraction of days are genuine spikes.

Reproducible: fixed seed, no wall-clock, no network.

    python3 make_m05_spend.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260822
ROWS = 5000
SPIKE_RATE = 0.012


def build() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)

    # Ordinary days: lognormal around roughly Rs 420.
    spend = rng.lognormal(mean=np.log(410.0), sigma=0.42, size=ROWS)

    # Spike days: a rent payment, a flight, a hospital bill. Few, and large
    # enough that they move the mean and leave the median alone.
    spikes = rng.random(ROWS) < SPIKE_RATE
    spend[spikes] *= rng.uniform(14.0, 45.0, spikes.sum())

    day = np.arange(1, ROWS + 1)
    return pd.DataFrame(
        {
            "day": day,
            "spend_inr": spend.round(2),
            "is_spike": spikes.astype(int),
        }
    )


def main() -> None:
    frame = build()
    out = Path(__file__).with_name("m05-spend.csv")
    frame.to_csv(out, index=False)
    spend = frame["spend_inr"]
    print(f"wrote {out.name}: {len(frame)} rows, {out.stat().st_size / 1024:.0f} KB")
    print(f"mean {spend.mean():.2f}  median {spend.median():.2f}  max {spend.max():.2f}")
    print(f"spike days {int(frame['is_spike'].sum())}")


if __name__ == "__main__":
    main()
