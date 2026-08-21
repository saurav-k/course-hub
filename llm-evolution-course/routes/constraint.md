# Route scope: By binding constraint

**Route id:** `constraint`
**Sections:** 7
**Pages:** 47 deep dives
**Status:** the default route

## What this route is

Seven eras, each named for the one thing that was holding the field back at the time.
Rules, then meaning, then reach, then scale, then usefulness, then cost, then thinking.

Every section opens with the problem in its own words and closes with what solved it.
That framing is the whole value of the route: it answers *why did anyone do this* rather than *what happened next*.

| Section | The binding constraint | What closed it |
|---|---|---|
| 01 Rules | Everything a machine knew about language had to be written by a person | Counting |
| 02 Meaning | Counted symbols carry no similarity, and most sequences are never seen | Learned vectors |
| 03 Reach | A model could not connect what it read to what it needed, and the fix was too slow | Attention, then attention without recurrence |
| 04 Scale | Nobody knew how big to build or what to feed it | Scaling laws, and the correction |
| 05 Usefulness | Models were capable and useless, and unreachable | Instruction tuning, human comparisons, a free text box |
| 06 Cost | Frontier capability cost more than anyone could pay | Open weights, adapters, sparsity, serving engineering |
| 07 Thinking | One forward pass was all the thought a question got | Not yet closed |

## Why it is the default

It is the framing that makes the most lessons feel inevitable rather than arbitrary, and it is the one a reader can hold in their head after finishing.
Seven words is a course-sized amount of structure.

Being the default has one mechanical consequence: a lesson's canonical URL, with no `route` parameter, is read in this route, and every committed pager and breadcrumb on a deep dive follows this route's order.
Changing the default therefore means regenerating every deep dive's pager, and the validator will tell you so.

## What it deliberately leaves out

- **The ten spine chapters.** They are a low-resolution pass over the same story, so putting them here would say the same thing twice in one reading. A reader who wants the short version takes the `spine` route.
- **Strict chronology.** The sections are roughly chronological because constraints were, but within a section the order is causal. A reader who wants dates in order takes the `era` route.
- **Any claim that a constraint was the only one.** More than one thing is always binding. The claim this route makes is about which one, once relieved, unblocked the most.
- **A verdict on section 07.** Thinking is presented as the constraint currently being worked on, not one that has been closed.

## Who it is for

Someone who wants to understand causation and will be answering questions about *why*.
It is the best route for a reader who intends to explain this to somebody else.

It is a poor first route for someone who wants a quick orientation, and a poor route for looking something up.

## How to extend it

When a lesson is added, place it in the section whose constraint it belongs to, not the section whose dates it belongs to.
Ask: what was impossible before this, and what became possible after it.
If the answer does not match any of the seven, that is worth noticing before you add an eighth.

**An eighth section is a real editorial event and should be argued for, not slipped in.**
The constraint after thinking is not yet visible, and the last lesson in the pool is a register of open questions rather than a prediction about it.
When it does become visible, the section header carries a problem statement and a "what closed it" line like every other, and lesson 0057 retires the corresponding open question with its answer and date.

Do not let this route accumulate lessons that are only about people or money.
It has exactly one of those, on the institutional layer of 2014 to 2017, and it earns its place because the later corporate decisions are unreadable without it.
