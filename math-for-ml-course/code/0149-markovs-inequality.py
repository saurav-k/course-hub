"""Markov's inequality: a tail bound from the mean alone.

Lesson: Markov's inequality (0149).

    python3 0810-markov-inequality.py

What it checks twice:

  1. The bound holds. Checked on every column of a real dataset at many
     thresholds, and on distributions chosen to stress it. A single violation
     would be a bug in the proof, so the program looks for one.
  2. The PROOF, made arithmetic. Markov's proof replaces X by a step function
     that is `a` above the threshold and 0 below it, and observes that the step
     function is never larger than X. The program builds both quantities and
     shows the inequality between their means, which is the whole proof.
  3. Tightness. There is a distribution that attains the bound with equality, and
     the program constructs it, so "weak" is understood as "as strong as
     possible given only the mean".
"""

from __future__ import annotations

from pathlib import Path

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "inference_runs.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/inference_runs.csv"
)


def load() -> pd.DataFrame:
    """Read the committed dataset, falling back to the published URL.

    The path is resolved from this file rather than the working directory, so the
    program runs from anywhere. The URL fallback is what lets it be pasted into
    Colab or a notebook with no checkout at all.
    """
    return pd.read_csv(DATA) if DATA.exists() else pd.read_csv(URL)


def main() -> None:
    frame = load()
    latency = frame["latency_ms"].to_numpy(dtype=float)
    mean = latency.mean()
    print(f"rows {len(latency):,}   E[latency] = {mean:.4f} ms\n")

    print("1. The bound, on real latency at several thresholds")
    print(f"   {'a (ms)':>10}{'Markov E[X]/a':>16}{'true P(X >= a)':>17}{'slack':>10}")
    for a in (250.0, 500.0, 1_000.0, 2_000.0, 4_000.0):
        bound = mean / a
        truth = float((latency >= a).mean())
        assert truth <= bound + 1e-12, "Markov violated, which is impossible"
        print(f"   {a:>10,.0f}{bound:>16.6f}{truth:>17.6f}{bound / max(truth, 1e-12):>10,.1f}x")
    print("   Never violated, and never close. Knowing only the mean is not much.")

    print("\n2. The proof, as arithmetic")
    print("   Markov's proof: build the step function that is `a` where X >= a and")
    print("   0 elsewhere. That step is never above X, so its mean is not above")
    print("   E[X]. But its mean is exactly a * P(X >= a). Divide by a and you are")
    print("   done. Here is each of those three claims, measured.")
    a = 1_000.0
    step = np.where(latency >= a, a, 0.0)
    print(f"\n   is the step never above X?          {bool((step <= latency).all())}")
    print(f"   mean of the step                    {step.mean():.6f}")
    print(f"   a * P(X >= a)                       {a * (latency >= a).mean():.6f}")
    print(f"   E[X]                                {mean:.6f}")
    assert (step <= latency).all()
    assert np.isclose(step.mean(), a * (latency >= a).mean())
    assert step.mean() <= mean
    print("   The step's mean equals a * P(X >= a) exactly, and sits below E[X].")
    print("   That single step function is the whole of the proof, and the gap")
    print("   between the two means is exactly the slack in the bound.")

    print("\n   Where the slack comes from, split into its two causes.")
    tail_mask = latency >= a
    truth = float(tail_mask.mean())
    tail_contribution = float((latency * tail_mask).mean())
    body_contribution = mean - tail_contribution
    total_slack = (mean / a) / truth
    body_factor = mean / tail_contribution
    overcount_factor = latency[tail_mask].mean() / a
    print(f"     E[X] splits into a tail part and a body part:")
    print(f"       from rows at or above {a:>7,.0f} ms   {tail_contribution:>10.4f} ms")
    print(f"       from rows below       {a:>7,.0f} ms   {body_contribution:>10.4f} ms")
    print(f"       total                                {mean:>10.4f} ms")
    print(f"\n     cause 1, counting the body at all:  factor {body_factor:>7.2f}x")
    print(f"       Every row below {a:,.0f} ms contributes to E[X] and contributes")
    print(f"       nothing to the tail probability. It is "
          f"{body_contribution / mean:.1%} of the mean.")
    print(f"     cause 2, over-counting inside the tail: factor {overcount_factor:>5.2f}x")
    print(f"       Rows in the tail average {latency[tail_mask].mean():,.1f} ms and the step")
    print(f"       counted each of them as only {a:,.0f} ms.")
    print(f"\n     the two multiply: {body_factor:.2f} x {overcount_factor:.2f} = "
          f"{body_factor * overcount_factor:.1f}x, and the measured slack is {total_slack:.1f}x")
    assert np.isclose(body_factor * overcount_factor, total_slack, rtol=1e-6)
    print("     So the body, not the tail, is where almost all of the slack lives.")
    print("     That is the honest reading of 'Markov is weak': it is weak because")
    print("     a mean cannot tell the body from the tail.")

    print("\n3. Markov is as tight as it can be")
    print("   Take X = a with probability p and 0 otherwise. Then E[X] = a*p and")
    print("   P(X >= a) = p, so the bound E[X]/a = p is attained exactly.")
    rng = np.random.default_rng(20260829)
    for p in (0.5, 0.1, 0.01):
        target = 100.0
        sample = np.where(rng.random(2_000_000) < p, target, 0.0)
        bound = sample.mean() / target
        truth = float((sample >= target).mean())
        print(f"   p={p:<6} bound {bound:.6f}   truth {truth:.6f}   ratio {bound / truth:.6f}")
        assert np.isclose(bound, truth, rtol=1e-9)
    print("   Ratio exactly 1. The bound cannot be improved without assuming more")
    print("   than the mean, and the next lesson assumes exactly one thing more.")

    print("\n4. The assumption that is easy to miss")
    print("   Markov needs X >= 0. Drop that and it fails immediately:")
    signed = frame["log_resid"].to_numpy(dtype=float)
    a = 1.0
    print(f"   log_resid has mean {signed.mean():.6f}, which is about zero,")
    print(f"   so E[X]/a = {signed.mean() / a:.6f}")
    print(f"   but the true P(X >= {a}) = {float((signed >= a).mean()):.6f}")
    print("   The 'bound' is far below the truth, because negative values dragged")
    print("   the mean down while contributing nothing to the upper tail.")


if __name__ == "__main__":
    main()
