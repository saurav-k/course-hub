"""0006 - Logarithms and exponentials: the rules and the shapes.

Checks all four identities this lesson proves against real numbers, produces a
counterexample to the rule that does not exist, and then fits an exponential
from its median and tests the fit against the data it came from.

Needs only numpy and pandas.
"""

import numpy as np
import pandas as pd

LOCAL = "../datasets/tickets.csv"
REMOTE = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/tickets.csv"


def load() -> pd.DataFrame:
    try:
        return pd.read_csv(LOCAL)
    except FileNotFoundError:
        return pd.read_csv(REMOTE)


def main() -> None:
    frame = load()
    seconds = frame.first_response_seconds.to_numpy()
    a = seconds[:1000]
    b = seconds[1000:2000]
    assert (a > 0).all() and (b > 0).all(), "the identities need positive arguments"

    print("the four identities, checked on 1,000 real pairs each")
    print(f"  ln(ab)     = ln a + ln b     max error {np.abs(np.log(a * b) - (np.log(a) + np.log(b))).max():.2e}")
    print(f"  ln(a/b)    = ln a - ln b     max error {np.abs(np.log(a / b) - (np.log(a) - np.log(b))).max():.2e}")
    print(f"  ln(a^3)    = 3 ln a          max error {np.abs(np.log(a ** 3) - 3 * np.log(a)).max():.2e}")
    print(f"  log2 a     = ln a / ln 2     max error {np.abs(np.log2(a) - np.log(a) / np.log(2)).max():.2e}")
    assert np.allclose(np.log(a * b), np.log(a) + np.log(b))
    assert np.allclose(np.log(a / b), np.log(a) - np.log(b))
    assert np.allclose(np.log(a ** 3), 3 * np.log(a))
    assert np.allclose(np.log2(a), np.log(a) / np.log(2))

    # And the one that is not a rule.
    left = np.log(a + b)
    right = np.log(a) + np.log(b)
    worst = int(np.abs(left - right).argmax())
    print(f"\n  ln(a+b) = ln a + ln b is NOT a rule")
    print(f"    a = {a[worst]:.3f}, b = {b[worst]:.3f}")
    print(f"    ln(a+b) = {left[worst]:.4f} but ln a + ln b = {right[worst]:.4f}")
    print(f"    smallest possible counterexample: ln(1+1) = {np.log(2):.4f}, ln 1 + ln 1 = 0.0000")
    assert not np.allclose(left, right), "these must not agree"
    assert not np.isclose(np.log(1.0 + 1.0), np.log(1.0) + np.log(1.0))

    # log turns exponential decay into a straight line: that is the diagnostic.
    print("\nfitting an exponential from its median")
    median = float(np.median(seconds))
    lam = np.log(2.0) / median
    print(f"  median = {median:.3f} s")
    print(f"  lambda = ln(2) / median = {lam:.8f} per second")
    print(f"  1/lambda = {1 / lam:.3f} s, and the sample mean is {seconds.mean():.3f} s")
    assert abs(1 / lam - seconds.mean()) / seconds.mean() < 0.10, (
        "an exponential's mean should be near 1/lambda"
    )

    # Check the fitted survival curve against the empirical one.
    print("\n  survival P(X > t): fitted against observed")
    for t in (200.0, 411.0, 800.0, 1500.0):
        fitted = float(np.exp(-lam * t))
        observed = float((seconds > t).mean())
        print(f"    t = {t:>6.0f}s   fitted {fitted:.4f}   observed {observed:.4f}")
        assert abs(fitted - observed) < 0.03, f"the fit is off at t = {t}"

    # By construction the median is where survival is one half.
    assert abs(float(np.exp(-lam * median)) - 0.5) < 1e-12
    print(f"\n  at t = median the fitted survival is exactly {np.exp(-lam * median):.6f}, by construction")

    # On a log axis, exponential decay is a straight line.
    edges = np.array([0.0, 300.0, 600.0, 900.0, 1200.0, 1500.0])
    survival = np.array([(seconds > t).mean() for t in edges])
    slopes = np.diff(np.log(survival)) / np.diff(edges)
    print(f"\n  d(ln survival)/dt over five intervals: {np.round(slopes, 6).tolist()}")
    print(f"  all near -lambda = {-lam:.6f}, which is what 'straight on a log axis' means")
    assert np.abs(slopes - (-lam)).max() < 0.0004

    print("\nall assertions passed")


if __name__ == "__main__":
    main()
