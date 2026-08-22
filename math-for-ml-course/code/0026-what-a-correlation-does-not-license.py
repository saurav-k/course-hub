"""What a correlation does not license: identical summaries, and reversals under grouping.

Two separate failures of the same inference, "r is large so I know what is going
on". The first is that a correlation coefficient does not determine the shape of
the data. The second is that an association measured on a whole population need
not hold, or even keep its sign, inside its subgroups.

PART ONE - Anscombe's quartet: four datasets, one set of summary statistics.

Anscombe, F. J. (1973). "Graphs in Statistical Analysis."
The American Statistician 27(1), 17-21.

There is no theorem here. There is a construction, and the point of the
construction is that the inference from a summary to a shape is invalid. Four
eleven-point datasets agree on the mean of x, the mean of y, the variance of
each, the correlation, the fitted line, the standard error of its slope, the
t statistic, and R-squared. They look nothing alike.

The program recomputes every statistic from the definitions rather than
quoting the paper, so the agreement is demonstrated rather than asserted, and
then prints a coarse text scatter of each set so the disagreement is visible
without a plotting library.

PART TWO - grouping. An association computed on a pooled population is a
weighted mixture of the associations inside its parts, and the weights are the
group sizes. When the groups differ in both their association and their mix,
the pooled number can sit outside the range of the parts, and in the extreme it
can reverse sign. That extreme is Simpson's paradox.

WHICH TABLE TO CONSULT IS NOT A STATISTICAL QUESTION. This is the honest limit
of the page and of the module. Both tables are arithmetically correct. Deciding
which one answers your question requires knowing what causes what, and no
summary of these numbers carries that. A statistical procedure can tell you the
association reversed; it cannot tell you which reading to act on.

Datasets: anscombe.csv, transcribed from the paper, and sessions.csv.

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent.parent / "datasets"
URL_BASE = "https://<hub>/math-for-ml-course/datasets"


def data(name: str) -> str:
    """Local file when the repo is present, published URL when it is not."""
    local = HERE / name
    return str(local) if local.exists() else f"{URL_BASE}/{name}"


DATA = data("anscombe.csv")
def summarise(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    n = x.size
    sxx = float(((x - x.mean()) ** 2).sum())
    syy = float(((y - y.mean()) ** 2).sum())
    sxy = float(((x - x.mean()) * (y - y.mean())).sum())
    slope = sxy / sxx
    intercept = float(y.mean() - slope * x.mean())
    ss_reg = slope * sxy
    ss_res = syy - ss_reg
    sigma2 = ss_res / (n - 2)
    se_slope = float(np.sqrt(sigma2 / sxx))
    r = sxy / float(np.sqrt(sxx * syy))
    return {
        "mean x": float(x.mean()), "mean y": float(y.mean()),
        "var x": float(x.var(ddof=1)), "var y": float(y.var(ddof=1)),
        "Sxx": sxx, "intercept": intercept, "slope": slope,
        "r": r, "R^2": r * r, "SSres": ss_res,
        "se(slope)": se_slope, "t": slope / se_slope,
    }


def text_scatter(x: np.ndarray, y: np.ndarray, width: int = 34, height: int = 11) -> list[str]:
    grid = [[" "] * width for _ in range(height)]
    x0, x1 = 3.0, 20.0
    y0, y1 = 2.0, 13.5
    for px, py in zip(x, y):
        col = int((px - x0) / (x1 - x0) * (width - 1))
        row = height - 1 - int((py - y0) / (y1 - y0) * (height - 1))
        if 0 <= col < width and 0 <= row < height:
            grid[row][col] = "#" if grid[row][col] == " " else "@"
    return ["|" + "".join(row) + "|" for row in grid]


def correlation(x: np.ndarray, y: np.ndarray) -> float:
    u, v = x - x.mean(), y - y.mean()
    return float((u * v).sum() / np.sqrt((u ** 2).sum() * (v ** 2).sum()))


def grouping_section() -> None:
    """Part two: does the pooled association survive inside the groups?"""
    sess = pd.read_csv(data("sessions.csv"))
    overall = correlation(sess.session_seconds.to_numpy(float), sess.spend.to_numpy(float))
    print(f"\npooled r(session_seconds, spend) over all {len(sess):,} sessions = {overall:.5f}")
    print(f"  {'device':>9}  {'n':>8}  {'r within the group':>20}")
    for device, group in sess.groupby("device"):
        r = correlation(group.session_seconds.to_numpy(float), group.spend.to_numpy(float))
        print(f"  {device:>9}  {len(group):>8,}  {r:>20.5f}")
    print("  Here the association survives grouping: every group sits close to the")
    print("  pooled value. That is what 'device is not confounding this' looks like,")
    print("  and it is worth seeing, because the interesting case is not the only case.")

    print("\nbut it does not have to. The same arithmetic, on a table built to reverse:")
    rows = [
        # device,    variant,     n,     conversions
        ("mobile", "control", 3000, 128),
        ("mobile", "treatment", 10400, 490),
        ("desktop", "control", 9000, 1351),
        ("desktop", "treatment", 1600, 260),
    ]
    print(f"  {'device':>9}  {'variant':>10}  {'conv':>6} / {'n':<7} {'rate':>9}")
    for device, variant, n, conv in rows:
        print(f"  {device:>9}  {variant:>10}  {conv:>6} / {n:<7} {conv / n:>9.5f}")
    for device in ("mobile", "desktop"):
        c = next(r for r in rows if r[0] == device and r[1] == "control")
        t = next(r for r in rows if r[0] == device and r[1] == "treatment")
        print(f"  within {device:<8}: treatment {t[3] / t[2]:.5f} against control {c[3] / c[2]:.5f}"
              f"  -> treatment {'wins' if t[3] / t[2] > c[3] / c[2] else 'loses'}")
    for variant in ("control", "treatment"):
        conv = sum(r[3] for r in rows if r[1] == variant)
        n = sum(r[2] for r in rows if r[1] == variant)
        print(f"  pooled {variant:<10}: {conv:>5} / {n:,} = {conv / n:.5f}")
    print("  Treatment wins inside mobile AND inside desktop, and loses pooled.")
    print("  No arithmetic error is involved. The arms carry different device mixes,")
    print("  and desktop converts far better, so the pooled numbers weight the two")
    print("  groups differently. Which table to act on is a question about what")
    print("  caused the mix difference, and the numbers alone cannot answer it.")


def main() -> None:
    df = pd.read_csv(DATA)
    sets = ["I", "II", "III", "IV"]
    stats = {}
    for name in sets:
        part = df[df.dataset == name]
        stats[name] = summarise(part.x.to_numpy(float), part.y.to_numpy(float))

    keys = list(stats["I"].keys())
    print("every statistic, recomputed from the definitions\n")
    print(f"{'statistic':>12}" + "".join(f"{name:>12}" for name in sets) + f"{'spread':>12}")
    for key in keys:
        values = [stats[name][key] for name in sets]
        spread = max(values) - min(values)
        print(f"{key:>12}" + "".join(f"{v:>12.4f}" for v in values) + f"{spread:>12.2e}")
    print("\n  The spread column is the largest disagreement between the four sets.")
    print("  Every row is zero to two decimal places. Anscombe chose the numbers so.")

    print("\nand now the same four datasets as pictures\n")
    pictures = {name: text_scatter(df[df.dataset == name].x.to_numpy(float),
                                   df[df.dataset == name].y.to_numpy(float)) for name in sets}
    for a, b in (("I", "II"), ("III", "IV")):
        print(f"  {'set ' + a:<36}  {'set ' + b:<36}")
        for left, right in zip(pictures[a], pictures[b]):
            print(f"  {left}  {right}")
        print()
    print("  I is honest scatter about a line. II is a clean parabola, and a straight")
    print("  line is the wrong model for it. III is an exact line with one outlier")
    print("  dragging the fit. IV has no evidence about slope at all: ten points share")
    print("  one x value and a single leverage point at x = 19 determines the entire")
    print("  line. The summary table cannot tell any of these apart.")

    grouping_section()


if __name__ == "__main__":
    main()
