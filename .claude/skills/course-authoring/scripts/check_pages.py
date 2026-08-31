#!/usr/bin/env python3
"""Check authored pages against the course-hub house standard.

``scripts/validate_site.py`` checks that the site hangs together: registration,
links and outlines. That is the gate on the pull request. This checks that a
page is one of these courses: the design-system links it must carry, the four
ways a Mermaid diagram breaks silently, the widget shapes in
``references/widgets.md`` and the counts in ``references/pedagogy.md``.

The caption pair splits across the two: whether a ``.fig-cap`` and a
``.fig-claim`` are in the right place is structural and belongs to
``validate_site.py``; how long they are and whether either is a question is
editorial and belongs here.

Deterministic and offline, no dependencies. Two severities:

* FAIL - a defect with no defensible reason to exist. Fix it.
* WARN - a bar a page may miss for a reason you can state in the pull request.

    python3 .claude/skills/course-authoring/scripts/check_pages.py            # whole hub
    python3 .claude/skills/course-authoring/scripts/check_pages.py <course>   # one course
    python3 .claude/skills/course-authoring/scripts/check_pages.py <file.html>
"""

from __future__ import annotations

import html
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

# .claude/skills/course-authoring/scripts/check_pages.py -> the repository root.
REPO_ROOT: Path = Path(__file__).resolve().parents[4]

MAX_OPTION_CHAR_SPREAD: int = 12
QUIZ_OPTIONS: int = 4
MIN_DIAGRAMS_PER_PAGE: int = 3
MIN_DIAGRAM_KINDS_PER_PAGE: int = 2
MIN_DIAGRAM_KINDS_PER_COURSE: int = 4
MIN_QUIZZES_PER_PAGE: int = 2
MAX_ANSWER_INDEX_SHARE: float = 0.40

# The orientation figure: the big picture, before the detail. It sits between
# the one-minute version and the first body section, so at most one <h2> - the
# one-minute version's own - may open before it. The word cap is the backstop
# for a page that puts its whole essay under a single heading: the longest
# one-minute version in the hub is 206 words, so 250 leaves a framing sentence
# and nothing more. Three content lines is what "where this sits in the whole"
# costs at minimum: what came before, this, what it enables.
MAX_SECTIONS_BEFORE_ORIENTATION: int = 1
MAX_WORDS_BEFORE_ORIENTATION: int = 250
MIN_ORIENTATION_LINES: int = 3

# Fewer words, more of the meaning carried by the picture. Both numbers are the
# measured ceiling of the pages that read best rather than a wish: every page in
# `llm-papers-course` and `llm-inference-course` sits under both.
MAX_PROSE_WORDS_PER_PAGE: int = 1800
MAX_PROSE_WORDS_PER_FIGURE: int = 400

# The figure's text budget above the drawing: a label that names the subject and
# a claim that says what the drawing proves. Both ceilings are measured on the
# 94 figures the anatomy comes from rather than chosen: a median of 3 words in
# the label and 11 in the claim, and no question mark in either.
#
# Six words is where the label stops being one line. The rule mark before it is
# a ::before on a flex row, so a wrapped label leaves its second line with no
# anchor and the figure loses its left edge - correct on a laptop, broken at
# narrow widths, and silent in both.
MAX_FIG_CAP_WORDS: int = 6
MAX_FIG_CLAIM_WORDS: int = 15

# Two floors are newer than the seven courses that predate this checker, so a
# course opts into them by name rather than inheriting them silently and turning
# every legacy page red. Joining this set is the last step of a retrofit under
# `retrofit.md`, not the first.
EXTENDED_BAR_COURSES: frozenset[str] = frozenset({"math-for-ml-course", "staff-ai-course", "llm-efficiency-course"})
MIN_PRACTICE_PER_PAGE: int = 1
MIN_CHARTS_PER_PAGE: int = 1

QUIZ_BLOCK = re.compile(r'<div class="q" data-answer="(\d+)">(.*?)</div>\s*</div>', re.S)
OPTION = re.compile(r'<button class="q-opt">(.*?)</button>', re.S)
FIGURE = re.compile(r"<figure[^>]*>(.*?)</figure>", re.S)
MERMAID_BLOCK = re.compile(r'<div class="mermaid"[^>]*>(.*?)</div>', re.S)
MERMAID_PRE = re.compile(r'<pre[^>]*class="[^"]*\bmermaid\b', re.I)
MATH_BLOCK = re.compile(r'<div class="math">(.*?)</div>\s*</div>', re.S)
READING_PILL = re.compile(r'<span class="pill">\s*(\d+)\s*min\s*</span>')
RUNG_PILL = re.compile(r'<span class="pill (easy|med|hard)">([^<]*)</span>')
PAGER = re.compile(r'<(?:div|nav) class="pager"')
SVG_CLASS = re.compile(r'class="([^"]*)"')

