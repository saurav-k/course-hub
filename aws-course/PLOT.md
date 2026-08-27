# PLOT - Inside AWS

The reading order below is the true order. The course map (`index.html`) and this
file are two views of one sequence and have to agree; when they disagree one of them
is wrong and it gets fixed before anything new is added.

## Written, in order

### Module 01 - The lay of the land

| Lesson | Title | Rung |
| 0100 | Regions, zones and the edge | foundation |
| 0101 | The account is the boundary | foundation |
| 0102 | The platform map | foundation |
| 0103 | Names that mislead | foundation |

### Module 02 - Compute

| Lesson | Title | Rung |
| 0200 | The instance and the catalogue | working |
| 0201 | The image and the template | working |
| 0202 | Where the instance lands | working |
| 0203 | Holding a fleet at a size | working |
| 0204 | Buying the same machine for less | working |

### Module 03 - Containers and serverless

| Lesson | Title | Rung |
| 0300 | Two orchestrators, one platform | working |
| 0301 | Fargate is a capacity mode | working |
| 0302 | The registry that feeds them | working |
| 0303 | Lambda and the function boundary | working |
| 0304 | Above the container | working |

### Module 04 - Storage

| Lesson | Title | Rung |
| 0400 | The object store and its classes | working |
| 0401 | The bucket types | working |
| 0402 | Block storage, bound to a zone | working |
| 0403 | Shared file systems | working |
| 0404 | Cold data and getting data in | working |

### Module 05 - Databases

| Lesson | Title | Rung |
| 0500 | Two storage designs under one API | working |
| 0501 | Capacity with no instance class | working |
| 0502 | DynamoDB and the partition | working |
| 0503 | Two in-memory services | working |
| 0504 | The purpose-built stores | working |

### Module 06 - Analytics

| Lesson | Title | Rung |
| 0600 | The lake is three layers | working |
| 0601 | Three ways to read the lake | working |
| 0602 | The warehouse beside the lake | working |
| 0603 | Two ways to run a Spark job | working |
| 0604 | Ingest, deliver, process | working |

### Module 07 - Networking and delivery

| Lesson | Title | Rung |
| 0700 | The interface, the address and the route | working |
| 0701 | Two filters that both must pass | working |
| 0702 | Egress and private access | working |
| 0703 | From peering to a hub | working |
| 0704 | The front door | working |

### Module 08 - Identity and access

| Lesson | Title | Rung |
| 0800 | The gates an access decision passes | working |
| 0801 | Machines carry no passwords | working |
| 0802 | Trusting an identity from outside | working |
| 0803 | Neither your staff nor your customers | working |
| 0804 | Keys, secrets and certificates | working |

## Planned, in order

Fourteen modules, following the platform the way a first architecture meets it:
where it runs, what it runs on, then data, plumbing, who may act, how it is governed
and watched, how change ships, and finally how it survives failure.

Lesson numbers are `MMxx`: the two-digit module number, then a two-digit sequence
inside it. Module 01 is `0100` upward, Module 02 is `0200` upward, and so on. Lesson
numbers are public URLs, so nothing published is ever renumbered.

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

- **Modules 09 to 14 above**, none started. New numbers go at the end of the
  sequence; nothing already published is renumbered or renamed.
- **Reference: glossary of AWS terms**, linked from every lesson foot once the
  first lessons exist. Not written yet.

No module opens for writing until its topics are covered by verified research.
