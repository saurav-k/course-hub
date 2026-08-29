#!/usr/bin/env python3
"""The contrast matrix: check G3, measured in a browser over every combination.

``scripts/contrast.py`` checks the colours ``hub.css`` states outright, which is
arithmetic and needs nothing. It cannot reach the rest of the palette. Nine
tokens are derived with ``color-mix()`` so no palette author hand-picks a tint,
and the per-course accent is an OKLCH hue rotation whose sRGB result depends on
the browser's own gamut mapping. Those are what this measures, by reading the
painted pixel back off a canvas, which is the method
``staff-ai-course/learning-records/0001-choosing-the-hue.md`` records.

**The matrix is palettes x modes x course hues, not palettes x modes.** The
rotation holds OKLCH lightness and chroma constant, but WCAG relative luminance
is not OKLCH lightness, so a hue rotation moves the measured ratio. The shipped
offsets are presumed sound and nothing had established it.

    6 palettes  x  2 modes  x  19 course hues  =  228 reachable combinations

**Which pairs are checked, and why not all of them.** A floor on a pair nobody
can see is noise, and noise is how a gate gets ignored, so the pair table is
evidence rather than assumption: it was built by walking every text node of the
harness sample in a browser and recording the colour each one computed against
the background actually behind it. That is why the body ink and the secondary
ink are checked against every tint and the faint ink is not - no page paints the
faint ink on a tinted block. Every foreground is checked against all six
surfaces, because a surface can turn up behind anything.

**What the focus ring is measured against.** The ring is drawn outside the
element with a positive offset, so what it abuts on both sides is the surface
behind the element, never the element's own fill. Those are the pairs that gate.
The fills a ring can enclose are reported beside them, because the specification
asks for both numbers, and the geometry is why only one of them is a floor.

**The palette swatches are out.** ``.pal-swatch i`` paints a palette's own
grounds as a preview of that palette. A contrast floor on it would forbid
showing a light palette at all, and WCAG exempts a graphic whose particular
presentation is essential. It is a colour sample, not a graphical object
carrying meaning of its own.

Both render states are proved rather than assumed. The 228 combinations are read
by writing the axes onto ``<html>``, which is what the appearance panel does, and
two of them are then loaded again as real pages with the preference seeded before
the first paint. A disagreement between the two is a rule that only matches on
one of them, and it fails the run.

    python3 scripts/contrast_matrix.py            # the gate, and the full report
    python3 scripts/contrast_matrix.py --quiet    # failures only

Exit code 0 means every reachable combination clears its floor.
"""

from __future__ import annotations

import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import contrast
from contrast import FLOOR_BODY, FLOOR_NON_TEXT, FLOOR_TEXT, RGB
from style_snapshot import PALETTES, SEED, SETTLE, Chrome, find_chrome, serve_repository

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
HUB_CSS: Path = REPO_ROOT / "assets" / "hub.css"

MODES: tuple[str, ...] = ("light", "dark")

# The page the matrix is read on. Any page carries the whole token layer, and
# the hub landing page carries no course, which is the one course value a real
# page cannot be loaded with any other way.
PROBE_PAGE: str = "index.html"

# The two pages that prove a written axis and a loaded one agree. One at each
# end of the hue range, in opposite modes and different palettes.
PARITY_PAGES: tuple[tuple[str, str, str, str], ...] = (
    ("staff-ai-course/index.html", "staff-ai-course", "paper", "light"),
    ("llm-inference-course/index.html", "llm-inference-course", "aubergine", "dark"),
)

COURSE_SELECTOR: re.Pattern[str] = re.compile(r':root\[data-course="(?P<course>[a-z0-9-]+)"\]')

# Every background a reader can find text on.
SURFACES: tuple[str, ...] = ("--bg", "--surface", "--surface-2", "--surface-3", "--rail-bg", "--code-bg")

# The derived tints. A callout, a practice block, a key number and the rail's
# current-lesson chip are all ink on one of these.
TINTS: tuple[str, ...] = (
    "--accent-soft", "--accent-wash", "--accent2-soft",
    "--ok-soft", "--warn-soft", "--gold-soft", "--course-soft",
)

# The eight mindmap and timeline branch fills, each of which carries a label.
BRANCH_TINTS: tuple[str, ...] = tuple(f"--branch-{step}-soft" for step in range(8))

