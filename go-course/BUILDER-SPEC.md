# Builder spec - the delta for Systems Engineering in Go

The house standard is `.claude/skills/course-authoring/`.
It carries the page contracts, the widget vocabulary, the teaching bar, and the verification gate, and it governs this course as it governs every other.

This file carries **only what is true of this course and not of the hub**.

## The gold page

`lessons/0100-how-go-talks-to-the-linux-kernel.html`. Read it in full before writing.
It is the page every other page in this course is matched against, so a divergence from it is a decision to defend, not an accident to leave in.

## What this course does differently

- **Code authenticity:** Code blocks must use real signatures, structs, and patterns from the 17 open-source repositories, citing package and commit/file path.
- **Orientation figure:** The opening figure (`.fig-cap`: `Where this sits`) must clearly depict the component's place within the host OS or distributed cluster before deep-diving into the Go package.
- **Accents:** Uses `--course-hue: -160` (defined in `assets/hub.css`), providing a clean, vibrant cyan-azure identity fitting Go's systems legacy.

## The lesson map

The map lives in `index.html`, and only there.

## Cross-linking

- Link to `backend-engineering-course` when discussing high-level HTTP/gRPC API contracts.
- Link to `production-systems-course` when referencing multi-scale failure domains.
