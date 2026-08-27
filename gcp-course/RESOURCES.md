# RESOURCES - Inside Google Cloud

The sources this course keeps returning to, and the provenance discipline that keeps
a future refresh cheap. This file is the one place in the course where dates belong.

## Canon

- **Google Cloud documentation** - <https://cloud.google.com/docs>. The vendor's own reference for every
  user-facing behaviour this course describes.

Two sibling roots are the same vendor and count as canon: <https://firebase.google.com>
for Firebase products, and <https://services.google.com> for the certification guides
the vendor publishes as PDFs. Anything outside those three roots is third-party and is
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
  Nothing in modules 01 to 04 rests on them; a future module 10 must re-check before use.
- **AlloyDB elastic scaling and read-pool autoscaling.** The inventory records the
  Autopilot-style Slices feature with an instruction to confirm its stage, and records
  read-pool autoscaling as preview. Named in lesson 0500; neither is stated as settled.
- **Database Center stage.** Recorded as preview with an explicit instruction to verify
  the stage before teaching it. Named in lesson 0504.
