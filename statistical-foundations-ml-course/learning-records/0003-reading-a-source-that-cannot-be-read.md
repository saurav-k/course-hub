# 0003 - Reading a source that cannot be read

**Date:** 2026-08-30
**Status:** Accepted
**Applies to:** `lessons/0061-the-quality-check-that-finds-nothing.html`, `lessons/0065-count-the-configurations.html`

## Context

Lecture 5 has two sources.
One is the lecturer's typeset examples handout, which states three problems and their official solutions.
The other is five pages of the captain's handwritten class notes for the same session, which carry material the handout does not: the general binomial, the sample-space sketch that limits counting, a conditional question, and a small enumeration.

Handwriting does not always resolve.
Two marks on those five pages will not, and they fail in two different ways.

**The first** sits beside the line for `Pr(X = 0)` in the dataset quality check.
The solution there is `C(950,20) / C(1000,20)`.
Next to it, with an arrow pointing at it and no surrounding words, is a second binomial coefficient that reads as `C(50,20)`.
Two readings are plausible.
It may be the opposite extreme, all twenty inspected images drawn from the fifty mislabelled ones, jotted as a contrast to the answer.
It may be a slip of the pen for the `C(950,20)` immediately above it.
Nothing on the page settles which.

**The second** is the last row of the four-image enumeration.
The board lists the configurations of four results holding exactly two errors, and five of the six rows are legible: `CCEE`, `ECCE`, `EECC`, `ECEC`, `CECE`.
The sixth row's first letter is overwritten and will not resolve into a `C` or an `E`.

## The tension

`AGENTS.md` says to teach the ideas in this course's own prose and never to invent a step to fill a gap.
`MISSION.md` says the learner must never have to reconstruct a missing step.
`BUILDER-SPEC.md` rule 9 says that where the lecture is loose, say so in a `.callout.warn`.

A page that silently picks one reading of the ink satisfies the second rule and breaks the first.
A page that omits the material satisfies the first and breaks the second.

## Decision

Treat the two cases differently, because they are different.

**Where the ink is ambiguous and the mathematics does not settle it**, name both readings on the page in a `.callout.warn`, state which one the published solution uses, and build on neither.
That is the `C(50,20)` mark on page 0061.
The handout's own solution uses `C(950,20)` and nothing else, so the page loses nothing by declining to guess.

**Where the ink is ambiguous but the mathematics settles it**, say the ink is unreadable, then derive the missing item and show the derivation.
That is the sixth configuration on page 0065.
Exactly two of four positions must hold an error, there are `C(4,2) = 6` such strings, and the five legible rows account for five of them, so the sixth is forced to be `CEEC`.
The page says all of that out loud, and notes that the argument does not depend on the reading either way, because what the formula consumes is the count of six and the count is forced.

## Why this and not something else

- **Not "pick the likelier reading and move on".** A reader who later sees the notes would find a page asserting something the notes do not, with no way to tell which of this course's readings were transcriptions and which were guesses. That is the same erosion `learning-record 0001` protects against for figures.
- **Not "omit both".** The four-image enumeration is the bridge from counting to the binomial and the whole page turns on the list being complete. Dropping a row would leave a list of five that visibly does not match its own count of six.
- **Not "derive both".** The mathematics forces the sixth configuration and does not force the stray coefficient. Deriving something the mathematics does not force is inventing a step, which is the thing being avoided.
- **Not "ask the captain".** Worth doing eventually, and it would resolve the first case. It does not change what the published page should say in the meantime, and neither case blocks the lecture.

## Difference from the earlier records

Record 0001 handles a source that **states a figure its own table does not reproduce**: print both and name the disagreement.
Record 0002 handles a source that **states no figure at all**: derive one, label the derivation, and check it by a second route.
This record handles a source that **cannot be read**: name the ambiguity, and derive only what the mathematics forces.

The shared rule under all three is unchanged: the reader must always be able to tell what the lecture said from what this course worked out.

## Cost of this decision

Two extra callouts, on two pages that already carry a good deal of honesty apparatus.
Lecture 5 is unusually heavy in that respect, because almost nothing in it is evaluated to a number and every decimal on ten pages is this course's own.

## Revisit when

The captain confirms what the `C(50,20)` mark was for, or a cleaner scan of page 2 of the notes appears.
If it turns out to be the opposite-extreme contrast, page 0061 can teach it as such and the callout becomes a sentence.
If it turns out to be a slip, the callout goes and nothing else on the page changes.
