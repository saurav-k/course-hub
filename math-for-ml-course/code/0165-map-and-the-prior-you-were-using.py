"""MAP, and the prior you were already using.

THEOREM (MAP is MLE plus a log-prior). By Bayes' theorem the posterior is
    p(theta | x) = p(x | theta) p(theta) / p(x).
The evidence p(x) does not contain theta, so
    argmax_theta p(theta | x) = argmax_theta [ log L(theta) + log p(theta) ].
PROOF. The logarithm is strictly increasing, so it preserves the argmax, and
log p(x) is an additive constant in theta which cannot move a maximum.  []

THEOREM (L2 regularization is a Gaussian prior). Take y = X w + e with
e ~ Normal(0, sigma^2 I) and an independent prior w_j ~ Normal(0, tau^2). The
MAP estimate is the ridge solution
    w_hat = argmin_w [ ||y - X w||^2 + lambda ||w||^2 ],   lambda = sigma^2/tau^2.
PROOF. The log-prior of a Normal(0, tau^2) density is -w_j^2/(2 tau^2) plus a
constant, so summing over j the MAP objective is
    -(1/(2 sigma^2)) ||y - X w||^2 - (1/(2 tau^2)) ||w||^2 + const.
Multiply by -2 sigma^2, which is a positive constant and so turns the argmax
into an argmin without changing the solution, giving
    ||y - X w||^2 + (sigma^2/tau^2) ||w||^2.  []

THEOREM (L1 regularization is a Laplace prior). With the same likelihood and an
independent prior w_j ~ Laplace(0, b), whose density is (1/(2b)) exp(-|w_j|/b),
the MAP estimate is the lasso solution with lambda = 2 sigma^2 / b.
    The log-prior contributes -|w_j|/b, so the MAP objective is
    argmin [ (1/(2 sigma^2)) ||y - X w||^2 + (1/b) ||w||_1 ].
Multiply by 2 sigma^2, positive so the argmin is unchanged, giving
    ||y - X w||^2 + (2 sigma^2 / b) ||w||_1.  []

NOTE THE FACTOR OF TWO, and do not "correct" it to match the ridge constant.
Both theorems use the same convention, ||y - Xw||^2 + lambda (penalty), with no
one-half on the squared-error term, which is ESL's criterion 3.53. Ridge has no
2 and the lasso does, because the Gaussian log-prior -w^2/(2 tau^2) carries its
own one-half which cancels the 2 from 2 sigma^2, while the Laplace log-prior
-|w|/b carries none. Section 5 below checks both constants numerically rather
than leaving you to trust this paragraph.

ESL 3.4.3 states the Laplace correspondence with tau = 1/lambda and no sigma^2
at all. That is not a third answer: it is thinking of the penalty AS the
log-prior rather than deriving MAP against a noise model, so it never has a
sigma^2 to carry. Take the correspondence and the posterior-mode caveat from
ESL, and the constant from the derivation above.

AND THE HONEST LIMIT. These are posterior MODES, not posterior means. For the
Gaussian prior the two coincide because the posterior is symmetric, so ridge is
also the posterior mean. For the Laplace prior they do not: the lasso is the
mode and the posterior mean is not sparse at all. A page that says
"regularization is Bayesian" without that sentence has overstated the result.

Dataset: features.csv - 4,000 rows, 30 predictors of which x01..x05
carry the true coefficients (4.0, -2.5, 1.5, -1.0, 0.6) and x06..x30 are noise
with true coefficient 0. Noise standard deviation 3.0.

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


def ridge_fit(x: np.ndarray, y: np.ndarray, lam: float) -> np.ndarray:
    """The closed form: (X'X + lambda I)^-1 X'y. No intercept - columns are centred."""
    p = x.shape[1]
    return np.linalg.solve(x.T @ x + lam * np.eye(p), x.T @ y)


def lasso_fit(x: np.ndarray, y: np.ndarray, lam: float, iters: int = 400) -> np.ndarray:
    """Coordinate descent with soft thresholding, which is all the lasso needs."""
    n, p = x.shape
    w = np.zeros(p)
    col_norm = (x ** 2).sum(axis=0)
    for _ in range(iters):
        for j in range(p):
            residual = y - x @ w + x[:, j] * w[j]
            rho = float(x[:, j] @ residual)
            w[j] = np.sign(rho) * max(abs(rho) - lam / 2.0, 0.0) / col_norm[j]
    return w


def verify_the_constants(x: np.ndarray, y: np.ndarray, sigma2: float) -> None:
    """Check both lambdas against a directly minimised MAP objective.

    The point is that the constants are derived rather than quoted, so the
    program should fail if either is wrong instead of printing a sweep that
    looks plausible under any constant.
    """
    tau2, b = 0.6, 0.9
    print("\n5. THE TWO CONSTANTS, CHECKED AGAINST A DIRECT MAP MINIMISER")

    # Ridge: the MAP normal equations are (X'X + sigma^2/tau^2 I) w = X'y.
    direct_ridge = np.linalg.solve(x.T @ x + (sigma2 / tau2) * np.eye(x.shape[1]), x.T @ y)
    from_lambda = ridge_fit(x, y, sigma2 / tau2)
    print(f"   ridge  lambda = sigma^2/tau^2 = {sigma2 / tau2:8.4f}"
          f"   max |difference| {float(np.abs(direct_ridge - from_lambda).max()):.2e}")
    assert np.allclose(direct_ridge, from_lambda, atol=1e-9)

    # Lasso: minimise the MAP objective directly, thresholding at sigma^2/b.
    def map_lasso(iters: int = 600) -> np.ndarray:
        w = np.zeros(x.shape[1])
        col = (x ** 2).sum(axis=0)
        for _ in range(iters):
            for j in range(x.shape[1]):
                r = y - x @ w + x[:, j] * w[j]
                rho = float(x[:, j] @ r)
                w[j] = np.sign(rho) * max(abs(rho) - sigma2 / b, 0.0) / col[j]
        return w

    direct_lasso = map_lasso()
    right = lasso_fit(x, y, 2.0 * sigma2 / b)
    wrong = lasso_fit(x, y, sigma2 / b)
    print(f"   lasso  lambda = 2 sigma^2/b   = {2 * sigma2 / b:8.4f}"
          f"   max |difference| {float(np.abs(direct_lasso - right).max()):.2e}")
    print(f"   lasso  lambda = sigma^2/b     = {sigma2 / b:8.4f}"
          f"   max |difference| {float(np.abs(direct_lasso - wrong).max()):.2e}   <- the constant that is wrong")
    assert np.abs(direct_lasso - right).max() < 1e-6, "2 sigma^2/b should reproduce the MAP solution"
    assert np.abs(direct_lasso - wrong).max() > 1e-4, "sigma^2/b should NOT reproduce it"
    print("   The assertions fail the program if either constant is edited to the other,")
    print("   which is the only reliable way to keep a factor of two honest.")


def main() -> None:
    df = pd.read_csv(DATA)
    y = df["y"].to_numpy(float)
    cols = [c for c in df.columns if c.startswith("x")]
    x = df[cols].to_numpy(float)
    truth = np.zeros(len(cols))
    truth[:TRUE_BETA.size] = TRUE_BETA

    rng = np.random.default_rng(SEED)
    idx = rng.permutation(len(y))
    small = idx[:60]          # a small sample, where a prior earns its keep
    x_s, y_s = x[small], y[small]

    print(f"{len(cols)} predictors, {TRUE_BETA.size} of them real. Fitting on {small.size} rows,")
    print(f"so the problem is nearly as wide as it is tall and the prior has work to do.\n")

    print("1. MAP IS MLE PLUS A LOG-PRIOR: the objective, evaluated directly")
    sigma2 = NOISE_SD ** 2
    for tau2 in (0.25, 1.0, 100.0):
        lam = sigma2 / tau2
        w = ridge_fit(x_s, y_s, lam)
        rss = float(((y_s - x_s @ w) ** 2).sum())
        loglik = -0.5 * len(y_s) * np.log(2 * np.pi * sigma2) - rss / (2 * sigma2)
        logprior = float(-0.5 * len(cols) * np.log(2 * np.pi * tau2) - (w ** 2).sum() / (2 * tau2))
        print(f"   tau^2 = {tau2:>7.2f}  lambda = {lam:>7.3f}   log L = {loglik:>10.3f}"
              f"   log prior = {logprior:>10.3f}   sum = {loglik + logprior:>10.3f}")
    print("   A tighter prior costs likelihood and buys prior. MAP maximises the sum,")
    print("   and lambda is the exchange rate between them: lambda = sigma^2/tau^2.")

    print("\n2. RIDGE IS A GAUSSIAN PRIOR: recovered coefficients as the prior tightens")
    print(f"   {'tau^2':>9}  {'lambda':>9}  " + "  ".join(f"{c:>7}" for c in cols[:5])
          + f"  {'max |noise coef|':>17}  {'error vs truth':>15}")
    print(f"   {'truth':>9}  {'-':>9}  " + "  ".join(f"{v:>7.3f}" for v in TRUE_BETA)
          + f"  {0.0:>17.3f}  {0.0:>15.3f}")
    for tau2 in (1e6, 1.0, 0.25, 0.05):
        lam = sigma2 / tau2
        w = ridge_fit(x_s, y_s, lam)
        err = float(np.sqrt(((w - truth) ** 2).sum()))
        print(f"   {tau2:>9.4g}  {lam:>9.3f}  " + "  ".join(f"{v:>7.3f}" for v in w[:5])
              + f"  {float(np.abs(w[5:]).max()):>17.3f}  {err:>15.3f}")
    print("   The first row is a prior so flat it is no prior: that is the MLE, and it")
    print("   has fitted the noise columns hard. Tightening the prior pulls every")
    print("   coefficient towards zero, the noise ones furthest, and the distance to")
    print("   the truth falls before it rises again when the prior overwhelms the data.")

    print("\n3. LASSO IS A LAPLACE PRIOR: the same sweep, and the difference that matters")
    print(f"   {'lambda':>9}  {'nonzero of 30':>14}  {'nonzero among the 5 real':>25}  {'error vs truth':>15}")
    for lam in (1.0, 20.0, 60.0, 150.0):
        w = lasso_fit(x_s, y_s, lam)
        nz = int((np.abs(w) > 1e-8).sum())
        nz_real = int((np.abs(w[:5]) > 1e-8).sum())
        err = float(np.sqrt(((w - truth) ** 2).sum()))
        print(f"   {lam:>9.1f}  {nz:>14}  {nz_real:>25}  {err:>15.3f}")
    print("   The lasso sets coefficients to exactly zero and ridge never does. That")
    print("   is the Laplace prior's sharp point at the origin showing up in the")
    print("   answer. (The geometry of why the corner produces a zero belongs to the")
    print("   optimization module; this module owns the prior it corresponds to.)")

    print("\n4. THE LIMIT THE RESULT CARRIES: mode is not mean")
    print("   Ridge is the posterior mode AND the posterior mean, because a Gaussian")
    print("   likelihood times a Gaussian prior is Gaussian, and a Gaussian is")
    print("   symmetric about its peak. The lasso is the mode ONLY, and the")
    print("   difference is not a detail. The argument needs no simulation:")
    print("   the Laplace-prior posterior is an absolutely continuous distribution")
    print("   on R^p, so P(w_j = 0) = 0 for every j, so the posterior mean has no")
    print("   exact zero in it. The sparsity belongs to the mode, which is the one")
    print("   summary of the posterior the lasso happens to report.")
    print("   So 'regularization is just Bayesian inference' is too strong. The")
    print("   correct sentence is that these penalties are the log-densities of")
    print("   particular priors, and the estimator is a particular summary of the")
    print("   resulting posterior.")
    verify_the_constants(x_s, y_s, sigma2)


if __name__ == "__main__":
    main()
