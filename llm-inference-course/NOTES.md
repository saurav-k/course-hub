# Notes

How this course teaches, and what an author needs to know before adding to it.
Read `MISSION.md` first for why it exists, then [`PLOT.md`](PLOT.md) for the reading order.

## Learner profile

An engineer who lives in a terminal.
They will paste the lab commands before they read the prose, so the commands have to be right, complete, and in runnable order.
They are comfortable with Docker, Python, and basic cloud, and they are new to inference specifically - Lesson 0 exists because prefill/decode and TTFT/TPOT were not vocabulary they carried.

## Cadence

Every lesson follows the same skeleton, which is also the contract a new lesson is held to:

1. The one-minute version - three or four bullets.
2. Why this matters.
3. Mechanism sections, diagram-first, numbered.
4. **The lab**: simulate or serve, measure, and compare against the claim the mechanism made.
5. A comparison or judgement section where the lesson has a real fork in it.
6. Check yourself - retrieval quiz with matched option lengths.
7. Your checklist for this lesson.
8. Primary source to go deeper.

The lab is the lesson's centre of gravity; the prose exists to make the measurements legible.

## Teaching preferences

- Every abstraction is introduced by measuring it, not by defining it. Show static batching losing money before naming why continuous batching fixes it.
- Diagrams explain the mechanism; the lab proves it. Both, in that order.
- Benchmarks are recorded honestly: hardware named, numbers labelled as one run on one machine. The capstone makes "publish your numbers and say what they cost" the final exercise for exactly this reason.
- Plain dash, never an em dash.

## Structure decisions

- Linear, single route, top to bottom. Serving stacks build on each other: batching before KV eviction, engines before routing, routing before economics.
- One lesson per technique rather than a survey chapter, because the reader is going to run each one.
- No difficulty ladder beyond the pills on the map. A hands-on course orders by dependency, not by hardness.

## Known gotchas

No course-specific renderer gotchas recorded yet; the hub-wide ones live in the root `AGENTS.md` and apply here as everywhere.
Add one below the first time a lab breaks for you in a way the next author would not expect.

Two authoring cautions that come from the shape of the material rather than from breakage:

- Lab output varies by hardware and by model version. Never present one machine's numbers as the expected result; present them as *a* result and say what moved them.
- Version-sensitive commands age fastest of anything in this hub. When a flag changes between versions, name both rather than quietly updating the command.

## Open threads

- No learning records yet. Add one when a learner has run the labs and can report which lesson lied to them about their own hardware.
- No central `RESOURCES.md`. Each lesson carries its own primary source link; if the citation list grows unwieldy, that is the moment to spin one up, not before.
- No `BUILDER-SPEC.md`, by decision recorded in `MISSION.md`.