# The categorical chart ramp: eight marks, palette-independent on purpose, drawn
# on any of the surfaces. Non-text graphical objects, so the floor is 3:1.
RAMP: tuple[str, ...] = (
    "--stat", "--prob", "--signal", "--noise",
    "--alarm", "--chart-gold", "--chart-plum", "--chart-sky",
)

DRAWN_ON: tuple[str, ...] = ("--bg", "--surface", "--surface-2", "--surface-3")

# (foreground, backgrounds, floor, the role that decides the floor)
PAIRS: tuple[tuple[str, tuple[str, ...], float, str], ...] = (
    ("--ink", SURFACES + TINTS + BRANCH_TINTS, FLOOR_BODY, "body text, SC 1.4.6"),
    ("--ink-soft", SURFACES + TINTS + BRANCH_TINTS, FLOOR_TEXT, "secondary text and every chart label"),
    ("--ink-faint", SURFACES, FLOOR_TEXT, "captions, panel headings, the read-time"),
    ("--accent", SURFACES + ("--accent-soft", "--accent-wash"), FLOOR_TEXT, "link text"),
    ("--accent-2", SURFACES + ("--accent2-soft",), FLOOR_TEXT, "eyebrows, callout tags, key numbers"),
    ("--gold", SURFACES + ("--gold-soft",), FLOOR_TEXT, "the key-idea tag"),
    ("--ok", SURFACES + ("--ok-soft",), FLOOR_TEXT, "success and read state"),
    ("--warn", SURFACES + ("--warn-soft",), FLOOR_TEXT, "error and danger"),
    ("--code-ink", ("--code-bg",), FLOOR_BODY, "code body text"),
    ("--accent-ink", ("--accent",), FLOOR_TEXT, "text on the accent, and the pressed mode card"),
    ("--course-accent", SURFACES + ("--course-soft",), FLOOR_TEXT,
     "the wordmark, a section number, the rail's current lesson"),
    ("--focus-ring-color", SURFACES + TINTS, FLOOR_NON_TEXT, "the focus ring, against what it abuts"),
    ("--line-strong", SURFACES, FLOOR_NON_TEXT, "the boundary of a control, SC 1.4.11"),
) + tuple((mark, DRAWN_ON, FLOOR_NON_TEXT, "a chart mark, SC 1.4.11") for mark in RAMP)

# Measured and printed, never gated. Two groups, and each is here for its own
# reason rather than because it was convenient to leave out.
WATCHED: tuple[tuple[str, tuple[str, ...], str], ...] = (
    (
        "--focus-ring-color",
        ("--accent", "--surface-2", "--surface-3"),
        "a fill the ring can enclose. The ring is offset, so on every one of these it abuts "
        "the surface around the control and not the control, and that is the pair that gates",
    ),
    (
        "--ink-faint",
        TINTS,
        "the faint ink on a tinted block. No page paints it there - a probe of every text node "
        "on the harness sample found the faint ink only on the plain surfaces - and these are "
        "the numbers that say it should stay that way",
    ),
)

# The recorded breaches, in the same shape and for the same reason as the ones in
# scripts/contrast.py: a gate that is red on the day it lands is a gate everyone
# learns to ignore, and fixing a token that fails is a change of its own with its
# own review. Each entry is the worst ratio measured when it was recorded.
#
# A pair that is not recorded and fails, fails the run. A recorded pair that has
# got worse fails. A recorded pair that clears its floor fails until its line is
# deleted. A recorded pair that has improved but still breaches is allowed
# through quietly, so an improvement is never punished.
#
# TOLERANCE is what a browser upgrade may move a value by without being called a
# regression. The two derived families here - a color-mix() tint and an OKLCH
# rotation clipped into sRGB - are the browser's arithmetic, not the
# stylesheet's, and they are entitled to a last digit of their own.
RECORDED: dict[tuple[str, str], float] = {
    ("--course-accent", "--course-soft"): 4.04,
    ("--course-accent", "--surface-2"): 4.42,
    ("--course-accent", "--rail-bg"): 4.42,
    ("--line-strong", "--bg"): 2.90,
    ("--line-strong", "--surface-2"): 2.87,
    ("--line-strong", "--rail-bg"): 2.87,
}

TOLERANCE: float = 0.1

