"""M06 L12 - Early stopping is the regularizer you did not write.

COMPUTES IT TWICE: the shrinkage early stopping applies to each Hessian
eigendirection, once by running gradient descent for tau steps and projecting
the answer into the eigenbasis, and once from the closed form
1 - (1 - eta*lambda)^tau. They must agree to machine precision.

It then puts that profile beside ridge's lambda/(lambda + alpha) and asks the
question the page is really about: is early stopping the SAME regularizer as
L2, or only the same KIND of regularizer?

The measured answer is worth more than the slogan. Both are shrinkage in the
Hessian eigenbasis and both spend their budget on low-curvature directions,
which is the whole mechanism. But the two profiles are different functions of
lambda, and on this dataset no single alpha reproduces early stopping at all.
The tidy reciprocal tau*eta ~ 1/alpha needs every eigenvalue to be small
RELATIVE TO alpha, and this program shows that regime is out of reach here.

    python3 m06-12-early-stopping.py

Needs numpy and pandas. Dataset: ../datasets/m06-credit.csv
"""

import numpy as np

from m06_common import load_regression


def patience_run(losses, patience):
    """Return (stop_epoch, restored_epoch), stop None if it never fires."""
    best, best_epoch, waited = np.inf, None, 0
    for epoch, value in enumerate(losses, start=1):
        if value < best:
            best, best_epoch, waited = value, epoch, 0
        else:
            waited += 1
            if waited >= patience:
                return epoch, best_epoch
    return None, best_epoch


def main() -> None:
    print("M06 L12 - a step budget is a constraint, measured")
    print()

    print("  PART 1. The page's worked example: patience on a noisy curve")
    losses = [0.90, 0.72, 0.61, 0.55, 0.52, 0.53, 0.51, 0.54, 0.55, 0.56, 0.58]
    print("    epoch losses: " + ", ".join(f"{v:.2f}" for v in losses))
    for patience in (1, 2, 3, 5):
        stop, restored = patience_run(losses, patience)
        stop_text = f"epoch {stop}" if stop else "never fires"
        print(f"    patience {patience}: stops at {stop_text:<12}"
              f" restores epoch {restored} (loss {losses[restored - 1]:.2f})")
    print("    Patience 1 ends the run at epoch 6 on a single bad step and")
    print("    restores epoch 5, missing the genuinely better epoch 7.")
    print()

    design, target = load_regression(standardise=True)
    hessian = design.T @ design / len(target)
    eigenvalues, eigenvectors = np.linalg.eigh(hessian)
    rate = 1.0 / eigenvalues[-1]
    optimum = np.linalg.solve(hessian, design.T @ target / len(target))
    optimum_rotated = eigenvectors.T @ optimum

    print("  PART 2. The shrinkage early stopping applies, two ways")
    print(f"    Hessian eigenvalues: {eigenvalues[0]:.4f} .. {eigenvalues[-1]:.4f}")
    print(f"    eta = 1/L = {rate:.6f}")
    print()
    for tau in (5, 20, 100):
        beta = np.zeros(design.shape[1])
        for _ in range(tau):
            beta -= rate * (design.T @ (design @ beta - target) / len(target))
        measured = (eigenvectors.T @ beta) / optimum_rotated
        closed_form = 1.0 - (1.0 - rate * eigenvalues) ** tau
        print(f"    tau = {tau:>4}   largest disagreement between the two: "
              f"{np.max(np.abs(measured - closed_form)):.3e}")
    print("    So early stopping IS a per-direction shrinkage, and this is it.")
    print()

    print("  PART 3. Is it the same regularizer as L2, or the same kind?")
    print("    Early stopping shrinks direction i by  1 - (1 - eta*lambda)^tau")
    print("    Ridge shrinks direction i by           lambda / (lambda + alpha)")
    print()
    tau = 20
    early = 1.0 - (1.0 - rate * eigenvalues) ** tau
    print(f"    At tau = {tau}, the alpha that would reproduce EACH direction:")
    print("      lambda     early-stopping factor    alpha needed for ridge")
    for index in (0, 1, 6, 11):
        factor = early[index]
        needed = eigenvalues[index] * (1 - factor) / factor if factor > 0 else np.inf
        print(f"      {eigenvalues[index]:>7.4f}   {factor:>20.10f}   {needed:>21.4e}")
    print()
    print("    Those alphas are not the same number, so no single ridge penalty")
    print("    reproduces this early-stopped model. The two are the same KIND of")
    print("    regularizer - both shrink, both spend their budget on the")
    print("    low-curvature directions - and they are not the same regularizer.")
    print()

    print("  PART 4. Why the tidy formula tau*eta ~ 1/alpha does not apply here")
    print("    It needs lambda_i / alpha << 1 for every i, so alpha must dominate")
    print(f"    lambda_max = {eigenvalues[-1]:.4f}. But alpha is predicted as")
    print("    1/(tau*eta), which SHRINKS as tau grows. The two demands fight.")
    print()
    print("      tau     alpha = 1/(tau*eta)     lambda_max / alpha    condition")
    for tau in (1, 5, 20, 200):
        alpha = 1.0 / (tau * rate)
        ratio = eigenvalues[-1] / alpha
        verdict = "holds" if ratio < 0.1 else "VIOLATED"
        print(f"      {tau:>5}     {alpha:>18.4f}     {ratio:>17.2f}    {verdict}")
    print()
    print("    Every row is violated, and the first row already is. The regime")
    print("    the approximation needs would mean stopping before the first step.")
    print()
    print("    Nothing here breaks the page. Result 1 - a step budget bounds the")
    print("    reachable region - holds unconditionally and is why early stopping")
    print("    regularises at all. Result 2's exact equivalence holds too. It is")
    print("    only the tidy reciprocal that needs a regime real problems rarely")
    print("    occupy, and a page that states the conditions has already said so.")


if __name__ == "__main__":
    main()
