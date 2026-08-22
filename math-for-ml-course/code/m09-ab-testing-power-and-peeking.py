"""A/B testing in production: power before the test, and the stopping rule during it.

THEOREM (sample size for a two-proportion test). To detect a difference
delta = p_B - p_A at significance alpha (two-sided) and power 1 - beta, the
required size per arm is approximately
    n = ( z_{alpha/2} sqrt(2 p_bar (1 - p_bar))  +  z_beta sqrt(p_A(1-p_A) + p_B(1-p_B)) )^2 / delta^2
with p_bar = (p_A + p_B)/2.
PROOF SKETCH. Under H0 the test statistic is centred at 0 with standard error
se_0 = sqrt(2 p_bar(1-p_bar)/n); under H1 it is centred at delta with standard
error se_1 = sqrt((p_A(1-p_A) + p_B(1-p_B))/n). Rejection needs the observed
difference to exceed z_{alpha/2} se_0. Requiring that to happen with
probability 1 - beta under H1 gives
    delta  =  z_{alpha/2} se_0  +  z_beta se_1,
and both standard errors carry a 1/sqrt(n), so solving for n gives the stated
expression.  []
Read the delta^2 in the denominator: halving the effect you want to detect
multiplies the traffic you need by four.

THE PEEKING PROBLEM. A fixed-horizon p-value is valid for ONE look at a
pre-committed n. Monitoring daily and stopping the first time p dips below
0.05 is a different procedure with a different false-positive rate, and it is
much larger than alpha. Nothing in the arithmetic of any individual look is
wrong; the error is the stopping rule. The program measures the inflation.

THE FIX. A sequential boundary spends alpha across the looks instead of
spending it all at each one. O'Brien-Fleming makes early stopping demanding
and late stopping close to the fixed-horizon threshold, which matches the
intuition that stopping early should need stronger evidence.

Dataset: nimbus-experiment.csv, which is under-powered on purpose (0.546).

Needs numpy and pandas only.
"""

import math
import pathlib

import numpy as np
import pandas as pd

LOCAL = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "nimbus-experiment.csv"
URL = "https://<hub>/math-for-ml-course/datasets/nimbus-experiment.csv"
DATA = LOCAL if LOCAL.exists() else URL
SEED = 20260822
Z_ALPHA2 = 1.959963985
Z_BETA80 = 0.841621234
Z_BETA90 = 1.281551566


def normal_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def required_n(p_a: float, p_b: float, z_beta: float = Z_BETA80) -> float:
    delta = abs(p_b - p_a)
    p_bar = (p_a + p_b) / 2.0
    term = (Z_ALPHA2 * math.sqrt(2 * p_bar * (1 - p_bar))
            + z_beta * math.sqrt(p_a * (1 - p_a) + p_b * (1 - p_b)))
    return term ** 2 / delta ** 2


def power_at(p_a: float, p_b: float, n: int) -> float:
    delta = p_b - p_a
    p_bar = (p_a + p_b) / 2.0
    se0 = math.sqrt(2 * p_bar * (1 - p_bar) / n)
    se1 = math.sqrt((p_a * (1 - p_a) + p_b * (1 - p_b)) / n)
    return (1 - normal_cdf((Z_ALPHA2 * se0 - delta) / se1)) + normal_cdf((-Z_ALPHA2 * se0 - delta) / se1)


def z_from_counts(k_a: int, n_a: int, k_b: int, n_b: int) -> float:
    if n_a == 0 or n_b == 0:
        return 0.0
    pool = (k_a + k_b) / (n_a + n_b)
    if pool <= 0 or pool >= 1:
        return 0.0
    se = math.sqrt(pool * (1 - pool) * (1 / n_a + 1 / n_b))
    return (k_b / n_b - k_a / n_a) / se


