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

## Gaps

Topics deliberately left unwritten because the verified inventory does not cover
them, rather than because they are unimportant:

- Latency figures for any path into or inside OCI. Oracle publishes no service-level
  number the inventory could verify, so pages teach relative positioning instead.
- Prices, including certification prices. The inventory records that no price appears
  on the official exam pages, so no page here states one.
- Contractual event-to-visibility delays for the telemetry streams. Operational
  observations exist in the inventory; no published commitment does.
