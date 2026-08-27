# RESOURCES - Inside Azure

The sources this course keeps returning to, and the provenance discipline that keeps
a future refresh cheap. This file is the one place in the course where dates belong.

## Canon

- **Microsoft Azure documentation** - <https://learn.microsoft.com/en-us/azure/>. The vendor's own reference for every
  user-facing behaviour this course describes.

Every technical claim in a lesson links a page under this root, fetched and read
while writing that lesson. Anything third-party is labelled as such at the point of
use.

## Provenance discipline

The course records what it rests on with the date it was read, so a refresh chases
only what changed:

- **Verified per-cloud inventory for Azure: complete.** Snapshot date **2026-08-26**.
  Scope: 184 service rows across 24 capability domains, 25 recorded absences, and a
  deep-dive report covering tenancy, telemetry, machine-to-machine authentication,
  deployment, networking and certification structure.
  The inventory passed original research, two independent audits on different models,
  a corrections pass, a reconciliation against the shared capability taxonomy, and a
  repair pass. Every claim in it traces to a vendor page fetched and read during that
  work, and the corrections are recorded case by case with the page that confirmed each.
- **Modules 01 to 04 were written only from that inventory.** No claim on any lesson
  page originates anywhere else. Where the inventory did not cover something a lesson
  wanted to say, the lesson does not say it, and the omission is listed under `## Gaps`
  below rather than filled from memory.

## The pages the written lessons rest on

Every link below is cited from at least one lesson page, and every one of them is a
page the verified inventory records as fetched and read.

**Module 01 - The lay of the land**

- <https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview>
- <https://learn.microsoft.com/en-us/azure/governance/management-groups/overview>
- <https://learn.microsoft.com/en-us/azure/governance/policy/overview>
- <https://learn.microsoft.com/en-us/azure/role-based-access-control/overview>
- <https://learn.microsoft.com/en-us/azure/role-based-access-control/deny-assignments>
- <https://learn.microsoft.com/en-us/azure/role-based-access-control/role-definitions>
- <https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources>
- <https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits>
- <https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview>
- <https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deployment-stacks>
- <https://learn.microsoft.com/en-us/azure/governance/resource-graph/overview>
- <https://learn.microsoft.com/en-us/azure/governance/blueprints/overview>
- <https://learn.microsoft.com/en-us/azure/governance/machine-configuration/>
- <https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview>
- <https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy>
- <https://learn.microsoft.com/en-us/azure/service-health/overview>
- <https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/activity-log>
- <https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-workspace-overview>
- <https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview>
- <https://learn.microsoft.com/en-us/entra/fundamentals/whatis>
- <https://learn.microsoft.com/en-us/azure/azure-arc/overview>
- <https://learn.microsoft.com/en-us/azure/data-explorer/>
- <https://learn.microsoft.com/en-us/azure/cosmos-db/>
- <https://learn.microsoft.com/en-us/azure/azure-sql/database/sql-database-paas-overview>
- <https://learn.microsoft.com/en-us/azure/ai-foundry/openai/overview>
- <https://learn.microsoft.com/en-us/azure/redis/>
- <https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-overview>
- <https://learn.microsoft.com/en-us/fabric/data-warehouse/>
- <https://learn.microsoft.com/en-us/azure/frontdoor/front-door-overview>
- <https://learn.microsoft.com/en-us/azure/network-watcher/vnet-flow-logs-overview>
- <https://learn.microsoft.com/en-us/azure/mysql/>
- <https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-overview>
- <https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-overview>
- <https://learn.microsoft.com/en-us/azure/dms/>
- <https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview>
- <https://learn.microsoft.com/en-us/azure/key-vault/general/overview>

**Module 02 - Compute**

