"""0002 - Sets, and why most data bugs are set bugs.

Verifies the two theorems this lesson proves - inclusion-exclusion for two sets
and both De Morgan laws - against real data rather than on paper, then audits
the split in tickets.csv and finds the leakage the generator put there.

Needs only numpy and pandas.
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "tickets.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/tickets.csv"


def load() -> pd.DataFrame:
    """Relative to this file so the repository works offline, URL so Colab works."""
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def iou_from_definition(box_a: tuple, box_b: tuple) -> float:
    """Intersection over union, written as the two set operations it is."""
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b
    overlap_x = max(0, min(ax2, bx2) - max(ax1, bx1))
    overlap_y = max(0, min(ay2, by2) - max(ay1, by1))
    intersection = overlap_x * overlap_y
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    union = area_a + area_b - intersection      # inclusion-exclusion, exactly
    return intersection / union


def main() -> None:
    frame = load()

    # ---- inclusion-exclusion, checked on real sets -----------------------
    train = set(frame.loc[frame.row_split == "train", "customer_id"])
    test = set(frame.loc[frame.row_split == "test", "customer_id"])
    lhs = len(train | test)
    rhs = len(train) + len(test) - len(train & test)
    print("inclusion-exclusion on the customer sets")
    print(f"  card(train)            = {len(train)}")
    print(f"  card(test)             = {len(test)}")
    print(f"  card(train and test)   = {len(train & test)}")
    print(f"  card(train or test)    = {lhs}")
    print(f"  card(A)+card(B)-card(A and B) = {rhs}")
    assert lhs == rhs, "inclusion-exclusion failed"

    # ---- De Morgan, checked on real sets ---------------------------------
    universe = set(frame["customer_id"])
    left = universe - (train | test)
    right = (universe - train) & (universe - test)
    assert left == right, "first De Morgan law failed"
    left2 = universe - (train & test)
    right2 = (universe - train) | (universe - test)
    assert left2 == right2, "second De Morgan law failed"
    print("\nboth De Morgan laws hold on these sets")

    # ---- the leakage the split contains ----------------------------------
    both = train & test
    print("\nsplit audit")
    print(f"  tickets are disjoint across the split by construction")
    print(f"  customers in BOTH train and test: {len(both)} of {len(test)} test customers")
    print(f"  that is {len(both) / len(test):.1%} of the test customers already seen in training")
    assert len(both) > 0, "expected the per-row split to leak at the customer level"

    # The fix: partition by the leakage unit.
    rng = np.random.default_rng(11)
    customers = np.array(sorted(universe))
    held = set(rng.choice(customers, size=len(customers) // 5, replace=False).tolist())
    grouped_test = frame[frame.customer_id.isin(held)]
    grouped_train = frame[~frame.customer_id.isin(held)]
    overlap = set(grouped_train.customer_id) & set(grouped_test.customer_id)
    print(f"  after splitting BY CUSTOMER: {len(overlap)} customers in both")
    assert overlap == set(), "a grouped split must leave no customer on both sides"

    # ---- IoU, from the definition and vectorised -------------------------
    predicted, truth = (50, 60, 150, 200), (70, 50, 170, 220)
    by_definition = iou_from_definition(predicted, truth)
    a = np.array(predicted, dtype=float)
    b = np.array(truth, dtype=float)
    inter = np.prod(np.maximum(0.0, np.minimum(a[2:], b[2:]) - np.maximum(a[:2], b[:2])))
    areas = np.prod(a[2:] - a[:2]) + np.prod(b[2:] - b[:2])
    vectorised = inter / (areas - inter)
    print(f"\nIoU from the definition = {by_definition:.5f}")
    print(f"IoU vectorised          = {vectorised:.5f}")
    assert np.isclose(by_definition, vectorised)
    print(f"  PASCAL VOC counts a detection at IoU > 0.5, so this one {'counts' if by_definition > 0.5 else 'does not count'}")

    print("\nall assertions passed")


if __name__ == "__main__":
    main()
