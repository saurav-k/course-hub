"""Survey sampling designs, and what each one buys.

Note the word collision this module has to hold. "Sampling" here means survey
design: how you choose which units of a real population to measure. Elsewhere
in the course it means drawing from a distribution. They are different topics.

THEOREM (simple random sampling is unbiased for the population mean). If a
sample of size n is drawn without replacement from a population of N units with
mean mu, then E[xbar] = mu.
PROOF. Let I_i be the indicator that unit i is in the sample. By symmetry every
unit is equally likely to be included, so E[I_i] = n/N for every i. Then
    E[ sum_i I_i x_i / n ] = (1/n) sum_i x_i E[I_i] = (1/n)(n/N) sum_i x_i = mu.  []

THEOREM (stratified sampling with proportional allocation never has larger
variance than simple random sampling of the same size). Writing the population
variance as the within-stratum part plus the between-stratum part,
    sigma^2 = sum_h W_h sigma_h^2  +  sum_h W_h (mu_h - mu)^2,
the proportionally allocated stratified estimator has variance approximately
(1/n) sum_h W_h sigma_h^2, while simple random sampling has approximately
sigma^2/n. The difference is the between-stratum term, which is a sum of
squares and so is never negative.
WHY IT MATTERS. Stratification removes the variation between strata from the
error, because it fixes the share of the sample each stratum receives instead
of letting chance decide it. The gain is large exactly when the strata means
differ a lot, and nil when they are identical.

CLUSTER SAMPLING moves the other way. Sampling whole clusters is cheaper per
unit and usually less precise, because units inside a cluster resemble each
other, so a cluster of size m carries less information than m independent
units. The program measures that loss rather than describing it.

Dataset: nimbus-population.csv. 30,000 units, four strata of deliberately
unequal size and spread, 600 clusters with within-cluster similarity built in.

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

DATA = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "nimbus-population.csv"
SAMPLE_SIZE = 600
TRIALS = 4000
SEED = 20260822


def main() -> None:
    pop = pd.read_csv(DATA)
    spend = pop["spend"].to_numpy(float)
    strata = pop["stratum"].to_numpy()
    clusters = pop["cluster"].to_numpy()
    n_pop = spend.size
    mu = float(spend.mean())

    print(f"population: {n_pop:,} units,  TRUE MEAN spend = {mu:.4f},  sd = {spend.std(ddof=0):.4f}")
    print("strata:")
    for name in sorted(set(strata)):
        sel = strata == name
        print(f"  {name:<10} N={int(sel.sum()):>6,}  W={sel.mean():.4f}"
              f"  mean={spend[sel].mean():>9.2f}  sd={spend[sel].std(ddof=1):>8.2f}")

    rng = np.random.default_rng(SEED)
    results: dict[str, np.ndarray] = {}

    # 1. Simple random sampling, without replacement.
    srs = np.empty(TRIALS)
    for t in range(TRIALS):
        idx = rng.choice(n_pop, size=SAMPLE_SIZE, replace=False)
        srs[t] = spend[idx].mean()
    results["simple random"] = srs

    # 2. Stratified, proportional allocation.
    names = sorted(set(strata))
    index_by_stratum = {h: np.flatnonzero(strata == h) for h in names}
    weights = {h: index_by_stratum[h].size / n_pop for h in names}
    alloc = {h: int(round(weights[h] * SAMPLE_SIZE)) for h in names}
    strat = np.empty(TRIALS)
    for t in range(TRIALS):
        total = 0.0
        for h in names:
            pick = rng.choice(index_by_stratum[h], size=alloc[h], replace=False)
            total += weights[h] * spend[pick].mean()
        strat[t] = total
    results["stratified (proportional)"] = strat

    # 3. Cluster sampling: take whole clusters until the budget is spent.
    cluster_ids = np.unique(clusters)
    members = {c: np.flatnonzero(clusters == c) for c in cluster_ids}
    mean_cluster_size = n_pop / cluster_ids.size
    n_clusters = max(int(round(SAMPLE_SIZE / mean_cluster_size)), 1)
    clus = np.empty(TRIALS)
    for t in range(TRIALS):
        chosen = rng.choice(cluster_ids, size=n_clusters, replace=False)
        idx = np.concatenate([members[c] for c in chosen])
        clus[t] = spend[idx].mean()
    results["cluster"] = clus

    print(f"\n{TRIALS:,} repeats of each design, about {SAMPLE_SIZE} units per sample")
    print(f"  (cluster sampling takes {n_clusters} whole clusters, mean size {mean_cluster_size:.1f})\n")
    print(f"{'design':>28}  {'E[estimate]':>13}  {'bias':>9}  {'sd of estimate':>15}  {'variance vs SRS':>16}")
    base = float(srs.var(ddof=1))
    for label, draws in results.items():
        v = float(draws.var(ddof=1))
        print(f"{label:>28}  {draws.mean():>13.4f}  {draws.mean() - mu:>9.4f}"
              f"  {np.sqrt(v):>15.4f}  {v / base:>15.3f}x")

    print("\n  All three designs are centred on the true mean: none of them is biased.")
    print("  They differ in spread, which is the whole point. Stratification fixes")
    print("  each stratum's share of the sample instead of letting chance set it,")
    print("  and this population's strata means run from about 240 to about 4,100,")
    print("  so there is a great deal of between-stratum variation to remove.")
    print("  Cluster sampling is worse than simple random here because units inside")
    print("  a cluster resemble one another, so each extra unit in a chosen cluster")
    print("  tells you less than a fresh independent unit would.")

    print("\nthe decomposition the stratified theorem turns on")
    within = sum(weights[h] * float(spend[index_by_stratum[h]].var(ddof=0)) for h in names)
    between = sum(weights[h] * (float(spend[index_by_stratum[h]].mean()) - mu) ** 2 for h in names)
    print(f"  within-stratum  sum W_h sigma_h^2      = {within:>14.4f}")
    print(f"  between-stratum sum W_h (mu_h - mu)^2  = {between:>14.4f}")
    print(f"  total                                  = {within + between:>14.4f}")
    print(f"  population variance                    = {float(spend.var(ddof=0)):>14.4f}")
    print(f"  the between-stratum share is {between / (within + between):.1%} of the total, and that is")
    print("  the part stratification takes off the table.")


if __name__ == "__main__":
    main()
