# RESOURCES - Inside OCI

The sources this course keeps returning to, and the provenance discipline that keeps
a future refresh cheap. This file is the one place in the course where dates belong.

## Canon

- **Oracle Cloud Infrastructure documentation** - <https://docs.oracle.com/en-us/iaas/>. The vendor's own reference for every
  user-facing behaviour this course describes.

Every technical claim in a lesson links a page under this root, and anything third-party
is labelled as such at the point of use.

## Provenance discipline

Lessons are written only from the **verified per-cloud inventory for OCI**, and never
from an author's own recollection or from a web search made while drafting. That
inventory is a research artefact held outside this repository: a service list, a
deep-dive report and a reference file, each entry naming the Oracle page it was read
from and the date it was read.

- Verified OCI inventory, snapshot read **2026-08-26**. Scope: the full capability
  taxonomy plus deep-dive sections on tenancy and access, telemetry streams,
  machine-to-machine authentication, infrastructure as code and deployment,
  networking, and the certification blueprints. It carries its own corrections
  record, so a claim this course makes can be traced back to the vendor page and
  the round that confirmed it.
- Where the inventory records a fact as unresolved, the lesson says so rather than
  choosing a side. The compartment limit is the live example: two Oracle pages
  disagree and lesson 0102 prints both.

## Sources cited, by module

### Module 01 - The lay of the land

