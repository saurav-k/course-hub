"""Information gain is mutual information, and it prefers columns with more values.

Lesson: Information gain.
Dataset: m10_signals.csv (12,000 rows), plus Quinlan's own fourteen-row table.

Runs on numpy and pandas and nothing else.

What it does:
  1. Reproduces the worked example from Quinlan's 1986 paper, all four gains and
     both gain ratios, and asserts each matches the figure printed in the paper.
  2. Checks Quinlan's footnote 3 numerically: information gain IS the mutual
     information between the attribute and the class. Same function, two names.
  3. Runs the same criterion on 12,000 real rows, where one column is a
     near-unique account identifier, and shows it wins by a factor of ten.
  4. Applies the gain ratio and reports honestly that it narrows the gap without
     closing it on this data.
  5. Compares the entropy criterion with Gini on the same splits.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

RAW = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/"

# Quinlan, "Induction of Decision Trees", Machine Learning 1 (1986), Table 1.
QUINLAN = pd.DataFrame({
    "outlook": ["sunny", "sunny", "overcast", "rain", "rain", "rain", "overcast",
                "sunny", "sunny", "rain", "sunny", "overcast", "overcast", "rain"],
    "temperature": ["hot", "hot", "hot", "mild", "cool", "cool", "cool",
                    "mild", "cool", "mild", "mild", "mild", "hot", "mild"],
    "humidity": ["high", "high", "high", "high", "normal", "normal", "normal",
                 "high", "normal", "normal", "normal", "high", "normal", "high"],
    "windy": ["false", "true", "false", "false", "false", "true", "true",
              "false", "false", "false", "true", "true", "false", "true"],
    "play": ["N", "N", "P", "P", "P", "N", "P",
             "N", "P", "P", "P", "P", "P", "N"],
})


def load(name: str) -> pd.DataFrame:
    local = pathlib.Path(__file__).resolve().parent.parent / "datasets" / name
    return pd.read_csv(local if local.exists() else RAW + name)


def entropy(counts) -> float:
    """H of a set of counts, in bits, with the 0 log 0 = 0 convention."""
    counts = np.asarray(counts, dtype=float)
    total = counts.sum()
    if total == 0.0:
        return 0.0
    p = counts[counts > 0] / total
    return float(-(p * np.log2(p)).sum())


def gini(counts) -> float:
    counts = np.asarray(counts, dtype=float)
    p = counts / counts.sum()
    return float(1.0 - (p * p).sum())


def split_score(frame: pd.DataFrame, attribute: str, label: str, impurity=entropy) -> float:
    """The weighted impurity after splitting on one attribute, Quinlan's E(A)."""
    n = len(frame)
    total = 0.0
    for _, group in frame.groupby(attribute, observed=True):
        counts = group[label].value_counts().to_numpy()
        total += (len(group) / n) * impurity(counts)
    return total


def gain(frame: pd.DataFrame, attribute: str, label: str, impurity=entropy) -> float:
    before = impurity(frame[label].value_counts().to_numpy())
    return before - split_score(frame, attribute, label, impurity)


def split_information(frame: pd.DataFrame, attribute: str) -> float:
    """Quinlan's IV(A): the entropy of the split itself, ignoring the label."""
    return entropy(frame[attribute].value_counts().to_numpy())


def mutual_information(frame: pd.DataFrame, attribute: str, label: str) -> float:
    """I(A; class), computed as a KL between the joint and the marginals."""
    joint = np.array(pd.crosstab(frame[attribute], frame[label]), dtype=float)
    joint = joint / joint.sum()
    px = joint.sum(axis=1)
    py = joint.sum(axis=0)
    total = 0.0
    for i in range(joint.shape[0]):
        for j in range(joint.shape[1]):
            if joint[i, j] > 0.0:
                total += joint[i, j] * np.log2(joint[i, j] / (px[i] * py[j]))
    return total


