"""Generate features.csv: a wide design matrix where most predictors are noise.

The dataset behind MAP and regularization, and behind the bias-variance
tradeoff, in M09. Every number in it is invented, and the generating
coefficients are stated here so bias can be MEASURED against a known truth
rather than estimated:

  - 30 predictors, all standard normal and mutually independent.
  - Only x01 to x05 carry signal. Their true coefficients are
    (4.0, -2.5, 1.5, -1.0, 0.6). Every one of x06 to x30 has true coefficient
    exactly 0, so a page can show a fitted model spending effort on nothing.
  - The response is y = X beta + Normal(0, 3.0). The noise standard deviation
    of 3.0 is the irreducible error: no model can drive test error below 9.0,
    and the bias-variance page prints that as a share of the total.
  - 4,000 rows, which is wide enough that fitting on a small subset makes the
    variance term visible without any special pleading. The regularization page
    fits on 60 rows for exactly that reason.
  - Predictors are independent of one another on purpose. Collinearity is a
    real problem and it belongs to a different page; mixing it in here would
    confound the one effect these pages are about.

Run: python3 make_features.py
Writes ../features.csv. Seeded, so it writes the same file every time.
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260828
ROWS = 4_000
N_PREDICTORS = 30
TRUE_BETA = (4.0, -2.5, 1.5, -1.0, 0.6)
NOISE_SD = 3.0
OUT = Path(__file__).resolve().parent.parent / "features.csv"


def build(rows: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    x = rng.normal(0.0, 1.0, size=(rows, N_PREDICTORS))
    beta = np.zeros(N_PREDICTORS)
    beta[:len(TRUE_BETA)] = TRUE_BETA
    y = x @ beta + rng.normal(0.0, NOISE_SD, size=rows)
    columns = {f"x{j + 1:02d}": np.round(x[:, j], 4) for j in range(N_PREDICTORS)}
    return pd.DataFrame({"y": np.round(y, 4), **columns})


def main() -> None:
    frame = build(ROWS, SEED)
    frame.to_csv(OUT, index=False)
    print(f"wrote {OUT}  {len(frame):,} rows  {OUT.stat().st_size / 1e3:.0f} KB")
    print(f"  true beta x01..x05 = {TRUE_BETA}, x06..x30 = 0, noise sd = {NOISE_SD}")


if __name__ == "__main__":
    main()
