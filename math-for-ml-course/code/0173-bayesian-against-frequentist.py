"""Bayesian and frequentist as two working habits.

THE DISAGREEMENT, stated precisely. It is about what is random.
  FREQUENTIST  the parameter is a fixed unknown constant and the DATA is
               random. Probability statements therefore attach to procedures:
               "this rule produces an interval covering the truth 95 per cent
               of the time."
  BAYESIAN     the data is what it is and the PARAMETER carries a distribution
               representing what is known about it. Probability statements
               attach to the parameter: "given the model and the prior, there
               is a 95 per cent probability that p lies here."
Almost every confusion in this module is one of those sentences read in the
other's grammar.

THEOREM (conjugacy of the Beta prior for a Bernoulli likelihood). If
p ~ Beta(a, b) a priori and k successes are observed in n trials, then
    p | data  ~  Beta(a + k, b + n - k).
PROOF. The posterior is proportional to likelihood times prior:
    p^k (1-p)^(n-k) . p^(a-1) (1-p)^(b-1)  =  p^(a+k-1) (1-p)^(b+n-k-1),
which is the Beta(a + k, b + n - k) kernel. A density is determined by its
kernel, so that is the posterior.  []
The posterior mean is (a+k)/(a+b+n), which is a weighted average of the prior
mean a/(a+b) and the sample proportion k/n. The prior acts exactly like
a + b extra prior observations, which is the honest way to describe its
strength: not "belief" in the abstract, but a count.

THEOREM (MAP under a flat prior is the MLE). If p(theta) is constant on the
parameter space then log p(theta) is an additive constant, so
argmax [log L + log p] = argmax log L.  []
That is where the two schools meet: with a flat prior and plenty of data the
likelihood dominates and the two intervals land in nearly the same place. They
diverge exactly where the data is thin, which is where it matters most.

THE HONEST LIMITS, both ways.
  - A flat prior is a choice, not the absence of one, and flatness is not
    preserved under reparameterisation: uniform on p is not uniform on log-odds.
  - Bayesian practice as actually done is not pure induction. Model checking
    and model revision sit outside the updating formalism and are essential
    to it.

Dataset: experiment.csv and sessions.csv.

Needs numpy and pandas only.
"""

import math
import pathlib

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent.parent / "datasets"
URL_BASE = "https://<hub>/math-for-ml-course/datasets"


def data(name: str) -> str:
    """Local file when the repo is present, published URL when it is not.

    This is what lets the program be pasted straight into Colab.
    """
    local = HERE / name
    return str(local) if local.exists() else f"{URL_BASE}/{name}"
SEED = 20260822
Z95 = 1.959963985
DRAWS = 400_000


def wald(k: int, n: int) -> tuple[float, float]:
    p = k / n
    half = Z95 * math.sqrt(p * (1 - p) / n)
    return p - half, p + half


def credible(rng: np.random.Generator, a: float, b: float) -> tuple[float, float, float]:
    """Posterior quantiles by sampling, which is how real Bayesian work is done."""
    s = rng.beta(a, b, size=DRAWS)
    lo, hi = np.quantile(s, [0.025, 0.975])
    return float(lo), float(hi), float(s.mean())


