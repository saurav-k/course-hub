# 0001 - Reading a formula: indices, sigma, and pi

| | |
|---|---|
| Module | M01 Foundations |
| Rung | foundation (`pill easy`) |
| Partition | core |
| Prose budget | 1,000 to 1,200 words |
| Prerequisites | none; this is the first content page after lesson zero |
| Needed by | every later page; M03 for the data matrix, M07 for expectations |
| Code | `code/0001-reading-a-formula.py` |
| Dataset | `datasets/tickets.csv` |
| Named theorem | **none.** Say so in the teacher note rather than manufacturing one. |

## The one idea

Every formula in a machine learning paper is a loop with an accumulator, and the index tells you what it loops over.

## The seam with lesson zero

Lesson zero is about the course.
This page is about the notation and it opens with a real formula on the screen inside the first two hundred words.

## Beats, in order

1. Name the reader's real problem in one paragraph: the difficulty is not the mathematics, it is that the notation compresses a loop into three characters and nobody says so out loud.
2. A variable, an index, and the two places an index can sit. `x^(i)` in parenthesised superscript is the **i-th example**; `x_j` in subscript is the **j-th feature**. Take the convention from the Deep Learning Book's notation table, which is what the field actually uses.
3. `Sum` as a for-loop with a running total. Three parts, named explicitly: where the index starts, where it stops, what is accumulated.
4. The index is a **bound** variable. `Sum_{i=1}^{n} a_i` and `Sum_{k=1}^{n} a_k` are the same number. This is the fact that unlocks reading unfamiliar papers.
5. `Prod` is the same loop with a running product. State the empty sum (0) and the empty product (1) here; both are load-bearing on 0007 and 0008.
6. Double sums as nested loops, and the trap: in `Sum_i Sum_j A_ij B_ij` the indices are independent, and tying them together silently computes something else.
7. Read one real formula end to end: the gradient estimate in Deep Learning Book Algorithm 8.1. Every symbol named in words before it is used.
8. Close on the habit: when a formula stops you, write down what the index ranges over before anything else.

## Figures (4, at least one `svg.chart`)

- **F1 orientation, `flowchart LR`.** "You can already read a for-loop" to "THIS PAGE: notation is a loop" to "every formula in the rest of this course", with a dotted node for M01 Foundations. Kills: that notation is a separate subject rather than a compression of something the reader has.
- **F2 `sequenceDiagram`.** The accumulator stepping through `Sum_{i=1}^{4} a_i`: participants Index, Term, Total, with Total's value shown updating four times. Kills: that `Sum` is one mysterious operation.
- **F3 inline `svg.chart`.** The data matrix as a grid of cells, **row 2 shaded** and labelled `x^(2)` (one ticket) and **column 3 shaded** and labelled `x_3` (one feature), meeting at `X_{2,3}`. Kills: reading the sample index as a feature index. Mermaid cannot draw a highlighted grid.
- **F4 `flowchart LR`.** The three parts of a `Sum` mapped onto the three parts of a `for` loop, accumulator drawn once and shared. Kills: that the notation contains anything the reader's own code does not.

## Worked example (eight parts)

Read Algorithm 8.1 aloud against a real minibatch of `tickets.csv`.
`m = 32`; `i` indexes tickets inside the minibatch, never features; `theta` carries no `i` because one parameter vector is shared by all 32.
Counting check: `Sum_{i=1}^{32} Sum_{j=1}^{d} X_ij^2` has `32 x d` scalar terms.

- **Sanity check.** The term count is the product of the two loop bounds, and nothing else.
- **What changes if** the minibatch doubles: the term count doubles and the average barely moves, which is the whole reason for the `1/m`.

## Code

`code/0001-reading-a-formula.py`.
Computes one quantity three ways against `tickets.csv` and asserts all three agree: an explicit double `for` loop, a NumPy vectorised expression, and a Pandas one-liner.
The point is that the three are the same `Sum`, so the reader sees the notation, the loop and the library as one thing.

## Quizzes

- **Q1** (misconception): in `x^(3)`, what does the parenthesised superscript pick out?
  `The third training example in the dataset` / `The third feature of the input vector` / `The third power of the feature value` / `The third layer of the trained network`
  Feedback: option 2 is the subscript's job; option 3 is what a bare superscript means in ordinary algebra, which is why the parentheses are there; option 4 names a real thing the notation never denotes.
- **Q2**: a ticket contains none of a model's known tokens, so its score sums over an empty set. What is the sum?
  `Undefined, so the score errors out` / `Zero, because an empty sum is zero` / `One, because an empty sum is one` / `The prior, which is added in later`
  Feedback: option 3 is the empty **product**; option 4 is true of naive Bayes and answers a different question; option 1 is what a naive implementation does, not what the notation says.

Answer indices assigned at module integration.

## Practice

Read a regularised loss and say what every index ranges over.
`J(theta) = (1/m) Sum_{i=1}^{m} (y^(i) - yhat^(i))^2 + lambda Sum_{j=1}^{d} theta_j^2`, with `m = 32` and `d` features.
(a) What does `i` range over, and `j`? (b) How many squared terms in each sum? (c) Why does the second sum carry no `i`?

- **Hint.** Read each `Sum`'s own bounds. Neither index escapes its own sum.
- **Solution.** (a) examples inside the minibatch, and parameters. (b) 32 and `d`. (c) one parameter vector is shared by all 32 examples, so the penalty belongs to the model, not to any example. If it carried an `i` you would penalise the same weights 32 times.
- **`.p-check`.** The two sums have different bounds, so any answer where both counts are equal has confused the two indices.

## Primary source to go deeper

Goodfellow, Bengio and Courville, *Deep Learning*, the Notation section, `https://www.deeplearningbook.org/contents/notation.html`.
