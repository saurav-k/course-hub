# Notes & Preferences

## Teaching preferences (from user)
- **Level**: total beginner to LLM internals -> Lesson 0 primer added before Attention.
- **Depth**: deep implementation. Concept + diagrams first, then full runnable code, training loops, benchmarks/ablations where they fit.
- **Cadence**: build all 38 lessons up front (publishable course), not one-at-a-time.
- **Diagrams**: LOTS. Every lesson must be diagram-heavy. Mermaid (block/sequence/flow/state) + hand SVG.
- **Everything grammatically explainable**: plain-English narration of every mechanism and every equation. No bare math.
- **No em dashes** anywhere (global user rule). Use `-`.

## Build architecture
- Shared design system: `assets/course.css` (Tufte-ish, print-friendly, dark/light).
- Shared JS: `assets/course.js` (mermaid init + quiz widget + code copy).
- One `index.html` = course home with the ranked 38-lesson syllabus (10 modules).
- Each lesson = `lessons/NNNN-slug.html`, links back to index, glossary, prev/next.
- Glossary reference at `reference/glossary.html` — canonical terms, adhered to everywhere.

## Lesson template (every lesson follows this)
1. Header: module, lesson #, paper title + year + authors + arXiv link.
2. TL;DR card (3-4 bullets).
3. "Why this paper exists" (the problem it solves).
4. Mechanism — diagram-first, then plain-English walkthrough.
5. The math, explained in words line by line.
6. Implementation — runnable code (PyTorch/Python), training loop / benchmark / ablation where relevant.
7. Retrieval quiz (equal-length answers, no formatting tells).
8. "How it connects" — lineage links to other lessons.
9. Primary source + "ask your teacher" reminder.

## Open follow-ups
- Consider a Module 0 math refresher card (linear algebra / softmax) if primer proves too dense.
