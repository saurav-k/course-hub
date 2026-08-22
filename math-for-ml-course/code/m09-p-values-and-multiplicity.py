"""The p-value's job, and the jobs it gets by mistake.

DEFINITION. The p-value is the probability that the chosen test statistic would
be at least as extreme as the value observed, IF every model assumption were
correct, the test hypothesis included. Every clause carries weight. It is
computed under H0, so it cannot be a probability about H0.

THEOREM (under H0 a p-value is Uniform(0,1)). If the test statistic T has a
continuous distribution under H0 with CDF F, and the p-value is defined as
P = 1 - F(T), then P ~ Uniform(0,1) under H0.
PROOF. F(T) is the probability integral transform of T under its own
distribution, so F(T) ~ Uniform(0,1), and 1 - U is Uniform(0,1) when U is.
Formally, for u in (0,1),
    P(P <= u) = P(1 - F(T) <= u) = P(F(T) >= 1 - u) = 1 - (1 - u) = u.  []
Two consequences follow immediately and neither is optional:
  - P(p <= 0.05) = 0.05 under H0. That IS the definition of the alpha level.
  - m independent true nulls give P(at least one p <= alpha) = 1 - (1-alpha)^m,
    which climbs fast. This is the multiple-comparisons problem in one line.

BONFERRONI controls the family-wise error rate, the probability of ANY false
positive, by testing each hypothesis at alpha/m. It is exact enough and it gets
conservative fast.
PROOF. By the union bound, P(any false positive) <= sum over true nulls of
P(p_i <= alpha/m) = m_0 (alpha/m) <= alpha.  []

BENJAMINI-HOCHBERG controls the false discovery rate, the expected PROPORTION
of false positives among the rejections. Sort the p-values ascending, find the
largest i with p_(i) <= (i/m) q, and reject the first i. Under independence
this controls FDR at q. That is a weaker guarantee than Bonferroni's and it is
usually the one you actually want at scale: rejecting 100 things of which 5 are
wrong is often fine, and rejecting nothing is not.

WHAT THE NUMBER IS NOT. Not P(H0 true). Not the probability the result is due
to chance. Not a measure of effect size. Not a measure of importance. A large
p-value is not evidence for H0. These are the readings the program is built to
make impossible to keep.

Dataset: nimbus-sessions.csv, sliced into many meaningless subgroups so the
multiplicity problem happens rather than being described.

Needs numpy and pandas only.
"""

import math
import pathlib

import numpy as np
import pandas as pd

DATA = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "nimbus-sessions.csv"
SEED = 20260822


def normal_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def two_proportion_p(k_a: int, n_a: int, k_b: int, n_b: int) -> float:
    if n_a == 0 or n_b == 0:
        return 1.0
    pool = (k_a + k_b) / (n_a + n_b)
    if pool in (0.0, 1.0):
        return 1.0
    se = math.sqrt(pool * (1 - pool) * (1 / n_a + 1 / n_b))
    z = (k_b / n_b - k_a / n_a) / se
    return 2 * (1 - normal_cdf(abs(z)))


def benjamini_hochberg(pvals: np.ndarray, q: float) -> np.ndarray:
    m = pvals.size
    order = np.argsort(pvals)
    thresholds = (np.arange(1, m + 1) / m) * q
    passing = pvals[order] <= thresholds
    reject = np.zeros(m, dtype=bool)
    if passing.any():
        cutoff = int(np.flatnonzero(passing).max())
        reject[order[:cutoff + 1]] = True
    return reject