- <https://learn.microsoft.com/en-us/azure/virtual-machines/>
- <https://learn.microsoft.com/en-us/azure/virtual-machines/sizes-gpu>
- <https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types>
- <https://learn.microsoft.com/en-us/azure/virtual-machines/dedicated-hosts>
- <https://learn.microsoft.com/en-us/azure/virtual-machines/spot-vms>
- <https://learn.microsoft.com/en-us/azure/virtual-machines/shared-image-galleries>
- <https://learn.microsoft.com/en-us/azure/virtual-machines/workloads/sap/get-started>
- <https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/>
- <https://learn.microsoft.com/en-us/azure/confidential-computing/>
- <https://learn.microsoft.com/en-us/azure/batch/>
- <https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-network-interface>
- <https://learn.microsoft.com/en-us/azure/virtual-network/network-security-group-how-it-works>
- <https://learn.microsoft.com/en-us/azure/bastion/bastion-overview>
- <https://learn.microsoft.com/en-us/entra/identity/devices/howto-vm-sign-in-azure-ad-linux>
- <https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview>

**Module 03 - Containers and serverless**

- <https://learn.microsoft.com/en-us/azure/aks/>
- <https://learn.microsoft.com/en-us/azure/aks/monitor-aks>
- <https://learn.microsoft.com/en-us/azure/aks/istio-about>
- <https://learn.microsoft.com/en-us/azure/aks/csi-secrets-store-driver>
- <https://learn.microsoft.com/en-us/azure/kubernetes-fleet/overview>
- <https://learn.microsoft.com/en-us/azure/backup/azure-kubernetes-service-backup-overview>
- <https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation>
- <https://learn.microsoft.com/en-us/azure/azure-monitor/metrics/prometheus-metrics-overview>
- <https://learn.microsoft.com/en-us/azure/azure-monitor/vm/vminsights-overview>
- <https://learn.microsoft.com/en-us/azure/container-apps/>
- <https://learn.microsoft.com/en-us/azure/container-instances/>
- <https://learn.microsoft.com/en-us/azure/container-registry/>
- <https://learn.microsoft.com/en-us/azure/azure-functions/>
- <https://learn.microsoft.com/en-us/azure/app-service/>
- <https://learn.microsoft.com/en-us/azure/app-service/deploy-staging-slots>
- <https://learn.microsoft.com/en-us/azure/static-web-apps/>
- <https://learn.microsoft.com/en-us/azure/spring-apps/basic-standard/retirement-announcement>

**Module 04 - Storage**

- <https://learn.microsoft.com/en-us/azure/storage/blobs/>
- <https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview>
- <https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction>
- <https://learn.microsoft.com/en-us/azure/storage/files/>
- <https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-introduction>
- <https://learn.microsoft.com/en-us/azure/storage/elastic-san/>
- <https://learn.microsoft.com/en-us/azure/azure-netapp-files/>
- <https://learn.microsoft.com/en-us/azure/databox/>
- <https://learn.microsoft.com/en-us/azure/storage-mover/service-overview>
- <https://learn.microsoft.com/en-us/azure/backup/backup-introduction-to-azure-backup>
- <https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview>
- <https://learn.microsoft.com/en-us/entra/identity/domain-services/overview>

**Module 05 - Databases**

- <https://learn.microsoft.com/en-us/azure/azure-sql/database/sql-database-paas-overview>
- <https://learn.microsoft.com/en-us/azure/azure-sql/managed-instance/sql-managed-instance-paas-overview>
- <https://learn.microsoft.com/en-us/azure/azure-sql/database/serverless-tier-overview>
- <https://learn.microsoft.com/en-us/azure/postgresql/>
- <https://learn.microsoft.com/en-us/azure/mysql/>
- <https://learn.microsoft.com/en-us/azure/cosmos-db/>
- <https://learn.microsoft.com/en-us/azure/documentdb/overview>
- <https://learn.microsoft.com/en-us/azure/cosmos-db/gremlin/overview>
- <https://learn.microsoft.com/en-us/azure/redis/>
- <https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-overview>
- <https://learn.microsoft.com/en-us/azure/data-explorer/>
- <https://learn.microsoft.com/en-us/azure/confidential-ledger/overview>
- <https://learn.microsoft.com/en-us/fabric/graph/overview>
- <https://learn.microsoft.com/en-us/sql/relational-databases/graphs/sql-graph-overview>
- <https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview>

**Module 06 - Analytics**

