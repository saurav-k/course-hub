"""Lesson 0130 - the uniform distribution, discrete and continuous.

Two halves, because the distribution has two forms.

Discrete: hash the request ids into 8 shards and check the result really is
uniform. Probability is computed from the definition, as a count over a count,
and compared against the 1/k the model predicts.

Continuous: Glorot and Bengio's published initialiser is uniform, and this
program computes its density from the formula and again from a histogram of
200,000 real draws. It also computes P(|W| < 0.01) two ways, once as a ratio of
widths and once as the empirical fraction, and asserts they agree.

The point of the continuous half is the number 6.53: a real, published,
widely-used initialiser has a probability density well above 1, and that is
fine, because probability is area.

Needs only numpy and pandas. Runs in a codebase, in Jupyter, or in Colab.
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "requests.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/requests.csv"
)

SEED = 20260822
DRAWS = 200_000
SHARDS = 8


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def glorot_bound(fan_in: int, fan_out: int) -> float:
    """The half-width of Glorot and Bengio's normalized initialisation, eq 16.

    W ~ U[-sqrt(6)/sqrt(fan_in + fan_out), +sqrt(6)/sqrt(fan_in + fan_out)].
    Note this is UNIFORM. The Gaussian initialiser people often mean is He et
    al. 2015, which Lesson 133 covers.
    """
    return float(np.sqrt(6.0) / np.sqrt(fan_in + fan_out))


def uniform_density(a: float, b: float) -> float:
    """f(u) = 1 / (b - a) on the interval, and 0 outside it."""
    return 1.0 / (b - a)


def probability_of_interval(a: float, b: float, low: float, high: float) -> float:
    """For a uniform, probability is width over width. No integral needed."""
    overlap = max(0.0, min(high, b) - max(low, a))
    return overlap / (b - a)


def main() -> None:
    frame = load()

    print("DISCRETE: 25,000 requests hashed into 8 shards")
    shard = frame["request_id"].to_numpy() % SHARDS
    counts = np.bincount(shard, minlength=SHARDS)
    print(f"    the model says each shard gets 1/{SHARDS} = {1 / SHARDS:.4f}")
    print(f"    and {len(frame):,} / {SHARDS} = {len(frame) / SHARDS:,.1f} requests")
    for index, count in enumerate(counts):
        print(f"      shard {index}: {count:5d} requests, "
              f"proportion {count / len(frame):.4f}")
    assert abs(counts.sum() - len(frame)) == 0, "a request went missing"
    print("    every shard is within a rounding of the prediction, because the")
    print("    ids are consecutive and the modulus spreads them exactly")

    print("\nCONTINUOUS: Glorot and Bengio's initialiser, a 512-to-512 layer")
    bound = glorot_bound(512, 512)
    width = 2 * bound
    density = uniform_density(-bound, bound)
    print(f"    bound   sqrt(6)/sqrt(1024) = {bound:.5f}")
    print(f"    width                      = {width:.5f}")
    print(f"    density 1 / width          = {density:.4f}   <- well above 1")
    print(f"    density x width            = {density * width:.4f}   <- the area is 1")

    rng = np.random.default_rng(SEED)
    weights = rng.uniform(-bound, bound, size=DRAWS)

    from_formula = probability_of_interval(-bound, bound, -0.01, 0.01)
    from_draws = float(np.mean(np.abs(weights) < 0.01))
    print(f"\n    P(|W| < 0.01) from the formula = {from_formula:.4f}")
    print(f"    P(|W| < 0.01) from {DRAWS:,} draws = {from_draws:.4f}")
    assert abs(from_formula - from_draws) < 0.005, "the two routes disagree"

    # An empirical density estimate: bin the draws and divide each bin's share
    # by the bin's width. A density is a probability PER UNIT, and this is what
    # that phrase means arithmetically.
    hist, edges = np.histogram(weights, bins=20)
    bin_width = float(edges[1] - edges[0])
    empirical_density = hist / DRAWS / bin_width
    print(f"\n    empirical density across 20 bins: "
          f"min {empirical_density.min():.3f}, max {empirical_density.max():.3f}")
    print(f"    exact density: {density:.3f} - flat, as a uniform must be")

    print(f"\n    mean     {weights.mean():+.6f}   formula (a+b)/2      = {0.0:+.6f}")
    print(f"    variance {weights.var():.8f}   formula (b-a)^2 / 12 = "
          f"{width ** 2 / 12:.8f}")

    print("\n    the same layer at 2048 to 2048, for contrast:")
    wider = glorot_bound(2048, 2048)
    print(f"      bound {wider:.5f}, density {uniform_density(-wider, wider):.2f}")
    print("      wider layers get smaller weights and a taller density,")
    print("      and the area under both is still exactly 1")


if __name__ == "__main__":
    main()
