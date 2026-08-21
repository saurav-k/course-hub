#!/usr/bin/env python3
"""Static checks for the Course Hub before anything is published.

Four checks, all deterministic and offline:

1. Every course folder has an ``index.html`` and the hub ``index.html`` links it.
2. Every ``lessons/*.html`` file is linked from its own course ``index.html``.
3. Every course ``outline.js`` names exactly the lessons that are on disk.
4. Every relative ``href``/``src`` in every page resolves to a file on disk.

Exit code 0 means the site is publishable. Exit code 1 lists every problem.
"""

from __future__ import annotations

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
        + check_local_links_resolve()
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
