"""Confidence intervals: what the ninety-five per cent is attached to.

DEFINITION. A 95 per cent confidence procedure is a rule that turns a sample
into an interval, such that intervals produced by that rule contain the true
parameter in 95 per cent of repetitions. The guarantee is a property of the
RULE across repetitions, not of any one interval it produced.

THEOREM (the Wald interval for a proportion has asymptotic coverage 1 - alpha).
If p_hat is the sample proportion from n independent Bernoulli(p) draws, then
by the central limit theorem
    Z = (p_hat - p) / sqrt(p(1-p)/n)  ->  Normal(0,1)  as n -> infinity,
so P(|Z| <= z) -> 1 - alpha with z the (1 - alpha/2) standard normal quantile.
Rearranging the event |p_hat - p| <= z sqrt(p(1-p)/n) for p, and substituting
p_hat for p inside the standard error, gives the interval
    p_hat  +/-  z sqrt(p_hat(1 - p_hat)/n).
The substitution is what makes the coverage asymptotic rather than exact, and
the program measures how badly it does when n is small or p is near an end.

WHAT THE INTERVAL DOES NOT SAY. Once computed, the interval is a fixed pair of
numbers and the parameter is a fixed number. It either contains it or it does
not. There is no 95 per cent left to attach to the one on your screen. Reading
it that way is the fallacy this page exists to prevent.

Datasets: nimbus-sessions.csv (converted) and nimbus-experiment.csv.

Needs numpy and pandas only.
"""

import math
import pathlib

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent.parent / "datasets"
SEED = 20260822
Z95 = 1.959963985
# Student t two-sided 0.975 quantiles, for the small-n comparison.
T975 = {4: 2.776445, 9: 2.262157, 29: 2.045230, 49: 2.009575, 199: 1.971957}


def normal_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def wald_interval(k: int, n: int, z: float = Z95) -> tuple[float, float]:
    p = k / n
    half = z * math.sqrt(p * (1 - p) / n)
    return p - half, p + half


def main() -> None:
    df = pd.read_csv(HERE / "nimbus-sessions.csv")
    conv = df["converted"].to_numpy(int)
    p_true = float(conv.mean())
    rng = np.random.default_rng(SEED)

    print(f"treat the column as the population: p = {p_true:.6f} over {conv.size:,} sessions\n")

    print("1. THE GUARANTEE IS ABOUT THE RULE. 20 intervals from 20 fresh samples of 800:")
    misses = 0
    for i in range(20):
        sample = rng.choice(conv, size=800, replace=False)
        lo, hi = wald_interval(int(sample.sum()), 800)
        covers = lo <= p_true <= hi
        misses += not covers
        flag = "        " if covers else "  MISS  "
        print(f"   {i + 1:>3}  [{lo:.5f}, {hi:.5f}]{flag}")
    print(f"   {20 - misses} of 20 covered. Each interval is either right or wrong;")
    print("   the 95 per cent describes the column, not any row in it.")

    print("\n2. COVERAGE, MEASURED OVER MANY REPEATS")
    print(f"   {'n':>7}  {'measured coverage':>18}  {'mean width':>12}")
    for n in (50, 200, 800, 3200):
        draws = rng.choice(conv, size=(20_000, n), replace=True)
        ks = draws.sum(axis=1)
        ps = ks / n
        half = Z95 * np.sqrt(ps * (1 - ps) / n)
        covered = np.mean((ps - half <= p_true) & (p_true <= ps + half))
        print(f"   {n:>7}  {covered:>18.4f}  {float(2 * half.mean()):>12.6f}")
    print("   The nominal level is 0.95 and the small-n rows fall short of it. That")
    print("   is the substitution of p_hat for p inside the standard error, and it")
    print("   bites hardest when n p is small, which is exactly the conversion-rate")
    print("   case: at n = 50 and p near 0.055 most samples contain no conversions")
    print("   at all, and an interval of zero width cannot cover anything.")

    print("\n3. WHERE THE WALD INTERVAL EMBARRASSES ITSELF")
    for k, n in ((0, 40), (1, 40), (3, 40)):
        lo, hi = wald_interval(k, n) if k else (0.0, 0.0)
        print(f"   {k} conversions in {n}:  p_hat = {k / n:.4f}   interval [{lo:.5f}, {hi:.5f}]"
              f"   width {hi - lo:.5f}")
    print("   Zero successes gives the interval [0, 0]: perfect certainty from no")
    print("   evidence. Any honest procedure has to widen there, and this one cannot.")
    print("   Report a rule-of-three bound or an exact interval when k is small.")

    print("\n4. z AGAINST t: when the difference is worth the trouble")
    print(f"   {'n':>6}  {'df':>5}  {'z multiplier':>13}  {'t multiplier':>13}  {'t interval wider by':>21}")
    for n in (5, 10, 30, 50, 200):
        df_ = n - 1
        t = T975[df_]
        print(f"   {n:>6}  {df_:>5}  {Z95:>13.6f}  {t:>13.6f}  {t / Z95 - 1:>20.2%}")
    print("   With sigma unknown the multiplier comes from t, and at n = 5 the normal")
    print("   interval is 42 per cent too narrow. Comparing two models over ten seeds")
    print("   is the n = 10 row, not the n = 200 row.")

    print("\n5. A REAL COMPARISON: two arms of the committed experiment")
    exp = pd.read_csv(HERE / "nimbus-experiment.csv")
    table = exp.groupby("variant").converted.agg(["sum", "count"])
    for variant, row in table.iterrows():
        k, n = int(row["sum"]), int(row["count"])
        lo, hi = wald_interval(k, n)
        print(f"   {variant:<10} {k:>4}/{n:,}  p_hat = {k / n:.5f}   95% CI [{lo:.5f}, {hi:.5f}]")
    print("   The two intervals overlap. That is NOT a verdict: overlap does not")
    print("   establish the absence of a difference, because the right comparison")
    print("   uses the standard error of the DIFFERENCE, not the two separate ones.")
    print("   The next lesson does that test properly.")


if __name__ == "__main__":
    main()
