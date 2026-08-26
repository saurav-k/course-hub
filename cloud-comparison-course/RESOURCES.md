# RESOURCES - Comparing the Four Clouds

The sources this course keeps returning to, and the provenance discipline that
keeps a future refresh cheap. This file is the one place in the course where dates
belong.

## Canon

- **Amazon Web Services documentation** - <https://docs.aws.amazon.com/>
- **Microsoft Azure documentation** - <https://learn.microsoft.com/en-us/azure/>
- **Google Cloud documentation** - <https://cloud.google.com/docs>
- **Oracle Cloud Infrastructure documentation** - <https://docs.oracle.com/en-us/iaas/>

Every filled cell in `matrix.js` links into the vendor's own docs for its cloud.
Every comparison claim in a lesson links a page under one of these four roots.

## Provenance discipline

Each course in this category records what it rests on with the date it was read,
so a refresh chases only what changed. For this course:

- The capability taxonomy (24 areas, 191 keys) is fixed by the shared research
  spec, v1, reconciled from the four verified inventories in the snapshot round
  dated 2026-08-26. The taxonomy lives committed in `matrix.js`; this note
  records where it came from. The 126-key starter list it replaced was the frame
  slice's placeholder and is gone.
- The service cells were filled from the four verified per-cloud inventories of
  that same round. Each cloud was inventoried, audited twice independently,
  reconciled onto the shared vocabulary, then repaired: a later pass found 67
  entries filed as absences that were real products, promoted them to rows with
  vendor links, and replaced three dead OCI documentation links.
  - AWS: verified 2026-08-26, 198 service rows, 20 declared gaps
  - Azure: verified 2026-08-26, 184 service rows, 25 declared gaps
  - Google Cloud: verified 2026-08-26, 187 service rows, 27 declared gaps
  - OCI: verified 2026-08-26, 152 service rows, 51 declared gaps
- Every one of the 764 cells resolves, and none is unfilled: 641 carry at least
  one service, 721 services in all; 21 say the cloud has the capability inside a
  service listed on another row, and link that row; 102 are genuine absences,
  each with the reason the audit recorded.
- Which 21 of the 123 gaps are cross-references rather than absences is not read
  out of their prose - five of them name no row at all, and five gaps that do
  name one are genuine absences pointing at the nearest neighbour. The list is
  the one the data repair pass enumerated, which rests in turn on the
  reconciliation's finding that thirteen capabilities are sold as a product by
  exactly one of the four clouds and built into a larger service on the rest.

## Refreshing the matrix

`matrix.js` is generated from those inventories, not hand-written. Correct a fact
in the inventory it came from and regenerate the file; a cell patched in place is
lost at the next refresh. Re-record the read dates above in the same pass, and run
`python3 scripts/validate_site.py --vendor-links` so a link that rotted since the
last round fails the pull request rather than the reader.

## Module 07 - governance, tenancy and telemetry

The four lessons of this module rest on the same verified round as the matrix
(2026-08-26) and cite the vendor pages that round recorded. Every vendor link on
the four pages was checked to resolve on 2026-08-26.

Two kinds of link on these pages sit outside the four documentation roots above,
and both are the source the verified round itself used:

- **Certification blueprints.** Domain names and weights are quoted from the
  verified round's exam sections, which read the vendors' own guides: the AWS
  Solutions Architect Professional guide, the Azure architect skills-measured
  page, the Google Cloud professional architect certification page, and Oracle's
  MyLearn exam-topics page. Oracle publishes its blueprint on
  `mylearn.oracle.com` rather than under `docs.oracle.com`, so that is the link
  the page carries.
- **The OCI landing zone**, which Oracle publishes as a Terraform repository on
  GitHub rather than as a documentation page. `matrix.js` links the same place.

Exam blueprints rot faster than anything else in this course: a vendor may
re-cut its domains without renaming the exam. Re-read those four pages on every
refresh, and treat a weight with no matching sentence on the vendor page as
stale rather than as a typo.

### Gaps found while writing this module

- **Google Cloud folder nesting depth.** The verified round flagged its own
  figure as not re-read against the current Resource Manager quota, so lesson 70
  states the other three depths and says plainly that this one is left out.
- **OCI Monitoring metric retention.** No retention figure for the OCI metric
  store appears in the verified round, so the retention figure on lesson 72
  carries three clouds and marks the fourth as not recorded rather than
  guessing it.

## Gaps

- One row is a content question the research directory has raised and not
  settled: OCI's `bulk-transfer-appliance` links a blog post that no longer
  answers, and Oracle appears to have folded the offline Data Transfer Appliance
  into Roving Edge. Repointing the link would point it at a different product, so
  the row stands as the audit left it until the service itself is re-read.
- OCI's `online-transfer` absence gives Storage Gateway as one of the ways to
  copy data online, and Storage Gateway is retired. The absence it declares is
  still correct; only that detail is stale.
- Every documentation URL in `matrix.js` carries the read date of its cloud's
  inventory above. No URL has a read date of its own.
