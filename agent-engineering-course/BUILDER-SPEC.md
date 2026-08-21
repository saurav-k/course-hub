# Builder Spec - read this before writing or editing any chapter

This course is organised as **chapters, not micro-lessons**, matching its sibling [`ai-system-design-course`](../ai-system-design-course/BUILDER-SPEC.md) so the two read as one library.
Each chapter covers one pillar and every topic inside it, so a chapter doubles as a reference index during a design review.

This is the **build track**. The sibling is the **interview track**.
The difference is the question each one answers: the interview track asks what you would say at a whiteboard, this one asks what you would put in a repository and what pages you when it is wrong.

Read `MISSION.md` and `NOTES.md` first.
Read `../ai-system-design-course/lessons/0000-llm-basics.html` in full as the gold template before writing anything, then read a chapter of this course to see where the two diverge.

## Hard rules

1. **No em dashes anywhere.** Use a plain `-`.
2. **Every topic is its own `<h3>` with an `id`,** matching the anchor the glossary links to. Breaking an anchor breaks the glossary, and the site validator will not catch it because it strips fragments before checking a link.
3. **Every topic carries a linked primary source** - a paper, a specification, or vendor documentation - written as `<em>Source: <a href="...">...</a>.</em>`. Never cite a blog summarising a specification when the specification is available. Fetch the URL and read it before you cite it.
4. **Never invent numbers.** If a figure is not in a source you can link, describe the effect qualitatively and tell the reader what determines it. Cost and saving figures in particular are decomposed into their factors, never asserted.
5. **Concept-only.** The learner is a Principal engineer with twelve years of distributed-systems experience. Do not re-teach queues, caches, replication, idempotency, or circuit breakers. Name the isomorphism and then say where it breaks.
6. **Say what it costs.** Every technique gets its trade-off named in the same subsection that introduces it. A subsection that only lists benefits is not finished.
7. **Field framing.** Every chapter ends with a `Field drill` section: the questions a Staff+ reviewer asks about a system you are going to run, each with the trap named.
8. Self-contained HTML with the same `<head>` block as the neighbouring chapters and the same spine nav, and nothing at the end of body. The design system is the hub's shared `assets/hub.css` and `assets/hub.js`, linked from `<head>`; this course adds no stylesheet of its own and must not fork one.

## Required section skeleton

1. `.eyebrow` = `Pillar NN &middot; <Pillar Name> &middot; Chapter N`
2. `<h1>` = chapter title, `.paper-meta` = topic-count pill plus a one-line framing.
3. `.card.tldr` = "The one-minute version", 4 bullets.
4. A mental-model section that names the distributed-systems concept the chapter is isomorphic to, carrying the first Mermaid diagram.
5. Topic sections, each an `<h3 id="...">` plus two or three paragraphs.
6. At least two Mermaid diagrams per chapter in `<figure class="diagram">`, each with a `<figcaption>` that explains it in plain English and bolds the takeaway.
7. At least two quizzes using `<div class="q" data-answer="N">`.
8. `Field drill` list.
9. `.teacher-note`, then `Primary source to go deeper`, then `.pager`, then footer.

Use `.callout.warn` for "the failure you will actually hit" boxes.
Reserve them for a failure that is silent, expensive, or both, at most one per chapter.

## Quizzes

Use the widget documented in the header of the hub's `assets/hub.js`.
**Every option must be the same length in words and as close as possible in characters**, ideally within about five characters across the four.
A visibly longer correct answer leaks the answer and destroys the retrieval practice, which is the entire point.

Vary which index is correct across a chapter.
Feedback in `.q-fb` must explain why each wrong answer is wrong, not merely restate the right one.
The strongest distractors are true statements that answer a different question.

## Cross-linking the interview track

Link to `../ai-system-design-course/lessons/NNNN-*.html#anchor` where the tracks genuinely touch and the other page adds something.
Verify the anchor exists in the target file before committing; the validator strips fragments and will not catch a dead one.
Do not cross-link for completeness.

## Adding a topic

Add the `<h3 id="...">` to the correct chapter, then add a matching row to `reference/glossary.html` linking to that anchor, then update the topic-count pill in the chapter, in `reference/glossary.html`, and in `index.html`.
Add the new source to `RESOURCES.md` under the right heading.
If the topic has no citable primary source, add it to the `## Gaps` section instead of citing something weaker.
