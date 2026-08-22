# 0171 Cross-validation as an estimator of generalisation error

| | |
|---|---|
| Module | M09 Estimation, testing, and inference |
| Rung | `pill hard` |
| Class | core |
| Word budget | 1,100 to 1,400 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S16 |

## One tight idea

A cross-validation score is not a measurement of your model, it is an estimate of expected prediction error, and it inherits every property `0161` named.

## Prerequisites

`0161` for bias, variance and MSE. `0170` for what it is estimating and for the learning-curve vocabulary.

## Downstream

The last page of the estimation arc. M11's capstone reports a cross-validated number and assumes this page.

## Boundaries: what this page must not teach

- **Not model selection as a workflow.** No grid search, no hyperparameter tuning recipe. The page is about what the number means.
- **Not the bootstrap.** One sentence naming it as the sibling resampling estimator.
- **Not nested cross-validation as a procedure to follow.** Name it in one sentence as the fix for selecting *and* estimating on the same data, and stop.
- This page has **no landed program**. It is the one M09 page whose `code/0171-cross-validation-as-an-estimator.py` must be written with the page. Every other M09 page reuses a program from #57.

## Beats, in order

1. Frame it as an estimator from the first sentence, because that framing is the whole page and it is not how the reader currently holds it.
2. The K-fold procedure, drawn: split into K parts, train on K-1, score the held-out one, rotate, average.
3. **What it estimates.** The expected extra-sample error, averaged over training sets, and *not* the error of the particular model you fitted on your particular training set. Quote the distinction; it is subtle and it is load-bearing.
4. Its bias: small `K` trains on less data, so if the learning curve is still rising at your sample size, 5-fold overestimates the error. Draw the learning curve and mark the two training sizes.
5. Its variance: leave-one-out is almost unbiased and highly variable, because its `n` fits are nearly identical and their errors are strongly correlated. The standing recommendation is 5 or 10 folds, and the page says why rather than asserting it.
6. **The trap, with numbers, in a `.callout.warn`.** Screen features on the whole dataset and then cross-validate, and with 50 samples, 5,000 pure-noise predictors and a true error of 50 per cent, the reported error comes out at about 3 per cent. Every step that *learns* must sit inside the fold.
7. Show why: the pre-selected predictors' correlations measured on a held-out fold average about 0.28 rather than 0. They have already seen the fold they are about to be tested on.
8. **The error bar is harder than it looks.** The fold scores are correlated because their training sets overlap, so the naive standard error across folds understates the true variance. There is no universal unbiased estimator of that variance.

## Named results and their stated proofs (D4)

**Result 1 (what K-fold estimates).** K-fold cross-validation estimates `Err = E[L(Y, f_hat(X))]`, the expected prediction error averaged over training sets of size roughly `n(K-1)/K`, drawn from the same distribution.

**Justification.** Each fold's score is an unbiased estimate of the prediction error of a model trained on that fold's training set, because the held-out rows were not used to fit it. Averaging over folds averages over `K` such training sets. What the average is therefore unbiased for is the expected error over training sets of that size, not the error of any one fitted model. The gap between "of size `n(K-1)/K`" and "of size `n`" is the bias in beat 4. []

**Result 2 (no unbiased variance estimator).** There is no universal estimator of the variance of the K-fold estimate that is unbiased under all distributions.

**Stated, not proved.** This is the main theorem of Bengio and Grandvalet (2004), whose text was read for this course. The proof rests on an eigen-decomposition of the covariance matrix of the fold errors, which has three distinct eigenvalues and therefore three degrees of freedom, and the argument is beyond this page. What the page owes the reader is the consequence: the naive standard error across folds ignores the correlation between them and **grossly underestimates** the variance, in the paper's own word.

**The honest boundary.** Result 1's "drawn from the same distribution" is the assumption that fails most often in practice: time-ordered data, grouped data, and any data where rows share a subject all break it, and the standard fix is to fold on the group rather than on the row. One sentence, named, not developed.

## Figures

- **Orientation**, `flowchart`: *the tradeoff (`0170`)* -> **THIS PAGE: measuring it, with an estimator that has its own bias and variance** -> *M11's capstone*.
- **`svg.chart`**, required: two bars, the reported cross-validation error against the true error, 3 per cent against 50 per cent, for the pre-screened pipeline. Kills: "a cross-validation number is self-validating".
- **`flowchart`**: the K-fold split with the held-out block moving across five rows and the averaging step at the end.
- **`svg.chart`**: a learning curve of accuracy against training-set size, with the 5-fold and 10-fold training sizes marked below the full size, and the vertical gap annotated as the bias.

## Worked example

`features.csv` reproduces the trap directly, since it carries five real predictors among thirty and the noise level is known. Run the wrong pipeline: screen for the most correlated predictors on all the rows, then cross-validate, and watch the reported error collapse below the truth. Then run the right one, with the screening moved inside the fold loop, and watch it come back. Print the histogram of pre-selected predictors' correlations measured on held-out folds, centred well away from zero.

Then the fold-correlation point: report the mean and the across-fold standard deviation, and say explicitly that the second is not a standard error you may quote.

## Quiz seeds

1. **Misconception.** You screen 5,000 features for label correlation, keep the best 100, then run 5-fold cross-validation. What is wrong? Answer: the selection step saw the held-out data. Distractors: five folds are too few; the model is too simple. Feedback names the 3-per-cent-against-50-per-cent result so the size of the error is concrete.
2. **Mechanism.** Leave-one-out compared with 10-fold is generally what? Answer: less biased, more variable. Distractor "better on both counts" must be present, since it is the intuition the recommendation contradicts.

## Practice seed

**Stem.** You have 200 labelled examples and a pipeline of standardise, then select the top 20 features by correlation, then fit logistic regression. Write the correct 5-fold procedure, saying which steps sit inside the fold loop and why. Then: you get CV accuracy 0.86 with a per-fold standard deviation of 0.04. May you report `0.86 +/- 0.036` as a 95 per cent interval?
**Hint.** Ask of each step: does it learn anything from the data? If so, it cannot see the held-out fold.
**Solution path.** Split into folds first; then per fold, fit the standardiser on the training folds only, select features using training-fold labels only, fit, and score the held-out fold; average the five scores. Both the standardiser and the selector learn, so both must sit inside. No, you may not report that interval: the five scores are not independent, their training sets overlap heavily, and Result 2 says the naive standard error understates the variance.
**`.p-check`.** If moving the selection inside the fold loop does not change your score at all, the selection is not learning from the labels, and you should check that it is doing anything.

## Code and dataset

**This page owes a new program.** `code/0171-cross-validation-as-an-estimator.py` against `datasets/features.csv`. It must compute the score twice: once with the screening outside the fold loop and once inside, print both against the known truth, and carry an assertion that the wrong pipeline reports a materially lower error than the right one. Follow BUILDER-SPEC section 6: numpy and pandas only, local path with a URL fallback, and the numbers the page quotes must be the numbers it prints.

## Sources

- Hastie, Tibshirani and Friedman, *ESL* 2nd edition, section 7.10 page 241 for what K-fold estimates, 7.10.1 page 243 for the bias and the 5-or-10 recommendation, and 7.10.2 page 245 for the worked trap and its 3-per-cent figure.
- Kohavi (1995), IJCAI-95, 1137-1143, for "leave-one-out is almost unbiased, but it has high variance" and the stratified ten-fold recommendation.
- Bengio and Grandvalet (2004), *JMLR* 5, 1089-1105, for Result 2 and for the naive estimator underestimating the variance.
