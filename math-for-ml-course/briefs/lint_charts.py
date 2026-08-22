#!/usr/bin/env python3
"""Static estimate of SVG chart text clipping and label collisions.

The real measurement is `getBBox()` in a browser, and it stays the gate. This
is the check you can run on every save, and it exists because chart text
running off a viewBox has been the most common defect class in this build.

It estimates each `<text>` element's box from three things it can read off the
markup: the character count, the font size implied by the class (from the
`.chart` rules in `assets/hub.css`), and `text-anchor`. It then flags a label
whose estimated box leaves the viewBox, or two labels whose boxes overlap.

An estimate has two failure modes and both are stated rather than hidden:

  * It cannot know the real advance width of a glyph, so it uses a calibrated
    average. Anything within CLEARANCE of an edge is reported as NEAR, not as
    a failure, because the estimate cannot resolve that margin.
  * It cannot see `transform` attributes. A rotated or translated label is
    skipped and counted, so the count is visible rather than silently zero.

    python3 lint_charts.py <file.html> [<file.html> ...]

Exit code 1 if any CLIP or OVERLAP is reported. Standard library only.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

SVG_CHART = re.compile(r'<svg class="chart"[^>]*viewBox="([^"]+)"(.*?)</svg>', re.S)
TEXT_TAG = re.compile(r'<text\b([^>]*)>(.*?)</text>', re.S)
ATTR = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')

# From the `.chart` block in assets/hub.css. The base rule is 13px and the
# classes below override it.
FONT_SIZE = {"lbl-sm": 11.5, "ttl": 13.5}
BASE_FONT = 13.0

# Average advance width as a fraction of font size, for the hub's sans stack.
# Calibrated so that the six figures corrected in PR #75 and the fifteen M07
# charts all report clean, while a label pushed past the edge is caught.
CHAR_W = 0.52
BOLD_EXTRA = 1.04          # .lbl-b and .ttl are weight 700
CLEARANCE = 6.0            # inside this margin the estimate cannot decide
MIN_OVERLAP = 2.0          # ignore hairline touches


def font_for(classes: list[str]) -> tuple[float, bool]:
    size = BASE_FONT
    for name, value in FONT_SIZE.items():
        if name in classes:
            size = value
    bold = "lbl-b" in classes or "ttl" in classes
    return size, bold


def box_of(attrs: dict[str, str], text: str) -> tuple[float, float, float, float] | None:
    """Estimated (x, y, width, height) of a rendered label."""
    try:
        x = float(attrs.get("x", "0"))
        y = float(attrs.get("y", "0"))
    except ValueError:
        return None
    classes = attrs.get("class", "").split()
    size, bold = font_for(classes)
    width = len(text) * size * CHAR_W * (BOLD_EXTRA if bold else 1.0)
    anchor = attrs.get("text-anchor", "start")
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    # y is the baseline: the box sits above it, with a little descender below.
    return x, y - size * 0.78, width, size


def check(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8")
    problems: list[str] = []

    for index, (viewbox, body) in enumerate(SVG_CHART.findall(source)):
        parts = viewbox.split()
        if len(parts) != 4:
            problems.append(f"CLIP: chart {index} has a malformed viewBox {viewbox!r}")
            continue
        vx, vy, vw, vh = (float(p) for p in parts)
        boxes: list[tuple[tuple[float, float, float, float], str]] = []
        skipped = 0

        for raw_attrs, raw_text in TEXT_TAG.findall(body):
            attrs = dict(ATTR.findall(raw_attrs))
            if "transform" in attrs:
                skipped += 1
                continue
            text = html.unescape(re.sub(r"<[^>]+>", "", raw_text)).strip()
            if not text:
                continue
            box = box_of(attrs, text)
            if box is None:
                skipped += 1
                continue
            x, y, w, h = box
            label = text[:24]
            over_right = (x + w) - (vx + vw)
            over_left = vx - x
            over_bottom = (y + h) - (vy + vh)
            over_top = vy - y
            worst = max(over_right, over_left, over_bottom, over_top)
            if worst > CLEARANCE:
                side = ("right" if worst == over_right else
                        "left" if worst == over_left else
                        "bottom" if worst == over_bottom else "top")
                problems.append(
                    f"CLIP: chart {index} label {label!r} runs {worst:.0f}px past the "
                    f"{side} edge of the {vw:.0f}x{vh:.0f} viewBox"
                )
            elif worst > 0:
                problems.append(
                    f"NEAR: chart {index} label {label!r} is within {worst:.0f}px of the "
                    f"edge - too close for this estimate to decide, measure it"
                )
            boxes.append((box, label))

        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                (ax, ay, aw, ah), a = boxes[i]
                (bx, by, bw, bh), b = boxes[j]
                dx = min(ax + aw, bx + bw) - max(ax, bx)
                dy = min(ay + ah, by + bh) - max(ay, by)
                if dx > MIN_OVERLAP and dy > MIN_OVERLAP:
                    problems.append(
                        f"OVERLAP: chart {index} {a!r} and {b!r} overlap by "
                        f"{dx:.0f}x{dy:.0f}px"
                    )

        if skipped:
            problems.append(
                f"NOTE: chart {index} has {skipped} label(s) this estimate skipped "
                "(a transform, or a non-numeric x or y). Measure those in a browser."
            )

    return problems


def main() -> int:
    paths = [Path(a) for a in sys.argv[1:]]
    if not paths:
        print(__doc__)
        return 2
    hard = 0
    for path in paths:
        for problem in check(path):
            print(f"  {path.name}: {problem}")
            hard += problem.startswith(("CLIP", "OVERLAP"))
    print(f"\nlinted {len(paths)} page(s): {hard} clipping or overlap problem(s)")
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