- [Regions and Availability Domains](https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm) - the nesting rule, three fault domains per availability domain, realm isolation, subscribed-region limits, availability-domain name randomisation.
- [Public cloud regions and data centers](https://www.oracle.com/cloud/public-cloud-regions/) - the marketed commercial region and country counts.
- [Services available in all cloud regions](https://www.oracle.com/cloud/distributed-cloud/service-availability/) - the sovereign and government region lists.
- [Oracle US Government Cloud](https://docs.oracle.com/en-us/iaas/Content/gov-cloud/govfedramp.htm) - the OC2 realm regions.
- [Sovereign Cloud](https://www.oracle.com/cloud/sovereign-cloud/) - Dedicated Region and Alloy positioning.
- [Compute Cloud@Customer](https://docs.oracle.com/en-us/iaas/compute-cloud-at-customer/home.htm) and [Roving Edge Infrastructure](https://docs.oracle.com/en-us/iaas/roving-edge-infrastructure/rvr/home.htm) - the same control plane off the public grid.
- [Managing Compartments](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingcompartments.htm) - six levels, global scope, empty-to-delete, ninety-day recovery.
- [Organization Management](https://docs.oracle.com/en-us/iaas/Content/General/organization/organization_management_overview.htm) - parent and child tenancies, shared subscription, cross-tenancy cost reporting.
- [Service Limits](https://docs.oracle.com/en-us/iaas/Content/General/Concepts/servicelimits.htm) - compartment, policy-object and policy-statement limits, including the hard per-hierarchy limit.
- [Policy Syntax](https://docs.oracle.com/en-us/iaas/Content/Identity/Concepts/policysyntax.htm) - the statement shape and the verb ladder.
- [Service Change Announcements](https://docs.oracle.com/en-us/iaas/Content/servicechanges.htm) - the authority on which service names are current.
- [Bastion](https://docs.oracle.com/en-us/iaas/Content/Bastion/Concepts/bastionoverview.htm) and [Object Storage behind API Gateway](https://docs.oracle.com/en/learn/oci-api-gateway-web-hosting/index.html) - the documented substitutes named on the platform-map page.
- [OCI Architect Professional exam page](https://mylearn.oracle.com/ou/exam/oracle-cloud-infrastructure-architect-professional-1z0-997-26/163295/161770/271322) and the [Architect Associate course](https://mylearn.oracle.com/ou/course/oracle-cloud-infrastructure-architect-associate-2026/161028) - what the certifications weight, stated as weighting and never as a schedule.

### Module 02 - Compute

- [Compute Shapes](https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm) - flexible shape families, the memory ratio, the per-family bandwidth ceilings, the network-card rule, and the bare metal series.
- [Supported compute shapes](https://docs.oracle.com/en-us/iaas/Content/data-science/using/supported-shapes.htm) - the statement that an OCPU is a physical core with multithreading, about two x86 virtual processors.
- [Burstable instances](https://docs.oracle.com/en-us/iaas/Content/Compute/References/burstable-instances.htm) - baseline-OCPU billing.
- [GPU compute](https://www.oracle.com/cloud/compute/gpu/) - virtual machine GPU shapes against bare metal superclusters.
- [Dedicated Virtual Machine Hosts](https://docs.oracle.com/en-us/iaas/Content/Compute/Concepts/dedicatedvmhosts.htm) - per-host billing, launching onto a named host, and the live-migration, autoscaling and pool exclusions.
- [Confidential computing](https://docs.oracle.com/en-us/iaas/Content/Compute/References/confidential_compute.htm) - memory encryption as a shape property, with per-instance keys held in the AMD secure processor.
- [Images](https://docs.oracle.com/en-us/iaas/Content/Compute/References/images.htm) - platform and custom images, import and export, and how a custom image is stored.
- [Instance management](https://docs.oracle.com/en-us/iaas/Content/Compute/Concepts/instancemanagement.htm) - what an instance configuration saves.
- [Autoscaling instance pools](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/autoscalinginstancepools.htm) - metric and schedule triggers, the fifty-policy limit, and the pool types supported.
- [Preemptible instances](https://docs.oracle.com/en-us/iaas/Content/Compute/Concepts/preemptible.htm) - the two-minute preemption event and the full exclusion list.
- [Preemptible capacity for Kubernetes worker nodes](https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contengusingpreemptiblecapacity.htm) - cordon and drain before reclaim.
- [Capacity reservations](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/reserve-capacity.htm) - holding capacity before launch.

### Module 03 - Containers and serverless

- [Enhanced and basic clusters](https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contengcomparingenhancedwithbasicclusters_topic.htm) - the feature matrix, the console and API defaults, the one-way upgrade and its precondition, and the agreement against the objective.
- [Granting workloads access to OCI resources](https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contenggrantingworkloadaccesstoresources.htm) - workload identity scoped to a Kubernetes service account.
- [Preemptible capacity for worker nodes](https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contengusingpreemptiblecapacity.htm) - cordon and drain before reclaim.
- [Container Instances](https://docs.oracle.com/en-us/iaas/Content/container-instances/home.htm) - serverless containers, per-second billing, the sixty-container cap and Vault-backed pull credentials.
- [OCI Batch](https://docs.oracle.com/en-us/iaas/Content/oci-batch/home.htm) - managed batch orchestration that provisions compute and tears it down.
- [Container Registry overview](https://docs.oracle.com/en-us/iaas/Content/Registry/Concepts/registryoverview.htm) - registry specification compliance, Helm and multi-architecture support, private access by service gateway, and the regional defaults.
- [Artifact Registry](https://docs.oracle.com/en-us/iaas/Content/artifacts/home.htm) - the store for everything that is not a container.
- [Vulnerability Scanning service](https://www.oracle.com/security/cloud-security/vulnerability-scanning-service/) - image scanning on push, alongside host scans. Vendor product page rather than documentation.
- [Service gateway](https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/servicegateway.htm) - one per virtual cloud network, same region only, mutually exclusive service labels.
- [Overview of Functions](https://docs.oracle.com/en-us/iaas/Content/Functions/Concepts/functionsoverview.htm) - the Fn Project base, the supported languages and the resource-principal model.
- [Changing default memory and timeout settings](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionscustomizing.htm) - the six-rung memory ladder, the synchronous default and maximum, and the detached range.
- [Exporting function log files](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsexportingfunctionlogfiles.htm) - invocation logging is off until enabled per application.
- [Visual Builder](https://docs.oracle.com/en-us/iaas/visual-builder/index.html) - the low-code application hosting row.
- [Static site hosting behind API Gateway](https://docs.oracle.com/en/learn/oci-api-gateway-web-hosting/index.html) - the documented composition for a bucket with a custom domain.
- [Service Mesh](https://docs.oracle.com/en-us/iaas/Content/service-mesh/overview.htm) - the end-of-life notice naming open-source Istio as the replacement.

### Module 04 - Storage

- [Understanding Object Storage tiers](https://docs.oracle.com/en-us/iaas/Content/Object/Concepts/understandingstoragetiers.htm) - the tier table, the minimum retention on Infrequent Access and Archive, the retrieval fee, auto-tiering behaviour, the durability claim and the immutable bucket default tier.
- [Overview of Archive Storage](https://docs.oracle.com/en-us/iaas/Content/Archive/Concepts/archivestorageoverview.htm) - restore before read, and first byte in about an hour.
- [Object Storage auto tiering](https://blogs.oracle.com/cloud-infrastructure/post/introducing-object-storage-auto-tiering) - the one-mebibyte threshold and the no-cost move. Vendor blog rather than documentation.
- [Block Volume performance](https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/blockvolumeperformance.htm) - the performance-unit ladder, the named tiers and the operations-per-second ceiling.
- [Changing the performance of an existing volume](https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/update-performance-block-bv-volume.htm) - the unit values and how auto-tune is enabled.
- [Dynamic performance scaling](https://blogs.oracle.com/cloud-infrastructure/post/announcing-dynamic-performance-scaling-with-oci-block-volume-autotuning) - the fast-up, slow-down asymmetry and the detached-volume behaviour. Vendor blog rather than documentation.
- [File Storage](https://docs.oracle.com/en-us/iaas/Content/File/home.htm) - NFS versions, elastic capacity, snapshots, clones, cross-region replication, and the mount target and export objects.
- [Using replication](https://docs.oracle.com/en-us/iaas/Content/Object/Tasks/usingreplication.htm) - bucket replication policies.
- [Scheduling volume backups](https://docs.oracle.com/en-us/iaas/Content/Block/Tasks/schedulingvolumebackups.htm) - backup policies, cross-region copies, volume groups and restore semantics.
- [Data Transfer Appliance](https://blogs.oracle.com/cloud-infrastructure/post/introducing-oracle-cloud-infrastructure-data-transfer-appliance) - the 150 TB appliance, free shipping, the NFS dataset mount and the tamper-evident seals. Vendor blog rather than documentation.
- [Service Change Announcements](https://docs.oracle.com/en-us/iaas/Content/servicechanges.htm) - the deprecation of the older File Storage encryption-key policy shape.

### Module 05 - Databases

- [Oracle Cloud Infrastructure Database Service](https://docs.oracle.com/en-us/iaas/Content/Database/home.htm) - the customer-managed rung: Base Database and Exadata Database Service, VM and bare metal DB systems, Exadata Cloud@Customer, Data Guard and Real Application Clusters.
- [Autonomous AI Database billing summary](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/autonomous-database-billing-overview.html) - the four workload types, the ECPU model, and the shared against dedicated deployment split.
- [Use auto scaling](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/autonomous-auto-scale.html) - compute autoscaling on by default at three times the provisioned ECPU count, storage autoscaling off by default.
- [Security and authentication in Autonomous Database](https://docs.oracle.com/en/cloud/paas/autonomous-database/serverless/adbsb/gs-security-and-authentation-autonomous-database.html) - database clients authenticating with IAM tokens instead of passwords.
- [MySQL HeatWave](https://docs.oracle.com/en-us/iaas/mysql-database/home.htm) - managed MySQL Enterprise Edition with the in-memory accelerator, transactions and analytics without an extract step, read replicas and a standby.
- [OCI Database with PostgreSQL](https://docs.oracle.com/en-us/iaas/Content/postgresql/home.htm) - managed community PostgreSQL with a pluggable engine and monitor.
- [OCI Cache](https://docs.oracle.com/en-us/iaas/Content/ocicache/home.htm) - Valkey and Redis version 7 compatible clusters, sharded and non-sharded topologies.
- [OCI Cache product page](https://www.oracle.com/cloud/cache/) - the two gigabyte to five hundred gigabyte range, the five-node ceiling, the Valkey 8.1 engine, the JSON module and vector search. Vendor product page rather than documentation.
- [NoSQL Database Cloud](https://docs.oracle.com/en/cloud/paas/nosql-cloud/) - serverless key-value tables, on-demand and provisioned capacity, global active tables.
- [Globally Distributed Autonomous Database](https://docs.oracle.com/en/cloud/paas/globally-distributed-autonomous-database/user/overview-distributed-adb1.html) - shared-nothing sharding, shards added online with rebalancing, and data residency as the headline case.
- [Property graphs in Autonomous Database](https://docs.oracle.com/en/cloud/paas/autonomous-database/serverless/adbsb/graph-autonomous-database.html) - Graph Studio, PGQL and notebooks inside the database rather than as a separate service.
- [Oracle Blockchain Platform](https://docs.oracle.com/en/cloud/paas/blockchain-cloud/index.html) - the managed Hyperledger Fabric network for multi-party ledgers.
- [Database Migration](https://docs.oracle.com/en-us/iaas/Content/database-migration/home.htm) - assessment, schema conversion guidance, and the online and offline paths for Oracle and non-Oracle sources.
- [Offline migration](https://docs.oracle.com/en-us/iaas/database-migration/doc/offline-migration.html) - the Data Pump path, against the GoldenGate path used online.
- [OCI GoldenGate](https://docs.oracle.com/en/cloud/paas/goldengate-service/index.html) - managed real-time change data capture across heterogeneous databases and into big-data targets.
- [Database Management](https://docs.oracle.com/en-us/iaas/database-management/home.htm) - the fleet console covering Autonomous, Base, Exadata and external databases through a management agent.
- [Service Change Announcements](https://docs.oracle.com/en-us/iaas/Content/servicechanges.htm) - the end of life of the Classic GoldenGate Cloud Service, which shares a name with the current one.

### Module 06 - Analytics

- [Autonomous AI Database billing summary](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/autonomous-database-billing-overview.html) - the Lakehouse workload type, and external tables querying Object Storage in place.
- [Data platform lakehouse reference architecture](https://docs.oracle.com/en/solutions/data-platform-lakehouse/index.html) - open table formats on Object Storage read by the Autonomous Lakehouse, by Data Flow Spark, or by external engines.
- [Data Catalog](https://docs.oracle.com/en-us/iaas/Content/data-catalog/home.htm) - technical, business and operational metadata, and the Hive metastore interface Spark engines use.
- [Streaming](https://docs.oracle.com/en-us/iaas/Content/Streaming/Concepts/streamingoverview.htm) - the serverless Kafka-compatible event log, partitions, the seven-day replay window and IAM-authenticated Kafka access.
- [Streaming with Apache Kafka](https://docs.oracle.com/en-us/iaas/Content/kafka/overview.htm) - managed Kafka clusters, full Kafka API compatibility, no partition ceiling, the availability commitment, and the comparison table between the two services.
- [Data Flow](https://www.oracle.com/big-data/data-flow/) - serverless Spark and Spark Streaming, per-second execution billing, the acceleration option, and Data Catalog as its metastore. Vendor product page rather than documentation.
- [Big Data Service](https://docs.oracle.com/en-us/iaas/Content/bigdata/home.htm) - persistent Hadoop, Spark, Trino and Flink clusters with Kerberos security and autoscaling.
- [Data Integration](https://docs.oracle.com/en-us/iaas/Content/data-integration/home.htm) - the serverless visual designer, schema drift protection, pushdown into Oracle targets, and the Data Flow, Data Science and Container Instance task types.
- [Oracle Integration 3](https://docs.oracle.com/en-us/iaas/application-integration/) - the process automation substitute named where a general workflow orchestrator is expected.
- [Search with OpenSearch](https://docs.oracle.com/en-us/iaas/Content/search-opensearch/home.htm) - managed OpenSearch clusters, OpenSearch Dashboards, vector search, searchable snapshots and alerting into Notifications.
- [Oracle Analytics Cloud](https://docs.oracle.com/en/cloud/paas/analytics-cloud/index.html) - semantic models, dashboards, self-service visualisation and natural-language questions, connected natively to the Autonomous Lakehouse.
- [Dashboards service](https://docs.oracle.com/en-us/iaas/Content/Dashboards/home.htm) - console-native widgets for metrics, logs and custom HTML, recorded as distinct from the business intelligence product.

### Module 07 - Networking and delivery

- [VCNs and subnets](https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/VCNs.htm) - the regional network, its address ranges, IPv6, and the regional against availability-domain subnet shapes.
- [Security rules](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/securityrules.htm) - security lists at the subnet, network security groups at the network card, the stateful and stateless choice per rule, and a group named as a source.
- [Route tables](https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/managingroutetables.htm) - the rule targets, including a private address for appliance insertion.
- [NAT gateway](https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/NATgateway.htm) - outbound-only access, the twenty thousand concurrent connections per destination address and port, and the restriction on peered and on-premises networks.
- [Service gateway](https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/servicegateway.htm) - one per network, same region only, and the mutually exclusive scope labels.
- [Local VCN peering](https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/localVCNpeering.htm) - one gateway per peer and the non-overlapping address requirement.
- [Dynamic Routing Gateway](https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/managingDRGs.htm) - the regional hub, its attachment types and the route table per attachment.
- [Transit routing](https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/transitrouting.htm) - hub and spoke scenarios and firewall insertion on the path.
- [Site-to-Site VPN](https://www.oracle.com/cloud/networking/site-to-site-vpn/) - two tunnels per connection, termination on the routing gateway, and no hourly or per-byte fee. Vendor product page rather than documentation.
- [FastConnect overview](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/fastconnectoverview.htm) - the cross-connect port sizes, partner virtual circuits, port-hour billing and link-layer encryption.
- [Oracle Interconnect for Azure](https://docs.oracle.com/en-us/iaas/Content/multicloud/interconnect-azure.htm) - the paired-region requirement and the pairing with the other provider's own circuit.
- [Network Load Balancer](https://docs.oracle.com/en-us/iaas/Content/NetworkLoadBalancer/home.htm) - layer-four passthrough, client address preservation, and availability across fault domains.
- [Flexible Load Balancer](https://docs.oracle.com/en-us/iaas/Content/Balance/home.htm) - the proxy, certificate offload, path routing, the bandwidth range and the firewall attachment point.
- [Traffic Management overview](https://docs.oracle.com/en-us/iaas/Content/TrafficManagement/Concepts/overview.htm) - DNS steering only, public zones only, and the pairing with Health Checks.
- [Traffic Management steering policies](https://docs.oracle.com/en-us/iaas/Content/TrafficManagement/Concepts/trafficmanagementapi.htm) - the six policy kinds and the filter, health, ordering and limit pipeline.
- [OCI DNS](https://docs.oracle.com/en-us/iaas/Content/DNS/home.htm) - anycast authoritative service for public zones, DNSSEC, and delegation rather than registration.
- [Private DNS](https://docs.oracle.com/en-us/iaas/Content/DNS/Tasks/privatedns.htm) - private zones, custom resolvers, listeners and forwarders to on-premises name servers.
- [DDoS protection on the OCI edge](https://docs.oracle.com/en/solutions/learn-ddos-prevention-oci/understand-ddos-layers-and-oracle-ddos-protection1.html) - always-on volumetric protection for public endpoints at no charge.

## Gaps

Topics deliberately left unwritten because the verified inventory does not cover
them, rather than because they are unimportant:

- Latency figures for any path into or inside OCI. Oracle publishes no service-level
  number the inventory could verify, so pages teach relative positioning instead.
- Prices, including certification prices. The inventory records that no price appears
  on the official exam pages, so no page here states one.
- Contractual event-to-visibility delays for the telemetry streams. Operational
  observations exist in the inventory; no published commitment does.