# A hand-authored figure's drawing, matched on the class list rather than on
# the exact string `class="chart"`: all 782 in the hub are spelled that way
# today, and a second class on one of them would otherwise make it count as no
# kind at all rather than as the kind it is.
CHART_SVG = re.compile(r'<svg[^>]*\bclass="[^"]*\bchart\b')
CSS_CLASS = re.compile(r"\.([a-zA-Z_-][\w-]*)")

# A Mermaid label: the text inside [] () {} (( )). Only the bracketed forms are
# parsed here, which is where the damage is.
MERMAID_LABEL = re.compile(r"[\[\(\{]+([^\[\]\(\)\{\}]+)[\]\)\}]+")

# Two kinds of entity end in a semicolon without being a statement separator,
# and both are correct in a label. `&lt;br/&gt;` is the house line break, written
# as an HTML entity so it survives the repaint. `#quot;` is Mermaid's own entity
# syntax, which is how a quotation mark gets inside a quoted label. Testing a
# raw label for ";" flags almost every diagram in the hub.
ENTITY = re.compile(r"[&#](?:#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]*);|#\d+;")

# The prefixed class names the stylesheet closes. `d-` is the diagram
# vocabulary and joins the five charting prefixes here for the same reason they
# are here: a misspelled `d-bxo` is a box that draws nothing, in every mode and
# every palette, and nothing else in the repository would say so.
CHART_SEMANTIC = re.compile(r"^(?:m|s|f|t|sw|d)-[a-z0-9-]+$")

# Every paint value inside a figure is either absent, so a class supplies it,
# or a var() naming a token the palette layer declares. A literal is a colour
# nobody checked: it is one mode's answer written down, and the mode it is
# wrong in is the one nobody looked at.
#
# Three forms carry a paint value and all three are read here. The rule this
# replaces read one spelling of one of them - `fill="#hex"` - so a colour
# written as a `style=` declaration, as `rgb()`, or by name walked straight
# past it, and so did every Mermaid `classDef`, which writes `fill:#hex`
# rather than `fill="#hex"`. All four were rendered on a real page before
# being called holes.
PAINT_PROPS = r"fill|stroke|stop-color|flood-color|lighting-color"
PAINT_ATTR = re.compile(rf'\b({PAINT_PROPS})\s*=\s*"([^"]*)"')
PAINT_DECL = re.compile(rf"\b({PAINT_PROPS})\s*:\s*([^;,\"']+)")
STYLE_ATTR = re.compile(r'\bstyle\s*=\s*"([^"]*)"')
CLASSDEF = re.compile(r"^\s*classDef\s+\S+\s+(.*)$", re.M)

# What a paint value is allowed to be. `context-stroke` and `context-fill` are
# not colours but references to one, which is how the shared arrowhead takes
# the colour of the line it sits on; `url(#...)` is the same kind of reference
# to a gradient or a marker.
PAINT_OK = re.compile(
    r"^\s*(?:none|transparent|currentColor|inherit"
    r"|context-stroke|context-fill|url\(#[\w-]+\)"
    r"|var\(\s*--[\w-]+\s*\))\s*$"
)

# The two lines of the caption pair. Whether they are in the right place is
# scripts/validate_site.py check 19, which parses the element stack; what is
# checked here is what an author wrote in them.
FIG_CAP = re.compile(r'<div class="fig-cap"[^>]*>(.*?)</div>', re.S)
FIG_CLAIM = re.compile(r'<div class="fig-claim"[^>]*>(.*?)</div>', re.S)

# Prose is what is left of the reading column once everything that is not prose
# is taken out of it: the figures, the code, the quizzes and the page chrome.
# It is the quantity the word bars are stated in, because it is the quantity a
# reader has to hold.
MAIN = re.compile(r"<main[^>]*>(.*?)</main>", re.S)
FIGURE_BLOCK = re.compile(r"<figure[^>]*>.*?</figure>", re.S)
PRE_BLOCK = re.compile(r"<pre[^>]*>.*?</pre>", re.S)
SCRIPTISH = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S)
def block_of(css_class: str) -> re.Pattern[str]:
    """A reading-column block that runs to the next structural boundary.

    A quiz and a practice problem both nest <div>s, so a non-greedy close would
    stop at the first inner one. Both are therefore anchored on the opening tag
    and terminated by a lookahead at whatever comes next in the page contract.
    """
    return re.compile(
        rf'<div class="{css_class}"[^>]*>.*?'
        r'(?=<h2|<div class="teacher-note"|<(?:div|nav) class="pager"|\Z)',
        re.S,
    )


