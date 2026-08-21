# Builder Spec - read this before writing any chapter

This course is the **practitioner reference** for production systems engineering: 111 topics across 11 chapters. Chapters are written in parallel by different authors, so this spec is the contract that keeps them one course rather than eleven.

Read `../ai-system-design-course/lessons/0000-llm-basics.html` in full as the structural template. Copy its skeleton. Change the content.

## Hard rules

1. **No em dashes anywhere.** Use a plain `-`. This is checked.
2. **Every topic is its own `<h3 id="...">`** with a kebab-case id. Anchors are linked from the glossary and from other chapters; breaking one breaks both.
3. **Every topic carries a linked primary source** - an RFC, a specification, a paper, or first-party vendor documentation. Format: `<em>Source: <a href="...">Name</a>.</em>` Never cite a blog summarising a primary source that exists. **Fetch every URL before citing it.**
4. **Never invent numbers.** No fabricated benchmarks or vendor figures. Numbers you derive yourself from stated assumptions are encouraged - show the arithmetic and label the assumptions. Numbers you attribute to someone else must be in the linked source.
5. Full normal prose. Complete sentences. Concept-first, no framework tutorials.

## The required shape of every topic

Each topic must answer four questions, in this order. This is what makes the course useful rather than a glossary.

1. **What it is and the mechanism.** The mental model first, then how it actually works.
2. **A named real-world example.** A concrete system that uses it and what would break without it. Name the industry: payments, streaming, ride-hailing, e-commerce, healthcare, ad tech, gaming, logistics. Prefer publicly documented architectures you can cite.
3. **The three scale tiers.** How the decision changes at **100 requests per second**, **1,000 requests per second**, and **10,000 requests per second**. This is the spine of the course. What is unnecessary at 100 is mandatory at 10,000, and something that works at 100 often collapses at 1,000. Say which.
4. **The trade-off and the failure mode.** What it costs, and how it fails when it fails.

Where the topic has arithmetic, show it. Capacity, queue depth, connection counts, cache hit economics, replication lag budgets, error budget minutes. Put equations in `<div class="math">...<span class="gloss">plain-English reading of every symbol</span></div>` and work at least one number through end to end.

## Diagrams

**Minimum 4 Mermaid diagrams per chapter, and aim for 6 to 8.** A chapter of ten topics with two diagrams has failed this spec. Mix the types:

- `flowchart` for block and component diagrams
- `sequenceDiagram` for request flows, retries, handshakes, and failure paths
- `stateDiagram-v2` for lifecycle and state machines

Every diagram goes in `<figure class="diagram"><div class="mermaid">...</div><figcaption>...</figcaption></figure>`. The figcaption explains the diagram in plain grammatical English and **bolds the key takeaway**. A diagram with no figcaption is incomplete.

## Cross-linking

Link to sibling chapters with relative links, for example `<a href="0001-resilience-patterns.html#circuit-breakers">circuit breakers</a>`. Link to the two sibling courses where they genuinely touch: `../../ai-system-design-course/lessons/0003-cost-and-performance.html` and `../../agent-engineering-course/lessons/0003-latency-cost-and-local-first.html`. Only link anchors you have confirmed exist.

## Required section skeleton

1. `.eyebrow` = `Chapter NN &middot; <Chapter Name>`
2. `<h1>` = chapter title. `.paper-meta` = topic-count pill plus a one-line framing.
3. `.card.tldr` = "The one-minute version", 4 bullets.
4. An opening section with the first diagram, framing what the chapter is about.
5. The topic sections, each an `<h3 id="...">` following the four-question shape above.
6. At least **3 quizzes** using `<div class="q" data-answer="N">`.
7. A `Scale drill` section: for a named system, walk what changes across the three tiers.
8. `.teacher-note`, then `Primary source to go deeper`, then `.pager`, then footer.

## Quizzes

Use the widget documented in the hub runtime, `assets/hub.js`. **Every option must be the same length in words and near-identical in characters** so formatting never leaks the answer. Feedback must explain why each wrong option is wrong, not merely restate the right one.

## Head, nav, and footer

Copy them verbatim from the template, changing only the title and the pager targets:

- in `<head>`, in this order: `<link rel="stylesheet" href="../../assets/hub.css">`, the mermaid
  CDN script, `<script src="../../assets/hub.js"></script>`, `<script src="../outline.js"></script>`.
  `hub.js` carries no `defer` and no `async`; that is what stops the flash of the wrong palette.
- the `.spine` nav with `PRODUCTION SYSTEMS` as the home label
- nothing at the end of `<body>`. The runtime loads from the head and mounts the rail, the
  appearance control and the reading progress bar itself.
