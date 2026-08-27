# RESOURCES - Inside Google Cloud

The sources this course keeps returning to, and the provenance discipline that keeps
a future refresh cheap. This file is the one place in the course where dates belong.

## Canon

- **Google Cloud documentation** - <https://cloud.google.com/docs>. The vendor's own reference for every
  user-facing behaviour this course describes.

Three sibling roots are the same vendor and count as canon: <https://firebase.google.com>
for Firebase products, <https://services.google.com> for the certification guides
the vendor publishes as PDFs, and <https://docs.cloud.google.com>, which now serves some
current documentation pages that have no equivalent under the main root. Anything outside those four roots is third-party and is
labelled as such at the point of use.

Every technical claim in a lesson links a page under one of them.

## Provenance discipline

The course records what it rests on with the date it was read, so a refresh chases
only what changed:

- **Verified per-cloud inventory for Google Cloud: complete, snapshot 2026-08-26.**
  It is the sole factual input to every module written so far: a service inventory, a deep-dive
  report and a reference set, produced by original research and then carried through a
  first independent audit, a second audit on a different model, a corrections pass, a
  reconciliation and a repair pass. Every claim in it traces to a vendor page fetched on
  that date, and the corrections pass re-verified each applied change against the vendor
  documentation the same day.
- Lessons cite the vendor page that inventory records for the claim, so every link on a
  page resolves to Google Cloud's own documentation rather than to the inventory.
- Where the inventory itself flagged a statement as unverified, the lesson says so in a
  warning callout instead of repeating it. Those flags are listed under `## Gaps` below.

## Pages the written modules rest on

All fetched 2026-08-26 as part of the verified inventory. Grouped by module.

