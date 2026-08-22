"""Generate the three datasets module M10 (information, similarity, dimension) uses.

Seeded and byte-reproducible. The contract is:

    python3 make_m10.py && git diff --exit-code

A diff means an unseeded source of randomness crept in, which is a bug and not a
new dataset. Every number quoted on an M10 page that comes from these files was
read out of a run of this script.

Writes, relative to this file, into ../:

    m10_classifier.csv   20000 rows   a five-class classifier's held-out logits
    m10_signals.csv      12000 rows   a churn table with designed dependence
    m10_embeddings.csv    3000 rows   48-dimensional anisotropic embeddings

Needs numpy and pandas and nothing else.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

OUT = pathlib.Path(__file__).resolve().parent.parent
SEED = 20260822


# --------------------------------------------------------------------------
# 1. m10_classifier.csv
# --------------------------------------------------------------------------
# What is designed in, so nobody mistakes it for evidence about the world:
#
#   * Five classes with a deliberately uneven prior, so the label entropy is
#     below log2(5) = 2.3219 bits and a reader can see the gap.
#   * The true-class logit gets a margin drawn from a lognormal, so the model is
#     usually right by a comfortable distance and occasionally right by an
#     enormous one. That heavy tail is what puts 28.7 per cent of rows above the
#     float16 exp() ceiling of 11.0.
#   * The resulting reliability curve crosses: the model is UNDERconfident below
#     about 0.85 and OVERconfident above it. That was not designed in, it fell
#     out of the confident errors, and page 2 reports it as measured.
#   * Roughly 1 row in 12 is a confident error: the margin is given to a wrong
#     class instead. Those rows are what make the mean cross-entropy much worse
#     than the accuracy suggests, which is page 2's whole point.
#   * Logits are written unnormalised and uncentred, so the reader has to do the
#     max-subtraction themselves.

def make_classifier(rng: np.random.Generator) -> pd.DataFrame:
    n = 20000
    k = 5
    prior = np.array([0.40, 0.25, 0.20, 0.10, 0.05])
    true_class = rng.choice(k, size=n, p=prior)

    # A base score per class per row, before the margin is applied.
    logits = rng.normal(0.0, 1.0, size=(n, k))

    # Where the margin lands: the true class most of the time, a wrong class
    # for the confident errors.
    confident_error = rng.random(n) < (1.0 / 12.0)
    target = true_class.copy()
    wrong = (true_class + 1 + rng.integers(0, k - 1, size=n)) % k
    target[confident_error] = wrong[confident_error]

    margin = rng.lognormal(mean=1.05, sigma=0.55, size=n)
    logits[np.arange(n), target] += margin

    # A per-row offset the reader must not be allowed to ignore. Softmax is
    # invariant to it; a naive exp() is not.
    logits += rng.normal(6.0, 2.5, size=(n, 1))

    frame = pd.DataFrame(
        {"row_id": np.arange(n), "true_class": true_class},
    )
    for j in range(k):
        frame[f"logit_{j}"] = np.round(logits[:, j], 6)
    return frame


# --------------------------------------------------------------------------
# 2. m10_signals.csv
# --------------------------------------------------------------------------
# A churn table built so that four different things are simultaneously true and
# a reader can measure each one:
#
#   * plan          three values, genuinely predictive. Positive mutual
#                   information with churned, and the largest information gain
#                   of the honest columns.
#   * support_tier  four values, weakly predictive.
#   * theme         two values, independent of the label by construction, so its
#                   mutual information is zero up to sampling noise. This is the
#                   column that shows an estimate of zero is never exactly zero.
#   * account_ref   a near-unique identifier. It carries no information about the
#                   population and attains the maximum possible information gain
#                   on the sample. This column exists to make page 10's bias
#                   measurable rather than assertable.
#   * tenure_months, monthly_spend
#                   two continuous columns with a strong designed correlation, so
#                   Euclidean and Mahalanobis distance from the centre disagree.
#   * sessions_week a third continuous column on a completely different scale, so
#                   an unstandardised Euclidean distance is dominated by spend.

def make_signals(rng: np.random.Generator) -> pd.DataFrame:
    n = 12000

    plan = rng.choice(["basic", "pro", "enterprise"], size=n, p=[0.50, 0.35, 0.15])
    support_tier = rng.choice(["none", "email", "priority", "dedicated"], size=n,
                              p=[0.40, 0.30, 0.20, 0.10])
    theme = rng.choice(["light", "dark"], size=n, p=[0.55, 0.45])

    churn_p = np.select(
        [plan == "basic", plan == "pro", plan == "enterprise"],
        [0.42, 0.22, 0.08],
    )
    churn_p = churn_p + np.select(
        [support_tier == "none", support_tier == "email",
         support_tier == "priority", support_tier == "dedicated"],
        [0.06, 0.01, -0.03, -0.05],
    )
    churn_p = np.clip(churn_p, 0.01, 0.95)
    churned = (rng.random(n) < churn_p).astype(int)

    # Two correlated continuous columns. rho = 0.85 in standardised space.
    rho = 0.85
    z1 = rng.normal(size=n)
    z2 = rho * z1 + np.sqrt(1.0 - rho * rho) * rng.normal(size=n)
    tenure_months = np.clip(np.round(18.0 + 9.0 * z1, 1), 0.1, None)
    monthly_spend = np.clip(np.round(640.0 + 210.0 * z2, 2), 1.0, None)

    # A third column on a different scale entirely, mildly anti-correlated with churn.
    sessions_week = np.clip(np.round(11.0 - 4.0 * churned + 3.0 * rng.normal(size=n), 2), 0.0, None)

    # The identifier. Near-unique by construction: 11800 distinct values over
    # 12000 rows, so most values appear exactly once.
    account_ref = rng.choice(np.arange(100000, 111800), size=n, replace=True)

    return pd.DataFrame({
        "account_ref": account_ref,
        "plan": plan,
        "support_tier": support_tier,
        "theme": theme,
        "tenure_months": tenure_months,
        "monthly_spend": monthly_spend,
        "sessions_week": sessions_week,
        "churned": churned,
    })


# --------------------------------------------------------------------------
# 3. m10_embeddings.csv
# --------------------------------------------------------------------------
# A 48-dimensional embedding matrix built to reproduce, at a size a laptop can
# hold, the two geometric facts M10 pages 7 and 9 are about:
#
#   * ANISOTROPY. Every vector carries a large shared component along one common
#     direction, so two random rows have a high average cosine similarity. That
#     is the cone Ethayarajh measured in real contextual embeddings, put here
#     deliberately so the reader can measure the baseline and subtract it.
#   * LOW INTRINSIC DIMENSION. The informative part of each vector is a mixture
#     of 6 latent topic directions, so the points live near a 6-dimensional
#     subspace inside a 48-dimensional space. That is why nearest-neighbour
#     search still works here, and it is the escape clause page 9 is about.
#
# The topic label is committed so a reader can check that within-topic pairs
# really are closer, rather than taking it on trust.

def make_embeddings(rng: np.random.Generator) -> pd.DataFrame:
    n = 3000
    d = 48
    n_topics = 6

    common = rng.normal(size=d)
    common /= np.linalg.norm(common)

    topics = rng.normal(size=(n_topics, d))
    topics /= np.linalg.norm(topics, axis=1, keepdims=True)

    topic_id = rng.integers(0, n_topics, size=n)
    vectors = topics[topic_id] * 1.00
    vectors += rng.normal(0.0, 0.10, size=(n, d))       # within-topic spread
    vectors += 1.49 * common                            # the cone
    vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)

    frame = pd.DataFrame({"doc_id": np.arange(n), "topic": topic_id})
    for j in range(d):
        frame[f"e{j:02d}"] = np.round(vectors[:, j], 6)
    return frame


def main() -> None:
    rng = np.random.default_rng(SEED)
    # Order matters: each call advances the one generator, so the three files
    # are only reproducible together and in this order.
    written = [
        ("m10_classifier.csv", make_classifier(rng)),
        ("m10_signals.csv", make_signals(rng)),
        ("m10_embeddings.csv", make_embeddings(rng)),
    ]
    for name, frame in written:
        path = OUT / name
        frame.to_csv(path, index=False, lineterminator="\n")
        print(f"{name}: {len(frame)} rows, {len(frame.columns)} columns, "
              f"{path.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
