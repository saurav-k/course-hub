# 1103 - What a fitted coefficient is worth

**Module** M11 Capstone: regression, end to end · Part 3 of 3 · the course's last page
**Rung** frontier · **Owner** mlm-sfml-notes-r11 · **Issue** #54

> Provisional number. See 1101.

## Prerequisites, by number

M09 the statistical model around least squares and its inference (its S14).
M08 the sampling distribution and the square-root law. M07 the error model.

## The one idea

A slope is not a finding. The same slope is worthless on eight rows and decisive on
twenty thousand, and the number that tells them apart is the standard error.

## Boundary

M09 owns the error model, the sampling distributions, `sigma-hat^2 = SSE/(n-2)`, the
t-test and the intervals. This page applies them once, to the fit page 1102 produced,
and reads the answer.

## Beats

1. Two fits, the same slope: 0.060141 on eight rows, 0.060111 on 20,000.
2. The standard errors: 0.093435 against 0.000762. t of 0.64 against 78.85.
3. The null column through the same machinery: t 0.284, p 0.777, interval straddling zero.
   The machinery is what tells a real column from a null one, and it is not the slope.
4. Mean against individual: the interval for the mean at 300 s is 0.843 wide, the
   interval for one new session is 106.167 wide, a factor of 126.
5. Honesty: the prediction interval's lower end is negative, and spend cannot be.
   R-squared is 0.2372, so the model explains under a quarter of the variation.
   Association, not cause.
6. The course closes: what the reader can now do that they could not at M01.

## Figures

1. Orientation: `flowchart`, M08 and M09 feeding the last page, and out to the hub.
2. `svg.chart` the two confidence intervals on one slope axis, with zero marked.
   The 8-row interval is 430 px wide and crosses zero; the 20,000-row interval is 3.5 px.
   This figure is the page's whole argument.
3. `svg.chart` the fitted line with both bands, showing the narrow one inside the wide one.
4. `quadrantChart` placing the two columns on significance against effect size.

## Quizzes

1. Misconception: a large sample makes an effect large. (It makes a small one detectable.)
2. Misconception carried from the seeding notes, naming no person, per D16: a test that
   fails to reject does not accept the null.

## Practice

Given the eight-row fit, compute the standard error and the t-statistic, decide, then
say what would have to change to reverse the decision. `.p-check`: the interval must
contain the point estimate and, at t below 2, must contain zero.

## Numbers

All from `capstone_numbers.py`.
