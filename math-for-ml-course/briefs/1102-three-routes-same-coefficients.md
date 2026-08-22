# 1102 - Three routes to the same two numbers

**Module** M11 Capstone: regression, end to end · Part 2 of 3
**Rung** frontier · **Owner** mlm-sfml-notes-r11 · **Issue** #54

> Provisional number. See 1101.

## Prerequisites, by number

M03 least squares as linear algebra and the projection picture (its L12).
M05 the gradient. M06 descent, step size, conditioning. M04 standardisation.

## The one idea

The closed form and the iterative method are not two answers. They are two ways of
reaching the one point where the gradient is zero.

## Boundary

M03 owns the derivation of the normal equations and the projection theorem.
M06 owns descent and conditioning. This page runs both on one dataset and checks
they agree. The only argument it makes for itself is why they must.

## Beats

1. The model in one line, every symbol named. Stated, not derived. Link to M03 and M09.
2. Route A, the normal equations, worked by hand on eight rows: slope 0.060141.
3. Route B, descent on standardised features, 40 iterations to slope 0.060111.
4. The stated proof of the capstone's own claim: the two routes share a fixed point
   because the gradient of the squared-error objective vanishes exactly at the normal
   equations. Four lines. The step that does the work is named.
5. Why standardising was not cosmetic: raw condition number 1.357e5, largest safe
   step 1.081e-5, against a standardised condition number of exactly 1.
6. The residual check: orthogonal to both columns, to 1e-7.

## Figures

1. Orientation: `flowchart`, M03 and M06 converging on one fit.
2. `svg.chart` coefficient path against iteration, with the closed form as a reference line.
3. `svg.chart` the projection picture: residual perpendicular to the fitted direction.
4. `sequenceDiagram` of one descent step, to separate order from structure.

## Quizzes

1. Misconception: descent is an approximation and the closed form is exact.
2. What the condition number predicts about the largest safe step.

## Practice

Two descent steps by hand from the standardised start, then compare to the table.
`.p-check`: each step must move toward 0.487 and never past it at this step size.

## Numbers

All from `capstone_numbers.py`.
