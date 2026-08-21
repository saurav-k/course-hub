# Routes: how one pool of lessons is travelled four ways

This directory holds the scope document for each route.
This file explains the mechanism they all run on.
Read it before you add a route, add a lesson, or change anything under `lessons/`.

## The idea in one paragraph

There is one pool of pages in `lessons/`.
A route is a named ordering and grouping of that pool, and nothing more.
A lesson has exactly one URL no matter which route reached it, so the route cannot live in the path.
It lives in a query parameter instead, which means a route can be shared, bookmarked, and switched without leaving the page you are on.

## The four files that make it work

| File | What it is |
|---|---|
| `routes.js` | The manifest. Hand-authored, and the single source of truth for what the four routes contain. |
| `outline.js` | The runtime. Resolves the active route, derives the outline the shared rail renders, and carries the route across links. |
| `index.html` | The course map. Contains all four route outlines as static markup; CSS shows one. |
| `assets/course-extras.css` | All route visibility. No JavaScript does layout work. |

### `routes.js`

```js
window.COURSE_ROUTES = {
  "key": "llm-evolution",
  "title": "How Language Models Happened",
  "default": "constraint",
  "pages":  { "0024-the-transformer-drops-recurrence.html": { "title": "...", "kind": "pool" }, ... },
  "extras": [ { "title": "Glossary", "href": "reference/glossary.html" }, ... ],
  "routes": [ { "id": "constraint", "name": "...", "blurb": "...", "kinds": ["pool"],
                "sections": [ { "n": "01", "title": "Rules", "lessons": ["0011-....html", ...] } ] }, ... ]
};
```

`pages` is identity: one entry per file in `lessons/`, keyed by file name, carrying the title and the kind.
A route lists the same file names in its own order and grouping.
Two kinds exist today: `pool` is a deep dive, `spine` is one of the ten short overview chapters.
A route declares which kinds it carries, and it must then contain every page of those kinds.

The manifest is a pure JSON literal on purpose, so that `scripts/validate_site.py` can parse it without executing anything.

### `outline.js`

Every other course in the hub ships a static `window.COURSE_OUTLINE` that the rail in `assets/hub.js` renders.
This course has four outlines over one pool, so it derives that object at load time from whichever route is active.
Nothing in `hub.js` needed changing: it still finds one `COURSE_OUTLINE`, and it still finds one script whose `src` ends in `outline.js`, which is how it locates the course root.

In the head, synchronously, before the body is parsed, it resolves the active route and sets `data-route` on `<html>`.
That is what stops the course map flashing all four outlines before settling on one.
On `DOMContentLoaded` it canonicalises the address, carries the route across in-course links, marks the active switch, re-points the pager, and rewrites the breadcrumb's section name.

## The URL contract

**The route is a query parameter. The path is the lesson's identity and never mentions a route.**

```
lessons/0024-the-transformer-drops-recurrence.html                    the default route
lessons/0024-the-transformer-drops-recurrence.html?route=capability   the capability ladder
```

Resolution order, highest first:

1. `?route=` in the address.
   Following a shared link switches your lens rather than fighting it, and the choice is remembered.
2. The stored preference, in `localStorage` under `coursehub.route.llm-evolution`.
3. The manifest's `default`.

A route named in the address that does not exist is ignored, and the default is used.

**The address always carries the route when the route is not the default, and never when it is.**
That is the rule that makes a shared link preserve the lens while keeping the canonical URL clean.
A reader in the capability ladder sees `?route=capability` in the address bar whether they arrived through a link or through their stored preference, so copying the address always shares what they are reading.
A reader in the default route sees a bare path, and the absence of the parameter is what preserves the default.
`outline.js` adds or removes the parameter with `history.replaceState`, which changes no history entry and reloads nothing.

A stored preference alone would not achieve this.
Storage is per-browser, so it tells the sender's browser which lens to use and tells the recipient's browser nothing.
Only something in the link can cross the gap.

## Without JavaScript

The page is complete, not degraded into uselessness.

