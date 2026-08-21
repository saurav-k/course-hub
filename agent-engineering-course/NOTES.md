# Notes

## Learner profile

- Principal engineer, twelve years, strong distributed systems background.
- Target: building and operating agent systems at Staff+ level.
- Already fluent in databases, caches, queues, sharding, replication, backpressure, circuit breakers, and idempotency. Do not re-teach these.
- The most effective teaching move for this learner is to name the distributed-systems concept the agent problem is isomorphic to, then say precisely where the isomorphism breaks.

## Teaching preferences

- Concept-only. No slow-walking of fundamentals and no code walkthroughs.
- Mental model first, then the mechanism, then the trade-off, then the failure mode.
- Every technical claim carries a citation. Parametric memory is not a source.
- Plain dash, never an em dash, in all content.
- Quiz options must match in length so formatting never leaks the answer.
- Say what a technique costs, not only what it buys. A chapter that only lists benefits has not been written yet.

## Structure decisions

- Chapters, not micro-lessons, matching the sibling interview course so the two read as one library.
- Each topic gets its own anchored subsection with a linked primary source, so a chapter also works as a reference index during a design review.
- Each chapter ends with a field drill: the questions a reviewer asks about a system you are going to run, and the trap in each.
- Chapters are deliberately uneven in topic count, from three to four. The pillar boundary is the honest one; padding a chapter to make the counts match would be worse.

## Cross-linking with the interview track

Cross-links go to `../ai-system-design-course/lessons/NNNN-*.html#anchor` and land on a real anchor.
Link where the two tracks genuinely touch and the other page adds something: prompt caching, latency budgets, semantic caching, golden datasets, A/B testing, async processing, circuit breakers, citation grounding, prompt injection.
Do not cross-link for completeness. A link that only says "this exists elsewhere too" costs the reader a click and returns nothing.

## Known gotchas while authoring

- Mermaid parses everything after the first colon in a sequence-diagram message as text, so extra colons are safe, but bracketed shapes in a flowchart need quoted labels when they contain punctuation.
- The site validator strips fragments before checking a link, so a glossary row pointing at a missing anchor passes validation and breaks silently. Check anchors by hand against the `id` attributes in the target file.
- The 30 percent semantic-caching saving that circulates in agent-engineering source lists has no primary source behind it. Frame savings as hit rate times avoided call cost and tell the reader what moves the hit rate.

## Open threads

- Chapter 3 wants a fourth topic on human-in-the-loop approval as a first-class workflow state. It is currently a paragraph inside inter-agent security and a sentence inside degradation, which is one topic pretending to be two footnotes.
- No learning records beyond the first. Add one once the learner builds against a chapter and reports what the chapter got wrong.
- A worked cost model, as a print-friendly reference sheet, would pair well with Chapter 4 once someone has run the arithmetic on a real workload.
