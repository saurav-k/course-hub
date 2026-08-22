"""Bias, variance, and the mean squared error that trades them off.

DEFINITIONS. For an estimator theta_hat of a fixed parameter theta,
    Bias(theta_hat) = E[theta_hat] - theta
    Var(theta_hat)  = E[(theta_hat - E[theta_hat])^2]
    MSE(theta_hat)  = E[(theta_hat - theta)^2]

THEOREM (the bias-variance decomposition of MSE).
    MSE(theta_hat) = Bias(theta_hat)^2 + Var(theta_hat).
PROOF. Write m = E[theta_hat] and split the error at m:
    theta_hat - theta = (theta_hat - m) + (m - theta).
Square and take expectations. The cross term is
    2 (m - theta) E[theta_hat - m] = 2 (m - theta) . 0 = 0,
because m - theta is a constant and E[theta_hat - m] = 0 by definition of m.
What remains is E[(theta_hat - m)^2] + (m - theta)^2 = Var + Bias^2.  []

WHAT THE THEOREM IS FOR. It makes "which estimator" a decidable question
instead of a matter of taste, and it shows that unbiasedness is not the goal.
An estimator that accepts a little bias for a large reduction in variance can
have a strictly smaller MSE, and shrinkage is exactly that trade. The program
demonstrates it with a shrinkage estimator, which is ridge regression's idea
stripped down to one number.

Dataset: sessions.csv, column session_seconds, treated as the
population so the truth is known.

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

LOCAL = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "sessions.csv"
URL = "https://<hub>/math-for-ml-course/datasets/sessions.csv"
DATA = LOCAL if LOCAL.exists() else URL
SEED = 20260822
TRIALS = 60_000
SAMPLE_N = 12


def report(name: str, estimates: np.ndarray, truth: float) -> tuple[float, float, float]:
    bias = float(estimates.mean() - truth)
    var = float(estimates.var(ddof=1))
    mse = float(((estimates - truth) ** 2).mean())
    print(f"  {name:<34} {bias:>10.5f}  {bias ** 2:>11.5f}  {var:>11.5f}"
          f"  {bias ** 2 + var:>12.5f}  {mse:>12.5f}")
    return bias, var, mse


def main() -> None:
    x = pd.read_csv(DATA)["session_seconds"].to_numpy(float)
    mu = float(x.mean())
    rng = np.random.default_rng(SEED)
    draws = rng.choice(x, size=(TRIALS, SAMPLE_N), replace=True)

    print(f"population mean mu = {mu:.6f}, samples of n = {SAMPLE_N}, {TRIALS:,} repeats\n")
    print(f"  {'estimator of mu':<34} {'bias':>10}  {'bias^2':>11}  {'variance':>11}"
          f"  {'bias^2+var':>12}  {'measured MSE':>12}")

    sample_mean = draws.mean(axis=1)
    report("sample mean", sample_mean, mu)
    report("sample median", np.median(draws, axis=1), mu)
    report("first observation only", draws[:, 0], mu)
    report("constant 12 (ignores the data)", np.full(TRIALS, 12.0), mu)

    print("\n  The bias^2+var column equals the measured MSE column in every row.")
    print("  That is the theorem, and it is an identity rather than an approximation.")
    print("  Read the rows against each other: the single observation is unbiased and")
    print("  useless, and the constant has no variance at all and is only as good as")
    print("  the guess. Neither bias nor variance alone ranks them. MSE does.")

    print("\nshrinkage: buying variance with bias, which is what a regulariser does")
    print("  Shrink the sample mean towards a fixed guess g:  est = (1-w).xbar + w.g")
    guess = 10.0
    print(f"  with g = {guess} and the truth at mu = {mu:.4f}\n")
    print(f"  {'w':>6}  {'bias':>10}  {'bias^2':>11}  {'variance':>11}  {'MSE':>12}  {'vs w=0':>8}")
    base = None
    best = (None, float("inf"))
    for w in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0):
        est = (1 - w) * sample_mean + w * guess
        bias = float(est.mean() - mu)
        var = float(est.var(ddof=1))
        mse = float(((est - mu) ** 2).mean())
        base = mse if w == 0.0 else base
        if mse < best[1]:
            best = (w, mse)
        print(f"  {w:>6.2f}  {bias:>10.5f}  {bias ** 2:>11.5f}  {var:>11.5f}"
              f"  {mse:>12.5f}  {mse / base:>8.3f}x")
    print(f"\n  The unbiased estimator is w = 0 and it is not the best row: w = {best[0]}")
    print(f"  has the smallest MSE, {best[1] / base:.3f} times the unbiased one, and it is")
    print("  biased on purpose. This is ridge regression's whole argument, with one")
    print("  parameter instead of many, and it is why 'unbiased' is not the goal.")
    print("  The trade only pays while the guess is not too far wrong: push w to 1")
    print("  and the estimator becomes the guess, with no variance and all the error.")


if __name__ == "__main__":
    main()
