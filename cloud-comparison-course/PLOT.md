# PLOT - Comparing the Four Clouds

The reading order below is the true order. The course map (`index.html`) and this
file are two views of one sequence and have to agree; when they disagree one of them
is wrong and it gets fixed before anything new is added.

## Written, in order

Nothing is written yet. The course map currently carries the capability matrix -
which is the course's opening artefact, not a lesson - and the planned modules
below as roadmap entries.

## Planned, in order

The comparison lessons follow the taxonomy's own arc. Each module takes a band of
capability areas and compares all four clouds row by row; each lesson inside it
takes one comparison that names alone do not settle.

| # | Module | Draws its rows from |
|---|---|---|
| 01 | How to read a four-way comparison | the whole matrix - method before findings |
| 02 | Compute: placement, scaling, containers | `compute-iaas`, `compute-scaling`, `containers`, `serverless-app` |
| 03 | Storage and data | `storage`, `databases` |
| 04 | Analytics | `analytics` |
| 05 | Networking, delivery and edge | `networking-core`, `networking-lb-edge`, `dns-domains`, `hybrid-connectivity` |
| 06 | Identity and access | `identity-workforce`, `identity-workload`, `identity-customer`, `secrets-keys` |
| 07 | Governance, tenancy and telemetry | `org-tenancy`, `governance-policy`, `observability`, `audit-telemetry` |
| 08 | Delivery, integration and intelligence | `iac-deployment`, `integration-messaging`, `ai-ml` |
| 09 | Resilience and migration | `resilience-migration` |

## Why this order and no other

Module 01 teaches the reader how to read the matrix before any finding asks them to.
Modules 02-05 walk outward from the workload core (compute and storage) through the
plumbing (network) in the same order a first architecture meets them. Identity comes
before governance because tenancy guardrails are expressed in identity terms on all
four clouds. Delivery and integration come late because they act on everything
earlier. Resilience closes because it is the property the whole design is judged on.

## Reserved, unwritten

- **The nine modules above**, none yet started. New numbers go at the end of the
  sequence; nothing already published is renumbered or renamed.
- **Reference: the capability taxonomy explained.** A glossary of what each of the
  twenty-four areas covers, linked from every lesson foot. Not written yet.

No module above may open for writing until its rows in `matrix.js` are filled from
verified research. An empty column never becomes prose.
