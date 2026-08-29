#!/usr/bin/env python3
"""The computed-style harness: proof that a stylesheet change moved nothing.

``scripts/validate_site.py`` checks that the site hangs together and that every
page reaches the design system. It cannot see what the design system then does.
This can. It loads a fixed sample of pages in headless Chrome and records the
computed value of every property that matters, for every class in the closed
widget vocabulary, across ``{6 palettes} x {light, dark}``, and writes the whole
lot as a committed snapshot.

A later change proves itself by producing a zero diff against that snapshot,
with this script naming the page, the element shape and the property that moved.
That is what converts a large mechanical edit from "hope review catches it" into
"the tool says zero".

    python3 scripts/style_snapshot.py                  # compare against the snapshot
    python3 scripts/style_snapshot.py --write          # record a new snapshot
    python3 scripts/style_snapshot.py --refresh-sample # re-pick the sample pages
    python3 scripts/style_snapshot.py --sample-only    # print the sample and stop

Exit code 0 means nothing moved. Exit code 1 lists every difference.

Five decisions worth knowing before you read the code.

*The run is hermetic.* Chrome resolves nothing but the loopback address, so the
Mermaid CDN never answers and no diagram renders. ``hub.js`` guards every
``window.mermaid`` call, so the pages are correct without it, and a harness that
depends on a third party is a harness that goes red for reasons of its own.

*Layout-computed geometry is left out, and what is left of it is rounded.*
``width`` and ``height`` are recorded by nothing here, because they follow the
text: a paragraph added to a sample page would move them, the snapshot would
need refreshing on a prose pull request, and a tool that cries wolf is a tool
reviewers learn to ignore. The seven properties that survive but are still
resolved from measured text - grid tracks, margins, ``max-width``,
``min-height`` - are recorded to the nearest whole pixel, because the same
stylesheet lays the same column out a fifth of a pixel differently on a Linux
runner than on a Mac and the snapshot has to compare equal on both. The rest of
the box model, and line height, are recorded exactly.

*A class is sampled once per element shape per page.* Every element carrying a
documented class is grouped by its tag and its own class list, and the first of
each group is recorded. That keeps ``.callout`` and ``.callout.warn`` apart,
keeps the snapshot the same size whether a page has one callout or thirty, and
keys every row on something that does not move when the prose does.

*The recorded matrix is the demanding one.* Each row is captured with the mode
chosen explicitly and the operating system asking for the opposite, because that
is the state the hub's mode-layer ordering was written for. The agreeing state
is checked too, as assertion A1 below, rather than stored twice.

*Three assertions run beside the snapshot, and none is stored.* The first two
are render states that a single capture cannot see; the third is the course
contract, which is a promise rather than a state.

    A1  system parity. A page with no ``data-mode`` and the operating system
        asking for a mode computes exactly what the same page computes with that
        mode chosen explicitly. A failure means an explicit-choice selector or a
        system-preference rule is missing one of the two.
    A2  switch parity. A page loaded on one palette and mode and then switched
        to another computes exactly what the same page computes when loaded on
        that setting directly. A failure means a rule that only matches on the
        first paint, or one that only matches after a change.

    A3  the course contract. Two throwaway courses are registered in an injected
        stylesheet and worn in turn on one published page. A registration
        carrying only `--course-hue` moves the accent and nothing else; one
        carrying all seven author tokens moves the display face, the mono face
        and the eyebrow treatment and still nothing else; an unregistered course
        name changes nothing at all; the reader's two controls keep working
        underneath; and removing the block restores the page exactly. A failure
        means a token the documentation promises is a token no rule reads. It
        runs once, not per page, because it proves a mechanism rather than a
        page.

There is no dependency and no build. Chrome is driven over its own pipe
transport with the standard library alone: NUL-delimited JSON on file
descriptors 3 and 4.
"""

from __future__ import annotations

import argparse
import functools
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
WIDGETS: Path = REPO_ROOT / ".claude" / "skills" / "course-authoring" / "references" / "widgets.md"
SAMPLE_FILE: Path = REPO_ROOT / "scripts" / "style-sample.txt"
BASELINE_DIR: Path = REPO_ROOT / "scripts" / "style-baseline"
COVERAGE_FILE: Path = BASELINE_DIR / "COVERAGE.txt"

VIEWPORT: tuple[int, int] = (1280, 900)

PALETTES: tuple[str, ...] = ("paper", "slate", "ink", "sage", "harbor", "aubergine")
MODES: tuple[str, ...] = ("light", "dark")

# Every property that decides how a component looks, and nothing that follows
# the text. Grouped the way a reader of a diff wants to read it.
PROPERTIES: tuple[str, ...] = (
    # colour
    "color",
    "background-color",
    "border-top-color",
    "border-right-color",
    "border-bottom-color",
    "border-left-color",
    "outline-color",
    "text-decoration-color",
    "fill",
    "stroke",
    "box-shadow",
    "opacity",
    # type
    "font-family",
    "font-size",
    "font-style",
    "font-weight",
    "line-height",
    "letter-spacing",
    "text-align",
    "text-transform",
    "text-decoration-line",
    "white-space",
    # box
    "display",
    "position",
    "box-sizing",
    "max-width",
    "min-height",
    "margin-top",
    "margin-right",
    "margin-bottom",
    "margin-left",
    "padding-top",
    "padding-right",
    "padding-bottom",
    "padding-left",
    "border-top-width",
    "border-right-width",
    "border-bottom-width",
    "border-left-width",
    "border-top-style",
    "border-right-style",
    "border-bottom-style",
    "border-left-style",
    "border-top-left-radius",
    "border-top-right-radius",
    "border-bottom-right-radius",
    "border-bottom-left-radius",
    "column-gap",
    "row-gap",
    "grid-template-columns",
    "flex-direction",
    "align-items",
    "justify-content",
    "overflow-x",
    "overflow-y",
)

# Six properties inherit ``currentColor`` and almost always still hold it, so a
# palette change would otherwise write the same new colour seven times on one
# row. Folding them back to the keyword keeps the exactness - a border that
# stops following the text colour differs from the keyword and shows - and
# removes the repetition that would bury it.
CURRENT_COLOUR: tuple[str, ...] = (
    "border-top-color",
    "border-right-color",
    "border-bottom-color",
    "border-left-color",
    "outline-color",
    "text-decoration-color",
)

