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

**Module 09 - Governance, tenancy and cost**

| # | Lesson | Capability |
|---|---|---|
| 0900 | The landing zone | `landing-zone`, `service-catalog`, `cross-account-resource-sharing` |
| 0901 | Labels, tags and quotas | `resource-tagging`, `resource-tags-governance`, `quota-management` |
| 0902 | Seeing and proving the estate | `resource-graph-query`, `policy-as-code`, `config-drift-assessment`, `compliance-pack` |
| 0903 | The bill, and where its detail lives | `cost-management` |
| 0904 | Paying less on purpose | `commitment-discounts`, `cost-advisory` |

`org-hierarchy` and `org-guardrail-policy` belong to this module's subject and were taught
in lessons 0101 and 0102, so module 09 builds on them rather than repeating them. Security
Command Center appears here on its compliance and drift face, and in module 11 on its
threat and posture face - one product, two audiences.

**Module 10 - Observability and audit**

| # | Lesson | Capability |
|---|---|---|
| 1000 | Where a log lands and how long it stays | `log-store`, `telemetry-export-pipeline`, `log-analytics`, `error-reporting` |
| 1001 | The four audit streams | `control-plane-audit-log`, `data-plane-access-log`, `policy-denied-audit-log`, `access-transparency-logs` |
| 1002 | The streams that are off until you turn them on | `network-flow-log`, `firewall-rules-log`, `nat-logs`, `load-balancer-access-log`, `dns-query-log`, `service-specific-log` |
| 1003 | Metrics, agents and three retention schedules | `metrics-store`, `managed-prometheus`, `telemetry-agent` |
| 1004 | Traces, profiles and being told | `alerting`, `dashboards`, `synthetic-monitoring`, `distributed-tracing`, `profiler`, `network-diagnostics`, `service-health-dashboard` |

`telemetry-export-pipeline` sits in the integration-messaging domain of the shared
taxonomy and is taught here, because the Log Router cannot be separated from the log
store it decides storage for. `identity-provider-audit-log` is a recorded absence named
in lesson 0803 and reaching Cloud Logging as Admin Activity records.

**Module 11 - Security services**

| # | Lesson | Capability |
|---|---|---|
| 1100 | The perimeter and the proxy | `service-perimeter`, `zero-trust-app-access`, `bastion`, `conditional-access` |
| 1101 | Stopping a request at the edge and in the fabric | `waf`, `recaptcha-enterprise`, `cloud-firewall`, `packet-mirroring` |
| 1102 | Threat detection and posture | `threat-detection`, `posture-management`, `security-investigation-graph` |
| 1103 | Scanning what you build, classifying what you hold | `vulnerability-scanning`, `data-classification`, `ai-safety-guardrails`, `verified-permissions` |

Four lessons rather than five: the standard firewall tier is taught in lesson 0701 where a
packet is followed, and `zero-trust-routing` is stated there as the same absence, so this
module carries only what those pages left.

**Module 12 - Delivery and integration**

| # | Lesson | Capability |
|---|---|---|
| 1200 | Infrastructure as code here | `native-iac-template`, `terraform-provider`, `iac-in-code-sdk`, `kubernetes-config-management` |
| 1201 | The pipeline, and the gate in it | `cicd-pipeline`, `progressive-delivery` |
| 1202 | Four shapes of message | `pub-sub`, `message-queue`, `event-bus`, `realtime-messaging`, `mqtt-broker` |
| 1203 | Orchestration and scheduling | `workflow-orchestration`, `scheduler-jobs`, `managed-integration` |
| 1204 | APIs at the front | `api-gateway`, `api-management-enterprise`, `graphql-api` |

`config-management` is taught in lesson 0301 as the fleet's reconciliation loop and is
pointed at from lesson 1200 rather than repeated. `artifact-registry` is taught in module
03, and Binary Authorization has no key of its own in the shared taxonomy and is taught in
lesson 1201 as the admission gate the pipeline hangs on.

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

- **Modules 13 and 14 above**, none started. Each module owns its own hundred of the
  `MMxx` sequence, so a later contributor takes the next free number inside its module
  rather than appending to the end of the course; nothing already published is
  renumbered or renamed.
- **Reference: glossary of GCP terms**, linked from every lesson foot once the
  first lessons exist. Not written yet.

No module opens for writing until its topics are covered by verified research.
