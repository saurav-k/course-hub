"""Inference in simple linear regression: a fitted slope is an estimate.

MODEL. Y_i = alpha + beta x_i + e_i, with the x_i treated as fixed and the
e_i independent Normal(0, sigma^2).

THEOREM (least squares is the MLE here). Maximising the Gaussian likelihood in
(alpha, beta) is minimising sum_i (y_i - alpha - beta x_i)^2, because those are
the only terms containing alpha and beta and they enter with a negative sign.
The solutions are
    B = S_xY / S_xx,        A = ybar - B xbar,
with S_xx = sum_i (x_i - xbar)^2 and S_xY = sum_i (x_i - xbar)(Y_i - ybar).

THEOREM (the slope's sampling distribution). B ~ Normal(beta, sigma^2 / S_xx).
PROOF. B is linear in the responses: writing w_i = (x_i - xbar)/S_xx, we have
B = sum_i w_i Y_i, because sum_i w_i = 0 makes the ybar term drop out. Then
    E[B] = sum_i w_i (alpha + beta x_i) = alpha sum_i w_i + beta sum_i w_i x_i = beta,
using sum_i w_i = 0 and sum_i w_i x_i = 1. And by independence
    Var(B) = sum_i w_i^2 sigma^2 = sigma^2 sum_i (x_i - xbar)^2 / S_xx^2 = sigma^2 / S_xx.
A linear combination of independent normals is normal.  []
Read Var(B) = sigma^2/S_xx: spreading your x values out buys precision on the
slope, which is a design lever, not a data accident.

THEOREM (the unbiased noise estimate). E[SSE/(n-2)] = sigma^2, where
SSE = sum_i (Y_i - A - B x_i)^2, and in fact SSE/sigma^2 ~ chi-square(n-2).
WHY n-2. Two parameters were fitted to the same data, so two degrees of
freedom are spent. It is the n-1 of the sample variance with one more
parameter estimated. Since sigma is unknown, replacing it by its estimate
turns the slope's z into a t:
    T = (B - beta) / sqrt( (SSE/(n-2)) / S_xx )  ~  t with n-2 degrees of freedom.

THE TWO INTERVALS THAT ARE NOT THE SAME. At a new x0, the interval for the
MEAN response carries sqrt(1/n + (x0 - xbar)^2/S_xx), while the interval for a
single new OBSERVATION carries sqrt(1 + 1/n + (x0 - xbar)^2/S_xx). The extra 1
is the irreducible noise of the new draw, and it is why a prediction interval
is much wider than a confidence band and does not shrink towards zero as n
grows. Both are widest far from xbar, which is the mathematics telling you not
to extrapolate.

Dataset: nimbus-adspend.csv, generated as
revenue_k = 12.5 + 3.20 * ad_spend_k + Normal(0, 8.0), so every estimate can be
checked against the truth.

Needs numpy and pandas only.
"""

import math
import pathlib

import numpy as np
import pandas as pd

LOCAL = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "nimbus-adspend.csv"
URL = "https://<hub>/math-for-ml-course/datasets/nimbus-adspend.csv"
DATA = LOCAL if LOCAL.exists() else URL
TRUE_INTERCEPT, TRUE_SLOPE, TRUE_SIGMA = 12.5, 3.20, 8.0
SEED = 20260822
# Two-sided 0.975 t quantiles.
T975 = {8: 2.306004, 18: 2.100922, 48: 2.010635, 198: 1.972017, 1998: 1.961151}


