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
  sources. Lessons are written only from it. All fourteen modules are written against
  this one snapshot, so a refresh chases the snapshot rather than the pages.
- Counts that move - regions, Availability Zones, edge locations, Kubernetes versions in
  support - are stated as they read at the snapshot and always carry the vendor page as
  the live authority.

## Gaps

Topics deliberately left unwritten, or named without being explained, because the
verified inventory does not cover them at the depth a lesson needs:

- **EC2 placement group strategies in detail.** The inventory records that cluster,
  partition and spread strategies exist and that Dedicated Hosts cannot be used inside
  a placement group, but not the per-strategy restrictions. Lesson 0202 teaches the
  three strategies by name and points at the vendor page for the detail.
- **EC2 billing granularity.** The inventory records per-second billing with a
  sixty-second minimum in a service row's notes, but names no specific vendor page
  as the source for it, so no lesson states it.
- **List prices anywhere.** Cost *shape* is taught and prices are linked, per
  `MISSION.md`.
- **Bedrock inference tiers.** The inventory names Standard, Flex, Priority and
  Reserved but does not characterise them, so lesson 1300 names the four and
  explains only the three purchase modes it can source.
- **Per-rule web ACL capacity costs.** The inventory records the 1,500 included and
  5,000 maximum capacity units and not what any individual rule or managed rule
  group consumes, so lesson 1100 teaches the budget and points at the vendor page
  for the per-rule arithmetic.
- **What each AWS support plan contains.** Three lessons record capabilities gated
  behind a Business or higher plan - the DDoS response team, the Health API and the
  full Trusted Advisor check set - and the inventory does not describe the plans
  themselves, so no page states what a plan includes.
- **Definitions of the Control Tower guidance categories.** Lesson 0902 uses
  mandatory, strongly recommended and elective as the vendor's own labels without
  explaining how a control is assigned to one.

## How a lesson cites

The inventory holds two kinds of source and lessons use both the same way:
`references.md` names the page a specific detail was read from, and each
`services.json` row's `doc_url` is the vendor page for that service. A lesson
links whichever of the two actually carries the claim, and never a page the
inventory does not record as fetched.
