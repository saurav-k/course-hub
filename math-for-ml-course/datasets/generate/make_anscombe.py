"""Write anscombe.csv: the quartet, transcribed from the paper.

This is the one file in this folder that is NOT generated. It is transcribed,
because the whole value of Anscombe's quartet is that these particular
forty-four points were constructed by hand to agree on every standard summary
statistic while looking nothing alike. Regenerating them would defeat it.

    Anscombe, F. J. (1973). "Graphs in Statistical Analysis."
    The American Statistician 27(1), 17-21.

The agreement the four sets share, recomputed from these points rather than
quoted from the paper: mean x 9.0, mean y 7.50, sample variance of x 11.0,
sample variance of y about 4.12, S_xx 110.0, fitted line y = 3.00 + 0.500x,
r 0.816, R-squared 0.667, standard error of the slope 0.118, t 4.24.

The script is here so the folder has one entry point per dataset and so the
citation travels with the data.

Run: python3 make_anscombe.py
Writes ../anscombe.csv.
"""

from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "anscombe.csv"

QUARTET = {
    "I": [(10, 8.04), (8, 6.95), (13, 7.58), (9, 8.81), (11, 8.33), (14, 9.96),
          (6, 7.24), (4, 4.26), (12, 10.84), (7, 4.82), (5, 5.68)],
    "II": [(10, 9.14), (8, 8.14), (13, 8.74), (9, 8.77), (11, 9.26), (14, 8.10),
           (6, 6.13), (4, 3.10), (12, 9.13), (7, 7.26), (5, 4.74)],
    "III": [(10, 7.46), (8, 6.77), (13, 12.74), (9, 7.11), (11, 7.81), (14, 8.84),
            (6, 6.08), (4, 5.39), (12, 8.15), (7, 6.42), (5, 5.73)],
    "IV": [(8, 6.58), (8, 5.76), (8, 7.71), (8, 8.84), (8, 8.47), (8, 7.04),
           (8, 5.25), (19, 12.50), (8, 5.56), (8, 7.91), (8, 6.89)],
}


def main() -> None:
    rows = [{"dataset": name, "x": float(px), "y": float(py)}
            for name, points in QUARTET.items() for px, py in points]
    frame = pd.DataFrame(rows)
    frame.to_csv(OUT, index=False)
    print(f"wrote {OUT}  {len(frame)} rows  {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
