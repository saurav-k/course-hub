# RESOURCES - Inside AWS

The sources this course keeps returning to, and the provenance discipline that keeps
a future refresh cheap. This file is the one place in the course where dates belong.

## Canon

- **Amazon Web Services documentation** - <https://docs.aws.amazon.com/>. The vendor's own reference for every
  user-facing behaviour this course describes.

Every technical claim in a lesson links a page under this root, fetched and read
while writing that lesson. Anything third-party is labelled as such at the point of
use.

## Provenance discipline

The course records what it rests on with the date it was read, so a refresh chases
only what changed:

- Verified per-cloud inventory for AWS: complete, snapshot 2026-08-26. Every vendor
  page cited by a lesson was fetched and read on that date by the research pass that
  produced the inventory, and each claim traces to a specific page rather than to a
  summary of one. The inventory survived an independent audit, a second audit on a
  different model, a corrections pass and a reconciliation before any lesson was written.
- Scope of that snapshot: 183 service rows across all 24 capability domains, 437 vendor
  sources. Lessons are written only from it.
- Counts that move - regions, Availability Zones, edge locations, Kubernetes versions in
  support - are stated as they read at the snapshot and always carry the vendor page as
  the live authority.

## Gaps

Topics deliberately left unwritten because the verified inventory does not cover them
at the depth a lesson needs:

- **EC2 placement group strategies in detail.** The inventory records that cluster,
  partition and spread strategies exist and that Dedicated Hosts cannot be used inside
  a placement group, but not the per-strategy restrictions. Lesson 0202 teaches the
  three strategies by name and points at the vendor page for the detail.
- **List prices anywhere.** Cost *shape* is taught and prices are linked, per
  `MISSION.md`.