QUIZ_WRAPPER = block_of("quiz")
NAV_BLOCK = re.compile(r"<nav[^>]*>.*?</nav>", re.S)
FOOTER_BLOCK = re.compile(r"<footer[^>]*>.*?</footer>", re.S)
PAGER_BLOCK = re.compile(r'<(div|nav) class="pager".*?</\1>', re.S)
# A practice problem is work the reader does, not prose they read, so it is
# excluded exactly as the quiz wrapper is. Without this every page carrying the
# problems the course requires would breach the word ceiling and the
# words-per-figure ceiling on the day it shipped: one 600-word practice section
# added to a page that cleared both took it to 2,139 words and 535 words per
PRACTICE_WRAPPER = block_of("practice")
PRACTICE_OPEN = re.compile(r'<div class="practice"[^>]*>')
PRACTICE_SOLUTION = re.compile(r'<details class="solution"[^>]*>')
PRACTICE_CHECK = re.compile(r'class="p-check"')
NOT_PROSE = (
    SCRIPTISH, NAV_BLOCK, FOOTER_BLOCK, PAGER_BLOCK,
    QUIZ_WRAPPER, PRACTICE_WRAPPER, FIGURE_BLOCK, PRE_BLOCK,
)
SECTION_HEADING = re.compile(r"<h2\b", re.I)
SVG_TEXT = re.compile(r"<text\b", re.I)
# Matched on the attribute rather than on one spelling of the tag, so that
# <svg viewBox="..." class="chart"> counts as well as <svg class="chart">.
CHART_SVG = re.compile(r'<svg\b[^>]*\bclass="[^"]*\bchart\b[^"]*"', re.I)


@dataclass(frozen=True)
class Finding:
    """One failed or borderline check, reported relative to the repository root."""

    where: str
    severity: str
    detail: str

    def render(self) -> str:
        return f"  {self.severity}  {self.where}: {self.detail}"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def plain(fragment: str) -> str:
    """Strip tags and unescape entities so a length comparison means something."""
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def is_lesson(page: Path) -> bool:
    return page.parent.name == "lessons"


def is_hub_landing(page: Path) -> bool:
    return page.parent == REPO_ROOT and page.name == "index.html"


def is_course(folder: Path) -> bool:
    """A top-level folder that teaches, as opposed to one that does not.

    Not every folder in the hub is a course. ``design-system/`` is a single
    reference page about the design system itself: it has no lessons, so it has
    no rail to build, no mission to declare and no diagram-kind spread to keep.
    Holding it to the course bar would report five failures that name nothing a
    reader or an author could act on.

    The test is the ``lessons/`` directory, because that is what a course *is*
    here and every one of them has one. It is deliberately structural rather
    than a list of folder names: a list would have to be edited by whoever adds
    the next course, and the failure mode of forgetting is a course that quietly
    stops being checked.
    """
    return folder.is_dir() and (folder / "lessons").is_dir()


def is_course_map(page: Path) -> bool:
    return page.name == "index.html" and page.parent.parent == REPO_ROOT


def declared_css_classes() -> frozenset[str]:
    """Every class name any stylesheet in the repository defines.

    The chart palette is a closed set that lives in ``assets/hub.css``, and two
    courses layer their own sheet after it. Reading the sheets rather than
    hard-coding the names is what stops this checker drifting from the design
    system the day someone adds a colour.
    """
    names: set[str] = set()
    for sheet in REPO_ROOT.rglob("*.css"):
        if any(part.startswith(".") for part in sheet.relative_to(REPO_ROOT).parts):
            continue
        names |= set(CSS_CLASS.findall(sheet.read_text(encoding="utf-8", errors="replace")))
    return frozenset(names)


def check_no_em_dash(page: Path, src: str) -> list[Finding]:
    if "—" not in src and "&mdash;" not in src:
        return []
    return [Finding(rel(page), "FAIL", "contains an em dash; the house dash is a plain -")]


def check_design_system(page: Path, src: str) -> list[Finding]:
    """One design system, linked one way, with the runtime in the head.

    ``hub.js`` writes data-mode, data-palette and data-course onto <html> in its
    head phase, before the first paint. A page that loads it late, or not at
    all, flashes the wrong colours or never gets the rail.
    """
    found: list[Finding] = []
    if not re.search(r'href="[^"]*assets/hub\.css"', src):
        found.append(Finding(rel(page), "FAIL", "does not link assets/hub.css"))
    if re.search(r'href="[^"]*assets/course\.css"', src) or re.search(r'src="[^"]*assets/course\.js"', src):
        found.append(Finding(rel(page), "FAIL", "links the retired course.css/course.js pair"))
    if not re.search(r'src="[^"]*assets/hub\.js"', src):
        found.append(Finding(rel(page), "FAIL", "does not load assets/hub.js"))
    elif "</head>" in src and re.search(r'src="[^"]*assets/hub\.js"', src.split("</head>", 1)[1] or ""):
        found.append(Finding(rel(page), "FAIL", "loads hub.js after </head>; it must run before the first paint"))
    # The rail is a course's table of contents, so only a course's pages owe one.
    # The hub landing page and the design-system reference have no lessons to
    # list and `hub.js` builds no rail for them.
    course = course_of(page)
    if course is not None and not re.search(r'src="[^"]*outline\.js"', src):
        found.append(Finding(rel(page), "FAIL", "does not load its course outline.js, so it has no sidebar rail"))
    if "theme-btn" in src:
        found.append(Finding(rel(page), "WARN", "carries a legacy .theme-btn; hub.js deletes it at mount"))

    has_mermaid = 'class="mermaid"' in src
    has_cdn = "mermaid.min.js" in src
    if has_mermaid and not has_cdn:
        found.append(Finding(rel(page), "FAIL", "has .mermaid blocks but never loads Mermaid"))
    if has_cdn and not has_mermaid:
        found.append(Finding(rel(page), "WARN", "loads Mermaid but has no diagram to draw"))
    if has_cdn and has_mermaid and src.index("mermaid.min.js") > src.index("assets/hub.js"):
        found.append(Finding(rel(page), "FAIL", "loads Mermaid after hub.js, which claims the render from it"))

    inline = len(re.findall(r'\sstyle="', src))
    if inline:
        found.append(Finding(rel(page), "WARN", f"{inline} inline style attribute(s); give it a class in assets/hub.css"))
    return found


