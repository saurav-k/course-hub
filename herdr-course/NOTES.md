# NOTES - Herdr from Zero

How this course teaches, and the gotchas found while porting and authoring it.

## Voice

Big pictures, few words; diagrams carry the meaning. Every lesson opens with an
orientation figure, states its one idea as a claim in the `h1`, and works
mental model, then mechanism, then trade-off. Full prose throughout - no fragments.

## The three metaphors

Introduced once, reused everywhere after:

- **The night watchman** - the server: it stays on site when everyone goes home.
- **Sticky notes** - detection manifests: a per-agent note on the door saying what
  "stuck" looks like.
- **The hotel that photographs every room nightly** - persistence by snapshot.

A lesson that needs one of these images reuses the established image rather than
inventing a second one for the same mechanism.

## Facts and their shelf life

Every technical claim cites herdr.dev or a file-and-line citation into the Herdr
repository at 0.8.2-era master. The repository moves; the citations were true of that
tree. When Herdr ships a change that invalidates a claim, update the lesson and say so
in the pull request rather than quietly editing a number.

Version-sensitive facts worth re-checking first when anything drifts:

- Install commands and package names (Lesson 05).
- The config file's key names and defaults (Lesson 06).
- Update channels and their names (Lesson 07).
- Manifest fields, capability names, and the marketplace topic (Lessons 10, 13).

## Porting notes

The thirteen lessons were authored as standalone pages with the design system inlined,
then ported into the hub. The port changed only what the hub contract forces: head
links instead of inline CSS/JS, the generated `outline.js` instead of a hand-written
manifest, hub spine, and course-map-relative paths. Teaching content is untouched.

## Gotchas

- Lesson 01's pager points back at the course map, and Lesson 13's points forward at
  it; both are `../index.html` from inside `lessons/`. A new lesson appended after 13
  must repoint Lesson 13's next-pager at itself.
- The quiz answer indices are distributed across the course; check the distribution
  over all thirteen pages, never one page, before adding a quiz.
- Mermaid labels use `&lt;br/&gt;` entities and dashes, never literal `<br/>` or
  semicolons - the two silent-repaint traps documented in the root `AGENTS.md`.
