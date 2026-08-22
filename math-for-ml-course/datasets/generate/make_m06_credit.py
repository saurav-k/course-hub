"""Generate the M06 Optimization dataset: m06-credit.csv.

Seeded and reproducible. Run with:

    cd math-for-ml-course/datasets/generate
    python3 make_m06_credit.py

Writes ../m06-credit.csv: 20,000 rows, 12 feature columns, one binary
target and one continuous target.

The dataset is built to make this module's optimization lessons real rather
than illustrative, so three properties are deliberate and not accidental:

1. Feature scales span roughly six orders of magnitude, from a ratio in
   [0, 1] to a rupee income in the hundreds of thousands. That gives the
   design matrix a large condition number, which is what M06 L04 measures.
2. Two features are strongly correlated by construction. That is what makes
   the lasso's instability on correlated predictors observable in L11
   rather than merely asserted.
3. Four columns are pure noise, independent of both targets. A working
   L1 path has to drive their coefficients to exactly zero.

Nothing here is a real person or a real lender's book. It is generated.
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260822
N_ROWS = 20_000
OUT = Path(__file__).resolve().parent.parent / "m06-credit.csv"


def generate(seed: int = SEED, n_rows: int = N_ROWS) -> pd.DataFrame:
    """Build the frame. Returns the full table including both targets."""
    rng = np.random.default_rng(seed)

    # Monthly income in rupees, lognormal so the tail is long and positive.
    income_inr = np.round(np.exp(rng.normal(10.9, 0.55, n_rows)), 2)

    age_years = np.clip(np.round(rng.normal(37.0, 10.5, n_rows), 1), 21.0, 74.0)

    # Credit utilisation, a ratio in [0, 1]. Six orders of magnitude below income.
    utilisation_ratio = np.clip(rng.beta(2.2, 4.0, n_rows), 0.0, 1.0)

    enquiries_6m = rng.poisson(1.4, n_rows).astype(float)
    tenure_months = np.clip(np.round(rng.gamma(3.0, 22.0, n_rows)), 1.0, 400.0)

    # emi_to_income is correlated with utilisation by construction: the
    # lasso has to choose between two predictors that carry the same signal.
    emi_to_income = np.clip(
        0.72 * utilisation_ratio + rng.normal(0.0, 0.055, n_rows), 0.0, 1.0
    )

    late_payments_12m = rng.poisson(0.55 + 2.1 * utilisation_ratio, n_rows).astype(float)
    card_count = np.clip(rng.poisson(2.3, n_rows), 0, 12).astype(float)

    noise = rng.normal(0.0, 1.0, (n_rows, 4))

    # The true log-odds. Coefficients chosen so no single feature dominates
    # and so the intercept puts the default rate near a realistic 12%.
    # Every term is centred on its own mean, so the intercept alone sets the
    # base default rate and no coefficient has to absorb an offset.
    z = (
        -1.99
        - 1.35e-5 * (income_inr - 62_900.0)
        - 0.021 * (age_years - 37.0)
        + 2.30 * (utilisation_ratio - 0.355)
        + 0.28 * (enquiries_6m - 1.40)
        - 0.0042 * (tenure_months - 66.0)
        + 0.95 * (emi_to_income - 0.256)
        + 0.46 * (late_payments_12m - 1.30)
        + 0.055 * (card_count - 2.30)
    )
    default = rng.binomial(1, 1.0 / (1.0 + np.exp(-z))).astype(int)

    # A continuous target for the least-squares and ridge/lasso pages.
    credit_limit_inr = np.round(
        np.clip(
            2.35 * income_inr
            + 145.0 * tenure_months
            - 41_000.0 * utilisation_ratio
            - 8_600.0 * late_payments_12m
            + 1_950.0 * card_count
            + rng.normal(0.0, 14_500.0, n_rows),
            5_000.0,
            None,
        ),
        2,
    )

    frame = pd.DataFrame(
        {
            "income_inr": income_inr,
            "age_years": age_years,
            "utilisation_ratio": np.round(utilisation_ratio, 6),
            "enquiries_6m": enquiries_6m,
            "tenure_months": tenure_months,
            "emi_to_income": np.round(emi_to_income, 6),
            "late_payments_12m": late_payments_12m,
            "card_count": card_count,
            "noise_1": np.round(noise[:, 0], 6),
            "noise_2": np.round(noise[:, 1], 6),
            "noise_3": np.round(noise[:, 2], 6),
            "noise_4": np.round(noise[:, 3], 6),
            "default": default,
            "credit_limit_inr": credit_limit_inr,
        }
    )
    return frame


def main() -> None:
    frame = generate()
    frame.to_csv(OUT, index=False)
    print(f"wrote {OUT} - {len(frame):,} rows, {OUT.stat().st_size / 1024:.0f} KB")
    print(f"default rate: {frame['default'].mean():.4f}")
    print(f"correlation utilisation_ratio vs emi_to_income: "
          f"{frame['utilisation_ratio'].corr(frame['emi_to_income']):.4f}")


if __name__ == "__main__":
    main()
