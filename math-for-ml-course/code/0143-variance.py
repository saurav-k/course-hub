"""Variance, the computational form, and how spreads combine.

Lesson: Variance, and the computational form.

    python3 0804-variance.py

What it checks twice:

  1. Var(X) = E[(X - mu)^2] against Var(X) = E[X^2] - (E[X])^2. Two formulas,
     one number. The second is the one you can compute in a single pass, and the
     program shows the catastrophic-cancellation risk that makes it dangerous.
  2. Var(aX + b) = a^2 Var(X), measured.
  3. Var(X + Y) = Var(X) + Var(Y) + 2Cov(X, Y) on a dependent pair, and the
     collapse to Var(X) + Var(Y) on an independent one. The general law is
     checked first, because the special case is what people misremember.
  4. Var(sample mean) = sigma^2 / n, measured by resampling at four sizes.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "inference_runs.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/inference_runs.csv"
)


def load() -> pd.DataFrame:
    """Read the committed dataset, falling back to the published URL.

    The path is resolved from this file rather than the working directory, so the
    program runs from anywhere. The URL fallback is what lets it be pasted into
    Colab or a notebook with no checkout at all.
    """
    return pd.read_csv(DATA) if DATA.exists() else pd.read_csv(URL)


def main() -> None:
    frame = load()
    latency = frame["latency_ms"].to_numpy()
    n = len(latency)
    print(f"rows {n:,}\n")

    print("1. Variance by two formulas, on latency_ms")
    mu = latency.mean()
    definition = float(((latency - mu) ** 2).mean())
    computational = float((latency**2).mean() - mu**2)
    print(f"   E[(X - mu)^2]            {definition:.8f}")
    print(f"   E[X^2] - (E[X])^2        {computational:.8f}")
    print(f"   absolute gap             {abs(definition - computational):.2e}")
    assert np.isclose(definition, computational, rtol=1e-9)
    print(f"   population sd            {np.sqrt(definition):.6f} ms")
    print(f"   pandas .var(ddof=1)      {frame['latency_ms'].var(ddof=1):.8f}")
    print("   (ddof=1 divides by n-1; the gap to the n version is a factor of n/(n-1).)")

    print("\n   Why the second formula is dangerous: shift the column by 10^8.")
    shifted = latency + 1e8
    shifted_mu = shifted.mean()
    naive = float((shifted**2).mean() - shifted_mu**2)
    stable = float(((shifted - shifted_mu) ** 2).mean())
    print(f"   E[X^2] - (E[X])^2 on the shifted column   {naive:.6f}")
    print(f"   E[(X - mu)^2] on the shifted column       {stable:.6f}")
    print(f"   the true answer is unchanged at           {definition:.6f}")
    print("   Subtracting two huge nearly-equal numbers destroys the digits that")
    print("   carried the answer. Algebraically identical, numerically not.")

    print("\n2. Scaling: Var(aX + b) = a^2 Var(X)")
    a, b = 2.5, 500.0
    print(f"   Var({a}X + {b})   measured {np.var(a * latency + b):.6f}")
    print(f"   {a}^2 Var(X)        predicted {a**2 * definition:.6f}")
    assert np.isclose(np.var(a * latency + b), a**2 * definition)
    print("   The shift b vanished and the scale a squared.")

    print("\n3. How variances combine")
    pairs = (
        ("dependent   (prompt, output)", "prompt_tokens", "output_tokens"),
        ("independent (latency, dpi)  ", "latency_ms", "screen_dpi"),
    )
    for label, left_name, right_name in pairs:
        left = frame[left_name].to_numpy().astype(float)
        right = frame[right_name].to_numpy().astype(float)
        total = float(np.var(left + right))
        naive_sum = float(np.var(left) + np.var(right))
        covariance = float(((left - left.mean()) * (right - right.mean())).mean())
        general = naive_sum + 2 * covariance
        print(f"\n   {label}")
        print(f"     Var(X + Y) measured                 {total:>16,.3f}")
        print(f"     Var(X) + Var(Y)                     {naive_sum:>16,.3f}")
        print(f"     Var(X) + Var(Y) + 2Cov(X, Y)        {general:>16,.3f}")
        print(f"     the covariance term alone           {2 * covariance:>16,.3f}")
        assert np.isclose(total, general, rtol=1e-9), "the general law must always hold"
        error = abs(total - naive_sum) / total
        print(f"     dropping the covariance term is off by {error:>7.2%}")
    print("\n   The general law held both times. The short version held once.")

    print("\n4. Var(sample mean) = sigma^2 / n")
    rng = np.random.default_rng(20260825)
    print(f"   population variance sigma^2 = {definition:,.3f}")
    print("   These are draws WITHOUT replacement from a finite population of")
    print("   40,000, so the exact prediction carries the finite-population factor")
    print("   (N - n) / (N - 1), which is why the plain sigma^2/n runs high.\n")
    print(
        f"   {'n':>7}  {'measured':>12}  {'sigma^2/n':>12}  "
        f"{'with FPC':>12}  {'ratio to FPC':>12}"
    )
    for size in (10, 100, 1_000, 10_000):
        means = np.array(
            [rng.choice(latency, size=size, replace=False).mean() for _ in range(3_000)]
        )
        measured = float(means.var())
        plain = definition / size
        fpc = plain * (n - size) / (n - 1)
        print(
            f"   {size:>7,}  {measured:>12.4f}  {plain:>12.4f}  "
            f"{fpc:>12.4f}  {measured / fpc:>12.3f}"
        )
    print(
        "\n   Against the corrected prediction every ratio sits near 1, including\n"
        "   n = 10,000 where the plain formula was 32 percent high. Sampling a\n"
        "   quarter of a finite population is not the same experiment as sampling\n"
        "   from an infinite one, and the correction is the difference."
    )


if __name__ == "__main__":
    main()
