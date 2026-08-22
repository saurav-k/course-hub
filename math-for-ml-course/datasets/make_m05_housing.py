"""Generate m05-housing.csv, the badly conditioned regression table for M05.

The point of this table is the SCALE DISPARITY between its columns. Area is in
thousands, bedrooms are in single digits, and lot size is in tens of thousands.
That disparity is what makes the Hessian of the squared-error loss badly
conditioned, which is what lessons on curvature, step size and feature scaling
need in order to say anything with a number in it.

Reproducible: fixed seed, no wall-clock, no network. Re-running overwrites the
csv with byte-identical content.

    python3 make_m05_housing.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260822
ROWS = 8000

# The rule the data is generated from. The lessons quote these as the truth the
# fitted coefficients are trying to recover, so they live in one place.
TRUE = {
    "intercept": 40.0,
    "area_sqft": 0.152,
    "bedrooms": 11.0,
    "age_years": -0.85,
    "lot_sqft": 0.021,
}
NOISE_SD = 18.0


def build() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)

    area = rng.normal(1900, 620, ROWS).clip(600, 4200)
    # Bedrooms track area, because a table where they did not would make the
    # collinearity lessons dishonest.
    bedrooms = np.round(1.0 + area / 900 + rng.normal(0, 0.55, ROWS)).clip(1, 6)
    age = rng.gamma(shape=2.2, scale=11.0, size=ROWS).clip(0, 90)
    lot = (area * rng.uniform(1.8, 6.5, ROWS)).clip(1500, 20000)

    price = (
        TRUE["intercept"]
        + TRUE["area_sqft"] * area
        + TRUE["bedrooms"] * bedrooms
        + TRUE["age_years"] * age
        + TRUE["lot_sqft"] * lot
        + rng.normal(0, NOISE_SD, ROWS)
    )

    return pd.DataFrame(
        {
            "area_sqft": area.round(1),
            "bedrooms": bedrooms.astype(int),
            "age_years": age.round(1),
            "lot_sqft": lot.round(1),
            "price_k": price.round(2),
        }
    )


def main() -> None:
    frame = build()
    out = Path(__file__).with_name("m05-housing.csv")
    frame.to_csv(out, index=False)
    print(f"wrote {out.name}: {len(frame)} rows, {out.stat().st_size / 1024:.0f} KB")
    print(frame.describe().round(2).to_string())


if __name__ == "__main__":
    main()
