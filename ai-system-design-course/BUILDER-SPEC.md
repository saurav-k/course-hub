# Builder Spec - read this before writing or editing any chapter

This course is organised as **chapters, not micro-lessons**. Each chapter covers one pillar and every topic inside it. That is deliberate: the learner asked for full-pillar coverage so a chapter doubles as a revision index the night before an interview.

Read `MISSION.md` and `NOTES.md` first. Read `lessons/0000-llm-basics.html` in full as the gold template before writing anything.

## Hard rules

1. **No em dashes anywhere.** Use a plain `-`.
2. **Every topic is its own `<h3>` with an `id`,** matching the anchor the glossary links to. Breaking an anchor breaks the glossary.
3. **Every topic carries a linked primary source** - a paper, a specification, or vendor documentation - written as `<em>Source: <a href="...">...</a>.</em>`. Never cite a blog summarising a paper when the paper is available.
4. **Never invent numbers.** If a figure is not in a source you can link, describe the effect qualitatively. Cost figures in particular must be framed as assumptions, not facts.
5. **Concept-only.** The learner is a Principal engineer with twelve years of distributed-systems experience. Do not re-teach queues, caches, or replication. Teach what is different.
6. **Interview framing.** Every chapter ends with an `Interview drill` section: the questions actually asked, each with the trap named.
7. Self-contained HTML with the same `<head>`, spine nav, and `../assets/course.js` at the end of body.

## Required section skeleton

1. `.eyebrow` = `Pillar NN &middot; <Pillar Name> &middot; Chapter N`
2. `<h1>` = chapter title, `.paper-meta` = topic-count pill plus a one-line framing.
3. `.card.tldr` = "The one-minute version", 4 bullets.
4. A mental-model section with the first Mermaid diagram.
5. Topic sections, each an `<h3 id="...">` plus one or two paragraphs.
6. At least two Mermaid diagrams per chapter in `<figure class="diagram">`, each with a `<figcaption>` that explains it in plain English and bolds the takeaway.
7. At least two quizzes using `<div class="q" data-answer="N">`.
8. `Interview drill` list.
9. `.teacher-note`, then `Primary source to go deeper`, then `.pager`, then footer.

## Quizzes

Use the widget documented in `assets/course.js`. **Every option must be the same length in words and as close as possible in characters.** A visibly longer correct answer leaks the answer and destroys the retrieval practice, which is the entire point.

Feedback in `.q-fb` must explain why the wrong answers are wrong, not merely restate the right one.

## Adding a topic

Add the `<h3 id="...">` to the correct chapter, then add a matching row to `reference/glossary.html` linking to that anchor, then update the topic-count pill in the chapter and in `index.html`. The site validator will not catch a missing glossary row, so this is on you.