- **Module 01.** [Regions and zones](https://cloud.google.com/compute/docs/regions-zones),
  [resource hierarchy](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy),
  [Resource Manager limits](https://cloud.google.com/resource-manager/docs/limits),
  [organization policy overview](https://cloud.google.com/resource-manager/docs/organization-policy/overview),
  [hierarchy evaluation](https://cloud.google.com/resource-manager/docs/organization-policy/understanding-hierarchy),
  [IAM overview](https://cloud.google.com/iam/docs/overview),
  [tags overview](https://cloud.google.com/resource-manager/docs/tags/tags-overview),
  [quotas](https://cloud.google.com/docs/quotas/view-manage),
  [product catalogue](https://cloud.google.com/products).
- **Module 02.** [Machine families](https://cloud.google.com/compute/docs/machine-resource),
  [images](https://cloud.google.com/compute/docs/images),
  [instance templates](https://cloud.google.com/compute/docs/instance-templates),
  [instance groups](https://cloud.google.com/compute/docs/instance-groups),
  [GPUs](https://cloud.google.com/compute/docs/gpus/overview),
  [TPUs](https://cloud.google.com/tpu/docs/tpus),
  [sole-tenant nodes](https://cloud.google.com/compute/docs/nodes/sole-tenant-nodes),
  [Confidential VM](https://cloud.google.com/compute/docs/about-confidential-vm),
  [bare metal instances](https://cloud.google.com/compute/docs/instances/bare-metal-instances),
  [Spot VMs](https://cloud.google.com/compute/docs/instances/spot),
  [preemptible VMs](https://cloud.google.com/compute/docs/instances/preemptible),
  [Batch](https://cloud.google.com/batch/docs/get-started),
  [committed use discounts](https://cloud.google.com/docs/cuds).
- **Module 03.** [GKE cluster modes](https://cloud.google.com/kubernetes-engine/docs/concepts/choose-cluster-mode),
  [fleets](https://cloud.google.com/kubernetes-engine/docs/fleets-overview),
  [Config Sync](https://cloud.google.com/kubernetes-engine/docs/config-sync-overview),
  [Cloud Service Mesh](https://cloud.google.com/service-mesh/docs/overview) and its
  [advanced traffic management](https://cloud.google.com/service-mesh/docs/service-routing/advanced-traffic-management),
  [Backup for GKE](https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/concepts/backup-for-gke),
  [Cloud Run](https://cloud.google.com/run/docs/overview/what-is-cloud-run),
  [Cloud Run functions](https://cloud.google.com/functions/docs/concepts/overview),
  [Eventarc](https://cloud.google.com/eventarc/docs/overview),
  [App Engine environments](https://cloud.google.com/appengine/docs/the-appengine-environments),
  [Firebase Hosting](https://firebase.google.com/products/hosting),
  [Artifact Registry](https://cloud.google.com/artifact-registry/docs/overview) and its
  [transition from Container Registry](https://cloud.google.com/artifact-registry/docs/transition/transition-from-gcr).
- **Module 04.** [Cloud Storage introduction](https://cloud.google.com/storage/docs/introduction),
  [storage classes](https://cloud.google.com/storage/docs/storage-classes),
  [storage quotas](https://cloud.google.com/storage/quotas),
  [availability and durability](https://cloud.google.com/storage/docs/availability-durability),
  [Rapid bucket](https://cloud.google.com/storage/docs/rapid/rapid-bucket),
  [Persistent Disk](https://cloud.google.com/compute/docs/disks/persistent-disks),
  [Hyperdisk](https://cloud.google.com/compute/docs/disks/hyperdisks),
  [Local SSD](https://cloud.google.com/compute/docs/disks/local-ssd),
  [Filestore](https://cloud.google.com/filestore/docs/overview),
  [NetApp Volumes](https://cloud.google.com/netapp/volumes),
  [Managed Lustre](https://cloud.google.com/managed-lustre/docs/overview),
  [Parallelstore](https://cloud.google.com/parallelstore/docs/overview),
  [Storage Transfer Service](https://cloud.google.com/storage-transfer/docs/overview),
  [Transfer Appliance](https://cloud.google.com/transfer-appliance/docs/4.0/overview).
- **Module 05.** [Cloud SQL](https://cloud.google.com/sql/docs/introduction),
  [AlloyDB](https://cloud.google.com/alloydb/docs/overview),
  [Spanner](https://cloud.google.com/spanner/docs/overview),
  [Spanner Graph](https://cloud.google.com/spanner/docs/graph),
  [Bigtable](https://cloud.google.com/bigtable/docs/overview),
  [Firestore](https://cloud.google.com/firestore/docs),
  [Memorystore for Redis](https://cloud.google.com/memorystore/docs/redis/redis-overview),
  [Memorystore for Valkey](https://cloud.google.com/memorystore/docs/valkey),
  [Database Migration Service](https://cloud.google.com/database-migration/docs),
  [Datastream](https://cloud.google.com/datastream/docs/overview),
  [Database Center](https://cloud.google.com/database-center/docs/overview).
- **Module 06.** [BigQuery](https://cloud.google.com/bigquery/docs/introduction),
  [BigLake](https://cloud.google.com/bigquery/docs/biglake-intro),
  [Dataflow](https://cloud.google.com/dataflow/docs/guides),
  [Managed Service for Apache Kafka](https://cloud.google.com/managed-kafka/docs/overview),
  [Dataproc](https://cloud.google.com/dataproc/docs/concepts/overview),
  [Managed Service for Apache Spark](https://cloud.google.com/products/managed-service-for-apache-spark),
  [Cloud Composer](https://cloud.google.com/composer/docs/concepts/overview),
  [Knowledge Catalog](https://cloud.google.com/dataplex/docs/introduction),
  [BigQuery data clean rooms](https://cloud.google.com/bigquery/docs/data-clean-rooms),
  [Looker](https://cloud.google.com/looker/docs),
  [Looker Studio](https://cloud.google.com/looker-studio).
- **Module 07.** [VPC networks](https://cloud.google.com/vpc/docs/vpc),
  [subnets](https://cloud.google.com/vpc/docs/subnets),
  [multiple network interfaces](https://cloud.google.com/compute/docs/instances/create-instance-multiple-nics),
  [routes](https://cloud.google.com/vpc/docs/routes),
  [Cloud Router](https://cloud.google.com/network-connectivity/docs/router/concepts/overview),
  [Cloud NAT](https://cloud.google.com/nat/docs/overview),
  [firewall rules](https://cloud.google.com/firewall/docs/firewalls),
  [network service tiers](https://cloud.google.com/network-tiers/docs/overview),
  [Private Google Access](https://cloud.google.com/vpc/docs/private-google-access-hybrid),
  [Private Services Access](https://cloud.google.com/vpc/docs/private-services-access),
  [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect),
  [VPC Network Peering](https://cloud.google.com/vpc/docs/vpc-peering),
  [Shared VPC](https://cloud.google.com/vpc/docs/shared-vpc),
  [Network Connectivity Center](https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/overview),
  [router appliance spokes](https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/ra-overview),
  [HA VPN](https://cloud.google.com/network-connectivity/docs/vpn/concepts/overview),
  [VPN quotas](https://cloud.google.com/network-connectivity/docs/vpn/quotas),
  [Dedicated Interconnect](https://cloud.google.com/network-connectivity/docs/interconnect/concepts/dedicated-overview),
  [Partner Interconnect](https://cloud.google.com/network-connectivity/docs/interconnect/concepts/partner-overview),
  [Cross-Cloud Interconnect](https://cloud.google.com/network-connectivity/docs/interconnect/concepts/cci-overview),
  [Google Distributed Cloud](https://cloud.google.com/distributed-cloud),
  [VMware Engine](https://cloud.google.com/vmware-engine/docs/overview),
  [load balancing](https://cloud.google.com/load-balancing/docs/load-balancing-overview),
  [Cloud CDN](https://cloud.google.com/cdn/docs/overview),
  [Media CDN](https://cloud.google.com/media-cdn/docs/overview),
  [Cloud Armor](https://cloud.google.com/armor/docs/cloud-armor-overview),
  [Cloud DNS](https://cloud.google.com/dns/docs/overview),
  [DNS routing policies](https://cloud.google.com/dns/docs/routing-policies-overview),
  [Cloud Domains](https://cloud.google.com/domains/docs/overview).
- **Module 08.** [IAM overview](https://cloud.google.com/iam/docs/overview),
  [policy types](https://cloud.google.com/iam/docs/policy-types),
  [roles overview](https://cloud.google.com/iam/docs/roles-overview),
  [Principal Access Boundary policies](https://cloud.google.com/iam/docs/principal-access-boundary-policies),
  [Privileged Access Manager](https://cloud.google.com/iam/docs/pam-overview),
  [VPC Service Controls](https://cloud.google.com/vpc-service-controls/docs/overview),
  [service accounts](https://cloud.google.com/iam/docs/service-account-overview),
  [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation),
  [short-lived credentials](https://cloud.google.com/iam/docs/create-short-lived-credentials-direct),
  [Workforce Identity Federation](https://cloud.google.com/iam/docs/workforce-identity-federation),
  [Cloud Identity](https://cloud.google.com/identity),
  [Managed Service for Microsoft AD](https://cloud.google.com/managed-microsoft-ad/docs/overview),
  [OS Login](https://cloud.google.com/compute/docs/oslogin),
  [Identity Platform](https://cloud.google.com/identity-platform/docs),
  [Cloud KMS](https://cloud.google.com/kms/docs/key-management-service),
  [Cloud HSM](https://cloud.google.com/kms/docs/hsm),
  [Cloud EKM](https://cloud.google.com/kms/docs/ekm),
  [Secret Manager](https://cloud.google.com/secret-manager/docs/overview),
  [Certificate Manager](https://cloud.google.com/certificate-manager/docs/overview),
  [Certificate Authority Service](https://cloud.google.com/certificate-authority-service/docs).
- **Module 09.** [Assured Workloads](https://cloud.google.com/assured-workloads/docs/overview),
  [Service Catalog](https://cloud.google.com/service-catalog/docs/overview),
  [tags and labels](https://cloud.google.com/resource-manager/docs/tags/tags-overview),
  [quotas](https://cloud.google.com/docs/quotas/view-manage),
  [Cloud Asset Inventory](https://cloud.google.com/asset-inventory/docs/overview),
  [custom organisation policy constraints](https://cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints),
  [Security Command Center](https://cloud.google.com/security-command-center/docs/security-command-center-overview),
  [security posture service](https://docs.cloud.google.com/security-command-center/docs/security-posture-overview),
  [billing export](https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables),
  [committed use discounts](https://cloud.google.com/docs/cuds),
  [Recommender](https://cloud.google.com/recommender/docs/overview).
- **Module 10.** [Cloud Logging storage](https://cloud.google.com/logging/docs/storage),
  [routing overview](https://cloud.google.com/logging/docs/routing/overview),
  [logging quotas](https://cloud.google.com/logging/quotas),
  [Observability Analytics](https://cloud.google.com/logging/docs/log-analytics),
  [Error Reporting](https://cloud.google.com/error-reporting/docs/grouping-errors),
  [audit logs overview](https://cloud.google.com/logging/docs/audit),
  [configuring Data Access logs](https://cloud.google.com/logging/docs/audit/configure-data-access),
  [VPC Flow Logs](https://cloud.google.com/vpc/docs/flow-logs),
  [firewall rules logging](https://cloud.google.com/firewall/docs/firewall-rules-logging),
  [Cloud NAT monitoring](https://cloud.google.com/nat/docs/monitoring),
  [DNS monitoring](https://cloud.google.com/dns/docs/monitoring),
  [logs viewer](https://cloud.google.com/logging/docs/view/logs_viewer),
  [Monitoring quotas](https://cloud.google.com/monitoring/quotas),
  [metric latency and retention](https://cloud.google.com/monitoring/api/v3/latency-n-retention),
  [Managed Service for Prometheus](https://cloud.google.com/stackdriver/docs/managed-prometheus),
  [Ops Agent](https://cloud.google.com/stackdriver/docs/solutions/agents/ops-agent),
  [alerting](https://cloud.google.com/monitoring/alerts),
  [uptime checks](https://cloud.google.com/monitoring/uptime-checks),
  [Cloud Trace](https://cloud.google.com/trace/docs/overview),
  [Cloud Profiler](https://cloud.google.com/profiler/docs/about-profiler),
  [Network Intelligence Center](https://cloud.google.com/network-intelligence-center),
  [Personalized Service Health](https://cloud.google.com/service-health/docs/overview).
- **Module 11.** [VPC Service Controls](https://cloud.google.com/vpc-service-controls/docs/overview),
  [Identity-Aware Proxy](https://cloud.google.com/iap/docs/concepts-overview),
  [Cloud Armor](https://cloud.google.com/armor/docs/cloud-armor-overview),
  [reCAPTCHA Enterprise](https://cloud.google.com/security/products/recaptcha),
  [Cloud NGFW policies](https://cloud.google.com/firewall/docs/firewall-policies),
  [Packet Mirroring](https://cloud.google.com/vpc/docs/packet-mirroring),
  [Security Command Center threats](https://cloud.google.com/security-command-center/docs/overview-threats),
  [security posture service](https://docs.cloud.google.com/security-command-center/docs/security-posture-overview),
  [Artifact Analysis](https://cloud.google.com/artifact-analysis/docs/),
  [Web Security Scanner](https://cloud.google.com/security-command-center/docs/how-to-use-web-security-scanner),
  [Sensitive Data Protection](https://cloud.google.com/sensitive-data-protection/docs),
  [Model Armor](https://cloud.google.com/security-command-center/docs/model-armor-overview).
- **Module 12.** [Infrastructure Manager](https://cloud.google.com/infrastructure-manager/docs/overview),
  [Deployment Manager deprecations](https://cloud.google.com/deployment-manager/docs/deprecations),
  [Config Connector](https://cloud.google.com/config-connector/docs/overview),
  [Cloud Build](https://cloud.google.com/build/docs/overview),
  [Cloud Deploy](https://cloud.google.com/deploy/docs/overview),
  [Binary Authorization](https://cloud.google.com/binary-authorization/docs/overview),
  [Cloud Source Repositories](https://cloud.google.com/source-repositories/docs),
  [Pub/Sub](https://cloud.google.com/pubsub/docs/overview),
  [Cloud Tasks](https://cloud.google.com/tasks/docs),
  [Eventarc](https://cloud.google.com/eventarc/docs/overview),
  [Firebase Realtime Database](https://firebase.google.com/docs/database),
  [Workflows](https://cloud.google.com/workflows/docs/overview),
  [Cloud Scheduler](https://cloud.google.com/scheduler/docs),
  [Application Integration](https://cloud.google.com/application-integration/docs/overview),
  [API Gateway](https://cloud.google.com/api-gateway/docs/about-api-gateway),
  [Apigee](https://cloud.google.com/apigee/docs/api-platform/get-started/what-apigee).
  The one third-party source the course links is the
  [Terraform google provider registry](https://registry.terraform.io/providers/hashicorp/google/latest/docs),
  labelled as third-party at the point of use in lesson 1200.
- **Module 13.** [Vertex AI generative models](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/overview),
  [Document AI](https://cloud.google.com/document-ai/docs/overview),
  [Vertex AI platform introduction](https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform),
  [Vector Search](https://cloud.google.com/vertex-ai/docs/vector-search/overview),
  [RAG Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview),
  [the enterprise search product](https://cloud.google.com/generative-ai-app-builder/docs/introduction),
  [the agent platform](https://cloud.google.com/agentspace/docs/overview).
- **Module 14.** [Backup and DR Service](https://cloud.google.com/backup-disaster-recovery/docs/concepts/backup-dr),
  [availability and durability](https://cloud.google.com/storage/docs/availability-durability),
  [Migrate to Virtual Machines](https://cloud.google.com/migrate/compute-engine/docs/overview),
  [the Well-Architected Framework](https://cloud.google.com/architecture/framework).
- **Certification weights**, used only to say what an exam tests and never as a schedule:
  the [Associate Cloud Engineer guide](https://services.google.com/fh/files/misc/associate_cloud_engineer_exam_guide_english.pdf)
  and the [Professional Cloud Architect guide](https://services.google.com/fh/files/misc/professional_cloud_architect_exam_guide_english.pdf).

## Gaps

Topics the verified inventory flagged as unfinished. Each is named on the page that
would otherwise have asserted it, in a warning callout, and none is stated as fact.

- **Standalone organization creation.** The hierarchy documentation confirms the flow
  exists; the mechanics were not verified. Named in lesson 0101.
- **App Engine positioning for new workloads.** The inventory records that Google steers
  new applications towards Cloud Run while App Engine remains generally available, and
  flags the steering statement as unverified. Lesson 0303 states only the general
  availability.
- **Rapid storage class stage.** Recorded as preview with an explicit instruction to
  re-check the stage before teaching it as settled. Named in lesson 0400.
- **Transfer Appliance capacities.** Vary by hardware generation and were recorded as
  needing a re-check; no capacity figure is printed. Named in lesson 0404.
- **Live region and zone counts.** Deliberately not printed anywhere, because the count
  moves. Lesson 0100 points at the vendor's live list instead.
- **Compute and runtime telemetry rows.** The inventory carries an explicit caution that
  its App Engine request-log behaviour and legacy storage-log rows were never verified.
  Nothing in this course rests on them; lesson 1002 names both as leads to check rather
  than as facts.
- **Log ingestion and retention prices.** Recorded in the inventory as figures per
  gibibyte. Not printed anywhere in the course, because `MISSION.md` puts list prices out
  of scope; lesson 1000 teaches the cost shape and links the vendor's page.
- **Cloud Trace BigQuery sink retirement.** Recorded with deprecation and shutdown dates.
  Lesson 1004 states that the sink is deprecated with a scheduled shutdown and prints no
  date, because dates belong only in this file.
- **AlloyDB elastic scaling and read-pool autoscaling.** The inventory records the
  Autopilot-style Slices feature with an instruction to confirm its stage, and records
  read-pool autoscaling as preview. Named in lesson 0500; neither is stated as settled.
- **Database Center stage.** Recorded as preview with an explicit instruction to verify
  the stage before teaching it. Named in lesson 0504.
- **Network interface limits per machine type.** The inventory flags the limits table as
  needing a re-check; no figure is printed. Named in lesson 0700.
- **Interconnect SLA percentages per topology.** Recorded as still open, to be read from the
  live vendor pages. No percentage is printed. Named in lesson 0704. The HA VPN 99.99%
  figure is separate and was verified.
- **Cloud Domains retirement.** The registrar service is recorded as retiring with the
  migration mechanics and dates unverified. Named in lesson 0705, which asserts nothing
  about them.
- **Downscoped access tokens.** The inventory records credential access boundaries with
  the current API surface flagged for confirmation. Named in lesson 0802; nothing about
  their shape is stated.
- **Detailed billing export cadence.** The inventory records the detailed export as
  updating more often than the daily standard export and hedges the exact figure. No
  cadence is printed. Named in lesson 0903.
- **Infrastructure Manager Terraform drift detection.** Claimed during research, could not
  be verified, and removed rather than softened. Nothing in this course rests on it;
  lesson 0902 says so explicitly.
- **Model Armor stage.** Recorded as preview with an instruction to confirm the stage
  before teaching it as settled. Named in lesson 1103, which asserts no availability.
- **Cloud IDS retirement.** Recorded as retiring. Lesson 1102 says so and prints no date,
  because dates belong only in this file.
- **Infrastructure Manager drift detection.** Already recorded above as removed during the
  corrections pass. Lesson 1200 repeats that plainly, because the inventory's own one-line
  summary of the product still mentions it and a future author will meet the same conflict.
- **Config Sync packaging.** The inventory notes the product has moved under the GKE
  Enterprise naming and says to verify the current product page. Named in lesson 1200.
- **Cloud Source Repositories retirement and Deployment Manager turndown.** Both recorded
  with dates. The lessons state the retirement and print no date.
- **Agent platform stage and branding.** Recorded as preview and as a naming hotspot, with
  a previous product page and its first replacement URL both gone. Lesson 1303 names no
  product name as settled and teaches the mechanism instead.
- **RAG Engine stage.** Recorded as preview. Named in lesson 1302 with an instruction to
  confirm.
- **Notebook surface naming.** The inventory records the certification guide and the product
  documentation using different wording. Lesson 1301 asserts no name for it.
- **Recovery points other than turbo replication.** The inventory records one figure for
  this area - roughly fifteen minutes for a dual-region bucket with turbo replication. No
  other window is printed; lesson 1401 marks the rest of the axis qualitatively and points
  at each mechanism's own documentation.
- **Live region count.** The inventory notes a scale of more than forty regions with an
  instruction to re-check. No count is printed anywhere, consistent with lesson 0100.