def main() -> None:
    print("1. POWER IS A DECISION YOU MAKE BEFORE THE EXPERIMENT, NOT AFTER")
    base = 0.05
    print(f"   baseline conversion {base:.3f}")
    print(f"   {'relative lift':>14}  {'absolute delta':>15}  {'n per arm for 80%':>19}  {'for 90%':>12}")
    for rel in (0.20, 0.10, 0.05, 0.02, 0.01):
        p_b = base * (1 + rel)
        print(f"   {rel:>13.0%}  {p_b - base:>15.5f}  {required_n(base, p_b):>19,.0f}"
              f"  {required_n(base, p_b, Z_BETA90):>12,.0f}")
    print("   delta is squared in the denominator, so halving the lift you want to")
    print("   detect costs four times the traffic. A 1 per cent relative lift on a")
    print("   5 per cent baseline needs millions per arm. That is a budget fact")
    print("   before it is a statistics fact, and it is why most teams cannot test")
    print("   the small effects they most want to know about.")

    print("\n2. THE COMMITTED EXPERIMENT WAS UNDER-POWERED, AND THAT WAS KNOWABLE")
    exp = pd.read_csv(DATA)
    t = exp.groupby("variant").converted.agg(["sum", "count"])
    n_arm = int(t.loc["control", "count"])
    p_a, p_b = 0.0500, 0.0560       # the generator's true rates
    print(f"   true rates {p_a} and {p_b}, arm size {n_arm:,}")
    print(f"   power at that size          {power_at(p_a, p_b, n_arm):.4f}")
    print(f"   size needed for 80% power   {required_n(p_a, p_b):>10,.0f} per arm")
    print(f"   what actually happened      {int(t.loc['control', 'sum'])}/{n_arm:,}"
          f" against {int(t.loc['treatment', 'sum'])}/{n_arm:,},"
          f" z = {z_from_counts(int(t.loc['control','sum']), n_arm, int(t.loc['treatment','sum']), n_arm):.4f}")
    print("   The test missed a real effect. At 0.546 power that is close to a coin")
    print("   flip, and the number was computable before a single user was assigned.")

    print("\n3. PEEKING: the same data, a different stopping rule, a different test")
    rng = np.random.default_rng(SEED)
    trials, per_day, days = 4000, 900, 14
    fixed_hits = peek_hits = 0
    for _ in range(trials):
        # A pure null experiment: both arms at the same rate.
        a = rng.binomial(per_day, 0.05, size=days).cumsum()
        b = rng.binomial(per_day, 0.05, size=days).cumsum()
        n_cum = np.arange(1, days + 1) * per_day
        zs = np.array([z_from_counts(int(a[d]), int(n_cum[d]), int(b[d]), int(n_cum[d]))
                       for d in range(days)])
        fixed_hits += abs(zs[-1]) > Z_ALPHA2                 # look once, at the end
        peek_hits += bool((np.abs(zs) > Z_ALPHA2).any())     # look daily, stop when green
    print(f"   {trials:,} null experiments, {days} days, {per_day} users per arm per day")
    print(f"   look ONCE at the end      false positive rate {fixed_hits / trials:.4f}   (alpha = 0.05)")
    print(f"   look EVERY day, stop early  false positive rate {peek_hits / trials:.4f}")
    print(f"   The stopping rule roughly {peek_hits / max(fixed_hits, 1):.1f}x the error rate you signed up")
    print("   for. Every individual test was computed correctly. The procedure was not.")

    print("\n4. THE FIX: spend alpha across the looks instead of at each one")
    print("   O'Brien-Fleming style boundaries for a 7-look experiment:")
    looks = 7
    print(f"   {'look':>6}  {'information fraction':>21}  {'two-sided p cutoff':>20}")
    for k in range(1, looks + 1):
        frac = k / looks
        # OBF spending: z_k = Z_ALPHA2 / sqrt(information fraction)
        z_k = Z_ALPHA2 / math.sqrt(frac)
        p_k = 2 * (1 - normal_cdf(z_k))
        print(f"   {k:>6}  {frac:>21.4f}  {p_k:>20.3e}")
    print("   Day one demands a p-value orders of magnitude below 0.05 and the final")
    print("   look lands close to it. Early stopping has to clear a much higher bar,")
    print("   which is what makes the whole procedure keep its promised alpha.")
    print("   These cutoffs use the z/sqrt(t) approximation to the O'Brien-Fleming")
    print("   boundary, which gets the SHAPE right and is not the exact alpha-")
    print("   spending function a production platform would use. Take the shape from")
    print("   here and the exact boundary from a sequential-design reference.")

    print("\n5. THE BASE RATE, WHICH IS THE MOST USEFUL NUMBER IN THIS LESSON")
    print("   Published experimentation programmes report that most ideas fail: about")
    print("   a third of tested ideas at Microsoft improved the metric they targeted,")
    print("   and in well-optimised surfaces the rate is lower still. Plan for a")
    print("   portfolio of mostly-null results, and treat a spectacular effect from a")
    print("   tiny change as a data-quality alarm before treating it as a discovery.")


if __name__ == "__main__":
    main()
