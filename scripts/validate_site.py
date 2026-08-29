#!/usr/bin/env python3
"""Static checks for the Course Hub before anything is published.

Eighteen checks, all deterministic and offline:

1. Every course folder has an ``index.html`` and the hub ``index.html`` links it.
2. Every ``lessons/*.html`` file is linked from its own course ``index.html``.
3. Every course ``outline.js`` names exactly the lessons that are on disk.
4. Every relative ``href``/``src`` in every page resolves to a file on disk.
5. No published page links a local ``.md`` file, which the deploy excludes.
6. Every course map's module sections are balanced and none nests inside another,
   which is the one structural break that renders correctly and reaches no console.
7. Every lesson's name agrees between the course map, the generated rail and every
   pager that points at it, by the rules in ``scripts/check_titles.py``. The page's
   ``h1`` is a claim rather than a name and is not compared.
8. The capability-matrix data (``window.CLOUD_CAPABILITY_MATRIX``, committed beside
   the comparison course): the taxonomy is intact, every capability key appears
   exactly once as a row, every row carries all four clouds, every cell is a
   service, a capability delivered under another row, a declared absence with a
   reason, or explicitly unfilled, every cross-reference resolves to a row that
   exists, every page rendering the widget binds to the documented
   ``figure.cmatrix`` frame, and every vendor link is well formed. Pass
   ``--vendor-links`` to also fetch each vendor link and fail on a dead one - the
   default run stays offline and deterministic.
9. The design registry in ``assets/hub.js`` and the ``:root[data-design="..."]``
   blocks in ``assets/hub.css`` name the same set of designs, so the appearance
   panel can offer nothing that resolves to nothing and the stylesheet can carry
   no block nobody can reach.
10. Every design declares the whole token set, compared against the default
   design's, and a design-axis token is declared in a design block and nowhere
   else. A half-declared design inherits the other one's values and looks nearly
   right; a token declared a second time outside a design block is out-specified
   by every design block and goes silently dead.
11. The three-layer property rule: no rule in ``hub.css`` reads a ``--*-user``
   property outside its own resolution line, and no control in ``hub.js`` writes
   anything on ``<html>`` but a ``--*-user`` property, a registered axis
   attribute, or the printed sheet's identity.
12. The course contract: every course folder is registered exactly once in
   ``assets/hub.css``, in the documented block shape, declaring only the seven
   author tokens and only values inside their stated ranges; the six tokens a
   design also declares keep their two names, so a design and a course never
   contend for one; no two courses hold one hue; no course ships a stylesheet
   of its own beyond the three grandfathered ones; and no eyebrow set in
   capitals runs past five words in a segment. What the registered hue then
   looks like needs a browser and is asserted in ``scripts/style_snapshot.py``.

13. The accessibility floor, by the arithmetic half of checks G1, G2 and G3 in
   ``scripts/contrast.py``: every registered ground is inside its lightness band,
   every ink clears 7:1 and sits on the right side of the L* 48.9 crossover, and
   every colour a palette states clears the floor its role carries. The derived
   tints and the per-course accent need a browser and are measured by
   ``scripts/contrast_matrix.py`` in the style job instead.
14. Every custom property a ``@page`` margin box reads is declared somewhere in
   ``hub.css``. A margin box that resolves to nothing prints an empty running
   foot, in the one render state no screen check can see.
15. Every width media query, in ``hub.css`` and in every course sheet, names a
   medium. A width feature is answered by the page box in print, and the printed
   page box is narrower than the hub's smallest breakpoint, so an unqualified
   one silently lays the paper out as a phone.
16. The font contract: every ``@font-face`` reaches a woff2 that is on disk,
   every woff2 on disk is named by a declaration, every face states a
   ``font-display``, and the payload stays under the two recorded ceilings.
17. Below 720px the topbar keeps the wordmark and the page's last link, so that
   last anchor is the whole of a phone reader's navigation and is the one anchor
   that may not also carry ``hide-sm``.
18. Every token a page names, in a ``data-token`` or a ``data-spec`` attribute,
   is a custom property ``assets/hub.css`` actually declares. Naming a token is
   how ``design-system/index.html`` documents the system, and a rename in the
   stylesheet would otherwise leave the reference page describing something that
   no longer exists, with nothing red anywhere.

Checks 9 to 16 read the shared asset files rather than the pages; 17 reads the
pages; and check 18 reads both. What the design system then *renders* is the
computed-style harness's job; see ``scripts/style_snapshot.py``.

A course may ship a ``routes.js`` manifest instead of a static ``outline.js``,
which lets one pool of lessons be read along several named routes. That course
derives its outline at load time, so check 3 does not apply to it and three
further checks do:

6. Its ``routes.js`` and its ``lessons/`` agree, every route covers every page
   of the kinds it declares, and every manifest title matches the page's ``h1``.
7. Every lesson's committed pager matches the route that owns the page, which is
   what makes navigation correct with scripting switched off.
8. Every lesson carries the living-document metadata that course requires.

Exit code 0 means the site is publishable. Exit code 1 lists every problem.
"""

from __future__ import annotations

import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib import request as _urlrequest
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit

import contrast

REPO_ROOT: Path = Path(__file__).resolve().parent.parent

LINK_PATTERN: re.Pattern[str] = re.compile(r'(?:href|src)\s*=\s*"([^"]+)"', re.IGNORECASE)

EXTERNAL_PREFIXES: tuple[str, ...] = ("http://", "https://", "//", "#", "mailto:", "data:", "javascript:")

OUTLINE_ASSIGNMENT: re.Pattern[str] = re.compile(
    r"window\.COURSE_OUTLINE\s*=\s*(?P<payload>\{.*\})\s*;", re.DOTALL
)

ROUTES_ASSIGNMENT: re.Pattern[str] = re.compile(
    r"window\.COURSE_ROUTES\s*=\s*(?P<payload>\{.*\})\s*;", re.DOTALL
)

H1_PATTERN: re.Pattern[str] = re.compile(r"<h1[^>]*>(?P<title>.*?)</h1>", re.DOTALL)

PAGER_PATTERN: re.Pattern[str] = re.compile(
    r'<nav class="pager" data-pager-route="(?P<route>[^"]+)"[^>]*>(?P<body>.*?)</nav>', re.DOTALL
)

ANCHOR_HREF: re.Pattern[str] = re.compile(r'<a\b[^>]*href="(?P<href>[^"]*)"', re.IGNORECASE)

MAIN_BLOCK: re.Pattern[str] = re.compile(r"<main[^>]*>(?P<body>.*)</main>", re.DOTALL)

HTML_COMMENT: re.Pattern[str] = re.compile(r"<!--.*?-->", re.DOTALL)

# `section` and `div` are the two elements a course map nests, and neither may be
# self-closing in HTML, so counting open and close tags is exact rather than an
# approximation.
NESTING_TAG: re.Pattern[str] = re.compile(r"<(?P<close>/?)(?P<tag>section|div)\b[^>]*>", re.IGNORECASE)

MODULE_SECTION: re.Pattern[str] = re.compile(r'<section class="module">')

# The capability matrix: the data assignment and the widget frame it must bind to.
MATRIX_ASSIGNMENT: re.Pattern[str] = re.compile(
    r"window\.CLOUD_CAPABILITY_MATRIX\s*=\s*(?P<payload>\{.*\})\s*;", re.DOTALL
)

MATRIX_FRAME: str = '<figure class="cmatrix"'

# The four clouds are fixed by the research spec; a comparison column is one of
# them and nothing else.
MATRIX_CLOUDS: frozenset[str] = frozenset({"aws", "azure", "gcp", "oci"})

# The taxonomy's areas are a closed list of twenty-four, fixed by the same spec.
MATRIX_DOMAIN_COUNT: int = 24

KEBAB: re.Pattern[str] = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# The four cell states. "absent" and "elsewhere" both start life as a gap entry
# in a cloud's inventory and they make opposite claims, so they are separate
# states rather than one state with a flag: "absent" is the only one that lets a
# reader conclude the cloud cannot do the thing.
CELL_STATES: frozenset[str] = frozenset({"unfilled", "absent", "elsewhere", "service"})


# ---------- the font contract ----------
# One @font-face block, and the three descriptors this repository holds it to.
FONT_FACE: re.Pattern[str] = re.compile(r"@font-face\s*\{(?P<body>[^}]*)\}", re.DOTALL)
FONT_SRC_URL: re.Pattern[str] = re.compile(r"""url\(\s*['"]?(?P<href>[^'")]+)['"]?\s*\)""")
FONT_DISPLAY: re.Pattern[str] = re.compile(r"font-display\s*:\s*(?P<value>[a-z-]+)")
FONT_UNICODE_RANGE: re.Pattern[str] = re.compile(r"unicode-range\s*:\s*(?P<value>[^;]+)")

# The basic-latin cut. A face gated to a range carrying it is one an English
# page fetches; every other range is a subset an English page never asks for.
FONT_LATIN_MARKER: str = "U+0000-00FF"

# The payload ceilings, in bytes, measured 2026-08-29 and carried here so that a
# fourth face is added against a known number rather than against a guess.
# Today: 470,312 bytes over eight files, of which 246,828 are the latin cuts,
# which is the most one English page can fetch. Each ceiling is today's figure
# rounded up to the next 10K, which leaves room for a font refresh and none at
# all for a new face. Raising one is a deliberate act; see assets/fonts/README.md.
FONT_BYTES_CEILING: int = 480 * 1024
FONT_LATIN_BYTES_CEILING: int = 250 * 1024


@dataclass(frozen=True)
class Problem:
    """One failed check, reported relative to the repository root."""

    where: str
    detail: str

    def render(self) -> str:
        return f"{self.where}: {self.detail}"


