"""Cross-validation is an estimator, so it has a bias and a variance.

A cross-validation score is not a measurement of your model. It is an estimate
of expected prediction error, and it inherits every property lesson 0161 named.

WHAT K-FOLD ESTIMATES. Split the rows into K parts, train on K-1, score the
held-out part, rotate, average. Each fold's score is an unbiased estimate of
the prediction error of a model trained on THAT fold's training set, because
the held-out rows were not used to fit it. Averaging over folds therefore
estimates the expected error over training sets of size about n(K-1)/K, drawn
from the same distribution. It does NOT estimate the error of the one model
you fitted on all n rows. The gap between "n(K-1)/K" and "n" is the bias.

ITS BIAS. Small K trains on less data. If the learning curve is still rising
at your sample size, 5-fold reports an error higher than the model you will
actually ship would have. Large K shrinks that gap.

ITS VARIANCE. Leave-one-out trains n models that differ by one row each, so
their errors are strongly correlated and the average is unstable. The standing
recommendation is 5 or 10 folds, which trades a little bias for much less
variance.

THE TRAP, which is the reason this page exists. Any step that LEARNS from the
labels must sit inside the fold loop. Screen features on the whole dataset and
then cross-validate, and the surviving features have already seen the rows they
are about to be tested on. This program reproduces the standard counterexample:
labels independent of every feature, so the true error of any classifier is
50 per cent, and the wrong pipeline reports a small single-digit number.

THE ERROR BAR. The fold scores are not independent, because their training sets
overlap heavily, so the naive standard deviation across folds understates the
true variance of the estimate. Bengio and Grandvalet (2004) prove there is no
universal unbiased estimator of that variance.

Datasets: features.csv for the honest half, and an in-program pure-noise
classification set for the trap, because no committed dataset has labels
independent of every column and inventing one to be useless would be odd.

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

LOCAL = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "features.csv"
URL = "https://<hub>/math-for-ml-course/datasets/features.csv"
DATA = LOCAL if LOCAL.exists() else URL

SEED = 20260822
NOISE_SD = 3.0          # stated in datasets/generate/make_features.py
IRREDUCIBLE = NOISE_SD ** 2


def fold_indices(n: int, k: int, rng: np.random.Generator) -> list[np.ndarray]:
    """K roughly equal parts of a random permutation."""
    return np.array_split(rng.permutation(n), k)


def ridge_fit(x: np.ndarray, y: np.ndarray, lam: float = 1.0) -> np.ndarray:
    return np.linalg.solve(x.T @ x + lam * np.eye(x.shape[1]), x.T @ y)


def cv_squared_error(x: np.ndarray, y: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray:
    """One mean squared error per fold. Nothing is fitted outside the loop."""
    scores = []
    for held in fold_indices(x.shape[0], k, rng):
        mask = np.ones(x.shape[0], dtype=bool)
        mask[held] = False
        beta = ridge_fit(x[mask], y[mask])
        scores.append(float(((y[held] - x[held] @ beta) ** 2).mean()))
    return np.array(scores)


def honest_half() -> None:
    frame = pd.read_csv(DATA)
    cols = [c for c in frame.columns if c.startswith("x")]
    x_all = frame[cols].to_numpy(float)
    y_all = frame["y"].to_numpy(float)
    rng = np.random.default_rng(SEED)
    n_pool = x_all.shape[0]

    print("1. THE LEARNING CURVE IS WHERE K-FOLD'S BIAS COMES FROM")
    print(f"   features.csv: {n_pool:,} rows, {x_all.shape[1]} predictors,")
    print(f"   generated with noise sd {NOISE_SD}, so no model can beat a squared error of {IRREDUCIBLE:.1f}.\n")
    print("   First, with no cross-validation anywhere: fit on m rows, score on 3,000")
    print("   rows the model never saw, and average over 60 fresh draws of the m rows.\n")
    print(f"   {'m, rows trained on':>20}  {'true error at that m':>21}")
    curve = {}
    for m in (100, 160, 180, 190, 199, 200):
        errs = []
        for r in range(60):
            g = np.random.default_rng(SEED + 31 * r)
            idx = g.choice(n_pool, size=m + 3000, replace=False)
            tr, te = idx[:m], idx[m:]
            beta = ridge_fit(x_all[tr], y_all[tr])
            errs.append(float(((y_all[te] - x_all[te] @ beta) ** 2).mean()))
        curve[m] = float(np.mean(errs))
        print(f"   {m:>20,}  {curve[m]:>21.4f}")
    print("   The curve falls as m grows and is still falling at 200, which is exactly")
    print("   the condition under which K-fold's bias bites.\n")

    print("   Now cross-validate 200 rows. K-fold trains on n(K-1)/K of them, so what")
    print("   it estimates is the error at THAT point on the curve above, not at 200.")
    print("   Both columns below average over 40 fresh 200-row datasets, so they are")
    print("   measuring the same thing in the same way.\n")
    print(f"   {'K':>18}  {'trains on':>10}  {'CV estimate':>12}  {'curve at that m':>16}  {'gap':>8}")
    for k in (2, 5, 10, 20, 200):
        trained_on = 200 - 200 // k
        vals = []
        for r in range(40):
            g = np.random.default_rng(SEED + 7 * r + 1)
            idx = g.choice(n_pool, size=200, replace=False)
            vals.append(cv_squared_error(x_all[idx], y_all[idx], k, g).mean())
        est = float(np.mean(vals))
        nearest = min(curve, key=lambda m: abs(m - trained_on))
        label = "200 (leave-one-out)" if k == 200 else str(k)
        print(f"   {label:>18}  {trained_on:>10,}  {est:>12.4f}  {curve[nearest]:>16.4f}"
              f"  {est - curve[nearest]:>+8.4f}")
    print("   Read the last two columns against each other, never against the error of")
    print("   a model trained on all 200 rows: K-fold is not estimating that quantity.")
    print("   The gap column is small and shrinks as K grows, which is the bias arriving")
    print("   exactly where the learning curve said it would.")

    print("\n2. AND ITS VARIANCE, WHICH IS WHERE THIS PROGRAM PARTS FROM THE FOLKLORE")
    print("   The estimator's variance is how much its answer moves when the DATA")
    print("   changes, so draw a fresh 200 rows each time. Measuring across partitions")
    print("   of one fixed dataset instead would flatter leave-one-out, which has no")
    print("   partition to vary and would print exactly zero.\n")
    print(f"   {'K':>18}  {'mean estimate':>14}  {'sd over 40 fresh datasets':>27}")
    for k in (5, 10, 20, 200):
        vals = []
        for r in range(40):
            g = np.random.default_rng(SEED + 7 * r + 1)
            idx = g.choice(n_pool, size=200, replace=False)
            vals.append(cv_squared_error(x_all[idx], y_all[idx], k, g).mean())
        label = "200 (leave-one-out)" if k == 200 else str(k)
        print(f"   {label:>18}  {float(np.mean(vals)):>14.4f}  {float(np.std(vals, ddof=1)):>27.5f}")
    print("\n   READ THIS HONESTLY. The textbook recommendation of five or ten folds")
    print("   rests on leave-one-out being almost unbiased but highly VARIABLE, and")
    print("   that is not what this table shows: the spread barely moves with K, and")
    print("   leave-one-out is if anything the tightest column, because it trains on")
    print("   the most data.")
    print("   The explanation is not that the textbooks are wrong. It is that this")
    print("   measurement does not isolate the quantity they are talking about. The")
    print("   spread here is dominated by which 200 rows were drawn, and the variance")
    print("   attributable to the partition is a separate component that Bengio and")
    print("   Grandvalet (2004) decompose into three parts, only one of which this")
    print("   crude experiment can see. Their main theorem is that no universal")
    print("   unbiased estimator of that variance exists at all.")
    print("   So: take the bias story from section 1, which is measured here, and take")
    print("   the variance story on citation. A page that printed this table and then")
    print("   claimed it demonstrated the recommendation would be misreading its own")
    print("   output.")


def the_trap() -> None:
    """Labels independent of every feature, so the true error is exactly 50 per cent."""
    print("\n3. THE TRAP: SELECTION OUTSIDE THE FOLD LOOP")
    rng = np.random.default_rng(SEED)
    n, p, keep, k = 50, 5000, 100, 5
    x = rng.normal(size=(n, p))
    y = rng.integers(0, 2, size=n)          # independent of x, by construction
    print(f"   {n} samples, {p:,} standard-normal predictors, labels drawn independently.")
    print("   No classifier can do better than chance here. The true error is 50.00%.\n")

    def nearest_neighbour_error(train_x, train_y, test_x, test_y) -> float:
        d = ((test_x[:, None, :] - train_x[None, :, :]) ** 2).sum(axis=2)
        return float((train_y[d.argmin(axis=1)] != test_y).mean())

    # WRONG: screen on all the data, then cross-validate the survivors.
    corr = np.array([abs(np.corrcoef(x[:, j], y)[0, 1]) for j in range(p)])
    chosen = np.argsort(corr)[-keep:]
    x_screened = x[:, chosen]
    wrong = [nearest_neighbour_error(x_screened[~np.isin(np.arange(n), h)],
                                     y[~np.isin(np.arange(n), h)],
                                     x_screened[h], y[h])
             for h in fold_indices(n, k, np.random.default_rng(SEED + 7))]
    wrong_error = float(np.mean(wrong))

    # RIGHT: screen inside the loop, using only the training rows of each fold.
    right = []
    for held in fold_indices(n, k, np.random.default_rng(SEED + 7)):
        mask = np.ones(n, dtype=bool)
        mask[held] = False
        c = np.array([abs(np.corrcoef(x[mask, j], y[mask])[0, 1]) for j in range(p)])
        pick = np.argsort(c)[-keep:]
        right.append(nearest_neighbour_error(x[mask][:, pick], y[mask], x[held][:, pick], y[held]))
    right_error = float(np.mean(right))

    print(f"   screening OUTSIDE the fold loop   reported error {wrong_error:6.2%}")
    print(f"   screening INSIDE the fold loop    reported error {right_error:6.2%}")
    print(f"   the truth                                        {0.5:6.2%}")
    assert wrong_error < right_error - 0.15, (
        "the wrong pipeline should report a materially lower error than the right one; "
        "if it does not, the screening step is not leaking and the demonstration is broken"
    )
    print("\n   Why. The screening step used every row, so the surviving predictors were")
    print("   chosen partly because they happened to match the labels of the rows they")
    print("   are then tested on. Leaving rows out AFTER selecting does not mimic a")
    print("   fresh test set, because those rows already voted on the selection.")

    held = fold_indices(n, k, np.random.default_rng(SEED + 7))[0]
    on_held = np.array([abs(np.corrcoef(x[held][:, j], y[held])[0, 1]) for j in chosen])
    fresh = rng.normal(size=(len(held), keep))
    baseline = np.array([abs(np.corrcoef(fresh[:, j], y[held])[0, 1]) for j in range(keep)])
    print(f"\n   measured on one held-out fold, the pre-selected predictors correlate")
    print(f"   with its labels at a mean of {on_held.mean():.4f}, against {baseline.mean():.4f}")
    print("   for predictors that never saw it. That difference is the leak, in a number.")


def the_error_bar() -> None:
    print("\n4. THE ERROR BAR IS HARDER THAN IT LOOKS")
    frame = pd.read_csv(DATA)
    cols = [c for c in frame.columns if c.startswith("x")]
    rng = np.random.default_rng(SEED)
    subset = rng.choice(len(frame), size=200, replace=False)
    x = frame[cols].to_numpy(float)[subset]
    y = frame["y"].to_numpy(float)[subset]

    scores = cv_squared_error(x, y, 10, np.random.default_rng(SEED + 3))
    naive_se = float(np.std(scores, ddof=1) / np.sqrt(scores.size))
    repeats = [cv_squared_error(x, y, 10, np.random.default_rng(SEED + 100 * r)).mean()
               for r in range(60)]
    true_sd = float(np.std(repeats, ddof=1))
    print(f"   mean of the 10 fold scores            {scores.mean():8.4f}")
    print(f"   naive standard error across folds     {naive_se:8.4f}")
    print(f"   actual sd of the estimate over 60 repartitions {true_sd:8.4f}")
    print("   The naive figure treats ten overlapping training sets as ten independent")
    print("   samples. They are not, and the two numbers are not measuring the same")
    print("   thing. Report the fold spread as a description, never as a standard error,")
    print("   and if the decision matters, repeat the whole cross-validation and report")
    print("   the spread across repetitions instead.")


def main() -> None:
    honest_half()
    the_trap()
    the_error_bar()


if __name__ == "__main__":
    main()