TOKENS: tuple[str, ...] = tuple(
    dict.fromkeys(
        [token for token, backgrounds, _, _ in PAIRS for token in (token, *backgrounds)]
        + [token for token, backgrounds, _ in WATCHED for token in (token, *backgrounds)]
    )
)

# One element per token, then a readback of the pixel the browser would actually
# paint. Two decisions in that sentence, and both were measured.
#
# *One element per token, never one element read many times.* Setting `color` on
# a single probe and reading `getComputedStyle` after each write returns the
# FIRST value for every token afterwards: 42 tokens all come back as whatever
# the first one was, silently, and every contrast ratio computes as 1.00. A
# fresh element per token cannot hit it, and reading all of them after they are
# all attached costs one style recalculation rather than 42.
#
# *The canvas rather than the computed string.* getComputedStyle hands back a
# colour in whatever space the author wrote - `oklch()` for the rotated course
# accent, `color(srgb ...)` for a color-mix() tint - and a WCAG ratio needs the
# clipped sRGB the reader actually sees. Painting the value and reading the
# pixel back is what performs that clipping, and it is the same method the
# course-hue learning record used.
PROBE = """
(function (tokens) {
  var nodes = tokens.map(function (token) {
    var probe = document.createElement('div');
    probe.setAttribute('aria-hidden', 'true');
    probe.style.cssText = 'position:absolute;left:-9999px;color:var(' + token + ')';
    document.body.appendChild(probe);
    return probe;
  });
  var canvas = document.createElement('canvas');
  canvas.width = canvas.height = 1;
  var pen = canvas.getContext('2d', { willReadFrequently: true });
  var out = {};
  tokens.forEach(function (token, index) {
    var painted = getComputedStyle(nodes[index]).color;
    pen.clearRect(0, 0, 1, 1);
    pen.fillStyle = 'rgb(1, 2, 3)';
    pen.fillStyle = painted;
    pen.fillRect(0, 0, 1, 1);
    var pixel = pen.getImageData(0, 0, 1, 1).data;
    out[token] = [pixel[0], pixel[1], pixel[2], pixel[3]];
  });
  nodes.forEach(function (node) { node.remove(); });
  return out;
})(%(tokens)s)
"""

WRITE_AXES = """
(function (palette, mode, course) {
  var root = document.documentElement;
  root.setAttribute('data-palette', palette);
  root.setAttribute('data-mode', mode);
  if (course) root.setAttribute('data-course', course); else root.removeAttribute('data-course');
  return root.getAttribute('data-palette') + ' ' + root.getAttribute('data-mode') + ' ' +
         (root.getAttribute('data-course') || '-');
})(%(palette)s, %(mode)s, %(course)s)
"""


@dataclass(frozen=True)
class Cell:
    """One reachable combination of the three axes that decide a colour."""

    palette: str
    mode: str
    course: str

    def render(self) -> str:
        return f"{self.palette}/{self.mode}/{self.course}"


@dataclass(frozen=True)
class Measurement:
    """The worst a pair got, and the combination that produced it."""

    foreground: str
    background: str
    floor: float
    role: str
    ratio: float
    cell: Cell

    @property
    def clears(self) -> bool:
        return self.ratio >= self.floor

    @property
    def recorded(self) -> float | None:
        return RECORDED.get((self.foreground, self.background))

    @property
    def verdict(self) -> str:
        """``ok``, ``debt``, or the sentence that says why the run fails."""
        recorded = self.recorded
        if self.clears:
            if recorded is None:
                return "ok"
            return (
                f"{self.foreground} on {self.background} is {self.ratio:.2f}:1 and clears its "
                f"{self.floor:g}:1 floor, but it is still recorded as a breach. Delete its line "
                "from RECORDED in scripts/contrast_matrix.py."
            )
        if recorded is None:
            return (
                f"{self.foreground} on {self.background} is {self.ratio:.2f}:1 at "
                f"{self.cell.render()}, below the {self.floor:g}:1 floor for {self.role}"
            )
        if self.ratio < recorded - TOLERANCE:
            return (
                f"{self.foreground} on {self.background} has got worse: {self.ratio:.2f}:1 at "
                f"{self.cell.render()}, against {recorded:.2f}:1 recorded"
            )
        return "debt"


