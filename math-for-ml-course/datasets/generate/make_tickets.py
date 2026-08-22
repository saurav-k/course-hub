"""Generate datasets/tickets.csv, the dataset every M01 program runs against.

Seeded and byte-reproducible: re-running this must leave the working tree clean.

    python3 make_tickets.py && git diff --exit-code

What is designed into the data, so that nobody mistakes it for evidence about
the world:

  * Token counts are heavy-tailed on purpose. Short tickets survive a naive
    product of per-token probabilities in float64 and long ones underflow to
    exactly 0.0, so lesson 0007 has a real cliff to point at rather than a
    hypothetical one.
  * ``first_response_seconds`` is exponential with a chosen median, so the
    relationship lambda = ln(2) / median in lesson 0006 is checkable against a
    number the generator put there.
  * ``score_urgent`` is a deliberately imperfect model score. Its AUC is good
    and not perfect, so lesson 0004 can show a monotone transform leaving AUC
    alone while accuracy at a fixed cutoff moves.
  * ``row_split`` is assigned per ROW, which is the bug lesson 0002 asks the
    reader to find: tickets from one customer land on both sides of the split.
  * The urgent and normal vocabularies overlap but differ in their weights, so
    a naive Bayes classifier built in lesson 0007 genuinely separates them.
"""

from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "tickets.csv"

SEED = 20260822
N_TICKETS = 5000
N_CUSTOMERS = 1000
MEDIAN_RESPONSE_SECONDS = 415.0

# A small closed vocabulary keeps the file a few megabytes rather than tens.
SHARED = [
    "account", "billing", "cannot", "charge", "click", "error", "help",
    "invoice", "login", "order", "page", "password", "payment", "please",
    "refund", "reset", "screen", "support", "thanks", "update",
]
URGENT_ONLY = [
    "outage", "down", "urgent", "critical", "blocked", "failing", "data",
    "loss", "breach", "production", "customers", "revenue", "escalate",
]
NORMAL_ONLY = [
    "question", "wondering", "curious", "someday", "minor", "cosmetic",
    "suggestion", "feedback", "typo", "documentation", "whenever", "nice",
]
VOCAB = SHARED + URGENT_ONLY + NORMAL_ONLY


def token_weights(rng: np.random.Generator, urgent: bool) -> np.ndarray:
    """Weights over VOCAB for one class, Zipf-ish so a few tokens dominate."""
    ranks = np.arange(1, len(VOCAB) + 1, dtype=float)
    weights = 1.0 / ranks
    shared_n, urgent_n = len(SHARED), len(URGENT_ONLY)
    if urgent:
        weights[shared_n:shared_n + urgent_n] *= 12.0
        weights[shared_n + urgent_n:] *= 0.08
    else:
        weights[shared_n:shared_n + urgent_n] *= 0.08
        weights[shared_n + urgent_n:] *= 12.0
    return weights / weights.sum()


def main() -> None:
    rng = np.random.default_rng(SEED)

    customer_id = rng.integers(1, N_CUSTOMERS + 1, size=N_TICKETS)
    is_urgent = rng.random(N_TICKETS) < 0.30

    # Heavy tail: lognormal, clipped, so most tickets are short and a real
    # minority are long enough to underflow a naive product.
    n_tokens = np.clip(
        np.round(rng.lognormal(mean=3.35, sigma=0.95, size=N_TICKETS)), 8, 600
    ).astype(int)

    urgent_w = token_weights(rng, urgent=True)
    normal_w = token_weights(rng, urgent=False)
    vocab = np.array(VOCAB)
    tokens = [
        " ".join(vocab[rng.choice(len(vocab), size=k, p=(urgent_w if u else normal_w))])
        for k, u in zip(n_tokens, is_urgent)
    ]

    # Exponential response times with the median we advertise.
    lam = np.log(2.0) / MEDIAN_RESPONSE_SECONDS
    first_response = rng.exponential(1.0 / lam, size=N_TICKETS)

    # An imperfect score: the true class plus noise, squashed into (0, 1).
    raw = np.where(is_urgent, 1.05, -1.05) + rng.normal(0.0, 1.0, size=N_TICKETS)
    score_urgent = 1.0 / (1.0 + np.exp(-raw))

    # Three-class logits for lesson 0005. Spam is a rare third class.
    is_spam = rng.random(N_TICKETS) < 0.05
    logit_urgent = np.where(is_urgent, 2.2, -0.6) + rng.normal(0, 0.8, N_TICKETS)
    logit_normal = np.where(is_urgent, -0.4, 2.0) + rng.normal(0, 0.8, N_TICKETS)
    logit_spam = np.where(is_spam, 2.6, -1.9) + rng.normal(0, 0.8, N_TICKETS)

    # Assigned per row, which is the bug lesson 0002 hunts.
    row_split = rng.choice(["train", "val", "test"], size=N_TICKETS, p=[0.7, 0.15, 0.15])

    frame = pd.DataFrame(
        {
            "ticket_id": np.arange(1, N_TICKETS + 1),
            "customer_id": customer_id,
            "row_split": row_split,
            "label": np.where(is_urgent, "urgent", "normal"),
            "n_tokens": n_tokens,
            "first_response_seconds": np.round(first_response, 2),
            "score_urgent": np.round(score_urgent, 5),
            "logit_urgent": np.round(logit_urgent, 4),
            "logit_normal": np.round(logit_normal, 4),
            "logit_spam": np.round(logit_spam, 4),
            "tokens": tokens,
        }
    )
    frame.to_csv(OUT, index=False, lineterminator="\n")
    print(f"wrote {OUT} - {len(frame):,} rows, {OUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
