"""Generate the three datasets module M03 (linear algebra) teaches against.

Run from this directory:

    python3 make_m03_datasets.py

Everything is seeded, so two runs produce byte-identical files. The datasets are
deliberately large enough that no result in M03 can be checked by hand and small
enough to open in a spreadsheet: about 2.6 MB in total.

Only numpy and pandas are used, because every program in M03 has the same rule.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

SEED: int = 20260822
OUT_HOUSING: str = "housing.csv"
OUT_DOCUMENTS: str = "documents.csv"
OUT_POINTS: str = "points2d.csv"


def make_housing(rng: np.random.Generator, rows: int = 20_000) -> pd.DataFrame:
    """A housing table with a deliberate redundancy and a known linear truth.

    `area_sqft` and `area_k_sqft` are the same measurement in two units. That is
    what makes the rank lesson honest: the column is real, a person would plausibly
    add it, and it carries no new information at all.

    Price is built from a linear rule plus noise, so least squares has a true
    answer to recover rather than only a fitted one.
    """
    area_k = rng.gamma(shape=6.0, scale=0.32, size=rows) + 0.45
    bedrooms = np.clip(np.round(area_k * 1.55 + rng.normal(0, 0.55, rows)), 1, 7)
    bathrooms = np.clip(np.round(bedrooms * 0.55 + rng.normal(0, 0.4, rows)), 1, 5)
    age_years = np.clip(rng.gamma(shape=2.2, scale=13.0, size=rows), 0, 120)
    lot_sqft = area_k * 1000 * rng.uniform(1.4, 4.2, size=rows)

    # The truth the least-squares page recovers, in US dollars.
    price = (
        38_000.0
        + 232_000.0 * area_k
        + 43_000.0 * bedrooms
        + 21_000.0 * bathrooms
        - 900.0 * age_years
        + 3.1 * lot_sqft
        + rng.normal(0.0, 26_000.0, rows)
    )

    return pd.DataFrame(
        {
            "area_k_sqft": np.round(area_k, 4),
            "area_sqft": np.round(area_k * 1000.0, 1),
            "bedrooms": bedrooms.astype(int),
            "bathrooms": bathrooms.astype(int),
            "age_years": np.round(age_years, 2),
            "lot_sqft": np.round(lot_sqft, 1),
            "price_usd": np.round(price, 2),
        }
    )


TOPICS: tuple[str, ...] = ("machine_learning", "cooking", "astronomy", "football")

TERMS: tuple[str, ...] = (
    "model", "data", "loss", "gradient", "tensor", "training", "vector", "matrix",
    "recipe", "oven", "flour", "sauce", "simmer", "knife", "dough", "flavour",
    "orbit", "telescope", "galaxy", "spectrum", "comet", "nebula", "parsec", "eclipse",
    "striker", "offside", "penalty", "midfield", "keeper", "stadium", "kickoff", "referee",
    "the", "of", "and", "a", "to", "in", "is", "for",
)

# Each topic loads its own eight terms, and every document also draws the eight
# stopwords at the end, which is what makes raw dot products misleading.
TOPIC_BLOCK: dict[str, slice] = {
    "machine_learning": slice(0, 8),
    "cooking": slice(8, 16),
    "astronomy": slice(16, 24),
    "football": slice(24, 32),
}
STOPWORDS: slice = slice(32, 40)


def make_documents(rng: np.random.Generator, rows: int = 8_000) -> pd.DataFrame:
    """Word-count vectors for documents of wildly different lengths.

    Length is drawn independently of topic, so a long document about cooking has a
    larger dot product with everything than a short document about cooking does.
    That is the whole point of the cosine page and it has to be in the data.
    """
    topic_index = rng.integers(0, len(TOPICS), size=rows)
    length = rng.lognormal(mean=5.6, sigma=0.85, size=rows).astype(int) + 40

    counts = np.zeros((rows, len(TERMS)), dtype=np.int32)
    for row in range(rows):
        topic = TOPICS[topic_index[row]]
        block = TOPIC_BLOCK[topic]
        total = int(length[row])

        weights = np.full(len(TERMS), 0.004)
        weights[block] = 0.085
        weights[STOPWORDS] = 0.055
        weights = weights / weights.sum()
        counts[row] = rng.multinomial(total, weights)

    frame = pd.DataFrame(counts, columns=list(TERMS))
    frame.insert(0, "topic", [TOPICS[i] for i in topic_index])
    frame.insert(0, "doc_id", [f"d{i:05d}" for i in range(rows)])
    return frame


def make_points2d(rng: np.random.Generator, rows: int = 10_000) -> pd.DataFrame:
    """Ten thousand points in the plane, in three labelled groups.

    The linear-map page applies a rotation, a dilation, a shear and a singular
    matrix to all ten thousand at once, which is a thing no reader can do by hand
    and which makes "a matrix is a function" something they can watch happen.
    """
    per = rows // 2
    ring_angle = rng.uniform(0.0, 2.0 * np.pi, per)
    ring_radius = 1.0 + rng.normal(0.0, 0.045, per)
    ring = np.column_stack([ring_radius * np.cos(ring_angle), ring_radius * np.sin(ring_angle)])

    blob = rng.multivariate_normal([0.0, 0.0], [[0.055, 0.032], [0.032, 0.055]], rows - per)

    xy = np.vstack([ring, blob])
    group = np.array(["ring"] * per + ["blob"] * (rows - per))
    return pd.DataFrame({"x": np.round(xy[:, 0], 6), "y": np.round(xy[:, 1], 6), "group": group})


def main() -> None:
    rng = np.random.default_rng(SEED)

    housing = make_housing(rng)
    housing.to_csv(OUT_HOUSING, index=False)

    documents = make_documents(rng)
    documents.to_csv(OUT_DOCUMENTS, index=False)

    points = make_points2d(rng)
    points.to_csv(OUT_POINTS, index=False)

    for name, frame in ((OUT_HOUSING, housing), (OUT_DOCUMENTS, documents), (OUT_POINTS, points)):
        print(f"{name}: {frame.shape[0]:,} rows x {frame.shape[1]} columns")


if __name__ == "__main__":
    main()