def course_hues() -> list[str]:
    """Every registered course, plus the hub itself, which wears the plain accent.

    The empty string is the hub landing page: it has no course folder in its
    path, so ``hub.js`` writes no ``data-course`` and ``--course-hue`` stays 0.
    """
    css = HUB_CSS.read_text(encoding="utf-8")
    return [""] + sorted({match.group("course") for match in COURSE_SELECTOR.finditer(css)})


def opaque(token: str, pixel: list[int]) -> RGB:
    """The measured triple, insisting the token is opaque.

    A translucent colour cannot be contrast-checked without knowing what is
    behind it, and no token in this list has an alpha. One that grew one would
    otherwise be measured against its own transparency and pass silently.
    """
    if len(pixel) != 4 or pixel[3] != 255:
        raise RuntimeError(f"{token} measured as {pixel}, which is not an opaque colour")
    return (pixel[0], pixel[1], pixel[2])


def measure(chrome: Chrome) -> dict[str, RGB]:
    raw = chrome.evaluate(PROBE % {"tokens": json.dumps(list(TOKENS))})
    if not isinstance(raw, dict):
        raise RuntimeError(f"the probe returned {raw!r} rather than a token map")
    return {token: opaque(token, pixel) for token, pixel in raw.items()}


def write_axes(chrome: Chrome, cell: Cell) -> None:
    written = chrome.evaluate(
        WRITE_AXES
        % {
            "palette": json.dumps(cell.palette),
            "mode": json.dumps(cell.mode),
            "course": json.dumps(cell.course or None),
        }
    )
    wanted = f"{cell.palette} {cell.mode} {cell.course or '-'}"
    if written != wanted:
        raise RuntimeError(f"the axes settled as {written}, expected {wanted}")


def emulate(chrome: Chrome, mode: str) -> None:
    """Ask the operating system for the opposite of what is chosen.

    That is the demanding state, and the one the mode layer's source order was
    written for: the system-preference block is guarded so an explicit light
    choice beats a dark OS, and the two explicit blocks come last so an explicit
    choice beats both. A run that agrees with the OS proves none of it.
    """
    chrome.page(
        "Emulation.setEmulatedMedia",
        {
            "media": "screen",
            "features": [
                {"name": "prefers-color-scheme", "value": "dark" if mode == "light" else "light"},
                {"name": "prefers-reduced-motion", "value": "reduce"},
                {"name": "forced-colors", "value": "none"},
            ],
        },
    )


def worst(readings: dict[Cell, dict[str, RGB]]) -> list[Measurement]:
    """The worst combination for every pair, which is the number that gates."""
    found: dict[tuple[str, str], Measurement] = {}
    for cell, colours in readings.items():
        for foreground, backgrounds, floor, role in PAIRS:
            for background in backgrounds:
                ratio = contrast.contrast(colours[foreground], colours[background])
                key = (foreground, background)
                seen = found.get(key)
                if seen is None or ratio < seen.ratio:
                    found[key] = Measurement(foreground, background, floor, role, ratio, cell)
    return sorted(found.values(), key=lambda entry: entry.ratio / entry.floor)


def lowest(readings: dict[Cell, dict[str, RGB]], foreground: str, background: str) -> tuple[Cell, float]:
    """The worst combination for one pair, and the ratio it measured there."""
    return min(
        (
            (cell, contrast.contrast(colours[foreground], colours[background]))
            for cell, colours in readings.items()
        ),
        key=lambda entry: entry[1],
    )


def report(measurements: list[Measurement], readings: dict[Cell, dict[str, RGB]]) -> None:
    print(f"\nThe worst of {len(readings)} combinations, for each of {len(measurements)} gated pairs.")
    print("Ordered by how close each one is to its own floor, tightest first.\n")
    print(f"  {'foreground':20} {'background':18} {'worst':>7} {'floor':>6}  where")
    for entry in measurements:
        flag = {"ok": " ", "debt": "-"}.get(entry.verdict, "!")
        print(
            f" {flag}{entry.foreground:20} {entry.background:18} {entry.ratio:7.2f} "
            f"{entry.floor:6g}  {entry.cell.render()}"
        )
    print("\n  '-' is a recorded breach, listed in RECORDED. '!' fails the run.")

    for foreground, backgrounds, why in WATCHED:
        print(f"\nMeasured, not gated - {foreground}, on {why}.\n")
        print(f"  {'background':20} {'worst':>7}  where")
        for background in backgrounds:
            cell, ratio = lowest(readings, foreground, background)
            print(f"  {background:20} {ratio:7.2f}  {cell.render()}")