# A property sitting at the value it has everywhere carries no information about
# the component, and fifty-four of those per row would bury the dozen that do.
# Omitted from the recorded base row only; a delta always prints what it found,
# so a property that moves away from its quiet value, or back to it, is still a
# line in the diff.
QUIET: dict[str, str] = {
    "background-color": "rgba(0, 0, 0, 0)",
    "border-top-color": "currentcolor",
    "border-right-color": "currentcolor",
    "border-bottom-color": "currentcolor",
    "border-left-color": "currentcolor",
    "outline-color": "currentcolor",
    "text-decoration-color": "currentcolor",
    "fill": "rgb(0, 0, 0)",
    "stroke": "none",
    "box-shadow": "none",
    "opacity": "1",
    "font-style": "normal",
    "letter-spacing": "normal",
    "text-align": "start",
    "text-transform": "none",
    "text-decoration-line": "none",
    "white-space": "normal",
    "position": "static",
    "box-sizing": "border-box",
    "max-width": "none",
    "min-height": "auto",
    "margin-top": "0px",
    "margin-right": "0px",
    "margin-bottom": "0px",
    "margin-left": "0px",
    "padding-top": "0px",
    "padding-right": "0px",
    "padding-bottom": "0px",
    "padding-left": "0px",
    "border-top-width": "0px",
    "border-right-width": "0px",
    "border-bottom-width": "0px",
    "border-left-width": "0px",
    "border-top-style": "none",
    "border-right-style": "none",
    "border-bottom-style": "none",
    "border-left-style": "none",
    "border-top-left-radius": "0px",
    "border-top-right-radius": "0px",
    "border-bottom-right-radius": "0px",
    "border-bottom-left-radius": "0px",
    "column-gap": "normal",
    "row-gap": "normal",
    "grid-template-columns": "none",
    "flex-direction": "row",
    "align-items": "normal",
    "justify-content": "normal",
    "overflow-x": "visible",
    "overflow-y": "visible",
}

# Seven properties Chrome resolves from measured text rather than from what the
# stylesheet said. A grid track sized to its content, a margin written `auto`, a
# measure written in `ch`: all of them come back a fifth of a pixel different on
# a Linux runner than on a Mac, because the same font rasterises differently.
# The snapshot is committed and has to compare equal on both, so these are
# recorded to the nearest whole pixel - a hair finer than the smallest change
# anyone writes into a stylesheet, and coarser than the noise. Two values a
# pixel apart stay a pixel apart after rounding, so nothing the harness is for
# is lost. Everything else is recorded exactly, line height included.
MEASURED: frozenset[str] = frozenset(
    {
        "grid-template-columns",
        "margin-top",
        "margin-right",
        "margin-bottom",
        "margin-left",
        "max-width",
        "min-height",
    }
)

FRACTIONAL_PIXELS: re.Pattern[str] = re.compile(r"(\d+\.\d+)px")

HTML_BLOCK: re.Pattern[str] = re.compile(r"```html\n(?P<body>.*?)```", re.DOTALL)
CLASS_ATTRIBUTE: re.Pattern[str] = re.compile(r'class="(?P<names>[^"]+)"')
CLASS_NAME: re.Pattern[str] = re.compile(r"^[a-z][a-z0-9-]*$")

CHROME_CANDIDATES: tuple[str, ...] = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
)


# ============================================================
# The vocabulary and the sample
# ============================================================


@functools.lru_cache(maxsize=1)
def widget_vocabulary() -> tuple[str, ...]:
    """Every class name the widget reference prescribes, in one sorted tuple.

    The vocabulary is closed and documented, so coverage is a real check rather
    than a sample. Reading it from ``widgets.md`` rather than from a list here
    means the reference stays the single source of truth and drift in it shows
    up as a diff in the coverage file.
    """
    source = WIDGETS.read_text(encoding="utf-8")
    names: set[str] = set()
    for block in HTML_BLOCK.findall(source):
        for attribute in CLASS_ATTRIBUTE.findall(block):
            names.update(name for name in attribute.split() if CLASS_NAME.match(name))
    return tuple(sorted(names))


def documented_classes(page: Path) -> set[str]:
    """The documented classes a page carries, read out of its own markup."""
    present: set[str] = set()
    for attribute in CLASS_ATTRIBUTE.findall(page.read_text(encoding="utf-8", errors="replace")):
        present.update(attribute.split())
    return present & set(widget_vocabulary())


def course_directories() -> list[Path]:
    return sorted(
        entry
        for entry in REPO_ROOT.iterdir()
        if entry.is_dir() and not entry.name.startswith(".") and entry.name not in {"assets", "scripts"}
    )


def pick_sample() -> list[str]:
    """The fixed sample, picked by rule and then committed.

    One page per course folder, the hub index, the widest widget page in the
    repository, and then whatever page it takes to reach a documented class the
    rest of the sample misses. A course's representative is the page that
    exercises the most of the vocabulary, which is what makes one page per
    course worth loading. The three courses that ship a ``course-extras.css``
    are courses like any other and are therefore in by construction - a design
    block can out-specify a course sheet silently, so a diff on one of those
    pages is a question for the course owner rather than an automatic pass.
    """
    every: list[Path] = []
    for course in course_directories():
        every += [
            page
            for page in sorted(course.rglob("*.html"))
            if not any(part.startswith(".") for part in page.relative_to(REPO_ROOT).parts)
        ]
    carried = {page: documented_classes(page) for page in every}

    chosen: list[str] = ["index.html"]
    for course in course_directories():
        pages = [page for page in every if page.is_relative_to(course)]
        if not pages:
            continue
        widest = min(pages, key=lambda page: (-len(carried[page]), str(page)))
        chosen.append(str(widest.relative_to(REPO_ROOT)))

    widest_overall = str(min(every, key=lambda page: (-len(carried[page]), str(page))).relative_to(REPO_ROOT))
    if widest_overall not in chosen:
        chosen.append(widest_overall)

    # Whatever the per-course pick misses, the vocabulary is the authority: a
    # documented class that exists somewhere in the hub and on no sample page is
    # a class this gate cannot see, so the first page carrying it joins the
    # sample. The capability matrix arrives this way - it lives on one page of
    # one course and no widest-page rule would ever land on it.
    covered = {name for page in chosen for name in carried.get(REPO_ROOT / page, set())}
    for name in widget_vocabulary():
        if name in covered:
            continue
        holders = [page for page in every if name in carried[page]]
        if not holders:
            continue
        chosen.append(str(holders[0].relative_to(REPO_ROOT)))
        covered |= carried[holders[0]]
    return chosen