| Part | With scripting | Without |
|---|---|---|
| Route switcher | The active lens is filled in | Four working links; the default is filled in by a CSS fallback selector |
| Course map | One route outline shown | All four shown one after another, each under its own heading, with a note saying so |
| Lesson body, figures, sources, quiz markup | Unchanged | Unchanged |
| Pager | Re-pointed at the active route | The committed pager, which is the route that owns the page |
| Breadcrumb | Section name of the active route | The committed section name, from the route that owns the page |
| Outline rail | Rendered from the active route | Absent, exactly as on every other course in the hub |

The route switcher is four real anchors with real `href` values, so switching route works with scripting off too: the links are `?route=name`, which resolves against the current page and therefore keeps you on the same lesson.
The only thing that stops working is the memory of your choice.

**The route that owns a page** is the first route in `routes.js` that contains it: the default route for a deep dive, and the spine route for a spine chapter, since the spine chapters appear in no other route.
The committed pager and breadcrumb follow that route, which is what makes them correct rather than arbitrary when nothing is running.

## What the validator enforces

`scripts/validate_site.py` fails the pull request on every one of these:

1. A file in `lessons/` that is not in `pages`, or a `pages` entry with no file.
2. A route listing a page that is not in `pages`, or listing one twice.
3. A route missing any page of a kind it declares. This is the check that catches "added a lesson, forgot three routes".
4. A `default` that names no route, or a route with no `kinds`.
5. A title in `pages` that does not match the `h1` of the page it names.
6. A committed `.pager` that does not match the owning route's neighbours.
7. A lesson missing `data-zone` or `data-asof`.
8. Any published page linking a local `.md` file, which the deploy excludes and which would therefore 404 on the live site.

The outline check that applies to every other course is skipped here, because this course's `outline.js` derives its outline instead of declaring one.
For the same reason `scripts/gen_outline.py` refuses to run against a course that ships `routes.js`.

## Adding a lesson

1. Take the next free number. **Numbers are identity; routes are order.** A lesson that belongs chronologically in the middle still gets the next free number at the end.
2. Write `lessons/NNNN-kebab-case.html`.
3. Add one entry to `pages` in `routes.js`, and add the file to **every** route whose `kinds` include its kind, in the position that route wants it.
4. Add a card to `index.html` inside every route map it belongs to.
5. Fix the committed `.pager` on its neighbours in the owning route, and its own.
6. Run the validator, then open the page and click through all four routes.

## Adding a route

A fifth route is a manifest entry, a card, an outline in `index.html`, and four CSS lines.
No JavaScript changes.

1. Append a route object to `routes` in `routes.js`, with a new `id`, a `name`, a `blurb`, its `kinds`, and its sections. It must contain every page of the kinds it declares.
2. Write `routes/<id>.md`, following the shape of the four already here: what it covers, what it deliberately leaves out, who it is for, and how to extend it.
3. Add a `.routecard` to the chooser in `index.html`, and a `.route-map` section holding the new outline.
4. Add the route's `id` to the four selector lists in `assets/course-extras.css`: the active switch, the active card, and the two map-visibility rules.
5. Add a `?route=<id>` link to the `.routebar` on every page. That is a mechanical edit across `lessons/`, `reference/` and `index.html`.
6. Run the validator.

Step 5 is the only part that scales with the number of pages, and it is a one-line insertion per page.
If a course ever wants routes to be cheap to add, that is the thing to change: render the switcher from the manifest at load time and accept that it disappears without scripting.
That trade was refused here, because a navigation control that vanishes without scripting is worse than a mechanical edit.

## Deliberate non-goals

- **No per-route lesson content.** A lesson reads the same in every route. If a lesson needs a different framing per route, it is two lessons, or the route boundary is in the wrong place.
- **No per-route progress.** Read state is keyed on the course, not the route, so progress follows the reader across lenses. That is the point of one pool.
- **No route in the path, ever.** It would double every URL and break the promise that a lesson has one address.
