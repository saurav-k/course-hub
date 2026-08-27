# 0002 - Finishing an arithmetic the lecture leaves open

**Date:** 2026-08-27
**Status:** Accepted
**Applies to:** `lessons/0049-the-negative-result-left-unfinished.html`

## Context

Lecture 4 works one medical-test example end to end.
It states a prevalence of `P(D) = 0.01`, a sensitivity of `P(+ | D) = 0.99` and a specificity of `P(- | D^c) = 0.95`, computes the probability of a positive test by total probability, and applies Bayes rule to reach a stated result of `P(D | +) ~ 0.17`.

Immediately after that, the notes write one further identity, aimed at the other test result:

```
P(D) = P(D and +) + P(D and -)
     = P(+) P(D | +) + P(-) P(D | -)
```

and then stop.
`P(D | -)` is never evaluated.
There is no figure for it anywhere on the board, so there is nothing to quote.

Every other number the page needs is already fixed by the lecture's own stated figures:

- `P(+) = 0.01 x 0.99 + 0.99 x 0.05 = 0.0594`, so `P(-) = 0.9406`.
- `P(D and -) = P(D) x P(- | D) = 0.01 x 0.01 = 0.0001`.
- Therefore `P(D | -) = 0.0001 / 0.9406 = 1 / 9,406`, about `0.000106`.

## The tension

Three rules in this repository pull in different directions here.

`MISSION.md` says every calculation is worked in full and the learner should never have to reconstruct a missing step.
`BUILDER-SPEC.md` rule 2 says every number matches the source deck exactly and a stated figure is quoted with `.keynum`.
`AGENTS.md` says where the lecture is loose, say so, rather than smoothing it over.

Working the number out satisfies the first rule and appears to violate the second.
Leaving it out satisfies the second and abandons the first.
Neither reading is available without a decision, because rule 2 assumes a deck figure exists to be matched, and here none does.

## Decision

Do all three, in this order, on the page:

1. **Show the identity exactly as the notes leave it**, with no number attached, and say in a `.callout.warn` that the lecture stops here and that no key figure exists to quote.
2. **Explain why an unfinished line is normal**, so the reader does not read the gap as an error by the lecturer. The identity is the teaching point; the division is bookkeeping.
3. **Finish the arithmetic in a separate `.callout.key` headed "This course's derivation"**, and work it by two independent routes - straight off the ten-thousand-person table, and by isolating the unknown in the lecture's own identity - so the unstated result is checked against something.

Nothing derived here is marked with `.keynum`.
That span means "the lecture said this", and on this page the lecture said only the identity.

## Why this and not something else

- **Not "print 0.000106 like any other result".** A reader who later opens the class notes would find a figure that is not in them and would have no way to tell which of this course's numbers are the lecturer's. That erodes every `.keynum` on every other page.
- **Not "leave the identity unevaluated, as the lecture does".** The mission is that the reader never has to reconstruct a missing step. Worse, the negative result is the more useful half of this example in practice: a negative divides the risk by 94.06, and a course that works the alarm and drops the all-clear teaches half of the base-rate lesson.
- **Not "raise it and stop".** There is no ambiguity to escalate. Every input is stated and the arithmetic has one answer; the only question was whose name goes on it.
- **Not "put it in a footnote".** The two routes and their agreement are the content. A footnote would present the answer without the check that makes it safe to publish.

## Difference from learning record 0001

Record 0001 handles a deck that **states a figure its own table does not reproduce**, and the decision there is to print both and name the disagreement.
This record handles a deck that **states no figure at all**, and the decision is to derive one and label the derivation.
The shared rule under both is the same: the reader must always be able to tell what the lecture said from what this course worked out.

## Cost of this decision

Part 4 carries two callouts and a longer section 4 than a smoother page would.
The trade is accepted for the same reason as in record 0001: noticing that a source stopped, and saying so out loud before continuing, is the habit this course exists to install.

## Revisit when

A later session of the source course evaluates `P(D | -)` for this example, or a corrected set of notes appears.
If the lecturer's own figure ever lands, quote it with `.keynum`, keep this course's derivation only if it still adds the two-route check, and update the callout wording so the page no longer claims the lecture is silent.