def check_mermaid(page: Path, src: str) -> list[Finding]:
    """The ways a diagram breaks without reaching the console.

    ``hub.js`` stashes a diagram's source as ``node.textContent`` so it can
    repaint on a mode or palette change. The first two checks are ways that
    stash stops matching what the author wrote. The semicolon checks are graded
    by where the semicolon sits, which was measured against Mermaid 11 rather
    than assumed: in a ``sequenceDiagram`` the free text after a colon is
    genuinely parsed as a statement and a semicolon there is a red error box,
    while a flowchart label, quoted or not, survives one.
    """
    found: list[Finding] = []

    if MERMAID_PRE.search(src):
        found.append(
            Finding(rel(page), "FAIL",
                    '<pre class="mermaid">: hub.js appends a copy button to every <pre>, so "copy" '
                    "becomes the last line of graph source. Use <div class=\"mermaid\">")
        )

    for index, graph in enumerate(MERMAID_BLOCK.findall(src)):
        if re.search(r"<br\s*/?>", graph, re.I):
            found.append(
                Finding(rel(page), "FAIL",
                        f"diagram {index} contains a literal <br/>, which textContent drops on repaint; "
                        "write it as &lt;br/&gt;")
            )

        text = plain(graph)
        if text.lstrip().startswith("sequenceDiagram"):
            for line in text.splitlines():
                head, sep, tail = line.partition(":")
                if sep and ";" in ENTITY.sub("", tail):
                    found.append(
                        Finding(rel(page), "FAIL",
                                f'diagram {index} has a semicolon in sequence text "{tail.strip()}", '
                                "which Mermaid parses as a statement separator; use a dash")
                    )
                    break

        for label in MERMAID_LABEL.findall(graph):
            if ";" in ENTITY.sub("", label):
                found.append(
                    Finding(rel(page), "WARN",
                            f'diagram {index} label "{label.strip()}" contains a semicolon; '
                            "Mermaid 11 tolerates one here but the house form is a dash")
                )
                break

        for label in re.findall(r"\w+\[([^\]\"]*)\]", graph):
            if any(char in label for char in "(),"):
                found.append(
                    Finding(rel(page), "FAIL", f'diagram {index} label "{label}" is unquoted and will not parse')
                )
                break
    return found


def literal_colours(body: str) -> list[str]:
    """Every paint value in a figure that is neither absent nor a token."""
    bad: list[str] = []
    for prop, value in PAINT_ATTR.findall(body):
        if not PAINT_OK.match(value):
            bad.append(f'{prop}="{value}"')
    for chunk in STYLE_ATTR.findall(body) + CLASSDEF.findall(body):
        for prop, value in PAINT_DECL.findall(chunk):
            if not PAINT_OK.match(value):
                bad.append(f"{prop}:{value.strip()}")
    return bad


def mermaid_kinds(src: str) -> set[str]:
    """The diagram type each block declares, ignoring an %%{init}%% preamble."""
    kinds: set[str] = set()
    for graph in MERMAID_BLOCK.findall(src):
        for line in plain(graph).splitlines():
            line = line.strip()
            if not line or line.startswith("%%"):
                continue
            word = re.match(r"([A-Za-z][\w-]*)", line)
            if word:
                kinds.add(word.group(1).replace("graph", "flowchart"))
            break
    return kinds


def svg_kind(figure: str) -> str:
    """Which instrument one hand-authored figure is drawn with.

    Read from the figure's own classes, the way the section rail is read from
    the page's own headings, because the alternative is a `data-kind` attribute
    on 763 existing figures and a second model of a drawing that can disagree
    with the drawing.

    Three instruments, and the order below is a precedence rather than a list.
    A structure drawing that also carries an axis - the log addressed by
    offset is the type case - is a diagram: the boxes carry the claim and the
    axis is how they are addressed. Asking about `d-` first is what settles it.
    """
    classes = {name for attribute in SVG_CLASS.findall(figure) for name in attribute.split()}
    if any(name.startswith("d-") for name in classes):
        return "svg-diagram"      # the claim is a structure: boxes, connectors, states
    if classes & {"axis", "grid", "tick"}:
        return "svg-plot"         # the claim is a quantity against a scale
    return "svg-chart"            # marks with no frame: a comparison, a strip, a swatch


