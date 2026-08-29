#!/usr/bin/env python3
"""Run the house-standard page checker in CI, against a recorded baseline.

``.claude/skills/course-authoring/scripts/check_pages.py`` has guarded part of
the design system since it was written - a hard-coded colour in an SVG, a chart
class the stylesheet does not define, an ``svg.chart`` with no ``aria-label`` or
no ``viewBox``, and the head-order contract - and CI has never run it. This is
what runs it.

It cannot simply be made a gate as it stands, because the hub carries failures
it already reported before anyone was listening. A gate that is red on the day
it lands teaches everyone to ignore it, so the failures that exist today are
recorded in ``scripts/check-pages-baseline.txt`` and the gate is on the
difference:

* a failure that is not in the baseline fails the run - that is a regression,
  and it is caught on the pull request that causes it;
* a failure in the baseline that no longer happens also fails the run, with the
  command to refresh the file - that is how the debt only ever gets smaller.

Fixing what the baseline records is a separate piece of work. This script does
not judge the entries; it stops the list growing.

    python3 scripts/check_pages_gate.py           # the gate
    python3 scripts/check_pages_gate.py --write   # re-record the baseline

Exit code 0 means the failure list is exactly the recorded one.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
CHECKER: Path = REPO_ROOT / ".claude" / "skills" / "course-authoring" / "scripts" / "check_pages.py"
BASELINE: Path = REPO_ROOT / "scripts" / "check-pages-baseline.txt"

HEADER: str = """# Every failure check_pages.py reports on this tree today.
#
# Recorded so that the checker can be a gate on the difference rather than on
# the total: a new failure fails the pull request that introduces it, and a
# failure that has been fixed fails until it is taken out of this file.
#
# Refresh with: python3 scripts/check_pages_gate.py --write
# Nothing here is approved. Every line is a page waiting to be fixed.
"""


def current_failures() -> list[str]:
    """Every FAIL line the checker reports, as ``where: detail``."""
    if not CHECKER.is_file():
        raise SystemExit(f"the page checker is missing: {CHECKER.relative_to(REPO_ROOT)}")
    finished = subprocess.run(
        [sys.executable, str(CHECKER)], capture_output=True, text=True, cwd=REPO_ROOT
    )
    if finished.returncode not in (0, 1):
        raise SystemExit(f"the page checker exited {finished.returncode}:\n{finished.stderr}")
    failures = [
        line.strip()[len("FAIL") :].strip()
        for line in finished.stdout.splitlines()
        if line.strip().startswith("FAIL")
    ]
    return sorted(failures)


def recorded_failures() -> list[str]:
    if not BASELINE.is_file():
        raise SystemExit(f"no baseline at {BASELINE.relative_to(REPO_ROOT)}; run --write")
    return sorted(
        line.strip()
        for line in BASELINE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--write", action="store_true", help="re-record the baseline from this tree")
    arguments = parser.parse_args()

    failures = current_failures()
    if arguments.write:
        BASELINE.write_text(HEADER + "\n".join(failures) + "\n", encoding="utf-8")
        print(f"{BASELINE.relative_to(REPO_ROOT)}: {len(failures)} recorded failure(s)")
        return 0

    recorded = recorded_failures()
    added = [failure for failure in failures if failure not in recorded]
    fixed = [failure for failure in recorded if failure not in failures]

    if added:
        print(f"{len(added)} new house-standard failure(s):\n")
        for failure in added:
            print(f"  - {failure}")
    if fixed:
        print(f"\n{len(fixed)} recorded failure(s) no longer happen:\n")
        for failure in fixed:
            print(f"  - {failure}")
        print("\nTake them out: python3 scripts/check_pages_gate.py --write")
    if added or fixed:
        return 1

    print(f"House standard: {len(failures)} known failure(s), none of them new.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
