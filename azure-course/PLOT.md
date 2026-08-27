# PLOT - Inside Azure

The reading order below is the true order. The course map (`index.html`) and this
file are two views of one sequence and have to agree; when they disagree one of them
is wrong and it gets fixed before anything new is added.

## Written, in order

**Module 01 - The lay of the land**

| Lesson | Title |
| 0100 | One door: Azure Resource Manager |
| 0101 | The four-scope ladder |
| 0102 | Regions, zones and the redundancy ladder |
| 0103 | The platform map |

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
- **Reference: glossary of Azure terms**, linked from every lesson foot once the
  first lessons exist. Not written yet.

No module opens for writing until its topics are covered by verified research.
