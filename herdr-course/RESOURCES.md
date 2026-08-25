# RESOURCES - Herdr from Zero

The sources this course keeps returning to. Every claim in a lesson links one of these
or a page of the herdr.dev docs.

## Canon

- **herdr.dev documentation** - <https://herdr.dev/docs/>. The concepts, configuration,
  plugins and marketplace pages are the primary reference for user-facing behaviour.
  Fetched while writing; states quoted verbatim where noted.
- **Herdr repository** - <https://github.com/herdrdev/herdr>, at 0.8.2-era master
  (`Cargo.toml:3` says 0.8.2). Lessons cite it file-and-line, e.g.
  `docs/next/website/src/content/docs/concepts.mdx:65-77`. Line numbers are true of
  that tree; re-verify before updating a claim against a newer one.

## The three investigations behind the pack

The lessons were written from three independent source investigations of the Herdr
repository, each carrying file-and-line citations:

1. **Architecture** - keeper/viewer split, PTY ownership, screen-state detection
   pipeline, snapshots, socket API surface.
2. **Install, config, deploy** - every install path per OS, config keys and defaults,
   update channels, how herdr.dev and the marketplace are served.
3. **Plugin development** - manifest contract, discovery, load path, run lifecycle,
   environment variables, callbacks, linking and marketplace publishing.

## Gaps

- Exact upstream release notes distinguishing 0.8.x patch behaviour were not consulted;
  claims are pinned to "0.8.2-era master" rather than to a release tag's published
  notes. If a reader needs release-level precision, the repository tree is the source.