- <https://learn.microsoft.com/en-us/fabric/data-warehouse/>
- <https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction>
- <https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/on-demand-workspace-overview>
- <https://learn.microsoft.com/en-us/azure/databricks/>
- <https://learn.microsoft.com/en-us/azure/data-factory/>
- <https://learn.microsoft.com/en-us/azure/event-hubs/>
- <https://learn.microsoft.com/en-us/azure/stream-analytics/>
- <https://learn.microsoft.com/en-us/azure/search/>
- <https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-what-is-desktop>
- <https://learn.microsoft.com/en-us/purview/purview>
- <https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-clean-rooms>

## Gaps

Things a written lesson wanted to say and did not, because the verified inventory
does not carry them. Each is a candidate for the next research pass, and none of
them was filled from memory.

- **How a generalised image differs from a specialised one in preparation.** Lesson
  0202 names the fork and points at the Compute Gallery page rather than restating a
  procedure the inventory does not record.
- **What the letters inside a virtual-machine size name mean beyond the family
  letter.** The inventory records the family letters and the presence of generation
  suffixes such as `Dav5`, and no decoding table. Lesson 0200 says so and links the
  vendor catalogue as the live authority.
- **Per-type performance ceilings for managed disks**, and per-share figures for
  Azure Files. Lesson 0402 teaches which types decouple performance from capacity
  and quotes no numbers, because the inventory quotes none.
- **Whether Flexible scale-set orchestration supports the scheduled and predictive
  autoscale profiles.** The inventory documents those against Uniform mode only, so
  lesson 0203 states exactly that and draws no conclusion about Flexible.
- **How much faster high-priority blob rehydration is.** The inventory records that
  it is faster and billed extra, with the standard figure at up to fifteen hours.
  Lesson 0401 shows the fifteen-hour bar and annotates the faster option without a
  number.
- **Concurrency and quota figures for Container Apps and for Azure Functions hosting
  plans.** Lesson 0303 teaches the plans as capabilities because the inventory
  records capabilities and not limits here.
- **Current availability of Azure Data Box Gateway.** The inventory flags it for
  re-checking, so lesson 0403 teaches the appliance family and does not assert the
  gateway's status.
- **Any figure for what an operation costs in request units, and any sizing table
  for DTU or vCore.** The inventory records these as capacity abstractions and quotes
  no numbers, so lessons 0501 and 0502 teach the mechanism and quote none either.
- **The contents of the MongoDB vCore feature-parity matrix.** The inventory records
  that the matrix exists and should be checked before a migration. Lesson 0502 says
  exactly that and reproduces nothing from it.
- **How Cosmos DB throughput is distributed across physical partitions.** The
  inventory names the partition key as the core design decision without describing
  the division mechanism, so lesson 0502 argues from access patterns rather than from
  a partition-throughput rule.
- **What a columnar file layout lets a query skip.** The inventory records which
  formats the serverless engine reads and that it bills by data processed, and says
  nothing about format internals. Lesson 0601 argues the cost case from those two
  facts and labels the format reasoning as general rather than Azure-specific inside
  the worked solution itself.
- **Named window types in the streaming query language.** The inventory records that
  windowing exists and names no window kinds, so lesson 0603 draws what a window is
  and names none. Its chart says in its own caption that it illustrates the idea
  rather than measuring a workload.
- **Throughput figures for a throughput unit or a processing unit.** The inventory
  records the two purchasing units and no capacities, so lesson 0603 teaches the unit
  model without a number in it.
- **Current naming of the Purview governance experiences.** The inventory records
  that classic portal capabilities are converging into the Unified Catalog and says
  to check the product page, so lesson 0604 names the Unified Catalog and links it.
- **A glossary of Azure terms.** Reserved in `PLOT.md` and not written, so no lesson
  links one and no lesson spine carries a Glossary entry.

## Derived figures

Two charts in these modules are arithmetic done in the course rather than a number
taken from a vendor page, and both say so in their own figcaption:

- Lesson 0201's per-machine share of a dedicated host price, which is one divided by
  the number of machines packed onto the host.
- Lesson 0403's network transfer times for 800 terabytes at three sustained rates,
  with the fully-sustained-link assumption named in the caption and repeated as a
  warning in the prose.
