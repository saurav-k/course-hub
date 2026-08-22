"""Maximum likelihood: the parameter that makes your data least surprising.

THE IDEA, before any distribution. You have data and a family of models indexed
by a parameter. Each candidate parameter assigns a probability to the data you
actually saw. Maximum likelihood picks the candidate that assigns the largest
one. Nothing more is being claimed: not that the parameter is probable, not
that the model is right, only that the data would have been least surprising
under this member of the family.

DEFINITION. For independent observations x_1..x_n with density or mass function
f( . | theta),
    L(theta) = prod_{i=1..n} f(x_i | theta),      l(theta) = log L(theta).

THEOREM (the log does not move the maximum). If g is strictly increasing then
argmax_theta h(theta) = argmax_theta g(h(theta)).
PROOF. Suppose h(a) >= h(b) for all b. Since g is strictly increasing,
g(h(a)) >= g(h(b)) for all b, so a maximises g o h as well. The same argument
in reverse gives the converse.  []
The logarithm is strictly increasing on (0, infinity) and every likelihood is
positive where it matters, so maximising l is maximising L. That is why every
derivation in this module works with the sum and not the product.

WHY IT IS NOT MERELY CONVENIENT. A product of n probabilities each below one
underflows to exactly zero in floating point at modest n, and once it is zero
the maximum cannot be found at all: every candidate ties. The sum of logs does
not underflow. The program shows the raw likelihood hitting zero, and shows
that the log-likelihood at the same parameters is perfectly well behaved.

WHAT IT IS NOT. L(theta) is a density in the DATA, read as a function of the
parameter. It is not a probability distribution over theta and does not
integrate to one over theta. Turning it into one requires a prior, which is the
MAP lesson.

Dataset: sessions.csv, column `returning`, a genuine Bernoulli column.

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

LOCAL = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "sessions.csv"
URL = "https://<hub>/math-for-ml-course/datasets/sessions.csv"
DATA = LOCAL if LOCAL.exists() else URL


def likelihood(p: float, x: np.ndarray) -> float:
    """The product, computed literally, so the reader can watch it underflow."""
    out = 1.0
    for value in x:
        out *= p if value else (1.0 - p)
    return out


def log_likelihood(p: float, x: np.ndarray) -> float:
    """The sum of logs, computed the same way, which does not underflow."""
    return float(np.sum(np.where(x == 1, np.log(p), np.log1p(-p))))


def main() -> None:
    x = pd.read_csv(DATA)["returning"].astype(int).to_numpy()
    n = x.size
    k = int(x.sum())
    mle = k / n
    print(f"n = {n:,} sessions, of which {k:,} are returning visitors")
    print(f"the maximum likelihood estimate is k/n = {mle:.6f}\n")

    print("1. THE LIKELIHOOD IS A CURVE, AND IT HAS A TOP")
    print(f"   {'candidate p':>13}  {'log-likelihood':>17}  {'how much worse than the peak':>30}")
    peak = log_likelihood(mle, x)
    for p in (0.20, 0.30, 0.38, mle, 0.45, 0.55, 0.70):
        ll = log_likelihood(p, x)
        mark = "   <- the MLE" if abs(p - mle) < 1e-12 else ""
        print(f"   {p:>13.6f}  {ll:>17.4f}  {ll - peak:>30.4f}{mark}")
    print("   Every row is negative against the peak, which is what 'maximum' means.")

    print("\n2. WHY THE LOG IS NOT OPTIONAL: the raw product underflows")
    print(f"   {'observations used':>19}  {'raw L(p_hat)':>16}  {'log L(p_hat)':>16}")
    for m in (10, 50, 200, 700, 2000):
        sub = x[:m]
        raw = likelihood(mle, sub)
        print(f"   {m:>19,}  {raw:>16.6e}  {log_likelihood(mle, sub):>16.4f}")
    print("   The raw column reaches exactly 0.0 and stays there. At that point every")
    print("   candidate parameter ties at zero and the maximum cannot be located at")
    print("   all. The log column is still an ordinary number at every size. The log")
    print("   is not a convenience, it is what makes the computation possible.")

    print("\n3. THE LOG DOES NOT MOVE THE ARGMAX")
    grid = np.linspace(0.30, 0.52, 2201)
    raw_small = np.array([likelihood(p, x[:120]) for p in grid])
    log_full = np.array([log_likelihood(p, x[:120]) for p in grid])
    print(f"   on the first 120 rows, where the raw product is still representable:")
    print(f"     argmax of L      = {grid[int(np.argmax(raw_small))]:.6f}")
    print(f"     argmax of log L  = {grid[int(np.argmax(log_full))]:.6f}")
    print(f"     k/n on those 120 = {x[:120].mean():.6f}")
    assert abs(grid[int(np.argmax(raw_small))] - grid[int(np.argmax(log_full))]) < 1e-9, \
        "the log moved the argmax, which would contradict the theorem"
    print("   The two agree to the grid's resolution, and the assertion above fails")
    print("   the program if they ever do not.")

    print("\n4. A LIKELIHOOD IS NOT A DISTRIBUTION OVER THE PARAMETER")
    grid = np.linspace(0.001, 0.999, 999)
    small = x[:40]
    values = np.array([likelihood(p, small) for p in grid])
    area = float(np.trapezoid(values, grid)) if hasattr(np, "trapezoid") else float(np.trapz(values, grid))
    print(f"   integrating L(p) over p in (0, 1), on 40 observations: {area:.6e}")
    print("   That is not 1, and nothing makes it 1. The curve is a density in the")
    print("   DATA read as a function of p. Reading its height as 'how probable this")
    print("   p is' is the single commonest misreading in this module, and giving it")
    print("   a probability interpretation is exactly what adding a prior does.")


if __name__ == "__main__":
    main()