def read_sample() -> list[str]:
    if not SAMPLE_FILE.is_file():
        raise SystemExit(f"no sample manifest at {SAMPLE_FILE.relative_to(REPO_ROOT)}; run --refresh-sample")
    lines = [
        line.strip()
        for line in SAMPLE_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    missing = [line for line in lines if not (REPO_ROOT / line).is_file()]
    if missing:
        raise SystemExit("the sample names pages that are not on disk: " + ", ".join(missing))
    return lines


def sample_gaps(sample: list[str]) -> list[str]:
    """Courses the sample does not represent. A gap here is a hole in the gate."""
    represented = {Path(name).parts[0] for name in sample}
    return [course.name for course in course_directories() if course.name not in represented]


def write_sample(sample: list[str]) -> None:
    header = (
        "# The fixed sample the computed-style harness loads.\n"
        "#\n"
        "# One page per course folder, the hub index, the widest widget page in the\n"
        "# repository, and then whatever page it takes to reach a documented class\n"
        "# the rest of the sample misses. Picked by rule with --refresh-sample and\n"
        "# then committed, so a content edit never silently moves the sample under a\n"
        "# snapshot.\n"
        "#\n"
        "# Adding a course means refreshing this file. scripts/style_snapshot.py\n"
        "# refuses to run while a course folder is unrepresented.\n"
    )
    SAMPLE_FILE.write_text(header + "\n".join(sample) + "\n", encoding="utf-8")


# ============================================================
# Chrome, driven over its pipe transport
# ============================================================


class Chrome:
    """A headless Chrome and a CDP client, speaking NUL-delimited JSON on a pipe.

    The pipe transport is the reason there is no dependency here. The WebSocket
    endpoint would need a WebSocket client; the pipe needs ``os.read``. Chrome
    reads commands from file descriptor 3 and writes replies to descriptor 4, so
    the only trick is getting the two ends onto those numbers in the child.
    """

    def __init__(self, binary: str) -> None:
        self._profile = tempfile.mkdtemp(prefix="hub-style-harness-")
        command_read, self._command_write = os.pipe()
        self._reply_read, reply_write = os.pipe()

        def place_fds() -> None:
            # CPython runs this before it closes the fds it was not told to keep,
            # which is why 3 and 4 are in pass_fds as well as the pipe ends.
            os.dup2(command_read, 3)
            os.dup2(reply_write, 4)

        self._process = subprocess.Popen(
            [
                binary,
                "--headless=new",
                "--remote-debugging-pipe",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-gpu",
                "--hide-scrollbars",
                "--force-device-scale-factor=1",
                "--disable-lcd-text",
                "--font-render-hinting=none",
                f"--window-size={VIEWPORT[0]},{VIEWPORT[1]}",
                f"--user-data-dir={self._profile}",
                # Nothing but the loopback server answers, so the run is offline
                # and the Mermaid CDN can never make it flaky.
                "--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1",
                "about:blank",
            ]
            # Chrome's own sandbox refuses to start as root, which is what a
            # container build gets. A developer machine keeps it.
            + (["--no-sandbox"] if os.geteuid() == 0 else []),
            preexec_fn=place_fds,
            pass_fds=tuple(sorted({command_read, reply_write, 3, 4})),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
        )
        os.close(command_read)
        os.close(reply_write)

        self._buffer = b""
        self._sequence = 0
        self._events: list[dict] = []
        target = self.call("Target.createTarget", {"url": "about:blank"})
        self.session = self.call(
            "Target.attachToTarget", {"targetId": target["targetId"], "flatten": True}
        )["sessionId"]

    def _receive(self) -> dict:
        while b"\0" not in self._buffer:
            chunk = os.read(self._reply_read, 65536)
            if not chunk:
                raise RuntimeError("Chrome closed the devtools pipe")
            self._buffer += chunk
        raw, self._buffer = self._buffer.split(b"\0", 1)
        return json.loads(raw)

    def call(self, method: str, params: dict | None = None, session: str | None = None) -> dict:
        self._sequence += 1
        message: dict = {"id": self._sequence, "method": method, "params": params or {}}
        if session:
            message["sessionId"] = session
        os.write(self._command_write, json.dumps(message).encode("utf-8") + b"\0")
        while True:
            reply = self._receive()
            if reply.get("id") != self._sequence:
                self._events.append(reply)
                continue
            if "error" in reply:
                raise RuntimeError(f"{method}: {reply['error']}")
            return reply.get("result", {})

    def page(self, method: str, params: dict | None = None) -> dict:
        return self.call(method, params, self.session)

    def drain(self) -> None:
        """Forget the events queued so far.

        Every command reply that is not the one being waited for lands in the
        queue, so a load event from an earlier navigation is still sitting there
        when the next one starts. Waiting on that stale event would return
        before the new document existed and read the old page's styles into the
        new page's row - a wrong snapshot with nothing to see in it. Clearing
        the queue immediately before a navigation is what keeps the wait honest,
        and only one navigation is ever in flight.
        """
        self._events.clear()

    def await_event(self, method: str, timeout: float = 30.0) -> None:
        deadline = time.time() + timeout
        while True:
            for index, event in enumerate(self._events):
                if event.get("method") == method:
                    del self._events[index]
                    return
            if time.time() > deadline:
                raise RuntimeError(f"timed out waiting for {method}")
            self._events.append(self._receive())

    def evaluate(self, expression: str, timeout: float = 60.0) -> object:
        result = self.page(
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": True,
                "timeout": int(timeout * 1000),
            },
        )
        if "exceptionDetails" in result:
            raise RuntimeError(result["exceptionDetails"].get("text", "evaluation failed"))
        return result["result"].get("value")

    def close(self) -> None:
        try:
            self._process.terminate()
            self._process.wait(timeout=10)
        except Exception:
            self._process.kill()
        finally:
            os.close(self._command_write)
            os.close(self._reply_read)
            shutil.rmtree(self._profile, ignore_errors=True)


def find_chrome() -> str:
    named = os.environ.get("CHROME")
    if named:
        if Path(named).is_file() or shutil.which(named):
            return named
        raise SystemExit(f"CHROME is set to {named}, which is not an executable")
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).is_file():
            return candidate
        found = shutil.which(candidate)
        if found:
            return found
    raise SystemExit("no Chrome found; install one or set CHROME to its path")


