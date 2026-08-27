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

**Module 03 - Containers and serverless**

| # | Lesson | Capability |
|---|---|---|
| 0300 | How much of the GKE cluster you run | `managed-kubernetes`, `kubernetes-node-autoscaler` |
| 0301 | Beyond one cluster | `kubernetes-fleet-management`, `service-mesh`, `kubernetes-backup` |
| 0302 | Cloud Run, a container with a URL | `serverless-containers`, `container-orchestrator-nonk8s` |
| 0303 | Functions and app runtimes | `functions-faas`, `paas-web-runtime`, `static-site-hosting` |
| 0304 | Choosing a runtime | runtime placement across the five |

**Module 04 - Storage**

| # | Lesson | Capability |
|---|---|---|
| 0400 | Cloud Storage and the bucket | `object-storage`, `object-storage-highperf` |
| 0401 | Classes, lifecycle and archive | `archive-storage` |
| 0402 | Block storage on Compute Engine | `block-storage` |
| 0403 | Shared filesystems | `file-storage` |
| 0404 | Where the storage menu stops | `hybrid-storage-gateway`, `object-storage-tables`, `bulk-transfer-appliance`, `online-transfer` |

**Module 05 - Databases**

| # | Lesson | Capability |
|---|---|---|
| 0500 | The managed relational tier | `relational-managed`, `relational-serverless` |
| 0501 | Spanner, and the rows it quietly fills | `globally-distributed-sql`, `graph-database`, `ledger` |
| 0502 | Bigtable and Firestore | `nosql-keyvalue`, `nosql-document`, `timeseries-database` |
| 0503 | Memorystore and the cache tier | `in-memory-cache` |
| 0504 | Moving a database in | `db-migration-service`, `change-data-capture`, `database-fleet-management` |

**Module 06 - Analytics**

| # | Lesson | Capability |
|---|---|---|
| 0600 | BigQuery, the warehouse and the query engine | `data-warehouse`, `serverless-query-engine` |
| 0601 | BigLake and the lakehouse | `data-lake` |
| 0602 | Dataflow and the streaming row | `etl-service`, `stream-analytics`, `stream-ingest` |
| 0603 | A recurring Spark job is two decisions | `managed-spark`, `workflow-orchestration` |
| 0604 | Governing and reading the data | `data-catalog`, `clean-rooms`, `bi-dashboards` |

`managed-search` belongs to the analytics domain in the shared taxonomy, and this course
teaches it in module 13 beside the agent platform and the retrieval pipeline it now ships
with. `workflow-orchestration` carries two products: Cloud Composer is taught here as the
data-pipeline orchestrator, and Workflows in module 12 as the lighter service orchestrator.

**Module 07 - Networking and delivery**

Six lessons rather than the usual four or five: this module carries four capability
domains - core networking, load balancing and edge, DNS, and hybrid connectivity - and
splitting them further would have produced pages with two ideas each.

| # | Lesson | Capability |
|---|---|---|
| 0700 | Subnets and the address plan | `virtual-network`, `subnet`, `network-interface`, `ip-address-management` |
| 0701 | Routing, egress and the firewall | `route-table`, `bgp-dynamic-routing`, `nat-gateway`, `stateful-packet-filter` |
| 0702 | Three private paths to a managed service | `private-google-access`, `private-services-access`, `private-endpoint` |
| 0703 | Joining networks | `network-peering`, `shared-vpc`, `transit-hub`, `network-manager` |
| 0704 | Reaching the ground | `site-to-site-vpn`, `dedicated-interconnect`, `partner-interconnect`, `cross-cloud-interconnect`, `sdwan-integration`, `on-prem-extension`, `vmware-stack-hosting`, `client-vpn`, `metro-edge-locations` |
| 0705 | The edge, and one anycast front door | `l7-load-balancer`, `l4-load-balancer`, `global-front-door`, `cdn`, `media-cdn`, `ddos-protection`, `authoritative-dns`, `private-dns`, `dns-routing-policies`, `domain-registrar`, `gateway-load-balancer` |

**Module 08 - Identity and access**

| # | Lesson | Capability |
|---|---|---|
| 0800 | The IAM evaluation chain | `iam-principals`, `iam-roles`, `iam-policy-language` |
| 0801 | Boundaries and privileged access | `permission-boundary`, `privileged-access` |
| 0802 | Machine identity without keys | `workload-identity`, `workload-identity-federation`, `cross-account-assumption`, `short-lived-credentials`, `agent-identity` |
| 0803 | Two kinds of human, two directories | `workforce-directory`, `workforce-sso`, `managed-directory`, `os-login`, `ciam-user-directory`, `ciam-social-federation`, `ciam-mfa` |
| 0804 | Keys, secrets and certificates | `key-management`, `hsm`, `byok-hyok`, `secrets-store`, `certificate-manager`, `certificate-authority` |

`conditional-access` and `identity-provider-audit-log` are named in lesson 0803 as
capabilities delivered elsewhere, and taught in modules 11 and 10 respectively.

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

- **Modules 09 to 14 above**, none started. Each module owns its own hundred of the
  `MMxx` sequence, so a later contributor takes the next free number inside its module
  rather than appending to the end of the course; nothing already published is
  renumbered or renamed.
- **Reference: glossary of GCP terms**, linked from every lesson foot once the
  first lessons exist. Not written yet.

No module opens for writing until its topics are covered by verified research.