def parity(chrome: Chrome, origin: str, readings: dict[Cell, dict[str, RGB]]) -> list[str]:
    """A written axis and a loaded page must compute the same colours.

    Everything above is read by writing ``data-palette``, ``data-mode`` and
    ``data-course`` onto ``<html>`` on one open page, which is exactly what the
    appearance panel does. This loads two of those combinations as real pages
    instead, with the preference seeded before the first paint and the course
    read out of the URL by ``hub.js``, and insists the two agree. They are the
    two render states the specification asks for, and a rule that only matches
    on one of them is caught here rather than by a reader.
    """
    problems: list[str] = []
    seeded: str | None = None
    for page, course, palette, mode in PARITY_PAGES:
        cell = Cell(palette, mode, course)
        emulate(chrome, mode)
        if seeded is not None:
            chrome.page("Page.removeScriptToEvaluateOnNewDocument", {"identifier": seeded})
        seeded = chrome.page(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": SEED % {"mode": json.dumps(mode), "palette": json.dumps(palette)}},
        )["identifier"]

        chrome.drain()
        chrome.page("Page.navigate", {"url": f"{origin}/{page}"})
        chrome.await_event("Page.loadEventFired")
        settled = str(chrome.evaluate(SETTLE))
        if settled != f"{palette} {mode}":
            problems.append(f"{page} settled as {settled}, expected {palette} {mode}")
            continue

        loaded = measure(chrome)
        written = readings[cell]
        moved = [token for token in TOKENS if loaded[token] != written[token]]
        if moved:
            problems.append(
                f"{page} loaded at {cell.render()} computes a different colour for "
                f"{', '.join(moved)} than the same combination written onto <html>"
            )
    return problems


def run(quiet: bool) -> int:
    started = time.time()
    courses = course_hues()
    cells = [
        Cell(palette, mode, course)
        for mode in MODES
        for palette in PALETTES
        for course in courses
    ]

    server, origin = serve_repository()
    chrome = Chrome(find_chrome())
    readings: dict[Cell, dict[str, RGB]] = {}
    try:
        chrome.page("Page.enable")
        chrome.page("Runtime.enable")
        chrome.drain()
        chrome.page("Page.navigate", {"url": f"{origin}/{PROBE_PAGE}"})
        chrome.await_event("Page.loadEventFired")
        chrome.evaluate(SETTLE)

        current: str | None = None
        for cell in cells:
            if cell.mode != current:
                emulate(chrome, cell.mode)
                current = cell.mode
            write_axes(chrome, cell)
            readings[cell] = measure(chrome)

        problems = parity(chrome, origin, readings)
    finally:
        chrome.close()
        server.shutdown()

    measurements = worst(readings)
    if not quiet:
        report(measurements, readings)

    failures = [entry.verdict for entry in measurements if entry.verdict not in ("ok", "debt")]
    unseen = sorted(
        pair for pair in RECORDED if pair not in {(entry.foreground, entry.background) for entry in measurements}
    )
    failures += [
        f"{foreground} on {background} is recorded as a breach but is no longer a pair this "
        "matrix checks. Delete its line from RECORDED in scripts/contrast_matrix.py."
        for foreground, background in unseen
    ]

    elapsed = time.time() - started
    if failures or problems:
        print(f"\n{len(failures) + len(problems)} failure(s):\n")
        for failure in failures + problems:
            print(f"  - {failure}")
        return 1

    debt = [entry for entry in measurements if entry.verdict == "debt"]
    print(
        f"\nThe contrast matrix holds: {len(cells)} combinations "
        f"({len(PALETTES)} palettes x {len(MODES)} modes x {len(courses)} course hues), "
        f"{len(measurements)} pairs, in {elapsed:.0f}s."
    )
    if debt:
        print(f"Note: {len(debt)} recorded breach(es), none of them new or worse:\n")
        for entry in debt:
            print(
                f"  - {entry.foreground} on {entry.background} is {entry.ratio:.2f}:1 at "
                f"{entry.cell.render()}, against a {entry.floor:g}:1 floor"
            )
    return 0


def main() -> int:
    return run(quiet="--quiet" in sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
