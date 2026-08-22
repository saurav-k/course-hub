"""Covariance, correlation, and why only one of them is comparable across units.

THEOREM (Cauchy-Schwarz, and hence -1 <= r <= 1). For samples x and y with
deviations u_i = x_i - xbar and v_i = y_i - ybar,
    ( sum_i u_i v_i )^2  <=  ( sum_i u_i^2 ) ( sum_i v_i^2 ),
so r = sum u v / sqrt(sum u^2 . sum v^2) lies in [-1, 1], with equality exactly
when v is a constant multiple of u, that is when the points are collinear.
PROOF. For any real t, the quadratic
    q(t) = sum_i (u_i . t + v_i)^2 = t^2 sum u^2 + 2t sum uv + sum v^2
is a sum of squares and so q(t) >= 0 for every t. A quadratic with a positive
leading coefficient that is never negative has a non-positive discriminant:
    (2 sum uv)^2 - 4 (sum u^2)(sum v^2) <= 0,
which rearranges to the claim. Equality needs q(t) = 0 for some t, which forces
u_i t + v_i = 0 for every i.  []

THEOREM (correlation is invariant to positive linear rescaling). For constants
a > 0, c > 0 and any b, d,
    r(a.x + b,  c.y + d) = r(x, y),
while Cov(a.x + b, c.y + d) = a.c.Cov(x, y).
PROOF. Adding b shifts both x_i and xbar by b, so every deviation u_i is
unchanged; multiplying by a scales every u_i by a. So the numerator of r picks
up a factor a.c and each square root in the denominator picks up |a| and |c|.
With a, c > 0 the factors cancel exactly. Covariance keeps its factor a.c,
which is why its magnitude has no interpretation on its own.  []

Dataset: sessions.csv. `spend` is driven by `session_seconds` plus independent
noise, so the pair correlates. `screen_brightness` was drawn independently of
everything, so its correlation with the same column is near zero. Having a real
correlation and a null one in the same table is what stops a reader learning
that "r is always big".

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

LOCAL = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "sessions.csv"
URL = "https://<hub>/math-for-ml-course/datasets/sessions.csv"
DATA = LOCAL if LOCAL.exists() else URL
def covariance_from_definition(x: np.ndarray, y: np.ndarray, ddof: int = 1) -> float:
    u, v = x - x.mean(), y - y.mean()
    return float((u * v).sum() / (x.size - ddof))


def correlation_from_definition(x: np.ndarray, y: np.ndarray) -> float:
    u, v = x - x.mean(), y - y.mean()
    return float((u * v).sum() / np.sqrt((u ** 2).sum() * (v ** 2).sum()))


def main() -> None:
    df = pd.read_csv(DATA)
    minutes = df["session_seconds"].to_numpy(float)
    payload = df["spend"].to_numpy(float)
    views = df["screen_brightness"].to_numpy(float)

    print(f"n = {minutes.size:,} sessions")
    print("session_seconds against spend")
    print(f"  cov from definition {covariance_from_definition(minutes, payload):14.6f}"
          f"   pandas {df.session_seconds.cov(df.spend):14.6f}")
    print(f"  r   from definition {correlation_from_definition(minutes, payload):14.6f}"
          f"   pandas {df.session_seconds.corr(df.spend):14.6f}")
    print("session_seconds against screen_brightness, built independent")
    print(f"  cov from definition {covariance_from_definition(minutes, views):14.6f}")
    print(f"  r   from definition {correlation_from_definition(minutes, views):14.6f}")
    print("  note that the two covariances cannot be ranked against each other at all:")
    print("  one is in second-pounds and the other in second-brightness-units.")
    print("  Only the r column compares, and it says one pair is related and one is not.")

    print("\nrescale: seconds -> minutes (a = 1/60), pounds -> pence (c = 100), both shifted")
    rows = [
        ("seconds, pounds", 1.0, 0.0, 1.0, 0.0),
        ("minutes, pounds", 1.0 / 60.0, 0.0, 1.0, 0.0),
        ("minutes, pence", 1.0 / 60.0, 0.0, 100.0, 0.0),
        ("minutes + 30, pence + 5", 1.0 / 60.0, 30.0, 100.0, 5.0),
    ]
    print(f"  {'units':>28}  {'covariance':>16}  {'correlation':>14}")
    for label, a, b, c, d in rows:
        xs, ys = a * minutes + b, c * payload + d
        print(f"  {label:>28}  {covariance_from_definition(xs, ys):>16.6f}"
              f"  {correlation_from_definition(xs, ys):>14.6f}")
    print("  the covariance column moves by exactly a.c each time and the shifts do")
    print("  nothing; the correlation column never moves at all. A covariance of 0.4")
    print("  is not 'weak' and a covariance of 4,000 is not 'strong': neither number")
    print("  means anything until you are told the units.")

    print("\nthe Cauchy-Schwarz bound, and the case that attains it")
    u, v = minutes - minutes.mean(), payload - payload.mean()
    lhs = float((u * v).sum() ** 2)
    rhs = float((u ** 2).sum() * (v ** 2).sum())
    print(f"  (sum uv)^2          = {lhs:.6e}")
    print(f"  (sum u^2)(sum v^2)  = {rhs:.6e}")
    print(f"  ratio               = {lhs / rhs:.8f}   which is r^2 = {correlation_from_definition(minutes, payload) ** 2:.8f}")
    exact = 2.5 * minutes - 7.0
    print(f"  r(seconds, 2.5*seconds - 7) = {correlation_from_definition(minutes, exact):.8f}"
          "   collinear, so the bound is attained")

    print("\nand the warning the number cannot carry")
    print("  r measures LINEAR association. A perfect parabola scores near zero:")
    t = np.linspace(-3, 3, 2001)
    print(f"    r(t, t^2) over a symmetric range = {correlation_from_definition(t, t ** 2):.6f}")
    print("  A zero correlation is not independence. It is the absence of a straight line.")


if __name__ == "__main__":
    main()