def main() -> None:
    # ---- 1. Quinlan's own table -------------------------------------------
    label = "play"
    before = entropy(QUINLAN[label].value_counts().to_numpy())
    print("Quinlan 1986, Table 1: 14 rows, 9 of class P and 5 of class N")
    print(f"  I(9, 5) = {before:.4f} bits   (the paper prints 0.940)")
    assert abs(before - 0.940) < 5e-4

    expected = {"outlook": 0.246, "temperature": 0.029, "humidity": 0.151, "windy": 0.048}
    print("\n  attribute      E(A) bits   gain bits   paper   IV(A) bits   gain ratio")
    for attribute, paper in expected.items():
        e = split_score(QUINLAN, attribute, label)
        g = gain(QUINLAN, attribute, label)
        iv = split_information(QUINLAN, attribute)
        assert abs(g - paper) < 1.5e-3, f"{attribute}: {g:.4f} against the paper's {paper}"
        print(f"  {attribute:<13} {e:9.4f}   {g:9.4f}   {paper:5.3f}   {iv:10.4f}   {g / iv:10.4f}")

    e_outlook = split_score(QUINLAN, "outlook", label)
    iv_outlook = split_information(QUINLAN, "outlook")
    assert abs(e_outlook - 0.694) < 5e-4
    assert abs(iv_outlook - 1.5774) < 5e-4
    print(f"\n  two places where full precision and the printed figure part company:")
    print(f"    gain(outlook)  computed {gain(QUINLAN, 'outlook', label):.4f}   paper 0.246")
    print(f"      the paper subtracts its own rounded intermediates, 0.940 - 0.694 = 0.246")
    print(f"    IV(outlook)    computed {iv_outlook:.4f}   paper 1.578")
    print(f"      1.5774 rounds to 1.577, so the paper's third decimal is one out")
    print(f"  Neither changes any decision the algorithm makes. Both are worth seeing once,")
    print(f"  because a number you derived and a number you quoted are different objects.")
    print(f"  E(outlook) = {e_outlook:.4f}, exactly as printed.")

    # ---- 2. Quinlan's footnote 3, checked ---------------------------------
    print("\nQuinlan's footnote 3: 'maximizing the gain is equivalent to minimizing")
    print("E(A), which is the mutual information of the attribute A and the class'")
    print("  attribute      gain(A)     I(A; class)")
    for attribute in expected:
        g = gain(QUINLAN, attribute, label)
        mi = mutual_information(QUINLAN, attribute, label)
        assert abs(g - mi) < 1e-12, "gain and mutual information disagree"
        print(f"  {attribute:<13} {g:.9f}   {mi:.9f}")
    print("  identical to twelve decimal places, on every column. They are one function.")

    # ---- 3. The bias, on 12,000 real rows ---------------------------------
    signals = load("m10_signals.csv")
    print(f"\nm10_signals.csv: {len(signals)} rows, label 'churned'")
    print(f"  H(churned) = {entropy(signals['churned'].value_counts().to_numpy()):.4f} bits")
    print("\n  attribute       values      gain bits    IV bits   gain ratio")
    rows = []
    for attribute in ["plan", "support_tier", "theme", "account_ref"]:
        g = gain(signals, attribute, "churned")
        iv = split_information(signals, attribute)
        rows.append((attribute, signals[attribute].nunique(), g, iv, g / iv))
        print(f"  {attribute:<14} {signals[attribute].nunique():>7}    {g:9.4f}  {iv:9.4f}   {g / iv:9.4f}")

    honest = max(r[2] for r in rows if r[0] != "account_ref")
    identifier = [r for r in rows if r[0] == "account_ref"][0]
    print(f"\n  account_ref is an identifier. It carries no information about churn in the")
    print(f"  population, and it wins on raw gain by a factor of {identifier[2] / honest:.1f}.")
    assert identifier[2] > 5 * honest

    # ---- 4. Does the gain ratio fix it? -----------------------------------
    honest_ratio = max(r[4] for r in rows if r[0] != "account_ref")
    print(f"\n  gain ratio narrows the gap from {identifier[2] / honest:.1f}x to "
          f"{identifier[4] / honest_ratio:.2f}x, and does not close it on this data.")
    average_gain = float(np.mean([r[2] for r in rows]))
    above = [r[0] for r in rows if r[2] >= average_gain]
    print(f"  Quinlan applies the ratio only among attributes with average-or-better gain.")
    print(f"  Average gain here is {average_gain:.4f}, so that filter admits {above} alone,")
    print(f"  and the criterion still selects the identifier.")
    print(f"  The honest conclusion: gain ratio is a mitigation, not a cure. The cure is")
    print(f"  not to offer a tree a column with one value per row.")

    # ---- 5. Entropy against Gini ------------------------------------------
    print("\n  the same splits scored with Gini impurity instead of entropy:")
    print("  attribute       gain (entropy)   gain (Gini)   same winner?")
    ranked_entropy = sorted(["plan", "support_tier", "theme"],
                            key=lambda a: -gain(signals, a, "churned"))
    ranked_gini = sorted(["plan", "support_tier", "theme"],
                         key=lambda a: -gain(signals, a, "churned", gini))
    for attribute in ["plan", "support_tier", "theme"]:
        print(f"  {attribute:<14} {gain(signals, attribute, 'churned'):14.6f}   "
              f"{gain(signals, attribute, 'churned', gini):11.6f}")
    print(f"  entropy order {ranked_entropy}")
    print(f"  Gini order    {ranked_gini}")
    print(f"  same order: {ranked_entropy == ranked_gini}")
    print("  On these columns the two criteria agree on the ranking and disagree on the")
    print("  units. Gini is not entropy, and it is not a worse entropy; it is a different")
    print("  impurity that happens to be cheaper because it needs no logarithm.")


if __name__ == "__main__":
    main()