def svg_kinds(src: str) -> set[str]:
    """Every hand-authored instrument a page draws with.

    `mermaid_kinds` counts each Mermaid type separately and this used to
    collapse every hand-authored figure to one name, `svg-chart`, however it
    was drawn. That asymmetry is what the kind floor was actually measuring: a
    page with three different hand-drawn figures scored one kind and warned,
    while two Mermaid types cleared the floor for free. Measured across the
    hub, 98.0% of lesson pages carry a flowchart and 90.1% open with one.

    A hand-drawn figure now counts the way a Mermaid one always has.
    """
    return {svg_kind(figure) for figure in FIGURE.findall(src) if CHART_SVG.search(figure)}


# The hand-authored instruments, which is what the course-level floor means by
# "something is drawn by hand here" now that there is more than one of them.
HAND_KINDS: frozenset[str] = frozenset({"svg-chart", "svg-plot", "svg-diagram"})


def caption_pair_findings(page: Path, index: int, body: str) -> list[Finding]:
    """What the author wrote in the two lines above the drawing.

    The label names the subject and never argues. The claim argues and never
    describes the picture. Neither is ever a question, and an author who is
    choosing what kind of sentence to write has already put the wrong thing in
    one of them - which is why the question mark is a FAIL in the label rather
    than a matter of taste.

    The claim's ceiling is a WARN: fifteen words is the measured median plus
    room, and a claim at seventeen is a sentence to tighten rather than a defect
    to reject.
    """
    found: list[Finding] = []
    for label in FIG_CAP.findall(body):
        words = plain(label).split()
        if len(words) > MAX_FIG_CAP_WORDS:
            found.append(Finding(rel(page), "FAIL",
                                 f"figure {index} .fig-cap is {len(words)} words, over {MAX_FIG_CAP_WORDS}; "
                                 "it wraps and the rule mark stays on the first line"))
        if "?" in plain(label):
            found.append(Finding(rel(page), "FAIL",
                                 f"figure {index} .fig-cap is a question; the label names the "
                                 "subject and the claim is what argues"))
    for claim in FIG_CLAIM.findall(body):
        words = plain(claim).split()
        if len(words) > MAX_FIG_CLAIM_WORDS:
            found.append(Finding(rel(page), "WARN",
                                 f"figure {index} .fig-claim is {len(words)} words, over "
                                 f"{MAX_FIG_CLAIM_WORDS}; the claim is one sentence, and the "
                                 "reading belongs in the figcaption"))
        if "?" in plain(claim):
            found.append(Finding(rel(page), "FAIL",
                                 f"figure {index} .fig-claim is a question; it states what the "
                                 "drawing proves"))
    return found


def check_figures(page: Path, src: str, css_classes: frozenset[str]) -> list[Finding]:
    found: list[Finding] = []
    figures = FIGURE.findall(src)
    for index, body in enumerate(figures):
        if "<figcaption" not in body:
            found.append(Finding(rel(page), "FAIL", f"figure {index} has no figcaption"))
        elif not re.search(r"<figcaption[^>]*>.*?<b>", body, re.S):
            found.append(Finding(rel(page), "FAIL", f"figure {index} has no bolded takeaway in its caption"))
        found.extend(caption_pair_findings(page, index, body))
        if "<svg" not in body:
            continue
        literals = literal_colours(body)
        if literals:
            found.append(Finding(
                rel(page), "FAIL",
                f"figure {index} states a colour of its own ({', '.join(literals[:3])}); "
                "paint comes from a chart class or a var(--token), never a value"))
        if 'class="chart"' in body and "aria-label" not in body:
            found.append(Finding(rel(page), "FAIL", f"figure {index} is an svg.chart with no aria-label"))
        if 'class="chart"' in body and "viewBox" not in body:
            found.append(Finding(rel(page), "FAIL", f"figure {index} is an svg.chart with no viewBox"))
        for attribute in SVG_CLASS.findall(body):
            for name in attribute.split():
                if CHART_SEMANTIC.match(name) and name not in css_classes:
                    found.append(
                        Finding(rel(page), "FAIL",
                                f'figure {index} uses .{name}, which no stylesheet defines; '
                                "the chart palette is a closed set in assets/hub.css")
                    )

    if not is_lesson(page):
        return found
    kinds = mermaid_kinds(src) | svg_kinds(src)
    if len(figures) < MIN_DIAGRAMS_PER_PAGE:
        found.append(Finding(rel(page), "WARN", f"{len(figures)} diagrams, the floor is {MIN_DIAGRAMS_PER_PAGE}"))
    if figures and len(kinds) < MIN_DIAGRAM_KINDS_PER_PAGE:
        found.append(Finding(
            rel(page), "WARN",
            f"{len(kinds)} diagram kind{'' if len(kinds) == 1 else 's'} "
            f"({', '.join(sorted(kinds)) or 'none'}); the floor is {MIN_DIAGRAM_KINDS_PER_PAGE}"))
    return found


