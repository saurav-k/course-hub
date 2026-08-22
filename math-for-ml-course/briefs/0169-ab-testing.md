# 0169 A/B testing, and the two-proportion test in production

| | |
|---|---|
| Module | M09 Estimation, testing, and inference |
| Rung | `pill med` |
| Class | core |
| Word budget | 1,100 to 1,400 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S12 |

## One tight idea

The arithmetic of an online experiment is the easy part; the design decisions before it and the stopping rule during it decide whether the number means anything.

## Prerequisites

`0167` for the test, `0168` for multiplicity, `0166` for the interval. `0027` for what randomisation is doing, and `0026` for why an observed association without it licenses nothing.

## Downstream

Nothing in M09 depends on this page, which is why it can carry the practice. M11's capstone reports an experiment and assumes it.

## Boundaries: what this page must not teach

- **Not a new test.** `0167` derived it. This page decides how much data to collect and when to look.
- **Not causal inference.** Randomisation is what licenses the causal claim here; observational adjustment is a different course and gets one sentence.
- **Not a platform tutorial.** No vendor, no SDK.
- Do not present sequential testing as solved. Give the shape of a boundary and say plainly that the exact spending function belongs to a sequential-design reference.

## Beats, in order

1. Randomisation first, because it is the only thing on the page that buys the causal claim. Everything after it is measurement.
2. The OEC and guardrail metrics: decide what "better" means before you look, or `0168`'s multiplicity arrives through the back door as forty metrics on a dashboard.
3. **Power before the experiment.** The sample-size formula, and the observation that `delta` is squared in the denominator, so halving the effect you want to detect costs four times the traffic.
4. Work the number that stops people arguing: a 1 per cent relative lift on a 5 per cent baseline is a 0.05 percentage point absolute effect and needs millions per arm. That is a budget fact before it is a statistics fact.
5. **Peeking**, and this is the page's sharpest beat. A fixed-horizon p-value is valid for one look at a pre-committed `n`. Monitoring daily and stopping when it goes green is a different procedure with a much larger false-positive rate. Measure the inflation rather than warning about it.
6. The fix: a sequential boundary spends `alpha` across the looks instead of at each one, so stopping early has to clear a much higher bar. Show the boundary's shape.
7. Sample-ratio mismatch as the cheapest data-quality check there is: if the arms do not carry the same mix, something upstream is broken and the readout is not yet worth reading.
8. **The base rate.** Most ideas fail. Published programmes report roughly a third of tested ideas improving their target metric, and less in well-optimised surfaces. Plan a portfolio of mostly-null results, and treat a spectacular effect from a tiny change as an alarm before treating it as a discovery.

## Named theorem and its stated proof (D4)

**Theorem (sample size for a two-proportion test).** To detect `delta = p_B - p_A` at two-sided significance `alpha` and power `1 - beta`, the required size per arm is approximately

  `n = ( z_{alpha/2} sqrt(2 p_bar (1 - p_bar)) + z_beta sqrt(p_A(1-p_A) + p_B(1-p_B)) )^2 / delta^2`,  `p_bar = (p_A + p_B)/2`.

**Proof.** Under `H0` the difference is centred at 0 with standard error `se_0 = sqrt(2 p_bar(1-p_bar)/n)`; under `H1` it is centred at `delta` with `se_1 = sqrt((p_A(1-p_A) + p_B(1-p_B))/n)`. Rejection requires the observed difference to exceed `z_{alpha/2} se_0`. Requiring that to happen with probability `1 - beta` under `H1` places the rejection boundary `z_beta` standard errors below `delta`, giving `delta = z_{alpha/2} se_0 + z_beta se_1`. Both standard errors carry a factor `1/sqrt(n)`, so substituting and solving for `n` gives the expression. []

**The honest boundary.** This is the normal approximation again and it inherits `0167`'s limits. It also ignores the second tail, which is why the formula is stated as approximate: the exact power includes a term for rejecting in the wrong direction, negligible at any `delta` worth detecting. And it assumes one look at the end, which is exactly the assumption beat 5 breaks.

## Figures

- **Orientation**, `sequenceDiagram`: user, assignment service, variant, metrics pipeline, analyst, with the randomisation message highlighted and annotated as the step that licenses the causal claim.
- **`svg.chart`**, required: required sample size per arm against detectable relative lift, log-scaled, with the 1-per-cent point annotated in millions. Kills: "a small effect needs a slightly bigger sample".
- **`svg.chart`**: a running p-value across fourteen days of a simulated null experiment, dipping below 0.05 and coming back, with the sequential boundary drawn over it. Kills: "it went significant on Tuesday".
- **`svg.chart`**: two bars, the false-positive rate under one look at the end against the rate under stop-when-green, 5.2 per cent against 21.9 per cent.

## Worked example

`experiment.csv`, which is under-powered on purpose. True rates 0.0500 and 0.0560, a real 12 per cent relative lift; at 12,000 per arm the power is 0.546 and 21,885 per arm would be needed for 0.80. The realisation duly misses: `596/12,000` against `643/12,000`, `z = 1.371`, `p = 0.1703`. Three things are true at once and the page says all three: the effect is real, the test failed to find it, and the 95 per cent interval on the difference, `[-0.168, +0.952]` percentage points, still covers the true `+0.600`. The failure was computable before a single user was assigned.

Then the peeking simulation: 4,000 null experiments over fourteen days, one look at the end giving a 5.2 per cent false-positive rate and daily stop-when-green giving 21.9 per cent.

## Quiz seeds

1. **Misconception.** You check the dashboard every morning and stop when `p` drops below 0.05. What is wrong? Answer: the false-positive rate is inflated. Distractors must include "the effect size is too small" and "the sample is not randomised", both real risks that are not what the stopping rule broke.
2. **Mechanism.** Roughly what fraction of tested ideas improve their target metric in published programmes? Answer: about one third. Distractors at four fifths and nineteen in twenty are the intuition the number exists to correct.

## Practice seed

**Stem.** A page converts at 5.0 per cent and you want to detect a 1 per cent relative lift. State the absolute effect, use `n ~ 16 p(1-p)/delta^2` for 80 per cent power at `alpha = 0.05` to get the size per arm, and at 50,000 visitors a day split evenly, say how long the test must run. Then: you get a significant result on day 2. What do you do?
**Hint.** A 1 per cent *relative* lift on a 5 per cent baseline is not a 1 percentage point change.
**Solution path.** `delta = 0.0005`; `n = 16 x 0.05 x 0.95 / 0.0005^2 = 0.76/2.5e-7 = 3,040,000` per arm; at 25,000 per arm per day that is about 122 days. On day 2 you do nothing: the horizon was 122 days and day 2 is a peek.
**`.p-check`.** If your sample size came out in the thousands rather than the millions, `delta` was taken as 0.01 instead of 0.0005. The squared denominator is what makes the difference a factor of 400.

## Code and dataset

`code/0169-ab-testing.py` against `datasets/experiment.csv`, already on main from #57. It prints the power table, the required sizes, the peeking simulation and a sequential boundary whose shape is right and whose exact spending function the docstring explicitly disclaims. Reference it; do not rewrite it.

## Sources

- Kohavi, Deng, Frasca, Walker, Xu and Pohlmann (2013), "Online Controlled Experiments at Large Scale", KDD, for the base rate, Twyman's law and the sequential-boundary practice.
- Johari, Pekelis and Walsh, "Always Valid Inference: Bringing Sequential Analysis to A/B Testing", arXiv:1512.04922, abstract only, for the statement that continuous monitoring invalidates fixed-horizon inference.
