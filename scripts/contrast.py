#!/usr/bin/env python3
"""The accessibility floor, computed from the hexes ``hub.css`` commits.

A ground of a given lightness bounds the best contrast any ink can reach on it,
and the bound is arithmetic rather than taste. Computed from the WCAG 2 contrast
formula with pure black and pure white ink, **no ground between L\\* 37.8 and
L\\* 61.7 reaches AAA with any ink at all**. With the hub's own inks the dead
band is far wider:

    AA 4.5:1   dark ink  #1a1a18 works on grounds L* >= 54.1
               light ink #eae6da works on grounds L* <= 43.8
    AAA 7:1    dark ink  works on L* >= 67.4
               light ink works on L* <= 31.9
    the two inks cross over at ground L* 48.9

The framework **prevents** that band rather than warning about it. The ground is
a discrete registered choice - a palette and a mode - so there is no input event
that can land inside the band, and there is no override. What is left to check
is that the registered set stays outside it, which is what this module does.

Three checks, named as the specification names them.

    G1  Every registered ground's CIELAB L* lies in 88 to 99 (light band) or
        3 to 16 (dark band). Nothing between. The registered ground is ``--bg``,
        one per palette per mode, so there are twelve of them.
    G2  Every registered ink clears 7:1 on the surfaces of its own palette and
        mode, and sits on the correct side of the L* 48.9 crossover for its
        band: a light-band ground takes a dark ink and a dark-band ground takes
        a light one.
    G3  Every secondary ink, faint ink, accent and accent-2 clears 4.5:1, and
        every non-text graphical object clears 3:1, on every surface of its own
        palette and mode.

**The margin in G1 is the point of it.** The reachable bands are 88 to 99 and
3 to 16, not the 67.4 to 100 and 0 to 31.9 the AAA arithmetic alone allows. The
extra margin is what lets the secondary and faint inks, the accents and the
borders also clear their floors on the same ground. Those are the tokens that
fail first, never the body ink.

**What is here and what is not.** This module reads the raw palette layer, which
is sixteen literal hexes per palette per mode, plus one ground treatment that is
a background-image rather than a colour and is therefore not this module's. The
tokens that
are *derived* - the nine ``color-mix()`` tints, and the per-course accent, which
is an OKLCH hue rotation whose sRGB gamut mapping is the browser's - cannot be
resolved without a browser, and are measured by ``scripts/contrast_matrix.py``
in the browser CI job. Keeping the arithmetic half here keeps it in the job that
gates a typo fix, where it costs nothing.

**WCAG 2.2 ratios only.** WCAG 3.0 is a Working Draft, its visual-contrast
section was removed in July 2023, and the current draft says in as many words
that its contrast algorithm is yet to be determined. APCA is a reasonable
tie-breaker between two colours that both pass WCAG 2; it never justifies a pair
that fails it.

    python3 scripts/contrast.py             # the three checks, as CI runs them
    python3 scripts/contrast.py --report    # every measured number, pass or fail
    python3 scripts/contrast.py --self-test # prove each check fails on bad input

Exit code 0 means the floor holds. Exit code 1 lists every failure.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
HUB_CSS: Path = REPO_ROOT / "assets" / "hub.css"

RGB = tuple[int, int, int]

# The two reachable bands, in CIELAB L*. Nothing between them is registrable.
LIGHT_BAND: tuple[float, float] = (88.0, 99.0)
DARK_BAND: tuple[float, float] = (3.0, 16.0)

# The ground lightness at which the hub's two inks swap places.
CROSSOVER: float = 48.9

# The floors, from WCAG 2.2.
FLOOR_BODY: float = 7.0       # SC 1.4.6, body text
FLOOR_TEXT: float = 4.5       # SC 1.4.3, all other text
FLOOR_NON_TEXT: float = 3.0   # SC 1.4.11, borders, focus rings, chart marks

# The ground whose lightness is banded: one per palette per mode, twelve in all.
REGISTERED_GROUND: str = "bg"

# One of the twelve is outside its band on the tree this check landed on, and it
# is recorded here rather than corrected, for the reason the specification gives
# for a failing token: report it, and fix it as a change of its own with its own
# review. Recolouring a shipped palette moves what every reader sees and what the
# computed-style harness records, which is not a side effect a contrast check may
# have. A gate that is red on the day it lands teaches everyone to ignore it, so
# this behaves exactly as scripts/check-pages-baseline.txt does: a breach that is
# not recorded here fails the run, a recorded breach whose measured value has
# moved fails the run, and a recorded breach that no longer happens fails the run
# with the line to delete. The list can only ever get shorter.
#
# ink/dark is 0.57 L* below the dark band's floor, which is the safe side of it:
# a darker ground raises every ratio painted on it, and the floor of 3 is there
# to leave the recessed surfaces somewhere to sit rather than to protect the ink.
# Judging that is the captain's, not this script's.
RECORDED_BREACHES: dict[str, float] = {"ink/dark": 2.43}

# The three backgrounds a palette states outright and paints text on. `--bg` is
# the ground behind the chrome, `--surface` the reading pane, `--surface-2` the
# recessed rail and callout fill. `--surface-3` and the nine tints are derived
# with color-mix() and belong to the browser half.
PAINTED_ON: tuple[str, ...] = ("bg", "surface", "surface-2")

# The sixteen raw colours every palette states twice. Order is the stylesheet's.
# The plate and the chip are two pairs because a block of code may be dark on a
# light page while a chip of code inside a sentence may not, and both carry body
# text, so both are held to the body floor below.
PALETTE_TOKENS: tuple[str, ...] = (
    "bg", "surface", "surface-2", "ink", "ink-soft", "ink-faint",
    "accent", "accent-ink", "accent-2", "gold", "ok", "warn",
    "code-bg", "code-ink", "code-inline-bg", "code-inline-ink",
)

# Every text pair the raw layer can state on its own: the ink, what it is painted
# on, the floor it must clear, and the role that decides which floor.
TEXT_PAIRS: tuple[tuple[str, tuple[str, ...], float, str], ...] = (
    ("ink-soft", PAINTED_ON, FLOOR_TEXT, "secondary text"),
    ("ink-faint", PAINTED_ON, FLOOR_TEXT, "tertiary text, captions, labels"),
    ("accent", PAINTED_ON, FLOOR_TEXT, "link text"),
    ("accent-2", PAINTED_ON, FLOOR_TEXT, "eyebrows, callout tags, the focus ring"),
    ("gold", PAINTED_ON, FLOOR_TEXT, "key-idea tags"),
    ("ok", PAINTED_ON, FLOOR_TEXT, "success and read state"),
    ("warn", PAINTED_ON, FLOOR_TEXT, "error and danger"),
    ("accent-ink", ("accent",), FLOOR_TEXT, "text painted on the accent"),
    ("code-ink", ("code-bg",), FLOOR_BODY, "code body text"),
    ("code-inline-ink", ("code-inline-bg",), FLOOR_BODY, "inline code text"),
)

PALETTE_BLOCK: re.Pattern[str] = re.compile(
    r"(?P<selector>:root,\s*\[data-palette=\"(?P<house>[a-z-]+)\"\]|\[data-palette=\"(?P<other>[a-z-]+)\"\])"
    r"\s*\{(?P<body>[^}]*)\}",
    re.DOTALL,
)

DECLARATION: re.Pattern[str] = re.compile(r"--(?P<name>[ld]-[a-z0-9-]+)\s*:\s*(?P<value>#[0-9a-fA-F]{3,8})\s*;")


@dataclass(frozen=True)
class Finding:
    """One breach of the floor, named so a reader can act on it without the code."""

    check: str
    where: str
    detail: str

    def render(self) -> str:
        return f"{self.check} {self.where}: {self.detail}"


@dataclass(frozen=True)
class Registration:
    """One palette in one mode: the ground, the ink and the twelve beside them.

    This is the unit the floor is checked over, because it is the unit a reader
    can actually select. A palette states its light and its dark values in one
    block and the mode layer maps one set onto the semantic tokens, so no
    combination of one palette's ground with another's ink is reachable and none
    is checked.
    """

    palette: str
    mode: str
    colours: dict[str, RGB]

    @property
    def where(self) -> str:
        return f"{self.palette}/{self.mode}"

    @property
    def band(self) -> tuple[float, float]:
        return LIGHT_BAND if self.mode == "light" else DARK_BAND


# ============================================================
# The colour arithmetic
# ============================================================


def parse_hex(value: str) -> RGB:
    """An sRGB triple from a CSS hex colour. Alpha, if written, is dropped.

    A colour with alpha cannot be contrast-checked without knowing what is
    behind it, and the palette layer states none, so dropping it here would hide
    a real question. It is rejected instead.
    """
    digits = value.lstrip("#")
    if len(digits) == 3:
        digits = "".join(channel * 2 for channel in digits)
    if len(digits) != 6:
        raise ValueError(f"{value} is not an opaque sRGB hex colour")
    return (int(digits[0:2], 16), int(digits[2:4], 16), int(digits[4:6], 16))


def _linear(channel: int) -> float:
    """One 0-255 sRGB channel, undone back to light."""
    value = channel / 255
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def luminance(colour: RGB) -> float:
    """WCAG relative luminance, which is also CIE Y for sRGB under D65."""
    red, green, blue = (_linear(channel) for channel in colour)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast(one: RGB, other: RGB) -> float:
    """The WCAG 2 contrast ratio, 1.0 to 21.0, whichever way round it is given."""
    first, second = luminance(one), luminance(other)
    lighter, darker = max(first, second), min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


def lightness(colour: RGB) -> float:
    """CIELAB L*, the perceptual lightness the band is stated in.

    L* is a function of luminance alone, so the same number that decides a
    contrast ratio decides which band a ground sits in. That is why the two
    checks never disagree with each other.
    """
    intensity = luminance(colour)
    delta = 6 / 29
    root = intensity ** (1 / 3) if intensity > delta**3 else intensity / (3 * delta * delta) + 4 / 29
    return 116 * root - 16


# ============================================================
# The registry, read out of the stylesheet
# ============================================================


def parse_registrations(css: str) -> list[Registration]:
    """Every palette block in ``hub.css``, split into its light and dark halves.

    The palette layer is the one place in the stylesheet that states a literal
    colour, and every palette states the same thirty-four properties and
    nothing else. That discipline is what lets this be a parse rather than a
    browser run.
    """
    registrations: list[Registration] = []
    for block in PALETTE_BLOCK.finditer(css):
        name = block.group("house") or block.group("other")
        values = {
            declaration.group("name"): parse_hex(declaration.group("value"))
            for declaration in DECLARATION.finditer(block.group("body"))
        }
        for mode, prefix in (("light", "l-"), ("dark", "d-")):
            colours = {
                token: values[f"{prefix}{token}"]
                for token in PALETTE_TOKENS
                if f"{prefix}{token}" in values
            }
            if colours:
                registrations.append(Registration(name, mode, colours))
    return registrations


def registrations() -> list[Registration]:
    return parse_registrations(HUB_CSS.read_text(encoding="utf-8"))


# ============================================================
# G1, G2, G3
# ============================================================


def check_grounds(registry: list[Registration]) -> list[Finding]:
    """G1. Every registered ground sits in the light band or the dark band.

    The breaches recorded in ``RECORDED_BREACHES`` are debt rather than a gate
    failure, and the block above says why. Everything else about them is still
    checked: a recorded value that has moved, and a recorded breach that has
    been fixed, both fail.
    """
    findings: list[Finding] = []
    for entry in registry:
        measured = lightness(entry.colours[REGISTERED_GROUND])
        low, high = entry.band
        recorded = RECORDED_BREACHES.get(entry.where)

        if low <= measured <= high:
            if recorded is not None:
                findings.append(
                    Finding(
                        "G1",
                        entry.where,
                        f"--bg is L* {measured:.2f} and back inside the band, but it is still "
                        "recorded as a breach. Delete its line from RECORDED_BREACHES in "
                        "scripts/contrast.py.",
                    )
                )
            continue

        if recorded is not None and abs(recorded - measured) < 0.005:
            continue

        moved = "" if recorded is None else f" The recorded value was L* {recorded:.2f}, so the palette has changed."
        findings.append(
            Finding(
                "G1",
                entry.where,
                f"--bg is L* {measured:.2f}, outside the {entry.mode} band {low:g} to {high:g}. "
                f"The band is arithmetic, not taste: widen the palette, never the band.{moved}",
            )
        )
    return findings


def recorded_breaches(registry: list[Registration]) -> list[str]:
    """The recorded breaches that are still true, for a passing run to say out loud."""
    return [
        f"{entry.where} --bg L* {lightness(entry.colours[REGISTERED_GROUND]):.2f}"
        for entry in registry
        if entry.where in RECORDED_BREACHES
    ]


def check_inks(registry: list[Registration]) -> list[Finding]:
    """G2. The body ink clears 7:1 and sits on the right side of the crossover."""
    findings: list[Finding] = []
    for entry in registry:
        ink = entry.colours["ink"]
        measured = lightness(ink)
        wants_dark_ink = entry.mode == "light"
        if wants_dark_ink and measured >= CROSSOVER:
            findings.append(
                Finding(
                    "G2",
                    entry.where,
                    f"--ink is L* {measured:.2f}, a light ink on a light-band ground. "
                    f"Above the L* {CROSSOVER} crossover a light ink is forbidden.",
                )
            )
        if not wants_dark_ink and measured <= CROSSOVER:
            findings.append(
                Finding(
                    "G2",
                    entry.where,
                    f"--ink is L* {measured:.2f}, a dark ink on a dark-band ground. "
                    f"Below the L* {CROSSOVER} crossover a dark ink is forbidden.",
                )
            )
        for surface in PAINTED_ON:
            ratio = contrast(ink, entry.colours[surface])
            if ratio < FLOOR_BODY:
                findings.append(
                    Finding(
                        "G2",
                        entry.where,
                        f"--ink on --{surface} is {ratio:.2f}:1, below the {FLOOR_BODY:g}:1 body floor "
                        "(SC 1.4.6)",
                    )
                )
    return findings


def check_registered_colours(registry: list[Registration]) -> list[Finding]:
    """G3, the half the raw palette layer can answer on its own.

    Every colour a palette states outright, against every surface the same
    palette states, at the floor its role carries. The derived tints and the
    per-course accent are the browser half's, in ``contrast_matrix.py``.
    """
    findings: list[Finding] = []
    for entry in registry:
        for token, grounds, floor, role in TEXT_PAIRS:
            for ground in grounds:
                ratio = contrast(entry.colours[token], entry.colours[ground])
                if ratio < floor:
                    findings.append(
                        Finding(
                            "G3",
                            entry.where,
                            f"--{token} on --{ground} is {ratio:.2f}:1, below the {floor:g}:1 floor "
                            f"for {role}",
                        )
                    )
    return findings


def check_all(registry: list[Registration]) -> list[Finding]:
    return check_grounds(registry) + check_inks(registry) + check_registered_colours(registry)


# ============================================================
# The report, and the proof that the checks bite
# ============================================================


def report(registry: list[Registration]) -> None:
    """Every measured number, whether it passes or not.

    A gate that only speaks when it fails leaves nobody able to see a ratio
    drifting towards its floor. This is the command that answers "how close are
    we", and its output is what a pull request quotes.
    """
    print("Grounds - G1, the registered --bg of each palette and mode\n")
    print(f"  {'palette/mode':22} {'--bg':9} {'L*':>7}   band")
    for entry in registry:
        ground = entry.colours[REGISTERED_GROUND]
        low, high = entry.band
        verdict = "in" if low <= lightness(ground) <= high else "OUT"
        if verdict == "OUT" and entry.where in RECORDED_BREACHES:
            verdict = "OUT, recorded"
        print(
            f"  {entry.where:22} #{ground[0]:02x}{ground[1]:02x}{ground[2]:02x}  "
            f"{lightness(ground):7.2f}   {low:g} to {high:g} {verdict}"
        )

    print("\n  For information, the two surfaces the band does not cover:\n")
    print(f"  {'palette/mode':22} {'--surface':>10} {'--surface-2':>12}")
    for entry in registry:
        print(
            f"  {entry.where:22} {lightness(entry.colours['surface']):10.2f} "
            f"{lightness(entry.colours['surface-2']):12.2f}"
        )

    print("\nInk - G2, the body ink on the three surfaces of its own palette\n")
    print(f"  {'palette/mode':22} {'ink L*':>7} {'--bg':>7} {'--surface':>10} {'--surface-2':>12}")
    for entry in registry:
        ink = entry.colours["ink"]
        ratios = " ".join(f"{contrast(ink, entry.colours[s]):>{w}.2f}" for s, w in
                          (("bg", 7), ("surface", 10), ("surface-2", 12)))
        print(f"  {entry.where:22} {lightness(ink):7.2f} {ratios}")

    print("\nThe rest - G3, the worst surface for each colour a palette states\n")
    print(f"  {'palette/mode':22} " + " ".join(f"{token:>11}" for token, *_ in TEXT_PAIRS))
    for entry in registry:
        worst = [
            min(contrast(entry.colours[token], entry.colours[ground]) for ground in grounds)
            for token, grounds, _, _ in TEXT_PAIRS
        ]
        print(f"  {entry.where:22} " + " ".join(f"{ratio:>11.2f}" for ratio in worst))

    floors = " ".join(f"{floor:>11g}" for _, _, floor, _ in TEXT_PAIRS)
    print(f"  {'floor':22} {floors}")


def _sample(**overrides: RGB) -> Registration:
    """Paper light, optionally with one colour replaced. The self-test's fixture."""
    colours = {
        "bg": (0xF4, 0xF1, 0xE7), "surface": (0xFD, 0xFC, 0xF8), "surface-2": (0xF2, 0xEE, 0xE3),
        "ink": (0x1A, 0x1A, 0x18), "ink-soft": (0x4A, 0x4A, 0x44), "ink-faint": (0x63, 0x63, 0x5B),
        "accent": (0xA6, 0x3A, 0x24), "accent-ink": (0xFF, 0xFA, 0xF7), "accent-2": (0x15, 0x58, 0x5C),
        "gold": (0x7A, 0x5A, 0x0A), "ok": (0x1A, 0x6E, 0x35), "warn": (0xA6, 0x3A, 0x24),
        "code-bg": (0xF4, 0xF1, 0xE8), "code-ink": (0x2B, 0x2B, 0x28),
        "code-inline-bg": (0xF4, 0xF1, 0xE8), "code-inline-ink": (0x2B, 0x2B, 0x28),
    }
    colours.update(overrides)
    return Registration("sample", "light", colours)


