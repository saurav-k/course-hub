"""The bias-variance tradeoff, and where it stops being the whole story.

THEOREM (bias-variance decomposition of prediction error). Suppose
Y = f(X) + e with E[e] = 0 and Var(e) = sigma_e^2, and let f_hat be fitted on a
random training set. At a fixed input x0, under squared-error loss,
    Err(x0) = E[(Y - f_hat(x0))^2 | X = x0]
            = sigma_e^2  +  ( E[f_hat(x0)] - f(x0) )^2  +  E[( f_hat(x0) - E[f_hat(x0)] )^2]
            = irreducible error  +  bias^2  +  variance.
PROOF. Write Y - f_hat = (Y - f(x0)) + (f(x0) - f_hat(x0)) = e + (f - f_hat).
The noise e is independent of the training set and has mean zero, so the cross
term vanishes in expectation and E[e^2] = sigma_e^2 splits off. What is left is
E[(f(x0) - f_hat(x0))^2], and applying the MSE decomposition of the estimation
lesson to f_hat as an estimator of the number f(x0) gives bias^2 + variance. []
(Hastie, Tibshirani and Friedman, The Elements of Statistical Learning, 2nd
edition, equation 7.9.)

THE k-NEAREST-NEIGHBOUR INSTANCE, which is the cleanest concrete case:
    Err(x0) = sigma_e^2 + [ f(x0) - (1/k) sum_{l=1..k} f(x_(l)) ]^2 + sigma_e^2 / k.
The variance term is exactly sigma_e^2/k and falls as k grows. The bias term is
the gap between f(x0) and the average of f over a widening neighbourhood, and
grows as k grows. Complexity moves the two in opposite directions, and it
cannot touch the first term at all.

WHERE IT STOPS. The classical U-curve describes the under-parameterised
regime. Past the interpolation threshold, where a model has enough capacity to
fit the training data exactly, test error can fall again. That is double
descent, it is an active area, and a course should name it rather than resolve
it.

Dataset: features.csv, whose true coefficients and noise level are
known, so bias and variance can be measured against the truth rather than
estimated.

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

LOCAL = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "features.csv"
URL = "https://<hub>/math-for-ml-course/datasets/features.csv"
DATA = LOCAL if LOCAL.exists() else URL
TRUE_BETA = np.array([4.0, -2.5, 1.5, -1.0, 0.6])
NOISE_SD = 3.0
SEED = 20260822


def main() -> None:
    df = pd.read_csv(DATA)
    cols = [c for c in df.columns if c.startswith("x")]
    x_all = df[cols].to_numpy(float)
    truth = np.zeros(len(cols))
    truth[:TRUE_BETA.size] = TRUE_BETA

    rng = np.random.default_rng(SEED)
    # One fixed test point, and its true noiseless response.
    x0 = x_all[0]
    f_x0 = float(x0 @ truth)
    print(f"a fixed test point x0 with true noiseless response f(x0) = {f_x0:.5f}")
    print(f"irreducible error sigma_e^2 = {NOISE_SD ** 2:.4f}, which no model can remove\n")

    print("1. COMPLEXITY AS THE NUMBER OF PREDICTORS THE MODEL IS ALLOWED TO USE")
    print("   Fitting on fresh 80-row training sets, 3,000 times, at each complexity.\n")
    print(f"   {'predictors':>11}  {'E[f_hat(x0)]':>13}  {'bias':>9}  {'bias^2':>9}"
          f"  {'variance':>10}  {'total Err':>11}")
    n_train, repeats = 80, 3000
    rows = []
    for p in (1, 2, 3, 5, 8, 15, 30, 50, 70):
        preds = np.empty(repeats)
        use = min(p, len(cols))
        for r in range(repeats):
            idx = rng.choice(len(x_all), size=n_train, replace=False)
            xt = x_all[idx][:, :use]
            # Regenerate the response so the noise is fresh each repeat.
            yt = x_all[idx] @ truth + rng.normal(0.0, NOISE_SD, size=n_train)
            if p > len(cols):
                # Beyond 30 real predictors, pad with pure-noise columns.
                extra = rng.normal(0.0, 1.0, size=(n_train, p - len(cols)))
                xt = np.hstack([xt, extra])
            beta, *_ = np.linalg.lstsq(xt, yt, rcond=None)
            xq = x0[:use]
            if p > len(cols):
                xq = np.concatenate([xq, np.zeros(p - len(cols))])
            preds[r] = float(xq @ beta)
        bias = float(preds.mean() - f_x0)
        var = float(preds.var(ddof=1))
        err = NOISE_SD ** 2 + bias ** 2 + var
        rows.append((p, err))
        print(f"   {p:>11}  {preds.mean():>13.5f}  {bias:>9.4f}  {bias ** 2:>9.4f}"
              f"  {var:>10.4f}  {err:>11.4f}")

    best = min(rows, key=lambda r: r[1])
    print(f"\n   The bias column shrinks as the model is allowed more of the five real")
    print(f"   predictors and is essentially gone by 5. The variance column climbs")
    print(f"   the whole way, because every extra column is another coefficient")
    print(f"   estimated from the same 80 rows. Total error is smallest at"
          f" {best[0]} predictors ({best[1]:.4f}).")
    print(f"   Of that {best[1]:.4f}, exactly {NOISE_SD ** 2:.1f} is irreducible:"
          f" {NOISE_SD ** 2 / best[1]:.1%} of the")
    print("   error at the optimum is not the model's fault and never was.")

    print("\n2. THE SAME SHAPE FROM THE OTHER DIRECTION: shrinkage instead of columns")
    print("   All 30 predictors, ridge penalty varied. Bias rises, variance falls.\n")
    print(f"   {'lambda':>9}  {'bias':>9}  {'bias^2':>9}  {'variance':>10}  {'total Err':>11}")
    for lam in (0.0, 1.0, 5.0, 20.0, 80.0, 400.0):
        preds = np.empty(repeats)
        for r in range(repeats):
            idx = rng.choice(len(x_all), size=n_train, replace=False)
            xt = x_all[idx]
            yt = xt @ truth + rng.normal(0.0, NOISE_SD, size=n_train)
            beta = np.linalg.solve(xt.T @ xt + lam * np.eye(len(cols)), xt.T @ yt)
            preds[r] = float(x0 @ beta)
        bias = float(preds.mean() - f_x0)
        var = float(preds.var(ddof=1))
        print(f"   {lam:>9.1f}  {bias:>9.4f}  {bias ** 2:>9.4f}  {var:>10.4f}"
              f"  {NOISE_SD ** 2 + bias ** 2 + var:>11.4f}")
    print("   This is the regularisation lesson's prior arriving from the other side:")
    print("   the same knob, described once as a belief about the weights and once as")
    print("   a position on this curve.")

    print("\n3. THE HONEST LIMIT")
    print("   Everything above is the classical, under-parameterised regime, where the")
    print("   model has fewer parameters than the training set has rows. Modern")
    print("   over-parameterised models sit past the interpolation threshold, where")
    print("   the fit passes exactly through the training data, and there the test")
    print("   error can fall AGAIN as capacity grows. The U-curve is not the last")
    print("   word on generalisation and this course does not claim it is.")


if __name__ == "__main__":
    main()
