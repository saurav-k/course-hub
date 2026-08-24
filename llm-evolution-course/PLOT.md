# Plot - the reading order of this course

This course is the hub's only **routed** course, so its plot is unusual and worth stating precisely.
There is no single reading order by design: there is one pool of 57 pages in `lessons/`, and four named orders over that pool, declared in [`routes.js`](routes.js).
The machine-readable form of this file is `routes.js`; this file records what it means, why it is shaped that way, and what is planned but unwritten.

The order rule, which holds here in its routed form and everywhere else in the hub in its plain form: **a course's reading order is its true order, and a tutorial or lab session that follows a lecture sits after that lecture in the course map, never in a separate list at the bottom.**
Here the "course map" is the outline of whichever route the reader is on, shown in `index.html`.
When any route's outline and this file disagree, one of them is wrong, and it gets fixed before anything new is added.

## The four true orders

| Route | Sections | The order it gives |
|---|---|---|
| `constraint` (**default**) | 7 | By binding constraint. Seven eras, each named for the one thing holding the field back: Rules, Meaning, Reach, Scale, Usefulness, Cost, Thinking. Every section opens with the problem and closes with what solved it. |
| `spine` | 10 | The ten short spine chapters telling the whole arc at low resolution, each followed by the deep dives that zoom into it. |
| `capability` | 6 | Six rungs: one thing machines learned to do per section, in the order they learned it. |
| `era` | 6 | Straight chronology, six periods, nothing rearranged to make an argument. |

A reader picks a lens; the pool does not change.
Every page has exactly one URL no matter which route reached it, the route travels in a query parameter, and `routes/README.md` specifies the whole contract, including what the validator enforces.

## Status

All 57 pages - ten spine chapters and 47 deep dives - are written and present in all four routes.
There are no reserved positions.

## Planned but unwritten

- **Nothing in the pool.** A new lesson takes the next free number, joins every route whose kinds include its kind at the position that route wants, gets a card in every route map in `index.html`, and gets its committed pager fixed against its owning route. That procedure is in `routes/README.md`, and the validator fails the pull request if any step is skipped.
- **Model comparison tables as data.** Deliberately deferred until the first such table exists; see the "Things deliberately not done" section of `NOTES.md`.

If a fifth route is ever wanted, it is a manifest entry, four CSS lines, a scope document under `routes/`, and cards; no JavaScript changes. `routes/README.md` walks through it.

## Adding a session to this course

1. Read `routes/README.md` first; it is authoritative over anything summarised here.
2. Take the next free lesson number. Numbers are identity; routes are order.
3. Add one entry to `pages` in `routes.js`, then add the file to **every** route whose kinds include its kind, at the position that route wants.
4. Add a card inside every route map it belongs to, fix the committed pagers in the owning route, run `python3 scripts/validate_site.py`, and click through all four routes before opening the pull request.