def fit(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    n = x.size
    sxx = float(((x - x.mean()) ** 2).sum())
    sxy = float(((x - x.mean()) * (y - y.mean())).sum())
    b = sxy / sxx
    a = float(y.mean() - b * x.mean())
    sse = float(((y - a - b * x) ** 2).sum())
    sigma2 = sse / (n - 2)
    return {"n": n, "a": a, "b": b, "Sxx": sxx, "SSE": sse,
            "sigma2": sigma2, "se_b": math.sqrt(sigma2 / sxx),
            "se_a": math.sqrt(sigma2 * (1.0 / n + x.mean() ** 2 / sxx))}


def main() -> None:
    ads = pd.read_csv(DATA)
    x = ads["ad_spend_k"].to_numpy(float)
    y = ads["revenue_k"].to_numpy(float)
    f = fit(x, y)
    n = int(f["n"])
    tcrit = T975[1998]

    print(f"n = {n:,} weeks.  truth: revenue = {TRUE_INTERCEPT} + {TRUE_SLOPE} * spend,"
          f" sigma = {TRUE_SIGMA}\n")
    print("1. THE FIT, AND THE THREE NUMBERS THAT MAKE IT AN ESTIMATE")
    print(f"   slope     B = {f['b']:.6f}     true beta  = {TRUE_SLOPE}")
    print(f"   intercept A = {f['a']:.6f}     true alpha = {TRUE_INTERCEPT}")
    print(f"   S_xx        = {f['Sxx']:.4f}")
    print(f"   SSE         = {f['SSE']:.4f}")
    print(f"   sigma_hat^2 = SSE/(n-2) = {f['sigma2']:.6f}   true sigma^2 = {TRUE_SIGMA ** 2}")
    print(f"   se(B) = sqrt(sigma_hat^2 / S_xx) = {f['se_b']:.6f}")

    print("\n2. THE TEST ON THE SLOPE")
    t_stat = f["b"] / f["se_b"]
    print(f"   H0: beta = 0     T = B/se(B) = {t_stat:.4f}   against t({n - 2}, 0.975) = {tcrit:.4f}")
    print(f"   REJECT H0 by a wide margin, as we should: the truth is {TRUE_SLOPE}.")
    lo, hi = f["b"] - tcrit * f["se_b"], f["b"] + tcrit * f["se_b"]
    print(f"   95% CI for beta:  [{lo:.6f}, {hi:.6f}]"
          f"   contains {TRUE_SLOPE}: {lo <= TRUE_SLOPE <= hi}")

    print("\n3. WHY n-2, DEMONSTRATED")
    rng = np.random.default_rng(SEED)
    print(f"   {'divisor':>10}  {'E[SSE/divisor]':>16}  {'true sigma^2':>13}")
    m = 12
    xs = np.linspace(2.0, 60.0, m)
    sses = np.empty(20_000)
    for r in range(20_000):
        ys = TRUE_INTERCEPT + TRUE_SLOPE * xs + rng.normal(0.0, TRUE_SIGMA, size=m)
        sses[r] = fit(xs, ys)["SSE"]
    for label, div in (("n", m), ("n-1", m - 1), ("n-2", m - 2), ("n-3", m - 3)):
        print(f"   {label:>10}  {float((sses / div).mean()):>16.4f}  {TRUE_SIGMA ** 2:>13.4f}")
    print("   Only n-2 lands on the truth. One degree of freedom went on the")
    print("   intercept and one on the slope.")

    print("\n4. THE SLOPE'S SAMPLING DISTRIBUTION, MEASURED")
    bs = np.empty(20_000)
    for r in range(20_000):
        ys = TRUE_INTERCEPT + TRUE_SLOPE * xs + rng.normal(0.0, TRUE_SIGMA, size=m)
        bs[r] = fit(xs, ys)["b"]
    sxx_design = float(((xs - xs.mean()) ** 2).sum())
    print(f"   E[B]      {bs.mean():.6f}   true beta {TRUE_SLOPE}")
    print(f"   sd(B)     {bs.std(ddof=1):.6f}   predicted sqrt(sigma^2/S_xx)"
          f" = {math.sqrt(TRUE_SIGMA ** 2 / sxx_design):.6f}")

    print("\n5. SPREADING THE x VALUES OUT IS A DESIGN LEVER")
    print(f"   {'x range':>18}  {'S_xx':>12}  {'se(B)':>10}  {'vs narrowest':>13}")
    ses = []
    for lo_x, hi_x in ((28.0, 34.0), (20.0, 42.0), (2.0, 60.0)):
        xd = np.linspace(lo_x, hi_x, m)
        sxx_d = float(((xd - xd.mean()) ** 2).sum())
        se_d = math.sqrt(TRUE_SIGMA ** 2 / sxx_d)
        ses.append(se_d)
        print(f"   [{lo_x:>5.1f}, {hi_x:>5.1f}]  {sxx_d:>12.4f}  {se_d:>10.6f}"
              f"  {ses[0] / se_d:>12.1f}x")
    print(f"   Same number of weeks and the same noise, and the widest design is")
    print(f"   {ses[0] / ses[-1]:.1f} times as precise on the slope as the narrowest, purely from")
    print("   choosing where to spend. S_xx is under your control in a way that")
    print("   sigma is not, and se(B) = sigma/sqrt(S_xx) is where that control acts.")

    print("\n6. THE TWO INTERVALS AT A NEW POINT, AND WHY ONLY ONE SHRINKS")
    xbar = float(x.mean())
    print(f"   xbar = {xbar:.3f}\n")
    print(f"   {'x0':>8}  {'fitted':>10}  {'CI for the mean':>26}  {'PI for one new week':>28}")
    for x0 in (10.0, xbar, 50.0, 90.0):
        pred = f["a"] + f["b"] * x0
        core = 1.0 / n + (x0 - xbar) ** 2 / f["Sxx"]
        half_ci = tcrit * math.sqrt(f["sigma2"] * core)
        half_pi = tcrit * math.sqrt(f["sigma2"] * (1.0 + core))
        note = "  <- extrapolation" if x0 > x.max() else ""
        print(f"   {x0:>8.2f}  {pred:>10.3f}  [{pred - half_ci:>10.3f}, {pred + half_ci:>9.3f}]"
              f"  [{pred - half_pi:>10.3f}, {pred + half_pi:>9.3f}]{note}")
    print("   The mean interval is narrowest at xbar and flares either side, because")
    print("   of the (x0 - xbar)^2 term. The prediction interval carries an extra 1")
    print("   under the root, so it is far wider and it never shrinks below the noise")
    print(f"   floor of about {tcrit * math.sqrt(f['sigma2']):.2f} however much data you collect.")
    print("   The last row is outside the observed spend range entirely. The formula")
    print("   returns a number and the model has no evidence there at all.")


if __name__ == "__main__":
    main()
