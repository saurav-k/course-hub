"""Generate failures.csv - machine readings with a binary outcome that is
actually predictable.

## Why this dataset exists when two already do

`sessions.csv` and `sensors.csv` between them carry ten of M05's twelve pages,
and the module reuses them rather than adding. Two pages cannot use either.

The chain-rule page differentiates a cross-entropy, and the integrals page
builds an ROC curve and integrates it. Both need a **binary label with an
informative score**. `sensors.csv` has no label at all. `sessions.csv` has
`returning`, which is a boolean, but it is not predictable from the other
columns: fitting a logistic regression to it by Newton's method gives an area
under the ROC curve of 0.507, which is a coin flip. A page that built an ROC
lesson on a curve with no area would be teaching nothing, and manufacturing a
score column by thresholding a regression target would be worse, because a
classifier score and a regression target are different objects.

So this file adds exactly one dataset, and only for the two pages that need it.

## The teaching properties designed into it

- **The label is genuinely predictable, and not too predictable.** A logistic
  regression fitted on the four drivers reaches an area under the ROC curve of
  0.8781. Far enough above 0.5 that the curve has a visible shape, far enough
  below 1.0 that the curve is not a corner and the trapezoids have something to
  measure.
- **The label is sampled from its own probability**, never thresholded. So the
  model that generated the data is a logistic model, the Bayes-optimal scorer
  is known, and a page may honestly say what the best achievable area is.
- **`hours_since_service` enters through a logarithm** and `load_pct` through a
  square, so a reader who fits the raw columns gets a worse model than one who
  thinks about the functional form. That is a hook for later modules and costs
  this one nothing.
- **No ties in the fitted scores**, because the features are continuous. The
  ROC sweep therefore has one point per row, which is what makes the
  trapezoid-against-pair-count agreement exact rather than approximate.
- **Class balance is uneven but not extreme**, 17.0 per cent positive (3,401
  of 20,000), so the page on why the area survives a change in prevalence has
  something to reweight, and the imbalance is realistic for a failure label.

Reproducible: fixed seed, no wall-clock, no network. Re-running must leave
`git status` clean.

    python3 make_failures.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260822
ROWS = 20000

# The generating model, in one place because the lessons quote it as the truth
# a fitted model is trying to recover.
TRUE = {
    "intercept": -2.55,
    "log_hours": 0.92,
    "load_sq": 1.45,
    "vibration": 0.61,
    "coolant": -0.78,
}


def sigmoid(z: np.ndarray) -> np.ndarray:
    """Logistic function, evaluated in whichever algebraically equal form
    cannot overflow at the sign of z."""
    out = np.empty_like(z, dtype=float)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    e = np.exp(z[~pos])
    out[~pos] = e / (1.0 + e)
    return out


def build() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)

    hours_since_service = rng.gamma(shape=2.4, scale=180.0, size=ROWS).clip(1.0, 4000.0)
    load_pct = rng.beta(2.6, 2.2, ROWS) * 100.0
    vibration_mm_s = rng.lognormal(mean=np.log(2.1), sigma=0.55, size=ROWS).clip(0.1, 40.0)
    coolant_c = rng.normal(38.0, 6.5, ROWS).clip(12.0, 70.0)

    # Standardised drivers, so the coefficients above are on a comparable scale
    # and the target rate is easy to hold.
    log_hours = np.log(hours_since_service)
    drivers = {
        "log_hours": (log_hours - log_hours.mean()) / log_hours.std(),
        "load_sq": (
            (load_pct**2 - (load_pct**2).mean()) / (load_pct**2).std()
        ),
        "vibration": (
            np.log(vibration_mm_s) - np.log(vibration_mm_s).mean()
        ) / np.log(vibration_mm_s).std(),
        "coolant": (coolant_c - coolant_c.mean()) / coolant_c.std(),
    }

    logit = TRUE["intercept"] + sum(TRUE[k] * v for k, v in drivers.items())
    probability = sigmoid(logit)

    # Sampled, not thresholded. This is what makes the Bayes-optimal scorer
    # known and the label honest.
    failed = (rng.random(ROWS) < probability).astype(int)

    return pd.DataFrame(
        {
            "reading_id": np.arange(1, ROWS + 1),
            "hours_since_service": hours_since_service.round(1),
            "load_pct": load_pct.round(2),
            "vibration_mm_s": vibration_mm_s.round(3),
            "coolant_c": coolant_c.round(2),
            "failed": failed,
        }
    )


def main() -> None:
    frame = build()
    out = Path(__file__).resolve().parent.parent / "failures.csv"
    frame.to_csv(out, index=False)
    positives = int(frame["failed"].sum())
    print(f"wrote {out.name}: {len(frame)} rows, {out.stat().st_size / 1024:.0f} KB")
    print(f"positives {positives} ({100 * positives / len(frame):.1f}%), "
          f"negatives {len(frame) - positives}")


if __name__ == "__main__":
    main()