def relative(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def read_links(page: Path) -> list[str]:
    """Return every href/src value in a page, in document order."""
    return LINK_PATTERN.findall(page.read_text(encoding="utf-8", errors="replace"))


def is_local(link: str) -> bool:
    return bool(link) and not link.startswith(EXTERNAL_PREFIXES)


def strip_suffixes(link: str) -> str:
    """Drop the query string and fragment so only the path remains."""
    return link.split("#", 1)[0].split("?", 1)[0]


def course_directories() -> list[Path]:
    """The top-level directories that ship a page.

    Every one of them is registered on the hub landing page and holds to the
    page contract, which is why this is what most checks here iterate. Not all
    of them teach; see :func:`teaching_courses`.
    """
    return sorted(
        entry
        for entry in REPO_ROOT.iterdir()
        if entry.is_dir()
        and not entry.name.startswith(".")
        and entry.name not in {"assets", "scripts"}
    )


def is_course(folder: Path) -> bool:
    """A top-level folder that teaches, as opposed to one that does not.

    ``design-system/`` is a single reference page about the design system
    itself. It has no lessons, so it has no identity to register in the course
    contract and no accent hue to be told apart by, and the sheet it does ship
    is that one page's own scaffolding rather than a course reaching for rules
    the hub sheet should own.

    The test is the ``lessons/`` directory, because that is what a course *is*
    here and every one of them has one. Deliberately structural rather than a
    list of names: a list has to be edited by whoever adds the next course, and
    the failure mode of forgetting is a course that quietly stops being checked.
    """
    return folder.is_dir() and (folder / "lessons").is_dir()


def teaching_courses() -> list[Path]:
    """The course folders the course contract applies to."""
    return [folder for folder in course_directories() if is_course(folder)]


def html_pages() -> list[Path]:
    """Every page the site actually publishes.

    Dot-directories are tool state, never site content: ``.git`` obviously, but
    also ``.lavish``, ``.vscode`` and anything else a contributor's tooling
    leaves in the tree. Scanning them turns a local scratch file into a failed
    pull request, so they are skipped by rule rather than by name.
    """
    return sorted(
        page
        for page in REPO_ROOT.rglob("*.html")
        if not any(part.startswith(".") for part in page.relative_to(REPO_ROOT).parts)
        and "node_modules" not in page.parts
    )


def check_courses_are_registered() -> list[Problem]:
    hub_index = REPO_ROOT / "index.html"
    if not hub_index.is_file():
        return [Problem("index.html", "the hub landing page is missing")]

    linked = {strip_suffixes(link) for link in read_links(hub_index) if is_local(link)}
    problems: list[Problem] = []

    for course in course_directories():
        course_index = course / "index.html"
        if not course_index.is_file():
            problems.append(Problem(relative(course), "course folder has no index.html"))
            continue
        if f"{course.name}/index.html" not in linked:
            problems.append(
                Problem("index.html", f"hub page does not link {course.name}/index.html")
            )
    return problems


def check_lessons_are_registered() -> list[Problem]:
    problems: list[Problem] = []

    for course in course_directories():
        course_index = course / "index.html"
        lessons_dir = course / "lessons"
        if not course_index.is_file() or not lessons_dir.is_dir():
            continue

        linked = {strip_suffixes(link) for link in read_links(course_index) if is_local(link)}
        for lesson in sorted(lessons_dir.glob("*.html")):
            if f"lessons/{lesson.name}" not in linked:
                problems.append(
                    Problem(relative(course_index), f"does not link lessons/{lesson.name}")
                )
    return problems


def outline_lessons(manifest: Path) -> set[str] | None:
    """Return the lesson file names the manifest declares, or None if unreadable."""
    match = OUTLINE_ASSIGNMENT.search(manifest.read_text(encoding="utf-8"))
    if match is None:
        return None
    try:
        payload = json.loads(match.group("payload"))
    except json.JSONDecodeError:
        return None
    return {
        lesson["href"].split("/")[-1]
        for section in payload.get("sections", [])
        for lesson in section.get("lessons", [])
    }


def check_outlines_match_disk() -> list[Problem]:
    problems: list[Problem] = []

    for course in course_directories():
        manifest = course / "outline.js"
        lessons_dir = course / "lessons"
        if not manifest.is_file() or not lessons_dir.is_dir():
            continue
        if (course / "routes.js").is_file():
            # A routed course derives its outline from the active route at load
            # time, so its outline.js holds logic rather than a literal. The
            # route checks below cover the same ground for it.
            continue

        declared = outline_lessons(manifest)
        if declared is None:
            problems.append(
                Problem(relative(manifest), "no readable window.COURSE_OUTLINE assignment")
            )
            continue

        on_disk = {lesson.name for lesson in lessons_dir.glob("*.html")}
        for missing in sorted(on_disk - declared):
            problems.append(
                Problem(relative(manifest), f"outline is stale: lessons/{missing} is not in it")
            )
        for ghost in sorted(declared - on_disk):
            problems.append(
                Problem(relative(manifest), f"outline names lessons/{ghost}, which is not on disk")
            )
    return problems


def route_manifest(course: Path) -> tuple[dict, list[Problem]]:
    """Parse a course's routes.js, or return the reason it could not be read."""
    manifest_path = course / "routes.js"
    match = ROUTES_ASSIGNMENT.search(manifest_path.read_text(encoding="utf-8"))
    if match is None:
        return {}, [Problem(relative(manifest_path), "no readable window.COURSE_ROUTES assignment")]
    try:
        return json.loads(match.group("payload")), []
    except json.JSONDecodeError as error:
        return {}, [Problem(relative(manifest_path), f"window.COURSE_ROUTES is not valid JSON: {error}")]


def route_files(route: dict) -> list[str]:
    return [name for section in route.get("sections", []) for name in section.get("lessons", [])]


def owning_route(manifest: dict, name: str) -> dict | None:
    """The first route containing a page. Its order is what the committed pager,
    breadcrumb and no-script navigation follow, so it has to be well defined."""
    for route in manifest.get("routes", []):
        if name in route_files(route):
            return route
    return None


def page_title(page: Path) -> str | None:
    match = H1_PATTERN.search(page.read_text(encoding="utf-8"))
    return None if match is None else html.unescape(re.sub(r"<[^>]+>", "", match.group("title"))).strip()


def check_routes_cover_the_pool() -> list[Problem]:
    problems: list[Problem] = []

    for course in course_directories():
        if not (course / "routes.js").is_file():
            continue
        where = relative(course / "routes.js")
        manifest, failures = route_manifest(course)
        if failures:
            problems.extend(failures)
            continue

        pages = manifest.get("pages", {})
        lessons_dir = course / "lessons"
        on_disk = {lesson.name for lesson in lessons_dir.glob("*.html")} if lessons_dir.is_dir() else set()

        for missing in sorted(on_disk - set(pages)):
            problems.append(Problem(where, f"lessons/{missing} is on disk but not in pages"))
        for ghost in sorted(set(pages) - on_disk):
            problems.append(Problem(where, f"pages names lessons/{ghost}, which is not on disk"))

        for name in sorted(set(pages) & on_disk):
            declared = pages[name].get("title", "")
            actual = page_title(lessons_dir / name)
            if actual is not None and actual != declared:
                problems.append(
                    Problem(where, f"lessons/{name} has h1 {actual!r} but pages says {declared!r}")
                )

        route_ids = [route.get("id") for route in manifest.get("routes", [])]
        if manifest.get("default") not in route_ids:
            problems.append(Problem(where, f"default {manifest.get('default')!r} names no route"))

        for route in manifest.get("routes", []):
            rid = route.get("id", "?")
            kinds = route.get("kinds") or []
            if not kinds:
                problems.append(Problem(where, f"route {rid} declares no kinds"))
                continue

            listed = route_files(route)
            seen: set[str] = set()
            for name in listed:
                if name in seen:
                    problems.append(Problem(where, f"route {rid} lists lessons/{name} twice"))
                seen.add(name)
                if name not in pages:
                    problems.append(Problem(where, f"route {rid} lists lessons/{name}, which is not in pages"))

            expected = {name for name, page in pages.items() if page.get("kind") in kinds}
            for gap in sorted(expected - seen):
                problems.append(
                    Problem(where, f"route {rid} declares kind {pages[gap].get('kind')!r} but omits lessons/{gap}")
                )
    return problems


def check_pagers_match_the_owning_route() -> list[Problem]:
    """The committed pager is the whole of a lesson's navigation with scripting
    off, so it has to be the owning route's neighbours and not a stale guess."""
    problems: list[Problem] = []

    for course in course_directories():
        if not (course / "routes.js").is_file():
            continue
        manifest, failures = route_manifest(course)
        if failures:
            continue
        pages = manifest.get("pages", {})
        lessons_dir = course / "lessons"

        for name in sorted(pages):
            lesson = lessons_dir / name
            if not lesson.is_file():
                continue
            where = relative(lesson)
            route = owning_route(manifest, name)
            if route is None:
                problems.append(Problem(where, "no route contains this lesson"))
                continue

            match = PAGER_PATTERN.search(lesson.read_text(encoding="utf-8"))
            if match is None:
                problems.append(Problem(where, 'no <nav class="pager" data-pager-route="..."> block'))
                continue
            if match.group("route") != route.get("id"):
                problems.append(
                    Problem(where, f"pager claims route {match.group('route')!r}, "
                                   f"but {route.get('id')!r} owns this lesson")
                )
                continue

            order = route_files(route)
            at = order.index(name)
            expected = [
                order[at - 1] if at > 0 else "../index.html",
                order[at + 1] if at < len(order) - 1 else "../index.html",
            ]
            found = ANCHOR_HREF.findall(match.group("body"))
            if found != expected:
                problems.append(
                    Problem(where, f"pager links {found} but route {route.get('id')!r} wants {expected}")
                )
    return problems


def check_lessons_carry_zone_metadata() -> list[Problem]:
    """A routed course also runs the living-document mechanism: every lesson
    declares how current it is, so a stale page says so rather than looking new."""
    problems: list[Problem] = []

    for course in course_directories():
        if not (course / "routes.js").is_file():
            continue
        lessons_dir = course / "lessons"
        if not lessons_dir.is_dir():
            continue
        for lesson in sorted(lessons_dir.glob("*.html")):
            body = lesson.read_text(encoding="utf-8")
            for attribute in ("data-zone", "data-asof"):
                if attribute not in body:
                    problems.append(Problem(relative(lesson), f"no {attribute} on the lesson status block"))
    return problems


def check_course_map_sections_are_balanced() -> list[Problem]:
    """A course map's module sections must not nest inside one another.

    This is the failure with no symptom. A ``section.module`` that never closes
    still renders: the browser repairs the tree, every link still resolves, and
    ``gen_outline.py`` still finds every heading, because it splits the page at
    each ``.module-h`` rather than at each section. So the page looks right, the
    outline is right, and the pull request is green, while every module after
    the broken one has quietly become a *child* of it.

    What that costs is the document outline a screen reader navigates by, and
    the CSS, where a nested ``.module`` inherits spacing meant for a top-level
    one. It reached ``main`` twice before anything caught it, both times the
    same way: a card list ended with ``</a>`` and the next module's ``.module-h``
    followed immediately, with the ``</div></section>`` pair missing between them.

    Three mechanical assertions, because the first two alone let a case through:

    1. Every close tag matches the element it closes. A ``</section>`` written
       where a ``</div>`` belongs keeps the depth count balanced and is invisible
       to any check that only counts, so the tags are matched on a stack instead.
    2. ``<main>`` closes with nothing left open.
    3. Every ``section.module`` opens at the same depth as the first one on the
       page. Deliberately *relative* rather than fixed at zero, because
       ``llm-evolution-course`` wraps all twenty-nine of its module sections in
       per-route containers and opens every one at depth two, which is correct
       and must stay legal.
    """
    problems: list[Problem] = []

    # The hub landing page carries the same section.module shape as a course map
    # and is exposed to the same break, so it is checked alongside them.
    maps = [course / "index.html" for course in course_directories()]
    maps.append(REPO_ROOT / "index.html")

    for page in maps:
        if not page.is_file():
            continue
        source = HTML_COMMENT.sub("", page.read_text(encoding="utf-8"))
        body = MAIN_BLOCK.search(source)
        if body is None:
            continue

        # Line numbers are counted from the start of the file so that a reported
        # line is the line an editor jumps to.
        offset = source[: body.start("body")].count("\n") + 1
        text = body.group("body")

        stack: list[tuple[str, int]] = []
        opened_at: list[int] = []
        mismatched = False

        for tag in NESTING_TAG.finditer(text):
            line = offset + text[: tag.start()].count("\n")
            name = tag.group("tag").lower()
            if tag.group("close"):
                if not stack:
                    problems.append(
                        Problem(relative(page), f"line {line}: </{name}> closes nothing")
                    )
                    mismatched = True
                    break
                opened, opened_line = stack.pop()
                if opened != name:
                    problems.append(
                        Problem(
                            relative(page),
                            f"line {line}: </{name}> closes a <{opened}> opened on line {opened_line}",
                        )
                    )
                    mismatched = True
                    break
            else:
                if MODULE_SECTION.match(tag.group(0)):
                    opened_at.append(len(stack))
                stack.append((name, line))

        if mismatched:
            continue

        if stack:
            name, line = stack[0]
            problems.append(
                Problem(
                    relative(page),
                    f"{len(stack)} element(s) never closed inside main; the first is "
                    f"<{name}> opened on line {line}",
                )
            )

        if len(set(opened_at)) > 1:
            expected = opened_at[0]
            strays = sorted({depth for depth in opened_at if depth != expected})
            problems.append(
                Problem(
                    relative(page),
                    f"module sections open at mixed nesting depths {sorted(set(opened_at))}; "
                    f"the first opens at {expected} and {len(opened_at) - opened_at.count(expected)} "
                    f"open at {strays}, so a section above them never closed",
                )
            )

    return problems


def _titles() -> object:
    """``check_titles`` as a module, imported from beside this file.

    It sits in the same directory, which is on ``sys.path`` whenever this file
    is run as a script. The insert makes the import work when it is not, such as
    when a test imports this module by path.
    """
    directory = str(Path(__file__).resolve().parent)
    if directory not in sys.path:
        sys.path.insert(0, directory)
    import check_titles

    return check_titles


def check_titles_agree() -> list[Problem]:
    """A lesson's NAME must agree everywhere it is echoed.

    The name is what the course map calls the lesson. It is echoed into the rail
    ``gen_outline.py`` generates from that map, and into the ``.ttl`` of every
    pager pointing at the lesson. Edit one and a reader clicks a link expecting
    one page and lands on a differently named one, while every link still
    resolves and every other check here stays green.

    The page's ``h1`` is a *claim* rather than a name, by the content-page
    contract, and is deliberately not compared with any of them.

    The rules live in ``scripts/check_titles.py`` and are called from here rather
    than duplicated, so there is one definition of what a faithful title is. This
    runs inside ``validate_site.py`` on purpose: the Validate workflow already
    runs this file, so titles are gated with no change to ``.github/workflows``.

    Courses named in that script's ``SWEEP_PENDING`` are mid-sweep. Their defects
    are counted by :func:`waived_title_defects` and reported as debt rather than
    failing the run, so a sweep in flight does not block everyone. Every other
    course, and every course added later, gates at zero.
    """
    titles = _titles()
    problems: list[Problem] = []

    for course in course_directories():
        if course.name in titles.SWEEP_PENDING or course.name in titles.FROZEN:
            continue
        for kind, page, shown, wanted in titles.audit(course, 0, 9999):
            problems.append(
                Problem(
                    relative(course / "lessons" / page),
                    f"{kind} shows {shown!r} but the course map names it {wanted!r}",
                )
            )
    return problems


def waived_title_defects() -> dict[str, int]:
    """Title defects in courses still being swept, so the debt stays visible."""
    titles = _titles()
    waived: dict[str, int] = {}
    for course in course_directories():
        if course.name not in titles.SWEEP_PENDING and course.name not in titles.FROZEN:
            continue
        count = len(titles.audit(course, 0, 9999))
        if count:
            waived[course.name] = count
    return waived


def split_head(source: str) -> tuple[str, str]:
    """A page split at the end of its ``<head>``.

    Everything the design system needs runs before the first paint, so where a
    tag sits is as load-bearing as whether it is there at all. A page with no
    closing tag is treated as all head, which fails on its own terms below
    rather than passing by accident.
    """
    end = source.lower().find("</head>")
    return (source, "") if end == -1 else (source[:end], source[end:])


def check_pages_link_the_design_system() -> list[Problem]:
    """Every page reaches the one design system, at its own depth in the tree.

    There is one stylesheet and one script and every page links both, which is
    what lets the whole hub be restyled by editing two files. Nothing else in
    this validator can see that: a pull request could strip the ``<link>`` from
    every page and the deploy would sync an unstyled site to the bucket.

    Three facts are checked, and all three are the same defect wearing different
    clothes - a page authored from a stale template, or a find-and-replace that
    walked one directory too far.

    1. ``assets/hub.css`` is linked, in the head, at the page's own depth.
    2. ``assets/hub.js`` is loaded, in the head. It writes ``data-mode``,
       ``data-palette``, ``data-design`` and ``data-course`` onto ``<html>``
       before the first paint, so a copy that runs after ``</head>`` means a
       colour flash, or a flash of the wrong form, on every load.
    3. A course that ships an ``assets/course-extras.css`` links it from every
       one of its pages, after the hub sheet and never before it. Those three
       sheets restyle shared elements, so a page that misses the link is styled
       by rules its neighbours do not have.
    """
    problems: list[Problem] = []
    extras_courses = {
        course.name
        for course in course_directories()
        if (course / "assets" / "course-extras.css").is_file()
    }

    for page in html_pages():
        parts = page.relative_to(REPO_ROOT).parts
        head, tail = split_head(page.read_text(encoding="utf-8", errors="replace"))
        head_links = LINK_PATTERN.findall(head)
        hub_css = "../" * (len(parts) - 1) + "assets/hub.css"

        for asset in ("hub.css", "hub.js"):
            wanted = "../" * (len(parts) - 1) + f"assets/{asset}"
            in_head = [href for href in head_links if href.endswith(f"assets/{asset}")]
            if wanted in in_head:
                continue
            if in_head:
                problems.append(
                    Problem(relative(page), f"reaches {asset} at the wrong depth -> {in_head[0]}, expected {wanted}")
                )
            elif any(href.endswith(f"assets/{asset}") for href in LINK_PATTERN.findall(tail)):
                problems.append(Problem(relative(page), f"loads {asset} after </head>; it must run before the first paint"))
            else:
                problems.append(Problem(relative(page), f"does not reach assets/{asset}; the page would publish unstyled"))

        if parts[0] not in extras_courses:
            continue
        wanted_extras = "../" * (len(parts) - 2) + "assets/course-extras.css"
        if wanted_extras not in head_links:
            problems.append(
                Problem(relative(page), f"its course ships a course-extras.css but the page does not link {wanted_extras}")
            )
        elif hub_css in head_links and head_links.index(wanted_extras) < head_links.index(hub_css):
            problems.append(
                Problem(relative(page), "links course-extras.css before hub.css; the course sheet layers after the hub sheet")
            )
    return problems


SPINE_BLOCK: re.Pattern[str] = re.compile(r'<nav class="spine">.*?</nav>', re.DOTALL)
SPINE_ANCHOR: re.Pattern[str] = re.compile(r"<a\b(?P<attributes>[^>]*)>", re.IGNORECASE)
CLASS_VALUE: re.Pattern[str] = re.compile(r'class="(?P<names>[^"]*)"', re.IGNORECASE)


def spine_anchor_classes(page: Path) -> list[frozenset[str]] | None:
    """The class list of every anchor in a page's topbar, in document order.

    ``None`` means the page has no topbar at all, which is not this check's
    business.
    """
    block = SPINE_BLOCK.search(page.read_text(encoding="utf-8", errors="replace"))
    if block is None:
        return None
    classes: list[frozenset[str]] = []
    for anchor in SPINE_ANCHOR.finditer(block.group(0)):
        names = CLASS_VALUE.search(anchor.group("attributes"))
        classes.append(frozenset(names.group("names").split()) if names else frozenset())
    return classes


def check_spine_keeps_a_link_on_a_phone() -> list[Problem]:
    """Below 720px the topbar keeps the wordmark and the page's last link.

    The row cannot hold more than that: ``hub.css`` hides every earlier link at
    that width, because six links only fit on a phone by being squeezed
    narrower than their own text, which is the defect this rule was written to
    end. So the last anchor in a spine is the whole of a phone reader's
    navigation, and it is the one anchor that may not also carry ``hide-sm`` -
    that class hides it at the same breakpoint, and the reader is left with a
    wordmark that points at the page it is already on.

    Nothing else can see it. The page is valid HTML, every link resolves, and
    the topbar looks complete on a laptop. It is checked here rather than in
    the computed-style harness because it is a fact about markup, and because
    it is the seam every page of this hub already passes through.
    """
    problems: list[Problem] = []
    for page in html_pages():
        classes = spine_anchor_classes(page)
        if classes is None:
            continue
        links = [names for names in classes if "home" not in names]
        if links and "hide-sm" in links[-1]:
            problems.append(
                Problem(
                    relative(page),
                    "the last topbar link carries hide-sm, so below 720px the page has no "
                    "topbar link at all; drop the class or put a link after it",
                )
            )
    return problems


# ---------------------------------------------------------------------------
# The design system's own three checks: the axis registry, token completeness
# and the three-layer property rule. Everything below parses the two shared
# asset files and needs no browser, which is why it belongs here rather than in
# the computed-style harness.
# ---------------------------------------------------------------------------

HUB_CSS: Path = REPO_ROOT / "assets" / "hub.css"
HUB_JS: Path = REPO_ROOT / "assets" / "hub.js"

# The attributes ``hub.js`` may write on ``<html>``. Three are the reader's own
# axes, one is derived from the URL and one from the hostname. A control that
# writes anything else has stepped outside the axis contract.
AXIS_ATTRIBUTES: frozenset[str] = frozenset(
    {"data-mode", "data-palette", "data-design", "data-course", "data-env"}
)

CSS_COMMENT: re.Pattern[str] = re.compile(r"/\*.*?\*/", re.DOTALL)

DESIGN_REGISTRY: re.Pattern[str] = re.compile(r"var DESIGNS\s*=\s*\[(?P<body>.*?)\];", re.DOTALL)

DESIGN_KEY: re.Pattern[str] = re.compile(r"key:\s*'(?P<key>[^']+)'")

DESIGN_ARM: re.Pattern[str] = re.compile(r':root\[data-design="(?P<key>[^"]+)"\]\s*$')

DESIGN_ATTRIBUTE: re.Pattern[str] = re.compile(r'\[data-design="(?P<key>[^"]*)"\]')

CUSTOM_DECLARATION: re.Pattern[str] = re.compile(r"(?P<name>--[a-z0-9-]+)\s*:(?P<value>[^;}]*)")

USER_PROPERTY: re.Pattern[str] = re.compile(r"var\(\s*(?P<name>--[a-z0-9-]+-user)\b")

# A resolution line reads the reader's value as the head of its own fallback
# chain. What follows the comma is the stylesheet's own answer - a `-default`
# for a token a control sets directly, a computation for a derived axis - and
# is not this check's business. What is its business is that nothing else in
# the declaration reaches the reader's value.
RESOLUTION_HEAD: re.Pattern[str] = re.compile(r"^var\(\s*--[a-z0-9-]+-user\s*,")

ROOT_ALIAS: re.Pattern[str] = re.compile(
    r"var\s+(?P<name>[A-Za-z_$][\w$]*)\s*=\s*document\.documentElement\b"
)

READING_PROPERTY: re.Pattern[str] = re.compile(r"prop:\s*'(?P<name>--[a-z0-9-]+)'")

CUSTOM_READ: re.Pattern[str] = re.compile(r"var\(\s*(?P<name>--[a-z0-9-]+)")

PAGE_AT_RULE: re.Pattern[str] = re.compile(r"@page\s*\{")

PRINT_AT_RULE: re.Pattern[str] = re.compile(r"@media\s+print\s*\{")

MEDIA_QUERY: re.Pattern[str] = re.compile(r"@media(?P<prelude>[^{]*)\{")


@dataclass(frozen=True)
class Rule:
    """One flat CSS rule: its selector list and the declarations inside it."""

    selector: str
    body: str


def css_rules(source: str) -> list[Rule]:
    """Every rule in a stylesheet, with at-rules flattened into their contents.

    Comments go first, so a selector quoted in prose is never mistaken for a
    real one, and brace depth is tracked so a rule inside ``@media`` is found
    rather than swallowed by the query around it.

    An at-rule body may hold declarations *and* nested rules - ``@page`` holds
    ``margin`` beside its margin boxes - and those loose declarations sit in
    front of the next rule's selector. Everything up to the last semicolon is
    therefore dropped rather than glued on: without it ``@page`` handed back
    ``Rule("margin: 14mm; @bottom-left", ...)``, a selector no check can read
    and one that could carry a token declaration past every check here.
    """
    rules: list[Rule] = []

    def walk(chunk: str) -> None:
        start = 0
        depth = 0
        head = 0
        for index, character in enumerate(chunk):
            if character == "{":
                if depth == 0:
                    head = index
                depth += 1
            elif character == "}":
                depth -= 1
                if depth:
                    continue
                selector = chunk[start:head].rsplit(";", 1)[-1].strip()
                body = chunk[head + 1 : index]
                walk(body) if selector.startswith("@") else rules.append(Rule(selector, body))
                start = index + 1

    walk(CSS_COMMENT.sub("", source))
    return rules


def hub_rules() -> list[Rule]:
    """``assets/hub.css``, parsed once for the three checks that read it."""
    if not _PARSED_HUB_CSS:
        _PARSED_HUB_CSS.extend(css_rules(HUB_CSS.read_text(encoding="utf-8")))
    return _PARSED_HUB_CSS


_PARSED_HUB_CSS: list[Rule] = []


def declares_a_design(rule: Rule) -> str | None:
    """The design a rule declares the tokens of, or ``None``.

    A design block carries the attribute as the whole of one selector arm.
    ``:root[data-design="press"] .card`` styles one element and is not the
    design's token declaration, so it is not one of these.
    """
    for arm in rule.selector.split(","):
        found = DESIGN_ARM.search(arm.strip())
        if found:
            return found.group("key")
    return None


def declared_properties(body: str) -> set[str]:
    """The custom properties one rule declares. A read has no colon after it."""
    return {match.group("name") for match in CUSTOM_DECLARATION.finditer(body)}


def registered_designs() -> list[str]:
    """The design keys ``hub.js`` offers, in registry order.

    The first entry is the registered default: an unknown stored key falls back
    to it, so it is the design a reader lands on unless they choose another.
    """
    match = DESIGN_REGISTRY.search(HUB_JS.read_text(encoding="utf-8"))
    return [] if match is None else [key.group("key") for key in DESIGN_KEY.finditer(match.group("body"))]


def design_blocks() -> dict[str, Rule]:
    """Every ``:root[data-design="..."]`` token block in ``hub.css``."""
    return {key: rule for rule in hub_rules() if (key := declares_a_design(rule))}


def check_design_registry_and_blocks() -> list[Problem]:
    """The design registry and the design blocks name the same set.

    ``hub.js`` holds the registry the picker is built from and the head phase
    validates a stored key against; ``hub.css`` holds one token block per
    design. Neither half can check the other at runtime, and each failure is
    silent in its own way. A key with no block is a design the picker offers
    that resolves to nothing, so a reader who chooses it gets the default and no
    explanation. A block with no key is a design nobody can reach: dead weight
    that reads as working code and goes stale unnoticed.
    """
    problems: list[Problem] = []
    registry = registered_designs()
    blocks = design_blocks()

    if not registry:
        return [Problem("assets/hub.js", "no DESIGNS registry found; the design axis has no registered value")]
    if not blocks:
        return [Problem("assets/hub.css", 'no :root[data-design="..."] block found; the design axis resolves to nothing')]

    for key in registry:
        if key not in blocks:
            problems.append(
                Problem("assets/hub.css", f'design "{key}" is registered in hub.js but has no :root[data-design="{key}"] block')
            )
    for key in sorted(blocks):
        if key not in registry:
            problems.append(
                Problem("assets/hub.js", f'design "{key}" has a block in hub.css but no entry in the DESIGNS registry; nothing can reach it')
            )

    # Any other spelling of the attribute names a design too - a descendant
    # selector inside a media query, most easily - and must name a registered one.
    for rule in hub_rules():
        if declares_a_design(rule):
            continue  # already compared against the registry above
        for found in DESIGN_ATTRIBUTE.finditer(rule.selector):
            if found.group("key") not in registry:
                problems.append(
                    Problem("assets/hub.css", f'selector "{rule.selector[:60]}" names design "{found.group("key")}", which is not registered')
                )
    return problems


def check_design_token_completeness() -> list[Problem]:
    """Every design declares the whole token set, and owns it alone.

    Two failures, and both leave a page that looks nearly right.

    A design that declares only part of the set inherits the rest from the bare
    ``:root`` arm. That is the trap the theme tokens sprang once, when a token
    added to ``:root`` alone silently kept its light value in dark mode,
    multiplied here by the number of designs. So the default design's block is
    the contract and every other design matches it exactly, in both directions:
    a token only one design declares is a token every other design is missing.

    And a design-axis token is declared in a design block and nowhere else. A
    design block is ``(0,2,0)`` against a bare ``:root`` at ``(0,1,0)``, so a
    second declaration of one of these tokens - in a media query, most easily -
    would be out-argued in every viewport and that override would go silently
    dead. ``--fs-body-default`` in the 720px block is the shape of the bug, and
    is why the body size is resolved outside the design block rather than in it.
    """
    problems: list[Problem] = []
    registry = registered_designs()
    blocks = design_blocks()
    if not registry or registry[0] not in blocks:
        return problems  # the registry check reports this; do not report it twice

    contract = declared_properties(blocks[registry[0]].body)
    if not contract:
        return [Problem("assets/hub.css", f'the default design "{registry[0]}" declares no tokens')]

    for key in registry[1:]:
        rule = blocks.get(key)
        if rule is None:
            continue
        declared = declared_properties(rule.body)
        for label, names in (("does not declare", contract - declared), ("declares, and the default design does not", declared - contract)):
            if names:
                listing = ", ".join(sorted(names)[:6]) + (" ..." if len(names) > 6 else "")
                problems.append(Problem("assets/hub.css", f'design "{key}" {label} {listing}'))

    for rule in hub_rules():
        if declares_a_design(rule):
            continue
        for name in sorted(declared_properties(rule.body) & contract):
            problems.append(
                Problem(
                    "assets/hub.css",
                    f'{name} is a design-axis token and is declared again by "{rule.selector[:60]}"; '
                    "a design block out-specifies that rule and would kill it silently",
                )
            )
    return problems


def at_rule_bodies(source: str, opener: re.Pattern[str]) -> list[str]:
    """Every body of the at-rule ``opener`` matches, with braces balanced.

    ``css_rules`` flattens at-rules away, and a ``@page`` margin box is nothing
    but declarations, so it leaves no rule behind for the two checks below to
    read. This reads the raw block instead.
    """
    stripped = CSS_COMMENT.sub("", source)
    bodies: list[str] = []
    for found in opener.finditer(stripped):
        depth = 0
        for index in range(found.end() - 1, len(stripped)):
            if stripped[index] == "{":
                depth += 1
            elif stripped[index] == "}":
                depth -= 1
                if depth == 0:
                    bodies.append(stripped[found.end() : index])
                    break
    return bodies


def page_margin_reads() -> set[str]:
    """Every custom property a ``@page`` block reads."""
    return {
        match.group("name")
        for body in at_rule_bodies(HUB_CSS.read_text(encoding="utf-8"), PAGE_AT_RULE)
        for match in CUSTOM_READ.finditer(body)
    }


def print_declares() -> set[str]:
    """Every custom property declared inside ``@media print``."""
    return {
        match.group("name")
        for body in at_rule_bodies(HUB_CSS.read_text(encoding="utf-8"), PRINT_AT_RULE)
        for match in CUSTOM_DECLARATION.finditer(body)
    }


def page_identity_properties() -> set[str]:
    """The properties ``hub.js`` may write on ``<html>`` that are not the
    reader's.

    A ``@page`` margin box can reach nothing about the document except a custom
    property on the root element - not its title, not a heading, and in Chrome
    not ``string()`` either, which renders on the first page and then stops. So
    the identity of a printed sheet has to arrive as a custom property, and
    that is the single exception to the rule below that ``hub.js`` writes only
    reader properties.

    The exception is granted by construction rather than by a list, and it
    needs both halves present: the property is read by a ``@page`` block, and
    it is also declared inside ``@media print``, which is the fallback that
    keeps the foot printing on a page with the script removed. A property with
    only one of the two is not an identity and gets no exception.
    """
    return page_margin_reads() & print_declares()


def stylesheets() -> list[Path]:
    """The hub sheet and every course sheet layered after it."""
    return [HUB_CSS] + sorted(REPO_ROOT.glob("*/assets/course-extras.css"))


def check_width_queries_name_a_medium() -> list[Problem]:
    """A width media query says which medium it is about.

    A width feature is answered by the page box in print, and the printed page
    box is narrow: A4 inside the browser's own margins is about 717px and US
    Letter about 739px. An unqualified ``@media (max-width: 720px)`` therefore
    applies to one paper and not the other, and an unqualified
    ``@media (max-width: 1040px)`` applies to both - which is how the rail's
    drawer arm, and the fixed 35%-black scrim it paints, reached every sheet of
    every printed lesson. Nothing on screen was wrong, so nothing on screen
    could catch it.

    The rule is therefore that a width query names ``screen`` or ``print``
    rather than leaving the medium open. It is checked here rather than in the
    computed-style harness because the harness holds the viewport at 1280px:
    the narrow arms do not match there in any medium, so the one state that
    shows the defect is the one state it cannot capture.
    """
    problems: list[Problem] = []
    for sheet in stylesheets():
        source = CSS_COMMENT.sub("", sheet.read_text(encoding="utf-8"))
        for found in MEDIA_QUERY.finditer(source):
            prelude = " ".join(found.group("prelude").split())
            if "width" not in prelude:
                continue
            if re.search(r"\b(screen|print|all)\b", prelude):
                continue
            problems.append(
                Problem(
                    str(sheet.relative_to(REPO_ROOT)),
                    f'"@media {prelude}" names no medium, so the printed page box answers it too; '
                    "say `screen and` unless paper is meant",
                )
            )
    return problems


def check_page_margin_boxes() -> list[Problem]:
    """Every property a ``@page`` margin box reads is declared somewhere.

    A margin box whose ``content`` resolves to nothing prints an empty running
    foot. No error is raised, no check downstream can see it, and the defect is
    invisible on screen by definition - it exists only on paper, which is the
    render state nobody looks at. So the declaration is checked here.
    """
    declared: set[str] = set()
    for rule in hub_rules():
        declared |= declared_properties(rule.body)
    declared |= print_declares()

    return [
        Problem("assets/hub.css", f"@page reads {name}, which nothing in the stylesheet declares; the margin box prints empty")
        for name in sorted(page_margin_reads() - declared)
    ]


def check_three_layer_rule() -> list[Problem]:
    """The reader's layer stays an input to a token and never a competitor.

    A configurable value exists in three layers: a ``-default`` the stylesheet
    owns, a ``--*-user`` property only ``hub.js`` writes inline on ``<html>``,
    and one resolved token that every rule reads. The rule exists because an
    inline ``--measure`` beat every stylesheet rule that was not ``!important``
    and pinned a reader who had widened the column, and it can rot from either
    end.

    A rule in ``hub.css`` that reads a ``--*-user`` property re-creates the trap
    one layer down, so only the resolution lines may name one. A control in
    ``hub.js`` that writes anything on ``<html>`` other than a ``--*-user``
    property or a registered axis attribute is a reader value no design can ever
    out-argue.

    There is one exception and it is not a reader value at all: the identity a
    ``@page`` margin box prints on every sheet, which can reach the document
    only as a custom property. ``page_identity_properties`` derives it from the
    stylesheet rather than from a list here, so the exception cannot outlive the
    mechanism that needs it.

    The stylesheet may resolve a ``--*-user`` layer no control writes yet - the
    reading controls arrive after the tokens they read - but a control that
    writes a name nothing resolves is a preference that reaches no pixel.

    What a resolution line is allowed to look like. The check first read the
    single literal ``--x: var(--x-user, var(--x-default))``, which was every
    resolution line the sheet then had. A derived axis cannot take that shape
    and the specification writes both exceptions out: ``--fs-body-ref`` resolves
    ``--fs-body-user`` under a different name because the reader's number is on
    a reference scale, and ``--lh-body`` falls back to a computation rather than
    to a bare default because the leading nudges with the measure. So the form
    is stated by its three properties instead of by one spelling, and each is
    the reason the rule exists:

    - only a **custom property** may read one, never ``max-width:
      var(--measure-user)``, which is the same defect and the likelier spelling;
    - it reads **exactly one**, as the head of its own fallback chain, so the
      reader's value is an input to that token and to nothing else;
    - and **exactly one declaration in the sheet reads it**, which is what the
      definite article in "the resolution line" means. That last one the single
      literal never checked at all: two rules could both carry it and both pass.
    """
    problems: list[Problem] = []
    source = HUB_JS.read_text(encoding="utf-8")

    resolved: dict[str, list[str]] = {}
    for rule in hub_rules():
        # Every declaration, not only the custom ones: `max-width:
        # var(--measure-user)` on an ordinary property is the same defect and
        # the more likely spelling of it.
        for declaration in rule.body.split(";"):
            read = {match.group("name") for match in USER_PROPERTY.finditer(declaration)}
            if not read:
                continue
            name, _, value = declaration.partition(":")
            name = name.strip()
            user = next(iter(read))
            if name.startswith("--") and len(read) == 1 and RESOLUTION_HEAD.match(value.strip()):
                resolved.setdefault(user, []).append(name)
                continue
            problems.append(
                Problem(
                    "assets/hub.css",
                    f'"{name}" reads {", ".join(sorted(read))} outside a resolution line; a reader value may be '
                    "read only by one custom property, once, as var(--x-user, <the default or the derivation>)",
                )
            )

    for user, names in sorted(resolved.items()):
        if len(names) > 1:
            problems.append(
                Problem(
                    "assets/hub.css",
                    f'{user} is resolved by {len(names)} declarations ({", ".join(sorted(names))}); '
                    "a reader value has one resolution line and every rule reads that",
                )
            )

    aliases = {match.group("name") for match in ROOT_ALIAS.finditer(source)}
    written: set[str] = set()
    for alias in sorted(aliases):
        for attribute in re.finditer(rf"\b{re.escape(alias)}\.(?:set|remove)Attribute\(\s*'([^']*)'", source):
            if attribute.group(1) not in AXIS_ATTRIBUTES:
                problems.append(
                    Problem("assets/hub.js", f'writes "{attribute.group(1)}" on <html>, which is not a registered axis attribute')
                )
        for call in re.finditer(rf"\b{re.escape(alias)}\.style\.(?:set|remove)Property\(\s*(?P<argument>[^,)]+)", source):
            argument = call.group("argument").strip()
            if argument.startswith("'") and argument.endswith("'"):
                written.add(argument.strip("'"))
            elif argument.endswith(".prop"):
                # The reading table's own field. Every value it can hold is read here.
                written |= {match.group("name") for match in READING_PROPERTY.finditer(source)}
            else:
                problems.append(
                    Problem(
                        "assets/hub.js",
                        f"writes a custom property on <html> named by `{argument}`, which this check cannot read; "
                        "name it with a literal or through the reading table's `prop` field",
                    )
                )

    identities = page_identity_properties()
    for name in sorted(written):
        if name in identities:
            continue  # the printed sheet's identity; see page_identity_properties
        if not name.endswith("-user"):
            problems.append(
                Problem("assets/hub.js", f"writes {name} on <html>; a reader control may write only a --*-user property")
            )
        elif name not in resolved:
            problems.append(
                Problem("assets/hub.js", f"writes {name}, which no resolution line in hub.css reads; the reader's value reaches nothing")
            )
    return problems


def check_contrast_floor() -> list[Problem]:
    """The accessibility floor, over the colours ``hub.css`` states outright.

    A ground of a given lightness bounds the best contrast any ink can reach on
    it, and that bound is arithmetic. The framework prevents the dead band
    rather than warning about it: the ground is a discrete registered choice, so
    no reader input can land inside the band, and this is the check that keeps
    the registered set outside it.

    ``scripts/contrast.py`` carries the arithmetic, the three checks and a
    ``--self-test`` that proves each one fails on a deliberately bad input. It
    lives beside this file rather than inside it because the browser half of the
    same floor imports it too, and because a check with its own command is a
    check a palette author can run while choosing a colour.
    """
    registry = contrast.registrations()
    if not registry:
        return [Problem("assets/hub.css", "no palette block found; the parser and the stylesheet disagree")]
    return [
        Problem(f"assets/hub.css [{finding.check} {finding.where}]", finding.detail)
        for finding in contrast.check_all(registry)
    ]

NAMED_TOKEN: re.Pattern[str] = re.compile(r'data-(?:token|spec)="(?P<name>--[a-z0-9-]+)"')


def declared_tokens() -> set[str]:
    """Every custom property ``assets/hub.css`` declares, anywhere in the file."""
    return {name for rule in hub_rules() for name in declared_properties(rule.body)}


def check_named_tokens_exist() -> list[Problem]:
    """A page that names a token names one that is there.

    ``design-system/index.html`` documents the framework by naming its tokens:
    ``data-token`` marks the cell the page fills with the resolved value, and
    ``data-spec`` marks the specimen its own stylesheet paints with that token.
    Both are a reference into ``assets/hub.css``, and a reference can rot.

    Nothing else would catch it. A renamed token leaves a ``var()`` that
    substitutes to nothing, so the specimen paints nothing and the value cell
    reports that the token is not set - on a page whose whole job is to be
    right about what exists. The page still renders, every link still resolves,
    and the computed-style harness records the new emptiness as the expected
    answer the moment anyone re-records it.

    So the check is on the name rather than on the pixel, it runs over every
    page rather than over one, and it costs one pass of a regular expression.

    Stylesheets are read as well as pages, because half of the reference lives
    there: an attribute selector is how one specimen is painted with one token,
    and a selector that matches nothing is the same rot with no page to show it.
    """
    declared = declared_tokens()
    if not declared:
        return [Problem("assets/hub.css", "declares no custom properties; the token layer is missing")]

    sheets = [
        sheet
        for sheet in REPO_ROOT.rglob("*.css")
        if not any(part.startswith(".") for part in sheet.relative_to(REPO_ROOT).parts)
        and "node_modules" not in sheet.parts
    ]

    problems: list[Problem] = []
    for source_file in html_pages() + sorted(sheets):
        source = source_file.read_text(encoding="utf-8", errors="replace")
        for name in sorted({match.group("name") for match in NAMED_TOKEN.finditer(source)}):
            if name not in declared:
                problems.append(
                    Problem(
                        relative(source_file),
                        f"names {name}, which assets/hub.css does not declare; "
                        "a renamed token leaves the reference describing something that is gone",
                    )
                )
    return problems


def check_no_local_markdown_links() -> list[Problem]:
    """The deploy syncs the repository minus ``*.md``, so a page that links a
    local Markdown file works from disk and returns a 404 on the published site."""
    problems: list[Problem] = []

    for page in html_pages():
        for link in read_links(page):
            if not is_local(link):
                continue
            if strip_suffixes(link).lower().endswith(".md"):
                problems.append(
                    Problem(relative(page), f"links a local Markdown file, which is never published -> {link}")
                )
    return problems


def check_local_links_resolve() -> list[Problem]:
    problems: list[Problem] = []

    for page in html_pages():
        for link in read_links(page):
            if not is_local(link):
                continue
            target_path = strip_suffixes(link)
            if not target_path:
                continue
            target = (page.parent / target_path).resolve()
            if not target.exists():
                problems.append(Problem(relative(page), f"broken link -> {link}"))
    return problems


def _js_data_files(assignment: re.Pattern[str]) -> list[Path]:
    """Every committed .js file carrying a given window.* data assignment."""
    return sorted(
        path
        for path in REPO_ROOT.rglob("*.js")
        if not any(part.startswith(".") for part in path.relative_to(REPO_ROOT).parts)
        and "node_modules" not in path.parts
        and assignment.search(path.read_text(encoding="utf-8"))
    )


def _vendor_url_problems(where: str, url: object) -> list[Problem]:
    """Well-formedness for one vendor link. Offline and deterministic."""
    if not isinstance(url, str) or not url.strip():
        return [Problem(where, f"vendor link is missing or empty -> {url!r}")]
    parts = urlsplit(url.strip())
    if parts.scheme != "https" or not parts.netloc or " " in url.strip():
        return [Problem(where, f"vendor link must be a well-formed https URL -> {url!r}")]
    return []


def _fetch_vendor_link(url: str, timeout: float = 20.0) -> str | None:
    """Fetch one vendor link, returning why it is dead or None if it resolves.

    A HEAD is tried first; servers that answer 405/501 to HEAD are retried with
    GET. Only an HTTP error status or an unreachable host counts as dead - a
    redirect is the vendor moving a page, which still serves the reader.
    """
    headers = {"User-Agent": "course-hub-link-check/1 (site validator)"}
    for method in ("HEAD", "GET"):
        req = _urlrequest.Request(url, headers=headers, method=method)
        try:
            with _urlrequest.urlopen(req, timeout=timeout):
                return None
        except HTTPError as error:
            if error.code in (405, 501) and method == "HEAD":
                continue
            return f"HTTP {error.code}"
        except URLError as error:
            return f"unreachable ({error.reason})"
        except TimeoutError:
            return "timed out"
    return "no usable response"


def _matrix_problems(where: str, data: object) -> list[Problem]:
    """The structural checks on one parsed capability-matrix payload.

    The taxonomy - twenty-four areas and their keys - is the join key four
    independently researched cloud columns meet on. A row that is not a key,
    or a key that is not a row, splits the comparison silently; that is what
    most of this function exists to prevent.
    """
    problems: list[Problem] = []
    if not isinstance(data, dict):
        return [Problem(where, "window.CLOUD_CAPABILITY_MATRIX is not an object")]

    clouds = data.get("clouds")
    if not isinstance(clouds, list) or len(clouds) != 4:
        return [Problem(where, f"clouds must be exactly the four columns {sorted(MATRIX_CLOUDS)}")]
    cloud_keys: list[str] = []
    for i, c in enumerate(clouds):
        key = c.get("key") if isinstance(c, dict) else None
        if key not in MATRIX_CLOUDS:
            problems.append(
                Problem(where, f"clouds[{i}] key {key!r} is not one of {sorted(MATRIX_CLOUDS)}")
            )
        else:
            cloud_keys.append(key)
    if len(set(cloud_keys)) != len(cloud_keys):
        problems.append(Problem(where, "a cloud column appears twice"))
    if set(cloud_keys) != MATRIX_CLOUDS:
        problems.append(
            Problem(where, f"clouds must cover exactly {sorted(MATRIX_CLOUDS)}, got {cloud_keys}")
        )
        return problems

    domains = data.get("domains")
    if not isinstance(domains, list) or len(domains) != MATRIX_DOMAIN_COUNT:
        problems.append(
            Problem(where, f"the taxonomy has {MATRIX_DOMAIN_COUNT} areas; got "
                           f"{len(domains) if isinstance(domains, list) else 'no list'}")
        )
        return problems

    home_domain: dict[str, str] = {}
    seen_slugs: set[str] = set()
    for d in domains:
        if not isinstance(d, dict):
            problems.append(Problem(where, "a taxonomy area is not an object"))
            continue
        slug = d.get("slug")
        if not isinstance(slug, str) or not KEBAB.match(slug):
            problems.append(Problem(where, f"area slug {slug!r} is not kebab-case"))
            continue
        if slug in seen_slugs:
            problems.append(Problem(where, f"area {slug} appears twice"))
        seen_slugs.add(slug)
        keys = d.get("keys")
        if not isinstance(keys, list) or not keys:
            problems.append(Problem(where, f"area {slug} carries no capability keys"))
            continue
        for k in keys:
            if not isinstance(k, str) or not KEBAB.match(k):
                problems.append(Problem(where, f"capability key {k!r} in {slug} is not kebab-case"))
            elif k in home_domain:
                problems.append(Problem(where, f"capability key {k} belongs to both {home_domain[k]} and {slug}"))
            else:
                home_domain[k] = slug

    rows = data.get("rows")
    if not isinstance(rows, list):
        problems.append(Problem(where, "rows is not a list"))
        return problems

    seen_rows: dict[str, int] = {}
    # A cross-reference names the row the capability actually lives in. It can
    # point forwards, so the targets are resolved once every row is known.
    references: list[tuple[str, str, str, str]] = []
    row_cells: dict[str, dict] = {}
    for i, row in enumerate(rows):
        at = f"{where}:rows[{i}]"
        if not isinstance(row, dict):
            problems.append(Problem(at, "row is not an object"))
            continue
        key = row.get("key")
        if not isinstance(key, str) or not KEBAB.match(key):
            problems.append(Problem(at, f"row key {key!r} is not kebab-case"))
            continue
        if key in seen_rows:
            problems.append(
                Problem(at, f"capability {key} has two rows (first at index {seen_rows[key]})")
            )
        seen_rows[key] = i
        row_cells[key] = row.get("cells") if isinstance(row.get("cells"), dict) else {}
        if key not in home_domain:
            problems.append(
                Problem(at, f"row names capability {key}, which no taxonomy area declares - an orphan row")
            )
        domain = row.get("domain")
        expected_home = home_domain.get(key)
        if domain != expected_home:
            problems.append(
                Problem(at, f"row {key} sits in area {domain!r} but the taxonomy files it under {expected_home!r}")
            )

        cells = row.get("cells")
        if not isinstance(cells, dict):
            problems.append(Problem(at, f"row {key} carries no cells object"))
            continue
        missing = [c for c in cloud_keys if c not in cells]
        extra = [c for c in cells if c not in MATRIX_CLOUDS]
        if missing:
            problems.append(Problem(at, f"row {key} has no cell for {', '.join(sorted(missing))}"))
        for c in extra:
            problems.append(Problem(at, f"row {key} carries a cell for unknown cloud {c!r}"))

        for c in [c for c in cloud_keys if c in cells]:
            cell_at = f"{at}:cells[{c}]"
            cell = cells[c]
            state = cell.get("state") if isinstance(cell, dict) else None
            if state not in CELL_STATES:
                problems.append(
                    Problem(cell_at, f"cell state {state!r} is not one of "
                                     f"{' / '.join(sorted(CELL_STATES))}")
                )
                continue
            if state in ("absent", "elsewhere") and not (
                isinstance(cell.get("reason"), str) and cell["reason"].strip()
            ):
                owed = "a declared absence" if state == "absent" else "a cross-reference"
                problems.append(
                    Problem(cell_at, f"{owed} in row {key} ({c}) owes a reason")
                )
            if state == "elsewhere":
                target = cell.get("see")
                if target is not None:
                    if not isinstance(target, str) or not KEBAB.match(target):
                        problems.append(
                            Problem(cell_at, f"cross-reference target {target!r} is not a capability key")
                        )
                    else:
                        references.append((cell_at, key, c, target))
            if state == "service":
                services = cell.get("services")
                if not isinstance(services, list) or not services:
                    problems.append(
                        Problem(cell_at, f'a "service" cell in row {key} ({c}) carries no services')
                    )
                    continue
                for j, svc in enumerate(services):
                    svc_at = f"{cell_at}.services[{j}]"
                    if not isinstance(svc, dict) or not (
                        isinstance(svc.get("name"), str) and svc["name"].strip()
                    ):
                        problems.append(Problem(svc_at, "service has no name"))
                    problems.extend(_vendor_url_problems(svc_at, svc.get("doc_url") if isinstance(svc, dict) else None))

    # A cross-reference is a promise that the capability is somewhere the reader
    # can reach. Pointing at a row that does not exist, at the cell itself, or at
    # a cell that is not a service on that same cloud breaks the promise while
    # still rendering as a confident sentence.
    for cell_at, key, c, target in references:
        if target not in row_cells:
            problems.append(
                Problem(cell_at, f"row {key} ({c}) says the capability lives in {target}, "
                                 f"which is not a row in the matrix")
            )
            continue
        if target == key:
            problems.append(
                Problem(cell_at, f"row {key} ({c}) cross-references itself")
            )
            continue
        landing = row_cells[target].get(c)
        landing_state = landing.get("state") if isinstance(landing, dict) else None
        if landing_state != "service":
            problems.append(
                Problem(cell_at, f"row {key} ({c}) says the capability lives in {target}, "
                                 f"but {c} carries no service there (it is {landing_state!r})")
            )

    unrepresented = sorted(set(home_domain) - set(seen_rows))
    for k in unrepresented:
        problems.append(
            Problem(where, f"taxonomy key {k} has no row - the matrix cannot render its comparison")
        )

    return problems


def check_comparison_matrix() -> list[Problem]:
    """The capability-matrix gate: taxonomy integrity, complete rows, honest
    cells, widget binding, and well-formed vendor links.

    The matrix data lives in ``window.CLOUD_CAPABILITY_MATRIX``, and the widget
    renders inside whatever page declares the documented ``figure.cmatrix``
    frame. Both ends are checked against each other: a data file no page binds
    to is invisible weight, and a frame with no data file renders as a
    broken-page note rather than a matrix.
    """
    problems: list[Problem] = []

    # Which published pages declare the frame, and which local .js files each loads.
    frames: dict[Path, set[Path]] = {}
    for page in html_pages():
        body = page.read_text(encoding="utf-8", errors="replace")
        if MATRIX_FRAME not in body:
            continue
        loaded: set[Path] = set()
        for link in LINK_PATTERN.findall(body):
            if not is_local(link):
                continue
            target = (page.parent / strip_suffixes(link)).resolve()
            if target.suffix == ".js" and target.is_file():
                loaded.add(target)
        frames[page] = loaded

    data_files = _js_data_files(MATRIX_ASSIGNMENT)
    if not data_files:
        for page in frames:
            problems.append(
                Problem(
                    relative(page),
                    "declares the capability-matrix frame but no "
                    "window.CLOUD_CAPABILITY_MATRIX data file exists",
                )
            )
        return problems

    for path in data_files:
        match = MATRIX_ASSIGNMENT.search(path.read_text(encoding="utf-8"))
        try:
            payload = json.loads(match.group("payload"))
        except json.JSONDecodeError as error:
            problems.append(
                Problem(relative(path), f"window.CLOUD_CAPABILITY_MATRIX is not valid JSON: {error}")
            )
            continue
        problems.extend(_matrix_problems(relative(path), payload))

    resolved = {path.resolve(): path for path in data_files}
    for page, loaded in frames.items():
        if not (set(loaded) & set(resolved)):
            problems.append(
                Problem(relative(page), "renders the capability matrix but does not load any "
                                        "matrix data file")
            )
    served = {target for loaded in frames.values() for target in loaded}
    for path in resolved.values():
        if path not in served:
            problems.append(
                Problem(relative(path), "no published page loads this capability-matrix data file")
            )

    return problems


def check_matrix_vendor_links_live() -> list[Problem]:
    """Fetch every vendor link in the matrix data and fail on a dead one.

    Behind ``--vendor-links`` because the default run promises to be offline
    and deterministic. This is the refresh-day command: run it before opening
    a pull request that touches the data file.
    """
    problems: list[Problem] = []
    for path in _js_data_files(MATRIX_ASSIGNMENT):
        where = relative(path)
        match = MATRIX_ASSIGNMENT.search(path.read_text(encoding="utf-8"))
        try:
            payload = json.loads(match.group("payload"))
        except json.JSONDecodeError:
            continue  # reported by check_comparison_matrix
        rows = payload.get("rows", []) if isinstance(payload, dict) else []
        for row in rows:
            if not isinstance(row, dict):
                continue
            cells = row.get("cells", {})
            if not isinstance(cells, dict):
                continue
            for cloud, cell in cells.items():
                if not isinstance(cell, dict) or cell.get("state") != "service":
                    continue
                for j, svc in enumerate(cell.get("services", [])):
                    url = svc.get("doc_url") if isinstance(svc, dict) else None
                    if isinstance(url, str) and url.startswith("https://"):
                        reason = _fetch_vendor_link(url)
                        if reason:
                            problems.append(
                                Problem(
                                    f"{where}:{row.get('key')}:{cloud}.services[{j}]",
                                    f"dead vendor link ({reason}) -> {url}",
                                )
                            )
    return problems


# ---------------------------------------------------------------------------
# The course contract
#
# A course declares its identity through seven tokens in one block keyed on the
# `data-course` attribute, and through nothing else. `assets/hub.css` carries
# the mechanism and the reasoning under "the course contract"; the widget
# reference carries the author-facing version. This is the enforcement, and it
# is deliberately the cheap half: registration is static text, so a script can
# read it, while what the resulting accent looks like needs a browser and lives
# in `scripts/style_snapshot.py`.
# ---------------------------------------------------------------------------

HUB_STYLESHEET: Path = REPO_ROOT / "assets" / "hub.css"

# The seven-token author surface, in the order the specification states it.
COURSE_TOKENS: tuple[str, ...] = (
    "--course-hue",
    "--font-display",
    "--font-mono",
    "--eyebrow-family",
    "--eyebrow-tracking",
    "--eyebrow-case",
    "--eyebrow-size",
)

# The six a design also wants to write. Each is split in two so the two writers
# never contend: the design writes the `-default`, a course writes the token.
# `--course-hue` is not among them, because a design carries no colour.
COURSE_LAYERED_TOKENS: tuple[str, ...] = COURSE_TOKENS[1:]

# The three that name a face rather than a value.
COURSE_FACE_TOKENS: tuple[str, ...] = ("--font-display", "--font-mono", "--eyebrow-family")

# A course names a face from the registry or one of the four role aliases over
# it; a literal font stack in a course block is a course shipping type, which
# the contract forbids. The registry itself is read out of the sheet rather than
# listed here, so a family added later is accepted without editing this file.
ROLE_TOKENS: tuple[str, ...] = ("--font-body", "--font-display", "--font-ui", "--font-mono")
GENERIC_FAMILIES: frozenset[str] = frozenset(
    {
        "serif",
        "sans-serif",
        "monospace",
        "cursive",
        "fantasy",
        "system-ui",
        "ui-serif",
        "ui-sans-serif",
        "ui-monospace",
        "ui-rounded",
    }
)

# `--eyebrow-tracking` runs 0em to 0.34em, and `--eyebrow-size` sits in the
# `--fs-xs` band, which is 10px to 12.5px, written here in rem at the 16px root.
TRACKING_BAND: tuple[float, float] = (0.0, 0.34)
EYEBROW_SIZE_BAND_REM: tuple[float, float] = (0.625, 0.78125)

# A course sheet is grandfathered, never a precedent. These three exist, they
# carry genuinely course-specific widgets, and no fourth may be added: a new
# widget belongs in the hub sheet, where one owner keeps it.
GRANDFATHERED_COURSE_SHEETS: frozenset[str] = frozenset(
    {
        "llm-evolution-course/assets/course-extras.css",
        "llm-inference-course/assets/course-extras.css",
        "statistical-foundations-ml-course/assets/course-extras.css",
    }
)

# Two courses shipped on the same hue and therefore wear the same accent. Moving
# a published hue changes what a reader already knows a course looks like, so it
# is recorded here rather than repaired by a validator. Any new collision fails,
# so this set can only shrink.
ACCEPTED_HUE_COLLISIONS: frozenset[frozenset[str]] = frozenset(
    {frozenset({"aws-course", "llm-efficiency-course"})}
)

# Capitals read 9.53% to 19.01% slower than lowercase, so `--eyebrow-case:
# uppercase` is defensible on a two to four word label and nowhere else. These
# 22 eyebrows run past five words in capitals and predate the rule. Each is one
# eyebrow on one page, almost all of them a course landing page's tagline.
# Rewriting them is a content change on 22 pages and belongs to whoever owns
# that prose; the list fails a new one, and fails an entry that has been fixed,
# so it only ever gets shorter.
LONG_UPPERCASE_EYEBROWS: dict[str, int] = {
    "agent-engineering-course/index.html": 1,
    "ai-system-design-course/index.html": 1,
    "aws-course/index.html": 1,
    "azure-course/index.html": 1,
    "cloud-comparison-course/index.html": 1,
    "coding-harness-course/index.html": 1,
    "gcp-course/index.html": 1,
    "herdr-course/index.html": 1,
    "index.html": 1,
    "llm-efficiency-course/index.html": 1,
    "llm-efficiency-course/lessons/0008-speculative-decoding-buys-bandwidth-with-compute.html": 1,
    "llm-efficiency-course/lessons/0009-case-study-glm-on-two-dgx-sparks.html": 1,
    "llm-efficiency-course/lessons/0010-case-study-mac-studio-256gb.html": 1,
    "llm-evolution-course/index.html": 1,
    "llm-inference-course/index.html": 1,
    "oci-course/index.html": 1,
    "probability-you-build-course/lessons/0408-week-5-problems.html": 1,
    "production-systems-course/index.html": 1,
    "staff-ai-course/index.html": 1,
    "statistical-foundations-ml-course/lessons/0020-conditional-probability.html": 1,
    "statistical-foundations-ml-course/lessons/0039-practice-independence-and-conditioning.html": 1,
    "statistical-foundations-ml-course/lessons/0040-practice-counting-and-arrangements.html": 1,
}

# An eyebrow is looked at rather than read, which is what makes capitals
# defensible. Five words is the limit the specification states as "about five",
# and the house target is two to four.
EYEBROW_WORD_LIMIT: int = 5

CSS_COMMENT: re.Pattern[str] = re.compile(r"/\*.*?\*/", re.DOTALL)
COURSE_BLOCK: re.Pattern[str] = re.compile(r"([^{}]*\[data-course=[^{}]*)\{([^{}]*)\}")
COURSE_BLOCK_SELECTOR: re.Pattern[str] = re.compile(r'^:root\[data-course="[^"]+"\]$')
DECLARATION: re.Pattern[str] = re.compile(r"(--[\w-]+)\s*:\s*([^;]+)")
UNITLESS_NUMBER: re.Pattern[str] = re.compile(r"^-?(?:\d+(?:\.\d+)?|\.\d+)$")
FACE_REFERENCE: re.Pattern[str] = re.compile(r"^var\(\s*(--[\w-]+)\s*\)$")
LENGTH: re.Pattern[str] = re.compile(r"^(-?(?:\d+(?:\.\d+)?|\.\d+))(em|rem|px)?$")
EYEBROW_ELEMENT: re.Pattern[str] = re.compile(r'class="eyebrow"[^>]*>(.*?)</', re.DOTALL)
EYEBROW_SEPARATOR: re.Pattern[str] = re.compile(r"&middot;|&bull;|&mdash;|&ndash;|\u00b7|\u2022|\|")
TAG: re.Pattern[str] = re.compile(r"<[^>]+>")


def hub_stylesheet() -> str:
    """The hub sheet with its comments removed, so an example cannot be read as a rule."""
    return CSS_COMMENT.sub("", HUB_STYLESHEET.read_text(encoding="utf-8"))


def registered_faces(source: str) -> frozenset[str]:
    """Every family the sheet loads, plus the role aliases a course may name.

    A family is recognised by its stack ending in a generic keyword, which is
    what makes a stack a fallback rather than a single name. Reading it out of
    the sheet means a face added to the registry later is accepted here without
    a second edit, exactly as a newly registered hue is.
    """
    found: set[str] = set(ROLE_TOKENS)
    for selector, body in re.findall(r"([^{}]*)\{([^{}]*)\}", source):
        if " ".join(selector.split()) != ":root":
            continue
        for name, value in declarations(body):
            last = value.split(",")[-1].strip().strip("\"'").lower()
            if last in GENERIC_FAMILIES:
                found.add(name)
    return frozenset(found)


def declarations(body: str) -> list[tuple[str, str]]:
    """Every custom property declared in one rule body, in source order."""
    return [(name, value.strip()) for name, value in DECLARATION.findall(body)]


def course_blocks(source: str) -> list[tuple[str, str, str]]:
    """Every rule keyed on ``data-course``, as (selector, course folder, body)."""
    blocks: list[tuple[str, str, str]] = []
    for selector, body in COURSE_BLOCK.findall(source):
        selector = " ".join(selector.split())
        named = re.findall(r'data-course="([^"]+)"', selector)
        blocks.append((selector, named[0] if named else "", body))
    return blocks


def registrations(source: str) -> dict[str, dict[str, str]]:
    """The declared identity of every registered course, keyed on its folder."""
    found: dict[str, dict[str, str]] = {}
    for _, course, body in course_blocks(source):
        if course:
            found.setdefault(course, {}).update(dict(declarations(body)))
    return found


def _face_problems(course: str, token: str, value: str, faces: frozenset[str]) -> list[Problem]:
    where = f"assets/hub.css [data-course=\"{course}\"]"
    reference = FACE_REFERENCE.match(value)
    if reference is None:
        return [
            Problem(
                where,
                f"{token} is {value!r}; a course names a face in the registry, "
                f"as var(--serif) or var(--font-mono), never a font stack of its own",
            )
        ]
    named = reference.group(1)
    if named == token:
        return [Problem(where, f"{token} names itself, which resolves to nothing")]
    if named not in faces:
        return [
            Problem(
                where,
                f"{token} names {named}, which is not a registered face; "
                f"the registry and its roles are {', '.join(sorted(faces))}",
            )
        ]
    return []


def _value_problems(course: str, token: str, value: str, faces: frozenset[str]) -> list[Problem]:
    where = f"assets/hub.css [data-course=\"{course}\"]"
    if token in COURSE_FACE_TOKENS:
        return _face_problems(course, token, value, faces)

    if token == "--course-hue":
        if UNITLESS_NUMBER.match(value):
            return []
        return [
            Problem(
                where,
                f"--course-hue is {value!r}; it must be a unitless number. Inside a "
                f"relative colour `h` is a number and not an angle, so calc(h + 25deg) "
                f"is a type error and silently drops the whole declaration",
            )
        ]

    if token == "--eyebrow-case":
        if value in {"uppercase", "none"}:
            return []
        return [Problem(where, f"--eyebrow-case is {value!r}; it is `uppercase` or `none`")]

    if token == "--eyebrow-tracking":
        if value == "var(--tracking-eyebrow)":
            return []
        measured = LENGTH.match(value)
        low, high = TRACKING_BAND
        if measured is not None and measured.group(2) in {"em", None}:
            if low <= float(measured.group(1)) <= high:
                return []
        return [
            Problem(
                where,
                f"--eyebrow-tracking is {value!r}; it is an em value between "
                f"{low}em and {high}em, or var(--tracking-eyebrow)",
            )
        ]

    if token == "--eyebrow-size":
        if value == "var(--fs-xs)":
            return []
        measured = LENGTH.match(value)
        low, high = EYEBROW_SIZE_BAND_REM
        if measured is not None:
            size = float(measured.group(1))
            if measured.group(2) == "px":
                size = size / 16
            if measured.group(2) in {"rem", "px"} and low <= size <= high:
                return []
        return [
            Problem(
                where,
                f"--eyebrow-size is {value!r}; it sits in the --fs-xs band, "
                f"{low}rem to {high}rem (10px to 12.5px), or names var(--fs-xs)",
            )
        ]

    return []


def _registration_problems(source: str) -> list[Problem]:
    """Every course folder is registered exactly once, in the documented shape."""
    faces = registered_faces(source)
    problems: list[Problem] = []
    seen: dict[str, int] = {}

    for selector, course, body in course_blocks(source):
        if not course:
            problems.append(
                Problem("assets/hub.css", f"a rule keys on data-course but names none: {selector}")
            )
            continue
        expected = f':root[data-course="{course}"]'
        if selector != expected:
            problems.append(
                Problem(
                    "assets/hub.css",
                    f"course block is written {selector!r}; it must be written "
                    f"{expected!r}, which is (0,2,0) and therefore wins the "
                    f"resolution line whatever the source order",
                )
            )
        seen[course] = seen.get(course, 0) + 1
        for token, value in declarations(body):
            if token not in COURSE_TOKENS:
                problems.append(
                    Problem(
                        f"assets/hub.css [data-course=\"{course}\"]",
                        f"{token} is not on the author surface. A course declares only "
                        f"{', '.join(COURSE_TOKENS)}",
                    )
                )
                continue
            problems += _value_problems(course, token, value, faces)

    for course, count in sorted(seen.items()):
        if count > 1:
            problems.append(
                Problem("assets/hub.css", f"{course} is registered {count} times; one block per course")
            )

    folders = {course.name for course in teaching_courses()}
    for course in sorted(folders - set(seen)):
        problems.append(
            Problem(
                "assets/hub.css",
                f"{course} has no registration, so it wears the plain palette accent "
                f"and is told apart from no other course",
            )
        )
    for course in sorted(set(seen) - folders):
        problems.append(
            Problem("assets/hub.css", f"{course} is registered but there is no such course folder")
        )
    return problems


def _hue_problems(declared: dict[str, dict[str, str]]) -> list[Problem]:
    """Two courses on one hue wear one accent, which is the thing the hue exists to prevent."""
    by_hue: dict[str, list[str]] = {}
    for course, tokens in declared.items():
        hue = tokens.get("--course-hue", "")
        if UNITLESS_NUMBER.match(hue):
            by_hue.setdefault(str(float(hue)), []).append(course)

    problems: list[Problem] = []
    for hue, courses in sorted(by_hue.items()):
        if len(courses) > 1 and frozenset(courses) not in ACCEPTED_HUE_COLLISIONS:
            problems.append(
                Problem(
                    "assets/hub.css",
                    f"{' and '.join(sorted(courses))} both hold --course-hue {hue}, so they "
                    f"wear the same accent in every palette and both modes. Split a gap on "
                    f"the circle instead; the 25-degree grid is full",
                )
            )
    return problems


def _layer_problems(source: str) -> list[Problem]:
    """The six shared tokens keep two names, so a design and a course never contend.

    The token is resolved once, at bare ``:root``, from its ``-default``. A
    course block may override it, because that is the course layer. Nothing else
    may write it: a design block and a course block are both (0,2,0), and two
    writers on one name is a contest the cascade settles silently on source
    order.
    """
    problems: list[Problem] = []
    writers: dict[str, list[tuple[str, str]]] = {token: [] for token in COURSE_LAYERED_TOKENS}
    defaults: set[str] = set()

    for selector, body in re.findall(r"([^{}]*)\{([^{}]*)\}", source):
        selector = " ".join(selector.split())
        for token, value in declarations(body):
            if token.endswith("-default"):
                defaults.add(token)
            elif token in writers:
                writers[token].append((selector, value))

    for token in COURSE_LAYERED_TOKENS:
        default = f"{token}-default"
        if default not in defaults:
            problems.append(
                Problem("assets/hub.css", f"{token} has no {default}; a design has nothing to write")
            )
        resolved = [
            value for selector, value in writers[token] if selector == ":root"
        ]
        if resolved != [f"var({default})"]:
            problems.append(
                Problem(
                    "assets/hub.css",
                    f"{token} must be resolved exactly once, at bare :root, as "
                    f"var({default}); found {resolved!r}",
                )
            )
        for selector, _value in writers[token]:
            if selector == ":root" or COURSE_BLOCK_SELECTOR.match(selector):
                continue
            problems.append(
                Problem(
                    "assets/hub.css",
                    f"{selector} writes {token}. Only the resolution line at bare :root "
                    f"and a course identity block may; anything else writes "
                    f"{token}-default instead",
                )
            )
    return problems


def _course_sheet_problems() -> list[Problem]:
    """A course ships no CSS of its own; the three that do are grandfathered."""
    problems: list[Problem] = []
    for course in teaching_courses():
        for sheet in sorted(course.rglob("*.css")):
            name = relative(sheet)
            if name not in GRANDFATHERED_COURSE_SHEETS:
                problems.append(
                    Problem(
                        name,
                        "a course ships no stylesheet of its own. Three exist and they are "
                        "grandfathered, not a precedent: a widget a second course could want "
                        "belongs in assets/hub.css, where it has one owner",
                    )
                )
    for name in sorted(GRANDFATHERED_COURSE_SHEETS):
        if not (REPO_ROOT / name).is_file():
            problems.append(
                Problem(
                    "scripts/validate_site.py",
                    f"{name} is recorded as grandfathered but is gone; drop it from "
                    f"GRANDFATHERED_COURSE_SHEETS",
                )
            )
    return problems


def eyebrow_strings(page: Path) -> list[str]:
    """The text of every eyebrow on a page, tags removed and whitespace folded."""
    source = page.read_text(encoding="utf-8", errors="replace")
    return [
        " ".join(TAG.sub(" ", found).split()) for found in EYEBROW_ELEMENT.findall(source)
    ]


def eyebrow_is_long(text: str) -> bool:
    """An eyebrow is measured by its longest segment, not by its whole line.

    A segmented label - ``Week 6 · Lesson 3 of 9 · ranking against detecting`` -
    is four short labels a reader looks at one at a time, so counting the words
    across the separators would condemn the shape the hub actually uses.
    """
    segments = [part for part in EYEBROW_SEPARATOR.split(text) if part.strip()]
    return max((len(part.split()) for part in segments), default=0) > EYEBROW_WORD_LIMIT


def _eyebrow_problems(declared: dict[str, dict[str, str]]) -> list[Problem]:
    """Capitals are defensible on a short label and nowhere else.

    Only a course's own ``--eyebrow-case: none`` exempts its pages. A design
    that turned capitals off would exempt them too, for as long as the reader
    kept that design, and a page has to be right under the house default rather
    than under one setting of a control the reader can move.
    """
    lowercase = {
        course
        for course, tokens in declared.items()
        if tokens.get("--eyebrow-case") == "none"
    }

    counted: dict[str, int] = {}
    for page in html_pages():
        name = relative(page)
        course = name.split("/", 1)[0] if "/" in name else ""
        if course in lowercase:
            continue
        found = sum(1 for text in eyebrow_strings(page) if eyebrow_is_long(text))
        if found:
            counted[name] = found

    problems: list[Problem] = []
    for name, found in sorted(counted.items()):
        recorded = LONG_UPPERCASE_EYEBROWS.get(name, 0)
        if found > recorded:
            problems.append(
                Problem(
                    name,
                    f"{found - recorded} eyebrow(s) run past {EYEBROW_WORD_LIMIT} words in a "
                    f"single segment while --eyebrow-case is uppercase. Capitals read 9.53% "
                    f"to 19.01% slower; the house target is two to four words",
                )
            )
    for name, recorded in sorted(LONG_UPPERCASE_EYEBROWS.items()):
        found = counted.get(name, 0)
        if found < recorded:
            problems.append(
                Problem(
                    "scripts/validate_site.py",
                    f"{name} now has {found} over-long uppercase eyebrow(s), not {recorded}. "
                    f"Lower or delete its entry in LONG_UPPERCASE_EYEBROWS so the list "
                    f"only ever gets shorter",
                )
            )
    return problems


def check_course_contract() -> list[Problem]:
    source = hub_stylesheet()
    declared = registrations(source)
    return (
        _registration_problems(source)
        + _hue_problems(declared)
        + _layer_problems(source)
        + _course_sheet_problems()
        + _eyebrow_problems(declared)
    )


def check_the_font_contract() -> list[Problem]:
    """The self-hosted faces: every declaration reaches a file, every file is
    reached, every face states how it behaves while it loads, and the payload
    stays under a ceiling somebody chose.

    Four failures, all of them silent on a published page.

    1. **A declaration naming a file that is not there.** The family stack falls
       through to a system face of the same class, which is exactly what the
       stacks are for, so the page still reads and nothing anywhere says the
       hub's own typography stopped being served.

    2. **A woff2 that no declaration names.** Dead weight in the repository and
       in the bucket, and the reader who does not fetch it is the only one who
       is unaffected.

    3. **A face with no ``font-display``.** The initial value is ``auto``, which
       Chrome treats as ``block``: the text is invisible until the face arrives,
       measured at 1.4s to 1.9s after first paint on a throttled connection.
       ``optional`` is refused for a different reason and the message carries it.

    4. **A payload nobody costed.** Two ceilings, because a reader does not
       fetch the repository: the total is what the bucket holds, and the latin
       cuts are what one English page can actually ask for.
    """
    problems: list[Problem] = []
    font_dir = REPO_ROOT / "assets" / "fonts"
    declared: set[Path] = set()
    latin: set[Path] = set()

    sheets = sorted(
        path
        for path in REPO_ROOT.rglob("*.css")
        if not any(part.startswith(".") for part in path.relative_to(REPO_ROOT).parts)
    )
    for sheet in sheets:
        where = relative(sheet)
        for face in FONT_FACE.finditer(sheet.read_text(encoding="utf-8")):
            body = face.group("body")
            hrefs = FONT_SRC_URL.findall(body)
            if not hrefs:
                problems.append(Problem(where, "an @font-face block has no src url()"))
                continue
            for href in hrefs:
                target = (sheet.parent / href).resolve()
                if not target.is_file():
                    problems.append(
                        Problem(where, f"@font-face names a file that is not on disk -> {href}")
                    )
                    continue
                declared.add(target)
                ranges = FONT_UNICODE_RANGE.search(body)
                if ranges is None or FONT_LATIN_MARKER in ranges.group("value").upper():
                    latin.add(target)

            display = FONT_DISPLAY.search(body)
            name = hrefs[0]
            if display is None:
                problems.append(
                    Problem(where, f"@font-face for {name} declares no font-display; "
                                   "the initial value hides the text until the face arrives")
                )
            elif display.group("value") == "optional":
                problems.append(
                    Problem(where, f"@font-face for {name} uses font-display: optional, which a face the "
                                   "reader can switch to may not use: a face that misses the first-paint "
                                   "deadline is dropped for the life of that page load and "
                                   "document.fonts.load() does not bring it back")
                )

    if font_dir.is_dir():
        for shipped in sorted(font_dir.glob("*.woff2")):
            if shipped.resolve() not in declared:
                problems.append(
                    Problem(relative(shipped), "no @font-face names this file; it is published and never fetched")
                )

    total = sum(path.stat().st_size for path in declared)
    latin_total = sum(path.stat().st_size for path in latin)
    if total > FONT_BYTES_CEILING:
        problems.append(
            Problem("assets/fonts", f"the declared faces are {total:,} bytes, over the "
                                    f"{FONT_BYTES_CEILING:,} byte ceiling; raise it deliberately "
                                    "or subset, and record the reason in assets/fonts/README.md")
        )
    if latin_total > FONT_LATIN_BYTES_CEILING:
        problems.append(
            Problem("assets/fonts", f"the latin cuts are {latin_total:,} bytes, over the "
                                    f"{FONT_LATIN_BYTES_CEILING:,} byte ceiling; that is what one "
                                    "English page fetches, so this is the reader's bill")
        )
    return problems


def main() -> int:
    problems = (
        check_courses_are_registered()
        + check_lessons_are_registered()
        + check_outlines_match_disk()
        + check_routes_cover_the_pool()
        + check_pagers_match_the_owning_route()
        + check_lessons_carry_zone_metadata()
        + check_course_map_sections_are_balanced()
        + check_titles_agree()
        + check_local_links_resolve()
        + check_no_local_markdown_links()
        + check_comparison_matrix()
        + check_pages_link_the_design_system()
        + check_spine_keeps_a_link_on_a_phone()
        + check_design_registry_and_blocks()
        + check_design_token_completeness()
        + check_three_layer_rule()
        + check_course_contract()
        + check_contrast_floor()
        + check_page_margin_boxes()
        + check_width_queries_name_a_medium()
        + check_the_font_contract()
        + check_named_tokens_exist()
    )
    if "--vendor-links" in sys.argv[1:]:
        # Opt-in live reachability for the matrix's vendor links. The default
        # run stays offline; this is the refresh-day command.
        problems += check_matrix_vendor_links_live()

    if problems:
        print(f"Course Hub validation failed with {len(problems)} problem(s):\n")
        for problem in problems:
            print(f"  - {problem.render()}")
        return 1

    waived = waived_title_defects()
    if waived:
        total = sum(waived.values())
        listing = ", ".join(f"{name} {count}" for name, count in sorted(waived.items()))
        print(
            f"Note: {total} title defect(s) waived ({listing}). SWEEP_PENDING is debt "
            "and its entry leaves scripts/check_titles.py when the sweep lands; FROZEN "
            "is a course nobody may edit, so its entry is permanent."
        )

    breaches = contrast.recorded_breaches(contrast.registrations())
    if breaches:
        print(
            f"Note: {len(breaches)} registered ground outside its lightness band is recorded as "
            f"debt ({', '.join(breaches)}). It is a palette to correct, not a band to widen; "
            "the record is in scripts/contrast.py and it may only ever get shorter."
        )

    print(f"Course Hub validation passed: {len(html_pages())} pages checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
