#!/usr/bin/env python3
"""Check C7: the derived type axes hold, for every registered reading face.

``scripts/style_snapshot.py`` proves that a change moved nothing. It cannot
prove that a *constant* is right, because a wrong constant is stable and a
stable wrong value is exactly what a snapshot agrees with. This can. It drives
the same headless Chrome, sets each registered face in turn, and measures what
the page actually renders against the two invariants the framework states.

    python3 scripts/type_invariants.py            # run every check
    python3 scripts/type_invariants.py --report   # print the measured tables too

Exit code 0 means every check passed. Exit code 1 names each failure.

Six things worth knowing before reading the code.

*The registry is parsed out of the stylesheet, not listed here.* A face is a
family plus three measured constants - the average prose advance, the x-height
per em and the apparent-size factor - and the derivations cannot compute
without all three. So the static half of this script reads every rule in
``assets/hub.css`` that declares ``--font-body`` and fails on one that is not a
``data-body-face`` entry carrying the other three. A face cannot be half
registered, which is the whole point of calling it a registry.

*The advance is measured from rendered ink, not from a font table.* A fixed
corpus of real hub prose is laid out in the reading column; every full line's
rendered ink width is summed and divided by the characters on those lines. The
corpus is committed beside this script, so the number does not drift when a
lesson is edited. Three published figures for Source Serif 4's advance disagree
- .4065, .4366 and .4619 - which is why the framework measures it and then
proves it rather than picking one.

*Invariant M1 is what settles that disagreement.* For every registered face, at
the default body size, ``--measure-chars: N`` must realise N plus or minus one
characters, for N in 55, 68, 80 and 85. The realised count is the column width
divided by the measured advance, which is how the research measured it and what
makes the check a comparison of a committed constant against a live rendering.
A face whose constant fails M1 is not registered.

*Invariant M2 holds a band, not a point.* ``--fs-mono`` over ``--fs-body`` must
sit inside .85 to .90 against a serif reading face, at every body size the
reader panel will offer. The ends of that band are measured; the point inside
it is judgement, so the check holds the ends.

*Only what is definite is gated.* Every gate here is a layout measurement or a
CSS computation, because those travel: the same prose lays out to an advance
that agrees in the fifth decimal on a Mac and on a Linux runner. Font-metric
lookups do not travel. The same woff2 file gives Source Serif 4 an x-height of
.4520 em through CSS ``1ex`` on a Mac and .4753 on a Linux runner, five per
cent apart, so a check built on one of those would go red for the machine
rather than for the stylesheet. Apparent size is therefore measured by drawing
the glyphs and reading the pixels back, and it is **printed rather than
asserted**: the apparent-size factor is a judgement built on two measurements,
and the specification says to look at it on a canvas rather than trust it
blind. What is gated instead is that the registered factor is the one the page
applied, which is exact.

*The last check removes the script.* Every derivation is pure CSS on purpose,
so the page has to be correct with ``hub.js`` blocked outright. The four
derived tokens are read back off a page served without it and must equal what
the same page computes with it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from style_snapshot import (  # noqa: E402
    Chrome,
    REPO_ROOT,
    find_chrome,
    serve_repository,
)

CORPUS_FILE: Path = REPO_ROOT / "scripts" / "type-corpus.txt"
STYLESHEET: Path = REPO_ROOT / "assets" / "hub.css"

# A lesson page rather than an index: it carries running prose in the reading
# column, which is what the measure is for, and it is already in the harness
# sample so a change to it is noticed by two checks rather than one.
PAGE: str = "production-systems-course/lessons/0005-distributed-data.html"

# Every property a registry entry must declare. The family alone is not a face.
REGISTRY_TOKENS: tuple[str, ...] = (
    "--font-body",
    "--face-advance",
    "--face-size-factor",
    "--xh-body",
)

# Invariant M1: the character counts the measure control will offer, at its ends
# and at the two recommended defaults.
M1_COUNTS: tuple[int, ...] = (55, 68, 80, 85)
M1_TOLERANCE: float = 1.0

# Invariant M2: the mono-to-prose band, measured against a serif reading face.
M2_BAND: tuple[float, float] = (0.85, 0.90)
M2_SIZES: tuple[int, ...] = (16, 19, 22, 25, 28)

# The reflow matrix, re-run rather than assumed. Both viewports, both ends of
# both ranges, and the two ends together.
REFLOW_VIEWPORTS: tuple[int, ...] = (1440, 320)
REFLOW_CELLS: tuple[tuple[int | None, int | None], ...] = (
    (None, None),
    (16, None),
    (28, None),
    (None, 55),
    (None, 85),
    (28, 85),
)

BLOCK: re.Pattern[str] = re.compile(r"(?P<selector>[^{}]+)\{(?P<body>[^{}]*)\}")
FACE_VALUE: re.Pattern[str] = re.compile(r'data-body-face="(?P<face>[a-z-]+)"')


# ============================================================
# The static half: is every face fully registered?
# ============================================================


def strip_comments(source: str) -> str:
    return re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)


def registry() -> tuple[dict[str, dict[str, str]], list[str]]:
    """The registered faces, and every complaint about how they are declared.

    A rule that declares ``--font-body`` is claiming to be a registry entry, so
    it is held to the whole contract: it must select on ``data-body-face`` and
    it must declare all four properties. That is the mechanical form of "a face
    is a name plus three measured constants", and it is what stops a design
    block moving the reading face without the numbers that follow it.
    """
    source = strip_comments(STYLESHEET.read_text(encoding="utf-8"))
    faces: dict[str, dict[str, str]] = {}
    complaints: list[str] = []
    for match in BLOCK.finditer(source):
        body = match.group("body")
        if "--font-body:" not in body:
            continue
        selector = " ".join(match.group("selector").split())
        declared = {
            name: value.strip()
            for name, value in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", body)
        }
        missing = [token for token in REGISTRY_TOKENS if token not in declared]
        if missing:
            complaints.append(
                f"{selector} sets --font-body without {', '.join(missing)}: "
                "a face is a name plus three measured constants"
            )
            continue
        names = FACE_VALUE.findall(selector)
        if not names:
            complaints.append(
                f"{selector} sets --font-body but selects on no data-body-face value, "
                "so no control can ever reach it"
            )
            continue
        for name in names:
            faces[name] = {token: declared[token] for token in REGISTRY_TOKENS}
    if not faces:
        complaints.append("no reading face is registered at all")
    return faces, complaints


# ============================================================
# The browser half
# ============================================================

MEASURE = r"""
(async function (corpus, faces, counts, sizes) {
  var root = document.documentElement;
  var main = document.querySelector('main.wrap') || document.querySelector('main');

  var probe = document.createElement('p');
  probe.style.cssText = 'margin:0;padding:0;hyphens:none;max-width:none;position:absolute;' +
                        'visibility:hidden;left:-99999px;top:0';
  probe.textContent = corpus;
  main.appendChild(probe);

  var pre = document.createElement('pre');
  pre.textContent = 'x';
  main.appendChild(pre);

  var settle = function () {
    return new Promise(function (done) {
      requestAnimationFrame(function () { requestAnimationFrame(done); });
    });
  };

  /* The average rendered advance of a prose character, in px.

     Every line but the last is a full line, so its ink width divided by its
     characters is one sample of the advance. Summing both sides across all of
     them rather than averaging the per-line ratios weights each line by how
     much text it holds, which is what "average prose advance" means. Trailing
     whitespace is dropped because it is not ink; a collapsed space returns no
     client rect at all and is carried to the end of the line it closes. */
  var advanceAt = function (widthPx) {
    probe.style.width = widthPx + 'px';
    var node = probe.firstChild, text = node.textContent;
    var range = document.createRange();
    var lines = [], top = null, chars = '', left = 0, right = 0;
    var close = function () { lines.push({ text: chars, ink: right - left }); };
    for (var i = 0; i < text.length; i++) {
      range.setStart(node, i);
      range.setEnd(node, i + 1);
      var rects = range.getClientRects();
      if (!rects.length) { chars += text[i]; continue; }
      var rect = rects[0];
      var y = Math.round(rect.top * 4) / 4;
      if (top === null) { top = y; left = rect.left; right = rect.right; }
      if (Math.abs(y - top) > 0.5) {
        close();
        chars = ''; top = y; left = rect.left; right = rect.right;
      }
      chars += text[i];
      if (rect.right > right) right = rect.right;
      if (rect.left < left) left = rect.left;
    }
    close();
    lines.pop();                                  // the last line is not full
    var characters = 0, ink = 0;
    lines.forEach(function (line) {
      characters += line.text.replace(/\s+$/, '').length;
      ink += line.ink;
    });
    return { advance: ink / characters, lines: lines.length };
  };

  /* The rendered width of the reading column, which is what --measure resolves
     to after the clamp that keeps it inside the viewport. Read off a real
     paragraph rather than off the token, so the number is what a reader sees. */
  var columnWidth = function () {
    var para = main.querySelector('p');
    return para.getBoundingClientRect().width;
  };

  /* The two halves of apparent size, measured by drawing the glyphs and
     reading the pixels back.

     Not from `1ex`, and not from canvas `actualBoundingBox`. Both are
     font-metric lookups and neither is portable: for the same woff2 file, a
     Mac reads Source Serif 4's x-height as .4520 em and a Linux CI runner
     reads .4753, five per cent apart, while the same two machines lay the same
     prose out to an advance that agrees in the fifth decimal. Layout travels;
     metric tables do not. A pixel readback measures what was actually drawn,
     and on the machine where the two can be compared it agrees with `1ex` to
     .1 per cent. */
  var readback = function (stack, text, size) {
    var side = size * 3;
    var canvas = document.createElement('canvas');
    canvas.width = side;
    canvas.height = side;
    var context = canvas.getContext('2d', { willReadFrequently: true });
    context.clearRect(0, 0, side, side);
    context.fillStyle = '#000';
    context.textBaseline = 'alphabetic';
    context.font = size + 'px ' + stack;
    context.fillText(text, size * 0.1, size * 1.8);
    var pixels = context.getImageData(0, 0, side, side).data;
    var top = -1, bottom = -1;
    for (var y = 0; y < side; y++) {
      for (var x = 0; x < side; x++) {
        if (pixels[(y * side + x) * 4 + 3] > 128) {
          if (top < 0) top = y;
          bottom = y;
          break;
        }
      }
    }
    return top < 0 ? 0 : (bottom - top + 1) / size;
  };

  var apparent = function () {
    var body = getComputedStyle(document.body);
    var size = parseFloat(body.fontSize);
    var xHeight = readback(body.fontFamily, 'x', 400) * size;
    var inkExtent = readback(body.fontFamily, 'Hxpdbq', 400) * size;
    return {
      size: size,
      xHeight: xHeight,
      inkExtent: inkExtent,
      parity: Math.sqrt(xHeight * inkExtent)
    };
  };

  var out = { faces: {} };

  for (var f = 0; f < faces.length; f++) {
    var face = faces[f];
    root.setAttribute('data-body-face', face);
    await document.fonts.ready;
    await settle();

    var record = { family: getComputedStyle(document.body).fontFamily.split(',')[0].trim() };
    record.apparent = apparent();
    record.declaredAdvance = parseFloat(getComputedStyle(root).getPropertyValue('--face-advance'));

    /* M1. Set the count the control will set, and measure what the column
       realises. Nothing here reads the token back: the point is to compare a
       committed constant against a rendering, so a token that agrees with
       itself proves nothing. */
    record.m1 = [];
    for (var c = 0; c < counts.length; c++) {
      root.style.setProperty('--measure-chars-user', String(counts[c]));
      await settle();
      var width = columnWidth();
      var measured = advanceAt(width);
      record.m1.push({
        asked: counts[c],
        columnPx: width,
        advanceEm: measured.advance / record.apparent.size,
        realised: width / measured.advance,
        lines: measured.lines
      });
    }
    root.style.removeProperty('--measure-chars-user');
    await settle();

    /* M2. The mono size is derived, so it moves with both the face and the
       reader's body size; the band has to hold across the whole control. */
    record.m2 = [];
    for (var s = 0; s < sizes.length; s++) {
      root.style.setProperty('--fs-body-user', sizes[s] + 'px');
      await settle();
      var bodyPx = parseFloat(getComputedStyle(document.body).fontSize);
      var monoPx = parseFloat(getComputedStyle(pre).fontSize);
      record.m2.push({ asked: sizes[s], bodyPx: bodyPx, monoPx: monoPx, ratio: monoPx / bodyPx });
    }
    root.style.removeProperty('--fs-body-user');
    await settle();

    out.faces[face] = record;
  }

  root.removeAttribute('data-body-face');
  probe.remove();
  pre.remove();
  return JSON.stringify(out);
})
"""

REFLOW = r"""
(async function (cells) {
  var root = document.documentElement;
  var settle = function () {
    return new Promise(function (done) {
      requestAnimationFrame(function () { requestAnimationFrame(done); });
    });
  };
  /* A broken box is one whose ink leaves the viewport on the right. An element
     inside something that scrolls sideways on purpose - a wide table, a code
     block - is not broken, so the walk stops at the first scrolling ancestor. */
  var broken = function () {
    var limit = document.documentElement.clientWidth + 1;
    var count = 0;
    var nodes = document.body.querySelectorAll('*');
    outer:
    for (var i = 0; i < nodes.length; i++) {
      var node = nodes[i];
      var rect = node.getBoundingClientRect();
      if (rect.width === 0 || rect.right <= limit) continue;
      for (var up = node.parentElement; up && up !== document.body; up = up.parentElement) {
        var overflow = getComputedStyle(up).overflowX;
        if (overflow === 'auto' || overflow === 'scroll' || overflow === 'hidden') continue outer;
      }
      count += 1;
    }
    return count;
  };
  var out = [];
  for (var i = 0; i < cells.length; i++) {
    var cell = cells[i];
    if (cell[0] === null) root.style.removeProperty('--fs-body-user');
    else root.style.setProperty('--fs-body-user', cell[0] + 'px');
    if (cell[1] === null) root.style.removeProperty('--measure-chars-user');
    else root.style.setProperty('--measure-chars-user', String(cell[1]));
    await settle();
    out.push({
      size: cell[0], chars: cell[1],
      overflow: Math.max(0, root.scrollWidth - root.clientWidth),
      broken: broken()
    });
  }
  root.style.removeProperty('--fs-body-user');
  root.style.removeProperty('--measure-chars-user');
  return JSON.stringify(out);
})
"""

DERIVED = r"""
(async function () {
  try { await document.fonts.ready; } catch (e) { /* no font loading API */ }
  await new Promise(function (done) {
    requestAnimationFrame(function () { requestAnimationFrame(done); });
  });
  var main = document.querySelector('main.wrap') || document.querySelector('main');
  /* Not every lesson carries a code block, and this read has to compare the
     mono size on both sides, so it brings its own. */
  var pre = main.appendChild(document.createElement('pre'));
  pre.textContent = 'x';
  var tokens = getComputedStyle(document.documentElement);
  var body = getComputedStyle(document.body);
  var out = {
    /* The outline rail is built by hub.js and exists in no page's source, so
       it is the honest answer to "did the script run". The spine is authored
       markup and would say yes either way. */
    scripted: !!document.getElementById('rail'),
    fontFamily: body.fontFamily,
    fontSize: body.fontSize,
    lineHeight: body.lineHeight,
    monoSize: getComputedStyle(pre).fontSize,
    column: main.querySelector('p').getBoundingClientRect().width.toFixed(2),
    measureChars: tokens.getPropertyValue('--measure-chars').trim(),
    faceAdvance: tokens.getPropertyValue('--face-advance').trim()
  };
  pre.remove();
  return JSON.stringify(out);
})()
"""


class Session:
    """One headless Chrome, one page, and the three measurements taken on it."""

    def __init__(self, chrome: Chrome, origin: str) -> None:
        self.chrome = chrome
        self.origin = origin
        self._seed: str | None = None
        chrome.page("Page.enable")
        chrome.page("Runtime.enable")
        chrome.page("Network.enable")

    def viewport(self, width: int, height: int = 900) -> None:
        self.chrome.page(
            "Emulation.setDeviceMetricsOverride",
            {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": False},
        )

    def block(self, patterns: list[str]) -> None:
        self.chrome.page("Network.setBlockedURLs", {"urls": patterns})

    def seed_face(self, face: str | None) -> None:
        """Choose the reading face before the first paint, the way a panel would."""
        if self._seed is not None:
            self.chrome.page("Page.removeScriptToEvaluateOnNewDocument", {"identifier": self._seed})
            self._seed = None
        if face is None:
            return
        # A document-start script runs before <html> exists, so it waits for it
        # rather than assuming it. That lands the attribute at the same moment
        # hub.js's head phase lands data-mode and data-palette: before the first
        # paint, and before any rule has been resolved against the old value.
        source = (
            "(function () {"
            "  var apply = function () {"
            "    if (!document.documentElement) return false;"
            f"    document.documentElement.setAttribute('data-body-face', {face!r});"
            "    return true;"
            "  };"
            "  if (apply()) return;"
            "  var watch = new MutationObserver(function () { if (apply()) watch.disconnect(); });"
            "  watch.observe(document, { childList: true, subtree: true });"
            "})();"
        )
        self._seed = self.chrome.page(
            "Page.addScriptToEvaluateOnNewDocument", {"source": source}
        )["identifier"]

    def load(self) -> None:
        self.chrome.drain()
        self.chrome.page("Page.navigate", {"url": f"{self.origin}/{PAGE}"})
        self.chrome.await_event("Page.loadEventFired")
        self.chrome.evaluate(
            "(async function () {"
            "  try { await document.fonts.ready; } catch (e) {}"
            "  await new Promise(function (d) {"
            "    requestAnimationFrame(function () { requestAnimationFrame(d); }); });"
            "})()"
        )

    def call(self, function: str, *arguments: object) -> object:
        payload = ", ".join(json.dumps(argument) for argument in arguments)
        return json.loads(str(self.chrome.evaluate(f"{function}({payload})")))


# ============================================================
# The checks
# ============================================================


def check_m1(faces: dict[str, dict], report: bool) -> list[str]:
    failures: list[str] = []
    for name, record in faces.items():
        if report:
            print(f"\n  M1  {name} ({record['family']}), advance {record['declaredAdvance']}")
            print("      asked  column px  measured advance  realised  error")
        for row in record["m1"]:
            error = row["realised"] - row["asked"]
            if report:
                print(
                    f"      {row['asked']:>5}  {row['columnPx']:>9.2f}"
                    f"  {row['advanceEm']:>16.5f}  {row['realised']:>8.2f}  {error:>+6.2f}"
                )
            if abs(error) > M1_TOLERANCE:
                failures.append(
                    f"M1 {name}: --measure-chars {row['asked']} realised "
                    f"{row['realised']:.2f} characters, off by {error:+.2f}. "
                    f"--face-advance {record['declaredAdvance']} does not match the "
                    f"{row['advanceEm']:.5f}em this face renders"
                )
    return failures


def check_m2(faces: dict[str, dict], report: bool) -> list[str]:
    low, high = M2_BAND
    failures: list[str] = []
    for name, record in faces.items():
        serif = "serif" in record["family"].lower() or name == "serif"
        if report:
            edge = "held" if serif else "reported"
            print(f"\n  M2  {name} ({record['family']}), band {edge}")
            print("      asked  body px  mono px  ratio")
        for row in record["m2"]:
            if report:
                print(
                    f"      {row['asked']:>5}  {row['bodyPx']:>7.2f}"
                    f"  {row['monoPx']:>7.2f}  {row['ratio']:>5.3f}"
                )
            if serif and not low <= row["ratio"] <= high:
                failures.append(
                    f"M2 {name}: at body {row['asked']}px the code size is "
                    f"{row['ratio']:.3f} of the prose, outside {low} to {high}"
                )
    return failures


def check_face_swap(faces: dict[str, dict], declared: dict[str, dict[str, str]], report: bool) -> list[str]:
    """Face-swap parity, gated on the half that is definite.

    Two things are promised when a reader changes the reading face. The line
    length they chose survives it, and the text stays the same size. The first
    is measured from layout and is exact. The second is gated here as "the
    registered factor is the one the page applied", which is a CSS computation
    and portable, rather than as "the rendered apparent size matches", which
    would gate the build on a perceptual construction the specification itself
    declines to trust: the factor is the geometric mean of two parity rules,
    calibrated against one rendered specimen, and re-deriving it from a
    different specimen moves it about two per cent. That figure is for the
    canvas, so it is printed below and not asserted.
    """
    failures: list[str] = []

    # The reference scale is the face whose factor is 1. Exactly one, or the
    # numbers on the body-size control mean two things at once.
    references = [name for name, entry in declared.items() if float(entry["--face-size-factor"]) == 1.0]
    if len(references) != 1:
        return [
            f"{len(references)} face(s) carry --face-size-factor 1; the reference scale "
            "the body-size control names must be exactly one face"
        ]
    reference = faces[references[0]]

    if report:
        print("\n  The registered size factor, against the size the page applied")
        print("      face     factor  expected px  rendered px")
    for name, record in faces.items():
        factor = float(declared[name]["--face-size-factor"])
        expected = reference["apparent"]["size"] * factor
        rendered = record["apparent"]["size"]
        if report:
            print(f"      {name:<8} {factor:>6}  {expected:>11.4f}  {rendered:>11.4f}")
        if abs(rendered - expected) > 0.01:
            failures.append(
                f"face swap {name}: the page renders {rendered:.4f}px where the registered "
                f"--face-size-factor {factor} asks for {expected:.4f}px"
            )

    # The count the reader chose must survive the swap, which is the whole
    # reason the measure is derived. M1 already proves it per face; this states
    # it across faces, because it is the promise the reader was made.
    counts = [record["m1"][0]["realised"] for record in faces.values()]
    if max(counts) - min(counts) > M1_TOLERANCE:
        failures.append(
            "face swap: at one --measure-chars the realised count moves by "
            f"{max(counts) - min(counts):.2f} characters across the registry"
        )
    return failures


def report_apparent_size(faces: dict[str, dict], reference_name: str) -> None:
    """Print the apparent-size drift. Reported for the canvas, never gated.

    The apparent-size factor is judgement built on two measurements, and the
    specification says to look at it on a canvas rather than trust it blind.
    So this table is here to be read, and a drift of a few per cent is a
    question for the person reviewing the canvas rather than a broken build.
    """
    reference = faces[reference_name]["apparent"]
    print("\n  Apparent size after the swap, reported for the canvas and not gated")
    print("      face     size px  x-height  ink extent  parity  drift")
    for name, record in faces.items():
        apparent = record["apparent"]
        drift = apparent["parity"] / reference["parity"] - 1
        print(
            f"      {name:<8} {apparent['size']:>7.2f}  {apparent['xHeight']:>8.2f}"
            f"  {apparent['inkExtent']:>10.2f}  {apparent['parity']:>6.2f}  {drift:>+6.1%}"
        )


def check_reflow(rows: list[dict], viewport: int, report: bool) -> list[str]:
    failures: list[str] = []
    if report:
        print(f"\n  Reflow at {viewport} CSS px")
        print("      body  chars  page overflow  broken boxes")
    for row in rows:
        size = "default" if row["size"] is None else f"{row['size']}px"
        chars = "default" if row["chars"] is None else str(row["chars"])
        if report:
            print(f"      {size:>7}  {chars:>5}  {row['overflow']:>13}  {row['broken']:>12}")
        if row["overflow"] or row["broken"]:
            failures.append(
                f"reflow at {viewport}px, body {size}, measure {chars}: "
                f"{row['overflow']}px of page overflow and {row['broken']} broken box(es)"
            )
    return failures


def check_face_switch(at_load: dict, switched: dict, report: bool) -> list[str]:
    """Both render states, for the axis this issue adds.

    A page that chose the sans face before its first paint and a page switched
    to it after load must compute the same thing. A failure means a rule that
    only matches on the first paint, or one that only matches after a change -
    the defect that survives review because it looks right on the next reload.
    """
    if report:
        print("\n  The sans face, chosen at load against switched after load")
    failures: list[str] = []
    for key in ("fontFamily", "fontSize", "lineHeight", "monoSize", "column", "faceAdvance"):
        if report:
            print(f"      {key:<22} {at_load[key]}")
        if at_load[key] != switched[key]:
            failures.append(
                f"face switch: {key} is {at_load[key]} when the face is chosen at load "
                f"and {switched[key]} when it is switched after it"
            )
    return failures


def check_script_free(scripted: dict, bare: dict, report: bool) -> list[str]:
    """Every derivation is CSS, so removing the script must move none of them."""
    if report:
        print("\n  With hub.js blocked")
        print(f"      panel built            {bare['scripted']} (with the script: {scripted['scripted']})")
    failures: list[str] = []
    if bare["scripted"]:
        failures.append("hub.js was meant to be blocked and the page still built its chrome")
    for key in ("fontFamily", "fontSize", "lineHeight", "monoSize", "column", "measureChars", "faceAdvance"):
        if report:
            print(f"      {key:<22} {bare[key]}")
        if scripted[key] != bare[key]:
            failures.append(
                f"script-free: {key} is {bare[key]} without hub.js and "
                f"{scripted[key]} with it; the derived layer is leaning on the script"
            )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--report", action="store_true", help="print the measured tables")
    arguments = parser.parse_args()

    faces, failures = registry()
    if arguments.report:
        print("The face registry, read out of assets/hub.css")
        for name, entry in sorted(faces.items()):
            print(f"  {name:<8} " + "  ".join(f"{k}={v}" for k, v in entry.items()))
    if failures:
        for failure in failures:
            print(f"  {failure}")
        print(f"\n{len(failures)} registry defect(s).")
        return 1

    corpus = CORPUS_FILE.read_text(encoding="utf-8")
    names = sorted(faces)
    server, origin = serve_repository()
    chrome = Chrome(find_chrome())
    try:
        session = Session(chrome, origin)
        session.viewport(1280)
        session.load()
        measured = session.call(MEASURE, corpus, names, list(M1_COUNTS), list(M2_SIZES))
        scripted = json.loads(str(chrome.evaluate(DERIVED)))

        failures += check_m1(measured["faces"], arguments.report)
        failures += check_m2(measured["faces"], arguments.report)
        failures += check_face_swap(measured["faces"], faces, arguments.report)
        if arguments.report and len(measured["faces"]) > 1:
            reference = next(
                (name for name, entry in faces.items() if float(entry["--face-size-factor"]) == 1.0),
                None,
            )
            if reference:
                report_apparent_size(measured["faces"], reference)

        for viewport in REFLOW_VIEWPORTS:
            session.viewport(viewport)
            session.load()
            rows = session.call(REFLOW, [list(cell) for cell in REFLOW_CELLS])
            failures += check_reflow(rows, viewport, arguments.report)

        session.viewport(1280)
        session.seed_face("sans")
        session.load()
        at_load = json.loads(str(chrome.evaluate(DERIVED)))
        session.seed_face(None)
        session.load()
        chrome.evaluate("document.documentElement.setAttribute('data-body-face', 'sans')")
        switched = json.loads(str(chrome.evaluate(DERIVED)))
        failures += check_face_switch(at_load, switched, arguments.report)

        session.block(["*hub.js*"])
        session.load()
        bare = json.loads(str(chrome.evaluate(DERIVED)))
        session.block([])
        failures += check_script_free(scripted, bare, arguments.report)
    finally:
        chrome.close()
        server.shutdown()

    print()
    if failures:
        for failure in failures:
            print(f"  {failure}")
        print(f"\n{len(failures)} invariant failure(s).")
        return 1
    print(
        f"{len(names)} registered face(s): M1 at {len(M1_COUNTS)} counts, "
        f"M2 at {len(M2_SIZES)} body sizes, face-swap parity, the reflow matrix "
        "at two viewports and the script-free read all hold."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
