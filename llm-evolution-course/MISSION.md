# Mission: How Language Models Happened

## Why this course exists

The hub can already explain how a large language model works.
It cannot explain how we got one.

`llm-papers-course` teaches thirty-seven papers at full mechanism depth, ordered easiest to hardest.
That ordering is right for its mission and it means the course structurally cannot double as a history: nineteen percent of its ordered lesson pairs are chronologically inverted, and its coverage before 2017 is zero.
No page anywhere in the hub mentions ELIZA, n-gram language models, word2vec, GloVe, seq2seq or Bahdanau attention.
The product and adoption story of the last three years is close to absent as well.

This course is the missing spine.
It runs from the 1950s to 2026, it starts from nothing, and it is built so that a beginner can finish it able to say, from memory, why each step had to happen.

## What this course owns

| This course | `llm-papers-course` |
|---|---|
| Chronology and causation: what problem was open, and what the previous step made possible | Mechanism: how the thing actually works |
| People, labs, dates, and the decisions behind them | Maths: the equation and its plain-English gloss |
| The pre-2017 era in full | Implementation: a runnable code block per paper |
| The product and adoption story | The per-paper retrieval quiz |
| What is still open, and how to tell a measurement from a claim | The lineage sidebar between adjacent papers |

Two rules keep that boundary honest, and both are repeated in `BUILDER-SPEC.md` because they are the rules that stop the two courses re-converging.

1. **No runnable code and no derivation in this course.**
   At most one intuition-level formula per lesson, in prose.
   The moment a lesson wants to derive something, it links to the papers lesson instead.
2. **Explain a mechanism only to the depth that makes the story's next step feel inevitable, then link.**
   If a reader could not follow the next lesson without the detail, include it.
   Otherwise it belongs in the papers course.

Of the roughly fifty topics this course touches, twenty-six are already taught at full paper depth next door.
Every one of those carries a cross-link rather than a re-derivation.

## The shape: one pool, four routes

The course is a single pool of pages that can be read along four different routes.
Ten of those pages are a short spine that carries the whole arc at low resolution with no maths, readable in an evening.
The other forty-seven are deep dives.

| Route | Sections | What it is for |
|---|---|---|
| `constraint` | 7 | Each section is the era when one thing was the bottleneck: rules, meaning, reach, scale, usefulness, cost, thinking. Every section opens with the problem and closes with what solved it. This is the default. |
| `spine` | 10 | The ten short chapters, each followed by the deep dives that zoom into it. |
| `capability` | 6 | Each section is one thing machines learned to do, in the order they learned it. |
| `era` | 6 | Straight chronology, nothing rearranged to make an argument. |

This shape is also the answer to a real disagreement between the four scout reports this course was built from.
The hub audit recommended twenty-six lessons for the whole story.
The three era scouts recommended thirteen, fourteen and sixteen for their own windows, which is forty-three.
Both were right about different readers.
A spine of ten short chapters is the twenty-six-lesson course; the pool behind it is the forty-three-lesson course; and a reader picks.
Nothing had to be cut, and nothing has to be read.

`routes/README.md` explains the mechanism.
Each route has its own scope document beside it.

## Who it is for

Someone who has heard of all of this and can explain none of it.
No maths beyond arithmetic is assumed anywhere, and no prior course in this hub is a prerequisite.

Specifically, `statistical-foundations-ml-course` is **not** a prerequisite and must never become one.
It covers descriptive statistics and inference for business decisions, which is the right maths for evaluating a model and the wrong maths for understanding one.
Its own mission rules machine learning out of scope.
This course teaches the small amount of maths it needs inline, at the moment the story needs it: vectors and dot products at the word-embedding lesson, loss and gradient descent at the neural network lesson, and the log-log plot at the scaling lesson.

## What "done" looks like

- All fifty-seven pages carry written prose rather than a brief.
- Every lesson names its own starting point before assuming any context, and every backward reference names and links what it refers to.
- Every lesson carries three or four retrieval-practice questions with matched option lengths.
- Every figure is a finished diagram rather than the scaffolded sketch it started as.
- Every claim about the last eighteen months carries a zone badge, an as-of date and one of the four claim labels.
- All four routes still cover what they declare, which `scripts/validate_site.py` checks.

## Out of scope

- **Mechanism, maths and code.** They live next door. This course links to them.
- **Tutorials.** Nothing here is a how-to. `llm-inference-course` and `agent-engineering-course` are the build tracks.
- **Prediction.** The last lesson is a register of open questions, not a forecast. Questions are retired with an answer and a date, never answered speculatively.
- **A leaderboard.** Benchmark numbers appear only as worked examples of how to read a benchmark claim.
- **Renaming or renumbering anything.** Numbers are identity in this course. Routes are order. A lesson that belongs chronologically in the middle still gets the next free number at the end.
