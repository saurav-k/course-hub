# Authoring outside the hub

This branch is for the skill installed into somebody else's project.
You produce self-contained HTML learning pages that open in a browser from disk.
Nothing is published, no pull request is opened, and no part of the course hub is cloned.

## Are you on this branch?

Run the test rather than guessing from the folder name.

```bash
ls assets/hub.css AGENTS.md 2>/dev/null
```

Both present, in a repository whose root also holds `scripts/validate_site.py`, means you are inside the course hub itself.
Go back to [`SKILL.md`](SKILL.md) and pick one of the other branches.

Either one missing means the skill was installed somewhere else, by `npx skills add saurav-k/course-hub` or by hand, and this is your branch.
The installed copy usually sits at `.agents/skills/course-authoring/`, with `.claude/skills/course-authoring` symlinked to it, so a sibling `assets/` directory is not there and never will be.

## What you produce

One or more HTML files under a folder in the user's own project.

Ask where they want it.
When they have no preference, propose `learning/` at the project root and say so rather than choosing silently.
Inside it, one file per idea, named the way the hub names lessons: `0001-kebab-case.html`, zero padded, in teaching order.

Each file opens with a double-click.
Each file carries its own design system, so it keeps working after the user is offline and after this repository moves.
There is no index, no manifest and no build step unless the user asks for a set large enough to need a map, and then that map is one more hand-written HTML file beside the others.

## Getting the design system

The hub is one stylesheet and one runtime, `assets/hub.css` and `assets/hub.js`.
A page in the hub links them; a standalone page inlines them, fetched once at authoring time.

```bash
RAW=https://raw.githubusercontent.com/saurav-k/course-hub/main/assets
curl -sS "$RAW/hub.css" | sed "s#url('fonts/#url('$RAW/fonts/#g" > /tmp/hub.inline.css
curl -sS "$RAW/hub.js" > /tmp/hub.inline.js
```

Three things about that command are load-bearing.

**Inline, do not link.** `raw.githubusercontent.com` serves both files as `text/plain` with `X-Content-Type-Options: nosniff`, so a browser refuses them as a stylesheet or a script. A `<link>` or a `<script src>` pointed at those URLs produces an unstyled page with no runtime, and the network tab is the only place it says so. The files must be read at authoring time and pasted into `<style>` and `<script>` blocks.

**Rewrite the font URLs.** `hub.css` declares eight `@font-face` rules whose `src` is relative, `url('fonts/inter-latin.woff2')`. Relative to a standalone page those resolve beside the page itself and 404. The `sed` above repoints them at the canonical raw URLs, which answer with `Access-Control-Allow-Origin: *`, so the cross-origin font load succeeds. Verified: Inter, Source Serif 4 and JetBrains Mono all reach `status: "loaded"` on a page built this way. Skipping the rewrite is not fatal, because every stack has a real system fallback, but the page then looks nothing like the hub.

**Mermaid stays on the CDN**, exactly as the hub loads it, and it must be loaded *before* the inlined `hub.js`, which claims the render from it while the page is still parsing.

## The page shape

Start from [`templates/lesson.html.tmpl`](templates/lesson.html.tmpl) and change only the head and the chrome.
Everything between `<main class="wrap">` and `</main>` is the same contract as a hub lesson.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>THE ONE IDEA - PACK NAME</title>
<meta name="description" content="ONE SENTENCE: THE ONE IDEA.">
<style>
  /* the whole of hub.inline.css, pasted */
</style>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>
  /* the whole of hub.inline.js, pasted */
</script>
</head>
<body>
<nav class="spine"><div class="spine-inner">
  <a class="home" href="0001-first-page.html">PACK NAME</a>
  <span class="sp"></span>
</div></nav>

<main class="wrap">
  <!-- from here down, the lesson template unchanged -->
