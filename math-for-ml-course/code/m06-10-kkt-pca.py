"""M06 L10 - Constrained optimization: Lagrange multipliers and KKT.

COMPUTES IT TWICE: the first principal direction and the variance it
captures, once by solving the eigenproblem S*w = lambda*w directly, and once
by projected gradient ascent on w'Sw with w renormalised to the unit sphere
after every step - which is the constrained optimization this page teaches,
run as an algorithm rather than solved in closed form.

The two must agree, and the program prints w'Sw at the answer to show it
equals the multiplier. That equality is the page's punchline: the Lagrange
multiplier IS the eigenvalue IS the captured variance.

It then measures the multiplier as a price, by re-solving a small constrained
problem at a ladder of constraint levels and differencing.

    python3 m06-10-kkt-pca.py

Needs numpy and pandas. Dataset: ../datasets/m06-credit.csv
"""

import numpy as np

from m06_common import load


def main() -> None:
    design, _ = load(standardise=True, add_intercept=False)
    covariance = np.cov(design, rowvar=False)
    print("M06 L10 - PCA as a Lagrange multiplier problem")
    print(f"covariance matrix: {covariance.shape[0]} x {covariance.shape[1]}")
    print()

    print("  Route 1: solve the eigenproblem S*w = lambda*w")
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    top = int(np.argmax(eigenvalues))
    w_eigen = eigenvectors[:, top]
    print(f"    largest eigenvalue : {eigenvalues[top]:.10f}")
    print(f"    ||w||              : {np.linalg.norm(w_eigen):.10f}")
    print()

    print("  Route 2: projected gradient ascent on w'Sw, ||w|| = 1")
    rng = np.random.default_rng(41)
    w = rng.normal(0.0, 1.0, covariance.shape[0])
    w /= np.linalg.norm(w)
    for step in range(1, 20_001):
        w = w + 0.01 * (2.0 * covariance @ w)     # ascend the objective
        w /= np.linalg.norm(w)                    # project back to the sphere
        if step in (1, 10, 100, 1_000, 20_000):
            print(f"    step {step:>6}   w'Sw = {float(w @ covariance @ w):.10f}")
    print()

    print("  Do the two agree?")
    # An eigenvector is defined up to sign, so compare the absolute alignment.
    alignment = abs(float(w @ w_eigen))
    print(f"    |cos angle between the two w|      : {alignment:.10f}")
    print(f"    eigenvalue from route 1            : {eigenvalues[top]:.10f}")
    print(f"    w'Sw at route 2's answer           : {float(w @ covariance @ w):.10f}")
    print(f"    difference                         : "
          f"{abs(eigenvalues[top] - float(w @ covariance @ w)):.3e}")
    print()
    print("  Stationarity gave S*w = lambda*w, and substituting back gave")
    print("  w'Sw = lambda. So the multiplier, the eigenvalue and the captured")
    print("  variance are one number. That is why this module's notation table")
    print("  lets lambda mean both: here they are not two things.")
    print()

    print("  The multiplier as a price: min x^2 + y^2 subject to x + y = b")
    print("    b        x = y      objective    predicted rise   actual rise")
    previous = None
    for b in (2.0, 2.1, 2.5, 3.0):
        # Stationarity: 2x = lambda, 2y = lambda, so x = y = b/2, lambda = b.
        x = b / 2.0
        objective = 2.0 * x * x
        multiplier = b
        if previous is not None:
            previous_b, previous_objective, previous_multiplier = previous
            predicted = previous_multiplier * (b - previous_b)
            actual = objective - previous_objective
            print(f"    {b:<7.1f}  {x:<9.3f}  {objective:<11.4f}"
                  f"  {predicted:<15.4f}  {actual:.4f}")
        else:
            print(f"    {b:<7.1f}  {x:<9.3f}  {objective:<11.4f}"
                  f"  {'-':<15}  -")
        previous = (b, objective, multiplier)
    print()
    print("    lambda predicts the rise well for a small relaxation and less well")
    print("    for a large one, because it is a first-order price. The gap is the")
    print("    second-order term, and saying so is the honest version.")


if __name__ == "__main__":
    main()
