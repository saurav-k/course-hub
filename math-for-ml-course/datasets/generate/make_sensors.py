"""Generate sensors.csv: a feature matrix with principal directions planted in it.

The dataset behind the vector, norm, dot-product and matrix pages (M03) and the
eigen, SVD and PCA pages (M04). It is built from a known low-rank signal plus
noise, so a reader who runs PCA on it gets an answer they can check against the
construction rather than against a printed number they must take on trust:

  - Eight sensors are generated from THREE latent factors, so the covariance
    matrix has three large eigenvalues and five small ones. The scree plot has a
    visible elbow at 3 because one was built in.
  - The three factors carry deliberately different strengths (6, 3, 1.5), so the
    first three eigenvalues are well separated and their order is stable.
  - `temp_c` is on a scale of tens and `pressure_kpa` on a scale of hundreds,
    while the rest sit near zero. Running PCA without standardising therefore
    gives a visibly wrong answer dominated by `pressure_kpa`. That is the point:
    the standardisation page needs a dataset that punishes skipping it.
  - Two sensors are near-duplicates of each other, so the matrix is close to rank
    deficient and its condition number is large enough to see.

Run: python3 make_sensors.py
Writes ../sensors.csv. Seeded, so it writes the same file every time.
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260822
ROWS = 12_000
OUT = Path(__file__).resolve().parent.parent / "sensors.csv"

STRENGTH = np.array([6.0, 3.0, 1.5])

# Each row is one sensor's loading on the three latent factors.
LOADINGS = np.array(
    [
        [0.90, 0.10, 0.05],   # vibration_x
        [0.88, 0.12, 0.04],   # vibration_y  - near-duplicate of vibration_x
        [0.20, 0.85, 0.10],   # acoustic_db
        [0.15, 0.80, 0.20],   # current_amp
        [0.05, 0.15, 0.88],   # humidity_pct
        [0.10, 0.20, 0.80],   # dust_index
        [0.35, 0.35, 0.30],   # temp_c
        [0.30, 0.40, 0.25],   # pressure_kpa
    ]
)

NAMES = [
    "vibration_x", "vibration_y", "acoustic_db", "current_amp",
    "humidity_pct", "dust_index", "temp_c", "pressure_kpa",
]


def build(rows: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    factors = rng.normal(0, 1, size=(rows, 3)) * STRENGTH
    signal = factors @ LOADINGS.T
    noise = rng.normal(0, 0.6, size=(rows, len(NAMES)))
    values = signal + noise

    frame = pd.DataFrame(np.round(values, 4), columns=NAMES)
    # Two columns are put on human units so that skipping standardisation is
    # visibly wrong rather than subtly wrong.
    frame["temp_c"] = np.round(42.0 + 3.0 * frame["temp_c"], 2)
    frame["pressure_kpa"] = np.round(310.0 + 25.0 * frame["pressure_kpa"], 2)
    frame.insert(0, "reading_id", np.arange(1, rows + 1))
    frame["machine"] = rng.choice(["A", "B", "C", "D"], size=rows)
    return frame


def main() -> None:
    frame = build(ROWS, SEED)
    frame.to_csv(OUT, index=False)
    print(f"wrote {OUT} - {len(frame):,} rows, {OUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
