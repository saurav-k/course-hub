#!/usr/bin/env python3
"""Check that a lesson's NAME agrees everywhere it is echoed.

A lesson has a **name** and it has a **claim**, and they are different objects.

The name is what the course map calls the lesson. It is echoed into the sidebar
rail, which ``gen_outline.py`` generates from the map, and into the ``.ttl`` of
every pager that points at the lesson. Those three must agree: they are one
object written down three times, and when one is edited and the others are not,
a reader clicks a link expecting one page and lands on a differently named one
while every link still resolves.

The claim is the page's ``<h1>``, which ``page-contracts.md`` requires to be
"the one idea, phrased as a claim with a verb in it rather than a topic". **A
claim is not a name and this checker does not compare them.** Requiring them
equal would force the h1 to stop being a claim or the card to stop being a
name, and either way it would break a rule older than this file.

That distinction was measured rather than assumed. Across the hub the pager
label tracks the map, not the h1: 111 of 111 in llm-evolution-course, 8 of 8,
10 of 10, 67 of 74. An earlier version of this check compared everything to the
h1 and reported 183 defects, of which most were the contract working correctly.

**A pager label and the name may differ by truncation, in either direction.**
The control is narrow so a pager shortens, and a map sometimes carries the
shorter form instead, so the test is symmetric: one must be a prefix of the
other once both are reduced to lower-case alphanumerics. It may not be a
*different* name, which is almost always a superseded one left by a rewrite.
Symmetry was checked against the corpus before being allowed: it clears the two
remaining defects in production-systems-course, where the map abbreviates and
the pager does not, and it changes none of the fifty-one in math-for-ml-course,
which are genuinely different titles rather than truncations.
A rail entry gets no latitude at all: it is generated from the map, so any
difference means a stale ``outline.js``.

The name is read exactly as ``gen_outline.py`` reads it - the ``.lt`` of a card,
or the anchor text where a course links its lessons from a parts list instead.
Using the generator's own definition is what makes the rail comparison mean
anything.

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
    }
)

# A frozen course cannot be swept, so listing it above would promise work nobody
# is allowed to do. statistical-foundations-ml-course is closed by a captain
# decision that no file under it may be modified, and its one defect is a pager
# label naming the destination's h1 rather than its map name, which was that
# course's convention before this rule existed.
FROZEN: frozenset[str] = frozenset({"statistical-foundations-ml-course"})

# The same two patterns gen_outline.py uses, so "the name" means the same thing
# here as it does in the file this compares against.
LESSON_LINK = re.compile(r'<a\b[^>]*href="(lessons/[^"#?]+)"[^>]*>(.*?)</a>', re.S)
CARD_TITLE = re.compile(r'<div class="lt">(.*?)</div>', re.S)
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

    # A map may link the same lesson several times. A routed course carries every
    # route's outline as static markup, so one lesson has one card per route it
    # appears in, and it also carries a "Start this route" call to action. The
    # card is the registration and the call to action is navigation, so a .lt
    # always wins over bare anchor text.
    #
    # Every card for the same lesson must agree with every other. Taking the
    # first or the last would hide a disagreement between two route outlines,
    # which is a real defect and one a reader meets by switching route.
    index = course / "index.html"
    cards: dict[str, list[str]] = {}
    bare: dict[str, str] = {}
    if index.is_file():
        for m in LESSON_LINK.finditer(index.read_text(encoding="utf-8")):
            page = m.group(1).split("/")[-1]
            card = CARD_TITLE.search(m.group(2))
            if card:
                cards.setdefault(page, []).append(clean(card.group(1)))
            elif page not in bare:
                bare[page] = clean(m.group(2))

    names: dict[str, str] = {page: titles[0] for page, titles in cards.items()}
    for page, title in bare.items():
        names.setdefault(page, title)

    # A routed course derives its outline from routes.js at load time, so its
    # outline.js holds logic rather than a literal and there is nothing to read.
    rail: dict[str, str] = {}
    outline = course / "outline.js"
    if outline.is_file() and not (course / "routes.js").is_file():
        for m in RAIL.finditer(outline.read_text(encoding="utf-8")):
            rail[m.group(2)] = m.group(1).encode().decode("unicode_escape")

    pagers: dict[str, list[tuple[str, str]]] = {}
    for page in sorted(lessons.glob("*.html")):
        for m in PAGER.finditer(page.read_text(encoding="utf-8")):
            pagers.setdefault(m.group(1).split("/")[-1], []).append((page.name, clean(m.group(2))))

    defects: list[tuple[str, str, str, str]] = []
    for page in sorted(n for n in names if in_range(n, low, high)):
        wanted = names[page]
        for other in cards.get(page, [])[1:]:
            if other != wanted:
                defects.append(("CARD disagrees with another card", page, other, wanted))
        if page in rail and rail[page] != wanted:
            defects.append(("RAIL", page, rail[page], wanted))
        for source, shown in pagers.get(page, []):
            if shown in ("Course map", wanted):
                continue
            label, name = norm(shown), norm(wanted)
            if name.startswith(label) or label.startswith(name):
                continue
            defects.append((f"PAGER in {source}", page, shown, wanted))
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
        waived = course.name in SWEEP_PENDING or course.name in FROZEN
        state = "FROZEN " if course.name in FROZEN else "PENDING" if waived else "FAIL   "
        print(f"  {state} {course.name}: {len(defects)} defect(s)")
        for kind, name, shown, wanted in defects:
            print(f"      {kind}\n         on   : {name}\n         shows: {shown}\n         name : {wanted}")
        if waived:
            pending += len(defects)
        else:
            blocking += len(defects)

    print(f"\n{blocking} blocking defect(s), {pending} waived")
    if pending:
        print("SWEEP_PENDING is debt, not exemption: delete the entry when the sweep lands.")
        print("FROZEN is a course nobody may edit, so its entry is permanent.")
    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
