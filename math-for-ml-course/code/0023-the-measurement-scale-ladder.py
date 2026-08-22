"""The measurement-scale ladder, and which operations each rung licenses.

Stevens, S. S. (1946). "On the Theory of Scales of Measurement." Science 103,
677-680. The ladder is a claim about which transformations leave a scale's
meaning intact, and therefore about which statistics are meaningful on it.

    NOMINAL   labels only. Meaningful under any one-to-one relabelling.
              Equality is the only relation. Mode yes, median no, mean no.
    ORDINAL   ordered labels. Meaningful under any order-preserving
              transformation. Ranks and quantiles yes, differences no.
    INTERVAL  differences are meaningful, the zero is a convention.
              Meaningful under x -> a.x + b with a > 0. Mean yes, ratios no.
    RATIO     a true zero. Meaningful under x -> a.x with a > 0.
              Ratios yes: "twice as fast" is a sentence that means something.

THE TEST, and it is the only one worth remembering: apply the transformation
the rung allows and see whether your conclusion survives. If it does not, the
statistic was not meaningful on that scale. The program applies exactly that
test to each column, which is why it prints conclusions twice.

Dataset: population.csv, which carries one column of each rung on purpose:
    `region` and `stratum` (nominal), `satisfaction` (ordinal),
    `office_temp_c` (interval), `spend` (ratio).
The interval column is the one the rest of the course does not have, and
without it the rung cannot be demonstrated, only described.

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

LOCAL = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "population.csv"
URL = "https://<hub>/math-for-ml-course/datasets/sessions.csv"
DATA = LOCAL if LOCAL.exists() else URL
PLAN_ORDER = ["free", "basic", "pro", "enterprise"]


def main() -> None:
    df = pd.read_csv(DATA)
    print(f"n = {len(df):,} population units\n")
    print(f"{'column':>18}  {'rung':>10}  {'what it licenses':>46}")
    for name, rung, note in (
        ("region", "nominal", "counts and the mode; no order, no arithmetic"),
        ("plan", "ordinal", "order, median, quantiles; not differences"),
        ("satisfaction", "ordinal", "order, median; a mean is a common abuse"),
        ("temp_c", "interval", "differences and the mean; not ratios"),
        ("latency_ms", "ratio", "everything, ratios included"),
        ("session_minutes", "ratio", "everything, ratios included"),
    ):
        print(f"{name:>18}  {rung:>10}  {note:>46}")

    print("\n1. NOMINAL: region. The mode survives relabelling; a mean does not exist.")
    counts = df.region.value_counts()
    print(f"   mode = {counts.index[0]} with {counts.iloc[0]:,} units")
    codes = {r: i for i, r in enumerate(sorted(df.region.unique()))}
    numeric = df.region.map(codes).to_numpy(float)
    relabel = {r: i for i, r in enumerate(sorted(df.region.unique(), reverse=True))}
    numeric2 = df.region.map(relabel).to_numpy(float)
    print(f"   encode regions 0..4 one way   -> 'mean region' = {numeric.mean():.4f}")
    print(f"   encode them another way       -> 'mean region' = {numeric2.mean():.4f}")
    print("   Same data, same question, two answers. The relabelling was allowed,")
    print("   so the statistic was never meaningful. The mode is unchanged by both.")

    print("\n2. ORDINAL: satisfaction, scored 1 to 5.")
    sat = df.satisfaction.to_numpy(float)
    print(f"   median = {np.median(sat):.1f}   mean = {sat.mean():.4f}")
    stretched = np.array([1.0, 2.0, 3.0, 4.0, 10.0])[df.satisfaction.to_numpy() - 1]
    print(f"   respace the top category as 10 instead of 5, which preserves the order:")
    print(f"   median = {np.median(stretched):.1f}   mean = {stretched.mean():.4f}")
    print("   The median is unmoved. The mean moved a long way, because it assumed")
    print("   the gap from 4 to 5 equals the gap from 1 to 2, and nothing on an")
    print("   ordinal scale promises that. Reporting a mean rating is a choice to")
    print("   assume interval spacing, and it should be a stated choice.")

    print("\n3. INTERVAL: office_temp_c. Differences mean something, ratios do not.")
    t = df.office_temp_c.to_numpy(float)
    f = t * 9.0 / 5.0 + 32.0
    warm, cool = float(np.quantile(t, 0.99)), float(np.quantile(t, 0.01))
    print(f"   mean {t.mean():.3f} C = {t.mean() * 9 / 5 + 32:.3f} F   the mean converts correctly")
    print(f"   difference p99 - p01 = {warm - cool:.3f} C = {(warm - cool) * 9 / 5:.3f} F"
          "   a difference converts correctly too")
    print(f"   ratio p99 / p01 in Celsius    = {warm / cool:.4f}")
    print(f"   ratio p99 / p01 in Fahrenheit = {(warm * 9 / 5 + 32) / (cool * 9 / 5 + 32):.4f}")
    print("   The two ratios disagree, and the conversion was legitimate, so the")
    print("   ratio was meaningless. 'Twice as warm' is not a fact about temperature.")

    print("\n4. RATIO: spend. The zero is real, so ratios survive.")
    lat = df.spend.to_numpy(float)
    p50, p99 = float(np.quantile(lat, 0.5)), float(np.quantile(lat, 0.99))
    print(f"   p99 / p50 in pounds = {p99 / p50:.4f}")
    print(f"   p99 / p50 in pence  = {(p99 * 100) / (p50 * 100):.4f}")
    print("   Identical, because the only transformation a ratio scale allows is")
    print("   multiplication by a positive constant, and that cancels. 'The tail is")
    print(f"   {p99 / p50:.1f} times the median' is a sentence that means something.")


if __name__ == "__main__":
    main()
