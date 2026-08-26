# PLOT - Comparing the Four Clouds

The reading order below is the true order. The course map (`index.html`) and this
file are two views of one sequence and have to agree; when they disagree one of them
is wrong and it gets fixed before anything new is added.

## Written, in order

The course map opens with the capability matrix - the course's opening artefact,
not a lesson - then every module that has been written, in module order, then the
roadmap of what remains.

**Module 02, Compute: placement, scaling, containers.** Four lessons, `0200` to
`0203`, one per capability area: `compute-iaas`, `compute-scaling`, `containers`,
`serverless-app`.

**Module 05, Networking, delivery and edge.** Four lessons, one per capability area.

| Lesson | Name | Capability area |
|---|---|---|
| `0500` | The private network | `networking-core` |
| `0501` | Load balancing and the edge | `networking-lb-edge` |
| `0502` | DNS and domains | `dns-domains` |
| `0503` | Hybrid connectivity | `hybrid-connectivity` |

**Module 06, Identity and access.** Four lessons, one per capability area.

| Lesson | Name | Capability area |
|---|---|---|
| `0600` | Workforce identity: where a grant attaches | `identity-workforce` |
| `0601` | Machine identity: proving it without a secret | `identity-workload` |
| `0602` | Customer identity: the directory you build on | `identity-customer` |
| `0603` | Secrets, keys and certificates: who holds custody | `secrets-keys` |

**Module 07, Governance, tenancy and telemetry.** Four lessons, `0700` to `0703`,
one per capability area: `org-tenancy`, `governance-policy`, `observability`,
`audit-telemetry`.

**Module 08, Security, delivery, integration and intelligence.** Four lessons, one
per capability area.

| Lesson | Name | Capability area |
|---|---|---|
| `0800` | The security services layer | `security-services` |
| `0801` | Infrastructure as code and deployment | `iac-deployment` |
| `0802` | Integration and messaging | `integration-messaging` |
| `0803` | AI and ML services | `ai-ml` |

`security-services` had no module in the original table.
It was placed here rather than in module 07 because a security service acts on a
running workload the way delivery and integration do, while module 07 governs the
estate around it, and the module name was widened to say so.

**Numbering is by module block, and this file's module table is what assigns it.**
A module owns the hundred its own number opens: module 02 owns `0200` to `0299`,
module 05 owns `0500` to `0599`, module 06 owns `0600` to `0699`, module 07 owns
`0700` to `0799`, and module 08 owns `0800` to `0899`. Modules are written in
parallel, so a single
running sequence collides the moment two contributors add a lesson at once. The
eyebrow, the card `.ln` and the footer carry the four digits unchanged. Module
grouping on the map carries teaching order, and file order is free to disagree
with it.

## Planned, in order

The comparison lessons follow the taxonomy's own arc. Each module takes a band of
capability areas and compares all four clouds row by row; each lesson inside it
takes one comparison that names alone do not settle.

| # | Module | Draws its rows from |
|---|---|---|
| 01 | How to read a four-way comparison | the whole matrix - method before findings |
| 03 | Storage and data | `storage`, `databases` |
| 04 | Analytics | `analytics` |
| 09 | Resilience and migration | `resilience-migration` |

## Why this order and no other

Module 01 teaches the reader how to read the matrix before any finding asks them to.
Modules 02-05 walk outward from the workload core (compute and storage) through the
plumbing (network) in the same order a first architecture meets them. Identity comes
before governance because tenancy guardrails are expressed in identity terms on all
four clouds. Security, delivery and integration come late because they act on everything
earlier. Resilience closes because it is the property the whole design is judged on.

## Reserved, unwritten

- **The four unwritten modules above**, none yet started. Each takes the hundred
  its module number opens, so nothing already published is renumbered or renamed.
- **Reference: the capability taxonomy explained.** A glossary of what each of the
  twenty-four areas covers, linked from every lesson foot. Not written yet.

No module above may open for writing until its rows in `matrix.js` are filled from
verified research. An empty column never becomes prose.
