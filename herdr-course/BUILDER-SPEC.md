# BUILDER-SPEC - Herdr from Zero

The course delta only. The house standard is
[`.claude/skills/course-authoring/SKILL.md`](../.claude/skills/course-authoring/SKILL.md)
and it wins wherever this file is silent or behind.

## What differs from the house standard

- **No `assets/` folder and no course-extras sheet.** Every widget on these pages comes
  from the shared vocabulary in `references/widgets.md`; the course owns only its hue
  line in `assets/hub.css`.
- **No reference sheets yet.** A glossary is planned (see `PLOT.md`) but unwritten, so
  lesson footers carry no glossary link yet. Add one to every footer when the sheet
  lands.
- **No practice-problem sections.** The retrieval bar here is two quizzes per lesson;
  the course does not opt into the extended practice/chart floors in
  `check_pages.py`'s `EXTENDED_BAR_COURSES`. Lessons are short and hands-on by design,
  and Lesson 11's worked build is the closest thing to a lab.
- **Version pinning in citations.** Claims cite the Herdr repository at 0.8.2-era
  master with file-and-line references. When updating a lesson against a newer Herdr,
  re-verify the cited lines still say what the page claims and update the version note
  in `RESOURCES.md`.

## Conventions specific to this course

- Course name in chrome: **HERDR FROM ZERO**; footer prefix "Herdr from Zero".
- The three metaphors in `NOTES.md` are load-bearing vocabulary: reuse them, do not
  invent synonyms.
- Plugin-track lessons (09-13) may assume Lessons 01-08; nothing else may assume
  anything not taught in an earlier numbered lesson.
