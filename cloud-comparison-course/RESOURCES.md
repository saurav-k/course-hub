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
  that same round. Each cloud was inventoried, audited twice independently, then
  reconciled onto the shared vocabulary:
  - AWS: verified 2026-08-26, 183 service rows, 35 declared absences
  - Azure: verified 2026-08-26, 157 service rows, 52 declared absences
  - Google Cloud: verified 2026-08-26, 178 service rows, 36 declared absences
  - OCI: verified 2026-08-26, 136 service rows, 67 declared absences
- Every one of the 764 cells resolves: 574 carry at least one service, 190 carry
  a declared absence with its reason, and none is unfilled.

## Refreshing the matrix

`matrix.js` is generated from those inventories, not hand-written. Correct a fact
in the inventory it came from and regenerate the file; a cell patched in place is
lost at the next refresh. Re-record the read dates above in the same pass, and run
`python3 scripts/validate_site.py --vendor-links` so a link that rotted since the
last round fails the pull request rather than the reader.

## Gaps

- 63 of the 190 declared absences say in their own reason that the cloud does have
  a peer capability which this snapshot did not inventory as its own row. The
  widget still labels them "no equivalent", which reads as stronger than the
  reason states. Resolving that needs a decision about the cell states, not a data
  edit, so it is recorded here rather than patched.
- Every documentation URL in `matrix.js` carries the read date of its cloud's
  inventory above. No URL has a read date of its own.
