"""Generate sessions.csv: one row per web session, with a known correlation structure.

The dataset behind the descriptive-statistics and correlation pages (M02) and the
estimation pages (M09). Every number in it is invented. It is built so that the
answers a reader computes are checkable rather than realistic:

  - `session_seconds` is lognormal, so its mean and median are far apart and the
    mean is the wrong summary. That is the whole point of the mean-against-median
    page, and a symmetric column would not make it.
  - `spend` is driven by `session_seconds` plus independent noise, so Pearson's r
    against it is strongly positive and reproducible.
  - `screen_brightness` is drawn independently of everything, so its correlation
    with `spend` is near zero. A course that only ever shows a real correlation
    never shows the reader what a null one looks like.
  - Roughly one session in four hundred is a bot with an enormous page count,
    which is what makes a trimmed summary visibly different from an untrimmed one.

Run: python3 make_sessions.py
Writes ../sessions.csv. Seeded, so it writes the same file every time.
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260822
ROWS = 20_000
OUT = Path(__file__).resolve().parent.parent / "sessions.csv"


def build(rows: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    session_seconds = np.round(rng.lognormal(mean=4.6, sigma=1.05, size=rows), 1)

    pages_viewed = np.maximum(1, np.round(session_seconds / 45 + rng.normal(0, 1.4, rows))).astype(int)
    bots = rng.random(rows) < 0.0025
    pages_viewed[bots] = rng.integers(300, 900, bots.sum())

    spend = np.maximum(0.0, np.round(0.11 * session_seconds + rng.normal(0, 9.0, rows), 2))
    spend[rng.random(rows) < 0.62] = 0.0

    screen_brightness = np.round(rng.uniform(0, 100, rows), 1)

    device = rng.choice(["mobile", "desktop", "tablet"], size=rows, p=[0.58, 0.34, 0.08])
    returning = rng.random(rows) < 0.41

    return pd.DataFrame(
        {
            "session_id": np.arange(1, rows + 1),
            "session_seconds": session_seconds,
            "pages_viewed": pages_viewed,
            "spend": spend,
            "screen_brightness": screen_brightness,
            "device": device,
            "returning": returning,
        }
    )


def main() -> None:
    frame = build(ROWS, SEED)
    frame.to_csv(OUT, index=False)
    print(f"wrote {OUT} - {len(frame):,} rows, {OUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
