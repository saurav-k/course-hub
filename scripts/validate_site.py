#!/usr/bin/env python3
"""Static checks for the Course Hub before anything is published.

Eight checks, all deterministic and offline:

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
   service, a declared absence with a reason, or explicitly unfilled, every page
   rendering the widget binds to the documented ``figure.cmatrix`` frame, and every
   vendor link is well formed. Pass ``--vendor-links`` to also fetch each vendor
   link and fail on a dead one - the default run stays offline and deterministic.

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

CELL_STATES: frozenset[str] = frozenset({"unfilled", "absent", "service"})


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
    """Course folders are the top-level directories that ship a page."""
    return sorted(
        entry
        for entry in REPO_ROOT.iterdir()
        if entry.is_dir()
        and not entry.name.startswith(".")
        and entry.name not in {"assets", "scripts"}
    )


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
                    Problem(cell_at, f"cell state {state!r} is not one of unfilled / absent / service")
                )
                continue
            if state == "absent" and not (
                isinstance(cell.get("reason"), str) and cell["reason"].strip()
            ):
                problems.append(
                    Problem(cell_at, f"a declared absence in row {key} ({c}) owes a reason")
                )
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

    print(f"Course Hub validation passed: {len(html_pages())} pages checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
