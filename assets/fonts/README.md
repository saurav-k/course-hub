# Fonts

Three open-licence variable faces, self-hosted so typography is identical on every
machine, works with the page opened straight from disk, and no third party ever sees
a reader. `hub.css` declares them at the top of the file; the `src` URLs resolve
relative to the stylesheet, so one declaration serves every page depth.

| file | family | `wght` axis in the file | subset | size |
|---|---|---|---|---|
| `inter-latin.woff2` | Inter | 400-900 | latin | 37.0K |
| `inter-latin-ext.woff2` | Inter | 400-900 | latin-ext | 61.4K |
| `source-serif-4-latin.woff2` | Source Serif 4 | 400-900, `opsz` 8-60 | latin | 85.2K |
| `source-serif-4-latin-ext.woff2` | Source Serif 4 | 400-900, `opsz` 8-60 | latin-ext | 69.7K |
| `source-serif-4-latin-italic.woff2` | Source Serif 4 italic | 400-900, `opsz` 8-60 | latin | 88.3K |
| `source-serif-4-latin-ext-italic.woff2` | Source Serif 4 italic | 400-900, `opsz` 8-60 | latin-ext | 75.8K |
| `jetbrains-mono-latin.woff2` | JetBrains Mono | 400-800 | latin | 30.6K |
| `jetbrains-mono-latin-ext.woff2` | JetBrains Mono | 400-800 | latin-ext | 11.3K |

Each `-ext` subset is gated by `unicode-range`, so an English page never downloads it.

Every one of the eight is reached by at least one page, so none is dead weight. Counted
across the 796 published pages, by where a character that needs the cut actually sits:

| cut | pages that reach it |
|---|---|
| serif latin, sans latin | 796, every page |
| mono latin | 608, the pages carrying `<code>` or `<pre>` |
| serif italic latin | 559, the pages carrying `<em>` or `<i>` |
| serif latin-ext, sans latin-ext | 34 |
| mono latin-ext | 5 |
| serif italic latin-ext | 2 |

The last three rows are the point of `unicode-range` rather than an argument against the
files: those pages fetch the cut and the other 762 never ask for it.

## What a reader actually downloads

The eight files are 459.3K on disk and no page fetches more than four of them.

| page | faces fetched | bytes |
|---|---|---|
| hub landing, a course map, a lesson with no italic | serif latin, sans latin, mono latin | **152.8K** |
| a lesson with `<em>` in its prose, which is 559 of the 796 pages | the three above plus serif latin italic | **241.0K** |

That is the budget. `scripts/validate_site.py` holds it: it fails when the eight
files together exceed the ceiling written into the check, so a new face is added
against a known number rather than against a guess. See "the font contract" there.

## Licences

All three families are SIL Open Font License 1.1. The full text and the copyright
notice for each ships beside the binaries, which is what the licence requires:

- `LICENSE-Inter.txt`
- `LICENSE-SourceSerif4.txt`
- `LICENSE-JetBrainsMono.txt`

## Where these came from

The subsets are the ones the Google Fonts CSS API serves for `latin` and
`latin-ext`. The `unicode-range` values in `hub.css` are that API's, unchanged.
To refresh them, request the stylesheet with a browser user agent and download the
`woff2` each `@font-face` names:

```
https://fonts.googleapis.com/css2?family=Inter:wght@400..800&family=JetBrains+Mono:wght@400..600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..600&display=swap
```

Match each block to the one in `hub.css` by family, `font-style` and
`unicode-range`, then run the second step below and replace the file of that name.

### The second step: cut the weights below 400

Google serves the whole `wght` axis. Inter's runs from 100 and Source Serif 4's from
200, and the hub asks for nothing under 400, so a quarter to a third of every one of
those six files is design space no page can reach. Removing the part of the axis
below the default costs nothing that can be seen and is worth 165.6K:

```
python3 -m fontTools varLib.instancer -o inter-latin.woff2             <downloaded> wght=400:900
python3 -m fontTools varLib.instancer -o inter-latin-ext.woff2         <downloaded> wght=400:900
python3 -m fontTools varLib.instancer -o source-serif-4-latin.woff2    <downloaded> wght=400:900
...and the same for the three other Source Serif 4 files.
```

Three things about that command are load-bearing.

**Only the lower bound moves.** Cutting the top of the axis as well, to
`wght=400:700`, is 2K smaller per file and is *not* lossless: re-parameterising the
variation data rounds every coordinate again, and the measured result was a 1 font
unit shift on 153 glyphs and a Mermaid label that wrapped one word differently.
Cutting only below the default leaves the remaining design space untouched, and the
measurement says so: advance widths are bit-identical at every weight the hub uses,
`hhea`, `OS/2` and `head` are unchanged, and no glyph outline moves by more than
half a font unit, which is a hundredth of a pixel at the body size.

**The upper bound stays at the file's own maximum**, not at the `font-weight` range
the `@font-face` declares. The declaration is what the browser clamps to, so the
extra design space above 700 is never selected; carrying it is what keeps the cut
lossless.

**JetBrains Mono is not cut.** Its axis already starts at 400, so the same command
saves 0.4K across both files and would rewrite two binaries for nothing.

`fonttools` is needed for this refresh and for nothing else, and the files committed
today were cut with 4.63.0. The hub ships no build step: the woff2 files are committed,
and a clone renders without installing anything.

Whatever version you use, check the result rather than trusting it. Instantiate the old
file and the new one at every weight the `@font-face` declares, and at several `opsz`
values for Source Serif 4, then compare `hmtx` advances and the `hhea`, `OS/2` and
`head` metrics. Advances must be bit-identical and the metrics unchanged; that is what
makes the cut invisible, and it is the check that caught `wght=400:700`.
