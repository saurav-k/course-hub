"""Frequency tables, class intervals, and what a histogram's bin width decides.

There is no theorem here, there is a design decision the reader keeps making
without noticing: the bin width. The same column produces different-looking
distributions under different widths, and two published rules disagree about
which width to use.

    Sturges (1926)          k = ceil(log2(n)) + 1 bins
    Freedman-Diaconis (1981) h = 2 * IQR * n^(-1/3)

Sturges is derived from a binomial approximation to a normal sample and is
known to under-bin large or non-normal samples: k grows only like log2(n), so
at n = 25,000 it asks for 16 bins whatever the data does. Freedman-Diaconis
sets the width from the IQR rather than the range, which makes it robust to
the heavy tail this column has.

A frequency table is the same object as a histogram: class intervals, counts,
relative frequencies, and the cumulative column that answers "what share is
below this?" and is the empirical CDF evaluated at the bin edges.

Dataset: nimbus-sessions.csv, column latency_ms.

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

DATA = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "nimbus-sessions.csv"


def sturges_bins(n: int) -> int:
    return int(np.ceil(np.log2(n)) + 1)


def freedman_diaconis_width(x: np.ndarray) -> float:
    iqr = float(np.quantile(x, 0.75) - np.quantile(x, 0.25))
    return 2.0 * iqr * x.size ** (-1.0 / 3.0)


def frequency_table(x: np.ndarray, edges: np.ndarray) -> pd.DataFrame:
    counts, _ = np.histogram(x, bins=edges)
    rel = counts / counts.sum()
    return pd.DataFrame({
        "from": edges[:-1].round(1),
        "to": edges[1:].round(1),
        "count": counts,
        "relative": rel.round(5),
        "cumulative": rel.cumsum().round(5),
    })


def main() -> None:
    df = pd.read_csv(DATA)
    x = df["latency_ms"].to_numpy(float)
    n = x.size
    print(f"n = {n:,} sessions, column latency_ms")
    print(f"  min {x.min():.1f}   max {x.max():.1f}   IQR {np.quantile(x, .75) - np.quantile(x, .25):.1f}\n")

    k_sturges = sturges_bins(n)
    h_fd = freedman_diaconis_width(x)
    print("what the two rules ask for")
    print(f"  Sturges           {k_sturges} bins over the full range"
          f"  ->  width {(x.max() - x.min()) / k_sturges:9.1f} ms")
    print(f"  Freedman-Diaconis width {h_fd:.2f} ms over the full range"
          f"  ->  {int(np.ceil((x.max() - x.min()) / h_fd)):,} bins")
    print("  The gap is enormous, and it is the heavy tail that causes it: Sturges")
    print("  spreads its 16 bins across a range set by one 10,839 ms outlier, so")
    print("  almost every session lands in the first bin.")

    edges = np.linspace(x.min(), x.max(), k_sturges + 1)
    table = frequency_table(x, edges)
    print("\nSturges, over the full range")
    print(table.head(4).to_string(index=False))
    print(f"  ... first bin alone holds {table['relative'].iloc[0]:.2%} of the data.")
    print("  A table whose first row is the answer is not a table.")

    cut = float(np.quantile(x, 0.99))
    body = x[x <= cut]
    edges = np.arange(0.0, cut + h_fd, h_fd)
    table = frequency_table(body, edges)
    print(f"\nFreedman-Diaconis width {h_fd:.2f} ms, over the body (to p99 = {cut:.1f} ms)")
    print(f"  {len(table)} class intervals covering {len(body):,} of {n:,} sessions")
    print(table.head(10).to_string(index=False))
    shown = table.head(10)
    print(f"  The first ten intervals cover {shown['cumulative'].iloc[-1]:.2%} of the body and the")
    print("  count column is still climbing, so the mode is further down the table.")
    reach = table.index[table["cumulative"] >= 0.5][0]
    print(f"  The cumulative column passes one half at interval {reach + 1} of {len(table)},"
          f" [{table['from'].iloc[reach]:.0f}, {table['to'].iloc[reach]:.0f}) ms,")
    print("  which is the median arriving as a row number. The shape is a single")
    print("  mode with a long right tail, and it was invisible under Sturges.")

    print("\na histogram is a density estimate, and the width is the estimate")
    for width in (5.0, h_fd, 40.0, 120.0):
        e = np.arange(0.0, cut + width, width)
        counts, _ = np.histogram(body, bins=e)
        peak = int(np.argmax(counts))
        print(f"  width {width:>7.2f} ms -> {len(counts):>4} bins,"
              f" modal interval [{e[peak]:.0f}, {e[peak + 1]:.0f}) ms,"
              f" holding {counts[peak] / counts.sum():.2%}")
    print("  The modal interval moves with the width, so 'the most common latency'")
    print("  is not a property of the data alone. Report the width, or report a")
    print("  quantile, which does not need one.")


if __name__ == "__main__":
    main()
