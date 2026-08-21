# Fonts

Three open-licence variable faces, self-hosted so typography is identical on every
machine, works with the page opened straight from disk, and no third party ever sees
a reader. `hub.css` declares them at the top of the file; the `src` URLs resolve
relative to the stylesheet, so one declaration serves every page depth.

| file | family | axis | subset |
|---|---|---|---|
| `inter-latin.woff2` | Inter | `wght` 100-900 | latin |
| `inter-latin-ext.woff2` | Inter | `wght` 100-900 | latin-ext |
| `source-serif-4-latin.woff2` | Source Serif 4 | `wght` 200-900, `opsz` 8-60 | latin |
| `source-serif-4-latin-ext.woff2` | Source Serif 4 | `wght` 200-900, `opsz` 8-60 | latin-ext |
| `source-serif-4-latin-italic.woff2` | Source Serif 4 italic | `wght` 200-900, `opsz` 8-60 | latin |
| `source-serif-4-latin-ext-italic.woff2` | Source Serif 4 italic | `wght` 200-900, `opsz` 8-60 | latin-ext |
| `jetbrains-mono-latin.woff2` | JetBrains Mono | `wght` 400-800 | latin |
| `jetbrains-mono-latin-ext.woff2` | JetBrains Mono | `wght` 400-800 | latin-ext |

Each `-ext` subset is gated by `unicode-range`, so an English page never downloads it.

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
`unicode-range`, then replace the file of that name. Nothing else changes.
