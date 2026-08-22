"""Hypothesis testing: making the null do the work.

WHY THE NULL. You cannot compute under "there is an effect", because that is a
family of hypotheses with no single sampling distribution. You can compute
under "there is no effect", because it pins the distribution down completely.
That, and nothing more principled, is why the null gets to be the null.

THEOREM (the pooled two-proportion test). Under H0: p_A = p_B = p, with
independent samples of sizes n_A and n_B,
    Var(p_hat_A - p_hat_B) = p(1-p)(1/n_A + 1/n_B),
so the statistic
    Z = (p_hat_B - p_hat_A) / sqrt( p_pool(1 - p_pool)(1/n_A + 1/n_B) ),
    p_pool = (k_A + k_B)/(n_A + n_B),
is approximately standard normal for large samples.
PROOF. Each proportion is a sample mean of Bernoulli draws, so by the sample
mean theorem Var(p_hat_A) = p(1-p)/n_A and likewise for B. The two samples are
independent, so the variance of their difference is the sum of the variances,
which factorises as stated. Under H0 the two arms share one rate, so the best
estimate of it uses all the data, which is p_pool. The normal approximation is
the central limit theorem applied to each arm.  []

WHY POOLED. The standard error is computed UNDER H0, and H0 says the two rates
are equal. Using the two separate estimates instead answers a different
question, and it is the same error as reading two overlapping confidence
intervals as a verdict.

THE WORDING THAT MATTERS. When the test does not reject, the conclusion is
"the data is compatible with H0", never "H0 is true". A test never ACCEPTS the
null. That distinction is the difference between "we did not detect an effect"
and "we showed there is none", and only the first is ever earned.

Datasets: the predecessor course's own numbers (A 300/1000, B 340/1000) and
nimbus-experiment.csv.

Needs numpy and pandas only.
"""

import math
import pathlib

import numpy as np
import pandas as pd

DATA = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "nimbus-experiment.csv"
SEED = 20260822


def normal_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def two_proportion_test(k_a: int, n_a: int, k_b: int, n_b: int) -> dict[str, float]:
    p_a, p_b = k_a / n_a, k_b / n_b
    p_pool = (k_a + k_b) / (n_a + n_b)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    z = (p_b - p_a) / se
    return {"p_a": p_a, "p_b": p_b, "diff": p_b - p_a, "p_pool": p_pool,
            "se": se, "z": z, "p_value": 2 * (1 - normal_cdf(abs(z)))}


def show(title: str, k_a: int, n_a: int, k_b: int, n_b: int) -> dict[str, float]:
    r = two_proportion_test(k_a, n_a, k_b, n_b)
    print(f"   {title}")
    print(f"     A {k_a}/{n_a:,} = {r['p_a']:.5f}     B {k_b}/{n_b:,} = {r['p_b']:.5f}")
    print(f"     step 1  H0: p_A = p_B          H1: p_A != p_B")
    print(f"     step 2  alpha = 0.05, two-sided")
    print(f"     step 3  p_pool = ({k_a} + {k_b})/({n_a:,} + {n_b:,}) = {r['p_pool']:.5f}")
    print(f"             SE = sqrt(p_pool(1-p_pool)(1/n_A + 1/n_B)) = {r['se']:.6f}")
    print(f"             Z  = {r['diff']:.5f} / {r['se']:.6f} = {r['z']:.4f}")
    print(f"     step 4  |Z| against 1.96, or p = {r['p_value']:.4f} against 0.05")
    verdict = "REJECT H0" if r["p_value"] < 0.05 else "FAIL TO REJECT H0"
    print(f"     step 5  {verdict}")
    return r


def main() -> None:
    print("1. THE DEBT THE PREDECESSOR COURSE LEFT")
    print("   statistical-foundations-ml-course lesson 0005 computes two confidence")
    print("   intervals, notes they overlap, and says the proper two-proportion test")
    print("   is coming once hypothesis testing is built up. Its roadmap never builds")
    print("   it. Here it is.\n")
    r = show("grey button against gold button", 300, 1000, 340, 1000)
    print(f"\n     The overlap heuristic and the proper test agree on the verdict, but")
    print(f"     only the test tells you HOW close it was: p = {r['p_value']:.4f} is a hair")
    print("     above 0.05, not a comfortable null. 'Not established' is the honest")
    print("     report; 'no difference' would not be.")

    print("\n2. THE SAME TEST ON THE COMMITTED EXPERIMENT")
    exp = pd.read_csv(DATA)
    t = exp.groupby("variant").converted.agg(["sum", "count"])
    k_c, n_c = int(t.loc["control", "sum"]), int(t.loc["control", "count"])
    k_t, n_t = int(t.loc["treatment", "sum"]), int(t.loc["treatment", "count"])
    print()
    show("control against treatment", k_c, n_c, k_t, n_t)
    print("\n     The generator's true rates are 0.0500 and 0.0560, so there IS an")
    print("     effect and this test failed to find it. That is not a contradiction,")
    print("     it is what 54.6 per cent power means, and the next lesson computes")
    print("     that number before the experiment rather than after it.")

    print("\n3. POOLED AGAINST UNPOOLED, on the same numbers")
    p_a, p_b = k_c / n_c, k_t / n_t
    se_unpooled = math.sqrt(p_a * (1 - p_a) / n_c + p_b * (1 - p_b) / n_t)
    r2 = two_proportion_test(k_c, n_c, k_t, n_t)
    print(f"   SE under H0 (pooled)      {r2['se']:.6f}   z = {r2['z']:.4f}")
    print(f"   SE not assuming H0        {se_unpooled:.6f}   z = {(p_b - p_a) / se_unpooled:.4f}")
    print("   Close here because the two rates are close. The pooled one is correct")
    print("   FOR THE TEST, because the test computes everything under H0. The")
    print("   unpooled one is correct for a confidence interval on the difference,")
    print("   which does not assume H0. Same data, two standard errors, two jobs.")

    print("\n4. THE TWO WAYS TO BE WRONG, AND THE TRADE BETWEEN THEM")
    rng = np.random.default_rng(SEED)
    n = 12_000
    trials = 20_000
    print(f"   {'alpha':>7}  {'Type I rate when H0 true':>25}  {'power when p=0.050 vs 0.056':>29}")
    null = rng.binomial(n, 0.05, size=(trials, 2))
    alt_a = rng.binomial(n, 0.050, size=trials)
    alt_b = rng.binomial(n, 0.056, size=trials)
    for alpha, crit in ((0.10, 1.644854), (0.05, 1.959964), (0.01, 2.575829)):
        zs_null = np.array([two_proportion_test(int(a), n, int(b), n)["z"] for a, b in null[:4000]])
        zs_alt = np.array([two_proportion_test(int(a), n, int(b), n)["z"]
                           for a, b in zip(alt_a[:4000], alt_b[:4000])])
        print(f"   {alpha:>7.2f}  {float(np.mean(np.abs(zs_null) > crit)):>25.4f}"
              f"  {float(np.mean(np.abs(zs_alt) > crit)):>29.4f}")
    print("   Lowering alpha lowers the false-positive rate and lowers the power with")
    print("   it. At fixed n the two move together, and only more data buys both.")


if __name__ == "__main__":
    main()