def main() -> None:
    rng = np.random.default_rng(SEED)
    exp = pd.read_csv(data("experiment.csv"))
    t = exp.groupby("variant").converted.agg(["sum", "count"])
    k, n = int(t.loc["control", "sum"]), int(t.loc["control", "count"])

    print(f"the control arm: {k} conversions in {n:,} assigned users\n")

    print("1. THE SAME DATA, BOTH WAYS")
    lo_f, hi_f = wald(k, n)
    lo_b, hi_b, mean_b = credible(rng, 1 + k, 1 + n - k)
    print(f"   frequentist  95% confidence interval  [{lo_f:.6f}, {hi_f:.6f}]")
    print(f"   Bayesian     95% credible interval    [{lo_b:.6f}, {hi_b:.6f}]"
          f"   (Beta(1,1) prior)")
    print(f"   they differ by {abs(lo_f - lo_b) * 100:.4f} and {abs(hi_f - hi_b) * 100:.4f}"
          " percentage points at the ends")
    print("   Nearly the same numbers. NOT the same sentence:")
    print("     the confidence interval says the RULE covers p 95 per cent of the time;")
    print("     the credible interval says p is in this range with probability 0.95,")
    print("     given the model and the prior.")
    print("   The second is the sentence everyone wants. It costs a prior to say it.")

    print("\n2. THE PRIOR IS A COUNT OF IMAGINARY OBSERVATIONS")
    print(f"   {'prior':>22}  {'prior mean':>11}  {'= extra obs':>12}  {'posterior mean':>15}  {'95% credible':>26}")
    for label, a, b in (("Beta(1,1)   flat", 1, 1),
                        ("Beta(2,38)  ~5%, weak", 2, 38),
                        ("Beta(20,380) ~5%, firm", 20, 380),
                        ("Beta(50,50)  ~50%, wrong", 50, 50)):
        lo, hi, m = credible(rng, a + k, b + n - k)
        print(f"   {label:>22}  {a / (a + b):>11.4f}  {a + b:>12}  {m:>15.6f}"
              f"  [{lo:.6f}, {hi:.6f}]")
    print(f"   The sample proportion is {k / n:.6f}. With 12,000 observations a prior")
    print("   worth 40 or 400 barely moves the answer, and even a badly wrong prior")
    print("   worth 100 is dragged most of the way to the data. That is what")
    print("   'the likelihood dominates' means, in units you can count.")

    print("\n3. WHERE THEY GENUINELY DIVERGE: thin data")
    print(f"   {'k / n':>12}  {'frequentist Wald':>28}  {'Bayesian, flat prior':>28}")
    for k_s, n_s in ((0, 40), (1, 40), (3, 60), (55, 1000)):
        lo_f2, hi_f2 = wald(k_s, n_s) if k_s else (0.0, 0.0)
        lo_b2, hi_b2, _ = credible(rng, 1 + k_s, 1 + n_s - k_s)
        print(f"   {k_s:>4} / {n_s:<5}  [{lo_f2:>11.6f}, {hi_f2:>11.6f}]"
              f"  [{lo_b2:>11.6f}, {hi_b2:>11.6f}]")
    print("   At zero successes the frequentist Wald interval collapses to [0, 0],")
    print("   which claims certainty from no evidence. The Bayesian interval stays")
    print("   open and says the rate is somewhere below about 9 per cent, which is")
    print("   what 40 observations actually support. The schools agree once the data")
    print("   is plentiful and disagree exactly where the answer is hard.")

    print("\n4. A FLAT PRIOR IS A CHOICE, NOT ITS ABSENCE")
    flat_p = rng.uniform(0.0, 1.0, size=DRAWS)
    induced = np.log(flat_p / (1 - flat_p))
    print(f"   uniform on p           : mean {flat_p.mean():.4f}, "
          f"share in [0.4, 0.6] = {float(np.mean((flat_p > 0.4) & (flat_p < 0.6))):.4f}")
    flat_logit = rng.uniform(-6.0, 6.0, size=DRAWS)
    back = 1 / (1 + np.exp(-flat_logit))
    print(f"   uniform on log-odds    : mean {back.mean():.4f}, "
          f"share in [0.4, 0.6] = {float(np.mean((back > 0.4) & (back < 0.6))):.4f}")
    print("   Two priors, each 'uninformative' on its own scale, disagree about how")
    print("   much weight sits near one half. Flatness is not a property of ignorance,")
    print("   it is a property of a parameterisation, and choosing not to state a")
    print("   prior is not the same as not having one.")

    print("\n5. WHAT NEITHER SCHOOL AUTOMATES")
    print("   Both frameworks take the model as given. Neither the p-value nor the")
    print("   posterior tells you the Bernoulli model was right, that the arms were")
    print("   assigned independently, or that the metric measures what you care")
    print("   about. Checking those is outside both formalisms and is the part that")
    print("   most often decides whether the number meant anything.")


if __name__ == "__main__":
    main()