def serve_repository() -> tuple[ThreadingHTTPServer, str]:
    """Serve the hub on the loopback address.

    ``file://`` gives every page its own opaque origin, so ``localStorage``
    raises there and ``hub.js`` would fall back to the default palette on every
    load. Over HTTP the head phase reads the seeded preference exactly as it
    does on the bucket.
    """

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args: object, **kwargs: object) -> None:
            super().__init__(*args, directory=str(REPO_ROOT), **kwargs)  # type: ignore[arg-type]

        def log_message(self, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


# ============================================================
# The probe
# ============================================================

PROBE = """
(function (classes, properties) {
  var shapeOf = function (node) {
    var own = Array.prototype.slice.call(node.classList).sort();
    return node.tagName.toLowerCase() + (own.length ? '.' + own.join('.') : '');
  };
  var out = {};
  for (var i = 0; i < classes.length; i++) {
    var nodes = document.getElementsByClassName(classes[i]);
    if (!nodes.length) continue;
    var byShape = {};
    for (var n = 0; n < nodes.length; n++) {
      var shape = shapeOf(nodes[n]);
      if (byShape[shape]) continue;
      var style = getComputedStyle(nodes[n]);
      var record = {};
      for (var p = 0; p < properties.length; p++) {
        record[properties[p]] = style.getPropertyValue(properties[p]).trim();
      }
      byShape[shape] = record;
    }
    out[classes[i]] = byShape;
  }
  return out;
})(%(classes)s, %(properties)s)
"""

SETTLE = """
(async function () {
  if (document.readyState !== 'complete') {
    await new Promise(function (done) { window.addEventListener('load', done, { once: true }); });
  }
  try { await document.fonts.ready; } catch (e) { /* no font loading API */ }
  await new Promise(function (done) { requestAnimationFrame(function () { requestAnimationFrame(done); }); });
  return document.documentElement.getAttribute('data-palette') + ' ' +
         (document.documentElement.getAttribute('data-mode') || '-');
})()
"""

SEED = """
try {
  localStorage.setItem('coursehub.mode', %(mode)s);
  localStorage.setItem('coursehub.palette', %(palette)s);
} catch (e) { /* storage blocked: the load below settles on the default and fails its own check */ }
"""

SWITCH = """
(async function (palette, mode) {
  var root = document.documentElement;
  var fingerprint = function () {
    var page = getComputedStyle(document.body);
    var tokens = getComputedStyle(root);
    return [page.color, page.backgroundColor, tokens.getPropertyValue('--ink'),
            tokens.getPropertyValue('--bg'), tokens.getPropertyValue('--accent')].join('|');
  };
  var before = fingerprint();
  root.setAttribute('data-palette', palette);
  if (mode) root.setAttribute('data-mode', mode); else root.removeAttribute('data-mode');
  for (var i = 0; i < 240; i++) {
    if (fingerprint() !== before) {
      await new Promise(function (done) {
        requestAnimationFrame(function () { requestAnimationFrame(done); });
      });
      return root.getAttribute('data-palette') + ' ' + (root.getAttribute('data-mode') || '-');
    }
    await new Promise(function (done) { setTimeout(done, 25); });
  }
  return 'no repaint';
})(%(palette)s, %(mode)s)
"""


CONTRACT = """
(async function () {
  var root = document.documentElement;
  var original = root.getAttribute('data-course');

  /* The fixture has to sit where a real registration sits, which is inside
     hub.css and therefore *before* everything the sheet declares after it. An
     injected <style> appended to the head is the last stylesheet in the
     document and wins every tie on source order, so a fixture placed there
     would pass while a real course registered in hub.css silently lost to a
     design block. Inserting it ahead of the sheet is if anything stricter than
     reality, so it can over-report and never under-report. */
  var sheet = document.createElement('style');
  sheet.id = '__course-contract-fixture';
  sheet.textContent =
    ':root[data-course="fixture-hue-only-course"] { --course-hue: 137; }' +
    ':root[data-course="fixture-full-course"] {' +
    '  --course-hue: -37;' +
    '  --font-display: var(--mono);' +
    '  --font-mono: var(--serif);' +
    '  --eyebrow-family: var(--serif);' +
    '  --eyebrow-tracking: .3em;' +
    '  --eyebrow-case: none;' +
    '  --eyebrow-size: .78rem;' +
    '}';

  /* Three probes in the closed vocabulary, so what is measured is the rule a
     page actually carries and not a token read back out of :root. The accent is
     read off the page's own wordmark, which is authored markup on every page. */
  var probe = document.createElement('div');
  probe.id = '__course-contract-probe';
  probe.innerHTML = '<p class="eyebrow">Course eyebrow</p><h1>Heading</h1><code>code</code>';
  document.body.appendChild(probe);

  var eyebrow = probe.querySelector('.eyebrow');
  var heading = probe.querySelector('h1');
  var code = probe.querySelector('code');
  var wordmark = document.querySelector('.spine .home');

  function settle() {
    return new Promise(function (done) {
      requestAnimationFrame(function () { requestAnimationFrame(done); });
    });
  }

  function readState() {
    var rootStyle = getComputedStyle(root);
    var eyebrowStyle = getComputedStyle(eyebrow);
    return {
      'accent': wordmark ? getComputedStyle(wordmark).color : 'no wordmark on this page',
      'display face': getComputedStyle(heading).fontFamily,
      'mono face': getComputedStyle(code).fontFamily,
      'eyebrow family': eyebrowStyle.fontFamily,
      'eyebrow size': eyebrowStyle.fontSize,
      'eyebrow tracking': eyebrowStyle.letterSpacing,
      'eyebrow case': eyebrowStyle.textTransform,
      'eyebrow weight': eyebrowStyle.fontWeight,
      'body face': getComputedStyle(document.body).fontFamily,
      'body size': getComputedStyle(document.body).fontSize,
      'measure': rootStyle.getPropertyValue('--measure').trim(),
      'measure characters': rootStyle.getPropertyValue('--measure-chars').trim(),
      'ui face': rootStyle.getPropertyValue('--font-ui').trim()
    };
  }

  async function underCourse(name) {
    if (name === null) root.removeAttribute('data-course');
    else root.setAttribute('data-course', name);
    await settle();
    return readState();
  }

  var states = {};
  states['house'] = await underCourse(original);
  states['no course'] = await underCourse(null);
  var rootSize = parseFloat(getComputedStyle(root).fontSize);

  var hub = document.querySelector('link[rel="stylesheet"][href*="hub.css"]');
  if (!hub) return { 'error': 'the page links no hub.css, so A3 cannot place its fixture' };
  hub.parentNode.insertBefore(sheet, hub);
  states['hue only'] = await underCourse('fixture-hue-only-course');
  states['seven tokens'] = await underCourse('fixture-full-course');
  states['unregistered'] = await underCourse('fixture-unregistered-course');

  /* The reader keeps every control while the course block is in force: a course
     writes none of the reader-reachable tokens, so nothing it declares can
     out-argue an inline --*-user property. */
  root.setAttribute('data-course', 'fixture-full-course');
  root.style.setProperty('--fs-body-user', '1.3125rem');
  root.style.setProperty('--measure-chars-user', '60');
  await settle();
  states['reader controls'] = readState();
  root.style.removeProperty('--fs-body-user');
  root.style.removeProperty('--measure-chars-user');

  sheet.remove();
  states['restored'] = await underCourse(original);
  probe.remove();

  return { 'states': states, 'rootSize': rootSize };
})()
"""

@dataclass(frozen=True)
class Difference:
    """One computed value that moved, named the way a fix needs it named."""

    page: str
    combination: str
    shape: str
    prop: str
    before: str
    after: str

    def render(self) -> str:
        return f"{self.page} [{self.combination}] {self.shape} {self.prop}: {self.before} -> {self.after}"


class Capture:
    """One headless browser, driving the whole matrix."""

    def __init__(self, chrome: Chrome, origin: str) -> None:
        self.chrome = chrome
        self.origin = origin
        self._seed_id: str | None = None
        chrome.page("Page.enable")
        chrome.page("Runtime.enable")
        chrome.page(
            "Emulation.setDeviceMetricsOverride",
            {"width": VIEWPORT[0], "height": VIEWPORT[1], "deviceScaleFactor": 1, "mobile": False},
        )
        self._probe = PROBE % {
            "classes": json.dumps(list(widget_vocabulary())),
            "properties": json.dumps(list(PROPERTIES)),
        }

    def emulate(self, scheme: str) -> None:
        self.chrome.page(
            "Emulation.setEmulatedMedia",
            {
                "media": "screen",
                "features": [
                    {"name": "prefers-color-scheme", "value": scheme},
                    # The reduced-motion block touches scroll behaviour and the
                    # two durations and nothing this harness records, so asking
                    # for it removes every transition without moving a value.
                    {"name": "prefers-reduced-motion", "value": "reduce"},
                    {"name": "forced-colors", "value": "none"},
                ],
            },
        )

    def seed(self, palette: str, mode: str) -> None:
        """Write the reader's preference before any page script runs."""
        if self._seed_id is not None:
            self.chrome.page("Page.removeScriptToEvaluateOnNewDocument", {"identifier": self._seed_id})
        source = SEED % {"mode": json.dumps(mode), "palette": json.dumps(palette)}
        self._seed_id = self.chrome.page(
            "Page.addScriptToEvaluateOnNewDocument", {"source": source}
        )["identifier"]

    def load(self, page: str, palette: str, mode: str) -> None:
        """Navigate, wait for the page to settle, and prove it is the state asked for.

        The axes are written onto ``<html>`` by the head phase from what was
        seeded, so reading them back is a cheap end-to-end check that the seed
        arrived, the navigation finished and the document being measured is the
        one intended. A harness that measures the wrong state silently is worse
        than no harness.
        """
        self.chrome.drain()
        self.chrome.page("Page.navigate", {"url": f"{self.origin}/{page}"})
        self.chrome.await_event("Page.loadEventFired")
        settled = str(self.chrome.evaluate(SETTLE))
        wanted = f"{palette} {mode or '-'}"
        if settled != wanted:
            raise RuntimeError(f"{page} settled as {settled}, expected {wanted}")

    def read(self, attempts: int = 16) -> dict[str, dict[str, dict[str, str]]]:
        """The whole page's computed styles, read only once the page has settled.

        A page keeps moving for a while after its load event - a web font
        arrives, a column is measured again - and a snapshot taken mid-move is a
        snapshot that will not reproduce. Two consecutive identical reads mean
        it has stopped. Every animation is already off, because the harness asks
        for reduced motion, so a page that never settles is a fault rather than
        a slow paint.

        Stability is not proof on its own, which is why ``switch`` waits for a
        positive signal instead: Chrome will hold the pre-switch values steadily
        enough that two agreeing reads say nothing at all.
        """
        previous: object = None
        for _ in range(attempts):
            value = normalise(self.chrome.evaluate(self._probe))
            if value == previous:
                return value
            previous = value
            self.chrome.evaluate(
                "new Promise(function (done) { setTimeout(function () "
                "{ requestAnimationFrame(done); }, 60); })"
            )
        raise RuntimeError(f"the page never settled: {attempts} reads and no two agreed")

    def switch(self, palette: str, mode: str) -> None:
        """Move the two axes on a page that is already open.

        This is what the appearance panel does: it writes the attributes onto
        ``<html>`` and lets the cascade do the rest.

        Knowing when the cascade has caught up is the hard part. Chrome will
        hand back the pre-switch computed values for a while after the attribute
        is set, and hold them steadily enough that two agreeing reads are not
        proof of anything. So the page itself waits for the ground and the ink
        to move before it reports back: every switch here changes both axes, so
        a fingerprint that has not changed means the repaint has not happened.
        """
        settled = self.chrome.evaluate(SWITCH % {"palette": json.dumps(palette), "mode": json.dumps(mode)})
        wanted = f"{palette} {mode or '-'}"
        if settled == "no repaint":
            raise RuntimeError(f"the page never repainted after switching to {wanted}")
        if settled != wanted:
            raise RuntimeError(f"the switch settled as {settled}, expected {wanted}")
        self.chrome.evaluate(
            "new Promise(function (done) { requestAnimationFrame(function () "
            "{ requestAnimationFrame(done); }); })"
        )


# ============================================================
# The snapshot file
# ============================================================


def baseline_path(page: str) -> Path:
    """The snapshot file for a page, mirroring the page's own path.

    One file per page rather than one file for the hub: a pull request that
    moves something on one page shows a diff on one file, and the file names
    the page without anyone having to read it.
    """
    return BASELINE_DIR / Path(page).with_suffix(".txt")


def normalise(captured: object) -> dict[str, dict[str, dict[str, str]]]:
    """One page's capture, with the platform's sub-pixel opinion taken out.

    Applied the moment the values leave the browser, so the snapshot, the two
    assertions and the settle comparison all read the same numbers.
    """
    assert isinstance(captured, dict)
    for shapes in captured.values():
        for record in shapes.values():
            for prop in MEASURED:
                record[prop] = FRACTIONAL_PIXELS.sub(
                    lambda found: f"{round(float(found.group(1)))}px", record[prop]
                )
    return captured


def fold(record: dict[str, str]) -> dict[str, str]:
    """One element's computed values, with the repetition taken out."""
    folded = dict(record)
    for prop in CURRENT_COLOUR:
        if folded[prop] == folded["color"]:
            folded[prop] = "currentcolor"
    return folded


def render_page_snapshot(page: str, captures: dict[str, dict[str, dict[str, str]]]) -> str:
    """One page's rows, base combination in full and the rest as deltas.

    The base carries every property it actually sets; every other combination
    carries only what the palette or the mode moved. A palette is a block of
    colour, so a delta row is a colour or two rather than fifty-four repeats,
    and the file stays something a reviewer can read in a pull request.
    """
    base_key = f"{PALETTES[0]} {MODES[0]}"
    lines = [
        f"# page: {page}",
        f"# viewport: {VIEWPORT[0]}x{VIEWPORT[1]} at device pixel ratio 1",
        f"# base: {base_key} in full; every other row lists only what moved from it",
        "",
    ]
    base = captures[base_key]
    for name in sorted(base):
        for shape in sorted(base[name]):
            record = fold(base[name][shape])
            body = "; ".join(
                f"{prop}={record[prop]}" for prop in PROPERTIES if record[prop] != QUIET.get(prop)
            )
            lines.append(f"{name} | {base_key} | {shape} | {body}")
            for palette in PALETTES:
                for mode in MODES:
                    key = f"{palette} {mode}"
                    if key == base_key:
                        continue
                    found = captures[key].get(name, {}).get(shape)
                    if found is None:
                        lines.append(f"{name} | {key} | {shape} | ABSENT")
                        continue
                    other = fold(found)
                    moved = [f"{prop}={other[prop]}" for prop in PROPERTIES if other[prop] != record[prop]]
                    lines.append(f"{name} | {key} | {shape} | " + ("; ".join(moved) if moved else "="))
    for key in sorted(captures):
        for name in sorted(captures[key]):
            for shape in sorted(captures[key][name]):
                if name not in base or shape not in base[name]:
                    lines.append(f"{name} | {key} | {shape} | ONLY-IN-THIS-COMBINATION")
    return "\n".join(lines) + "\n"


def render_coverage(sample: list[str], covered: dict[str, list[str]]) -> str:
    """Which of the documented vocabulary the sample actually exercises.

    A class nobody in the sample uses is a class this gate cannot see, so the
    gap is written down rather than left to be discovered. A change to the line
    for any class is a change in what is guarded, and it shows up as a diff.
    """
    vocabulary = widget_vocabulary()
    lines = [
        "# Coverage of the closed widget vocabulary by the harness sample.",
        "#",
        "# The vocabulary is read from",
        "# .claude/skills/course-authoring/references/widgets.md, which is the single",
        "# documented source. A class with no page beside it is styled by nothing this",
        "# gate can see; a class that loses its pages has stopped being used.",
        "#",
        f"# {len(sample)} sample pages, {len(vocabulary)} documented classes, "
        f"{len([name for name in vocabulary if covered.get(name)])} covered.",
        "",
    ]
    for name in vocabulary:
        pages = covered.get(name, [])
        lines.append(f"{name}: {len(pages)} page(s)" if pages else f"{name}: UNCOVERED")
    return "\n".join(lines) + "\n"


def compare(page: str, recorded: str, produced: str) -> list[Difference]:
    """Every row that moved, named by shape and property rather than by line number."""

    def rows(text: str) -> dict[tuple[str, str, str], str]:
        table: dict[tuple[str, str, str], str] = {}
        for line in text.splitlines():
            if not line or line.startswith("#"):
                continue
            name, combination, shape, body = (part.strip() for part in line.split("|", 3))
            table[(name, combination, shape)] = body
        return table

    def properties(body: str) -> dict[str, str]:
        if body in {"=", "ABSENT", "ONLY-IN-THIS-COMBINATION"}:
            return {"(row)": body}
        return dict(entry.split("=", 1) for entry in body.split("; ") if "=" in entry)

    before, after = rows(recorded), rows(produced)
    differences: list[Difference] = []
    for key in sorted(set(before) | set(after)):
        name, combination, shape = key
        if key not in after:
            differences.append(Difference(page, combination, f".{name} {shape}", "(row)", "recorded", "gone"))
            continue
        if key not in before:
            differences.append(Difference(page, combination, f".{name} {shape}", "(row)", "absent", "new"))
            continue
        old, new = properties(before[key]), properties(after[key])
        for prop in sorted(set(old) | set(new)):
            if old.get(prop, "(unset)") != new.get(prop, "(unset)"):
                differences.append(
                    Difference(
                        page,
                        combination,
                        f".{name} {shape}",
                        prop,
                        old.get(prop, "(unset)"),
                        new.get(prop, "(unset)"),
                    )
                )
    return differences


def diff_captures(
    page: str, combination: str, expected: dict, actual: dict
) -> list[Difference]:
    """Two captures of the same page compared directly, for A1 and A2."""
    differences: list[Difference] = []
    for name in sorted(set(expected) | set(actual)):
        shapes_expected, shapes_actual = expected.get(name, {}), actual.get(name, {})
        for shape in sorted(set(shapes_expected) | set(shapes_actual)):
            one, two = shapes_expected.get(shape), shapes_actual.get(shape)
            where = f".{name} {shape}"
            if one is None or two is None:
                differences.append(
                    Difference(
                        page,
                        combination,
                        where,
                        "(row)",
                        "present" if one else "absent",
                        "absent" if one else "present",
                    )
                )
                continue
            for prop in PROPERTIES:
                if one[prop] != two[prop]:
                    differences.append(Difference(page, combination, where, prop, one[prop], two[prop]))
    return differences


# ============================================================
# The run
# ============================================================


def capture_page(capture: Capture, page: str, assertions: bool) -> tuple[dict, list[Difference]]:
    """Every combination for one page, plus the two render-state assertions."""
    captures: dict[str, dict] = {}
    findings: list[Difference] = []

    for palette in PALETTES:
        for mode in MODES:
            # The demanding state: the reader chose, and the operating system
            # asks for the other one.
            capture.emulate("dark" if mode == "light" else "light")
            capture.seed(palette, mode)
            capture.load(page, palette, mode)
            captures[f"{palette} {mode}"] = capture.read()

    if not assertions:
        return captures, findings

    # A1: no stored choice, the operating system asking, must equal the choice.
    for palette in PALETTES:
        for mode in MODES:
            capture.emulate(mode)
            capture.seed(palette, "")
            capture.load(page, palette, "")
            findings += [
                Difference(page, f"A1 {palette} {mode}", d.shape, d.prop, d.before, d.after)
                for d in diff_captures(page, "", captures[f"{palette} {mode}"], capture.read())
            ]

    # A2: loaded on one setting and then switched to another, must equal the
    # page loaded on that setting directly. Every iteration starts from a fresh
    # load on a different palette and the other mode, so the switch always moves
    # both axes and never measures a no-op.
    #
    # The operating system's preference is held still for the whole assertion.
    # Chrome applies a media emulation well after it acknowledges the command,
    # and a style read inside that window comes back half old, so the fewer
    # times it moves the better. Holding it still costs nothing here: every row
    # this compares against was captured with the mode chosen explicitly, and
    # the recorded matrix has already proved that an explicit choice beats the
    # system asking for the other one.
    capture.emulate("dark")
    for index, palette in enumerate(PALETTES):
        for mode in MODES:
            other_palette = PALETTES[(index + 1) % len(PALETTES)]
            other_mode = MODES[0] if mode == MODES[1] else MODES[1]
            capture.seed(other_palette, other_mode)
            capture.load(page, other_palette, other_mode)
            capture.switch(palette, mode)
            findings += [
                Difference(page, f"A2 {palette} {mode}", d.shape, d.prop, d.before, d.after)
                for d in diff_captures(page, "", captures[f"{palette} {mode}"], capture.read())
            ]
    return captures, findings


def contract_page(sample: list[str]) -> str:
    """The page A3 runs on: the first lesson in the sample.

    A lesson rather than a course map, because the wordmark A3 reads the accent
    from is authored into every lesson's spine, and because a lesson is what a
    reader of a course actually holds open.
    """
    for page in sample:
        if "/lessons/" in page:
            return page
    raise RuntimeError("the sample contains no lesson page, so A3 has nothing to run on")


def _near(measured: str, expected: float) -> bool:
    """Two lengths in px agree to the hundredth, which is finer than any paint."""
    try:
        return abs(float(measured.replace("px", "")) - expected) < 0.01
    except ValueError:
        return False


@dataclass(frozen=True)
class Claim:
    """One thing A3 asserts about one registration.

    Most claims are an equality: this property computes exactly that value.
    A few are the opposite - the accent has to *move*, and a registration that
    changed nothing would be a passing test of a broken mechanism - so the
    direction is a field rather than a convention in the expected string.
    """

    state: str
    prop: str
    expected: str
    measured: str
    must_differ: bool = False

    def holds(self) -> bool:
        if self.must_differ:
            return self.measured != self.expected
        if self.measured == self.expected:
            return True
        return self.expected.endswith("px") and _near(self.measured, float(self.expected[:-2]))

    def as_difference(self, page: str) -> Difference:
        wanted = f"anything but {self.expected}" if self.must_differ else self.expected
        return Difference(page, f"A3 {self.state}", "the registration", self.prop, wanted, self.measured)


def _unchanged(state: str, house: dict[str, str], measured: dict[str, str], *, except_for: str) -> list[Claim]:
    """Every property but one computes what the house computes."""
    return [
        Claim(state, prop, value, measured[prop])
        for prop, value in sorted(house.items())
        if prop != except_for
    ]


def _contract_claims(states: dict[str, dict[str, str]], root_size: float) -> list[Claim]:
    """Every claim A3 makes.

    The two faces and the eyebrow family are compared against another face the
    same page already computes, rather than against a font name, so the
    assertion keeps holding when the registry changes what a role points at.
    """
    house = states["house"]
    full = states["seven tokens"]
    size = 0.78 * root_size

    # A hue on its own moves the accent and nothing else. That is the whole
    # promise of the cheapest registration there is.
    claims = [Claim("hue only", "accent", house["accent"], states["hue only"]["accent"], must_differ=True)]
    claims += _unchanged("hue only", house, states["hue only"], except_for="accent")

    # All seven: the three faces and the eyebrow move, and the four values a
    # course may never reach do not.
    claims += [
        Claim("seven tokens", "accent", house["accent"], full["accent"], must_differ=True),
        Claim("seven tokens", "display face", house["mono face"], full["display face"]),
        Claim("seven tokens", "mono face", house["body face"], full["mono face"]),
        Claim("seven tokens", "eyebrow family", house["body face"], full["eyebrow family"]),
        Claim("seven tokens", "eyebrow size", f"{size:.4g}px", full["eyebrow size"]),
        Claim("seven tokens", "eyebrow tracking", f"{0.3 * size:.4g}px", full["eyebrow tracking"]),
        Claim("seven tokens", "eyebrow case", "none", full["eyebrow case"]),
        # Not on the author surface, so a course must not be able to move it.
        Claim("seven tokens", "eyebrow weight", house["eyebrow weight"], full["eyebrow weight"]),
        Claim("seven tokens", "body face", house["body face"], full["body face"]),
        Claim("seven tokens", "body size", house["body size"], full["body size"]),
        Claim("seven tokens", "measure", house["measure"], full["measure"]),
        Claim("seven tokens", "ui face", house["ui face"], full["ui face"]),
    ]

    # A course folder nobody registered is dull, never broken: it wears the
    # palette accent unrotated, which is what a page with no course wears.
    claims.append(
        Claim("unregistered", "accent", states["no course"]["accent"], states["unregistered"]["accent"])
    )
    claims += _unchanged("unregistered", house, states["unregistered"], except_for="accent")

    # A course declares none of the reader-reachable tokens, so the reader keeps
    # every control while a course block is in force.
    #
    # Both are written the way the panel writes them: the body size in rem, on
    # the reference scale the stylesheet's own default uses, and the measure in
    # real characters. The measure is asserted on --measure-chars rather than on
    # the width it derives, so the claim stays about the reader's number
    # reaching the token and does not also restate the face's advance constant,
    # which `scripts/type_invariants.py` is the guard on.
    claims += [
        Claim("reader controls", "body size", "21px", states["reader controls"]["body size"]),
        Claim("reader controls", "measure characters", "60", states["reader controls"]["measure characters"]),
    ]

    # Removing the block restores the page exactly. The kill switch is lossless.
    claims += [
        Claim("restored", prop, value, states["restored"][prop]) for prop, value in sorted(house.items())
    ]
    return claims


def assert_course_contract(capture: Capture, page: str) -> list[Difference]:
    """A3: the course contract, proved on a published page.

    ``scripts/validate_site.py`` checks that a registration is well formed. It
    cannot see what the browser then does with it, which is the half that
    matters: a token nothing reads is a token that documents a promise the sheet
    does not keep. So A3 registers two throwaway courses in a stylesheet it
    injects, wears each one in turn, and reads the result off three probes in
    the closed vocabulary plus the page's own wordmark.

    Nothing here is stored. The fixture is removed before the assertion ends and
    the page is left exactly as it was found, which the ``restored`` state
    proves rather than assumes.
    """
    capture.emulate("dark")
    capture.seed(PALETTES[0], MODES[0])
    capture.load(page, PALETTES[0], MODES[0])
    measured = capture.chrome.evaluate(CONTRACT)
    if not isinstance(measured, dict):
        raise RuntimeError("A3 read nothing back from the page")

    if "error" in measured:
        raise RuntimeError(f"A3 on {page}: {measured['error']}")

    states = measured["states"]
    if states["house"]["accent"].startswith("no wordmark"):
        raise RuntimeError(f"A3 needs a page with a .spine .home wordmark; {page} has none")

    return [
        claim.as_difference(page)
        for claim in _contract_claims(states, measured["rootSize"])
        if not claim.holds()
    ]


def run(write: bool, assertions: bool) -> int:
    sample = read_sample()
    gaps = sample_gaps(sample)
    if gaps:
        print("the sample does not represent every course: " + ", ".join(gaps))
        print("run: python3 scripts/style_snapshot.py --refresh-sample")
        return 1

    started = time.time()
    server, origin = serve_repository()
    chrome = Chrome(find_chrome())
    covered: dict[str, list[str]] = {}
    moved: list[Difference] = []
    failed_assertions: list[Difference] = []

    try:
        capture = Capture(chrome, origin)
        for page in sample:
            captures, findings = capture_page(capture, page, assertions)
            failed_assertions += findings
            for name in captures[f"{PALETTES[0]} {MODES[0]}"]:
                covered.setdefault(name, []).append(page)

            produced = render_page_snapshot(page, captures)
            target = baseline_path(page)
            if write:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(produced, encoding="utf-8")
            elif not target.is_file():
                moved.append(Difference(page, "-", "-", "(page)", "no recorded snapshot", "captured"))
            else:
                moved += compare(page, target.read_text(encoding="utf-8"), produced)
            print(f"  {page}", flush=True)

        # A3 runs once rather than per page: it proves a mechanism, not a
        # page, and a mechanism proved twenty-two times is nineteen minutes
        # spent on the same answer.
        if assertions:
            failed_assertions += assert_course_contract(capture, contract_page(sample))
    finally:
        chrome.close()
        server.shutdown()

    coverage = render_coverage(sample, covered)
    if write:
        COVERAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
        COVERAGE_FILE.write_text(coverage, encoding="utf-8")
        prune(sample)
    elif not COVERAGE_FILE.is_file() or COVERAGE_FILE.read_text(encoding="utf-8") != coverage:
        moved.append(
            Difference("scripts/style-baseline/COVERAGE.txt", "-", "-", "(coverage)", "recorded", "changed")
        )

    elapsed = time.time() - started
    print(
        f"\n{len(sample)} page(s) x {len(PALETTES)} palettes x {len(MODES)} modes "
        f"in {elapsed:.0f}s"
    )

    if write:
        print(f"snapshot written to {BASELINE_DIR.relative_to(REPO_ROOT)}")
    elif moved:
        report("the computed style moved", moved)
    else:
        print("nothing moved.")

    # The assertions are never stored, so they fail a write exactly as they fail
    # a comparison. A snapshot recorded while one of them is red would record the
    # defect as the expected answer.
    if failed_assertions:
        report("a render state disagrees with the recorded one", failed_assertions)
    return 1 if moved or failed_assertions else 0


def prune(sample: list[str]) -> None:
    """Drop snapshots for pages the sample no longer names.

    A refreshed sample would otherwise leave the old page's file behind, and a
    snapshot nothing compares against is a file that rots quietly.
    """
    kept = {baseline_path(page) for page in sample} | {COVERAGE_FILE}
    for recorded in sorted(BASELINE_DIR.rglob("*.txt")):
        if recorded not in kept:
            recorded.unlink()
    for directory in sorted(BASELINE_DIR.rglob("*"), reverse=True):
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()


def report(headline: str, differences: list[Difference], limit: int = 200) -> None:
    print(f"\n{headline}, in {len(differences)} place(s):\n")
    for difference in differences[:limit]:
        print(f"  - {difference.render()}")
    if len(differences) > limit:
        print(f"  ... and {len(differences) - limit} more")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--write", action="store_true", help="record a new snapshot instead of comparing")
    parser.add_argument("--refresh-sample", action="store_true", help="re-pick the sample pages by rule")
    parser.add_argument("--sample-only", action="store_true", help="print the sample and stop")
    parser.add_argument(
        "--no-assertions",
        action="store_true",
        help="skip the A1 and A2 render-state assertions (they are two thirds of the run)",
    )
    arguments = parser.parse_args()

    if arguments.refresh_sample:
        sample = pick_sample()
        write_sample(sample)
        print(f"{SAMPLE_FILE.relative_to(REPO_ROOT)}: {len(sample)} page(s)")
        return 0
    if arguments.sample_only:
        for page in read_sample():
            print(page)
        return 0
    return run(write=arguments.write, assertions=not arguments.no_assertions)


if __name__ == "__main__":
    sys.exit(main())
