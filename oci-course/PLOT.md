# PLOT - Inside OCI

The reading order below is the true order. The course map (`index.html`) and this
file are two views of one sequence and have to agree; when they disagree one of them
is wrong and it gets fixed before anything new is added.

## How a lesson is numbered, permanently

`lessons/MMxx-*.html`, where `MM` is the module number in the table below and `xx`
is that module's own two-digit sequence. Module 01 owns 0100 to 0199, module 02
owns 0200 to 0299, and so on. Modules are written by different contributors at
different times, so one running sequence across the whole course would collide the
moment two of them add a lesson. The eyebrow, the card `.ln` and the footer carry
the four-digit number unchanged: dropping the padding would render 0200 as
"Lesson 200". Nothing already published is renumbered.

## Written, in order

**Module 01 - The lay of the land**

| Lesson | Title |
| 0100 | Regions, availability domains and fault domains |
| 0101 | Realms, subscriptions and where OCI runs |
| 0102 | The tenancy, the compartment and the organization above them |
| 0103 | The platform map, and the names that mislead |

**Module 02 - Compute**

| Lesson | Title |
| 0200 | The shape is a dial, and it moves more than you think |
| 0201 | Placement, host tenancy and what maintenance does |
| 0202 | From one instance to a fleet |
| 0203 | Capacity you can be asked to give back |

**Module 03 - Containers and serverless**

| Lesson | Title |
| 0300 | OKE: the cluster kind you pick once |
| 0301 | Containers that live only as long as the work |
| 0302 | Container Registry: where every runtime gets its image |
| 0303 | Functions: the two timeouts that decide the design |
| 0304 | Where OCI sells a pattern instead of a runtime |

**Module 04 - Storage**

| Lesson | Title |
| 0400 | Four shapes of storage, and the choice a bucket cannot take back |
| 0401 | Object Storage tiers and the auto-tiering rule |
| 0402 | Block Volume: performance is bought by the gigabyte |
| 0403 | File Storage: the mount target is the thing with a location |
| 0404 | Moving bytes in, out and duplicated |

**Module 05 - Databases**

| Lesson | Title |
| 0500 | The database ladder, and where the managed line falls |
| 0501 | Autonomous Database and the two autoscale switches |
| 0502 | The open-source engines, and the cache that came back |
| 0503 | When one relational database is the wrong shape |
| 0504 | Getting data in, keeping it in sync, and seeing the fleet |

**Module 06 - Analytics**

| Lesson | Title |
| 0600 | The lakehouse is a workload type, not a separate product |
| 0601 | Two Kafka products, and the line between them |
| 0602 | Two ways to run Spark, and where stream analytics lives |
| 0603 | The managed pipeline layer, and what it orchestrates |
| 0604 | Reading the answers back, and the two kinds of dashboard |

**Module 07 - Networking and delivery**

| Lesson | Title |
| 0700 | The VCN, the subnet, and the two places a rule lives |
| 0701 | Six gateways, and what a route table may point at |
| 0702 | The routing gateway is the hub, and peering is the spoke |
| 0703 | Two load balancers, and the front door that is not a proxy |
| 0704 | DNS at the edge and inside the network |

**Module 08 - Identity and access**

| Lesson | Title |
| 0800 | Who acts: identity domains, groups, and the missing role |
| 0801 | The policy language, and the deny that is a one-way door |
| 0802 | How a machine proves who it is |
| 0803 | Crossing a boundary without assuming a role |
| 0804 | Keys, secrets and certificates |

**Module 09 - Governance, tenancy and cost**

| Lesson | Title |
| 0900 | Four guardrails, and which of them actually blocks |
| 0901 | The landing zone is a framework, and how you check what exists |
| 0902 | Tagging is the cost model |
| 0903 | Seeing and shaping the bill |

**Module 10 - Observability and audit**

| Lesson | Title |
| 1000 | Three log families, one store, and the one that is always on |
| 1001 | Metrics, the query language, and the alarm that resets |
| 1002 | Every stream, and what each one silently misses |
| 1003 | Traces, synthetics and the agent |
| 1004 | Getting telemetry out, and where it can go |

**Module 11 - Security services**

| Lesson | Title |
| 1100 | Two firewalls at two layers, and where each one attaches |
| 1101 | A fourth check on every packet |
| 1102 | Finding what is wrong: posture, vulnerabilities and intelligence |
| 1103 | Reaching a private host, and copying the traffic |

**Module 12 - Delivery and integration**

| Lesson | Title |
| 1200 | Terraform is the native language, and the stack is where it runs |
| 1201 | The pipeline, and the two progressive strategies |
| 1202 | Five messaging services, and how to tell them apart |
| 1203 | The gateway in front, and the integration platform beside it |
| 1204 | Keeping the fleet configured after it is deployed |

**Module 13 - AI and ML**

| Lesson | Title |
| 1300 | The managed model API, and the capacity behind it |
| 1301 | The vector store is a database you already have |
| 1302 | Agents, knowledge bases and the conversation layer |
| 1303 | Training your own, and the ladder of pretrained services |

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
- **Reference: glossary of OCI terms**, linked from every lesson foot once the
  first lessons exist. Not written yet.

No module opens for writing until its topics are covered by verified research.