def reading_column(src: str) -> str:
    """The page body, which is what a reader reads. Chrome lives outside it."""
    body = MAIN.search(src)
    return body.group(1) if body else src


def prose(fragment: str) -> int:
    """Words of prose in a fragment of the reading column."""
    for pattern in NOT_PROSE:
        fragment = pattern.sub(" ", fragment)
    return len(plain(fragment).split())


def figure_lines(body: str) -> int:
    """How much a figure actually draws.

    A Mermaid diagram is counted in content lines of graph source, which works
    across every kind the hub uses without parsing any of them, and a
    hand-authored chart in its ``<text>`` labels. A two-box picture cannot place
    an idea inside a larger whole, and the count is what says so.
    """
    lines = 0
    for graph in MERMAID_BLOCK.findall(body):
        source = [line.strip() for line in plain(graph).splitlines()]
        content = [
            line
            for line in source[1:]
            if line and not line.startswith("%%") and line not in {"end"}
        ]
        lines += len(content)
    return lines + len(SVG_TEXT.findall(body))


def check_orientation(page: Path, src: str) -> list[Finding]:
    """The big picture comes first.

    Every content page opens with a figure that says where this idea sits in the
    whole: what it is part of, what came before it, what it enables. It is the
    page's first figure and it stands between the one-minute version and the
    first body section, so a reader who looks at nothing else knows what the
    page is about and why it exists.
    """
    if not is_lesson(page):
        return []
    body = reading_column(src)
    start = body.find("<figure")
    if start < 0:
        return [Finding(rel(page), "WARN", "no orientation figure; a content page opens with the big picture")]

    found: list[Finding] = []
    lead = body[:start]
    sections = len(SECTION_HEADING.findall(lead))
    if sections > MAX_SECTIONS_BEFORE_ORIENTATION:
        found.append(
            Finding(rel(page), "WARN",
                    f"the first figure arrives {sections} sections in; the orientation figure belongs "
                    "between the one-minute version and the first body section")
        )
    words = prose(lead)
    if words > MAX_WORDS_BEFORE_ORIENTATION:
        found.append(
            Finding(rel(page), "WARN",
                    f"{words} words of prose before the first figure, the cap is "
                    f"{MAX_WORDS_BEFORE_ORIENTATION}; the reader gets the picture first")
        )
    end = body.find("</figure>", start)
    drawn = figure_lines(body[start:end if end > 0 else len(body)])
    if drawn < MIN_ORIENTATION_LINES:
        found.append(
            Finding(rel(page), "WARN",
                    f"the orientation figure draws {drawn} thing(s), the floor is {MIN_ORIENTATION_LINES}; "
                    "it must show what came before this idea, the idea, and what it enables")
        )
    return found


def check_word_load(page: Path, src: str) -> list[Finding]:
    """Fewer words, and more of the meaning carried by the picture.

    Both ceilings are measured off the pages that read best rather than chosen:
    every page in ``llm-papers-course`` and ``llm-inference-course`` clears them.
    When a paragraph and a figure say the same thing, the paragraph goes.
    """
    if not is_lesson(page):
        return []
    found: list[Finding] = []
    words = prose(reading_column(src))
    figures = len(FIGURE.findall(src))
    if words > MAX_PROSE_WORDS_PER_PAGE:
        found.append(
            Finding(rel(page), "WARN",
                    f"{words} words of prose, the ceiling is {MAX_PROSE_WORDS_PER_PAGE}; "
                    "cut what a figure already says, or split the page")
        )
    if figures and words / figures > MAX_PROSE_WORDS_PER_FIGURE:
        found.append(
            Finding(rel(page), "WARN",
                    f"{round(words / figures)} words per figure, the ceiling is {MAX_PROSE_WORDS_PER_FIGURE}; "
                    "the picture is not carrying its share")
        )
    return found


def on_extended_bar(page: Path) -> bool:
    """Whether this page's course has opted into the bars added after the seven."""
    course = course_of(page)
    return course is not None and course.name in EXTENDED_BAR_COURSES


def check_practice(page: Path, src: str) -> list[Finding]:
    """A quiz is answered in the head; a problem is worked on paper.

    The reader attempts it before anything is revealed, so every problem owes a
    hidden worked solution and the sanity check that lets them catch their own
    arithmetic without being told the answer twice.
    """
    if not is_lesson(page) or not on_extended_bar(page):
        return []
    body = reading_column(src)
    blocks = len(PRACTICE_OPEN.findall(body))
    if blocks < MIN_PRACTICE_PER_PAGE:
        return [
            Finding(rel(page), "FAIL",
                    f"{blocks} practice problem(s), the floor is {MIN_PRACTICE_PER_PAGE}; "
                    "a quiz is answered in the head and a problem is worked on paper")
        ]
    found: list[Finding] = []
    solutions = len(PRACTICE_SOLUTION.findall(body))
    if solutions < blocks:
        found.append(
            Finding(rel(page), "FAIL",
                    f"{blocks} practice problem(s) but {solutions} details.solution; "
                    "every problem reveals its own worked solution")
        )
    checks = len(PRACTICE_CHECK.findall(body))
    if checks < blocks:
        found.append(
            Finding(rel(page), "FAIL",
                    f"{blocks} practice problem(s) but {checks} .p-check; every solution ends with "
                    "the sanity check that lets a reader catch their own error")
        )
    return found


