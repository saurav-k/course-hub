#!/usr/bin/env python3
"""Look at every figure on every page of a course, in both render states.

``check_pages.py`` reads markup and ``validate_site.py`` reads links; neither
renders a page, and the defects that matter most on this hub are visible only
when one is rendered. A semicolon in sequence text is a red error box. A
literal ``<br/>`` in a Mermaid label joins two words with no space, because
``hub.js`` stashes the graph source as ``textContent`` before the first render
and repaints from the stash. A nowrap row spills at a narrow width. None of it
reaches the console.

This is the machine half of the browser pass in
``.claude/skills/course-authoring/references/verify.md``. It loads every page of
a course in headless Chrome with the network on, waits for every diagram to
render, and records three things: the number of Mermaid error boxes, the label
text of every rendered diagram, and whether the body scrolls sideways. Then it
presses the reader's own light-and-dark control, waits for the repaint, and
records the three again. A page fails on an error box or a blank render in
either state, on any label whose text changed between the two - which is the
repaint path disagreeing with the first paint - and on a body that scrolls
horizontally. With ``--narrow`` it also lays every page out at 360px and fails
one whose body scrolls there.

What it cannot do is read the drawing. A diagram that parses can still say the
wrong thing, a `d-ghost` box can carry a live connector, and a chart label can
be cut at the frame edge with the element present and happy. Those are the
human half of the same pass, and this script exists so that the human half is
spent on them rather than on counting error boxes.

    python3 scripts/render_sweep.py <course>                     # every page of one course
    python3 scripts/render_sweep.py <course>/lessons/0001-x.html # one page
    python3 scripts/render_sweep.py <course> --narrow            # also at 360px
    python3 scripts/render_sweep.py <course> --palette ink       # first paint on another palette

Exit code 0 means every page rendered clean in both states. Exit code 1 lists
every failure, one line per page and defect, in the shape ``check_pages.py``
uses. It needs Chrome and the network; the Chrome driver is the one
``style_snapshot.py`` owns, told not to block the Mermaid CDN.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from style_snapshot import VIEWPORT, Chrome, find_chrome, serve_repository  # noqa: E402

REPO_ROOT: Path = Path(__file__).resolve().parent.parent

# How long one page may take to render every diagram before the wait gives up
# and the page is reported. Twenty seconds covers a cold font load, the CDN and
# a page carrying a dozen diagrams; a page that needs longer has a problem worth
# reporting rather than waiting out.
RENDER_TIMEOUT: float = 20.0
# How often the wait asks whether the render has finished.
POLL: float = 0.1
# The narrow width. 360px is the width `verify.md` names, because it is what a
# small phone reports and what the topbar and the figures were measured at.
NARROW: tuple[int, int] = (360, 740)

# Every `.mermaid` block is rendered when Mermaid has written `data-processed`
# on it; `hub.js` takes the attribute off before a repaint and Mermaid puts it
# back after, so the same test answers both waits. A page with no `.mermaid`
# is rendered as soon as it has loaded.
RENDERED = """
(function () {
  var all = document.querySelectorAll('.mermaid');
  var done = document.querySelectorAll('.mermaid[data-processed]');
  return all.length === done.length;
})()
"""

# What one render state looks like. A diagram's label text is read as the
# rendered text of its block - `innerText`, which keeps the line structure an
# HTML label has and drops the SVG's own <style> element, where Mermaid writes
# its classDef colours and where the palette changes them by design. A block
# Mermaid has marked processed and left with no <svg> is a render that failed
# without an error box, which `suppressErrorRendering` and a thrown parser both
# produce, so it is counted apart from the boxes.
STATE = """
(function () {
  var root = document.documentElement;
  var blocks = Array.prototype.slice.call(document.querySelectorAll('.mermaid'));
  return {
    mode: root.getAttribute('data-mode') || 'system',
    palette: root.getAttribute('data-palette') || '',
    diagrams: blocks.length,
    blank: blocks.filter(function (b) { return b.hasAttribute('data-processed') && !b.querySelector('svg'); }).length,
    errors: document.querySelectorAll('.mermaid .error-icon, .mermaid text.error-text').length,
    labels: blocks.map(function (b) { return (b.innerText || b.textContent).replace(/\\s+/g, ' ').trim(); }),
    overflow: root.scrollWidth - root.clientWidth
  };
})()
"""

# The reader's own control: the mode button in the floating cluster, which is
# the same button `verify.md` tells a human to press. Pressing it is what puts
# `hub.js` through the repaint path, so nothing here sets `data-mode` by hand.
TOGGLE = """
(function () {
  var button = document.querySelector('.dock button[aria-label^="Switch to"]');
  if (!button) return false;
  button.click();
  return true;
})()
"""

PALETTE_SEED = "try { localStorage.setItem('coursehub.palette', %s); localStorage.removeItem('coursehub.mode'); } catch (e) {}"


def pages_under(target: Path) -> list[Path]:
    """Every published page under a target, in a stable order."""
    if target.is_file():
        return [target]
    return sorted(
        page
        for page in target.rglob("*.html")
        if not any(part.startswith(".") for part in page.relative_to(REPO_ROOT).parts)
    )


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


class Sweep:
    """One Chrome, one loopback server, and the three reads per page."""

    def __init__(self, chrome: Chrome, origin: str, palette: str | None) -> None:
        self.chrome = chrome
        self.origin = origin
        chrome.page("Page.enable")
        chrome.page("Runtime.enable")
        self.desktop()
        # The seed runs before the page's own scripts, so `hub.js` reads the
        # requested palette in its head phase exactly as it reads a reader's.
        seed = PALETTE_SEED % json.dumps(palette) if palette else "try { localStorage.removeItem('coursehub.mode'); } catch (e) {}"
        chrome.page("Page.addScriptToEvaluateOnNewDocument", {"source": seed})

    def desktop(self) -> None:
        self.chrome.page(
            "Emulation.setDeviceMetricsOverride",
            {"width": VIEWPORT[0], "height": VIEWPORT[1], "deviceScaleFactor": 1, "mobile": False},
        )

    def narrow(self) -> None:
        self.chrome.page(
            "Emulation.setDeviceMetricsOverride",
            {"width": NARROW[0], "height": NARROW[1], "deviceScaleFactor": 1, "mobile": True},
        )

    def load(self, page: Path) -> None:
        self.chrome.drain()
        self.chrome.page("Page.navigate", {"url": f"{self.origin}/{rel(page)}"})
        self.chrome.await_event("Page.loadEventFired")

    def rendered(self) -> bool:
        """Wait for every diagram, and say whether the wait succeeded."""
        deadline = time.time() + RENDER_TIMEOUT
        while time.time() < deadline:
            if self.chrome.evaluate(RENDERED):
                # Mermaid marks the block before hub.js has settled the SVG's
                # width and colour; one more tick lets that finish.
                time.sleep(POLL * 3)
                return True
            time.sleep(POLL)
        return False

    def state(self) -> dict:
        return self.chrome.evaluate(STATE)  # type: ignore[return-value]

    def toggle(self) -> bool:
        return bool(self.chrome.evaluate(TOGGLE))


def sweep_page(sweep: Sweep, page: Path, narrow: bool) -> list[str]:
    """Every defect one page shows, as ``where: detail`` lines."""
    where = rel(page)
    found: list[str] = []
    sweep.load(page)
    if not sweep.rendered():
        found.append(f"{where}: a diagram did not finish rendering within {RENDER_TIMEOUT:g}s")
    first = sweep.state()
    if first["errors"]:
        found.append(f"{where}: {first['errors']} Mermaid error box(es) on first paint ({first['mode']}, {first['palette']})")
    if first["blank"]:
        found.append(f"{where}: {first['blank']} diagram(s) rendered nothing on first paint; the source is still in the block")
    if first["overflow"] > 0:
        found.append(f"{where}: the body scrolls {first['overflow']}px sideways at {VIEWPORT[0]}px")

    if not sweep.toggle():
        found.append(f"{where}: no light-and-dark control in the floating cluster; hub.js did not mount")
        return found
    if not sweep.rendered():
        found.append(f"{where}: a diagram did not finish repainting within {RENDER_TIMEOUT:g}s")
    second = sweep.state()
    if second["mode"] == first["mode"]:
        found.append(f"{where}: pressing the mode control left data-mode at {first['mode']}; the repaint path did not run")
    if second["errors"]:
        found.append(f"{where}: {second['errors']} Mermaid error box(es) after the repaint ({second['mode']}, {second['palette']})")
    if second["blank"]:
        found.append(f"{where}: {second['blank']} diagram(s) rendered nothing after the repaint")
    if len(second["labels"]) != len(first["labels"]):
        found.append(f"{where}: {len(first['labels'])} diagram(s) on first paint and {len(second['labels'])} after the repaint")
    else:
        for index, (before, after) in enumerate(zip(first["labels"], second["labels"])):
            if before != after:
                found.append(
                    f"{where}: diagram {index} label text changed on the repaint, so the stashed source "
                    f"and the authored source disagree (before: \"{before[:60]}\", after: \"{after[:60]}\")"
                )
    # Put the reader's stored mode back, so the next page's first paint is the
    # same state this page's was.
    sweep.toggle()

    if narrow:
        sweep.narrow()
        time.sleep(POLL * 3)
        overflow = sweep.chrome.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        if isinstance(overflow, (int, float)) and overflow > 0:
            found.append(f"{where}: the body scrolls {overflow:g}px sideways at {NARROW[0]}px")
        sweep.desktop()
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("targets", nargs="+", help="a course folder or a page, relative to the repository root")
    parser.add_argument("--narrow", action="store_true", help=f"also lay every page out at {NARROW[0]}px")
    parser.add_argument("--palette", help="the palette the first paint uses, by its registered key")
    arguments = parser.parse_args()

    pages: list[Path] = []
    for target in arguments.targets:
        path = (REPO_ROOT / target).resolve()
        if not path.exists():
            raise SystemExit(f"{target} is not a file or folder under the repository root")
        pages.extend(pages_under(path))
    if not pages:
        raise SystemExit("nothing to sweep")

    server, origin = serve_repository()
    chrome = Chrome(find_chrome(), offline=False)
    failures: list[str] = []
    try:
        sweep = Sweep(chrome, origin, arguments.palette)
        for page in pages:
            for line in sweep_page(sweep, page, arguments.narrow):
                failures.append(line)
                print(f"  FAIL  {line}")
    finally:
        chrome.close()
        server.shutdown()

    print(f"\nswept {len(pages)} page(s) in both render states: {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
