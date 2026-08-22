"""Generate m05-scores.csv, the classifier score table for M05.

Twenty thousand held-out predictions from a binary classifier: the true label,
the model's logit, and the probability the logit maps to. Two lessons need it.

The integrals lesson needs an ROC curve with enough points that no reader could
sum its trapezoids by hand, so that the area has to be computed and can then be
checked a second way by counting ranked pairs. The chain-rule lesson needs real
logits to differentiate a cross-entropy against.

The positives and the negatives are drawn from overlapping normals on the logit
scale, which is what a real calibrated classifier produces and which puts the
area under the curve somewhere honest rather than at 0.99.

Reproducible: fixed seed, no wall-clock, no network.

    python3 make_m05_scores.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260822
ROWS = 20000
POSITIVE_RATE = 0.31

# Separation between the two logit distributions. This single number sets the
# area under the ROC curve, so it is the dial to turn if the area ever needs to
# move; everything else in the file follows from it.
POS_MEAN, POS_SD = 1.15, 1.35
NEG_MEAN, NEG_SD = -0.85, 1.30


def sigmoid(z: np.ndarray) -> np.ndarray:
    """Numerically safe logistic. exp of a large positive number overflows, so
    each half of the domain is evaluated in the form that cannot."""
    out = np.empty_like(z, dtype=float)
    positive = z >= 0
    out[positive] = 1.0 / (1.0 + np.exp(-z[positive]))
    exp_z = np.exp(z[~positive])
    out[~positive] = exp_z / (1.0 + exp_z)
    return out


def build() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)

    label = (rng.random(ROWS) < POSITIVE_RATE).astype(int)
    logit = np.where(
        label == 1,
        rng.normal(POS_MEAN, POS_SD, ROWS),
        rng.normal(NEG_MEAN, NEG_SD, ROWS),
    )

    return pd.DataFrame(
        {
            "label": label,
            "logit": logit.round(6),
            "score": sigmoid(logit).round(6),
        }
    )


def main() -> None:
    frame = build()
    out = Path(__file__).with_name("m05-scores.csv")
    frame.to_csv(out, index=False)
    positives = int(frame["label"].sum())
    print(f"wrote {out.name}: {len(frame)} rows, {out.stat().st_size / 1024:.0f} KB")
    print(f"positives {positives}, negatives {len(frame) - positives}")


if __name__ == "__main__":
    main()
