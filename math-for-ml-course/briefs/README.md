# Briefs

One file per planned page. A writer picks up `NNNN-slug.md` and writes `lessons/NNNN-slug.html` from it without needing to ask anything.

## Why a brief is markdown and not a stub page

A planned page has **no file under `lessons/`**, because two rules in this repository make that impossible together:

- `scripts/validate_site.py` requires every `lessons/*.html` to be a registered card in the course `index.html` and to appear in `outline.js`.
- `.claude/skills/course-authoring/references/widgets.md` requires a page that is planned and unwritten to be plain text in a `.roadmap`, **never a link**.

So a stub page would have to be simultaneously registered and unregistered. The brief lives here instead. The deploy excludes `*.md`, the validator ignores this folder, and **no published page ever links a brief** - a local `.md` link fails the validator.

## Writing the brief claims the number

The page number appears in the file name, the `.eyebrow`, the `<footer>` and the `.pager`. Two crews both taking `0034` is the one merge conflict this layout cannot absorb.

**The brief is the register.** If `0034-something.md` exists, that number is taken. Create the brief before you start writing the page, and in the same pull request as any change to the course map's `.roadmap`.

## Which numbers you may use

Page numbers come from **one table**. Blocks are sparse on purpose: the tooling only ever sorts, so a gap costs nothing, while a collision costs a rename across the file name, the `.eyebrow`, the `<footer>` and the `.pager`.

| Module | Block | | Module | Block |
|---|---|---|---|---|
| M01 Foundations | `0001-0019` | | M07 Probability | `0120-0139` |
| M02 Data and summaries | `0020-0039` | | M08 Expectation, limits, simulation | `0140-0159` |
| M03 Vectors, matrices, linear maps | `0040-0059` | | M09 Estimation, testing, inference | `0160-0179` |
| M04 Eigenvalues, SVD, PCA | `0060-0079` | | M10 Information, similarity, dimension | `0180-0199` |
| M05 Calculus for machine learning | `0080-0099` | | M11 Capstone: regression | `0200-0219` |
| M06 Optimization | `0100-0119` | | | |

**Read your row. Do not compute your block.** A mnemonic published beside this table was off by one and sent three crews into the next module's block before anyone noticed, because a rule and a table are two sources of truth and they disagreed silently. The rows are the only source. M01 starts at `0001` rather than `0000` because lesson zero already holds `0000`, which is exactly the kind of exception an arithmetic rule loses.

Fill your block from the bottom upwards in teaching order and leave the headroom at the top, so a page discovered later lands beside its neighbours rather than at the end of the course.

**Reference another module by its module, not by a number, until that module's briefs exist.** Writing "`0016` needs this" while M02 is unwritten is a guess that will be wrong, and it will be wrong silently. Write "M02 needs this" and let the crew that claims the number make it specific.

## Numbering is a topological order

File order is a valid reading order: no page needs a page that comes after it. That is a property to preserve, not a coincidence. If a new page belongs logically in the middle, it takes the next free number at the end and the course map's module grouping carries the teaching order instead, per `AGENTS.md` rule 6.

## What every brief carries

| Section | What it is for |
|---|---|
| **Module, rung, class** | which module, `foundation`/`working`/`frontier`, and `core` or `depth` |
| **One tight idea** | one sentence. If it takes two, it is two pages |
| **Prerequisites** | by page number, all of them earlier |
| **Downstream** | who breaks if this page is wrong |
| **Boundaries** | what this page must NOT teach, and who owns it instead |
| **Beats** | the page in order, one line each |
| **Stated proof** | required by D4 wherever the page names a theorem |
| **Figures** | each named by widget kind, including the orientation figure and at least one `svg.chart` |
| **Worked example** | the setting and the actual numbers |
| **Quiz seeds** | at least two, one testing a misconception |
| **Practice seed** | stem, hint, solution path, and the `.p-check` sanity line |
| **Code and dataset** | which program, which dataset, what it computes twice |
| **Sources** | primary only |
| **Word budget** | prose only; practice and quiz text do not count |

## What a brief is not

It is not a draft of the page. It carries decisions, numbers and sources, not prose. A writer who finds themselves copying sentences out of a brief should stop: the brief was written at the wrong altitude.
