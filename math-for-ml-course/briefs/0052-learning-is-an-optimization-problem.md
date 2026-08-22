# M06 L01 - Learning is an optimization problem

**Page `lessons/0052-learning-is-an-optimization-problem.html`** &middot; module M06, lesson 1 of 12 &middot; program `code/0052-learning-is-an-optimization-problem.py` &middot; dataset `datasets/m06-credit.csv`

**Label:** `core`
**Rung:** `med` / working
**Reading time target:** 9 min

## The single tight idea

A trained model is the answer to a minimisation problem, and naming its three parts - what varies, what is scored, what is forbidden - tells you exactly what you are allowed to change.

## Prerequisites

| Needs | From |
|---|---|
| Functions, and reading a symbol you have not met | M01 Foundations |
| A vector, so parameters can be one point in a space | M03 Vectors, matrices, and linear maps |
| The sum of a loss over rows of a data matrix | M03, rows-as-samples (D7) |

Forward cross-link only, no derivation: **M09 owns the gap between the average loss on your sample and the loss on the world.** One sentence and a link.

## Beats, in order

1. **A trained model is one chosen point in parameter space.** Same model, three different parameter vectors, three different scores. Nothing about "learning" yet.
2. **The three parts, named.** Parameters `theta` (what varies), objective `J(theta)` (what is scored), constraints (what is forbidden). Every training run is these three plus a solver.
3. **The objective is not the metric.** Accuracy is a step function of the parameters, flat between decision flips, so its gradient carries no direction. Cross-entropy is the differentiable stand-in. Name the substitution as a substitution, because the whole module optimises the stand-in.
4. **The objective is an average over the rows you have.** State the gap to the risk you care about in one sentence and hand it to M09.
5. **Read one real objective end to end.** L2-regularised logistic regression, every symbol named in words before it appears in the formula. This seeds L02 (is it convex?), L05 (that sum over rows is why SGD exists) and L11 (that second term is a constraint in disguise).
6. **The trade-off, in the same section as the technique.** Choosing a differentiable surrogate is what makes the problem solvable and is also what makes it the wrong problem.

## Named theorem and its stated proof

**None.** This page states no theorem, so D4 does not bite. It carries one derivation instead: the gradient of the regularised logistic objective, worked in full, because L03 steps along it four pages later.

## Planned figures

1. **Orientation, `flowchart`.** This page's slice of the prerequisite graph: "M03 vectors and the data matrix" and "M01 functions" into "THIS PAGE - training is minimising an objective" into "L02 convexity" and "L03 gradient descent", with "Every model in this course" attached by a dotted edge.
2. **`svg.chart`** (satisfies the floor). One parameter on the x-axis, objective on the y-axis, one `s-signal` curve, three candidate parameter values as dots, the best in `m-gold`. Kills: a loss being a number the model reports rather than a surface over the parameters.
3. **`quadrantChart`.** Axes "differentiable" against "what you are paid for". Accuracy, F1, AUC, MSE, cross-entropy placed. Kills "why not just optimise accuracy?" without a paragraph. Point labels under 26 characters.

## The worked example, in eight parts

Reading `sklearn.linear_model.LogisticRegression` as an objective, then evaluating it by hand.

1. The call the reader has made: `LogisticRegression()` with its current signature `(penalty='deprecated', *, C=1.0, l1_ratio=0.0, ..., solver='lbfgs', max_iter=100)`.
2. `C = 1.0` means the model you thought was unregularised is regularised. `C` is the **inverse** penalty strength.
3. Write the objective that signature implies, naming `theta`, `x_i`, `y_i`, `n`, `C`.
4. Four rows from `m06-credit.csv`, printed.
5. Candidate A: compute logit, probability, row loss, for each of the four.
6. Candidate B: the same four.
7. Average each, then add `||theta||^2 / (2C)`.
8. Compare. **The beat that matters: the penalty can flip the ranking the likelihood alone would give.** That flip is why the second term is there.

**Live-API warning for the writer.** `penalty='deprecated'` is current as of 2026-08-22 and is a moving target. Re-read the scikit-learn reference page on the day this page is written; do not write "the default penalty is l2", which was true for years and is not the current state.

## Quiz seeds

**Q1 (misconception).** In `LogisticRegression(C=1.0)`, what does `C` control?
Correct: the inverse of the regularization strength. Distractors: `max_iter`, `tol`, and "the learning rate the solver steps with", which does not exist because `lbfgs` has none.
Feedback must say a *smaller* `C` regularises harder, so the default is not "no regularization".

**Q2.** Why is classification accuracy not used as a training objective?
Correct: its gradient is zero almost everywhere. Distractors: too expensive (false, it is cheaper than the loss), undefined under imbalance (confuses undefined with misleading), cannot be computed until the epoch ends (false for a running estimate).

## Practice seed

**Stem.** Two candidate parameter vectors and six rows of `m06-credit.csv`. Which does the objective prefer at `C = 1.0`, and does the answer change at `C = 0.01`?
**Hint.** Compute the average log-loss and the penalty separately, and only add them at the end. The penalty does not depend on the data at all.
**Solution.** Eight lines: logits, probabilities, per-row losses, mean, penalty at each `C`, two totals each, the comparison, and the sentence naming which term changed the ranking.
**`.p-check`.** Both probabilities must lie strictly between 0 and 1, and the penalty at `C = 0.01` must be exactly 100 times the penalty at `C = 1.0`. If either fails, the arithmetic is wrong before the comparison starts.

## Code and dataset

**Program:** `code/m06-01-objective.py`. **Dataset:** `datasets/m06-credit.csv` (20,000 rows, seeded, generated by `datasets/make_m06_credit.py`).
**What it computes twice:** the regularised objective, once by an explicit Python loop over rows and once as a vectorised NumPy expression. The two must agree to machine precision, which is the point: the loop is what the page teaches and the vector form is what a codebase runs.

## Sources, primary only

- scikit-learn reference page for `LogisticRegression`, read for the signature and the meaning of `C`.
- Goodfellow, Bengio & Courville, *Deep Learning*, ch. 8, for empirical risk against true risk.
- Boyd & Vandenberghe, *Convex Optimization*, 7.1.1, for the logistic objective's form. (Its convexity is L02's claim, not this page's.)
