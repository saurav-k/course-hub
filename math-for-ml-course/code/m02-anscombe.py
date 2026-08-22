"""Anscombe's quartet: four datasets, one set of summary statistics.

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

Dataset: anscombe.csv, transcribed from the paper.

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

LOCAL = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "anscombe.csv"
URL = "https://<hub>/math-for-ml-course/datasets/anscombe.csv"
DATA = LOCAL if LOCAL.exists() else URL
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


if __name__ == "__main__":
    main()
