#!/usr/bin/env python3
"""Static lint for the Mermaid failure modes that reach no console.

`check_pages.py` is the house checker and it already catches several of these.
This is a module-local belt-and-braces pass over M07's pages, written because
the shared browser used for render verification is contended across crews and a
Mermaid defect is invisible without one.

It checks the four documented silent-breakage rules from BUILDER-SPEC section 8,
plus the two label-length limits from widgets.md.

    python3 lint_mermaid.py <file.html> [<file.html> ...]

Exit code 1 if any FAIL is reported. Needs only the standard library.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MERMAID_DIV = re.compile(r'<div class="mermaid">(.*?)</div>', re.S)
MERMAID_PRE = re.compile(r'<pre[^>]*class="[^"]*mermaid', re.I)
LITERAL_BR = re.compile(r"<br\s*/?>", re.I)
UNQUOTED_NODE = re.compile(r"(?<![\w\"])([A-Za-z][\w]*)\[(?!\")")
QUADRANT_POINT = re.compile(r'^\s*"([^"]{1,200})"\s*:\s*\[', re.M)
ENTITY = re.compile(r"&[a-zA-Z][a-zA-Z0-9]*;|&#[0-9]+;")

MAX_QUADRANT_LABEL = 26
MAX_TIMELINE_COLUMNS = 6


def check(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []

    if MERMAID_PRE.search(text):
        problems.append(
            "FAIL: a <pre> carries class 'mermaid'. hub.js appends a copy button to "
            "every <pre>, so the word 'copy' joins the graph source and the figure "
            "renders as a syntax error. Use <div class=\"mermaid\">."
        )

    for index, graph in enumerate(MERMAID_DIV.findall(text), start=1):
        where = f"{path.name} mermaid block {index}"

        if LITERAL_BR.search(graph):
            problems.append(
                f"FAIL: {where} contains a literal <br/>. textContent drops it, so the "
                "first paint is right and every repaint joins the halves with no space. "
                "Write &lt;br/&gt;."
            )

        # An HTML entity ends in a semicolon, and `&lt;br/&gt;` is the *required*
        # spelling of a line break, so entities are stripped before this check.
        # Only a semicolon that survives is a Mermaid statement separator.
        if ";" in ENTITY.sub(" ", graph):
            problems.append(
                f"FAIL: {where} contains a semicolon. In a sequenceDiagram the free text "
                "after a colon is parsed as a statement and a semicolon there is a red "
                "error box. Use a dash everywhere."
            )

        for node in UNQUOTED_NODE.findall(graph):
            problems.append(
                f"FAIL: {where} node '{node}[' has an unquoted label. Parentheses, commas "
                'and mathematics all break the parser bare. Wrap it in double quotes.'
            )

        if graph.lstrip().startswith("quadrantChart"):
            for label in QUADRANT_POINT.findall(graph):
                if len(label) > MAX_QUADRANT_LABEL:
                    problems.append(
                        f"FAIL: {where} quadrant point label {label!r} is {len(label)} "
                        f"characters, the cap is {MAX_QUADRANT_LABEL}. It is centred under "
                        "its point and is neither clipped nor wrapped."
                    )

        if graph.lstrip().startswith("timeline"):
            columns = len(re.findall(r"^\s{2,}\S.*:", graph, re.M))
            if columns > MAX_TIMELINE_COLUMNS:
                problems.append(
                    f"WARN: {where} timeline has about {columns} columns. A timeline "
                    f"shrinks rather than wraps - keep it to {MAX_TIMELINE_COLUMNS} and "
                    "split a longer one into two figures."
                )

    return problems


def main() -> int:
    paths = [Path(argument) for argument in sys.argv[1:]]
    if not paths:
        print(__doc__)
        return 2

    failures = 0
    for path in paths:
        for problem in check(path):
            print(f"  {problem}")
            failures += problem.startswith("FAIL")

    print(f"\nlinted {len(paths)} page(s): {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