def check_quantitative(page: Path, src: str) -> list[Finding]:
    """Mermaid cannot draw a distribution, a density, a vector or a unit ball.

    A mathematics page that states a quantity and draws only boxes and arrows has
    made a claim it did not show.
    """
    if not is_lesson(page) or not on_extended_bar(page):
        return []
    if len(CHART_SVG.findall(reading_column(src))) >= MIN_CHARTS_PER_PAGE:
        return []
    return [
        Finding(rel(page), "FAIL",
                f"no hand-authored svg.chart, the floor is {MIN_CHARTS_PER_PAGE}; "
                "Mermaid cannot draw a distribution, a density or a vector")
    ]


def check_math(page: Path, src: str) -> list[Finding]:
    return [
        Finding(rel(page), "FAIL", "a .math block has no .gloss naming its symbols")
        for body in MATH_BLOCK.findall(src)
        if 'class="gloss"' not in body
    ]


def check_quizzes(page: Path, src: str) -> tuple[list[Finding], list[int]]:
    found: list[Finding] = []
    answers: list[int] = []
    blocks = QUIZ_BLOCK.findall(src)
    for index, (raw_answer, body) in enumerate(blocks):
        answer = int(raw_answer)
        options = [plain(option) for option in OPTION.findall(body)]
        where = f"quiz {index}"
        if len(options) != QUIZ_OPTIONS:
            found.append(Finding(rel(page), "FAIL", f"{where} has {len(options)} options, not {QUIZ_OPTIONS}"))
            continue
        if not 0 <= answer < len(options):
            found.append(Finding(rel(page), "FAIL", f"{where} data-answer={answer} is out of range"))
            continue
        answers.append(answer)
        if 'class="q-stem"' not in body:
            found.append(Finding(rel(page), "FAIL", f"{where} has no .q-stem"))
        if 'class="q-fb"' not in body:
            found.append(Finding(rel(page), "FAIL", f"{where} has no .q-fb explaining the wrong options"))
        lengths = [len(option) for option in options]
        spread = max(lengths) - min(lengths)
        if spread > MAX_OPTION_CHAR_SPREAD:
            found.append(
                Finding(rel(page), "FAIL",
                        f"{where} option lengths spread {spread} chars, the cap is {MAX_OPTION_CHAR_SPREAD} ({lengths})")
            )
    if is_lesson(page) and len(blocks) < MIN_QUIZZES_PER_PAGE and "start-here" not in page.name:
        found.append(Finding(rel(page), "WARN", f"{len(blocks)} quizzes, the floor is {MIN_QUIZZES_PER_PAGE}"))
    return found, answers


def check_signposting(page: Path, src: str) -> list[Finding]:
    if not is_lesson(page):
        return []
    found: list[Finding] = []
    meta = re.search(r'<p class="paper-meta">(.*?)</p>', src, re.S)
    meta_text = meta.group(1) if meta else ""
    if not READING_PILL.search(meta_text):
        found.append(Finding(rel(page), "WARN", "no reading-time pill in .paper-meta"))
    rungs = RUNG_PILL.findall(meta_text)
    if not rungs:
        found.append(Finding(rel(page), "WARN", "no rung pill in .paper-meta"))
    elif len(rungs) > 1:
        found.append(Finding(rel(page), "WARN", f"{len(rungs)} rung pills; a page sits at one rung"))
    if '<div class="card tldr">' not in src:
        found.append(Finding(rel(page), "WARN", "no .card.tldr one-minute version"))
    if not PAGER.search(src):
        found.append(Finding(rel(page), "FAIL", "no .pager"))
    if 'class="teacher-note"' not in src:
        found.append(Finding(rel(page), "WARN", "no .teacher-note"))
    return found


def check_course_files(course: Path) -> list[Finding]:
    required = ("MISSION.md", "NOTES.md", "RESOURCES.md", "BUILDER-SPEC.md", "index.html")
    found = [
        Finding(rel(course), "FAIL", f"course is missing {name}")
        for name in required
        if not (course / name).is_file()
    ]
    if not (course / "outline.js").is_file():
        found.append(Finding(rel(course), "FAIL", "course has no outline.js; run scripts/gen_outline.py"))
    return found


