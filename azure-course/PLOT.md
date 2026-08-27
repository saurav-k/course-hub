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

**Module 02 - Compute**

| Lesson | Title |
| 0200 | The virtual machine |
| 0201 | Who else is on the host |
| 0202 | Images and the gallery |
| 0203 | Holding a fleet at a size |

**Module 03 - Containers and serverless**

| Lesson | Title |
| 0300 | Azure Kubernetes Service |
| 0301 | What AKS adds around the cluster |
| 0302 | Serverless containers and the registry |
| 0303 | Azure Functions |
| 0304 | App Service and Static Web Apps |

**Module 04 - Storage**

| Lesson | Title |
| 0400 | The storage account and Blob Storage |
| 0401 | Tiers, lifecycle and archive |
| 0402 | Managed disks and Elastic SAN |
| 0403 | Shared file systems and bulk transfer |

**Module 05 - Databases**

| Lesson | Title |
| 0500 | The relational shapes |
| 0501 | Buying relational capacity |
| 0502 | Cosmos DB: the request unit and the partition key |
| 0503 | The specialised stores |

**Module 06 - Analytics**

| Lesson | Title |
| 0600 | The analytics fork |
| 0601 | The lake and the engines that read it |
| 0602 | Pipelines and the runtime that reaches your data |
| 0603 | Streams and the units that carry them |
| 0604 | Who reads the result |

**Module 07 - Networking and delivery**

| Lesson | Title |
| 0700 | The virtual network is an address plan |
| 0701 | Rules and routes |
| 0702 | Joining networks |
| 0703 | Private endpoints and the DNS behind them |
| 0704 | The edge |
| 0705 | Paths in from outside |

**Module 08 - Identity and access**

| Lesson | Title |
| 0800 | One tenant, three populations |
| 0801 | How a request is authorised |
| 0802 | What is demanded at sign-in |
| 0803 | Machine identity without secrets |
| 0804 | Keys, secrets and certificates |

**Module 09 - Governance, tenancy and cost**

| Lesson | Title |
| 0900 | Policy is the guardrail engine |
| 0901 | Policy as code and the effect ramp |
| 0902 | Landing zones and subscription vending |
| 0903 | Knowing what you have |
| 0904 | Paying for it |

**Module 10 - Observability and audit**

| Lesson | Title |
| 1000 | Three planes and one routing primitive |
| 1001 | What is on by default |
| 1002 | What keeping it costs |
| 1003 | Instrumenting what the platform cannot see |
| 1004 | Alerts, health and the blind spots |

**Module 11 - Security services**

| Lesson | Title |
| 1100 | Two managed firewalls at two layers |
| 1101 | Boundaries and access without a path |
| 1102 | Knowing how exposed you are |
| 1103 | Detection and response |

**Module 12 - Delivery and integration**

| Lesson | Title |
| 1200 | Four ways to describe infrastructure |
| 1201 | A deployment is an object |
| 1202 | Shipping change |
| 1203 | Messages, events and the three that get confused |
| 1204 | APIs, workflows and what is not a product |

## Planned, in order

Modules 13 and 14 remain unwritten. The full fourteen-module plan is below, unchanged.

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

- **Modules 13 and 14**, neither started. New numbers go at the end of the
  sequence; nothing already published is renumbered or renamed.
- **Reference: glossary of Azure terms**, linked from every lesson foot once it
  exists. Not written yet, so no lesson links it and no lesson spine carries a
  Glossary entry.

No module opens for writing until its topics are covered by verified research.
