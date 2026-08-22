"""Conditional expectation is the best predictor squared error can have.

Lesson: Conditional expectation and MMSE.

    python3 0816-conditional-expectation-mmse.py

What it checks twice:

  1. E[Y|X] is a FUNCTION of X, not a number. The program builds it as a lookup
     from X to a value, and shows the tower property E[E[Y|X]] = E[Y].
  2. The MMSE theorem, tested by brute force. Among many candidate predictors,
     including deliberately good ones, none beats the conditional mean. The
     program searches for a counterexample and fails to find one.
  3. Orthogonality: the residual Y - E[Y|X] is uncorrelated with EVERY function
     of X. That is the projection picture, made arithmetic.
  4. The law of total variance, checked to machine precision, and the contrast
     that matters in practice: squared error targets the conditional MEAN, and
     absolute error targets the conditional MEDIAN.
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
RNG = np.random.default_rng(20260903)


def load() -> pd.DataFrame:
    """Read the committed dataset, falling back to the published URL.

    The path is resolved from this file rather than the working directory, so the
    program runs from anywhere. The URL fallback is what lets it be pasted into
    Colab or a notebook with no checkout at all.
    """
    return pd.read_csv(DATA) if DATA.exists() else pd.read_csv(URL)


def main() -> None:
    frame = load()
    # Predict latency from a discretised load level, so every conditional slice
    # has thousands of rows and E[Y|X] is estimated rather than interpolated.
    frame["load_level"] = pd.qcut(frame["gpu_util"], 8, labels=False)
    y = frame["latency_ms"].to_numpy(dtype=float)
    x = frame["load_level"].to_numpy()
    print(f"rows {len(frame):,}, predicting latency_ms from an 8-level load bucket\n")

    print("1. E[Y|X] is a function of X")
    conditional = frame.groupby("load_level")["latency_ms"].agg(["count", "mean", "median", "var"])
    print(conditional.round(4).to_string())
    lookup = conditional["mean"].to_numpy()
    predictor = lookup[x]
    print(f"\n   E[Y]           {y.mean():.6f}")
    print(f"   E[E[Y|X]]      {predictor.mean():.6f}   (the tower property)")
    assert np.isclose(y.mean(), predictor.mean())
    print("   Equal. Averaging the slice means, weighted by how often each slice")
    print("   happens, returns the overall mean.")

    print("\n2. The MMSE theorem, attacked by brute force")
    print("   Claim: no function of X beats E[Y|X] on squared error. Try to break it.")

    def mse(prediction: np.ndarray) -> float:
        return float(((y - prediction) ** 2).mean())

    baseline = mse(predictor)
    candidates = {
        "E[Y|X], the conditional mean": predictor,
        "the overall mean E[Y]": np.full_like(y, y.mean()),
        "the conditional median": conditional["median"].to_numpy()[x],
        "conditional mean, scaled 1.02": predictor * 1.02,
        "conditional mean, scaled 0.98": predictor * 0.98,
        "conditional mean + 5 ms": predictor + 5.0,
        "conditional mean, shrunk 10% to E[Y]": 0.9 * predictor + 0.1 * y.mean(),
    }
    print(f"\n   {'predictor':<40}{'MSE':>16}{'vs baseline':>14}")
    for name, prediction in candidates.items():
        value = mse(prediction)
        print(f"   {name:<40}{value:>16.4f}{value - baseline:>+14.4f}")
        assert value >= baseline - 1e-9, f"{name} beat the conditional mean"

    print("\n   And 20,000 random perturbations of the slice values:")
    best_found = baseline
    for _ in range(20_000):
        perturbed = lookup + RNG.normal(0, 12.0, len(lookup))
        best_found = min(best_found, mse(perturbed[x]))
    print(f"   best MSE found by random search   {best_found:.4f}")
    print(f"   the conditional mean              {baseline:.4f}")
    assert best_found >= baseline - 1e-9
    print("   Nothing beat it. The theorem is not a heuristic.")

    print("\n3. Why: the residual is orthogonal to every function of X")
    residual = y - predictor
    print(f"   mean residual                                {residual.mean():>12.2e}")
    print(f"   correlation with X itself                    {np.corrcoef(residual, x)[0, 1]:>12.2e}")
    print(f"   correlation with X squared                   "
          f"{np.corrcoef(residual, x.astype(float) ** 2)[0, 1]:>12.2e}")
    print(f"   correlation with the prediction itself       "
          f"{np.corrcoef(residual, predictor)[0, 1]:>12.2e}")
    for _ in range(3):
        arbitrary = RNG.normal(size=len(lookup))[x]
        print(f"   correlation with a random function of X      "
              f"{np.corrcoef(residual, arbitrary)[0, 1]:>12.2e}")
    print("   All zero to machine precision. That is what 'projection' means: the")
    print("   error points straight out of the space of functions of X, so no")
    print("   function of X can absorb any more of it.")

    print("\n4. The law of total variance")
    within = float(
        (frame.groupby("load_level")["latency_ms"].transform(lambda s: s - s.mean()) ** 2).mean()
    )
    between = float(((predictor - y.mean()) ** 2).mean())
    print(f"   E[Var(Y|X)]  unexplained   {within:>14.6f}")
    print(f"   Var(E[Y|X])  explained     {between:>14.6f}")
    print(f"   sum                        {within + between:>14.6f}")
    print(f"   Var(Y)                     {y.var():>14.6f}")
    assert np.isclose(within + between, y.var())
    print(f"\n   the load bucket explains {between / y.var():.2%} of the variance in latency")

    print("\n5. Squared error targets the mean; absolute error targets the median")
    print("   The slices are strongly right-skewed, so the two differ a lot.")

    def mae(prediction: np.ndarray) -> float:
        return float(np.abs(y - prediction).mean())

    median_predictor = conditional["median"].to_numpy()[x]
    print(f"\n   {'predictor':<28}{'MSE':>16}{'MAE':>14}")
    print(f"   {'conditional mean':<28}{mse(predictor):>16.4f}{mae(predictor):>14.4f}")
    print(f"   {'conditional median':<28}{mse(median_predictor):>16.4f}"
          f"{mae(median_predictor):>14.4f}")
    assert mse(predictor) < mse(median_predictor)
    assert mae(median_predictor) < mae(predictor)
    print("\n   Each wins its own loss and loses the other. Which one a model learns")
    print("   is decided entirely by which loss it was trained on, and on skewed")
    print("   targets they are visibly different predictions. That is why an")
    print("   MSE-trained model on a multimodal target produces the blurred")
    print("   average rather than any answer that actually occurs.")


if __name__ == "__main__":
    main()