def main() -> None:
    rng = np.random.default_rng(SEED)

    print("1. UNDER H0 A P-VALUE IS UNIFORM. 40,000 tests where nothing is going on:")
    n = 4000
    a = rng.binomial(n, 0.05, size=40_000)
    b = rng.binomial(n, 0.05, size=40_000)
    pvals = np.array([two_proportion_p(int(x), n, int(y), n) for x, y in zip(a, b)])
    print(f"   {'bucket':>14}  {'share of p-values':>19}  {'expected if uniform':>21}")
    for lo, hi in ((0.0, 0.05), (0.05, 0.10), (0.10, 0.50), (0.50, 1.0)):
        share = float(np.mean((pvals >= lo) & (pvals < hi)))
        print(f"   [{lo:.2f}, {hi:.2f})  {share:>19.4f}  {hi - lo:>21.4f}")
    print(f"   share at or below 0.05: {float(np.mean(pvals <= 0.05)):.4f}")
    print("   A p-value below 0.05 is not rare when the null is TRUE. It happens one")
    print("   time in twenty by construction. That is what the threshold means.")

    print("\n2. SO RUNNING MORE TESTS MANUFACTURES FINDINGS")
    print(f"   {'metrics tested':>16}  {'P(at least one p<=0.05)':>25}  {'measured':>10}")
    for m in (1, 5, 10, 20, 40):
        analytic = 1 - 0.95 ** m
        blocks = pvals[: (40_000 // m) * m].reshape(-1, m)
        measured = float(np.mean((blocks <= 0.05).any(axis=1)))
        print(f"   {m:>16}  {analytic:>25.4f}  {measured:>10.4f}")
    print("   Twenty guardrail metrics on an experiment where nothing changed will")
    print("   show you a significant one about two times in three.")

    print("\n3. IT HAPPENS ON REAL DATA TOO: slice the sessions until something 'works'")
    df = pd.read_csv(DATA)
    # Assign a meaningless coin-flip label. By construction it affects nothing.
    df = df.assign(fake_arm=rng.integers(0, 2, size=len(df)))
    slices = []
    for region in sorted(df.region.unique()):
        for plan in sorted(df.plan.unique()):
            sub = df[(df.region == region) & (df.plan == plan)]
            arm0, arm1 = sub[sub.fake_arm == 0], sub[sub.fake_arm == 1]
            p = two_proportion_p(int(arm0.converted.sum()), len(arm0),
                                 int(arm1.converted.sum()), len(arm1))
            slices.append((f"{region}/{plan}", len(sub), p))
    slices.sort(key=lambda r: r[2])
    print(f"   {len(slices)} region-by-plan slices, split by a coin flip that changes nothing")
    print(f"   {'slice':>22}  {'n':>7}  {'p-value':>9}")
    for name, size, p in slices[:5]:
        print(f"   {name:>22}  {size:>7,}  {p:>9.4f}")
    hits = sum(1 for _, _, p in slices if p <= 0.05)
    print(f"   {hits} of {len(slices)} slices came in at or below 0.05.")
    print("   Reporting the best of these as a finding is p-hacking, and note that")
    print("   no step in it required dishonesty: each individual test was computed")
    print("   correctly. The error is choosing what to report after looking.")

    print("\n4. THE TWO CORRECTIONS, ON THOSE SLICES")
    ps = np.array([p for _, _, p in slices])
    m = ps.size
    bonf = ps <= 0.05 / m
    bh = benjamini_hochberg(ps, 0.05)
    print(f"   uncorrected at 0.05        rejects {int((ps <= 0.05).sum())} of {m}")
    print(f"   Bonferroni at 0.05/{m:<2}      rejects {int(bonf.sum())} of {m}"
          f"   (threshold {0.05 / m:.5f})")
    print(f"   Benjamini-Hochberg at q=0.05  rejects {int(bh.sum())} of {m}")
    print("   Both corrections reject nothing here, which is the right answer,")
    print("   because the label was a coin flip.")

    print("\n5. AND WHERE THEY DIFFER: twenty p-values, five of them genuinely small")
    mixed = np.concatenate([rng.uniform(0.0, 0.004, size=5), rng.uniform(0.0, 1.0, size=15)])
    m2 = mixed.size
    print(f"   {'rank':>5}  {'p-value':>9}  {'Bonferroni 0.05/m':>19}  {'BH (i/m)q':>11}  {'BH rejects':>11}")
    order = np.argsort(mixed)
    bh2 = benjamini_hochberg(mixed, 0.05)
    for rank, idx in enumerate(order[:8], start=1):
        print(f"   {rank:>5}  {mixed[idx]:>9.5f}  {0.05 / m2:>19.5f}"
              f"  {(rank / m2) * 0.05:>11.5f}  {str(bool(bh2[idx])):>11}")
    print(f"   Bonferroni rejects {int((mixed <= 0.05 / m2).sum())}, BH rejects {int(bh2.sum())}.")
    print("   BH's threshold rises with rank, so a run of small p-values supports")
    print("   each other. Bonferroni's does not, and it pays for that with power.")


if __name__ == "__main__":
    main()
