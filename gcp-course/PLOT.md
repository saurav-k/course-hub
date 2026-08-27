# PLOT - Inside Google Cloud

The reading order below is the true order. The course map (`index.html`) and this
file are two views of one sequence and have to agree; when they disagree one of them
is wrong and it gets fixed before anything new is added.

## Written, in order

Lesson numbers are `MMxx`: the two-digit module number, then a two-digit sequence inside
that module. Module 01 owns 0100 to 0199, module 02 owns 0200 to 0299, and so on.
Modules are written in parallel by different contributors, so a single running sequence
would collide the moment two of them add a lesson. Nothing already published is
renumbered.

**Module 01 - The lay of the land**

| # | Lesson | Capability |
|---|---|---|
| 0100 | Regions, zones and the scope of a resource | `region-az-model` |
| 0101 | The resource hierarchy and the project | `org-hierarchy` |
| 0102 | What flows down the tree | `org-guardrail-policy` |
| 0103 | The platform map and the names that moved | platform map |

**Module 02 - Compute**

| # | Lesson | Capability |
|---|---|---|
| 0200 | The machine you shape yourself | `vm-instances` |
| 0201 | Images, families and templates | `vm-images`, `instance-template` |
| 0202 | Five levers on the same machine | `gpu-compute`, `dedicated-hosts`, `confidential-compute`, `bare-metal`, `spot-capacity` |
| 0203 | Managed instance groups and Batch | `autoscaling-group`, `batch-compute` |

## Planned, in order

Fourteen modules, following the platform the way a first architecture meets it:
where it runs, what it runs on, then data, plumbing, who may act, how it is governed
and watched, how change ships, and finally how it survives failure.

| # | Module | Covers |
| 01 | The lay of the land | regions and availability, the account hierarchy, and the platform map |
| 02 | Compute | virtual machines, images, placement and scaling |
| 03 | Containers and serverless | Kubernetes, serverless containers, functions and app runtimes |
| 04 | Storage | object, block, file and archive tiers |
| 05 | Databases | relational, NoSQL, in-memory and specialised stores |
| 06 | Analytics | warehouse, lakehouse, pipelines and streaming |
| 07 | Networking and delivery | virtual networks, load balancing, DNS, CDN and hybrid connectivity |
| 08 | Identity and access | workforce identity, machine identity, customer identity, keys and secrets |
| 09 | Governance, tenancy and cost | organisation policy, landing zones, quotas and cost control |
| 10 | Observability and audit | metrics, logs, traces, and every telemetry stream the platform emits |
| 11 | Security services | edge protection, threat detection and posture management |
| 12 | Delivery and integration | infrastructure as code, pipelines, queues, events and APIs |
| 13 | AI and ML | managed model APIs, training platforms and vector storage |
| 14 | Resilience and migration | backup, disaster recovery, replication and moving workloads in |

## Why this order and no other

Modules 01-03 build the words everything else needs (hierarchy, compute, runtime).
04-07 are the substrate a workload stands on: storage, databases, analytics, then
the network that connects them. Identity comes before governance because guardrails
are expressed through identity on every cloud. Observability and security follow
governance because both hang off its structures. Delivery and integration come late
because they act on everything earlier, and resilience closes because it is judged
against all of it.

## Reserved, unwritten

- **The fourteen modules above**, none started. New numbers go at the end of the
  sequence; nothing already published is renumbered or renamed.
- **Reference: glossary of GCP terms**, linked from every lesson foot once the
  first lessons exist. Not written yet.

No module opens for writing until its topics are covered by verified research.