</main>
</body>
</html>
```

**`nav.spine` with its `.spine-inner` is not decoration and it is not optional.**
`hub.js` mounts the whole topbar into it and returns immediately when it is missing.
Delete it and the reader loses the Appearance control, which means they cannot change mode or palette, and *you* lose the repaint that moves a page between the two render states, which is the check that catches the second Mermaid trap. A standalone page without a spine cannot be verified.

## The sidebar

**Standalone pages ship without the sidebar rail, and that is a deliberate omission rather than a bug.**

The rail is built from `window.COURSE_OUTLINE`, which the hub generates into a per-course `outline.js` from that course's `index.html`.
`gen_outline.py` is not available here and there is no course map for it to read.
`hub.js` handles the absence cleanly: no `COURSE_OUTLINE` means no rail, and the topbar, quizzes, copy buttons, reading progress and Mermaid all still wire. Verified on a page built exactly as above.

For a set of five pages or more, where the reader would otherwise be lost, hand-write the manifest into the page instead of generating it.
Put it in its own `<script>` **before** the inlined `hub.js`, and give every `href` a path relative to the folder the pages sit in.

```html
<script>
window.COURSE_OUTLINE = {
  "key": "my-pack",
  "title": "PACK NAME",
  "sections": [
    { "n": "01", "title": "MODULE NAME", "lessons": [
      { "title": "FIRST PAGE", "href": "0001-first-page.html" },
      { "title": "SECOND PAGE", "href": "0002-second-page.html" }
    ]}
  ]
};
</script>
```

The names in that manifest must match the `h1` claims the way the hub requires: the rail entry is the page's **name**, which is a different object from its `h1` **claim**. [`references/page-contracts.md`](references/page-contracts.md) has the distinction.
Copy the same block into every page in the set, and remember that nothing checks it for you here, so a page added later and not added to the manifest is invisible in the rail on every other page.

## What still binds, in full

Standalone changes where the file lands. It changes nothing about what makes the page worth reading.

- **The teaching bar.** [`references/pedagogy.md`](references/pedagogy.md) applies unchanged: the orientation figure before the first body section, 1,800 prose words per page, 400 prose words per figure, two diagram kinds, and the retrieval-practice quiz. A page the reader cannot orient from is the same failure here as it is in the hub.
- **The closed vocabulary.** Every visual element comes from [`references/widgets.md`](references/widgets.md), copied character for character. The runtime is byte-identical to the hub's, so it still styles only the class names it knows and a hand-rolled quiz shape still binds to no click handler.
- **Facts carry sources.** Every technical claim links a source you fetched and read this session. A local file that nobody reviews is a weaker check on accuracy than a pull request, not a stronger one, so this bar matters more here rather than less.
- **All five silent-breakage traps.** They are properties of `hub.js` and Mermaid, and both are the same code. `<div class="mermaid">` and never `<pre>`; `&lt;br/&gt;` and never a literal `<br/>`; a dash and never a semicolon inside a Mermaid label; look at every figure in **both** render states; and match `.error-icon` rather than counting SVGs, because an error box is itself an `<svg>`. [`SKILL.md`](SKILL.md) carries the mechanism behind each one.

## What is not available

Say so plainly to the user rather than letting them assume otherwise.

- **`scripts/validate_site.py`** does not exist here, and would have nothing to check if it did: it gates registration, cross-page links and outline agreement inside the hub.
- **`scripts/gen_outline.py`** does not exist here either. It parses a course `index.html` that a standalone pack does not have. Hand-write the manifest above or do without the rail.
- **`scripts/check_pages.py`** ships inside this skill but **cannot run against a standalone page.** It resolves the repository root as four directories above itself, which from an installed copy points at the parent of the user's project, and it FAILs any page that does not *link* `assets/hub.css` and `assets/hub.js`, which is exactly what a standalone page does not do. Do not run it and do not report its output.
- **A course `BUILDER-SPEC.md`, `MISSION.md`, `NOTES.md` and `RESOURCES.md`.** There is no course to carry deltas from. Settle the scope and the learner with the user in conversation before drafting, and write the answers into a short `README.md` beside the pages if the pack is more than two files.
- **Cross-course links.** `../../llm-papers-course/index.html` resolves to nothing outside the hub. Link the live site by absolute URL when you want to point at a hub course, or do not point at it.

## The gate

[`references/verify.md`](references/verify.md) is still the gate, minus layer one, which has no scripts to run here.
Layers two and three are unchanged and they are where the real defects live.

Serve the folder rather than opening the file directly:

```bash
python3 -m http.server 8000
```

Chrome gives every `file://` page its own opaque origin, so `localStorage` fails, the mode and palette the runtime persists cannot be read back, and the repaint path you are about to test is the one that will not run.

Then walk the browser pass in [`references/verify.md`](references/verify.md) in full: every figure looked at, the palette or mode changed from the Appearance control, every figure looked at again, every quiz answered, both modes, 360px wide, print preview, every link clicked.

```js
document.querySelectorAll('.mermaid .error-icon, .mermaid text.error-text').length   // must be 0, in both render states
```

Finally, confirm the portability claim you are making.
Turn the network off, reload, and check what survives: the prose, the widgets, the quizzes, the copy buttons and the theme controls all work from the inlined runtime, the fonts fall back to the system stack, and **the diagrams do not render, because Mermaid is on the CDN.**
Tell the user that, in those words.
If they need diagrams offline, inline `mermaid.min.js` and base64 the four woff2 files into the page as well, and warn them the file goes from roughly 110KB to well over 1MB.

Then hand over the files and stop.
There is no pull request to open and nothing to publish.
