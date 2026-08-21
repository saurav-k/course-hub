#!/usr/bin/env python3
"""Static checks for the Course Hub before anything is published.

Eight checks, all deterministic and offline:

1. Every course folder has an ``index.html`` and the hub ``index.html`` links it.
2. Every ``lessons/*.html`` file is linked from its own course ``index.html``.
3. Every course ``outline.js`` names exactly the lessons that are on disk.
4. Every relative ``href``/``src`` in every page resolves to a file on disk.
5. No published page links a local ``.md`` file, which the deploy excludes.

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


def main() -> int:
    problems = (
        check_courses_are_registered()
        + check_lessons_are_registered()
        + check_outlines_match_disk()
        + check_routes_cover_the_pool()
        + check_pagers_match_the_owning_route()
        + check_lessons_carry_zone_metadata()
        + check_local_links_resolve()
        + check_no_local_markdown_links()
    )

    if problems:
        print(f"Course Hub validation failed with {len(problems)} problem(s):\n")
        for problem in problems:
            print(f"  - {problem.render()}")
        return 1

    print(f"Course Hub validation passed: {len(html_pages())} pages checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
