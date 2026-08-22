import re, html, pathlib, sys

"""Check that a lesson's h1 agrees with every place its title is echoed.

A title lives in four places: the page's own h1, its card in the course
index, the sidebar rail generated from that card, and the .ttl of every
pager that points at it. When one of them is edited and the others are not,
the reader clicks a link expecting one page and lands on a differently
titled one, and nothing in validate_site.py or check_pages.py notices.

That is the defect class this catches. It was found by walking the pager
chain of M02 and M09 by hand, where one stale card title was echoed into
the rail as well, so a single edit produced two visible wrong titles.

A pager label is allowed to be a faithful ABBREVIATION of the destination's
h1, because the control is narrow and shortening is an editorial choice the
hub already makes widely. It is not allowed to be a different title, which
is almost always a superseded one left behind by a rewrite.

Usage:
    python3 scripts/check_titles.py [<first> <last>]

With no arguments it checks every lesson in math-for-ml-course. With two
four-digit numbers it checks that range, which is how a module owner checks
only their own block.

Exits non-zero if any defect is found, so it can gate a pull request.
"""


root = pathlib.Path("/Users/sauravtrivedi/.treehouse/course-hub-965b61/9/course-hub/math-for-ml-course")
def clean(x): return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x))).strip()
def norm(s): return re.sub(r"[^a-z0-9 ]", "", s.lower())
LO, HI = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) == 3 else (0, 9999)


def mine(n):
    try:
        v = int(n[:4])
    except ValueError:
        return False
    return LO <= v <= HI

h1 = {}
for f in sorted((root / "lessons").glob("*.html")):
    m = re.search(r"<h1>(.*?)</h1>", f.read_text(), re.S)
    if m: h1[f.name] = clean(m.group(1))

idx = (root / "index.html").read_text()
cards = {m.group(1): clean(m.group(2)) for m in
         re.finditer(r'<a class="lcard" href="lessons/([^"]+)".*?<div class="lt">(.*?)</div>', idx, re.S)}

rail = {}
for m in re.finditer(r'"title"\s*:\s*"((?:[^"\\]|\\.)*)"\s*,\s*"href"\s*:\s*"lessons/([^"]+)"', (root/"outline.js").read_text()):
    rail[m.group(2)] = m.group(1).encode().decode("unicode_escape")

pagers = {}
for f in sorted((root / "lessons").glob("*.html")):
    for m in re.finditer(r'<a[^>]*href="([^"]+\.html)"[^>]*>\s*<span class="dir">[^<]*</span><span class="ttl">(.*?)</span>', f.read_text(), re.S):
        pagers.setdefault(m.group(1).split("/")[-1], []).append((f.name, clean(m.group(2))))

defects, ok_abbrev = [], []
for name in sorted(n for n in h1 if mine(n)):
    t = h1[name]
    if name in cards and cards[name] != t:
        defects.append(("CARD", name, cards[name], t))
    if name in rail and rail[name] != t:
        defects.append(("RAIL", name, rail[name], t))
    for src, got in pagers.get(name, []):
        if got in ("Course map", t): continue
        if norm(t).startswith(norm(got)):      # a faithful abbreviation
            ok_abbrev.append((src, name, got))
        else:
            defects.append((f"PAGER in {src}", name, got, t))

print(f"lessons scanned: {sum(1 for n in h1 if mine(n))} (range {LO:04d}-{HI:04d})")
print(f"card entries {len(cards)}, rail entries {len(rail)}, pager links to my pages {sum(len(pagers.get(n,[])) for n in h1 if mine(n))}")
print(f"\nfaithful abbreviations (left alone): {len(ok_abbrev)}")
for s, n, g in ok_abbrev: print(f"   {s} -> {n}: \"{g}\"")
print(f"\nDEFECTS: {len(defects)}")
for kind, name, got, want in defects:
    print(f"  {kind}\n     on   : {name}\n     shows: {got}\n     h1   : {want}")

raise SystemExit(1 if defects else 0)
