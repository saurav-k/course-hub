#!/usr/bin/env python3
"""Tab through the hub and insist every stop shows the hub's own focus ring.

A reader on a keyboard has to be able to see where they are. The rule is in
``hub.css`` and nothing could see whether it held: the computed-style harness
captures a page at rest, and a focus ring exists only in a state that capture
never enters. So this walks the page the way a reader does, with real Tab keys
dispatched into the browser, and reads the outline off whatever ``:focus-visible``
lands on.

Three things are checked at every stop.

    1. There is a ring: an outline style that is not ``none`` and a width above 0.
    2. It is *this* hub's ring, not the browser's. The outline colour must be the
       computed value of ``--focus-ring-color``. Chrome's own ring is a cold blue
       that belongs to no palette here, and it is what an element the stylesheet
       forgot falls back to.
    3. It is offset off the element. A ring drawn on the border box of a scroll
       container is clipped by that container and disappears.

And one thing is checked before any of them, on a page nothing has typed into
yet: **a mouse click paints no ring.** That is the whole reason the rule is
written against ``:focus-visible`` rather than ``:focus``, and a rule that quietly
went back to ``:focus`` would pass every check above. It has to come first,
because Chrome keeps ``:focus-visible`` on an element that already had it, so the
same click tested after a walk would be measuring the walk's own keyboard
modality rather than the click.

The walk covers three pages, both panels, and one narrow viewport, in both
modes. The panels are here because a settings panel is the classic place a
design system fails its own floor, because a study notes panel is thirteen more
controls and a textarea on the same footing, and because both are built by
script at the moment they are opened, so neither existed when the page was
first painted - which is exactly the state a capture of the first paint cannot
see. The narrow viewport is here because a scroll container only earns its tab
stop when it genuinely scrolls, and at a full-width column nothing in this hub
does.

The palettes are not walked. The ring's colour is a token, and the token is
measured against every surface in every palette and mode by
``scripts/contrast_matrix.py``; what is left for this script is whether the ring
is drawn at all, and that is decided by selectors rather than by the palette.

    python3 scripts/focus_walk.py             # the gate, and the walk
    python3 scripts/focus_walk.py --quiet     # failures only
    python3 scripts/focus_walk.py --self-test # prove the walk fails on a broken ring

Exit code 0 means every stop wore the ring.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

from style_snapshot import SEED, SETTLE, Chrome, find_chrome, serve_repository

REPO_ROOT: Path = Path(__file__).resolve().parent.parent

# Three pages, each carrying a control the others do not.
#
#   the lesson    a rail, a topbar, a quiz, code plates: the ordinary page
#   the audit     the hub's only textarea, which is the control the old rule
#                 missed and the browser's own ring was drawing
#   the matrix    wide tables and code, which hub.js gives a tabindex to when
#                 they genuinely scroll, so the ring on a scroll container is
#                 walked rather than assumed
WALKED: tuple[str, ...] = (
    "staff-ai-course/lessons/0001-should-this-be-an-ai-system.html",
    "probability-you-build-course/lessons/0508-the-audit-card.html",
    "cloud-comparison-course/lessons/0203-the-function-container-boundary.html",
)

MODES: tuple[str, ...] = ("light", "dark")
PALETTE: str = "paper"

# The narrow pass. Below 720px hub.css turns a table into a scroll container, and
# hub.js gives every box that genuinely scrolls a tabindex so a reader with no
# mouse can reach its right-hand columns. That tab stop takes the ring at the
# wider of the two offsets, and at 1280px no box on any page here overflows, so
# the rule would never be walked at all without this.
NARROW: tuple[int, int] = (700, 900)

# A page whose code plate is wider than a 700px column, so it genuinely scrolls
# and genuinely earns its tab stop.
NARROW_PAGE: str = "llm-inference-course/lessons/0014-inference-unit-economics.html"

# Enough stops to leave any page in this hub, and a bound so a focus trap ends
# the run instead of hanging it.
MAX_STOPS: int = 400

# The floor on a walk, and it is deliberately far below what any of these pages
# actually has. How many stops a page offers is decided by layout - a box only
# takes a tab stop when it genuinely scrolls, and how much scrolls depends on
# the renderer's own text metrics, which is why the same walk finds 419 stops on
# a Mac and 384 on the CI runner. Asserting a count would be asserting a font.
# What this catches is a walk that has collapsed: a page that stops taking focus
# after three controls passes every per-stop check and proves nothing.
MIN_STOPS: int = 8

TAB_DOWN: dict[str, object] = {
    "type": "rawKeyDown", "key": "Tab", "code": "Tab",
    "windowsVirtualKeyCode": 9, "nativeVirtualKeyCode": 9,
}
TAB_UP: dict[str, object] = {
    "type": "keyUp", "key": "Tab", "code": "Tab",
    "windowsVirtualKeyCode": 9, "nativeVirtualKeyCode": 9,
}

# What the ring should be, read off the same token every rule reads.
EXPECTED = """
(function () {
  var probe = document.createElement('div');
  probe.style.cssText = 'position:absolute;left:-9999px;color:var(--focus-ring-color)';
  document.body.appendChild(probe);
  var colour = getComputedStyle(probe).color;
  probe.remove();
  return colour;
})()
"""

# The element focus has landed on, named the way a reader of a failure needs it,
# and the four properties that decide whether a ring is there.
#
# Each element is marked as it is visited, and the mark is what ends the walk.
# Ending it on a repeated name instead would stop early on any page with two
# links that read the same, which is most of them: one walk here ended after 31
# of 52 stops that way and looked like a complete pass. The attribute matches no
# selector in the stylesheet, so marking cannot change what is measured.
STOP = """
(function () {
  var el = document.activeElement;
  if (!el || el === document.body || el === document.documentElement) return null;
  var repeat = el.hasAttribute('data-focus-walk');
  el.setAttribute('data-focus-walk', '');
  var style = getComputedStyle(el);
  var name = el.tagName.toLowerCase();
  if (el.id) name += '#' + el.id;
  if (el.className && typeof el.className === 'string') name += '.' + el.className.trim().split(/\\s+/).join('.');
  return {
    repeat: repeat,
    name: name,
    label: (el.getAttribute('aria-label') || el.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 40),
    visible: el.matches(':focus-visible'),
    style: style.outlineStyle,
    width: style.outlineWidth,
    offset: style.outlineOffset,
    colour: style.outlineColor
  };
})()
"""

# The two panels, each reached by the button that names it. The selector is
# `aria-controls` rather than `aria-haspopup="dialog"` because two buttons in
# the topbar now say they open a dialog, and a positional selector between them
# would silently walk one panel twice the day either is appended in the other
# order. `attachOpener` in hub.js writes the attribute, so a panel that reaches
# the topbar at all is reachable here.
#
# Both are left open. Two open panels is a state a reader can reach - they are
# non-modal and neither closes the other - and the second walk is bounded by
# its own container either way.
PANELS: tuple[tuple[str, str, str], ...] = (
    ("the appearance panel", '.tb-btn[aria-controls="panel-appearance"]', ".settings"),
    ("the study notes panel", '.tb-btn[aria-controls="panel-notes"]', ".notes"),
)

# The button the mouse check clicks. It only has to be a control that opens
# something, and the appearance panel's is the one that has always been it.
PANEL_BUTTON: str = PANELS[0][1]

CLICK_TARGET = """
(function (selector) {
  var button = document.querySelector(selector);
  if (!button) return null;
  var box = button.getBoundingClientRect();
  return { x: Math.round(box.left + box.width / 2), y: Math.round(box.top + box.height / 2) };
})(%(selector)s)
"""

OPEN_PANEL = """
(function (selector, within) {
  var button = document.querySelector(selector);
  if (!button) return 'no button matching ' + selector + ' in the topbar';
  button.click();
  var panel = document.querySelector(within);
  if (!panel) return 'the panel was never built';
  if (panel.hidden) return 'the panel did not open';
  var first = panel.querySelector('a, button, input, select, textarea, [tabindex]');
  if (!first) return 'the panel has no control to focus';
  first.focus();
  return 'open';
})(%(selector)s, %(within)s)
"""

INSIDE = """
(function (selector) {
  var panel = document.querySelector(selector);
  return !!(panel && document.activeElement && panel.contains(document.activeElement));
})(%(selector)s)
"""


@dataclass(frozen=True)
class Failure:
    where: str
    detail: str

    def render(self) -> str:
        return f"{self.where}: {self.detail}"


def settle(chrome: Chrome) -> None:
    """Let the focus change reach the computed style before anything reads it.

    Chrome hands back a half-applied style if it is asked immediately after the
    key: the outline style has flipped to ``solid`` but the width and the colour
    are still the element's unfocused values, so the ring reads as
    ``3px solid currentcolor`` - which is indistinguishable from the browser's
    own ring and would fail every stop for a reason that is not real. Two frames
    is what it takes, and it is the same lesson ``style_snapshot.py`` records
    about reading a computed style straight after a change.
    """
    chrome.evaluate(
        "new Promise(function (done) { requestAnimationFrame(function () "
        "{ requestAnimationFrame(done); }); })"
    )


def load(chrome: Chrome, origin: str, page: str, palette: str, mode: str) -> str | None:
    """Open the page fresh, and say so if it did not arrive in the state asked for.

    The lesson is loaded again between the mouse check and the walk rather than
    reset in place. Blurring does not move the sequential focus navigation
    starting point: the next Tab carries on from whatever was last focused, so a
    walk after a click begins in the middle of the page and reports a clean pass
    over the two thirds of the controls it saw. A load is the only thing that
    puts the starting point back at the top.
    """
    chrome.drain()
    chrome.page("Page.navigate", {"url": f"{origin}/{page}"})
    chrome.await_event("Page.loadEventFired")
    settled = str(chrome.evaluate(SETTLE))
    return None if settled == f"{palette} {mode}" else f"settled as {settled}, expected {palette} {mode}"


def tab(chrome: Chrome) -> None:
    chrome.page("Input.dispatchKeyEvent", TAB_DOWN)
    chrome.page("Input.dispatchKeyEvent", TAB_UP)
    settle(chrome)


def judge(where: str, stop: dict, expected: str) -> list[Failure]:
    """Everything wrong with one focus stop, named so it can be fixed without the code."""
    who = f"{where} {stop['name']}"
    if stop["label"]:
        who += f" ({stop['label']})"
    failures: list[Failure] = []

    if not stop["visible"]:
        # Chrome decided this stop is not focus-visible even under a Tab key.
        # That is not a defect in the stylesheet, and there is nothing to judge.
        return failures
    if stop["style"] == "none" or stop["width"] in ("0px", "0"):
        failures.append(Failure(who, f"has no focus ring: outline {stop['style']} {stop['width']}"))
        return failures
    if stop["colour"] != expected:
        failures.append(
            Failure(who, f"rings in {stop['colour']}, not the hub's {expected}. A stop the stylesheet "
                         "missed falls back to the browser's own ring.")
        )
    if stop["offset"] in ("0px", "0") or stop["offset"].startswith("-"):
        failures.append(
            Failure(who, f"rings at an offset of {stop['offset']}; a ring on the border box of a "
                         "scroll container is clipped by it")
        )
    return failures


def walk(chrome: Chrome, where: str, within: str | None = None) -> tuple[list[dict], list[Failure]]:
    """Every stop from here on, and what is wrong with each of them.

    ``within`` bounds the walk to one container, which is how the panel is
    walked: the panel is appended to the end of the body, so tabbing out of it
    lands back in the page rather than wrapping, and the walk has to know where
    it ends. Without it the walk runs until a stop repeats.
    """
    expected = str(chrome.evaluate(EXPECTED))
    inside = None if within is None else INSIDE % {"selector": json.dumps(within)}
    stops: list[dict] = []
    failures: list[Failure] = []

    if within is not None:
        first = chrome.evaluate(STOP)
        if isinstance(first, dict):
            stops.append(first)
            failures += judge(where, first, expected)

    for _ in range(MAX_STOPS):
        tab(chrome)
        if inside is not None and not chrome.evaluate(inside):
            break
        stop = chrome.evaluate(STOP)
        if not isinstance(stop, dict) or stop["repeat"]:
            break
        stops.append(stop)
        failures += judge(where, stop, expected)

    if len(stops) < MIN_STOPS:
        failures.append(
            Failure(where, f"only {len(stops)} stop(s) took focus, below the {MIN_STOPS} a walk of "
                           "anything in this hub reaches. The walk collapsed rather than passed.")
        )
    return stops, failures


def mouse_leaves_no_ring(chrome: Chrome, where: str) -> list[Failure]:
    """A click must paint nothing. That is what :focus-visible buys, and it is easy to lose."""
    target = chrome.evaluate(CLICK_TARGET % {"selector": json.dumps(PANEL_BUTTON)})
    if not isinstance(target, dict):
        return [Failure(where, "no appearance button to click; the mouse check proved nothing")]
    def press() -> None:
        for kind in ("mousePressed", "mouseReleased"):
            chrome.page(
                "Input.dispatchMouseEvent",
                {"type": kind, "x": target["x"], "y": target["y"], "button": "left", "clickCount": 1},
            )
        settle(chrome)

    press()
    stop = chrome.evaluate(STOP)
    # The button is a toggle and this one opened the panel. Close it again, so
    # the walk that follows starts from the page as a reader first meets it.
    press()
    if not isinstance(stop, dict):
        return [Failure(where, "the click focused nothing; the mouse check proved nothing")]
    if stop["visible"] or (stop["style"] != "none" and stop["width"] not in ("0px", "0")):
        return [
            Failure(
                f"{where} {stop['name']}",
                f"paints a ring on a mouse click: outline {stop['style']} {stop['width']} "
                f"{stop['colour']}. The rule must be :focus-visible, never :focus.",
            )
        ]
    return []


def run(quiet: bool) -> int:
    server, origin = serve_repository()
    chrome = Chrome(find_chrome())
    failures: list[Failure] = []
    walked: list[tuple[str, list[dict]]] = []
    try:
        chrome.page("Page.enable")
        chrome.page("Runtime.enable")
        for mode in MODES:
            chrome.page(
                "Emulation.setEmulatedMedia",
                {
                    "media": "screen",
                    "features": [
                        {"name": "prefers-color-scheme", "value": "dark" if mode == "light" else "light"},
                        {"name": "prefers-reduced-motion", "value": "reduce"},
                    ],
                },
            )
            chrome.page(
                "Page.addScriptToEvaluateOnNewDocument",
                {"source": SEED % {"mode": json.dumps(mode), "palette": json.dumps(PALETTE)}},
            )
            for page in WALKED:
                wrong = load(chrome, origin, page, PALETTE, mode)
                if wrong:
                    failures.append(Failure(page, wrong))
                    continue

                # The mouse first, on a page nothing has typed into yet: Chrome
                # keeps :focus-visible on an element that already had it, so a
                # click tested after the walk would be testing the walk's own
                # keyboard modality rather than the click.
                failures += mouse_leaves_no_ring(chrome, f"the mouse on {page} [{PALETTE}/{mode}]")

                wrong = load(chrome, origin, page, PALETTE, mode)
                if wrong:
                    failures.append(Failure(page, wrong))
                    continue
                where = f"{page} [{PALETTE}/{mode}]"
                stops, found = walk(chrome, where)
                walked.append((where, stops))
                failures += found

                for label, opener, selector in PANELS:
                    where = f"{label} on {page} [{PALETTE}/{mode}]"
                    opened = str(chrome.evaluate(
                        OPEN_PANEL % {"selector": json.dumps(opener), "within": json.dumps(selector)}
                    ))
                    if opened != "open":
                        failures.append(Failure(where, opened))
                        continue
                    settle(chrome)
                    stops, found = walk(chrome, where, within=selector)
                    walked.append((where, stops))
                    failures += found
            chrome.page(
                "Emulation.setDeviceMetricsOverride",
                {"width": NARROW[0], "height": NARROW[1], "deviceScaleFactor": 1, "mobile": False},
            )
            page = NARROW_PAGE
            wrong = load(chrome, origin, page, PALETTE, mode)
            if wrong:
                failures.append(Failure(page, wrong))
            else:
                where = f"{page} at {NARROW[0]}px [{PALETTE}/{mode}]"
                stops, found = walk(chrome, where)
                walked.append((where, stops))
                failures += found
                if not any("tabindex" in stop["name"] or stop["name"].startswith(("pre", "table"))
                           for stop in stops):
                    failures.append(
                        Failure(where, "no scroll container took a tab stop, so the ring on one was "
                                       "never walked. Either the page stopped overflowing or hub.js "
                                       "stopped marking it.")
                    )
            chrome.page("Emulation.clearDeviceMetricsOverride")
    finally:
        chrome.close()
        server.shutdown()

    if not quiet:
        for where, stops in walked:
            print(f"\n{where}: {len(stops)} stop(s)\n")
            for stop in stops:
                ring = "not focus-visible" if not stop["visible"] else (
                    f"{stop['width']} {stop['style']} {stop['colour']} at {stop['offset']}"
                )
                print(f"  {stop['name'][:44]:46} {ring}")

    if failures:
        print(f"\n{len(failures)} focus failure(s):\n")
        for failure in failures:
            print(f"  - {failure.render()}")
        return 1

    total = sum(len(stops) for _, stops in walked)
    print(f"\nEvery focus stop wears the hub's ring: {total} stop(s) over {len(walked)} walk(s).")
    return 0


BREAK = """
(function (rule) {
  var style = document.createElement('style');
  style.textContent = rule;
  document.head.appendChild(style);
  return true;
})(%(rule)s)
"""

# Each one is a way a focus ring is lost in practice, and the walk has to say so.
BROKEN: tuple[tuple[str, str, str], ...] = (
    ("a ring removed outright", "a:focus-visible { outline: none !important; }", "has no focus ring"),
    ("a ring left to the browser", "a:focus-visible { outline: 1px solid rgb(0, 95, 204) !important; }", "not the hub's"),
    ("a ring flat on the border box", "a:focus-visible { outline-offset: 0 !important; }", "offset of 0px"),
)


def self_test() -> int:
    """Prove the walk fails on a deliberately broken ring, and passes on the real one.

    A check nobody has seen fail is a check nobody knows works. Each case breaks
    one page's links in one way and asserts the walk names it.
    """
    server, origin = serve_repository()
    chrome = Chrome(find_chrome())
    problems: list[str] = []
    try:
        chrome.page("Page.enable")
        chrome.page("Runtime.enable")
        for description, rule, phrase in BROKEN:
            wrong = load(chrome, origin, WALKED[0], PALETTE, "")
            if wrong and "expected paper" not in wrong:
                problems.append(f"{description}: {wrong}")
                continue
            chrome.evaluate(BREAK % {"rule": json.dumps(rule)})
            _, failures = walk(chrome, "self-test")
            hit = [failure for failure in failures if phrase in failure.detail]
            if hit:
                print(f"  pass  {description} -> {hit[0].render()}")
            else:
                reported = "; ".join(failure.detail for failure in failures) or "nothing"
                problems.append(f"{description}: expected a failure mentioning {phrase!r}, got {reported}")
    finally:
        chrome.close()
        server.shutdown()

    if problems:
        print("\nThe walk does not bite:\n")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"\n{len(BROKEN)} broken rings caught.")
    return 0


def main() -> int:
    if "--self-test" in sys.argv[1:]:
        return self_test()
    return run(quiet="--quiet" in sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