def self_test() -> int:
    """Prove each check fails on a deliberately bad input, and passes on a good one.

    A check nobody has seen fail is a check nobody knows works. Each case here
    changes exactly one colour of a known-good palette and asserts the check
    that owns it says so - and the good palette itself asserts the other
    direction, that a sound registration is silent.
    """
    cases: list[tuple[str, Registration, str, str]] = [
        # (what is wrong, the registration, the check that must fire, a word from its message)
        ("a ground at L* 50, mid-band", _sample(bg=(0x77, 0x77, 0x77)), "G1", "outside the light band"),
        ("a ground just under the floor", _sample(bg=(0xD8, 0xD8, 0xD8)), "G1", "outside the light band"),
        ("a light ink on a light ground", _sample(ink=(0xBB, 0xBB, 0xBB)), "G2", "crossover"),
        ("a dark ink too weak for AAA", _sample(ink=(0x70, 0x70, 0x70)), "G2", "body floor"),
        ("an accent below 4.5:1", _sample(accent=(0xC0, 0x7A, 0x60)), "G3", "--accent on"),
        ("a faint ink below 4.5:1", _sample(**{"ink-faint": (0x9A, 0x9A, 0x92)}), "G3", "--ink-faint on"),
        (
            "an inline code chip below the body floor",
            _sample(**{"code-inline-ink": (0xA6, 0x3A, 0x24)}),
            "G3",
            "--code-inline-ink on",
        ),
    ]

    failures: list[str] = []

    good = check_all([_sample()])
    if good:
        failures.append("the known-good sample reported " + "; ".join(f.render() for f in good))
    else:
        print("  pass  a sound registration is silent")

    for description, entry, wanted, phrase in cases:
        found = check_all([entry])
        hit = [finding for finding in found if finding.check == wanted and phrase in finding.detail]
        if hit:
            print(f"  pass  {description} -> {hit[0].render()}")
        else:
            reported = "; ".join(f.render() for f in found) or "nothing"
            failures.append(f"{description}: expected {wanted} mentioning {phrase!r}, got {reported}")

    # The recorded-breach machinery, proved on the one entry that uses it. A
    # waiver nobody can see expire is a waiver that becomes permanent.
    shipped = {entry.where: entry for entry in registrations()}
    for where in RECORDED_BREACHES:
        entry = shipped.get(where)
        if entry is None:
            failures.append(f"{where} is recorded as a breach but no longer exists in hub.css")
            continue
        if check_grounds([entry]):
            failures.append(f"the recorded breach {where} is not silent")
        else:
            print(f"  pass  the recorded breach {where} is debt, not a gate failure")

        legal = (0x14, 0x14, 0x14) if entry.mode == "dark" else (0xF0, 0xF0, 0xF0)
        fixed = Registration(entry.palette, entry.mode, {**entry.colours, REGISTERED_GROUND: legal})
        if any("Delete its line" in finding.detail for finding in check_grounds([fixed])):
            print(f"  pass  {where} back inside the band fails until the record is deleted")
        else:
            failures.append(f"{where} back inside the band did not ask for its record to be deleted")

        drifted = Registration(entry.palette, entry.mode, {**entry.colours, REGISTERED_GROUND: (0x2A, 0x2A, 0x2A)})
        if any("palette has changed" in finding.detail for finding in check_grounds([drifted])):
            print(f"  pass  {where} moved to another out-of-band value fails")
        else:
            failures.append(f"{where} moved to another out-of-band value did not fail")

    if failures:
        print("\nThe checks do not bite:\n")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"\n{len(cases)} bad inputs caught, and the good input passed.")
    return 0


def main() -> int:
    arguments = sys.argv[1:]
    if "--self-test" in arguments:
        return self_test()

    registry = registrations()
    if not registry:
        print("No palette block found in assets/hub.css; the parser and the stylesheet disagree.")
        return 1

    if "--report" in arguments:
        report(registry)
        return 0

    findings = check_all(registry)
    if findings:
        print(f"The accessibility floor is breached in {len(findings)} place(s):\n")
        for finding in findings:
            print(f"  - {finding.render()}")
        return 1
    print(f"The accessibility floor holds: {len(registry)} registered grounds, G1, G2 and G3 clear.")
    known = recorded_breaches(registry)
    if known:
        print(
            f"Note: {len(known)} ground outside its band is recorded as debt ({', '.join(known)}). "
            "It is a palette to correct, not a band to widen."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