def check_course_hue(course: Path) -> list[Finding]:
    """A course with no line in the course-accent block wears the plain palette
    accent, which is dull rather than broken, and is therefore never noticed."""
    sheet = REPO_ROOT / "assets" / "hub.css"
    if not sheet.is_file():
        return []
    if f'[data-course="{course.name}"]' in sheet.read_text(encoding="utf-8", errors="replace"):
        return []
    return [Finding(rel(course), "WARN", "no --course-hue line in assets/hub.css; it wears the plain palette accent")]


def check_course_totals(course: Path, answers: list[int], kinds: set[str], cards: int) -> list[Finding]:
    found: list[Finding] = []
    if answers:
        counts = Counter(answers)
        top, count = counts.most_common(1)[0]
        share = count / len(answers)
        if share > MAX_ANSWER_INDEX_SHARE:
            found.append(
                Finding(rel(course), "WARN",
                        f"{share:.0%} of answers sit at index {top} ({count}/{len(answers)}); "
                        f"the cap is {MAX_ANSWER_INDEX_SHARE:.0%}")
            )
    if kinds and len(kinds) < MIN_DIAGRAM_KINDS_PER_COURSE:
        found.append(
            Finding(rel(course), "WARN",
                    f"{len(kinds)} diagram kinds across the course ({', '.join(sorted(kinds))}); "
                    f"the floor is {MIN_DIAGRAM_KINDS_PER_COURSE}")
        )
    if not kinds & HAND_KINDS:
        found.append(Finding(rel(course), "WARN", "no hand-authored svg.chart anywhere; nothing is drawn by hand"))
    lessons = len(list((course / "lessons").glob("*.html"))) if (course / "lessons").is_dir() else 0
    if lessons and cards < lessons:
        found.append(Finding(rel(course), "WARN", f"course map carries {cards} rung pills for {lessons} lessons"))
    return found


def pages_under(target: Path) -> list[Path]:
    """Every published page under a target.

    Dot-directories are tool state and never site content, which is also how
    ``scripts/validate_site.py`` decides. It is what keeps this checker from
    walking into its own templates.
    """
    if target.is_file():
        return [target]
    return sorted(
        page
        for page in target.rglob("*.html")
        if not any(part.startswith(".") for part in page.relative_to(REPO_ROOT).parts)
        and "node_modules" not in page.parts
    )


def course_of(page: Path) -> Path | None:
    """The course a page belongs to, or ``None`` if it belongs to no course.

    A page directly under the repository root is the hub landing page, and a
    page under a top-level folder that ships no ``lessons/`` is part of a hub
    section rather than of a course. Both answer ``None``, which is what keeps
    the course-wide bars off a page that is not teaching anything.
    """
    for parent in page.parents:
        if parent.parent == REPO_ROOT and is_course(parent):
            return parent
    return None


def main() -> int:
    targets = [Path(argument).resolve() for argument in sys.argv[1:]] or [REPO_ROOT]
    # A course-wide bar cannot be judged from one page: "50% of answers sit at
    # index 2" out of a single quiz pair says nothing, and the diagram-kind
    # floor is a property of the course. Checking one file reports on that file.
    whole_courses = all(target.is_dir() for target in targets)
    css_classes = declared_css_classes()
    findings: list[Finding] = []
    per_course_answers: dict[Path, list[int]] = {}
    per_course_kinds: dict[Path, set[str]] = {}

    pages: list[Path] = []
    for target in targets:
        pages.extend(pages_under(target))

    for page in pages:
        src = page.read_text(encoding="utf-8", errors="replace")
        findings += check_no_em_dash(page, src)
        findings += check_design_system(page, src)
        findings += check_mermaid(page, src)
        findings += check_figures(page, src, css_classes)
        findings += check_orientation(page, src)
        findings += check_word_load(page, src)
        findings += check_math(page, src)
        findings += check_practice(page, src)
        findings += check_quantitative(page, src)
        findings += check_signposting(page, src)
        quiz_findings, answers = check_quizzes(page, src)
        findings += quiz_findings

        course = course_of(page)
        if course is None:
            continue
        per_course_answers.setdefault(course, []).extend(answers)
        kinds = per_course_kinds.setdefault(course, set())
        kinds |= mermaid_kinds(src) | svg_kinds(src)

    for course in sorted(set(per_course_answers) | set(per_course_kinds)) if whole_courses else []:
        findings += check_course_files(course)
        findings += check_course_hue(course)
        course_map = course / "index.html"
        cards = (
            len(RUNG_PILL.findall(course_map.read_text(encoding="utf-8", errors="replace")))
            if course_map.is_file()
            else 0
        )
        findings += check_course_totals(
            course, per_course_answers.get(course, []), per_course_kinds.get(course, set()), cards
        )

    fails = [finding for finding in findings if finding.severity == "FAIL"]
    warns = [finding for finding in findings if finding.severity == "WARN"]

    for finding in fails + warns:
        print(finding.render())

    print(f"\nchecked {len(pages)} page(s): {len(fails)} failure(s), {len(warns)} warning(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
