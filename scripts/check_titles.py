#!/usr/bin/env python3
"""Check that a lesson's h1 agrees with every place its title is echoed.

A title lives in four places: the page's own ``h1``, its card in the course
index, the sidebar rail generated from that card, and the ``.ttl`` of every
pager that points at it. When one is edited and the others are not, a reader
clicks a link expecting one page and lands on a differently titled one, and
neither ``validate_site.py`` nor ``check_pages.py`` notices.

That is the defect class this catches. It was found by walking the pager chain
of M02 and M09 by hand, where one stale card title was echoed into the rail as
well, so a single edit produced two visible wrong titles.

**A pager label may be a faithful abbreviation of the destination's h1**,
because the control is narrow and shortening is an editorial choice the hub
makes widely. The test is that the h1 begins with the label once both are
reduced to lower-case alphanumerics. It may not be a *different* title, which
is almost always a superseded one left behind by a rewrite. A card and a rail
entry get no such latitude: they have the room, and the rail is generated from
the card, so a difference there is always a mistake rather than a choice.

Usage:

    python3 scripts/check_titles.py                          every course
    python3 scripts/check_titles.py math-for-ml-course       one course
    python3 scripts/check_titles.py math-for-ml-course 20 39 one number block

Exits non-zero when a course outside SWEEP_PENDING has a defect, so it can gate
a pull request.
"""

from __future__ import annotations

import html
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

# Courses whose titles predate this check and are being swept. A course is
# reported but does not fail the exit code while it is listed here, and its
# entry is deleted as the last step of its sweep. **This set is expected to
# reach empty**; anything still in it is visible debt rather than a settled
# exemption.
SWEEP_PENDING: frozenset[str] = frozenset(
    {
        "llm-inference-course",
        "llm-papers-course",
        "math-for-ml-course",
        "production-systems-course",
        "statistical-foundations-ml-course",
    }
)

H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S)
CARD = re.compile(r'<a class="lcard" href="lessons/([^"]+)".*?<div class="lt">(.*?)</div>', re.S)
RAIL = re.compile(r'"title"\s*:\s*"((?:[^"\\]|\\.)*)"\s*,\s*"href"\s*:\s*"lessons/([^"]+)"')
PAGER = re.compile(
    r'<a[^>]*href="([^"]+\.html)"[^>]*>\s*<span class="dir">[^<]*</span><span class="ttl">(.*?)</span>',
    re.S,
)


def clean(fragment: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", fragment))).strip()


def norm(text: str) -> str:
    """Lower-case alphanumerics only, which is what an abbreviation is compared on."""
    return re.sub(r"[^a-z0-9 ]", "", text.lower())


def in_range(name: str, low: int, high: int) -> bool:
    try:
        return low <= int(name[:4]) <= high
    except ValueError:
        return False


def audit(course: pathlib.Path, low: int, high: int) -> list[tuple[str, str, str, str]]:
    lessons = course / "lessons"
    if not lessons.is_dir():
        return []

    titles: dict[str, str] = {}
    for page in sorted(lessons.glob("*.html")):
        match = H1.search(page.read_text(encoding="utf-8"))
        if match:
            titles[page.name] = clean(match.group(1))

    index = course / "index.html"
    cards = (
        {m.group(1): clean(m.group(2)) for m in CARD.finditer(index.read_text(encoding="utf-8"))}
        if index.is_file()
        else {}
    )

    rail: dict[str, str] = {}
    outline = course / "outline.js"
    if outline.is_file():
        for m in RAIL.finditer(outline.read_text(encoding="utf-8")):
            rail[m.group(2)] = m.group(1).encode().decode("unicode_escape")

    pagers: dict[str, list[tuple[str, str]]] = {}
    for page in sorted(lessons.glob("*.html")):
        for m in PAGER.finditer(page.read_text(encoding="utf-8")):
            pagers.setdefault(m.group(1).split("/")[-1], []).append((page.name, clean(m.group(2))))

    defects: list[tuple[str, str, str, str]] = []
    for name in sorted(n for n in titles if in_range(n, low, high)):
        wanted = titles[name]
        if name in cards and cards[name] != wanted:
            defects.append(("CARD", name, cards[name], wanted))
        if name in rail and rail[name] != wanted:
            defects.append(("RAIL", name, rail[name], wanted))
        for source, shown in pagers.get(name, []):
            # A pager pointing at the course map is labelled for the map, whose
            # h1 is a claim rather than the course's name by contract.
            if shown in ("Course map", wanted):
                continue
            if norm(wanted).startswith(norm(shown)):
                continue
            defects.append((f"PAGER in {source}", name, shown, wanted))
    return defects


def main() -> int:
    args = sys.argv[1:]
    only = args[0] if args and not args[0].isdigit() else None
    numbers = [a for a in args if a.isdigit()]
    low, high = (int(numbers[0]), int(numbers[1])) if len(numbers) == 2 else (0, 9999)

    courses = sorted(p for p in REPO_ROOT.glob("*-course") if (p / "lessons").is_dir())
    if only:
        courses = [p for p in courses if p.name == only]
        if not courses:
            print(f"no course named {only}")
            return 2

    blocking = 0
    pending = 0
    for course in courses:
        defects = audit(course, low, high)
        if not defects:
            print(f"  ok      {course.name}")
            continue
        waived = course.name in SWEEP_PENDING
        print(f"  {'PENDING' if waived else 'FAIL   '} {course.name}: {len(defects)} defect(s)")
        for kind, name, shown, wanted in defects:
            print(f"      {kind}\n         on   : {name}\n         shows: {shown}\n         h1   : {wanted}")
        if waived:
            pending += len(defects)
        else:
            blocking += len(defects)

    print(f"\n{blocking} blocking defect(s), {pending} waived while a sweep is pending")
    if pending:
        print("Courses in SWEEP_PENDING are debt, not exemptions. Delete the entry when the sweep lands.")
    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
