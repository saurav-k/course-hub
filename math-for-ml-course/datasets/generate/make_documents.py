"""Generate documents.csv: word-count vectors whose length varies independently of topic.

The dataset behind the dot product and cosine page (M03). `sensors.csv` cannot
carry that lesson: the lesson is about two vectors pointing the same way at very
different magnitudes, and a sensor reading has no analogue of document length.

Three properties are designed in, and the third is the whole reason the file exists:

  - Four topics load eight topic words each, so the subjects are separable.
  - Every document also draws from eight shared stopwords at STOPWORD_WEIGHT, so
    the topics are NOT trivially separable and the cosine has something to do.
  - Length is drawn from a lognormal INDEPENDENTLY of topic, so the corpus holds
    52-word and 5,965-word documents on every subject. A long document about
    anything therefore has a large dot product with everything, which is what makes
    a raw dot product rank by length instead of by subject.

Measured on the committed output by code/0021-dot-product-and-cosine.py, over 500
random queries:

    ranked by raw dot product   the top ten share the query's topic  50.3% of the time
    ranked by cosine            the top ten share the query's topic 100.0% of the time

One document makes the mechanism visible on its own. d02546 is a 93-word astronomy
document. Its nearest neighbour by raw dot product is a 5,760-word FOOTBALL
document; by cosine it is a 179-word astronomy document.

The numbers are invented. No page cites this corpus as evidence about language.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

SEED: int = 20260822
OUT: Path = Path(__file__).resolve().parent.parent / "documents.csv"

TOPICS: tuple[str, ...] = ("machine_learning", "cooking", "astronomy", "football")

TERMS: tuple[str, ...] = (
    "model", "data", "loss", "gradient", "tensor", "training", "vector", "matrix",
    "recipe", "oven", "flour", "sauce", "simmer", "knife", "dough", "flavour",
    "orbit", "telescope", "galaxy", "spectrum", "comet", "nebula", "parsec", "eclipse",
    "striker", "offside", "penalty", "midfield", "keeper", "stadium", "kickoff", "referee",
    "the", "of", "and", "a", "to", "in", "is", "for",
)

TOPIC_BLOCK: dict[str, slice] = {
    "machine_learning": slice(0, 8),
    "cooking": slice(8, 16),
    "astronomy": slice(16, 24),
    "football": slice(24, 32),
}
STOPWORDS: slice = slice(32, 40)

# The single number that decides how badly a raw dot product misbehaves. At 0.14
# the eight shared stopwords take about a third of every document's mass, which is
# the right order for English: the ten commonest words are roughly a quarter of
# tokens in ordinary prose. It was chosen by sweeping it and measuring, not by eye.
STOPWORD_WEIGHT: float = 0.14


def build(rows: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    topic_index = rng.integers(0, len(TOPICS), size=rows)
    length = rng.lognormal(mean=5.6, sigma=0.85, size=rows).astype(int) + 40

    counts = np.zeros((rows, len(TERMS)), dtype=np.int32)
    for row in range(rows):
        weights = np.full(len(TERMS), 0.004)
        weights[TOPIC_BLOCK[TOPICS[topic_index[row]]]] = 0.085
        weights[STOPWORDS] = STOPWORD_WEIGHT
        counts[row] = rng.multinomial(int(length[row]), weights / weights.sum())

    frame = pd.DataFrame(counts, columns=list(TERMS))
    frame.insert(0, "topic", [TOPICS[i] for i in topic_index])
    frame.insert(0, "doc_id", [f"d{i:05d}" for i in range(rows)])
    return frame


def main() -> None:
    frame = build(rows=8_000, seed=SEED)
    frame.to_csv(OUT, index=False)
    print(f"{OUT}: {frame.shape[0]:,} rows x {frame.shape[1]} columns, {OUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
