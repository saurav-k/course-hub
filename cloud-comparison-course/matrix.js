/* The capability matrix data for Comparing the Four Clouds.

   One file is the single source of truth for both the rendered matrix and the
   validation gate:

     - clouds   the four columns, in column order
     - domains  the twenty-four capability areas of the shared taxonomy, each
                carrying the capability keys that belong to it
     - rows     one row per capability key, one cell per cloud

   A cell is exactly one of four states, and the reader must be able to tell the
   middle two apart at a glance, because they make opposite claims:

     {"state": "unfilled"}
         Nobody has filled this cell in yet. Rendered as a dashed, quiet box;
         it means "not written yet", never "this cloud has nothing here".
     {"state": "absent", "reason": "..."}
         A finding: this cloud genuinely ships no equivalent for the
         capability, and the reason says what is nearest and how it differs.
         This is the only state that supports the reading "this cloud cannot
         do that", which is why the widget spends the words NO EQUIVALENT here
         and nowhere else.
     {"state": "elsewhere", "reason": "...", "see": "<capability key>"}
         The cloud has the capability. It is delivered by a service that holds
         a row under another key, because only one of the four clouds packages
         it as its own product. The reason names the service in the audit's own
         words and "see" names the row it lives in, which the widget renders as
         a link to that row. Five of these entries name no single row, so "see"
         is absent on them and the reason carries the whole answer.
     {"state": "service", "services": [{"name": ..., "short_name": ...,
                                         "doc_url": ..., "one_line": ...,
                                         "status": ...}]}
         One or more services answering the capability, each linking that
         vendor's own documentation. "status" is ga, preview, retiring or
         deprecated; the widget badges everything that is not ga, which is how
         a reader tells a current service from the legacy one beside it, and
         therefore which one a new design should pick.

   "snapshot" is data, not page text. This course forbids dates on its pages, so
   the widget does not paint it and RESOURCES.md carries the same date as the
   reader-facing provenance. It sits here so a refresh knows what it refreshes.

   scripts/validate_site.py enforces all of this: every row resolves to a key
   in the taxonomy and appears once, every row carries all four clouds, every
   cell is one of the four states, every "see" resolves to a real row, and every
   doc_url is well formed.

   Generated from the verified inventories, not hand-edited. Four clouds, two
   independent audits each, then a reconciliation onto one vocabulary and a
   repair pass. Correct a fact in the inventory it came from and regenerate; do
   not patch a cell here, because the next regeneration would silently drop the
   patch. */
window.CLOUD_CAPABILITY_MATRIX = {
  "version": 1,
  "note": "One row per capability key; one column per cloud. A cell is a service (with a link to that vendor's own documentation), a declared absence with a reason, or unfilled until verified research fills it.",
  "snapshot": "2026-08-26",
  "clouds": [
    {
      "key": "aws",
      "short": "AWS",
      "name": "Amazon Web Services",
      "docs": "https://docs.aws.amazon.com/"
    },
    {
      "key": "azure",
      "short": "Azure",
      "name": "Microsoft Azure",
      "docs": "https://learn.microsoft.com/en-us/azure/"
    },
    {
      "key": "gcp",
      "short": "GCP",
      "name": "Google Cloud",
      "docs": "https://cloud.google.com/docs"
    },
    {
      "key": "oci",
      "short": "OCI",
      "name": "Oracle Cloud Infrastructure",
      "docs": "https://docs.oracle.com/en-us/iaas/"
    }
  ],
  "domains": [
    {
      "slug": "compute-iaas",
      "name": "Compute (IaaS)",
      "covers": "VMs, instance families, images, bare metal, GPU, spot/preemptible, placement, dedicated hosts",
      "keys": [
        "bare-metal",
        "batch-compute",
        "confidential-compute",
        "dedicated-hosts",
        "gpu-compute",
        "spot-capacity",
        "vm-images",
        "vm-instances",
        "vm-instances-simplified"
      ]
    },
    {
      "slug": "compute-scaling",
      "name": "Compute scaling",
      "covers": "autoscaling groups/sets, instance templates, health-based replacement, scheduled and predictive scaling",
      "keys": [
        "autoscaling-group",
        "instance-template"
      ]
    },
    {
      "slug": "containers",
      "name": "Containers",
      "covers": "managed Kubernetes, serverless containers, container registry, service mesh, container build",
      "keys": [
        "container-orchestrator-nonk8s",
        "container-registry",
        "kubernetes-backup",
        "kubernetes-fleet-management",
        "kubernetes-node-autoscaler",
        "managed-kubernetes",
        "serverless-containers",
        "service-mesh"
      ]
    },
    {
      "slug": "serverless-app",
      "name": "Serverless and app hosting",
      "covers": "functions/FaaS, app hosting platforms, PaaS web/app runtimes, static site hosting",
      "keys": [
        "functions-faas",
        "paas-web-runtime",
        "static-site-hosting"
      ]
    },
    {
      "slug": "storage",
      "name": "Storage",
      "covers": "object, block, file, archive/cold tiers, storage gateway, bulk data transfer appliances",
      "keys": [
        "archive-storage",
        "block-storage",
        "bulk-transfer-appliance",
        "file-storage",
        "hybrid-storage-gateway",
        "object-storage",
        "object-storage-highperf",
        "object-storage-tables"
      ]
    },
    {
      "slug": "databases",
      "name": "Databases",
      "covers": "relational, NoSQL, key-value, document, in-memory, graph, time-series, ledger, migration services",
      "keys": [
        "change-data-capture",
        "database-fleet-management",
        "db-migration-service",
        "globally-distributed-sql",
        "graph-database",
        "in-memory-cache",
        "ledger",
        "nosql-document",
        "nosql-keyvalue",
        "relational-managed",
        "relational-serverless",
        "timeseries-database"
      ]
    },
    {
      "slug": "analytics",
      "name": "Analytics",
      "covers": "data warehouse, lakehouse, ETL/ELT, streaming, managed Spark/Flink, search, BI, data catalog",
      "keys": [
        "bi-dashboards",
        "clean-rooms",
        "data-catalog",
        "data-lake",
        "data-warehouse",
        "etl-service",
        "managed-search",
        "managed-spark",
        "serverless-query-engine",
        "stream-analytics",
        "stream-ingest"
      ]
    },
    {
      "slug": "networking-core",
      "name": "Networking core",
      "covers": "virtual networks, subnets, routing, NAT, private endpoints/service links, peering, IP address management, network interfaces",
      "keys": [
        "bgp-dynamic-routing",
        "ip-address-management",
        "nat-gateway",
        "network-interface",
        "network-manager",
        "network-peering",
        "private-endpoint",
        "route-table",
        "shared-vpc",
        "stateful-packet-filter",
        "subnet",
        "transit-hub",
        "virtual-network"
      ]
    },
    {
      "slug": "networking-lb-edge",
      "name": "Load balancing and edge",
      "covers": "L4 and L7 load balancers, global anycast front doors, CDN, DDoS-scrubbing edge, traffic managers",
      "keys": [
        "cdn",
        "ddos-protection",
        "gateway-load-balancer",
        "global-front-door",
        "l4-load-balancer",
        "l7-load-balancer"
      ]
    },
    {
      "slug": "dns-domains",
      "name": "DNS and domains",
      "covers": "authoritative DNS, private DNS zones, domain registrar, health-checked and geo/latency routing policies",
      "keys": [
        "authoritative-dns",
        "dns-routing-policies",
        "domain-registrar",
        "private-dns"
      ]
    },
    {
      "slug": "hybrid-connectivity",
      "name": "Hybrid connectivity",
      "covers": "site-to-site and client VPN, dedicated private circuits, on-prem/edge racks and stacks, SD-WAN partners",
      "keys": [
        "client-vpn",
        "cross-cloud-interconnect",
        "dedicated-interconnect",
        "metro-edge-locations",
        "on-prem-extension",
        "sdwan-integration",
        "site-to-site-vpn",
        "vmware-stack-hosting"
      ]
    },
    {
      "slug": "identity-workforce",
      "name": "Identity - workforce",
      "covers": "the cloud's own IAM: users, groups, roles, policy language, permission boundaries, SSO/workforce federation, privileged access",
      "keys": [
        "conditional-access",
        "iam-policy-language",
        "iam-principals",
        "iam-roles",
        "managed-directory",
        "os-login",
        "permission-boundary",
        "privileged-access",
        "workforce-sso"
      ]
    },
    {
      "slug": "identity-workload",
      "name": "Identity - machine",
      "covers": "machine identity: instance/pod/function identity, workload identity federation, cross-account and cross-tenant role assumption, short-lived credential issuance",
      "keys": [
        "agent-identity",
        "cross-account-assumption",
        "short-lived-credentials",
        "workload-identity",
        "workload-identity-federation"
      ]
    },
    {
      "slug": "identity-customer",
      "name": "Identity - customer (CIAM)",
      "covers": "CIAM for the apps you build: user pools/directories, social and enterprise federation, MFA, token issuance, B2C tenants",
      "keys": [
        "ciam-mfa",
        "ciam-social-federation",
        "ciam-user-directory"
      ]
    },
    {
      "slug": "secrets-keys",
      "name": "Secrets and keys",
      "covers": "key management, HSM, secrets stores, certificate issuance and lifecycle, envelope encryption, BYOK/HYOK",
      "keys": [
        "byok-hyok",
        "certificate-authority",
        "certificate-manager",
        "hsm",
        "key-management",
        "secrets-store"
      ]
    },
    {
      "slug": "org-tenancy",
      "name": "Organisation and tenancy",
      "covers": "the account/subscription/project/compartment hierarchy, org policy and guardrails, landing zones, quotas, tagging, billing and cost management",
      "keys": [
        "commitment-discounts",
        "cost-advisory",
        "cost-management",
        "cross-account-resource-sharing",
        "landing-zone",
        "org-guardrail-policy",
        "org-hierarchy",
        "quota-management",
        "resource-tagging",
        "service-catalog"
      ]
    },
    {
      "slug": "governance-policy",
      "name": "Governance and policy",
      "covers": "policy-as-code, configuration/drift assessment, compliance packs and attestation, resource graph/inventory query",
      "keys": [
        "compliance-pack",
        "config-drift-assessment",
        "policy-as-code",
        "resource-graph-query"
      ]
    },
    {
      "slug": "observability",
      "name": "Observability",
      "covers": "metrics, logs, traces, dashboards, alerting, synthetic monitoring, profilers, the query language",
      "keys": [
        "alerting",
        "dashboards",
        "distributed-tracing",
        "error-reporting",
        "log-store",
        "managed-prometheus",
        "metrics-store",
        "network-diagnostics",
        "profiler",
        "service-health-dashboard",
        "synthetic-monitoring",
        "telemetry-agent"
      ]
    },
    {
      "slug": "audit-telemetry",
      "name": "Audit and telemetry",
      "covers": "the SPECIFIC telemetry streams the platform emits - control-plane audit, data-plane access, network flow logs, service-specific logs - see section D2",
      "keys": [
        "access-transparency-logs",
        "control-plane-audit-log",
        "data-plane-access-log",
        "dns-query-log",
        "firewall-rules-log",
        "identity-provider-audit-log",
        "load-balancer-access-log",
        "nat-logs",
        "network-flow-log",
        "policy-denied-audit-log",
        "service-specific-log"
      ]
    },
    {
      "slug": "security-services",
      "name": "Security services",
      "covers": "WAF, firewall, threat detection, posture management, vulnerability scanning, data classification, incident response tooling",
      "keys": [
        "ai-safety-guardrails",
        "bastion",
        "cloud-firewall",
        "data-classification",
        "packet-mirroring",
        "posture-management",
        "security-investigation-graph",
        "service-perimeter",
        "threat-detection",
        "verified-permissions",
        "vulnerability-scanning",
        "waf",
        "zero-trust-app-access",
        "zero-trust-routing"
      ]
    },
    {
      "slug": "iac-deployment",
      "name": "IaC and deployment",
      "covers": "native templates, Terraform/OpenTofu providers, imperative-in-code SDKs, config management, pipeline/CI-CD services, progressive delivery",
      "keys": [
        "artifact-registry",
        "cicd-pipeline",
        "config-management",
        "iac-in-code-sdk",
        "kubernetes-config-management",
        "native-iac-template",
        "progressive-delivery",
        "terraform-provider"
      ]
    },
    {
      "slug": "integration-messaging",
      "name": "Integration and messaging",
      "covers": "queues, pub/sub, event buses, workflow orchestration, API gateways, managed integration/iPaaS",
      "keys": [
        "api-gateway",
        "event-bus",
        "graphql-api",
        "managed-integration",
        "message-queue",
        "mqtt-broker",
        "pub-sub",
        "realtime-messaging",
        "scheduler-jobs",
        "telemetry-export-pipeline",
        "workflow-orchestration"
      ]
    },
    {
      "slug": "ai-ml",
      "name": "AI and ML",
      "covers": "managed model APIs, training and tuning platforms, vector stores, agent platforms, speech/vision/document extraction",
      "keys": [
        "agent-platform",
        "managed-model-api",
        "managed-rag-pipeline",
        "model-training-platform",
        "speech-vision-document-ai",
        "vector-store"
      ]
    },
    {
      "slug": "resilience-migration",
      "name": "Resilience and migration",
      "covers": "backup, DR orchestration, replication, migration services and assessment tooling, chaos/resilience testing, region/AZ model",
      "keys": [
        "backup-service",
        "cross-region-replication",
        "dr-orchestration",
        "migration-service",
        "online-transfer",
        "region-az-model",
        "resilience-assessment",
        "well-architected-framework"
      ]
    }
  ],
  "rows": [
    {
      "key": "bare-metal",
      "domain": "compute-iaas",
      "title": "Bare metal",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon EC2 Bare Metal Instances",
              "short_name": "Bare Metal (.metal)",
              "doc_url": "https://docs.aws.amazon.com/ec2/latest/instancetypes/ec2-nitro-instances.html",
              "one_line": "Instance types where the OS runs directly on the physical server with no hypervisor while keeping full VPC integration.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Baremetal Infrastructure",
              "short_name": "Baremetal",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-machines/workloads/sap/get-started",
              "one_line": "Single-tenant bare-metal instances certified mainly for SAP HANA workloads.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Bare Metal Solution / Bare Metal instances",
              "short_name": "BMS",
              "doc_url": "https://cloud.google.com/compute/docs/instances/bare-metal-instances",
              "one_line": "Single-tenant physical servers for specialized/licensed workloads (notably Oracle).",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Bare Metal Compute",
              "short_name": "Bare Metal",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm",
              "one_line": "Entire physical servers with no hypervisor, up to BM.Standard.E6.256 class machines.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "batch-compute",
      "domain": "compute-iaas",
      "title": "Batch compute",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Batch",
              "short_name": "Batch",
              "doc_url": "https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html",
              "one_line": "Fully managed batch scheduling over EC2, Fargate, or EKS compute environments: job queues, array jobs, and multi-node parallel jobs with priority sharing.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Batch",
              "short_name": "Batch",
              "doc_url": "https://learn.microsoft.com/en-us/azure/batch/",
              "one_line": "Managed job scheduler that runs parallel HPC workloads on pools of VMs.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Batch",
              "short_name": "Batch",
              "doc_url": "https://cloud.google.com/batch/docs/get-started",
              "one_line": "Fully managed scheduler for batch jobs on CE resources without cluster management.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "OCI Batch",
              "short_name": "Batch",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/oci-batch/home.htm",
              "one_line": "Managed batch job orchestration engine that provisions compute, runs containerized tasks, and tears down automatically.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "confidential-compute",
      "domain": "compute-iaas",
      "title": "Confidential compute",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Nitro Enclaves",
              "short_name": "Nitro Enclaves",
              "doc_url": "https://docs.aws.amazon.com/enclaves/latest/user/nitro-enclave.html",
              "one_line": "Isolated hardened virtual machines carved out of an EC2 instance, with no persistent storage, no interactive access, and no external networking.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Confidential Computing",
              "short_name": "Confidential VMs",
              "doc_url": "https://learn.microsoft.com/en-us/azure/confidential-computing/",
              "one_line": "VM sizes with hardware trusted execution environments (AMD SEV-SNP, Intel TDX, NVIDIA H100 TEE).",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Confidential VMs / Confidential Space",
              "short_name": "Conf CC",
              "doc_url": "https://cloud.google.com/compute/docs/about-confidential-vm",
              "one_line": "Memory-encrypted computing with attestation for sensitive data processing.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "OCI Confidential Computing",
              "short_name": "Confidential VMs",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Compute/References/confidential_compute.htm",
              "one_line": "Virtual machine and bare metal shapes whose memory is encrypted from the hypervisor by AMD Secure Encrypted Virtualization.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "dedicated-hosts",
      "domain": "compute-iaas",
      "title": "Dedicated hosts",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon EC2 Dedicated Hosts",
              "short_name": "Dedicated Hosts",
              "doc_url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-overview.html",
              "one_line": "Physical servers fully dedicated to one customer enabling per-core/socket BYOL licensing; bills per host rather than per instance.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Dedicated Host",
              "short_name": "Dedicated Host",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-machines/dedicated-hosts",
              "one_line": "A physical server reserved for your subscription hosting one or more VMs.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Sole-Tenant Nodes",
              "short_name": "Sole-tenant",
              "doc_url": "https://cloud.google.com/compute/docs/nodes/sole-tenant-nodes",
              "one_line": "Dedicated physical hosts for licensing/compliance isolation of your VMs.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Dedicated Virtual Machine Hosts",
              "short_name": "Dedicated VM Hosts",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Compute/Concepts/dedicatedvmhosts.htm",
              "one_line": "A single-tenant physical server that runs only your virtual machines, for licensing, isolation, or placement control.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "gpu-compute",
      "domain": "compute-iaas",
      "title": "GPU compute",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon EC2 Accelerated Computing Instances",
              "short_name": "P/G/Trn/Inf instances",
              "doc_url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/accelerated-computing-instances.html",
              "one_line": "GPU and AWS-chip instances: NVIDIA P/G families plus Trainium for training and Inferentia for inference.",
              "status": "ga"
            },
            {
              "name": "EC2 Capacity Blocks for ML",
              "short_name": "Capacity Blocks",
              "doc_url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-blocks.html",
              "one_line": "Future-dated short-duration GPU capacity reservations inside EC2 UltraClusters, bookable up to 8 weeks ahead.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "GPU-optimized N-series VMs",
              "short_name": "N-series",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-machines/sizes-gpu",
              "one_line": "VM sizes with NVIDIA GPUs for AI training/inference and visualization.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud GPUs",
              "short_name": "GPUs",
              "doc_url": "https://cloud.google.com/compute/docs/gpus/overview",
              "one_line": "Attach NVIDIA accelerators (T4/L4/A4/H-series lines) to VMs or use GPU-optimized machine types.",
              "status": "ga"
            },
            {
              "name": "Cloud TPUs",
              "short_name": "TPU",
              "doc_url": "https://cloud.google.com/tpu/docs/tpus",
              "one_line": "Google-custom tensor processors for ML training/inference, sold as v5e/v5p/v6e-class slices.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "GPU Shapes and OCI Supercluster",
              "short_name": "GPU compute",
              "doc_url": "https://www.oracle.com/cloud/compute/gpu/",
              "one_line": "VM GPU shapes (A10 etc.) and bare-metal superclusters with NVIDIA H100/H200/Blackwell and AMD Instinct for large-scale AI training.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "spot-capacity",
      "domain": "compute-iaas",
      "title": "Spot capacity",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon EC2 Spot Instances",
              "short_name": "Spot",
              "doc_url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/how-spot-instances-work.html",
              "one_line": "Spare EC2 capacity at up to 90 percent discount reclaimable with a two-minute interruption notice.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Spot Virtual Machines",
              "short_name": "Spot VMs",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-machines/spot-vms",
              "one_line": "Deeply discounted evictable VM capacity taken from surplus Azure hardware.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Spot VMs",
              "short_name": "Spot",
              "doc_url": "https://cloud.google.com/compute/docs/instances/spot",
              "one_line": "Deeply discounted reclaimable capacity with no SLA and no fixed max runtime.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Preemptible Instances",
              "short_name": "Preemptible",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Compute/Concepts/preemptible.htm",
              "one_line": "Interruptible capacity reclaimed any time at a discount for fault-tolerant workloads.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "vm-images",
      "domain": "compute-iaas",
      "title": "VM images",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Machine Image (AMI)",
              "short_name": "AMI",
              "doc_url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html",
              "one_line": "Region-bound boot template holding OS, software, and block-device mapping required to launch an EC2 instance.",
              "status": "ga"
            },
            {
              "name": "EC2 Image Builder",
              "short_name": "Image Builder",
              "doc_url": "https://docs.aws.amazon.com/imagebuilder/latest/userguide/what-is-image-builder.html",
              "one_line": "Managed pipeline that builds, tests, and distributes hardened AMIs and container images on a schedule.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Compute Gallery",
              "short_name": "Compute Gallery",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-machines/shared-image-galleries",
              "one_line": "Managed repository for generalized and specialized VM images with versioning and regional replication.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Compute Engine images & image families",
              "short_name": "Images",
              "doc_url": "https://cloud.google.com/compute/docs/images",
              "one_line": "Public/custom boot images with versioned families and OS image lifecycle management.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Custom Images and Platform Images",
              "short_name": "Images",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Compute/References/images.htm",
              "one_line": "Platform images (Oracle Linux, Ubuntu, Windows) plus customer-created custom images captured from instances or imported from Object Storage.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "vm-instances",
      "domain": "compute-iaas",
      "title": "VM instances",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon EC2",
              "short_name": "EC2",
              "doc_url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html",
              "one_line": "Resizable virtual machines from hardware-defined instance types across general purpose, compute, memory, storage, and accelerated families.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Virtual Machines",
              "short_name": "VMs",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-machines/",
              "one_line": "General-purpose resizable Linux and Windows VMs across many series and sizes.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Compute Engine",
              "short_name": "CE",
              "doc_url": "https://cloud.google.com/compute/docs/machine-resource",
              "one_line": "Customizable VMs across machine families with live migration by default.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Compute Service (virtual machines)",
              "short_name": "Compute VMs",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm",
              "one_line": "Virtual machines on flexible shapes where OCPU count and memory are chosen independently.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "vm-instances-simplified",
      "domain": "compute-iaas",
      "title": "VM instances (simplified)",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Lightsail",
              "short_name": "Lightsail",
              "doc_url": "https://docs.aws.amazon.com/lightsail/latest/userguide/what-is-amazon-lightsail.html",
              "one_line": "Bundled virtual private servers with predictable monthly pricing - instances, managed databases, storage, and load balancing prepackaged for simple projects.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "absent",
          "reason": "No bundled fixed-price virtual private server product. A hand-sized B-series virtual machine is the nearest thing, billed per component."
        },
        "gcp": {
          "state": "absent",
          "reason": "No bundled fixed-price virtual private server product. E2 machine types with committed use discounts are the nearest thing, billed per component."
        },
        "oci": {
          "state": "absent",
          "reason": "No bundled virtual private server product, although the Always Free micro shapes cover the smallest cases. Compute bills per OCPU and per gigabyte."
        }
      }
    },
    {
      "key": "autoscaling-group",
      "domain": "compute-scaling",
      "title": "Autoscaling group",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon EC2 Auto Scaling Group",
              "short_name": "ASG",
              "doc_url": "https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-groups.html",
              "one_line": "Manages a fleet of instances to min/max/desired capacity with health-based replacement, AZ balancing, and dynamic, predictive, or scheduled scaling policies.",
              "status": "ga"
            },
            {
              "name": "EC2 Fleet / Spot Fleet",
              "short_name": "Fleets",
              "doc_url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet.html",
              "one_line": "Single-request launch of thousands of instances across types, AZs, and purchase options with automatic Spot replacement.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Virtual Machine Scale Sets (VMSS)",
              "short_name": "VMSS",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/",
              "one_line": "Homogeneous groups of load-balanced VMs with automatic scaling and health-based replacement.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Managed Instance Groups (MIG)",
              "short_name": "MIG",
              "doc_url": "https://cloud.google.com/compute/docs/instance-groups",
              "one_line": "Stateless/stateful VM groups with autoscaling, autohealing, rolling updates, multi-zone distribution.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Instance Pools with Autoscaling",
              "short_name": "Instance pools",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/autoscalinginstancepools.htm",
              "one_line": "Groups of identical instances from an instance configuration, scaled by metric thresholds or schedules.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "instance-template",
      "domain": "compute-scaling",
      "title": "Instance template",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon EC2 Launch Template",
              "short_name": "Launch Template",
              "doc_url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html",
              "one_line": "Versioned reusable launch-parameter set (AMI, type, network, user data) consumed by ASGs, Fleets, and direct launches - the AWS equivalent of an instance template.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "absent",
          "reason": "Azure ships no standalone reusable instance-template resource. The nearest equivalents are the VMSS model (the desired-state definition inside a scale set) and ARM/Bicep modules that stamp out VMs; scheduled scaling lives in Azure Monitor autoscale profiles rather than the template."
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Instance Templates",
              "short_name": "Template",
              "doc_url": "https://cloud.google.com/compute/docs/instance-templates",
              "one_line": "Reusable VM blueprints consumed by MIGs and bulk creation.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Instance Configurations",
              "short_name": "Instance config",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Compute/Concepts/instancemanagement.htm",
              "one_line": "Saved launch template (shape, image, metadata, networking) used to create instance pools.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "container-orchestrator-nonk8s",
      "domain": "containers",
      "title": "Container orchestrator (non-Kubernetes)",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Elastic Container Service",
              "short_name": "ECS",
              "doc_url": "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html",
              "one_line": "AWS-native container orchestrator built on task definitions, services, and capacity providers (Fargate, EC2, external).",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "absent",
          "reason": "No proprietary non-Kubernetes orchestrator. Container Apps is the nearest managed alternative, and it runs on Kubernetes and KEDA underneath."
        },
        "gcp": {
          "state": "absent",
          "reason": "No proprietary non-Kubernetes orchestrator. Cloud Run is the nearest managed alternative and is a serverless runtime rather than a general orchestrator."
        },
        "oci": {
          "state": "absent",
          "reason": "No proprietary non-Kubernetes orchestrator. Container Instances runs single containers, and anything larger goes to OKE."
        }
      }
    },
    {
      "key": "container-registry",
      "domain": "containers",
      "title": "Container registry",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Elastic Container Registry",
              "short_name": "ECR",
              "doc_url": "https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html",
              "one_line": "Managed private OCI image registry with IAM auth, scan-on-push, replication, and pull-through caching of Docker Hub/Quay/GHCR.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Container Registry",
              "short_name": "ACR",
              "doc_url": "https://learn.microsoft.com/en-us/azure/container-registry/",
              "one_line": "Private Docker/OCI registry with geo-replication, task automation, and Helm/OCI artifact support.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Container Registry",
              "short_name": "GCR",
              "doc_url": "https://cloud.google.com/artifact-registry/docs/transition/transition-from-gcr",
              "one_line": "Legacy global container registry - deprecated; reads redirect into Artifact Registry.",
              "status": "deprecated"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Container Registry (OCIR)",
              "short_name": "OCIR",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Registry/Concepts/registryoverview.htm",
              "one_line": "Oracle-managed OCI-spec registry for Docker images, Helm charts, and multi-arch manifest lists.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "kubernetes-backup",
      "domain": "containers",
      "title": "Kubernetes backup",
      "cells": {
        "aws": {
          "state": "absent",
          "reason": "No workload-aware Kubernetes backup service. AWS Backup does not cover EKS objects, so teams run Velero themselves."
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Backup for AKS",
              "short_name": "AKS Backup",
              "doc_url": "https://learn.microsoft.com/en-us/azure/backup/azure-kubernetes-service-backup-overview",
              "one_line": "Workload-aware backup and restore of AKS cluster resources together with their persistent volumes, scheduled and retained by a backup vault policy.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Backup for GKE",
              "short_name": "BfGKE",
              "doc_url": "https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/concepts/backup-for-gke",
              "one_line": "Workload-aware backup/restore of GKE clusters (configs + volumes) with plans.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No workload-aware Kubernetes backup service. Block Volume backup policies cover the persistent volumes, not the cluster objects."
        }
      }
    },
    {
      "key": "kubernetes-fleet-management",
      "domain": "containers",
      "title": "Kubernetes fleet management",
      "cells": {
        "aws": {
          "state": "absent",
          "reason": "No fleet abstraction across clusters. EKS clusters are managed one at a time, with policy applied through the account and organisation layers."
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Kubernetes Fleet Manager",
              "short_name": "Fleet Manager",
              "doc_url": "https://learn.microsoft.com/en-us/azure/kubernetes-fleet/overview",
              "one_line": "A fleet resource that groups AKS clusters so upgrades, workload placement, and multi-cluster load balancing are managed once rather than cluster by cluster.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "GKE Enterprise fleet management",
              "short_name": "Fleets",
              "doc_url": "https://cloud.google.com/kubernetes-engine/docs/fleets-overview",
              "one_line": "Group clusters across projects/regions/on-prem for policy, Config Sync, and multi-cluster services.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No fleet abstraction across OKE clusters."
        }
      }
    },
    {
      "key": "kubernetes-node-autoscaler",
      "domain": "containers",
      "title": "Kubernetes node autoscaler",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Karpenter",
              "short_name": "Karpenter",
              "doc_url": "https://karpenter.sh/docs/",
              "one_line": "Open-source node lifecycle manager provisioning right-sized EC2 nodes directly from unschedulable pods, then consolidating them away.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "elsewhere",
          "reason": "Node autoprovisioning in AKS is the peer capability and is Karpenter-based, but it is a mode of the cluster rather than a separate product.",
          "see": "managed-kubernetes"
        },
        "gcp": {
          "state": "elsewhere",
          "reason": "Node auto-provisioning and the cluster autoscaler are built into GKE, and Autopilot removes node management entirely.",
          "see": "managed-kubernetes"
        },
        "oci": {
          "state": "absent",
          "reason": "The cluster autoscaler add-on and virtual nodes cover node scaling; there is no just-in-time right-sized node provisioner."
        }
      }
    },
    {
      "key": "managed-kubernetes",
      "domain": "containers",
      "title": "Managed Kubernetes",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Elastic Kubernetes Service",
              "short_name": "EKS",
              "doc_url": "https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html",
              "one_line": "Managed upstream-Kubernetes control plane with curated add-ons, managed node groups, Fargate, Auto Mode, and hybrid nodes.",
              "status": "ga"
            },
            {
              "name": "Amazon EKS Auto Mode",
              "short_name": "EKS Auto Mode",
              "doc_url": "https://docs.aws.amazon.com/eks/latest/userguide/automode.html",
              "one_line": "Mode where AWS also operates the Kubernetes data plane: nodes, autoscaling (Karpenter-based), load balancing, DNS, storage, and network policy.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Kubernetes Service",
              "short_name": "AKS",
              "doc_url": "https://learn.microsoft.com/en-us/azure/aks/",
              "one_line": "Managed Kubernetes control plane with integrated Azure networking, identity, and upgrades.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Google Kubernetes Engine",
              "short_name": "GKE",
              "doc_url": "https://cloud.google.com/kubernetes-engine/docs/concepts/choose-cluster-mode",
              "one_line": "Managed Kubernetes with Autopilot (Google runs nodes) and Standard modes, regional control planes.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Container Engine for Kubernetes (OKE)",
              "short_name": "OKE",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contengcomparingenhancedwithbasicclusters_topic.htm",
              "one_line": "Managed Kubernetes with enhanced clusters (SLA-backed, virtual nodes, add-on management, workload identity) and free basic clusters.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "serverless-containers",
      "domain": "containers",
      "title": "Serverless containers",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Fargate",
              "short_name": "Fargate",
              "doc_url": "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html",
              "one_line": "Serverless per-task/pod container runtime shared by ECS and EKS, each workload in its own kernel-isolated environment.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Container Apps",
              "short_name": "Container Apps",
              "doc_url": "https://learn.microsoft.com/en-us/azure/container-apps/",
              "one_line": "Serverless container platform built on Kubernetes and KEDA with scale-to-zero and revision-based traffic splitting.",
              "status": "ga"
            },
            {
              "name": "Azure Container Instances",
              "short_name": "ACI",
              "doc_url": "https://learn.microsoft.com/en-us/azure/container-instances/",
              "one_line": "Per-container serverless compute without any orchestrator.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Run",
              "short_name": "Run",
              "doc_url": "https://cloud.google.com/run/docs/overview/what-is-cloud-run",
              "one_line": "Scale-to-zero container platform: services (HTTP), jobs (batch), worker pools, single instances.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Container Instances",
              "short_name": "Container Instances",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/container-instances/home.htm",
              "one_line": "Run single containers or small groups without managing servers, billed per second of OCPU/memory.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "service-mesh",
      "domain": "containers",
      "title": "Service mesh",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS App Mesh",
              "short_name": "App Mesh",
              "doc_url": "https://docs.aws.amazon.com/app-mesh/latest/userguide/what-is-app-mesh.html",
              "one_line": "Envoy-based service mesh; discontinued after Sept 30 2026 with migration paths to ECS Service Connect and VPC Lattice.",
              "status": "retiring"
            },
            {
              "name": "Amazon ECS Service Connect",
              "short_name": "Service Connect",
              "doc_url": "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-connect.html",
              "one_line": "ECS-native service discovery and traffic management using an AWS-managed proxy in each task; replaces App Mesh for ECS.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Istio add-on for AKS",
              "short_name": "Istio add-on",
              "doc_url": "https://learn.microsoft.com/en-us/azure/aks/istio-about",
              "one_line": "AKS-managed Istio mesh providing mTLS, traffic management, and L7 observability.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Service Mesh",
              "short_name": "CSM",
              "doc_url": "https://cloud.google.com/service-mesh/docs/overview",
              "one_line": "Managed Istio-derived service mesh for GKE/fleets (formerly Anthos Service Mesh).",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "OCI Service Mesh (retired)",
              "short_name": "Service Mesh",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/service-mesh/overview.htm",
              "one_line": "Formerly managed Istio-style mesh with mTLS, traffic splitting, telemetry.",
              "status": "deprecated"
            }
          ]
        }
      }
    },
    {
      "key": "functions-faas",
      "domain": "serverless-app",
      "title": "Functions (FaaS)",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Lambda",
              "short_name": "Lambda",
              "doc_url": "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html",
              "one_line": "Event-driven serverless functions billed per request and GB-second with no servers to manage.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Functions",
              "short_name": "Functions",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-functions/",
              "one_line": "Event-driven FaaS with triggers/bindings across HTTP, queues, timers, and 60+ event sources.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Run functions",
              "short_name": "CR functions",
              "doc_url": "https://cloud.google.com/functions/docs/concepts/overview",
              "one_line": "Event-driven functions (formerly Cloud Functions) built on Cloud Run infrastructure.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "OCI Functions",
              "short_name": "Functions",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Functions/Concepts/functionsoverview.htm",
              "one_line": "Fn Project based FaaS; pay per invocation, scales to zero.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "paas-web-runtime",
      "domain": "serverless-app",
      "title": "PaaS web runtime",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS App Runner",
              "short_name": "App Runner",
              "doc_url": "https://docs.aws.amazon.com/apprunner/latest/dg/apprunner-availability-change.html",
              "one_line": "Deploy source code or a container straight to an autoscaled managed web service; closed to new customers, successor is ECS Express Mode.",
              "status": "deprecated"
            },
            {
              "name": "AWS Elastic Beanstalk",
              "short_name": "Beanstalk",
              "doc_url": "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.platforms.html",
              "one_line": "Classic PaaS provisioning EC2-based environments per language platform with full underlying-resource control.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure App Service",
              "short_name": "App Service",
              "doc_url": "https://learn.microsoft.com/en-us/azure/app-service/",
              "one_line": "Fully managed web hosting for code and containers with deployment slots, TLS, and VNet integration.",
              "status": "ga"
            },
            {
              "name": "Azure Spring Apps",
              "short_name": "Spring Apps",
              "doc_url": "https://learn.microsoft.com/en-us/azure/spring-apps/",
              "one_line": "Managed Spring Boot hosting with app lifecycle, config server, and service discovery.",
              "status": "retiring"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "App Engine",
              "short_name": "AE",
              "doc_url": "https://cloud.google.com/appengine/docs/the-appengine-environments",
              "one_line": "Classic PaaS: Standard (gen2 runtimes, scale-to-zero) and Flexible environments.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Visual Builder and APEX Service",
              "short_name": "VB / APEX",
              "doc_url": "https://docs.oracle.com/en-us/iaas/visual-builder/index.html",
              "one_line": "Low-code web/mobile app hosting (Visual Builder) and low-code apps backed by Autonomous DB (APEX workload type).",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "static-site-hosting",
      "domain": "serverless-app",
      "title": "Static site hosting",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Amplify Hosting",
              "short_name": "Amplify Hosting",
              "doc_url": "https://docs.aws.amazon.com/amplify/latest/userguide/welcome.html",
              "one_line": "Git-driven hosting for static and SSR web apps on CloudFront-backed CDN with branch previews.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Static Web Apps",
              "short_name": "SWA",
              "doc_url": "https://learn.microsoft.com/en-us/azure/static-web-apps/",
              "one_line": "Global static site hosting from Git with integrated API functions and PR-preview environments.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Firebase Hosting",
              "short_name": "FB Hosting",
              "doc_url": "https://firebase.google.com/products/hosting",
              "one_line": "Global static + web-framework hosting with CDN, preview channels, custom domains.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Object Storage static hosting pattern",
              "short_name": "Static sites",
              "doc_url": "https://docs.oracle.com/en/learn/oci-api-gateway-web-hosting/index.html",
              "one_line": "Serve static sites from Object Storage behind API Gateway for custom domains and TLS.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "archive-storage",
      "domain": "storage",
      "title": "Archive storage",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "S3 Glacier Flexible Retrieval and Deep Archive",
              "short_name": "Glacier classes",
              "doc_url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/glacier-storage-classes.html",
              "one_line": "Archive storage classes inside S3 requiring restore before read: Flexible (1-5 min expedited to 12h bulk) and Deep Archive (12-48h, lowest cost).",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Archive access tier",
              "short_name": "Archive tier",
              "doc_url": "https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview",
              "one_line": "Coldest Blob Storage tier priced near tape with rehydration latency measured in hours.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Storage Archive class",
              "short_name": "Archive class",
              "doc_url": "https://cloud.google.com/storage/docs/storage-classes",
              "one_line": "Lowest-cost GCS class for >=365-day retention data within the same bucket API.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Archive Storage",
              "short_name": "Archive",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Archive/Concepts/archivestorageoverview.htm",
              "one_line": "Cold-tier object storage requiring explicit restore before read.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "block-storage",
      "domain": "storage",
      "title": "Block storage",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Elastic Block Store",
              "short_name": "EBS",
              "doc_url": "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volume-types.html",
              "one_line": "AZ-scoped SSD/HDD block volumes for EC2 with snapshots, provisioned IOPS, and multi-attach.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Managed Disks",
              "short_name": "Managed Disks",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types",
              "one_line": "Block volumes attached to VMs: Standard HDD/SSD, Premium SSD v1/v2, Ultra Disk.",
              "status": "ga"
            },
            {
              "name": "Azure Elastic SAN",
              "short_name": "Elastic SAN",
              "doc_url": "https://learn.microsoft.com/en-us/azure/storage/elastic-san/",
              "one_line": "Cloud-native SAN delivering iSCSI volumes from a provisioned capacity pool shared across VMs.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Persistent Disk",
              "short_name": "PD",
              "doc_url": "https://cloud.google.com/compute/docs/disks/persistent-disks",
              "one_line": "Durable block storage (zonal/regional, balanced/ssd/hdd/extreme), snapshot-able, bootable.",
              "status": "ga"
            },
            {
              "name": "Hyperdisk",
              "short_name": "Hyperdisk",
              "doc_url": "https://cloud.google.com/compute/docs/disks/hyperdisks",
              "one_line": "New-generation disaggregated block storage: independently provisioned IOPS/throughput (Balanced/HA/Extreme/ML/Throughput).",
              "status": "ga"
            },
            {
              "name": "Local SSD",
              "short_name": "Local SSD",
              "doc_url": "https://cloud.google.com/compute/docs/disks/local-ssd",
              "one_line": "Physically attached NVMe scratch storage - fastest IO, ephemeral, no durability.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Block Volume",
              "short_name": "Block Volume",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/blockvolumeperformance.htm",
              "one_line": "Durable block storage with elastic performance priced in VPUs per GB, attachable to VMs and bare metal.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "bulk-transfer-appliance",
      "domain": "storage",
      "title": "Bulk transfer appliance",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Snow Family",
              "short_name": "Snowball Edge",
              "doc_url": "https://docs.aws.amazon.com/snowball/latest/developer-guide/device-differences.html",
              "one_line": "Rugged offline petabyte-transfer and edge-compute appliances; closed to new customers, support ends Dec 31 2026.",
              "status": "retiring"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Data Box",
              "short_name": "Data Box",
              "doc_url": "https://learn.microsoft.com/en-us/azure/databox/",
              "one_line": "Family of rugged appliances (Disk 8 TB to Heavy ~800 TB usable) for offline bulk import/export.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Transfer Appliance",
              "short_name": "TA",
              "doc_url": "https://cloud.google.com/transfer-appliance/docs/4.0/overview",
              "one_line": "Shippable storage appliance for petabyte-scale offline ingestion to GCS.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Data Transfer Appliance and Disk",
              "short_name": "DTA / DT Disk",
              "doc_url": "https://blogs.oracle.com/cloud-infrastructure/post/introducing-oracle-cloud-infrastructure-data-transfer-appliance",
              "one_line": "Offline bulk import: Oracle-shipped 150 TB appliances or encrypted commodity disks uploaded into your bucket by Oracle.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "file-storage",
      "domain": "storage",
      "title": "File storage",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Elastic File System",
              "short_name": "EFS",
              "doc_url": "https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html",
              "one_line": "Elastic NFS file system with Elastic throughput mode, lifecycle tiering into IA/Archive classes, and One Zone option.",
              "status": "ga"
            },
            {
              "name": "Amazon FSx family",
              "short_name": "FSx",
              "doc_url": "https://aws.amazon.com/fsx/",
              "one_line": "Four managed third-party file engines: Lustre (HPC, up to 1000 GB/s, S3-linked), NetApp ONTAP, OpenZFS, and Windows File Server (SMB+AD).",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Files",
              "short_name": "Files",
              "doc_url": "https://learn.microsoft.com/en-us/azure/storage/files/",
              "one_line": "Managed SMB and NFS file shares with AD-domain join and premium solid-state tiers.",
              "status": "ga"
            },
            {
              "name": "Azure NetApp Files",
              "short_name": "ANF",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-netapp-files/",
              "one_line": "Enterprise-grade NFS/SMB file service with extreme performance tiers and cross-region replication.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Filestore",
              "short_name": "Filestore",
              "doc_url": "https://cloud.google.com/filestore/docs/overview",
              "one_line": "Managed NFS (Basic through High Scale tiers) for GKE and lift-and-shift file workloads.",
              "status": "ga"
            },
            {
              "name": "Google Cloud NetApp Volumes",
              "short_name": "GCNV",
              "doc_url": "https://cloud.google.com/netapp/volumes",
              "one_line": "Enterprise NFS/SMB volumes (NetApp ONTAP) named explicitly in the ACE exam guide.",
              "status": "ga"
            },
            {
              "name": "Managed Lustre",
              "short_name": "Lustre",
              "doc_url": "https://cloud.google.com/managed-lustre/docs/overview",
              "one_line": "Fully managed Lustre parallel FS optimized for AI/HPC training reads.",
              "status": "ga"
            },
            {
              "name": "Parallelstore",
              "short_name": "Parallelstore",
              "doc_url": "https://cloud.google.com/parallelstore/docs/overview",
              "one_line": "DAOS-based managed parallel file system for HPC/AI with very low latency.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "File Storage Service (FSS)",
              "short_name": "File Storage",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/File/home.htm",
              "one_line": "Fully managed NFSv3/NFSv4 file systems with snapshot, clone, and cross-region replication.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "hybrid-storage-gateway",
      "domain": "storage",
      "title": "Hybrid storage gateway",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Storage Gateway",
              "short_name": "Storage Gateway",
              "doc_url": "https://aws.amazon.com/storagegateway/",
              "one_line": "On-prem VM or EC2 appliance exposing S3-backed File (NFS/SMB), Tape, and Volume (iSCSI cached/stored) interfaces.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure File Sync",
              "short_name": "File Sync",
              "doc_url": "https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-introduction",
              "one_line": "Keeps Windows Server file servers in sync with Azure Files with cloud tiering of cold blocks.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "absent",
          "reason": "GCP ships no first-party storage gateway appliance. Nearest: Cloud Storage FUSE (mount buckets as filesystem) and Storage Transfer Service agents; partner gateways fill the rest."
        },
        "oci": {
          "state": "absent",
          "reason": "No first-party storage gateway. OCI Storage Gateway, the on-premises NFS appliance backed by Object Storage, is retired: Oracle's own documentation page for it now says only that the service is no longer available. On-premises access to Object Storage is left to the CLI, rclone, S3-compatible clients, or a partner appliance."
        }
      }
    },
    {
      "key": "object-storage",
      "domain": "storage",
      "title": "Object storage",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon S3",
              "short_name": "S3",
              "doc_url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html",
              "one_line": "Unlimited object storage with lifecycle-managed storage classes, 11-nines durability, versioning, Object Lock WORM, and replication.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Blob Storage",
              "short_name": "Blob Storage",
              "doc_url": "https://learn.microsoft.com/en-us/azure/storage/blobs/",
              "one_line": "REST object store for blocks and append data with hot/cool/cold/archive tiers and rich lifecycle rules.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Storage",
              "short_name": "GCS",
              "doc_url": "https://cloud.google.com/storage/docs/introduction",
              "one_line": "Multi-class object store: Standard/Nearline/Coldline/Archive, dual-region turbo replication, HNS folders.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Object Storage (Standard and Infrequent Access)",
              "short_name": "Object Storage",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Object/Concepts/understandingstoragetiers.htm",
              "one_line": "Regional, unbounded object storage with Standard (hot) and Infrequent Access tiers plus auto-tiering.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "object-storage-highperf",
      "domain": "storage",
      "title": "Object storage (high-performance)",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon S3 Express One Zone",
              "short_name": "S3 Express One Zone",
              "doc_url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-bucket-high-performance.html",
              "one_line": "Single-AZ directory-bucket class delivering consistent single-digit millisecond latency, up to 10x faster than S3 Standard.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "absent",
          "reason": "No single-zone high-performance object class. Premium block blob accounts are SSD-backed with single-digit millisecond first-byte latency and per-transaction pricing, but they stay regionally redundant, so they do not make the trade this capability describes: dropping cross-zone redundancy to buy consistently low latency."
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Rapid Bucket / Rapid storage class",
              "short_name": "Rapid",
              "doc_url": "https://cloud.google.com/storage/docs/rapid/rapid-bucket",
              "one_line": "Zonal high-performance object storage with HNS + streaming/appends for AI/analytics co-location.",
              "status": "preview"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No single-zone high-performance object tier. Object Storage is regional and replicated across availability or fault domains by default."
        }
      }
    },
    {
      "key": "object-storage-tables",
      "domain": "storage",
      "title": "Object storage (tables)",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon S3 Tables",
              "short_name": "S3 Tables",
              "doc_url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables.html",
              "one_line": "Table buckets storing Apache Iceberg tables natively with automatic compaction and Glue/Athena/Redshift integration.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "absent",
          "reason": "OneLake and the Fabric Lakehouse hold Delta tables with managed maintenance; Azure Storage itself has no table-aware bucket type. See data-lake."
        },
        "gcp": {
          "state": "absent",
          "reason": "Cloud Storage has no table-aware bucket type. BigLake managed Iceberg tables do give managed Iceberg storage with automatic optimisation, but the tables are created and maintained by BigQuery over ordinary buckets, so the storage service itself still holds table files as opaque objects. Recorded in the data-lake row."
        },
        "oci": {
          "state": "absent",
          "reason": "No table-aware object storage type. Iceberg tables sit as ordinary objects and are maintained by the query engine."
        }
      }
    },
    {
      "key": "change-data-capture",
      "domain": "databases",
      "title": "Change data capture",
      "cells": {
        "aws": {
          "state": "elsewhere",
          "reason": "Delivered as the ongoing-replication mode of Database Migration Service rather than as a separate product.",
          "see": "db-migration-service"
        },
        "azure": {
          "state": "elsewhere",
          "reason": "Delivered as the online mode of Database Migration Service plus Data Factory and Fabric change data capture. There is no standalone CDC product."
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Datastream",
              "short_name": "Datastream",
              "doc_url": "https://cloud.google.com/datastream/docs/overview",
              "one_line": "Serverless CDC from Oracle/MySQL/PostgreSQL/SQL Server into BigQuery, Cloud SQL, Spanner.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "GoldenGate (OCI GoldenGate)",
              "short_name": "GoldenGate",
              "doc_url": "https://docs.oracle.com/en/cloud/paas/goldengate-service/index.html",
              "one_line": "Managed real-time CDC replication platform for heterogeneous databases and streaming into big-data targets.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "database-fleet-management",
      "domain": "databases",
      "title": "Database fleet management",
      "cells": {
        "aws": {
          "state": "absent",
          "reason": "No fleet-wide database health console. Per-engine views live in the RDS console, with CloudWatch and Performance Insights covering the metrics side."
        },
        "azure": {
          "state": "absent",
          "reason": "No fleet-wide console covering every database engine. SQL-family estates are viewed through Azure Monitor and SQL Insights."
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Database Center",
              "short_name": "DB Center",
              "doc_url": "https://cloud.google.com/database-center/docs/overview",
              "one_line": "Fleet-level console for database health, security, cost, and reliability insights.",
              "status": "preview"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Database Management",
              "short_name": "DB Management",
              "doc_url": "https://docs.oracle.com/en-us/iaas/database-management/home.htm",
              "one_line": "Fleet-wide console for Oracle databases showing health, performance, storage, and configuration across the estate rather than one database at a time.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "db-migration-service",
      "domain": "databases",
      "title": "Database migration service",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Database Migration Service",
              "short_name": "DMS",
              "doc_url": "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Introduction.html",
              "one_line": "Managed heterogeneous/homogeneous database migration with continuous CDC replication between any source-target pair where one side is AWS.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Database Migration Service",
              "short_name": "DMS",
              "doc_url": "https://learn.microsoft.com/en-us/azure/dms/",
              "one_line": "Guided online/offline migration of databases into Azure SQL/MySQL/PostgreSQL/Cosmos.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Database Migration Service",
              "short_name": "DMS",
              "doc_url": "https://cloud.google.com/database-migration/docs",
              "one_line": "Serverless homogeneous migrations (MySQL/Postgres/SQL Server) into Cloud SQL/AlloyDB with continuous CDC.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Database Migration service",
              "short_name": "DB Migration",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/database-migration/home.htm",
              "one_line": "Assessment, schema conversion guidance, and online/offline migration of Oracle and non-Oracle databases into OCI using Data Pump, GoldenGate, or Zero-Downtime Migration.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "globally-distributed-sql",
      "domain": "databases",
      "title": "Globally distributed SQL",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Aurora DSQL",
              "short_name": "Aurora DSQL",
              "doc_url": "https://docs.aws.amazon.com/aurora-dsql/latest/userguide/what-is-aurora-dsql.html",
              "one_line": "Serverless PostgreSQL-compatible distributed SQL with an active-active design and strongly consistent multi-region writes.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "absent",
          "reason": "No globally consistent relational engine. Cosmos DB is globally distributed but offers tunable consistency over a NoSQL model rather than one strongly consistent SQL image."
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Spanner",
              "short_name": "Spanner",
              "doc_url": "https://cloud.google.com/spanner/docs/overview",
              "one_line": "Globally consistent relational DB with TrueTime ordering, multi-region configs, processing-unit billing.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Globally Distributed Autonomous Database",
              "short_name": "Distributed ADB",
              "doc_url": "https://docs.oracle.com/en/cloud/paas/globally-distributed-autonomous-database/user/overview-distributed-adb1.html",
              "one_line": "Autonomous Database sharded across availability domains or regions, presenting one logical database while each shard holds its own subset of the data.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "graph-database",
      "domain": "databases",
      "title": "Graph database",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Neptune",
              "short_name": "Neptune",
              "doc_url": "https://docs.aws.amazon.com/neptune/latest/userguide/intro.html",
              "one_line": "Property-graph database supporting Gremlin, openCypher, and SPARQL, with Neptune Analytics for in-memory algorithms and vector search.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Graph in Microsoft Fabric",
              "short_name": "Fabric Graph",
              "doc_url": "https://learn.microsoft.com/en-us/fabric/graph/overview",
              "one_line": "Scale-out labeled-property-graph engine over OneLake with GQL (ISO/IEC 39075) querying; generally available June 2026.",
              "status": "ga"
            },
            {
              "name": "Azure Cosmos DB for Apache Gremlin",
              "short_name": "Cosmos Gremlin",
              "doc_url": "https://learn.microsoft.com/en-us/azure/cosmos-db/gremlin/overview",
              "one_line": "Fully managed Apache TinkerPop/Gremlin graph database service inside Azure Cosmos DB.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Spanner Graph",
              "short_name": "Graph",
              "doc_url": "https://cloud.google.com/spanner/docs/graph",
              "one_line": "Property-graph capability on Spanner with GQL queries over the same global infrastructure.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Property Graph (Graph Studio in Autonomous DB)",
              "short_name": "Graph Studio",
              "doc_url": "https://docs.oracle.com/en/cloud/paas/autonomous-database/serverless/adbsb/graph-autonomous-database.html",
              "one_line": "In-database property graph model with PGQL queries and notebooks inside Autonomous Database.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "in-memory-cache",
      "domain": "databases",
      "title": "In-memory cache",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon ElastiCache",
              "short_name": "ElastiCache",
              "doc_url": "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html",
              "one_line": "Managed Valkey, Redis OSS, and Memcached caches in serverless or node form.",
              "status": "ga"
            },
            {
              "name": "Amazon MemoryDB",
              "short_name": "MemoryDB",
              "doc_url": "https://docs.aws.amazon.com/memorydb/latest/devguide/what-is-memorydb.html",
              "one_line": "Redis OSS and Valkey compatible durable primary database persisting every write to a Multi-AZ transactional log.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Managed Redis",
              "short_name": "AMR",
              "doc_url": "https://learn.microsoft.com/en-us/azure/redis/",
              "one_line": "Current-generation managed Redis service (Redis Enterprise engines) succeeding Azure Cache for Redis.",
              "status": "ga"
            },
            {
              "name": "Azure Cache for Redis",
              "short_name": "Cache for Redis",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-overview",
              "one_line": "Legacy managed Redis (OSS Redis engines; Enterprise tiers on Redis Inc. software) retiring on fixed dates - migrate instances to Azure Managed Redis.",
              "status": "retiring"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Memorystore (Redis, Redis Cluster, Valkey, Memcached)",
              "short_name": "Memorystore",
              "doc_url": "https://cloud.google.com/memorystore/docs/redis/redis-overview",
              "one_line": "Managed in-memory caches across four engines with different feature envelopes.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "OCI Cache (Valkey and Redis)",
              "short_name": "OCI Cache",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/ocicache/home.htm",
              "one_line": "Fully managed Valkey/Redis v7-compatible cache clusters with sharded or non-sharded topologies.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "ledger",
      "domain": "databases",
      "title": "Ledger",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon QLDB",
              "short_name": "QLDB",
              "doc_url": "https://docs.aws.amazon.com/general/latest/gr/full_shutdown_services.html",
              "one_line": "Cryptographically verifiable ledger database; fully shut down July 31 2025 with migration path to Aurora PostgreSQL.",
              "status": "deprecated"
            },
            {
              "name": "Amazon Managed Blockchain",
              "short_name": "Managed Blockchain",
              "doc_url": "https://aws.amazon.com/managed-blockchain/",
              "one_line": "Managed Ethereum, Polygon, Bitcoin, and Hyperledger Fabric networks - multi-party permissioned ledgers rather than a single-owner verifiable journal.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure confidential ledger",
              "short_name": "Confidential Ledger",
              "doc_url": "https://learn.microsoft.com/en-us/azure/confidential-ledger/overview",
              "one_line": "Tamper-evident append-only store running inside hardware enclaves, returning a cryptographic receipt for every write.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "absent",
          "reason": "No managed ledger/QSQL-style product. Nearest: Bucket Lock/Object Retention Lock immutability plus Spanner for transactional history."
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Oracle Blockchain Platform",
              "short_name": "Blockchain Platform",
              "doc_url": "https://docs.oracle.com/en/cloud/paas/blockchain-cloud/index.html",
              "one_line": "Managed Hyperledger Fabric network for multi-party permissioned ledgers, with membership, ordering, and smart contracts run by Oracle.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "nosql-document",
      "domain": "databases",
      "title": "NoSQL document",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon DocumentDB (with MongoDB compatibility)",
              "short_name": "DocumentDB",
              "doc_url": "https://aws.amazon.com/documentdb/faqs/",
              "one_line": "MongoDB-API-compatible document database on Aurora-style distributed storage with elastic clusters scaling to 4 PiB.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Cosmos DB for MongoDB (vCore)",
              "short_name": "Mongo vCore",
              "doc_url": "https://learn.microsoft.com/en-us/azure/documentdb/overview",
              "one_line": "MongoDB-compatible document service running vCore clusters with full driver compatibility.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Firestore",
              "short_name": "Firestore",
              "doc_url": "https://cloud.google.com/firestore/docs",
              "one_line": "Serverless document DB in Native mode (live sync, offline) or Datastore mode; MongoDB-compatible interface layer.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Autonomous JSON Database",
              "short_name": "JSON DB",
              "doc_url": "https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/autonomous-database-billing-overview.html",
              "one_line": "Document-model Autonomous Database (JSON workload type) with MongoDB-driver compatible Oracle Database API.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "nosql-keyvalue",
      "domain": "databases",
      "title": "NoSQL key-value",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon DynamoDB",
              "short_name": "DynamoDB",
              "doc_url": "https://aws.amazon.com/dynamodb/",
              "one_line": "Serverless multi-active key-value and document store with single-digit millisecond latency at any scale.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Cosmos DB for NoSQL",
              "short_name": "Cosmos DB",
              "doc_url": "https://learn.microsoft.com/en-us/azure/cosmos-db/",
              "one_line": "Globally distributed multi-model NoSQL with guaranteed single-digit-ms read latency and RU/s pricing.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Bigtable",
              "short_name": "Bigtable",
              "doc_url": "https://cloud.google.com/bigtable/docs/overview",
              "one_line": "Wide-column NoSQL at petabyte scale - also Google's documented time-series pattern.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "NoSQL Database Cloud",
              "short_name": "NoSQL",
              "doc_url": "https://docs.oracle.com/en/cloud/paas/nosql-cloud/",
              "one_line": "Serverless key-value/fixed-schema tables with predictable single-digit millisecond latency and active-active regional tables.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "relational-managed",
      "domain": "databases",
      "title": "Relational (managed)",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Relational Database Service",
              "short_name": "RDS",
              "doc_url": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.html",
              "one_line": "Managed MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, and Db2 with Multi-AZ HA, automated backups, and gp3 storage.",
              "status": "ga"
            },
            {
              "name": "Amazon Aurora",
              "short_name": "Aurora",
              "doc_url": "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html",
              "one_line": "MySQL and PostgreSQL compatible clustered database with distributed fault-tolerant storage, up to 15 readers, and Global Database.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure SQL Database",
              "short_name": "SQL DB",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-sql/database/sql-database-paas-overview",
              "one_line": "Managed PaaS SQL Server database engine with vCore/DTU purchasing and built-in HA.",
              "status": "ga"
            },
            {
              "name": "Azure Database for PostgreSQL Flexible Server",
              "short_name": "PG Flexible",
              "doc_url": "https://learn.microsoft.com/en-us/azure/postgresql/",
              "one_line": "Community PostgreSQL with tunable maintenance, zone-redundant HA, and read replicas.",
              "status": "ga"
            },
            {
              "name": "Azure Database for MySQL Flexible Server",
              "short_name": "MySQL Flexible",
              "doc_url": "https://learn.microsoft.com/en-us/azure/mysql/",
              "one_line": "Community MySQL with HA options and read replicas.",
              "status": "ga"
            },
            {
              "name": "Azure SQL Managed Instance",
              "short_name": "SQL MI",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-sql/managed-instance/sql-managed-instance-paas-overview",
              "one_line": "Near-complete SQL Server engine (SQL Agent, cross-db queries, CLR) deployed inside your own VNet.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud SQL",
              "short_name": "Cloud SQL",
              "doc_url": "https://cloud.google.com/sql/docs/introduction",
              "one_line": "Managed MySQL, PostgreSQL, and SQL Server with HA pairs and read replicas.",
              "status": "ga"
            },
            {
              "name": "AlloyDB for PostgreSQL",
              "short_name": "AlloyDB",
              "doc_url": "https://cloud.google.com/alloydb/docs/overview",
              "one_line": "PostgreSQL-compatible engine with built-in columnar acceleration for HTAP and AI workloads.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Base Database Service / Exadata Database Service",
              "short_name": "Base DB / ExaDB",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Database/home.htm",
              "one_line": "Customer-managed Oracle Database on VM or bare metal DB systems, including Exadata infrastructure options.",
              "status": "ga"
            },
            {
              "name": "MySQL HeatWave",
              "short_name": "HeatWave",
              "doc_url": "https://docs.oracle.com/en-us/iaas/mysql-database/home.htm",
              "one_line": "Fully managed MySQL Enterprise Edition with an in-memory HeatWave accelerator for analytics, ML, GenAI, and Lakehouse queries over Object Storage.",
              "status": "ga"
            },
            {
              "name": "OCI Database with PostgreSQL",
              "short_name": "PostgreSQL",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/postgresql/home.htm",
              "one_line": "Fully managed community PostgreSQL with pluggable engine and monitor.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "relational-serverless",
      "domain": "databases",
      "title": "Relational (serverless)",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Aurora Serverless v2",
              "short_name": "Aurora Serverless v2",
              "doc_url": "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.html",
              "one_line": "Aurora capacity configuration scaling in 0.5 ACU increments within min/max bounds, including pause-to-zero auto-pause when idle.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure SQL Database serverless tier",
              "short_name": "SQL serverless",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-sql/database/serverless-tier-overview",
              "one_line": "Compute tier that auto-scales between min/max vCores and pauses to zero when idle.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "absent",
          "reason": "No true serverless relational database SKU. Nearest things: Spanner bills in processing units (elastic but provisioned), AlloyDB read-pool autoscaling floors at 1 node and is Preview, Cloud SQL Enterprise Plus autoscales read pools. None scale to zero."
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Autonomous Transaction Processing (serverless)",
              "short_name": "ATP",
              "doc_url": "https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/autonomous-database-billing-overview.html",
              "one_line": "Self-driving Oracle Database for mixed transactional workloads, ECPU-billed, instant scaling, no administration.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "timeseries-database",
      "domain": "databases",
      "title": "Time-series database",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Timestream",
              "short_name": "Timestream",
              "doc_url": "https://docs.aws.amazon.com/timestream/latest/developerguide/what-it-is.html",
              "one_line": "Time-series family: serverless Timestream for LiveAnalytics and managed-instance Timestream for InfluxDB.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Data Explorer (Kusto)",
              "short_name": "ADX/Kusto",
              "doc_url": "https://learn.microsoft.com/en-us/azure/data-explorer/",
              "one_line": "Fast columnar analytics engine for telemetry and time-series with KQL as its query language.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "absent",
          "reason": "No dedicated managed time-series product. Google's documented pattern is Bigtable for time series; Monitoring's own TSDB is internal-only. The obvious counter-example, Timeseries Insights API, is retired - its docs URL now returns HTTP 404. Recorded as a gap rather than stretching nosql-keyvalue."
        },
        "oci": {
          "state": "absent",
          "reason": "No managed time-series database service. Nearest things: the Monitoring metrics store for platform telemetry, and Telemetry Streaming (a time-series database feature built on Oracle AI Database 26ai) for self-managed metric workloads; neither is a managed multi-model TSDB like AWS Timestream."
        }
      }
    },
    {
      "key": "bi-dashboards",
      "domain": "analytics",
      "title": "BI dashboards",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon QuickSight (Quick Sight)",
              "short_name": "QuickSight",
              "doc_url": "https://docs.aws.amazon.com/quicksight/latest/user/welcome.html",
              "one_line": "Serverless BI with SPICE in-memory engine, embedded dashboards, and natural-language Q questions.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Power BI (incl. Embedded)",
              "short_name": "Power BI",
              "doc_url": "https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-what-is-desktop",
              "one_line": "Enterprise BI service with paginated reports, dashboards, and an embedding SDK for ISVs.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Looker",
              "short_name": "Looker",
              "doc_url": "https://cloud.google.com/looker/docs",
              "one_line": "Governed BI platform with LookML modeling layer over warehouses.",
              "status": "ga"
            },
            {
              "name": "Looker Studio (+ Pro)",
              "short_name": "Studio",
              "doc_url": "https://cloud.google.com/looker-studio",
              "one_line": "Free self-serve dashboards/reports connecting to BQ and 800+ sources.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Oracle Analytics Cloud",
              "short_name": "OAC",
              "doc_url": "https://docs.oracle.com/en/cloud/paas/analytics-cloud/index.html",
              "one_line": "Enterprise BI platform: semantic models, dashboards, self-service visualization, natural-language Q&A.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "clean-rooms",
      "domain": "analytics",
      "title": "Clean rooms",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Clean Rooms",
              "short_name": "Clean Rooms",
              "doc_url": "https://docs.aws.amazon.com/clean-rooms/latest/userguide/what-is.html",
              "one_line": "Multi-party data collaboration with analysis rules, differential privacy, and cryptographic computing without moving raw data.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Confidential Clean Rooms",
              "short_name": "Clean Rooms",
              "doc_url": "https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-clean-rooms",
              "one_line": "Protected environment where several parties analyse combined sensitive datasets without exposing their raw rows to each other or to the operator.",
              "status": "preview"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "BigQuery data clean rooms",
              "short_name": "Data clean rooms",
              "doc_url": "https://cloud.google.com/bigquery/docs/data-clean-rooms",
              "one_line": "Analytics Hub listings that let several parties query joined data under privacy policies, without any party reading the other's rows.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No multi-party clean room service."
        }
      }
    },
    {
      "key": "data-catalog",
      "domain": "analytics",
      "title": "Data catalog",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Glue Data Catalog",
              "short_name": "Glue Data Catalog",
              "doc_url": "https://aws.amazon.com/glue/",
              "one_line": "Central Hive-compatible metadata catalog consumed by Athena, Redshift Spectrum, EMR, Glue ETL, and Lake Formation permissions.",
              "status": "ga"
            },
            {
              "name": "Amazon DataZone",
              "short_name": "DataZone",
              "doc_url": "https://docs.aws.amazon.com/datazone/latest/userguide/what-is-datazone.html",
              "one_line": "Business data catalog and subscription portal publishing Glue/Redshift assets with approval workflows.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Microsoft Purview Unified Catalog",
              "short_name": "Purview UC",
              "doc_url": "https://learn.microsoft.com/en-us/purview/purview",
              "one_line": "Data map, scanning, classification, lineage, and glossary across Azure and external estates.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Knowledge Catalog (ex-Dataplex Universal Catalog)",
              "short_name": "KC",
              "doc_url": "https://cloud.google.com/dataplex/docs/introduction",
              "one_line": "Data catalog/lakehouse governance: zones, assets, business glossary, lineage, policy tags driving BQ column security.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Data Catalog",
              "short_name": "Data Catalog",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/data-catalog/home.htm",
              "one_line": "Metadata catalog with technical/business/operational metadata and Hive-metastore API for Spark engines.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "data-lake",
      "domain": "analytics",
      "title": "Data lake",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Lake Formation (on Amazon S3)",
              "short_name": "Lake Formation",
              "doc_url": "https://aws.amazon.com/lake-formation/",
              "one_line": "Governance layer over the S3 data lake providing database-grant-style fine-grained permissions, tag-based access control, and cross-account sharing.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Data Lake Storage Gen2",
              "short_name": "ADLS Gen2",
              "doc_url": "https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction",
              "one_line": "Hierarchical-namespace overlay on Blob Storage enabling POSIX-style ACLs for lake workloads.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "BigLake / lakehouse on Cloud Storage",
              "short_name": "BigLake",
              "doc_url": "https://cloud.google.com/bigquery/docs/biglake-intro",
              "one_line": "Open-format lakehouse: external tables (Iceberg/Delta/Parquet) governed via BigQuery engines.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Object Storage data lake pattern",
              "short_name": "Data lake",
              "doc_url": "https://docs.oracle.com/en/solutions/data-platform-lakehouse/index.html",
              "one_line": "Open-table-format lakehouse directly on Object Storage queried by Autonomous AI Lakehouse, Data Flow Spark, or external engines.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "data-warehouse",
      "domain": "analytics",
      "title": "Data warehouse",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Redshift",
              "short_name": "Redshift",
              "doc_url": "https://aws.amazon.com/redshift/",
              "one_line": "Petabyte cloud data warehouse with RA3/Graviton RG nodes, Serverless RPU model, concurrency scaling, Spectrum, and zero-ETL integrations.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Microsoft Fabric Warehouse / Synapse dedicated SQL pools",
              "short_name": "Fabric DW",
              "doc_url": "https://learn.microsoft.com/en-us/fabric/data-warehouse/",
              "one_line": "Cloud data warehouse spanning Fabric Lakehouse/Warehouse and the legacy Synapse dedicated pools.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "BigQuery",
              "short_name": "BQ",
              "doc_url": "https://cloud.google.com/bigquery/docs/introduction",
              "one_line": "Serverless warehouse+lakehouse: separated storage/compute, SQL, streaming inserts, ML/AI built in.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Autonomous AI Lakehouse (Autonomous Data Warehouse)",
              "short_name": "ADW / Lakehouse",
              "doc_url": "https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/autonomous-database-billing-overview.html",
              "one_line": "Self-driving analytical warehouse on shared Exadata, renamed to Lakehouse workload with Iceberg support.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "etl-service",
      "domain": "analytics",
      "title": "ETL service",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Glue",
              "short_name": "Glue",
              "doc_url": "https://aws.amazon.com/glue/",
              "one_line": "Serverless Spark ETL with visual studio, crawlers, Schema Registry, Real-Time Mode, and generative-AI authoring assist.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Data Factory",
              "short_name": "ADF",
              "doc_url": "https://learn.microsoft.com/en-us/azure/data-factory/",
              "one_line": "Serverless orchestrated ETL/ELT with 90+ connectors, mapping data flows, and SSIS lift-and-shift.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Dataflow",
              "short_name": "Dataflow",
              "doc_url": "https://cloud.google.com/dataflow/docs/guides",
              "one_line": "Apache Beam batch+stream pipelines as a managed serverless service (windowing, exactly-once).",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Data Integration",
              "short_name": "Data Integration",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/data-integration/home.htm",
              "one_line": "Serverless visual ETL/ELT designer with schema-drift protection and SQL pushdown to Oracle targets.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "managed-search",
      "domain": "analytics",
      "title": "Managed search",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon OpenSearch Service",
              "short_name": "OpenSearch Service",
              "doc_url": "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html",
              "one_line": "Managed OpenSearch domains and Serverless collections (search, time-series, vector) with UltraWarm and cold tiers.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure AI Search",
              "short_name": "AI Search",
              "doc_url": "https://learn.microsoft.com/en-us/azure/search/",
              "one_line": "Managed search index with lexical, vector, and hybrid retrieval plus semantic ranking.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Vertex AI Search (now Agent Search)",
              "short_name": "VAIS",
              "doc_url": "https://cloud.google.com/generative-ai-app-builder/docs/introduction",
              "one_line": "Google-quality enterprise search/RAG grounding over sites, documents, retail catalogs.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Search with OpenSearch",
              "short_name": "OpenSearch",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/search-opensearch/home.htm",
              "one_line": "Managed OpenSearch clusters with OpenSearch Dashboards for full-text search and log analytics.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "managed-spark",
      "domain": "analytics",
      "title": "Managed Spark",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon EMR",
              "short_name": "EMR",
              "doc_url": "https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-overview.html",
              "one_line": "Managed Hadoop/Spark/Hive platform on EC2, EKS, and EMR Serverless for big-data processing.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Databricks / Fabric Spark runtime",
              "short_name": "Databricks",
              "doc_url": "https://learn.microsoft.com/en-us/azure/databricks/",
              "one_line": "Managed Apache Spark offered through Azure Databricks and the native Fabric Spark runtime.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Dataproc",
              "short_name": "Dataproc",
              "doc_url": "https://cloud.google.com/dataproc/docs/concepts/overview",
              "one_line": "Fast ephemeral Hadoop/Spark clusters on CE with Spot workers and autoscaling.",
              "status": "ga"
            },
            {
              "name": "Managed Service for Apache Spark",
              "short_name": "Spark serverless",
              "doc_url": "https://cloud.google.com/products/managed-service-for-apache-spark",
              "one_line": "Zero-ops serverless Spark batches/sessions (formerly Dataproc Serverless), Lightning-accelerated.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Data Flow (serverless Spark)",
              "short_name": "Data Flow",
              "doc_url": "https://www.oracle.com/big-data/data-flow/",
              "one_line": "Run Apache Spark and Spark Streaming applications with no cluster to manage, paying per second of execution.",
              "status": "ga"
            },
            {
              "name": "Big Data Service",
              "short_name": "Big Data",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/bigdata/home.htm",
              "one_line": "Persistent Hadoop/Spark/Trino/Flink clusters with Kerberos security and autoscaling.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "serverless-query-engine",
      "domain": "analytics",
      "title": "Serverless query engine",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Athena",
              "short_name": "Athena",
              "doc_url": "https://docs.aws.amazon.com/athena/latest/ug/what-is.html",
              "one_line": "Serverless interactive SQL (and Spark) queried directly against S3, with federated connectors to other stores; the standard query engine for S3-delivered telemetry streams.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Synapse serverless SQL pool",
              "short_name": "Serverless SQL",
              "doc_url": "https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/on-demand-workspace-overview",
              "one_line": "T-SQL run directly over files in the data lake with no cluster to provision, billed per terabyte of data processed.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "elsewhere",
          "reason": "Delivered by BigQuery itself, which is serverless and bills per byte scanned over both managed storage and external lake tables.",
          "see": "data-warehouse"
        },
        "oci": {
          "state": "elsewhere",
          "reason": "Delivered by Autonomous AI Lakehouse external tables and Data Flow SQL over Object Storage, rather than as a standalone per-query engine."
        }
      }
    },
    {
      "key": "stream-analytics",
      "domain": "analytics",
      "title": "Stream analytics",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Managed Service for Apache Flink",
              "short_name": "Managed Flink",
              "doc_url": "https://docs.aws.amazon.com/managed-flink/latest/java/what-is.html",
              "one_line": "Managed Apache Flink for stateful stream processing: windowed SQL, the DataStream and Table APIs, checkpointed state, and exactly-once sinks.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Stream Analytics",
              "short_name": "ASA",
              "doc_url": "https://learn.microsoft.com/en-us/azure/stream-analytics/",
              "one_line": "SQL-subset streaming processor with windowing, reference joins, and anomaly detection functions.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "elsewhere",
          "reason": "Delivered by Dataflow, whose Apache Beam pipelines carry windowing, triggers, and exactly-once semantics over unbounded sources.",
          "see": "etl-service"
        },
        "oci": {
          "state": "elsewhere",
          "reason": "Delivered by Data Flow Spark Streaming and GoldenGate Stream Analytics rather than as a dedicated streaming SQL product.",
          "see": "managed-spark"
        }
      }
    },
    {
      "key": "stream-ingest",
      "domain": "analytics",
      "title": "Stream ingest",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Kinesis Data Streams",
              "short_name": "Kinesis Data Streams",
              "doc_url": "https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html",
              "one_line": "Shard-based real-time record streaming with provisioned and on-demand capacity and retention from 24 hours to 365 days.",
              "status": "ga"
            },
            {
              "name": "Amazon Managed Streaming for Apache Kafka",
              "short_name": "MSK",
              "doc_url": "https://aws.amazon.com/msk/",
              "one_line": "Managed Kafka clusters (Provisioned with Express brokers or Serverless) with IAM auth and Glue Schema Registry integration.",
              "status": "ga"
            },
            {
              "name": "Amazon Data Firehose",
              "short_name": "Firehose",
              "doc_url": "https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html",
              "one_line": "Fully managed delivery stream loading streaming data into S3, Redshift, OpenSearch, Iceberg tables, Splunk, Snowflake, and HTTP endpoints.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Event Hubs",
              "short_name": "Event Hubs",
              "doc_url": "https://learn.microsoft.com/en-us/azure/event-hubs/",
              "one_line": "High-throughput event ingestion platform with Kafka protocol endpoint and Capture to blob.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Managed Service for Apache Kafka",
              "short_name": "MSK-GCP",
              "doc_url": "https://cloud.google.com/managed-kafka/docs/overview",
              "one_line": "Kafka-protocol managed clusters (topic/ACL APIs) for event streaming and Kafka ecosystem lift-in.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Streaming (classic, Kafka-compatible)",
              "short_name": "Streaming",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Streaming/Concepts/streamingoverview.htm",
              "one_line": "Serverless Apache-Kafka-compatible event log with partitions and 7-day replay.",
              "status": "ga"
            },
            {
              "name": "Streaming with Apache Kafka (managed clusters)",
              "short_name": "Kafka service",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/kafka/overview.htm",
              "one_line": "Fully managed Kafka clusters, 100% Kafka-API compatible, no partition ceiling, 99.9% SLA.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "bgp-dynamic-routing",
      "domain": "networking-core",
      "title": "BGP dynamic routing",
      "cells": {
        "aws": {
          "state": "elsewhere",
          "reason": "The BGP speaker is embedded in the virtual private gateway, the Direct Connect gateway, and Transit Gateway rather than exposed as its own resource."
        },
        "azure": {
          "state": "elsewhere",
          "reason": "The BGP speaker is embedded in the VPN Gateway and the ExpressRoute gateway rather than exposed as its own resource."
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Router",
              "short_name": "Router",
              "doc_url": "https://cloud.google.com/network-connectivity/docs/router/concepts/overview",
              "one_line": "BGP speaker exchanging dynamic routes with VPN tunnels and Interconnect VLAN attachments.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "elsewhere",
          "reason": "The BGP speaker is embedded in the Dynamic Routing Gateway rather than exposed as its own resource."
        }
      }
    },
    {
      "key": "ip-address-management",
      "domain": "networking-core",
      "title": "IP address management",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon VPC IP Address Manager (IPAM)",
              "short_name": "VPC IPAM",
              "doc_url": "https://docs.aws.amazon.com/vpc/latest/ipam/what-it-is-ipam.html",
              "one_line": "Plans, tracks, and monitors public and private IP space with scopes, pools, and allocations, integrated with AWS Organizations for company-wide management.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Virtual Network Manager IP address management",
              "short_name": "AVNM IPAM",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-network-manager/concept-ip-address-management",
              "one_line": "Central address pools that plan CIDR space, allocate non-overlapping ranges to Azure resources automatically, and report utilisation across the estate.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "absent",
          "reason": "The internal ranges API reserves and tracks address space, but there is no org-wide address plan with pools, scopes, and utilisation reporting."
        },
        "oci": {
          "state": "absent",
          "reason": "No address management service. CIDR planning is done by hand per VCN."
        }
      }
    },
    {
      "key": "nat-gateway",
      "domain": "networking-core",
      "title": "NAT gateway",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "NAT Gateway",
              "short_name": "NAT GW",
              "doc_url": "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html",
              "one_line": "AZ-scoped managed NAT giving private subnets outbound-only internet access, scaling from 5 Gbps baseline toward 100 Gbps.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure NAT Gateway",
              "short_name": "NAT GW",
              "doc_url": "https://learn.microsoft.com/en-us/azure/nat-gateway/nat-overview",
              "one_line": "Zone-scoped managed SNAT service giving outbound internet egress predictable public IPs.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud NAT",
              "short_name": "NAT",
              "doc_url": "https://cloud.google.com/nat/docs/overview",
              "one_line": "Regional managed egress NAT giving private VMs/serverless outbound internet without inbound exposure.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "NAT Gateway",
              "short_name": "NAT GW",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/NATgateway.htm",
              "one_line": "Highly available outbound-only internet access for private subnets.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "network-interface",
      "domain": "networking-core",
      "title": "Network interface",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Elastic Network Interface",
              "short_name": "ENI",
              "doc_url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html",
              "one_line": "Virtual NIC carrying IPs, security groups, and MAC that follows attach/detach cycles within its AZ.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Network Interface (NIC)",
              "short_name": "NIC",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-network-interface",
              "one_line": "Per-VM virtual adapter carrying IP configs, NSGs, and the unit where flow/effective-rule views live.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Network interfaces (NICs) & alias IPs",
              "short_name": "NICs",
              "doc_url": "https://cloud.google.com/compute/docs/instances/create-instance-multiple-nics",
              "one_line": "Per-VM NICs bound one-to-one to subnets; multiple NICs per VM; alias CIDR blocks on a NIC.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Virtual Network Interface Cards (VNICs)",
              "short_name": "VNIC",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/managingVNICs.htm",
              "one_line": "Per-instance NICs with private/public IPs; bandwidth and count scale with shape.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "network-manager",
      "domain": "networking-core",
      "title": "Network manager",
      "cells": {
        "aws": {
          "state": "absent",
          "reason": "No central multi-network management plane. Cloud WAN policy documents carry topology and segmentation for the WAN, and Firewall Manager pushes security rules across accounts, but neither manages VPC topology as a whole. See transit-hub."
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Virtual Network Manager",
              "short_name": "AVNM",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-network-manager/overview",
              "one_line": "Central management of connectivity topologies (mesh/hub-spoke) and security admin rules across many VNets.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "absent",
          "reason": "No central multi-network management plane. Shared VPC centralises ownership and hierarchical firewall policies push rules from the organisation and folder levels."
        },
        "oci": {
          "state": "absent",
          "reason": "No central multi-network management plane. Compartments and the Dynamic Routing Gateway carry central control instead."
        }
      }
    },
    {
      "key": "network-peering",
      "domain": "networking-core",
      "title": "Network peering",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "VPC Peering",
              "short_name": "Peering",
              "doc_url": "https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-basics.html",
              "one_line": "One-to-one private connection between two VPCs across accounts and Regions; strictly non-transitive with no overlapping CIDRs.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Virtual network peering",
              "short_name": "Peering",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview",
              "one_line": "Direct non-transitive private connectivity between VNets, regional or global.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "VPC Network Peering",
              "short_name": "Peering",
              "doc_url": "https://cloud.google.com/vpc/docs/vpc-peering",
              "one_line": "Private non-transitive connectivity between VPCs across projects/orgs.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Local and Remote VCN Peering",
              "short_name": "Peering",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/localVCNpeering.htm",
              "one_line": "Private IP connectivity between VCNs in one region (LPG) or across regions (Remote Peering Connection on DRG).",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "private-endpoint",
      "domain": "networking-core",
      "title": "Private endpoint",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS PrivateLink and VPC Endpoints",
              "short_name": "PrivateLink",
              "doc_url": "https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-access-aws-services.html",
              "one_line": "Private connectivity to AWS services and your own services via interface endpoints (ENIs) or free gateway endpoints (S3, DynamoDB).",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Private Link / Private Endpoint",
              "short_name": "Private Endpoint",
              "doc_url": "https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview",
              "one_line": "NIC with a private IP placed in your subnet connecting privately to a PaaS service or your own service behind a Standard LB.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Private Service Connect",
              "short_name": "PSC",
              "doc_url": "https://cloud.google.com/vpc/docs/private-service-connect",
              "one_line": "Consumer-controlled private endpoints to managed services and published producer services via global forwarding rules.",
              "status": "ga"
            },
            {
              "name": "Private Google Access",
              "short_name": "PGA",
              "doc_url": "https://cloud.google.com/vpc/docs/private-google-access-hybrid",
              "one_line": "Subnet flag so IP-less VMs reach Google APIs over internal routes.",
              "status": "ga"
            },
            {
              "name": "Private Services Access",
              "short_name": "PSA",
              "doc_url": "https://cloud.google.com/vpc/docs/private-services-access",
              "one_line": "Peering-based private connectivity into producer VPCs (e.g., Cloud SQL private IP).",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Service Gateway and Private Service Access",
              "short_name": "SGW / PSA",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/servicegateway.htm",
              "one_line": "Private paths from a VCN to Oracle Services Network (service gateway) and newer per-service Private Service Access endpoints.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "route-table",
      "domain": "networking-core",
      "title": "Route table",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "VPC Route Table",
              "short_name": "Route Table",
              "doc_url": "https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html",
              "one_line": "Route set (destination CIDR/prefix list to gateway/ENI/TGW target) applied to subnets or gateways, with main-table fallback and propagation.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "User-defined routes (UDR)",
              "short_name": "UDR",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-udr-overview",
              "one_line": "Custom route tables attached to subnets overriding Azure system routes with explicit next hops.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Routes",
              "short_name": "Routes",
              "doc_url": "https://cloud.google.com/vpc/docs/routes",
              "one_line": "System-generated and custom static routes with priorities; dynamic routes arrive via Cloud Router BGP.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Route Tables",
              "short_name": "Route tables",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/managingroutetables.htm",
              "one_line": "Per-subnet rule sets routing traffic to gateways, DRG, LPGs, private IPs, or PEERED sources.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "shared-vpc",
      "domain": "networking-core",
      "title": "Shared VPC",
      "cells": {
        "aws": {
          "state": "elsewhere",
          "reason": "VPC sharing delivers the same pattern: an owning account shares subnets with participant accounts through Resource Access Manager.",
          "see": "cross-account-resource-sharing"
        },
        "azure": {
          "state": "absent",
          "reason": "No network-sharing construct. A hub subscription owns the virtual network, and workload subscriptions peer into it or receive RBAC on its subnets."
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Shared VPC",
              "short_name": "SharedVPC",
              "doc_url": "https://cloud.google.com/vpc/docs/shared-vpc",
              "one_line": "Host project owns networks/subnets; service projects attach workloads under central control.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "Not needed in the same form. A VCN lives in a compartment, and policy grants other compartments the right to attach workloads to its subnets inside the one tenancy."
        }
      }
    },
    {
      "key": "stateful-packet-filter",
      "domain": "networking-core",
      "title": "Stateful packet filter",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Security groups and network ACLs",
              "short_name": "SG / NACL",
              "doc_url": "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html",
              "one_line": "Stateful allow-only rules at the network interface (security groups) plus stateless numbered allow and deny rules at the subnet edge (network ACLs).",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Network Security Groups + Application Security Groups",
              "short_name": "NSG/ASG",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview",
              "one_line": "Stateful L3/L4 filter rules applied at subnet or NIC, with ASGs grouping NICs by role instead of IP.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "VPC firewall rules and hierarchical firewall policies",
              "short_name": "VPC firewall rules",
              "doc_url": "https://cloud.google.com/firewall/docs/firewalls",
              "one_line": "Distributed stateful filter enforced at every instance interface, with rules targeted by network tag, secure tag, or service account rather than only by address.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Security lists and network security groups",
              "short_name": "Security lists / NSG",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/securityrules.htm",
              "one_line": "Stateful ingress and egress rules applied at the subnet (security lists) or at the individual VNIC (network security groups), with both evaluated together.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "subnet",
      "domain": "networking-core",
      "title": "Subnet",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "VPC Subnet",
              "short_name": "Subnet",
              "doc_url": "https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html",
              "one_line": "CIDR slice confined to one Availability Zone; public/private/isolated nature set purely by its routes.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Subnets",
              "short_name": "Subnet",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-manage-subnet",
              "one_line": "Address ranges inside a VNet where NICs, gateways, and private endpoints attach.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Subnets",
              "short_name": "Subnet",
              "doc_url": "https://cloud.google.com/vpc/docs/subnets",
              "one_line": "Regional IP ranges inside a VPC, with optional secondary ranges for containers/PSC.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Subnets (regional or AD-specific)",
              "short_name": "Subnets",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/VCNs.htm",
              "one_line": "Subdivisions of a VCN; new subnets can be regional (recommended) or tied to one availability domain.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "transit-hub",
      "domain": "networking-core",
      "title": "Transit hub",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Transit Gateway",
              "short_name": "TGW",
              "doc_url": "https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html",
              "one_line": "Regional hub-and-spoke router connecting thousands of VPCs, VPNs, DX gateways, Connect appliances, and inter-Region peers with segmented route tables.",
              "status": "ga"
            },
            {
              "name": "AWS Cloud WAN",
              "short_name": "Cloud WAN",
              "doc_url": "https://docs.aws.amazon.com/network-manager/latest/cloudwan/what-is-cloudwan.html",
              "one_line": "Managed wide-area network service: a global core network with segments, network policies, and VPC/VPN/Direct Connect attachments, run centrally through Network Manager.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Virtual WAN hub",
              "short_name": "vWAN",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-about",
              "one_line": "Microsoft-managed hub supporting branch/VPN/ExpressRoute/spoke connectivity with optional integrated firewall and routing intent.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Network Connectivity Center",
              "short_name": "NCC",
              "doc_url": "https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/overview",
              "one_line": "Hub-and-spoke transit plane joining VPC spokes, VPN, Interconnect, and Router appliances.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Dynamic Routing Gateway (DRG v2)",
              "short_name": "DRG",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/managingDRGs.htm",
              "one_line": "Regional router/hub attaching VCNs, FastConnect, VPN, and remote peering with route distribution and import rules.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "virtual-network",
      "domain": "networking-core",
      "title": "Virtual network",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Virtual Private Cloud",
              "short_name": "VPC",
              "doc_url": "https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html",
              "one_line": "Software-defined isolated network with controllable CIDRs (/16-/28), subnets per AZ, route tables, and gateways.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Virtual Network",
              "short_name": "VNet",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview",
              "one_line": "Private address space (regional) containing subnets with platform-integrated routing and security.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "VPC networks",
              "short_name": "VPC",
              "doc_url": "https://cloud.google.com/vpc/docs/vpc",
              "one_line": "GLOBAL software-defined networks containing regional subnets; auto or custom mode.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Virtual Cloud Network (VCN)",
              "short_name": "VCN",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/VCNs.htm",
              "one_line": "Software-defined regional private network with configurable CIDRs and gateways.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "cdn",
      "domain": "networking-lb-edge",
      "title": "CDN",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon CloudFront",
              "short_name": "CloudFront",
              "doc_url": "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html",
              "one_line": "Global CDN with 700+ edge POPs, OAC-signed S3 origins, CloudFront Functions vs Lambda@Edge, and Shield integration.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure CDN (legacy SKUs)",
              "short_name": "CDN",
              "doc_url": "https://learn.microsoft.com/en-us/azure/frontdoor/front-door-overview",
              "one_line": "Legacy content-delivery products (Akamai/Edgio-based SKUs) largely superseded by Front Door.",
              "status": "deprecated"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud CDN",
              "short_name": "CDN",
              "doc_url": "https://cloud.google.com/cdn/docs/overview",
              "one_line": "Google-edge caching in front of external LBs: cache modes, signed URLs, invalidation.",
              "status": "ga"
            },
            {
              "name": "Media CDN",
              "short_name": "MediaCDN",
              "doc_url": "https://cloud.google.com/media-cdn/docs/overview",
              "one_line": "YouTube-grade edge platform for video/VOD/large-object delivery with middleware hooks.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No first-party general-purpose CDN. A first-party offering announced in 2023 never materialized as a durable product. Nearest capabilities: partner/marketplace CDNs (e.g., Akamai) fronting OCI origins, OCI WAF at the edge, Traffic Management DNS steering, and Media Streams streaming delivery via OCI Edge or external CDNs."
        }
      }
    },
    {
      "key": "ddos-protection",
      "domain": "networking-lb-edge",
      "title": "DDoS protection",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Shield Standard and Advanced",
              "short_name": "Shield",
              "doc_url": "https://aws.amazon.com/shield/pricing/",
              "one_line": "Standard DDoS protection always-on and free on Route 53/CloudFront/ELB; Advanced adds cost protection, response team, and L7 rule groups at $3,000/month.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure DDoS Network Protection",
              "short_name": "DDoS",
              "doc_url": "https://learn.microsoft.com/en-us/azure/ddos-protection/ddos-protection-overview",
              "one_line": "Always-on volumetric scrubbing tuned per public IP with cost rebate during active attacks.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Armor (standard always-on)",
              "short_name": "Armor std",
              "doc_url": "https://cloud.google.com/armor/docs/cloud-armor-overview",
              "one_line": "Always-on L3/L4 defense at Google edge plus configurable security policies on LBs.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Edge DDoS protection",
              "short_name": "DDoS",
              "doc_url": "https://docs.oracle.com/en/solutions/learn-ddos-prevention-oci/understand-ddos-layers-and-oracle-ddos-protection1.html",
              "one_line": "Always-on volumetric protection included on OCI edge for public endpoints, with SOC monitoring.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "gateway-load-balancer",
      "domain": "networking-lb-edge",
      "title": "Gateway load balancer",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Gateway Load Balancer",
              "short_name": "GWLB",
              "doc_url": "https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html",
              "one_line": "Transparent L3 entry point deploying and scaling third-party security appliances (firewall, IDS/IPS) inline via GENEVE tunnels.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Load Balancer (Gateway SKU)",
              "short_name": "Gateway LB",
              "doc_url": "https://learn.microsoft.com/en-us/azure/load-balancer/gateway-overview",
              "one_line": "Bump-in-the-wire insertion point that chains third-party network virtual appliances into the traffic path without changing the application's addressing.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "absent",
          "reason": "No transparent appliance-insertion load balancer. Appliances are inserted with an internal passthrough load balancer as the next hop plus policy-based routes."
        },
        "oci": {
          "state": "absent",
          "reason": "No transparent appliance-insertion load balancer. Appliances are inserted with route rules that point at a private IP."
        }
      }
    },
    {
      "key": "global-front-door",
      "domain": "networking-lb-edge",
      "title": "Global front door",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Global Accelerator",
              "short_name": "Global Accelerator",
              "doc_url": "https://docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html",
              "one_line": "Two static anycast IPs riding the AWS global backbone to healthy regional endpoints with sub-minute failover and traffic dials.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Front Door (Standard/Premium)",
              "short_name": "AFD",
              "doc_url": "https://learn.microsoft.com/en-us/azure/frontdoor/front-door-overview",
              "one_line": "Global anycast ingress with TLS termination, caching, rules engine, WAF, and origin health steering.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Global anycast entry (external ALB plays front door)",
              "short_name": "Front door",
              "doc_url": "https://cloud.google.com/load-balancing/docs/load-balancing-overview",
              "one_line": "GCP has no separate 'front door' SKU - global ALB + Premium tier anycast + Cloud Armor + CDN is the pattern.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Traffic Management (DNS-level global steering)",
              "short_name": "TM",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/TrafficManagement/Concepts/overview.htm",
              "one_line": "DNS steering policies for failover, weighted, geolocation, ASN, and IP-prefix routing across regions.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "l4-load-balancer",
      "domain": "networking-lb-edge",
      "title": "L4 load balancer",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Network Load Balancer",
              "short_name": "NLB",
              "doc_url": "https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html",
              "one_line": "Ultra-high-performance L4 balancer with static/EIP addresses per AZ, flow-hash stickiness, and zonal isolation removing unhealthy zones from DNS.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Load Balancer",
              "short_name": "LB",
              "doc_url": "https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-overview",
              "one_line": "Ultra-low-latency L4 pass-through balancer (public/internal, regional) with hash-based distribution.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Network Load Balancer / proxy load balancers",
              "short_name": "NLB",
              "doc_url": "https://cloud.google.com/load-balancing/docs/network",
              "one_line": "Passthrough L4 (regional/global) and proxy L4 (TLS/TCP/UDP) family incl internal variants.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Network Load Balancer",
              "short_name": "NLB",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/NetworkLoadBalancer/home.htm",
              "one_line": "Layer-4 passthrough load balancer preserving client IPs, with high availability across fault domains.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "l7-load-balancer",
      "domain": "networking-lb-edge",
      "title": "L7 load balancer",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Application Load Balancer",
              "short_name": "ALB",
              "doc_url": "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html",
              "one_line": "Layer-7 balancer routing on host/path/header/query with OIDC-Cognito authentication actions, Lambda targets, and WAF attachment.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Application Gateway v2",
              "short_name": "AppGW",
              "doc_url": "https://learn.microsoft.com/en-us/azure/application-gateway/overview",
              "one_line": "Regional L7 reverse proxy with path/host routing, cookie affinity, TLS termination, and optional WAF.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Global external Application Load Balancer (+ regional variants)",
              "short_name": "ALB",
              "doc_url": "https://cloud.google.com/load-balancing/docs/load-balancing-overview",
              "one_line": "Global anycast L7 LB with URL maps, TLS termination at edge POPs, serverless NEG backends.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Flexible Load Balancer (LBaaS)",
              "short_name": "Load Balancer",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Balance/home.htm",
              "one_line": "Proxy load balancer for HTTP/HTTPS/TCP with SSL offload, path routing, WAF enforcement point.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "authoritative-dns",
      "domain": "dns-domains",
      "title": "Authoritative DNS",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Route 53 (public hosted zones)",
              "short_name": "Route 53",
              "doc_url": "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-working-with.html",
              "one_line": "Authoritative DNS with a 100% monthly uptime SLA per hosted zone and health-checked record sets.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure DNS (public zones)",
              "short_name": "Azure DNS",
              "doc_url": "https://learn.microsoft.com/en-us/azure/dns/dns-overview",
              "one_line": "Authoritative hosted DNS zones with alias records pointing at Azure resources.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud DNS (public zones)",
              "short_name": "Cloud DNS",
              "doc_url": "https://cloud.google.com/dns/docs/overview",
              "one_line": "Managed authoritative DNS with 100% availability SLA, anycast serving, DNSSEC.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "OCI DNS (public zones)",
              "short_name": "DNS",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/DNS/home.htm",
              "one_line": "Anycast authoritative DNS for public zones with DNSSEC support.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "dns-routing-policies",
      "domain": "dns-domains",
      "title": "DNS routing policies",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Route 53 Routing Policies",
              "short_name": "Routing policies",
              "doc_url": "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html",
              "one_line": "Eight policies: simple, weighted, latency, failover, geolocation, geoproximity, multivalue answer, and IP-based.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Traffic Manager",
              "short_name": "TM",
              "doc_url": "https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-overview",
              "one_line": "DNS-level traffic steering with priority, weighted, performance, geographic, and subnet methods plus endpoint monitoring.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud DNS routing policies",
              "short_name": "DNS policies",
              "doc_url": "https://cloud.google.com/dns/docs/routing-policies-overview",
              "one_line": "Weighted round robin, geolocation, geofenced, and failover routing on record sets.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Traffic Management Steering Policies",
              "short_name": "Steering policies",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/TrafficManagement/Concepts/trafficmanagementapi.htm",
              "one_line": "Rule-based DNS answers: FAILOVER, LOAD_BALANCE (weights), GEOLOCATION, ASN, IP PREFIX, plus CUSTOM composition.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "domain-registrar",
      "domain": "dns-domains",
      "title": "Domain registrar",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Route 53 Registrar",
              "short_name": "Registrar",
              "doc_url": "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/registrar.html",
              "one_line": "ICANN-accredited domain registration, transfer, renewal, and DNSSEC configuration integrated with hosted zones.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "App Service Domains",
              "short_name": "AS Domains",
              "doc_url": "https://learn.microsoft.com/en-us/azure/app-service/manage-custom-dns-buy-domain",
              "one_line": "Domain purchase/management surfaced through Azure (partner registry) with Azure DNS hosting.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Domains",
              "short_name": "Domains",
              "doc_url": "https://cloud.google.com/domains/docs/overview",
              "one_line": "Registrar service managing registrations/transfers integrated with Cloud DNS.",
              "status": "retiring"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "Oracle states plainly: OCI isn't a registrar. Register domains at a third-party registrar and delegate the zone to OCI authoritative DNS."
        }
      }
    },
    {
      "key": "private-dns",
      "domain": "dns-domains",
      "title": "Private DNS",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Route 53 Private Hosted Zones",
              "short_name": "Private Hosted Zone",
              "doc_url": "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-private.html",
              "one_line": "VPC-associated internal DNS zones with split-view answers distinct from the public zone.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Private DNS zones",
              "short_name": "Private DNS",
              "doc_url": "https://learn.microsoft.com/en-us/azure/dns/private-dns-privatednszone",
              "one_line": "VNet-linked private zones resolving internal names; auto-registration optionally writes VM records.",
              "status": "ga"
            },
            {
              "name": "Azure DNS Private Resolver",
              "short_name": "DNS Resolver",
              "doc_url": "https://learn.microsoft.com/en-us/azure/dns/dns-private-resolver-overview",
              "one_line": "Managed inbound/outbound DNS forwarding endpoints with rule sets replacing hand-built forwarder VMs.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud DNS private zones",
              "short_name": "Private zones",
              "doc_url": "https://cloud.google.com/dns/docs/zones",
              "one_line": "Project- or org-shared internal zones resolved by VPCs; forwarding zones and inbound/outbound peering.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Private DNS (resolvers, zones, endpoints)",
              "short_name": "Private DNS",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/DNS/Tasks/privatedns.htm",
              "one_line": "Private zone resolution inside VCNs with custom resolvers, listeners, and forwarders to on-premises DNS.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "client-vpn",
      "domain": "hybrid-connectivity",
      "title": "Client VPN",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Client VPN",
              "short_name": "Client VPN",
              "doc_url": "https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/what-is.html",
              "one_line": "Managed OpenVPN-based remote access with AD, certificate, or SAML federation authentication.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Point-to-Site VPN + Azure Bastion",
              "short_name": "P2S/Bastion",
              "doc_url": "https://learn.microsoft.com/en-us/azure/bastion/bastion-overview",
              "one_line": "Per-user remote access via OpenVPN/IKEv2 tunnels (cert or Entra auth) and browser-based bastion host.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "absent",
          "reason": "No managed client VPN service. Nearest: Identity-Aware Proxy TCP forwarding for SSH/RDP without a bastion, plus third-party VPN servers on GKE/CE."
        },
        "oci": {
          "state": "absent",
          "reason": "No native remote-access/client VPN service. Oracle's own tutorial states OCI does not offer a native Remote Access VPN; documented alternatives are Bastion for session-brokered administrative access and marketplace OpenVPN appliances on compute."
        }
      }
    },
    {
      "key": "cross-cloud-interconnect",
      "domain": "hybrid-connectivity",
      "title": "Cross-cloud interconnect",
      "cells": {
        "aws": {
          "state": "absent",
          "reason": "No first-party circuit into another provider's fabric. Cross-cloud links are built from Direct Connect plus a colocation or partner cross-connect."
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "ExpressRoute to OCI FastConnect direct interconnect",
              "short_name": "Azure-OCI interconnect",
              "doc_url": "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/connectivity-to-other-providers-oci",
              "one_line": "Direct private path between Azure and Oracle Cloud Infrastructure, pairing an ExpressRoute circuit with an OCI FastConnect circuit and no cross-connect of your own.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cross-Cloud Interconnect",
              "short_name": "CCI",
              "doc_url": "https://cloud.google.com/network-connectivity/docs/interconnect/concepts/cci-overview",
              "one_line": "Direct high-capacity physical links between GCP and other cloud providers' fabrics.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Oracle Interconnect for Azure and Google Cloud",
              "short_name": "Oracle Interconnect",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/multicloud/interconnect-azure.htm",
              "one_line": "Direct private links between OCI and another provider's fabric, pairing a FastConnect circuit with the partner cloud's own circuit and no cross-connect of your own.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "dedicated-interconnect",
      "domain": "hybrid-connectivity",
      "title": "Dedicated interconnect",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Direct Connect",
              "short_name": "DX",
              "doc_url": "https://docs.aws.amazon.com/directconnect/latest/UserGuide/connection_options.html",
              "one_line": "Dedicated private circuits (1/10/100/400 Gbps dedicated, 50 Mbps-25 Gbps hosted) bypassing the public internet, with MACsec on select ports.",
              "status": "ga"
            },
            {
              "name": "AWS Direct Connect Gateway",
              "short_name": "DX Gateway",
              "doc_url": "https://docs.aws.amazon.com/directconnect/latest/UserGuide/direct-connect-gateways-intro.html",
              "one_line": "Global resource attaching one DX private virtual interface to VPCs or transit gateways across Regions and accounts without public BGP.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "ExpressRoute",
              "short_name": "ERX",
              "doc_url": "https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction",
              "one_line": "Private BGP-peered circuit to Microsoft edge: provider circuits 50 Mbps-10 Gbps or Direct ports at 10/100/400 Gbps.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Dedicated Interconnect",
              "short_name": "Dedicated IC",
              "doc_url": "https://cloud.google.com/network-connectivity/docs/interconnect/concepts/dedicated-overview",
              "one_line": "Physical 10, 100, or 400 Gbps circuits in colos carved into VLAN attachments (up to 8x400G = 3200 Gbps).",
              "status": "ga"
            },
            {
              "name": "Partner Interconnect",
              "short_name": "Partner IC",
              "doc_url": "https://cloud.google.com/network-connectivity/docs/interconnect/concepts/partner-overview",
              "one_line": "Provider-mediated connectivity 50 Mbps to 50 Gbps where colo presence is impractical.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "FastConnect",
              "short_name": "FastConnect",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/fastconnectoverview.htm",
              "one_line": "Private dedicated connectivity: cross-connects at 1/10/100/400 Gbps or partner virtual circuits, port-hour billing with zero data-transfer charges.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "metro-edge-locations",
      "domain": "hybrid-connectivity",
      "title": "Metro edge locations",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Local Zones",
              "short_name": "Local Zones",
              "doc_url": "https://docs.aws.amazon.com/local-zones/latest/ug/how-local-zones-work.html",
              "one_line": "Metro extensions of a parent Region with their own internet and Direct Connect egress for single-digit millisecond latency.",
              "status": "ga"
            },
            {
              "name": "AWS Wavelength",
              "short_name": "Wavelength",
              "doc_url": "https://docs.aws.amazon.com/wavelength/latest/developerguide/what-is-wavelength.html",
              "one_line": "Compute embedded inside carrier 5G networks behind carrier gateways for ultra-low-latency mobile workloads.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "absent",
          "reason": "No broadly available metro or carrier edge tier in this snapshot. The nearest options are Azure Local at an operator site and partner edge estates; verify the current status of Azure public multi-access edge compute before rendering this cell."
        },
        "gcp": {
          "state": "absent",
          "reason": "No metro or carrier edge tier inside the region model. Google Distributed Cloud Edge places hardware at your own or an operator's site instead. See on-prem-extension."
        },
        "oci": {
          "state": "absent",
          "reason": "No metro or carrier edge tier. Roving Edge devices and Compute Cloud@Customer place hardware at your site instead. See on-prem-extension."
        }
      }
    },
    {
      "key": "on-prem-extension",
      "domain": "hybrid-connectivity",
      "title": "On-prem extension",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Outposts",
              "short_name": "Outposts",
              "doc_url": "https://docs.aws.amazon.com/outposts/latest/userguide/what-is-outposts.html",
              "one_line": "AWS racks installed on-premises running native EC2/EBS/S3-on-Outposts/RDS/EKS with local gateways; 1U/2U servers end-of-sale.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Arc",
              "short_name": "Arc",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-arc/overview",
              "one_line": "Projects servers, Kubernetes, and data services anywhere into ARM for unified policy/security/monitoring.",
              "status": "ga"
            },
            {
              "name": "Azure Local",
              "short_name": "Azure Local",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-local/overview",
              "one_line": "Microsoft-validated on-premises hyperconverged cluster (formerly Azure Stack HCI) operated through Azure.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Google Distributed Cloud (edge & air-gapped)",
              "short_name": "GDC",
              "doc_url": "https://cloud.google.com/distributed-cloud",
              "one_line": "Google-run GKE/VMware stacks on customer edge or fully air-gapped premises.",
              "status": "ga"
            },
            {
              "name": "Google Distributed Cloud Edge",
              "short_name": "GDC Edge",
              "doc_url": "https://cloud.google.com/distributed-cloud",
              "one_line": "Ruggedized edge racks with GKE + local AI inference close to data sources.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Compute Cloud@Customer and Private Cloud Appliance",
              "short_name": "C@C / PCA",
              "doc_url": "https://docs.oracle.com/en-us/iaas/compute-cloud-at-customer/home.htm",
              "one_line": "Full OCI control-plane and services running in your own data center as rack-scale systems.",
              "status": "ga"
            },
            {
              "name": "Roving Edge Infrastructure",
              "short_name": "Roving Edge",
              "doc_url": "https://docs.oracle.com/en-us/iaas/roving-edge-infrastructure/rvr/home.htm",
              "one_line": "Ruggedized portable OCI-capable devices for field, disconnected, and edge processing.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "sdwan-integration",
      "domain": "hybrid-connectivity",
      "title": "SD-WAN integration",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Transit Gateway Connect",
              "short_name": "TGW Connect",
              "doc_url": "https://docs.aws.amazon.com/vpc/latest/tgw/tgw-connect.html",
              "one_line": "GRE-plus-BGP attachment integrating SD-WAN appliances into a transit gateway over a VPC or DX transport.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "vWAN partner SD-WAN / NVA hubs",
              "short_name": "SD-WAN",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-about",
              "one_line": "Third-party SD-WAN controllers and NVAs integrating branches into Azure Virtual WAN hubs.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Network Connectivity Center router appliance spokes",
              "short_name": "Router appliance",
              "doc_url": "https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/ra-overview",
              "one_line": "Attaches a third-party SD-WAN or router virtual appliance to the Network Connectivity Center hub as a spoke, so branch routes join the cloud routing domain over BGP.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No SD-WAN attachment construct. Third-party appliances connect over IPSec to the Dynamic Routing Gateway or run as instances in a hub VCN."
        }
      }
    },
    {
      "key": "site-to-site-vpn",
      "domain": "hybrid-connectivity",
      "title": "Site-to-site VPN",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Site-to-Site VPN",
              "short_name": "Site-to-Site VPN",
              "doc_url": "https://docs.aws.amazon.com/vpn/latest/s2svpn/VPNTunnels.html",
              "one_line": "Managed IPsec connectivity with two redundant tunnels per connection terminating in separate AZs.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "VPN Gateway (S2S)",
              "short_name": "VPN GW",
              "doc_url": "https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpngateways",
              "one_line": "IPsec/IKE tunnel terminating in a gateway subnet with BGP support and active-active options.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "HA VPN (+ Classic VPN legacy)",
              "short_name": "HA VPN",
              "doc_url": "https://cloud.google.com/network-connectivity/docs/vpn/concepts/overview",
              "one_line": "IPsec site-to-site with two interfaces/tunnels for 99.99% SLA; dynamic routing via Cloud Router.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Site-to-Site VPN (VPN Connect v2)",
              "short_name": "IPSec VPN",
              "doc_url": "https://www.oracle.com/cloud/networking/site-to-site-vpn/",
              "one_line": "Next-generation IPSec tunnels with policy or BGP routing, customizable IKE parameters, and per-tunnel metrics.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "vmware-stack-hosting",
      "domain": "hybrid-connectivity",
      "title": "VMware stack hosting",
      "cells": {
        "aws": {
          "state": "absent",
          "reason": "VMware Cloud on AWS is no longer sold by AWS following the Broadcom transition, so there is no first-party VMware stack in this snapshot. Verify the current offer before rendering this cell."
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure VMware Solution",
              "short_name": "AVS",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-vmware/introduction",
              "one_line": "VMware Cloud Foundation stack running on dedicated Azure bare-metal hosts, administered with vCenter, NSX, and vSAN exactly as on-premises.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Google Cloud VMware Engine",
              "short_name": "VMware Engine",
              "doc_url": "https://cloud.google.com/vmware-engine/docs/overview",
              "one_line": "Native VMware Cloud Foundation stack (vSphere/vSAN/NSX) on bare metal in GCP regions.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Oracle Cloud VMware Solution",
              "short_name": "OCVS",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/VMware/Concepts/ocvsoverview.htm",
              "one_line": "Customer-administered VMware Cloud Foundation stack on OCI bare metal, with vCenter, NSX, and vSAN run by you rather than by Oracle.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "conditional-access",
      "domain": "identity-workforce",
      "title": "Conditional access",
      "cells": {
        "aws": {
          "state": "absent",
          "reason": "No signal-driven sign-in policy engine. The nearest controls are IAM condition keys such as aws:SourceIp and aws:MultiFactorAuthPresent, evaluated per API request rather than once at authentication."
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Conditional Access",
              "short_name": "CA",
              "doc_url": "https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview",
              "one_line": "Signal-driven policy engine enforcing MFA/device/location/risk requirements at authentication time.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "elsewhere",
          "reason": "Delivered as Access Context Manager access levels applied through IAM conditions and Identity-Aware Proxy, rather than as one sign-in policy engine.",
          "see": "zero-trust-app-access"
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Identity domain sign-on policies with Adaptive Security",
              "short_name": "Sign-on policies",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Identity/adaptivesecurity/overview.htm",
              "one_line": "Sign-on policy rules that allow, deny, or step up authentication per sign-in based on group, network perimeter, client, and a risk score.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "iam-policy-language",
      "domain": "identity-workforce",
      "title": "IAM policy language",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "IAM Policy Language and Evaluation Logic",
              "short_name": "Policy language",
              "doc_url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html",
              "one_line": "JSON grammar (Effect/Action/Resource/Condition) with defined evaluation order: explicit deny wins, then SCP/RCP/boundary intersection, identity/resource union, session policy last.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure RBAC role definitions",
              "short_name": "RBAC defs",
              "doc_url": "https://learn.microsoft.com/en-us/azure/role-based-access-control/role-definitions",
              "one_line": "JSON permission sets expressed as Actions/NotActions/DataActions/NotDataActions with wildcard matching.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Policy language: conditions, deny policies, PAB",
              "short_name": "Policy lang",
              "doc_url": "https://cloud.google.com/iam/docs/policy-types",
              "one_line": "Allow bindings with CEL conditions; v2 deny rules that always win; principal access boundary policies.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "IAM Policy Language",
              "short_name": "Policy language",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Identity/Concepts/policysyntax.htm",
              "one_line": "Policy language for Allow statements plus explicit Deny statements (opt-in since November 20, 2025).",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "iam-principals",
      "domain": "identity-workforce",
      "title": "IAM principals",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Identity and Access Management (users, groups)",
              "short_name": "IAM",
              "doc_url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/id.html",
              "one_line": "Account-local users, groups, roles, and policy evaluation; root user restricted to rare tasks with MFA enforced by default.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Microsoft Entra ID (users, groups, service principals)",
              "short_name": "Entra ID",
              "doc_url": "https://learn.microsoft.com/en-us/entra/fundamentals/whatis",
              "one_line": "Directory service whose tenant is the hard boundary owning all Azure subscriptions' identity plane.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "IAM principals & allow policies",
              "short_name": "IAM",
              "doc_url": "https://cloud.google.com/iam/docs/overview",
              "one_line": "Google accounts, groups, domains, workforce identities, and service accounts bound to roles via allow policies.",
              "status": "ga"
            },
            {
              "name": "Cloud Identity",
              "short_name": "CI",
              "doc_url": "https://cloud.google.com/identity",
              "one_line": "Standalone IdP/user directory (Workspace-free) managing accounts/groups synced to IAM.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Users, Groups, Dynamic Groups",
              "short_name": "IAM principals",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Identity/getstarted/identity-domains.htm",
              "one_line": "Human users in identity domains, static groups, and rule-based dynamic groups that match instances/functions/pods.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "iam-roles",
      "domain": "identity-workforce",
      "title": "IAM roles",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "IAM Roles",
              "short_name": "Roles",
              "doc_url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html",
              "one_line": "Assumable identities with trust policies granting temporary credentials to users, services, and external principals.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Role assignments and built-in roles",
              "short_name": "Assignments",
              "doc_url": "https://learn.microsoft.com/en-us/azure/role-based-access-control/overview",
              "one_line": "Binding of principal + role definition + scope; additive across overlapping assignments.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Roles: basic / predefined / custom",
              "short_name": "Roles",
              "doc_url": "https://cloud.google.com/iam/docs/roles-overview",
              "one_line": "Collections of permissions; basic roles are coarse (owner/editor/viewer), predefined are curated, custom are assembled.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No role primitive: access attaches to groups (human) and dynamic groups (workload) via policy statements; there is no assumable role object and no role-permission bundle to attach."
        }
      }
    },
    {
      "key": "managed-directory",
      "domain": "identity-workforce",
      "title": "Managed directory",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Directory Service",
              "short_name": "Directory Service",
              "doc_url": "https://docs.aws.amazon.com/directoryservice/latest/admin-guide/what_is.html",
              "one_line": "Managed Microsoft Active Directory options: AWS Managed Microsoft AD, AD Connector proxy to existing AD, and Simple AD - the bridge for Windows auth, LDAP, and domain-joined workloads.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Microsoft Entra Domain Services",
              "short_name": "Entra DS",
              "doc_url": "https://learn.microsoft.com/en-us/entra/identity/domain-services/overview",
              "one_line": "Managed Active Directory domain offering LDAP, Kerberos, NTLM, and domain join with no domain controllers of your own to run.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Managed Service for Microsoft Active Directory",
              "short_name": "Managed AD",
              "doc_url": "https://cloud.google.com/managed-microsoft-ad/docs/overview",
              "one_line": "Managed Active Directory domain running real Microsoft domain controllers, offering LDAP, Kerberos, and domain join with no controllers of your own to patch.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No managed Active Directory service. Identity domains are the cloud directory, and AD integration is by federation or a self-run domain controller."
        }
      }
    },
    {
      "key": "os-login",
      "domain": "identity-workforce",
      "title": "OS login",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "EC2 Instance Connect",
              "short_name": "Instance Connect",
              "doc_url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-methods.html",
              "one_line": "IAM-authorised SSH to EC2: a one-time public key is pushed to instance metadata for 60 seconds instead of a long-lived key kept on the instance.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Microsoft Entra login for virtual machines",
              "short_name": "Entra VM login",
              "doc_url": "https://learn.microsoft.com/en-us/entra/identity/devices/howto-vm-sign-in-azure-ad-linux",
              "one_line": "VM extension that authorises operating-system sign-in through Entra ID roles and Conditional Access instead of keys or local accounts managed inside the guest.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "OS Login",
              "short_name": "OSLogin",
              "doc_url": "https://cloud.google.com/compute/docs/oslogin",
              "one_line": "Centralized Linux SSH authorization tied to IAM, with optional 2FA and SSH certificates.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No IAM-controlled SSH authorisation. Keys are supplied at instance launch and managed in the guest, and the Bastion service brokers the session."
        }
      }
    },
    {
      "key": "permission-boundary",
      "domain": "identity-workforce",
      "title": "Permission boundary",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "IAM Permissions Boundaries",
              "short_name": "Boundaries",
              "doc_url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html",
              "one_line": "Managed policy capping maximum permissions of one user or role; grants nothing alone, intersects with everything else.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "absent",
          "reason": "No first-class permission-boundary object exists (nothing like a delegated admin constraint on role grants). Nearest tools: platform-created deny assignments (only Azure itself creates them, e.g. via Deployment Stack deny settings), Azure Policy DenyAction effect, and custom-role NotActions - each narrower than a true boundary."
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "IAM Conditions + Principal Access Boundary",
              "short_name": "Boundary",
              "doc_url": "https://cloud.google.com/iam/docs/principal-access-boundary-policies",
              "one_line": "No boolean max-permissions object; boundaries are expressed as conditional grants plus deny/PAB layers.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No control that caps the maximum permissions a principal can ever be granted, even by a delegated administrator (nothing like AWS permissions boundaries). IAM Deny subtracts but anyone with policy-write authority can add/remove it; governance rules cap child tenancies from above rather than capping your own admins."
        }
      }
    },
    {
      "key": "privileged-access",
      "domain": "identity-workforce",
      "title": "Privileged access",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "IAM Access Analyzer and privileged-access controls",
              "short_name": "Access Analyzer",
              "doc_url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html",
              "one_line": "External and unused-access findings, policy validation, least-privilege generation from CloudTrail, MFA-conditioned STS, break-glass patterns.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Privileged Identity Management (PIM)",
              "short_name": "PIM",
              "doc_url": "https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-configure",
              "one_line": "Just-in-time activation of Entra and Azure roles with approval, MFA, and time-boxed assignment.",
              "status": "ga"
            },
            {
              "name": "Entra ID Governance (access reviews, entitlements)",
              "short_name": "ID Governance",
              "doc_url": "https://learn.microsoft.com/en-us/entra/id-governance/identity-governance-overview",
              "one_line": "Lifecycle workflows, access packages, and recurring attestation campaigns.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Privileged Access Manager + Policy Analyzer + Access Approval/Transparency",
              "short_name": "PAM stack",
              "doc_url": "https://cloud.google.com/iam/docs/pam-overview",
              "one_line": "JIT time-boxed role elevation with approvals, access-explainer tooling, and Google-side access governance.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Access Governance",
              "short_name": "Access Governance",
              "doc_url": "https://www.oracle.com/security/cloud-security/access-governance/",
              "one_line": "Oracle Access Governance cloud service for access reviews, role mining, and privileged-access campaigns across OCI and hybrid identities.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "workforce-sso",
      "domain": "identity-workforce",
      "title": "Workforce SSO",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "IAM Identity Center",
              "short_name": "Identity Center",
              "doc_url": "https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html",
              "one_line": "Organization-wide SSO and workforce management: one identity source (directory, AD, external SAML IdP), permission sets mapped to accounts.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Entra enterprise applications (SAML/OIDC federation)",
              "short_name": "Enterprise SSO",
              "doc_url": "https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/what-is-application-management",
              "one_line": "App-gallery and custom app federation giving workforce SSO plus automated provisioning (SCIM).",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Workforce Identity Federation",
              "short_name": "WIF-workforce",
              "doc_url": "https://cloud.google.com/iam/docs/workforce-identity-federation",
              "one_line": "Federate Okta/Entra/ADFS etc. so external users get direct GCP access without Cloud Identity sync.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Identity Domains federation and SSO",
              "short_name": "SSO",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Identity/Concepts/federation.htm",
              "one_line": "SAML 2.0/OIDC federation with corporate IdPs (Entra ID, Okta, AD FS), SCIM provisioning, and app single sign-on.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "agent-identity",
      "domain": "identity-workload",
      "title": "Agent identity",
      "cells": {
        "aws": {
          "state": "elsewhere",
          "reason": "Delivered inside Bedrock AgentCore rather than as a directory object: AgentCore Identity issues and scopes agent credentials.",
          "see": "agent-platform"
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Microsoft Entra Agent ID",
              "short_name": "Agent ID",
              "doc_url": "https://learn.microsoft.com/en-us/entra/agent-id/what-is-microsoft-entra-agent-id",
              "one_line": "Purpose-built identity lifecycle for AI agents with sponsorship and governance controls.",
              "status": "preview"
            }
          ]
        },
        "gcp": {
          "state": "absent",
          "reason": "No distinct agent identity object. Agents run as ordinary service accounts, so agent lifecycle and human sponsorship are not modelled separately."
        },
        "oci": {
          "state": "absent",
          "reason": "No distinct agent identity object. Agents authenticate with resource principals like any other OCI service."
        }
      }
    },
    {
      "key": "cross-account-assumption",
      "domain": "identity-workload",
      "title": "Cross-account assumption",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Cross-account role assumption and External ID",
              "short_name": "External ID pattern",
              "doc_url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html",
              "one_line": "Trust-policy sts:ExternalId condition defeating confused-deputy replay when third parties assume roles across customers.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Cross-tenant access (multi-tenant apps, Lighthouse)",
              "short_name": "Cross-tenant",
              "doc_url": "https://learn.microsoft.com/en-us/azure/lighthouse/concepts/cross-tenant-management-experience",
              "one_line": "Patterns for one tenant's workload acting in another: multi-tenant app registration + consent, or Azure Lighthouse delegation.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Service account impersonation",
              "short_name": "Impersonate",
              "doc_url": "https://cloud.google.com/iam/docs/create-short-lived-credentials-direct",
              "one_line": "roles/iam.serviceAccountTokenCreator lets principals mint credentials FOR a target SA across projects/orgs.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Cross-compartment and cross-tenancy policies",
              "short_name": "Cross-tenancy",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Identity/policieshow/iam-cross-domain.htm",
              "one_line": "No AssumeRole primitive: access across boundaries is granted by policy statements (optionally with Define tenancy aliases and Endorse statements).",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "short-lived-credentials",
      "domain": "identity-workload",
      "title": "Short-lived credentials",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS STS Temporary Credentials",
              "short_name": "STS",
              "doc_url": "https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html",
              "one_line": "15-minute-to-12-hour scoped credentials minted per mechanism; role chaining caps sessions at 1 hour.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Entra tokens and SAS contrast",
              "short_name": "Token lifetimes",
              "doc_url": "https://learn.microsoft.com/en-us/entra/identity-platform/configurable-token-lifetimes",
              "one_line": "Access tokens default roughly 60-90 minutes with refresh tokens rotating; SAS/account keys are the long-lived exception to avoid.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "IAM Credentials API & OIDC ID tokens",
              "short_name": "SLC",
              "doc_url": "https://cloud.google.com/iam/docs/create-short-lived-credentials-direct",
              "one_line": "generateAccessToken/signJwt/generateIdToken plus metadata-server OAuth tokens: all credentials are temporary.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Session and delegation tokens",
              "short_name": "Short-lived creds",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/callingservicesfrominstances.htm",
              "one_line": "Console/API session tokens, instance principal session tokens (about 1 hour, refreshable), function delegation tokens, and IAM database tokens replace long-lived secrets.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "workload-identity",
      "domain": "identity-workload",
      "title": "Workload identity",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Workload roles for compute (instance profiles, task roles, execution roles)",
              "short_name": "Workload roles",
              "doc_url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html",
              "one_line": "EC2 instance profiles wrap one role; Lambda assumes its execution role; ECS splits task role (app perms) from task execution role (agent perms).",
              "status": "ga"
            },
            {
              "name": "EKS Pod Identity and IRSA",
              "short_name": "Pod Identity / IRSA",
              "doc_url": "https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html",
              "one_line": "Two ways to map IAM roles to Kubernetes service accounts: Pod Identity (no OIDC provider, single pods.eks.amazonaws.com principal) and IRSA (cluster OIDC provider, AssumeRoleWithWebIdentity).",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Managed identities",
              "short_name": "MI",
              "doc_url": "https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview",
              "one_line": "Credential-free Entra service principals bound to Azure compute lifecycle (system-assigned) or standalone (user-assigned).",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Attached service accounts (VM/Run/GKE)",
              "short_name": "SA attach",
              "doc_url": "https://cloud.google.com/iam/docs/service-account-overview",
              "one_line": "Workloads run AS a service account; libraries pull short-lived tokens from the metadata server.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Instance Principals and Resource Principals",
              "short_name": "Instance principals",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/callingservicesfrominstances.htm",
              "one_line": "Compute instances and services authenticate as themselves via certificates minted by the platform - no stored keys.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "workload-identity-federation",
      "domain": "identity-workload",
      "title": "Workload identity federation",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "OIDC/SAML federation and IAM Roles Anywhere",
              "short_name": "Web identity federation",
              "doc_url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html",
              "one_line": "AssumeRoleWithWebIdentity against registered OIDC issuers (GitHub Actions etc.), SAML 2.0 enterprise federation, and X.509-based Roles Anywhere for off-cloud servers.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Workload identity federation (FIC)",
              "short_name": "Federation",
              "doc_url": "https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation",
              "one_line": "OIDC trust configuration letting external IdPs (GitHub, any Kubernetes, Google, SPIFFE) exchange tokens for Entra tokens with zero secrets.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Workload Identity Federation",
              "short_name": "WIF",
              "doc_url": "https://cloud.google.com/iam/docs/workload-identity-federation",
              "one_line": "Keyless trust for external workloads via OIDC/SAML/AWS/X.509 pools+providers with attribute conditions.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "OKE Workload Identity",
              "short_name": "Workload Identity",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contenggrantingworkloadaccesstoresources.htm",
              "one_line": "Pods authenticate to OCI APIs using Kubernetes service accounts matched by IAM policy on enhanced OKE clusters.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "ciam-mfa",
      "domain": "identity-customer",
      "title": "CIAM MFA",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Cognito MFA and Passkeys",
              "short_name": "CIAM MFA",
              "doc_url": "https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow-methods.html",
              "one_line": "TOTP, SMS, email OTP factors plus WebAuthn passkeys usable as first factor or MFA.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Microsoft Entra multifactor authentication",
              "short_name": "MFA",
              "doc_url": "https://learn.microsoft.com/en-us/entra/identity/authentication/concept-mfa-howitworks",
              "one_line": "Second-factor enforcement: authenticator push, TOTP, FIDO2/passkeys, SMS/voice fallbacks.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Identity Platform MFA",
              "short_name": "CIAM MFA",
              "doc_url": "https://cloud.google.com/identity-platform/docs/web/mfa",
              "one_line": "SMS and TOTP second factors enforced per tenant/policy.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Identity Domain MFA",
              "short_name": "MFA",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Identity/mfa/configure-multi-factor-authentication-settings.htm",
              "one_line": "Multi-factor authentication policies per domain: TOTP, SMS, Duo Security, FIDO2/Yubico, Oracle Mobile Authenticator.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "ciam-social-federation",
      "domain": "identity-customer",
      "title": "CIAM social federation",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Cognito social and enterprise federation (+ Identity Pools)",
              "short_name": "CIAM federation",
              "doc_url": "https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow-methods.html",
              "one_line": "Brokered sign-in with Google/Apple/Facebook and SAML/OIDC providers; legacy identity pools exchange tokens for AWS credentials.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "External ID social & enterprise federation",
              "short_name": "Social IdPs",
              "doc_url": "https://learn.microsoft.com/en-us/entra/external-id/customers/concept-authentication-methods-customers",
              "one_line": "Federate Google/Facebook/apple plus OIDC/SAML enterprise IdPs into customer flows.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Identity Platform federated providers",
              "short_name": "Federated CIAM",
              "doc_url": "https://cloud.google.com/identity-platform/docs",
              "one_line": "Social (Google/Microsoft/Apple...) and SAML/OIDC enterprise federation into your app identities.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Social sign-in in Identity Domains",
              "short_name": "Social login",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Identity/sku/overview.htm",
              "one_line": "Federated sign-in with social providers configured per identity domain (limits 5 IdPs free tier, up to 30 paid).",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "ciam-user-directory",
      "domain": "identity-customer",
      "title": "CIAM user directory",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Cognito User Pools",
              "short_name": "Cognito",
              "doc_url": "https://aws.amazon.com/cognito/pricing/",
              "one_line": "Application user directories with hosted UI, JWT issuance, and three pricing tiers since Nov 2024 re-pricing.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Microsoft Entra External ID",
              "short_name": "External ID",
              "doc_url": "https://learn.microsoft.com/en-us/entra/external-id/customers/overview-customers-ciam",
              "one_line": "Customer-identity platform (CIAM) with branded sign-up/sign-in for external users in dedicated external tenants.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Identity Platform",
              "short_name": "IDP",
              "doc_url": "https://cloud.google.com/identity-platform/docs",
              "one_line": "Multi-tenant CIAM directories with email/password, phone, anonymous, and custom auth.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "External User identity domains",
              "short_name": "CIAM directory",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Identity/sku/overview.htm",
              "one_line": "Consumer-facing user directories billed per monthly active user with self-registration and consent management.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "byok-hyok",
      "domain": "secrets-keys",
      "title": "BYOK and HYOK",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "KMS Imported Key Material and External Key Store",
              "short_name": "BYOK / XKS",
              "doc_url": "https://docs.aws.amazon.com/kms/latest/developerguide/keystore-external.html",
              "one_line": "Import your own key material into KMS, or keep keys entirely outside AWS behind an external key store proxy (true HYOK, symmetric only).",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Customer-managed keys (BYOK)",
              "short_name": "CMK",
              "doc_url": "https://learn.microsoft.com/en-us/azure/security/fundamentals/encryption-atrest",
              "one_line": "Pattern wiring a Key Vault key as the root of each service's envelope encryption.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud External Key Manager (EKM)",
              "short_name": "EKM",
              "doc_url": "https://cloud.google.com/kms/docs/ekm",
              "one_line": "Keys held OUTSIDE Google (your KMS or partner) controlling GCP data - the HYOK pattern.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Vault imported key material and Dedicated Key Management",
              "short_name": "BYOK / Dedicated KMS",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/importingkeys.htm",
              "one_line": "Import your own key material into a Vault key, or hold keys in a single-tenant HSM partition that only your tenancy uses.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "certificate-authority",
      "domain": "secrets-keys",
      "title": "Certificate authority",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Private Certificate Authority",
              "short_name": "Private CA",
              "doc_url": "https://docs.aws.amazon.com/privateca/latest/userguide/PcaWelcome.html",
              "one_line": "Managed private CA hierarchies that issue, renew, and revoke internal X.509 certificates for mutual TLS between your own workloads.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "absent",
          "reason": "No managed private CA service. Key Vault issues certificates through integrated public CAs, and private hierarchies run on your own AD Certificate Services."
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Certificate Authority Service",
              "short_name": "CAS",
              "doc_url": "https://cloud.google.com/certificate-authority-service/docs",
              "one_line": "Private CA you operate: hierarchies, issuance policies, integration with workloads.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "elsewhere",
          "reason": "Delivered inside the Certificates service, which runs a managed internal CA alongside imported third-party certificates.",
          "see": "certificate-manager"
        }
      }
    },
    {
      "key": "certificate-manager",
      "domain": "secrets-keys",
      "title": "Certificate manager",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Certificate Manager",
              "short_name": "ACM",
              "doc_url": "https://docs.aws.amazon.com/acm/latest/userguide/acm-renewal.html",
              "one_line": "Free public TLS certificates with auto-renewal for integrated services (ALB, CloudFront, API GW) plus paid Private CA.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Key Vault certificates + App Service managed certs",
              "short_name": "Certificates",
              "doc_url": "https://learn.microsoft.com/en-us/azure/app-service/configure-ssl-certificate",
              "one_line": "Certificate lifecycle (CSR, renewal with integrated CAs) plus free managed certs for web apps.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Certificate Manager",
              "short_name": "CertMgr",
              "doc_url": "https://cloud.google.com/certificate-manager/docs/overview",
              "one_line": "Google-managed/self-managed TLS certs deployed via maps to LBs incl regional and hybrid patterns.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Certificates service",
              "short_name": "Certificates",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/certificates/home.htm",
              "one_line": "Managed internal CA issuing TLS certificates, plus imported third-party certificates, for LBs and other resources.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "hsm",
      "domain": "secrets-keys",
      "title": "HSM",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS CloudHSM",
              "short_name": "CloudHSM",
              "doc_url": "https://docs.aws.amazon.com/cloudhsm/latest/userguide/fips-validation.html",
              "one_line": "Single-tenant HSM clusters, hsm2m.medium FIPS 140-3 Level 3 certified, for exclusive key custody.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Key Vault Managed HSM",
              "short_name": "MHSM",
              "doc_url": "https://learn.microsoft.com/en-us/azure/key-vault/managed-hsm/",
              "one_line": "Fully managed single-tenant HSM pools (FIPS 140-3 Level 3 validated) with local RBAC.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud HSM",
              "short_name": "HSM",
              "doc_url": "https://cloud.google.com/kms/docs/hsm",
              "one_line": "FIPS 140-2 Level 3 validated key protection tier inside Cloud KMS API.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Dedicated Key Management (single-tenant HSM)",
              "short_name": "Dedicated KMS",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/dedicated_kms.htm",
              "one_line": "Customer-owned HSM partitions as a service with direct PKCS#11 access; three auto-synced partitions per cluster.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "key-management",
      "domain": "secrets-keys",
      "title": "Key management",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Key Management Service",
              "short_name": "KMS",
              "doc_url": "https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html",
              "one_line": "HSM-backed key management with envelope encryption, annual automatic rotation for customer-managed symmetric keys (opt-in), and multi-region keys.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Key Vault (keys) + platform encryption",
              "short_name": "Key Vault",
              "doc_url": "https://learn.microsoft.com/en-us/azure/key-vault/general/overview",
              "one_line": "Managed HSM-backed key store; every Azure service encrypts at rest with platform keys by default and accepts CMK.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Key Management Service",
              "short_name": "KMS",
              "doc_url": "https://cloud.google.com/kms/docs/key-management-service",
              "one_line": "Managed symmetric/asymmetric keys, key rings, rotation, CMEK across GCP services.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Vault Key Management",
              "short_name": "Vault keys",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/KeyManagement/Concepts/keyoverview.htm",
              "one_line": "Central management of master encryption keys (software or HSM-protected) used by OCI services via envelope encryption.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "secrets-store",
      "domain": "secrets-keys",
      "title": "Secrets store",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Secrets Manager",
              "short_name": "Secrets Manager",
              "doc_url": "https://aws.amazon.com/secrets-manager/pricing/",
              "one_line": "Purpose-built secret storage with native rotation (Lambda or managed), staging-label versioning, and cross-region replication at $0.40/secret/month.",
              "status": "ga"
            },
            {
              "name": "SSM Parameter Store",
              "short_name": "Parameter Store",
              "doc_url": "https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html",
              "one_line": "Hierarchical config store; standard tier free up to 10k parameters, SecureString adds KMS encryption, but no native rotation.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Key Vault secrets + Secrets Store CSI Driver",
              "short_name": "Secrets",
              "doc_url": "https://learn.microsoft.com/en-us/azure/aks/csi-secrets-store-driver",
              "one_line": "Versioned secret storage with rotation-friendly URI addressing; CSI driver mounts them into pods.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Secret Manager",
              "short_name": "SecretMgr",
              "doc_url": "https://cloud.google.com/secret-manager/docs/overview",
              "one_line": "Versioned secrets with IAM, replication policy, rotation notifications, CMEK.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Secret Management",
              "short_name": "Secrets",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/secret-management/overview.htm",
              "one_line": "Versioned secret storage (base64 contents) with rotation schedules and retrieval bundles.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "commitment-discounts",
      "domain": "org-tenancy",
      "title": "Commitment discounts",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Savings Plans",
              "short_name": "Savings Plans",
              "doc_url": "https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html",
              "one_line": "1- or 3-year dollar-per-hour commitment for up to 72% savings flexing across instance family/size/OS/Region including Fargate and Lambda.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Reservations and savings plan for compute",
              "short_name": "Reservations / Savings plan",
              "doc_url": "https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/save-compute-costs-reservations",
              "one_line": "Term commitments traded for a lower rate: a reservation commits to a specific resource type in a region, the savings plan commits to an hourly compute spend that flexes across eligible services and regions.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Committed use discounts",
              "short_name": "CUDs",
              "doc_url": "https://cloud.google.com/docs/cuds",
              "one_line": "One-year or three-year commitments traded for a lower rate, either resource-based against a machine family in a region or spend-based against an hourly dollar amount.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Oracle Universal Credits (Annual Flex)",
              "short_name": "Universal Credits",
              "doc_url": "https://www.oracle.com/cloud/universal-credits/",
              "one_line": "An annual dollar commitment drawn down by any eligible OCI service in any region, traded for a discount off pay-as-you-go rates.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "cost-advisory",
      "domain": "org-tenancy",
      "title": "Cost advisory",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Trusted Advisor",
              "short_name": "Trusted Advisor",
              "doc_url": "https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor.html",
              "one_line": "Best-practice checks across cost optimization, performance, security, fault tolerance, service limits, and operational excellence, with prioritized recommendations at enterprise scale.",
              "status": "ga"
            },
            {
              "name": "AWS Compute Optimizer",
              "short_name": "Compute Optimizer",
              "doc_url": "https://docs.aws.amazon.com/compute-optimizer/latest/ug/what-is-compute-optimizer.html",
              "one_line": "ML-driven rightsizing recommendations from utilization metrics for EC2, EBS volumes, Lambda functions, ECS services on Fargate, and autoscaling groups.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Advisor",
              "short_name": "Advisor",
              "doc_url": "https://learn.microsoft.com/en-us/azure/advisor/advisor-overview",
              "one_line": "Personalised recommendations across cost, reliability, security, performance, and operational excellence, scored against the Well-Architected pillars.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Recommender and Active Assist",
              "short_name": "Recommender",
              "doc_url": "https://cloud.google.com/recommender/docs/overview",
              "one_line": "Automated recommendations across cost, security, performance, reliability, and manageability, each with an estimated impact and an apply path.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "OCI Cloud Advisor",
              "short_name": "Cloud Advisor",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/CloudAdvisor/Concepts/cloudadvisoroverview.htm",
              "one_line": "Automated recommendations across cost, performance, availability, and security, each with an estimated saving and a direct apply action.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "cost-management",
      "domain": "org-tenancy",
      "title": "Cost management",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Billing and Cost Management (Cost Explorer, Budgets, Anomaly Detection)",
              "short_name": "Billing tools",
              "doc_url": "https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html",
              "one_line": "Consolidated billing, Cost Explorer (13 months history, 18-month forecast), six budget types, ML anomaly detection three times daily.",
              "status": "ga"
            },
            {
              "name": "AWS Data Exports (CUR 2.0)",
              "short_name": "CUR 2.0",
              "doc_url": "https://docs.aws.amazon.com/cur/latest/userguide/what-is-data-exports.html",
              "one_line": "Successor to legacy Cost and Usage Report: SQL-selectable columns, FOCUS 1.2 exports, recurring delivery to S3.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Cost Management + Billing",
              "short_name": "Cost Mgmt",
              "doc_url": "https://learn.microsoft.com/en-us/azure/cost-management-billing/understand/",
              "one_line": "Cost analysis views, budgets with action-group triggers, exports to storage, and reservation/savings-plan tracking.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Billing (budgets, exports, reports, calculator)",
              "short_name": "Billing",
              "doc_url": "https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables",
              "one_line": "Billing accounts linked to projects; budgets/alerts; BigQuery detailed export for analysis; pricing calculator.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Budgets, Cost Analysis, Cost and Usage Reports",
              "short_name": "Cost mgmt",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/budgetsoverview.htm",
              "one_line": "Budget alerts on compartments/tags, interactive Cost Analysis with forecasting, hourly CUR/FOCUS reports in Object Storage.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "cross-account-resource-sharing",
      "domain": "org-tenancy",
      "title": "Cross-account resource sharing",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Resource Access Manager (RAM)",
              "short_name": "RAM",
              "doc_url": "https://docs.aws.amazon.com/ram/latest/userguide/what-is.html",
              "one_line": "Shares supported resources - subnets, Transit Gateways, Dedicated Hosts, licence configurations - across accounts, OUs, or an organization without duplicating them.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "absent",
          "reason": "No general resource-sharing service. Sharing is done by placing the resource in a shared subscription and granting RBAC at the right scope, or by peering."
        },
        "gcp": {
          "state": "absent",
          "reason": "No general resource-sharing service. Networks are shared through Shared VPC, and everything else by granting IAM on the owning project."
        },
        "oci": {
          "state": "absent",
          "reason": "No general resource-sharing service. Compartments plus cross-tenancy policy statements (endorse, admit, define) grant the access instead."
        }
      }
    },
    {
      "key": "landing-zone",
      "domain": "org-tenancy",
      "title": "Landing zone",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Control Tower",
              "short_name": "Control Tower",
              "doc_url": "https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html",
              "one_line": "Opinionated landing zone: Account Factory vending, preventive (SCP/RCP), detective (Config), proactive (CFN Hooks) controls at OU level.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure landing zones (CAF)",
              "short_name": "ALZ",
              "doc_url": "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/",
              "one_line": "Reference architecture: platform landing zone (connectivity/identity/management subs) + application landing zones distributed by subscription vending.",
              "status": "ga"
            },
            {
              "name": "Subscription vending",
              "short_name": "Vending",
              "doc_url": "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/subscription-vending",
              "one_line": "Automated pipeline issuing pre-governed subscriptions (budget, policy, network, RBAC baked in).",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Assured Workloads (+ Fabric FAST blueprints)",
              "short_name": "Landing zone",
              "doc_url": "https://cloud.google.com/assured-workloads/docs/overview",
              "one_line": "Compliance-regime folders (FedRAMP/CJIS/EU...) enforced by policy; FAST gives reference landing zones.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "CIS Landing Zone framework",
              "short_name": "Landing Zone",
              "doc_url": "https://github.com/oracle-quickstart/oci-landing-zones",
              "one_line": "Oracle-published Terraform landing zone (Landing Zones framework / LZ service) deploying compartments, policies, budgets, Cloud Guard, and network baseline.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "org-guardrail-policy",
      "domain": "org-tenancy",
      "title": "Org guardrail policy",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Service Control Policies and Resource Control Policies",
              "short_name": "SCP / RCP",
              "doc_url": "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scp.html",
              "one_line": "SCPs cap what principals may do (max 10 attached, 10240 chars); RCPs cap what may happen to your resources regardless of caller (max 5 attached, 5120 chars).",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Policy (assignments, initiatives, exemptions)",
              "short_name": "Policy",
              "doc_url": "https://learn.microsoft.com/en-us/azure/governance/policy/overview",
              "one_line": "Declarative guardrail engine evaluating resource properties/actions with effects deny/audit/modify/deployIfNotExists/DenyAction.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Organization Policy Service",
              "short_name": "Org policy",
              "doc_url": "https://cloud.google.com/resource-manager/docs/organization-policy/overview",
              "one_line": "Inheritable constraints (boolean/list/custom CEL) restricting resource shapes org-wide; dry-run mode.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Security Zones",
              "short_name": "Security Zones",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/security-zone/home.htm",
              "one_line": "Compartment-scoped preventive guardrail recipes that BLOCK non-compliant resource creation and actions.",
              "status": "ga"
            },
            {
              "name": "Governance Rules (Organization Management)",
              "short_name": "Governance rules",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/General/organization/add-governance.htm",
              "one_line": "Parent-created controls attached to child tenancies - allowed regions, quota policies, tags - locked so the child cannot modify them.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "org-hierarchy",
      "domain": "org-tenancy",
      "title": "Org hierarchy",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Organizations",
              "short_name": "Organizations",
              "doc_url": "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html",
              "one_line": "Management account, root, OUs (5 levels deep), member accounts (up to 50k), consolidated billing, delegated administrators.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Tenant > management group > subscription > resource group",
              "short_name": "Hierarchy",
              "doc_url": "https://learn.microsoft.com/en-us/azure/governance/management-groups/overview",
              "one_line": "Four nesting levels: directory owns subscriptions; management groups (up to six levels below root) group them for inherited policy/RBAC.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Resource Manager hierarchy",
              "short_name": "Org/Folders/Projects",
              "doc_url": "https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy",
              "one_line": "Organization > folders > projects tree providing inheritance scope for IAM, org policy, VPC SC.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Tenancy and Compartments",
              "short_name": "Compartments",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingcompartments.htm",
              "one_line": "Single root tenancy containing nested compartments up to six levels deep; every resource lives in exactly one compartment.",
              "status": "ga"
            },
            {
              "name": "Organization Management (child tenancies)",
              "short_name": "Org Management",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/General/organization/organization_management_overview.htm",
              "one_line": "Multi-tenancy tree above compartments: create or invite child tenancies under one parent, map subscriptions, and centralize cost reporting.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "quota-management",
      "domain": "org-tenancy",
      "title": "Quota management",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Service Quotas",
              "short_name": "Service Quotas",
              "doc_url": "https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html",
              "one_line": "Central view, utilization tracking, and increase requests for per-service quotas; global quotas requested in us-east-1.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Quotas and subscription/resource limits",
              "short_name": "Quotas",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits",
              "one_line": "Per-region per-family quotas adjustable via support requests or the Quotas API/CLI.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Quotas system",
              "short_name": "Quotas",
              "doc_url": "https://cloud.google.com/docs/quotas/view-manage",
              "one_line": "Per-project service quotas (rate + allocation) with console/gcloud increase requests.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Compartment Quotas",
              "short_name": "Quotas",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Quotas/Concepts/resourcequotas.htm",
              "one_line": "Policy-like quota statements capping resource counts/services per compartment, complementing tenant-wide service limits.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "resource-tagging",
      "domain": "org-tenancy",
      "title": "Resource tagging",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Tag Editor, Tag Policies, Cost Allocation Tags",
              "short_name": "Tagging",
              "doc_url": "https://docs.aws.amazon.com/tag-editor/latest/userguide/tageditor.html",
              "one_line": "Org-level tag policies enforcing key/value standards, Tag Editor bulk ops, activated cost-allocation tags feeding Cost Explorer.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Resource tags",
              "short_name": "Tags",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources",
              "one_line": "Key/value metadata on resources and resource groups for cost allocation, ops, and policy targeting.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Labels",
              "short_name": "Labels",
              "doc_url": "https://cloud.google.com/resource-manager/docs/tags/tags-overview",
              "one_line": "Key/value metadata for cost breakdown, filtering, automation triggers.",
              "status": "ga"
            },
            {
              "name": "Resource Manager Tags",
              "short_name": "Tags",
              "doc_url": "https://cloud.google.com/resource-manager/docs/tags/tags-overview",
              "one_line": "Governance-grade tag values referenced by IAM Conditions and org policy rules.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Tagging (defined, free-form, cost-tracking)",
              "short_name": "Tagging",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Tagging/Concepts/taggingoverview.htm",
              "one_line": "Namespaced defined tags with value lists, defaults, and inheritance, plus free-form tags.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "service-catalog",
      "domain": "org-tenancy",
      "title": "Service catalog",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Service Catalog",
              "short_name": "Service Catalog",
              "doc_url": "https://docs.aws.amazon.com/servicecatalog/latest/adminguide/introduction.html",
              "one_line": "Curated portfolios of approved, templated products (CloudFormation/Terraform) that end users self-provision within constraints set by central teams.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Managed Applications and Deployment Environments",
              "short_name": "Managed Apps / ADE",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/managed-applications/overview",
              "one_line": "Curated templated products that internal users deploy themselves inside guardrails: managed applications publish a locked-down resource group, deployment environments hand teams pre-approved infrastructure templates.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Google Cloud Service Catalog",
              "short_name": "Service Catalog",
              "doc_url": "https://cloud.google.com/service-catalog/docs/overview",
              "one_line": "Internal catalogue where an administrator publishes approved solutions and users deploy them into their own projects inside the guardrails set for them.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No curated self-service catalogue. Resource Manager stacks and private Marketplace listings are the nearest path."
        }
      }
    },
    {
      "key": "compliance-pack",
      "domain": "governance-policy",
      "title": "Compliance pack",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Audit Manager (maintenance mode) and AWS Artifact",
              "short_name": "Audit Manager / Artifact",
              "doc_url": "https://docs.aws.amazon.com/audit-manager/latest/userguide/audit-manager-availability-change.html",
              "one_line": "Audit Manager automated evidence collection entering maintenance Apr 2026; Artifact self-serves AWS's own SOC/ISO/PCI attestations.",
              "status": "retiring"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Regulatory compliance (initiatives + Defender standards)",
              "short_name": "Compliance",
              "doc_url": "https://learn.microsoft.com/en-us/azure/governance/policy/samples/",
              "one_line": "Built-in initiative packs mapping controls to CIS/ISO/NIST/PCI plus Microsoft cloud security benchmark scoring.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Security Command Center (compliance & posture)",
              "short_name": "SCC",
              "doc_url": "https://cloud.google.com/security-command-center/docs/security-command-center-overview",
              "one_line": "Misconfiguration/threat findings plus compliance reports against CIS/ISO/NIST benchmarks.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Guard CIS recipe and compliance documents",
              "short_name": "Compliance packs",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/cloud-guard/home.htm",
              "one_line": "Prebuilt CIS Foundation benchmark detector recipe plus downloadable SOC/ISO compliance artifacts in the console.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "config-drift-assessment",
      "domain": "governance-policy",
      "title": "Config drift assessment",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Config Recorder, Configuration Items, Timeline",
              "short_name": "Config recorder",
              "doc_url": "https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html",
              "one_line": "Records point-in-time configuration items and relationships powering timelines, aggregators, and drift-style assessment.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Change tracking (ARG change history + Change Tracking)",
              "short_name": "Drift",
              "doc_url": "https://learn.microsoft.com/en-us/azure/governance/resource-graph/how-to/get-resource-changes",
              "one_line": "Property-level change detection: Resource Graph change history (control plane, ±30 min context in portal) and agent-based in-guest Change Tracking.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Security Command Center security posture service",
              "short_name": "SCC Posture",
              "doc_url": "https://docs.cloud.google.com/security-command-center/docs/security-posture-overview",
              "one_line": "Defines benchmark postures and raises findings whenever resource/config drift occurs outside them.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Resource Manager drift detection",
              "short_name": "Drift detection",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/ResourceManager/Tasks/detect-drift.htm",
              "one_line": "Stack-level drift reports comparing live infrastructure to last-applied Terraform state, per-resource granularity.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "policy-as-code",
      "domain": "governance-policy",
      "title": "Policy as code",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Config Rules and Conformance Packs",
              "short_name": "Config rules",
              "doc_url": "https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config.html",
              "one_line": "Continuous configuration compliance: managed/custom rules, proactive evaluation, org-wide conformance packs bundling rules plus remediations.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Policy as Code",
              "short_name": "PaC",
              "doc_url": "https://learn.microsoft.com/en-us/azure/governance/policy/concepts/policy-as-code",
              "one_line": "Definitions/initiatives/assignments authored in repos, CI-validated, deployed through pipelines with safe-rollout patterns.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Organization Policy custom constraints (+ Terraform validation)",
              "short_name": "PaC",
              "doc_url": "https://cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints",
              "one_line": "CEL-based custom org constraints enforced at resource creation act as the policy-as-code plane.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Security Zones recipes (+ Cloud Guard detectors)",
              "short_name": "Guardrails as code",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/security-zone/home.htm",
              "one_line": "Declarative recipe packs that prevent misconfiguration, with detector/responder recipes evaluating continuously.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "resource-graph-query",
      "domain": "governance-policy",
      "title": "Resource graph query",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Resource Explorer and Config Advanced Queries",
              "short_name": "Resource Explorer",
              "doc_url": "https://aws.amazon.com/resourceexplorer/",
              "one_line": "Index-backed cross-account/region keyword search plus SQL-SELECT-subset queries over Config items; no unified graph query language exists.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Resource Graph",
              "short_name": "ARG",
              "doc_url": "https://learn.microsoft.com/en-us/azure/governance/resource-graph/overview",
              "one_line": "At-scale KQL querying over ARM resource properties across subscriptions/tenants with change-history tables.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Asset Inventory",
              "short_name": "Asset Inventory",
              "doc_url": "https://cloud.google.com/asset-inventory/docs/overview",
              "one_line": "Org-wide asset metadata: export snapshots/feeds to BigQuery/GCS/Pub/Sub, search API, analyzer hooks.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Search (structured resource query language)",
              "short_name": "Resource Search",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Search/Concepts/querysyntax.htm",
              "one_line": "query <type> resources where ... return ... sorted by ... across subscribed regions (up to three in console).",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "alerting",
      "domain": "observability",
      "title": "Alerting",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "CloudWatch Alarms",
              "short_name": "Alarms",
              "doc_url": "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Create_Composite_Alarm.html",
              "one_line": "Metric alarms acting on sustained state change plus composite alarms (AND/OR/NOT expressions) cutting alarm-storm noise.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Monitor alerts",
              "short_name": "Alerts",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview",
              "one_line": "Metric alerts (incl. dynamic thresholds), log-search alerts, activity-log/Service/Resource-health alerts routed via action groups.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Alerting policies & notification channels",
              "short_name": "Alerts",
              "doc_url": "https://cloud.google.com/monitoring/alerts",
              "one_line": "Metric/log/SLO-based alert policies with conditions, duration, and channel fan-out (email/SMS/PagerDuty/webhook/Pub/Sub).",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Alarms (Monitoring)",
              "short_name": "Alarms",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Monitoring/Tasks/managingalarms.htm",
              "one_line": "MQL-defined threshold/absence alarms publishing to Notifications topics or Streaming.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "dashboards",
      "domain": "observability",
      "title": "Dashboards",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "CloudWatch Dashboards",
              "short_name": "Dashboards",
              "doc_url": "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Dashboards.html",
              "one_line": "Cross-account cross-region widget dashboards over metrics, alarms, and log queries.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Dashboards, Workbooks, Managed Grafana",
              "short_name": "Visualization",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-monitor/visualize/workbooks-overview",
              "one_line": "Three visualization layers: pinned portal dashboards, parameterized workbooks, and managed Grafana (Prometheus-first).",
              "status": "ga"
            },
            {
              "name": "Curated insights (VM insights, Container insights, others)",
              "short_name": "Insights",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-monitor/vm/vminsights-overview",
              "one_line": "Packaged dashboards + data collection per workload: VM insights (perf + process maps), Container insights (stdout/stderr/events), App insights dashboards.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Monitoring dashboards",
              "short_name": "Dashboards",
              "doc_url": "https://cloud.google.com/monitoring/charts",
              "one_line": "Custom dashboards (JSON-defined), predefined library, SLO burn views.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Dashboards service",
              "short_name": "Dashboards",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Dashboards/home.htm",
              "one_line": "Console-native dashboard widgets for metrics, logs, and custom HTML, scoped per compartment.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "distributed-tracing",
      "domain": "observability",
      "title": "Distributed tracing",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS X-Ray",
              "short_name": "X-Ray",
              "doc_url": "https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html",
              "one_line": "Distributed tracing with segments/subsegments, annotations (indexed) vs metadata, sampling rules, and 30-day service map.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Application Insights tracing (OpenTelemetry)",
              "short_name": "Tracing",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-overview",
              "one_line": "End-to-end distributed traces via the Azure Monitor OpenTelemetry distro with application map correlation.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Trace",
              "short_name": "Trace",
              "doc_url": "https://cloud.google.com/trace/docs/overview",
              "one_line": "OpenTelemetry-based distributed tracing; spans kept 30 days in _Trace bucket.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "APM Distributed Tracing (Trace Explorer)",
              "short_name": "APM tracing",
              "doc_url": "https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/use-trace-explorer.html",
              "one_line": "OpenTelemetry/OpenTracing span collection with trace explorer query language, browser-to-database views, Functions integration.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "error-reporting",
      "domain": "observability",
      "title": "Error reporting",
      "cells": {
        "aws": {
          "state": "absent",
          "reason": "No automatic exception grouping service. CloudWatch Logs metric filters and Application Signals surface error rates but do not deduplicate stack traces into tracked issues."
        },
        "azure": {
          "state": "elsewhere",
          "reason": "Delivered inside Application Insights, whose failures view groups exceptions by problem ID. Not a separate service.",
          "see": "distributed-tracing"
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Error Reporting",
              "short_name": "ErrRep",
              "doc_url": "https://cloud.google.com/error-reporting/docs/grouping-errors",
              "one_line": "Auto-groups exceptions from ingested logs into error counts with first/last seen tracking.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No automatic exception grouping service. APM traces and Logging searches carry the raw errors."
        }
      }
    },
    {
      "key": "log-store",
      "domain": "observability",
      "title": "Log store",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon CloudWatch Logs",
              "short_name": "CW Logs",
              "doc_url": "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html",
              "one_line": "Log-group storage with never-expire default retention, Logs Insights (QL/PPL/SQL), metric filters, subscription filters, Live Tail, export tasks.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Log Analytics workspaces",
              "short_name": "Log Analytics",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-workspace-overview",
              "one_line": "KQL-queryable log store with three table plans: Analytics (full features), Basic (cheap, query-scanned billing), Auxiliary (cheapest archival-ish ingest).",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Logging",
              "short_name": "Logging",
              "doc_url": "https://cloud.google.com/logging/docs/storage",
              "one_line": "Central log store with Log Router, buckets (_Required 400d locked, _Default 30d), views, Log Analytics SQL.",
              "status": "ga"
            },
            {
              "name": "Log Analytics",
              "short_name": "LogAnalytics",
              "doc_url": "https://cloud.google.com/logging/docs/log-analytics",
              "one_line": "SQL over logs and traces via Observability Analytics (formerly Log Analytics) on upgraded log buckets.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Logging service",
              "short_name": "Logging",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/loggingoverview.htm",
              "one_line": "Unified log store for Audit logs, service logs, and agent/API-ingested custom logs, organized in log groups with a search query language.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "managed-prometheus",
      "domain": "observability",
      "title": "Managed Prometheus",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Managed Service for Prometheus",
              "short_name": "AMP",
              "doc_url": "https://docs.aws.amazon.com/prometheus/latest/userguide/what-is-Amazon-Managed-Service-Prometheus.html",
              "one_line": "Managed Prometheus-compatible metric store queried with PromQL, with agentless collection from EKS and Alertmanager-compatible rules.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Monitor managed service for Prometheus",
              "short_name": "Managed Prometheus",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-monitor/metrics/prometheus-metrics-overview",
              "one_line": "Managed Prometheus-compatible metric store in an Azure Monitor workspace, queried with PromQL and alerted on with Prometheus rule groups.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Google Cloud Managed Service for Prometheus",
              "short_name": "ManagedProm",
              "doc_url": "https://cloud.google.com/stackdriver/docs/managed-prometheus",
              "one_line": "Managed Prometheus collection+store with PromQL; auto-deploy on GKE or self-deployed collectors.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No managed Prometheus store. Prometheus endpoints are scraped into the Monitoring service by the management agent instead."
        }
      }
    },
    {
      "key": "metrics-store",
      "domain": "observability",
      "title": "Metrics store",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon CloudWatch Metrics",
              "short_name": "CW Metrics",
              "doc_url": "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html",
              "one_line": "Regional time-series store: namespaces, up to 30 dimensions, 1-minute standard or 1-second high-resolution, retention rollups (1-min points kept 15 days, hourly 455 days).",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Monitor Metrics",
              "short_name": "Metrics",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-monitor/metrics/data-platform-metrics",
              "one_line": "Time-series database holding free platform metrics (1-minute cadence, 93-day retention) plus custom metrics.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Monitoring metric store",
              "short_name": "Monitoring",
              "doc_url": "https://cloud.google.com/monitoring/docs",
              "one_line": "Time series for every service auto-ingested + custom/OTel/Prometheus metrics; MQL and PromQL query surfaces.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Monitoring service (metrics)",
              "short_name": "Monitoring",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Monitoring/Concepts/monitoringoverview.htm",
              "one_line": "Time-series metric store for service metrics, custom metrics, and Connector Hub-derived metrics, queried in MQL.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "network-diagnostics",
      "domain": "observability",
      "title": "Network diagnostics",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "VPC Reachability Analyzer and Network Access Analyzer",
              "short_name": "Reachability Analyzer",
              "doc_url": "https://docs.aws.amazon.com/vpc/latest/reachability/what-is-reachability-analyzer.html",
              "one_line": "Configuration analysis of network paths: Reachability Analyzer says whether one resource can reach another and names the blocking component, Network Access Analyzer finds which paths exist against a stated intent.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Network Watcher",
              "short_name": "Network Watcher",
              "doc_url": "https://learn.microsoft.com/en-us/azure/network-watcher/network-watcher-overview",
              "one_line": "Diagnostic suite for network paths: connection troubleshoot, IP flow verify, next hop, effective security rules, and packet capture.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Network Intelligence Center",
              "short_name": "NINT",
              "doc_url": "https://cloud.google.com/network-intelligence-center",
              "one_line": "Connectivity Tests, Performance Dashboard, Firewall Insights, Flow Analyzer under one console.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Network Path Analyzer",
              "short_name": "Path Analyzer",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/path_analyzer.htm",
              "one_line": "Traces the intended path between two endpoints across gateways, route tables, security lists, and network security groups, and names what blocks it.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "profiler",
      "domain": "observability",
      "title": "Profiler",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "CloudWatch Application Signals and CodeGuru Profiler",
              "short_name": "App Signals",
              "doc_url": "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Monitoring-Sections.html",
              "one_line": "OTel-based APM with zero-code auto-instrumentation, golden metrics, SLOs, and service map; CodeGuru Profiler continues for JVM flame graphs.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": ".NET Profiler + Snapshot Debugger",
              "short_name": "Profiler",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-monitor/profiler/profiler-overview",
              "one_line": "Production CPU/allocation profiling and exception-triggered debug snapshots for .NET apps.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Profiler",
              "short_name": "Profiler",
              "doc_url": "https://cloud.google.com/profiler/docs/about-profiler",
              "one_line": "Continuous production CPU/heap profiling for Java/Go/Node/Python/.NET/Ruby with 30-day retention.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No managed continuous profiler across languages (AWS CodeGuru Profiler / GCP Cloud Profiler class). Nearest capabilities are Java-only: JMS JFR-based recordings and APM Thread Snapshots (agent/tracer stack snapshots at a 250 ms default interval)."
        }
      }
    },
    {
      "key": "service-health-dashboard",
      "domain": "observability",
      "title": "Service health dashboard",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Health Dashboard",
              "short_name": "AWS Health",
              "doc_url": "https://docs.aws.amazon.com/health/latest/ug/what-is-aws-health.html",
              "one_line": "Account-scoped feed of service events, scheduled changes, and account notifications, naming the resources of yours that are affected.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Service Health",
              "short_name": "Service Health",
              "doc_url": "https://learn.microsoft.com/en-us/azure/service-health/overview",
              "one_line": "Subscription-scoped feed of service issues, planned maintenance, and health advisories, naming the resources of yours that are affected.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Personalized Service Health",
              "short_name": "PSH",
              "doc_url": "https://cloud.google.com/service-health/docs/overview",
              "one_line": "Incident feed scoped to YOUR affected resources/services instead of generic status page.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Console Announcements",
              "short_name": "Announcements",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/General/Concepts/announcements.htm",
              "one_line": "Tenancy-scoped feed of service events, planned maintenance, and required actions, delivered in the console and subscribable through Notifications.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "synthetic-monitoring",
      "domain": "observability",
      "title": "Synthetic monitoring",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "CloudWatch Synthetics Canaries",
              "short_name": "Synthetics",
              "doc_url": "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html",
              "one_line": "Scheduled scripted probes (Node.js/Python/Java, Playwright/Puppeteer/Selenium) run as often as once per minute with screenshots and heartbeat metrics.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Availability tests (standard)",
              "short_name": "Synthetic",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-monitor/app/availability-overview",
              "one_line": "URL ping-style checks executed from Azure points of presence with SSL cert expiry and custom headers.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Uptime checks / Synthetics",
              "short_name": "Synthetic",
              "doc_url": "https://cloud.google.com/monitoring/uptime-checks",
              "one_line": "Global HTTP/HTTPS/TCP/GRPC probes from multiple geographies with alert integration.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "APM Availability Monitoring (synthetics)",
              "short_name": "Synthetics",
              "doc_url": "https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/application-performance-monitoring.html",
              "one_line": "Scheduled Browser/Scripted Browser/REST/Scripted REST/Network/DNS/FTP/SQL monitors from public vantage points, dedicated vantage points, or on-prem workers.",
              "status": "ga"
            },
            {
              "name": "Health Checks service",
              "short_name": "Health Checks",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/HealthChecks/Concepts/healthchecks.htm",
              "one_line": "Lightweight external HTTP/ping probes from global vantage points feeding Traffic Management health evaluation.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "telemetry-agent",
      "domain": "observability",
      "title": "Telemetry agent",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Distro for OpenTelemetry and CloudWatch Agent",
              "short_name": "ADOT / CW Agent",
              "doc_url": "https://aws.amazon.com/otel/",
              "one_line": "ADOT collector distribution (actively released, not deprecated) plus unified CloudWatch agent collecting logs/metrics/traces, StatsD, collectd, OTLP.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Monitor Agent",
              "short_name": "AMA",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-overview",
              "one_line": "Supported collector that ships host logs, performance counters, and events into Log Analytics, with data collection rules deciding what each machine sends.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Ops Agent",
              "short_name": "OpsAgent",
              "doc_url": "https://cloud.google.com/stackdriver/docs/solutions/agents/ops-agent",
              "one_line": "One agent for VM logs+metrics pipelines (third-party apps included) feeding Logging/Monitoring.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Management Agent",
              "short_name": "Management Agent",
              "doc_url": "https://docs.oracle.com/en-us/iaas/management-agents/home.htm",
              "one_line": "Supported collector installed on cloud or on-premises hosts that ships logs, host metrics, and Prometheus scrapes into Logging and Monitoring.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "access-transparency-logs",
      "domain": "audit-telemetry",
      "title": "Access transparency logs",
      "cells": {
        "aws": {
          "state": "absent",
          "reason": "No equivalent stream. CloudTrail records your own principals and the AWS service principals acting on your behalf; it does not record AWS support or operations staff reading your content."
        },
        "azure": {
          "state": "absent",
          "reason": "No equivalent log stream. Customer Lockbox gates Microsoft engineer access behind your approval, so it produces approval records rather than a continuous access log."
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Access Transparency logs",
              "short_name": "AT",
              "doc_url": "https://cloud.google.com/logging/docs/audit",
              "one_line": "Logs when Google personnel access your content, for governance/compliance review.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No equivalent stream. The Audit service records API calls made against your tenancy, not Oracle operations staff access to your content."
        }
      }
    },
    {
      "key": "control-plane-audit-log",
      "domain": "audit-telemetry",
      "title": "Control-plane audit log",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS CloudTrail (management events and Lake)",
              "short_name": "CloudTrail",
              "doc_url": "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/how-cloudtrail-works.html",
              "one_line": "Default-on 90-day Event history; trails deliver JSON to S3/CW Logs/EventBridge (first copy free, about 5-minute typical delivery); Lake offers immutable SQL-queryable stores.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Activity Log",
              "short_name": "Activity Log",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/activity-log",
              "one_line": "Control-plane event stream for ARM operations (create/update/delete, who, when), retained 90 days free.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Admin Activity + System Event audit logs",
              "short_name": "AdminActivity",
              "doc_url": "https://cloud.google.com/logging/docs/audit",
              "one_line": "Always-on immutable records of configuration-changing API calls and Google-side system actions.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Audit service",
              "short_name": "Audit",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Audit/Concepts/auditoverview.htm",
              "one_line": "Automatic recording of every API call to OCI public endpoints (control plane), immutable and always on.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "data-plane-access-log",
      "domain": "audit-telemetry",
      "title": "Data-plane access log",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "CloudTrail Data Events",
              "short_name": "Data events",
              "doc_url": "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html",
              "one_line": "Object/item/invoke-level API logging for S3, Lambda, DynamoDB and more; OFF by default, $0.10 per 100k events, advanced selectors filter by eventName/ARN.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Resource logs (diagnostic settings)",
              "short_name": "Resource logs",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/resource-logs",
              "one_line": "Per-resource operational/audit logs (off by default) covering data-plane access across nearly every service.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Data Access audit logs",
              "short_name": "DataAccess",
              "doc_url": "https://cloud.google.com/logging/docs/audit/configure-data-access",
              "one_line": "Read/write data-plane records OFF by default for most services (BigQuery partially excepted); enable per-service.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Object Storage and File Storage access logs",
              "short_name": "Storage logs",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/loggingoverview.htm",
              "one_line": "Bucket-level read/write access event logs and FSS access logs delivered into the Logging service.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "dns-query-log",
      "domain": "audit-telemetry",
      "title": "DNS query log",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Route 53 Resolver Query Logging",
              "short_name": "DNS query logs",
              "doc_url": "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-query-logs.html",
              "one_line": "Logs VPC-originated and endpoint DNS queries plus DNS Firewall actions to CW Logs/S3/Firehose; cache hits are NOT logged.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "DNS query logging (firewall + resolver)",
              "short_name": "DNS logs",
              "doc_url": "https://learn.microsoft.com/en-us/azure/firewall/monitor-firewall",
              "one_line": "Query visibility comes from Azure Firewall DNS-proxy logs (AZFWDnsQuery) and DNS Private Resolver query logs; public-zone per-query logging is not offered.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud DNS query logging",
              "short_name": "DNS logs",
              "doc_url": "https://cloud.google.com/dns/docs/monitoring",
              "one_line": "Private-zone query records via server policy per network; public-zone logging toggle available.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Private DNS Resolver Query Logging",
              "short_name": "DNS query logs",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/private-dns-logging.htm",
              "one_line": "Per-query private DNS resolver query/response logs (qname, qtype, rcode, latency, protocol, answers) delivered to the Logging service.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "firewall-rules-log",
      "domain": "audit-telemetry",
      "title": "Firewall rules log",
      "cells": {
        "aws": {
          "state": "absent",
          "reason": "Security groups and network ACLs emit no per-rule verdict log; only VPC Flow Logs record accept and reject. Network Firewall alert and flow logs cover the managed firewall layer. See service-specific-log."
        },
        "azure": {
          "state": "absent",
          "reason": "Network security groups emit no per-rule verdict log; virtual network flow logs carry the allow or deny outcome instead. Azure Firewall rule logs cover the managed firewall layer."
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Firewall Rules / NGFW logging",
              "short_name": "FW logs",
              "doc_url": "https://cloud.google.com/firewall/docs/firewall-rules-logging",
              "one_line": "Per-rule connection verdicts (allow/deny) when logging flag set on rule.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "Security lists and network security groups emit no per-rule verdict log; VCN Flow Logs record accepted and rejected traffic. Network Firewall logs cover the managed firewall layer."
        }
      }
    },
    {
      "key": "identity-provider-audit-log",
      "domain": "audit-telemetry",
      "title": "Identity provider audit log",
      "cells": {
        "aws": {
          "state": "absent",
          "reason": "No separate directory audit stream. IAM and IAM Identity Center events land in CloudTrail alongside every other control-plane call, so sign-in analysis shares one pipeline with resource changes."
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Microsoft Entra audit & sign-in logs",
              "short_name": "Entra logs",
              "doc_url": "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/overview-monitoring-health",
              "one_line": "Tenant-level identity control-plane (audit) and authentication (sign-in/non-interactive/service-principal) streams.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "absent",
          "reason": "No separate directory audit stream inside the cloud. Cloud Identity and Workspace admin and login events are recorded in the admin console audit logs and reach Cloud Logging as Admin Activity records."
        },
        "oci": {
          "state": "absent",
          "reason": "No separate directory audit stream. Identity domain events land in the Audit service alongside every other API call."
        }
      }
    },
    {
      "key": "load-balancer-access-log",
      "domain": "audit-telemetry",
      "title": "Load-balancer access log",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "ELB Access Logs",
              "short_name": "LB access logs",
              "doc_url": "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html",
              "one_line": "Per-request ALB/NLB logs gzipped to S3 every 5 minutes per node; disabled by default; only S3 storage cost applies.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Edge and gateway access/firewall logs",
              "short_name": "LB/edge logs",
              "doc_url": "https://learn.microsoft.com/en-us/azure/application-gateway/application-gateway-diagnostics",
              "one_line": "Access and firewall logs from Application Gateway, Front Door, and related edge services delivered via diagnostic settings.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Load balancer request logs",
              "short_name": "LB logs",
              "doc_url": "https://cloud.google.com/load-balancing/docs/https",
              "one_line": "Per-request LB records (enableLogging per backend service) with sampling control.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Load Balancer access and error logs",
              "short_name": "LB logs",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Balance/Tasks/create_log.htm",
              "one_line": "Per-LB access log (one allowed) plus error log capturing request timing, client/proxy IPs, backend address, response provider incl WAF blocks.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "nat-logs",
      "domain": "audit-telemetry",
      "title": "NAT logs",
      "cells": {
        "aws": {
          "state": "absent",
          "reason": "NAT Gateway emits metrics only. Port exhaustion appears as the ErrorPortAllocation metric, and there is no per-translation log."
        },
        "azure": {
          "state": "absent",
          "reason": "NAT Gateway emits metrics only. There is no per-translation log, and SNAT exhaustion is inferred from connection metrics."
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud NAT logs",
              "short_name": "NAT logs",
              "doc_url": "https://cloud.google.com/nat/docs/monitoring",
              "one_line": "Translation events or errors-only mode (port exhaustion drops) per gateway.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "NAT Gateway emits metrics only. There is no per-translation log."
        }
      }
    },
    {
      "key": "network-flow-log",
      "domain": "audit-telemetry",
      "title": "Network flow log",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "VPC Flow Logs",
              "short_name": "Flow Logs",
              "doc_url": "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html",
              "one_line": "ENI-level IP flow records to CloudWatch Logs, S3 (text or Parquet), or Firehose; off by default; excludes DNS resolver, metadata 169.254.169.254, DHCP, NTP traffic.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Virtual network flow logs",
              "short_name": "Flow logs",
              "doc_url": "https://learn.microsoft.com/en-us/azure/network-watcher/vnet-flow-logs-overview",
              "one_line": "L4 IP flow tuples collected at VNet scope every minute into append-only storage blobs, with optional Traffic Analytics enrichment.",
              "status": "ga"
            },
            {
              "name": "Traffic Analytics",
              "short_name": "TA",
              "doc_url": "https://learn.microsoft.com/en-us/azure/network-watcher/traffic-analytics",
              "one_line": "Aggregates raw flow logs with geography/security/topology enrichment into Log Analytics tables.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "VPC Flow Logs",
              "short_name": "FlowLogs",
              "doc_url": "https://cloud.google.com/vpc/docs/flow-logs",
              "one_line": "Sampled per-connection flow records aggregated over configurable intervals (5s-15min) across org/network/subnet/attachment/tunnel scopes.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "VCN Flow Logs",
              "short_name": "Flow Logs",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/vcn-flow-logs.htm",
              "one_line": "Metadata records of accepted/rejected traffic per VNIC, driven by capture filters with sampling rates.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "policy-denied-audit-log",
      "domain": "audit-telemetry",
      "title": "Policy-denied audit log",
      "cells": {
        "aws": {
          "state": "absent",
          "reason": "No dedicated denial stream. Denials appear inside CloudTrail management events with an errorCode of AccessDenied and the policy that produced them."
        },
        "azure": {
          "state": "absent",
          "reason": "No dedicated denial stream. Policy denials appear in the Activity Log as failed operations naming the assignment that blocked them."
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Policy Denied audit logs",
              "short_name": "PolicyDenied",
              "doc_url": "https://cloud.google.com/logging/docs/audit",
              "one_line": "Records requests a service rejects over a security policy violation; always generated, billed, stored in _Default.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No dedicated denial stream. Authorisation failures appear in Audit service records with the failing response code."
        }
      }
    },
    {
      "key": "service-specific-log",
      "domain": "audit-telemetry",
      "title": "Service-specific log",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Service log delivery family (Lambda, EKS control plane, RDS, ElastiCache, MSK, Redshift, CloudFront, WAF)",
              "short_name": "Service logs",
              "doc_url": "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AWS-logs-and-resource-policy.html",
              "one_line": "Per-service opt-in log delivery to CloudWatch Logs/S3/Firehose: Lambda always-on function logs, EKS five control-plane log types all off by default, RDS engine logs, CloudFront standard (best-effort) and real-time (seconds via Kinesis), WAF via Firehose.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Service-specific diagnostic categories",
              "short_name": "Svc logs",
              "doc_url": "https://learn.microsoft.com/en-us/azure/aks/monitor-aks",
              "one_line": "Each service ships named log categories: KeyVault AuditEvent, Storage Transaction/StorageRead..., Cosmos DataPlaneRequests, AKS kube-audit family, SQL SQLSecurityAuditEvents, etc.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Service runtime logs (GKE/AE/Run/GCS legacy...)",
              "short_name": "Svc logs",
              "doc_url": "https://cloud.google.com/logging/docs/view/logs_viewer",
              "one_line": "Each managed service emits its own request/runtime streams into Logging with service-specific fields.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Service logs family (WAF, API Gateway, Functions, OKE, VPN, Data Safe...)",
              "short_name": "Service logs",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/loggingoverview.htm",
              "one_line": "Each service exposes predefined log categories enabled per resource into log groups: WAF request logs, API Gateway execution logs, Functions invoke logs, OKE audit/control-plane logs, Site-to-Site VPN tunnel logs, Data Safe database audit, GoldenGate, MySQL HeatWave, NoSQL, DevOps pipelines.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "ai-safety-guardrails",
      "domain": "security-services",
      "title": "AI safety guardrails",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Bedrock Guardrails",
              "short_name": "Guardrails",
              "doc_url": "https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html",
              "one_line": "Configurable safeguards for generative AI applications: harmful-content filters, denied topics, word filters, sensitive-information redaction, and contextual grounding checks.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure AI Content Safety",
              "short_name": "Content Safety",
              "doc_url": "https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview",
              "one_line": "Detects harmful user-generated and model-generated content in text and images, in front of any model endpoint.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Model Armor",
              "short_name": "ModelArmor",
              "doc_url": "https://cloud.google.com/security-command-center/docs/model-armor-overview",
              "one_line": "Prompt/response safety screening (jailbreak, PI extraction, unsafe content) for LLM endpoints.",
              "status": "preview"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No first-party prompt and response screening service. Safety filtering is whatever the hosted model itself applies."
        }
      }
    },
    {
      "key": "bastion",
      "domain": "security-services",
      "title": "Bastion",
      "cells": {
        "aws": {
          "state": "elsewhere",
          "reason": "Delivered by Systems Manager Session Manager, an agent-brokered shell that needs no open port, no public IP, and no jump host.",
          "see": "config-management"
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Bastion",
              "short_name": "Bastion",
              "doc_url": "https://learn.microsoft.com/en-us/azure/bastion/bastion-overview",
              "one_line": "Browser/native-client jump service exposing SSH/RDP without public IPs on target VMs.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "elsewhere",
          "reason": "Delivered by Identity-Aware Proxy TCP forwarding, which tunnels SSH and RDP to instances that have no public IP.",
          "see": "zero-trust-app-access"
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Bastion",
              "short_name": "Bastion",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Bastion/Concepts/bastionoverview.htm",
              "one_line": "Managed time-boxed SSH/port-forward sessions to private-subnet targets without exposing them publicly.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "cloud-firewall",
      "domain": "security-services",
      "title": "Cloud firewall",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Network Firewall",
              "short_name": "Network Firewall",
              "doc_url": "https://docs.aws.amazon.com/network-firewall/latest/developerguide/rule-groups.html",
              "one_line": "Managed stateless + Suricata-compatible stateful IPS for VPC inspection, deployed centrally in inspection-VPC architectures with TLS inspection.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Firewall",
              "short_name": "AzFW",
              "doc_url": "https://learn.microsoft.com/en-us/azure/firewall/overview",
              "one_line": "Stateful managed firewall-as-a-service with DNAT/SNAT, FQDN filtering, TLS inspection, and IDPS on Premium.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Next Generation Firewall (Cloud NGFW)",
              "short_name": "NGFW",
              "doc_url": "https://cloud.google.com/firewall/docs/firewall-policies",
              "one_line": "VPC firewall rules + hierarchical firewall policies (org/folder) with secure tags and service accounts as targets.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Network Firewall",
              "short_name": "Network Firewall",
              "doc_url": "https://www.oracle.com/cloud/networking/network-firewall/",
              "one_line": "Managed next-gen firewall (powered by Palo Alto Networks technology) with ML-based IPS, TLS inspection options, hub-VCN placement.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "data-classification",
      "domain": "security-services",
      "title": "Data classification",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Macie",
              "short_name": "Macie",
              "doc_url": "https://docs.aws.amazon.com/macie/latest/user/data-discovery.html",
              "one_line": "ML discovery of PII/secrets/payment data in S3 using managed identifiers, scheduled discovery jobs, and $1/GB inspection pricing.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Data Security Posture Management + Purview labels",
              "short_name": "DSPM",
              "doc_url": "https://learn.microsoft.com/en-us/purview/information-protection",
              "one_line": "Automatic sensitive-data discovery across stores feeding Defender CSPM risk views, with Purview sensitivity labeling for documents.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Sensitive Data Protection (ex-DLP)",
              "short_name": "SDP",
              "doc_url": "https://cloud.google.com/sensitive-data-protection/docs",
              "one_line": "Inspect/classify/de-identify PII across GCS/BQ/streams; discovery profiles automate cataloging.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Data Safe (sensitive data discovery and masking)",
              "short_name": "Data Safe",
              "doc_url": "https://docs.oracle.com/en-us/iaas/data-safe/index.html",
              "one_line": "Database-centric security service: sensitive-data discovery/classification, audit collection, masking formats, user assessment.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "packet-mirroring",
      "domain": "security-services",
      "title": "Packet mirroring",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon VPC Traffic Mirroring",
              "short_name": "Traffic Mirroring",
              "doc_url": "https://docs.aws.amazon.com/vpc/latest/mirroring/what-is-traffic-mirroring.html",
              "one_line": "Copies traffic from an elastic network interface to out-of-band security and monitoring appliances for content inspection, threat monitoring, and troubleshooting.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure virtual network TAP",
              "short_name": "VNet TAP",
              "doc_url": "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-tap-overview",
              "one_line": "Streams a virtual machine's network traffic continuously from its network interface to a packet collector or analytics appliance.",
              "status": "preview"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Packet Mirroring",
              "short_name": "PktMirror",
              "doc_url": "https://cloud.google.com/vpc/docs/packet-mirroring",
              "one_line": "Clone instance/subnet traffic to out-of-band collectors (IDS/NDR appliances).",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "VCN Traffic Mirroring (VTAP)",
              "short_name": "VTAP",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/vtap.htm",
              "one_line": "Copies traffic from a source VNIC, subnet, or load balancer to an out-of-band collector for intrusion detection and packet analysis.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "posture-management",
      "domain": "security-services",
      "title": "Posture management",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Security Hub CSPM and Firewall Manager",
              "short_name": "Security Hub CSPM",
              "doc_url": "https://aws.amazon.com/security-hub/cspm/",
              "one_line": "CSPM checks (FSBP, CIS, PCI, NIST) with consolidated controls and scores, org-wide aggregation; Firewall Manager deploys WAF/Shield/NFW/SG policy org-wide.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Defender for Cloud CSPM",
              "short_name": "CSPM",
              "doc_url": "https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-cloud-introduction",
              "one_line": "Secure score, recommendations mapped to the Microsoft cloud security benchmark, attack-path analysis on paid tier.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "SCC posture management (CSPM)",
              "short_name": "CSPM",
              "doc_url": "https://docs.cloud.google.com/security-command-center/docs/security-posture-overview",
              "one_line": "Continuous misconfiguration assessment, attack-path simulation, security health scoring.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Guard (CSPM)",
              "short_name": "Cloud Guard",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/cloud-guard/home.htm",
              "one_line": "Continuous posture assessment: detectors (configuration/activity/threat), problems, responders, global reporting region.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "security-investigation-graph",
      "domain": "security-services",
      "title": "Security investigation graph",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Detective",
              "short_name": "Detective",
              "doc_url": "https://docs.aws.amazon.com/detective/latest/userguide/detective-investigation-about.html",
              "one_line": "Behavior graph over CloudTrail/Flow Logs/GuardDuty findings for triage-scoping-response investigations with finding groups.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "elsewhere",
          "reason": "Delivered inside Microsoft Sentinel, whose investigation graph and entity pages correlate incidents across sources.",
          "see": "threat-detection"
        },
        "gcp": {
          "state": "elsewhere",
          "reason": "Delivered inside Security Command Center Enterprise, which folds in Google SecOps case management and attack-path analysis.",
          "see": "threat-detection"
        },
        "oci": {
          "state": "absent",
          "reason": "No correlated investigation graph. Cloud Guard problems and Threat Intelligence lookups are joined by hand."
        }
      }
    },
    {
      "key": "service-perimeter",
      "domain": "security-services",
      "title": "Service perimeter",
      "cells": {
        "aws": {
          "state": "absent",
          "reason": "No single perimeter object. The equivalent data perimeter is assembled from resource control policies, service control policies, VPC endpoint policies, and resource policy conditions, and it is evaluated per request rather than as one boundary."
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Network Security Perimeter",
              "short_name": "NSP",
              "doc_url": "https://learn.microsoft.com/en-us/azure/private-link/network-security-perimeter-concepts",
              "one_line": "Logical boundary around PaaS resources that blocks public network access by default, with explicit inbound and outbound access rules for the traffic allowed to cross it.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "VPC Service Controls",
              "short_name": "VPC SC",
              "doc_url": "https://cloud.google.com/vpc-service-controls/docs/overview",
              "one_line": "Service perimeters around managed APIs blocking data exfiltration even with valid credentials; dry-run supported.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No API-level perimeter. Security Zones prevent non-compliant resource creation and Zero Trust Packet Routing constrains the network path, but neither blocks a credentialed read from outside the boundary."
        }
      }
    },
    {
      "key": "threat-detection",
      "domain": "security-services",
      "title": "Threat detection",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon GuardDuty",
              "short_name": "GuardDuty",
              "doc_url": "https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html",
              "one_line": "Agentless ML threat detection analyzing CloudTrail, VPC Flow Logs, and DNS logs, with protection plans for S3, EKS Runtime, RDS, Lambda, Malware, and AI workloads.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Microsoft Sentinel + Defender XDR correlation",
              "short_name": "Sentinel",
              "doc_url": "https://learn.microsoft.com/en-us/azure/sentinel/overview",
              "one_line": "Cloud-native SIEM/SOAR running on Log Analytics workspaces with UEBA, watchlists, and incident fusion.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Event Threat Detection / SCC threats (+ Cloud IDS legacy)",
              "short_name": "ETD",
              "doc_url": "https://cloud.google.com/security-command-center/docs/overview-threats",
              "one_line": "Anomaly detection over logs (crypto mining, exfil, brute force); SCC Enterprise extends with runtime insights; Cloud IDS retiring.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Threat Intelligence service",
              "short_name": "Threat Intel",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/threat-intel/home.htm",
              "one_line": "Curated IP reputation intelligence browsable and joinable against flow logs/WAF logs for triage.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "verified-permissions",
      "domain": "security-services",
      "title": "Verified permissions",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Verified Permissions",
              "short_name": "Verified Permissions",
              "doc_url": "https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/what-is-avp.html",
              "one_line": "Fine-grained application authorization using open-source Cedar language (principal-action-resource-context) integrated with Cognito and API Gateway/AppSync.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "absent",
          "reason": "No managed application authorisation service. Application permission models are built on Entra app roles and group claims, or on a self-run policy engine."
        },
        "gcp": {
          "state": "absent",
          "reason": "No managed application authorisation service. Cloud IAM governs Google resources, not your application's own objects."
        },
        "oci": {
          "state": "absent",
          "reason": "No managed application authorisation service. OCI IAM governs OCI resources, not your application's own objects."
        }
      }
    },
    {
      "key": "vulnerability-scanning",
      "domain": "security-services",
      "title": "Vulnerability scanning",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Inspector",
              "short_name": "Inspector",
              "doc_url": "https://docs.aws.amazon.com/inspector/latest/user/scanning-resources.html",
              "one_line": "Continuous scanning of EC2 (SSM-agent based plus agentless snapshot scans), ECR images (enhanced continuous), and Lambda functions/layers/code.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Vulnerability assessment (Defender plans)",
              "short_name": "VA",
              "doc_url": "https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-cloud-introduction",
              "one_line": "Agentless CSPM scanning plus agent-based scanners (Qualys lineage) under Defender for Servers; container registry image scans under Defender for Containers.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Artifact Analysis",
              "short_name": "ArtAnalysis",
              "doc_url": "https://cloud.google.com/artifact-analysis/docs/",
              "one_line": "On-push container/package vulnerability metadata in Artifact Registry & GKE.",
              "status": "ga"
            },
            {
              "name": "Web Security Scanner",
              "short_name": "WSS",
              "doc_url": "https://cloud.google.com/security-command-center/docs/how-to-use-web-security-scanner",
              "one_line": "DAST crawling of App Engine/GKE/Run apps finding XSS/mixed content/clear-text issues.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Vulnerability Scanning service",
              "short_name": "VSS",
              "doc_url": "https://www.oracle.com/security/cloud-security/vulnerability-scanning-service/",
              "one_line": "Agent-based host scans (CVEs/CIS benchmarks/open ports) daily or weekly plus OCIR image scanning on push.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "waf",
      "domain": "security-services",
      "title": "WAF",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS WAF",
              "short_name": "WAF",
              "doc_url": "https://docs.aws.amazon.com/waf/latest/developerguide/how-aws-waf-works.html",
              "one_line": "L7 web ACL firewall with managed rule groups, bot/fraud/DDoS premium groups, CAPTCHA challenges; attaches to CloudFront, ALB, API GW, AppSync, Cognito.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Web Application Firewall",
              "short_name": "WAF",
              "doc_url": "https://learn.microsoft.com/en-us/azure/web-application-firewall/overview",
              "one_line": "OWASP CRS/bot-protection ruleset engine attached to Application Gateway (regional) or Front Door (global).",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Armor WAF (preconfigured rules)",
              "short_name": "WAF",
              "doc_url": "https://cloud.google.com/armor/docs/cloud-armor-overview",
              "one_line": "Managed OWASP-style rule sets (SQLi/XSS/LFI/RFI/RCE/scanners) plus custom CEL rules on LB policies.",
              "status": "ga"
            },
            {
              "name": "reCAPTCHA Enterprise",
              "short_name": "reCAPTCHA",
              "doc_url": "https://cloud.google.com/security/products/recaptcha",
              "one_line": "Fraud/abuse scoring for logins/checkouts with WAF integration (App Firewall).",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Web Application Firewall (WAF)",
              "short_name": "WAF",
              "doc_url": "https://www.oracle.com/security/cloud-security/web-application-firewall/",
              "one_line": "OWASP-rule WAF enforceable globally (edge policy) or regionally on Flexible Load Balancers, with bot management and threat-intel feeds.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "zero-trust-app-access",
      "domain": "security-services",
      "title": "Zero-trust app access",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Verified Access",
              "short_name": "Verified Access",
              "doc_url": "https://docs.aws.amazon.com/verified-access/latest/ug/what-is-verified-access.html",
              "one_line": "VPN-less zero-trust application access evaluating identity (Identity Center/OIDC) and device-posture trust per request with Cedar policies.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Microsoft Entra Private Access",
              "short_name": "Entra Private Access",
              "doc_url": "https://learn.microsoft.com/en-us/entra/global-secure-access/concept-private-access",
              "one_line": "VPN-less access to internal applications through the Global Secure Access client and private connectors, with Conditional Access deciding each session.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Identity-Aware Proxy",
              "short_name": "IAP",
              "doc_url": "https://cloud.google.com/iap/docs/concepts-overview",
              "one_line": "Context-aware zero-trust fronting of web apps and TCP services (SSH/RDP without bastion/VPN).",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No identity-aware application proxy. The Bastion service brokers host sessions, and application access is fronted by the load balancer and WAF."
        }
      }
    },
    {
      "key": "zero-trust-routing",
      "domain": "security-services",
      "title": "Zero-trust routing",
      "cells": {
        "aws": {
          "state": "absent",
          "reason": "No attribute-based network intent layer. Reachability is decided by route tables, security groups, and network ACLs, all of which resolve to addresses and groups rather than resource attributes."
        },
        "azure": {
          "state": "absent",
          "reason": "No attribute-based network intent layer. Application security groups come closest by grouping interfaces by role, but rules still resolve to addresses and ports."
        },
        "gcp": {
          "state": "absent",
          "reason": "Secure tags on firewall policies come closest, letting rules reference resource tags instead of addresses, but they do not constrain the path independently of the underlying network the way an intent policy does."
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Zero Trust Packet Routing (ZPR)",
              "short_name": "ZPR",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/zero-trust-packet-routing/overview.htm",
              "one_line": "Attribute-based intent policies enforcing network access on tagged resources regardless of underlying NSG/security-list sprawl.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "artifact-registry",
      "domain": "iac-deployment",
      "title": "Artifact registry",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS CodeArtifact",
              "short_name": "CodeArtifact",
              "doc_url": "https://aws.amazon.com/codeartifact/",
              "one_line": "Managed npm/Maven/PyPI/NuGet package registry proxying public repos and hosting private packages (containers live in ECR).",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Artifacts",
              "short_name": "Artifacts",
              "doc_url": "https://learn.microsoft.com/en-us/azure/devops/artifacts/overview",
              "one_line": "Universal package feed (NuGet/npm/Maven/PyPI/upstreams) inside Azure DevOps; ACR covers containers.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Artifact Registry",
              "short_name": "AR",
              "doc_url": "https://cloud.google.com/artifact-registry/docs/overview",
              "one_line": "Multi-format artifact repository (images, language packages, OS packages) with remote repos.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Artifact Registry",
              "short_name": "Artifacts",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/artifacts/home.htm",
              "one_line": "Generic artifact repository (zip, jar, helm tgz, manifests) with mutable/immutable semantics consumed by DevOps deployments.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "cicd-pipeline",
      "domain": "iac-deployment",
      "title": "CI/CD pipeline",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS CodePipeline, CodeBuild, CodeConnections, CodeCommit",
              "short_name": "Code* CI",
              "doc_url": "https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome-introducing.html",
              "one_line": "Pipeline orchestrator (V1/V2), buildspec-driven CodeBuild, CodeConnections to GitHub/GitLab/Bitbucket; CodeCommit reopened to new customers Nov 25 2025 after July 2024 closure.",
              "status": "ga"
            },
            {
              "name": "AWS CodeDeploy",
              "short_name": "CodeDeploy",
              "doc_url": "https://docs.aws.amazon.com/codedeploy/latest/userguide/welcome.html",
              "one_line": "Deployment automation for EC2/on-prem (in-place or blue-green), Lambda (canary/linear/all-at-once alias shifting with hooks), ECS (task-set blue-green).",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure DevOps Pipelines + GitHub Actions",
              "short_name": "Pipelines",
              "doc_url": "https://learn.microsoft.com/en-us/azure/devops/pipelines/get-started/what-is-azure-pipelines",
              "one_line": "First-party CI/CD: Azure Pipelines (classic/YAML, self-hosted agents) and GitHub Actions with OIDC federation to Azure.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Build",
              "short_name": "Build",
              "doc_url": "https://cloud.google.com/build/docs/overview",
              "one_line": "Serverless CI: container-step builds, triggers from repos/PRs, private pools, SBOM/provenance output.",
              "status": "ga"
            },
            {
              "name": "Cloud Source Repositories",
              "short_name": "CSR",
              "doc_url": "https://cloud.google.com/source-repositories/docs",
              "one_line": "Private git hosting deprecated/shut down - migrate to external git hosts.",
              "status": "retiring"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "DevOps service (build + deploy pipelines)",
              "short_name": "OCI DevOps",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/devops/using/deployment_pipelines.htm",
              "one_line": "Integrated CI/CD: managed Git repos, build runners, artifact delivery, deployment pipelines to OKE/instances/Functions with approval gates.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "config-management",
      "domain": "iac-deployment",
      "title": "Config management",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Systems Manager",
              "short_name": "SSM",
              "doc_url": "https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html",
              "one_line": "State Manager desired-state associations, Run Command remote execution, Patch Manager baselines, Session Manager shell without SSH ports.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Machine Configuration (guest config/DSC)",
              "short_name": "Machine Config",
              "doc_url": "https://learn.microsoft.com/en-us/azure/governance/machine-configuration/",
              "one_line": "Audit/enforce in-guest state (files, registry, packages, scripts) via Policy guest-configuration assignments.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Config Sync / Config Controller",
              "short_name": "ConfigSync",
              "doc_url": "https://cloud.google.com/kubernetes-engine/docs/config-sync-overview",
              "one_line": "GitOps reconciliation of K8s + selected GCP configs across fleets (ex-Anthos Config Management).",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "OS Management Hub",
              "short_name": "OSMH",
              "doc_url": "https://docs.oracle.com/en-us/iaas/osmh/doc/home.htm",
              "one_line": "Patch and configure Oracle Linux/Windows/Ubuntu fleets across OCI, on-premises, and third-party clouds; groups, lifecycle stages, versioned software sources, Ksplice.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "iac-in-code-sdk",
      "domain": "iac-deployment",
      "title": "IaC-in-code SDK",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS SDKs (boto3, JS v3, Java, .NET, Go)",
              "short_name": "SDKs",
              "doc_url": "https://aws.amazon.com/developer/tools/",
              "one_line": "Language SDKs calling provisioning APIs imperatively; CDK Toolkit Library embeds synth/deploy programmatically.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Pulumi Azure Native / CDKTF",
              "short_name": "In-code IaC",
              "doc_url": "https://www.pulumi.com/registry/packages/azure-native/",
              "one_line": "Third-party imperative-language IaC generating ARM calls (Pulumi Azure Native) or Terraform (CDKTF).",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "absent",
          "reason": "No first-party imperative-in-code IaC SDK. Nearest: CDK for Terraform / Pulumi (third-party) generating google provider calls, plus client libraries + gcloud scripting; Infrastructure Manager runs the resulting plans."
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "CDK for Terraform with OCI provider / OCI SDKs",
              "short_name": "CDKTF + SDKs",
              "doc_url": "https://registry.terraform.io/providers/oracle/oci/latest/docs",
              "one_line": "Declarative IaC from code via CDKTF over the oracle/oci provider, or imperative provisioning through first-class SDKs (Python, Java, TypeScript, Go, Ruby) and the CLI.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "kubernetes-config-management",
      "domain": "iac-deployment",
      "title": "Kubernetes config management",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Controllers for Kubernetes",
              "short_name": "ACK",
              "doc_url": "https://aws-controllers-k8s.github.io/community/docs/community/overview/",
              "one_line": "Service-specific Kubernetes controllers that expose AWS resources as custom resources so kubectl and GitOps manage cloud objects.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Service Operator",
              "short_name": "ASO",
              "doc_url": "https://azure.github.io/azure-service-operator/",
              "one_line": "Kubernetes operator that exposes Azure resources as custom resources so one control plane reconciles both cluster workloads and cloud objects.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Config Connector",
              "short_name": "KCC",
              "doc_url": "https://cloud.google.com/config-connector/docs/overview",
              "one_line": "GCP resources as Kubernetes CRDs so kubectl/IaC-of-record manage cloud objects.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No first-party operator that exposes OCI resources as Kubernetes custom resources."
        }
      }
    },
    {
      "key": "native-iac-template",
      "domain": "iac-deployment",
      "title": "Native IaC template",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS CloudFormation",
              "short_name": "CloudFormation",
              "doc_url": "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html",
              "one_line": "Native declarative YAML/JSON templates, stacks, change sets, automatic rollback, StackSets multi-account deployment, drift detection, IaC generator import.",
              "status": "ga"
            },
            {
              "name": "AWS Cloud Development Kit",
              "short_name": "CDK",
              "doc_url": "https://docs.aws.amazon.com/cdk/v2/guide/home.html",
              "one_line": "Infrastructure in TypeScript/Python/Java/C#/Go synthesized to CloudFormation with L1/L2/L3 constructs and CDK Pipelines.",
              "status": "ga"
            },
            {
              "name": "AWS SAM (Serverless Application Model)",
              "short_name": "SAM",
              "doc_url": "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html",
              "one_line": "CloudFormation shorthand transform for serverless with sam CLI local invoke/emulate, sync, and DeploymentPreference canary wiring to CodeDeploy.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Deployment Stacks",
              "short_name": "Stacks",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deployment-stacks",
              "one_line": "Grouping ARM/Bicep deployments into a managed unit with lifecycle delete and optional deny-write/delete protections.",
              "status": "ga"
            },
            {
              "name": "ARM templates (JSON)",
              "short_name": "ARM",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/overview",
              "one_line": "Original declarative JSON template language executing through Resource Manager with incremental/complete modes.",
              "status": "ga"
            },
            {
              "name": "Bicep",
              "short_name": "Bicep",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview",
              "one_line": "Microsoft's DSL transpiling to ARM JSON: symbolic references, modules, typed params, no state file.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Infrastructure Manager",
              "short_name": "InfraMgr",
              "doc_url": "https://cloud.google.com/infrastructure-manager/docs/overview",
              "one_line": "Google-managed Terraform deployments: state hosted, drift detection, service-agent driven.",
              "status": "ga"
            },
            {
              "name": "Cloud Deployment Manager",
              "short_name": "DM",
              "doc_url": "https://cloud.google.com/deployment-manager/docs/deprecations",
              "one_line": "Original YAML/python template engine - deprecated; existing deployments need migration plans.",
              "status": "deprecated"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Resource Manager (managed Terraform)",
              "short_name": "Resource Manager",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/ResourceManager/Concepts/resourcemanager.htm",
              "one_line": "Terraform-as-a-service: stacks from zip/Git/compartment-scan, plan/apply/destroy/import-state/drift jobs, server-side state locking.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "progressive-delivery",
      "domain": "iac-deployment",
      "title": "Progressive delivery",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Progressive delivery set (CodeDeploy configs, AppConfig flags, API Gateway canary stages, Lambda aliases)",
              "short_name": "Progressive delivery",
              "doc_url": "https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html",
              "one_line": "Traffic-shifting deploys per compute type, feature-flag gradual rollout with validators, alarm-triggered auto-rollback, manual approval gates.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Deployment slots & revision traffic-splitting",
              "short_name": "Progressive",
              "doc_url": "https://learn.microsoft.com/en-us/azure/app-service/deploy-staging-slots",
              "one_line": "Native canary primitives: App Service slot swap with warmup, Container Apps revisions with weighted traffic.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Deploy",
              "short_name": "Deploy",
              "doc_url": "https://cloud.google.com/deploy/docs/overview",
              "one_line": "Delivery pipelines to GKE/Cloud Run with canary/blue-green targets, approvals, rollback.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Blue-green and canary deployment strategies",
              "short_name": "Progressive delivery",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/devops/using/bgoke_deploy.htm",
              "one_line": "Built-in blue/green (namespace swap + NGINX ingress shift) and canary (weighted traffic shift) strategies for OKE and instance groups.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "terraform-provider",
      "domain": "iac-deployment",
      "title": "Terraform provider",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Terraform AWS Provider and AWSCC Provider",
              "short_name": "Terraform on AWS",
              "doc_url": "https://registry.terraform.io/providers/hashicorp/aws/latest/docs",
              "one_line": "hashicorp/aws community-standard provider plus weekly-generated awscc provider exposing CloudFormation registry resources via Cloud Control API.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Terraform/OpenTofu azurerm provider",
              "short_name": "azurerm",
              "doc_url": "https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs",
              "one_line": "HashiCorp-style provider tracking Azure resources in tfstate with plan/apply workflow.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Terraform google/google-beta providers",
              "short_name": "Terraform",
              "doc_url": "https://registry.terraform.io/providers/hashicorp/google/latest/docs",
              "one_line": "HashiCorp-maintained provider covering the GCP surface; google-beta tracks pre-GA resources.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Terraform OCI provider (oracle/oci)",
              "short_name": "TF provider",
              "doc_url": "https://registry.terraform.io/providers/oracle/oci/latest/docs",
              "one_line": "HashiCorp-provider covering essentially every OCI resource; used standalone or inside Resource Manager.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "api-gateway",
      "domain": "integration-messaging",
      "title": "API gateway",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon API Gateway",
              "short_name": "API Gateway",
              "doc_url": "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html",
              "one_line": "REST (regional/edge/private, usage plans, mapping templates, WAF, canary stages) vs HTTP APIs (~70% cheaper, JWT authorizer native) vs WebSocket APIs.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure API Management",
              "short_name": "APIM",
              "doc_url": "https://learn.microsoft.com/en-us/azure/api-management/api-management-key-concepts",
              "one_line": "Full API gateway: policies (throttle/JWT/cache), versions/revisions, developer portal, self-hosted gateway.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "API Gateway",
              "short_name": "APIGW",
              "doc_url": "https://cloud.google.com/api-gateway/docs/about-api-gateway",
              "one_line": "OpenAPI/gRPC-config-driven managed gateway (ESPv2) fronting serverless backends.",
              "status": "ga"
            },
            {
              "name": "Apigee X",
              "short_name": "Apigee",
              "doc_url": "https://cloud.google.com/apigee/docs/api-platform/get-started/what-apigee",
              "one_line": "Full API lifecycle platform: policies, mediation, developer portal, monetization, analytics; named in PCA guide.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "API Gateway",
              "short_name": "API GW",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/APIGateway/Concepts/apigatewayconcepts.htm",
              "one_line": "Regional gateways exposing backend routes (Functions, HTTP, private endpoints) with auth, rate limiting, usage plans, SDK generation.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "event-bus",
      "domain": "integration-messaging",
      "title": "Event bus",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon EventBridge (buses, Pipes, Scheduler, Schema Registry)",
              "short_name": "EventBridge",
              "doc_url": "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-bus.html",
              "one_line": "Serverless event buses routing AWS/partner/custom events via JSON pattern rules to five targets per rule; Pipes for filtered point-to-point; Scheduler for timed invokes.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Event Grid",
              "short_name": "Event Grid",
              "doc_url": "https://learn.microsoft.com/en-us/azure/event-grid/overview",
              "one_line": "Discrete-event routing fabric delivering push notifications to 20+ handlers with filtering and retries.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Eventarc",
              "short_name": "Eventarc",
              "doc_url": "https://cloud.google.com/eventarc/docs/overview",
              "one_line": "Standardized CloudEvents routing from 100+ sources to Run/functions/Workflows/GKE via triggers/channels/pipelines.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Events service",
              "short_name": "Events",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Events/Concepts/eventsoverview.htm",
              "one_line": "Rules reacting to structured service events (object created, instance launched, etc.) triggering Functions/Topics/Streams.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "graphql-api",
      "domain": "integration-messaging",
      "title": "GraphQL API",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS AppSync",
              "short_name": "AppSync",
              "doc_url": "https://docs.aws.amazon.com/appsync/latest/devguide/what-is-appsync.html",
              "one_line": "Serverless GraphQL APIs with typed schema, resolvers, subscriptions, plus AppSync Events WebSocket broadcast (Mar 2025).",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "absent",
          "reason": "No managed general-purpose GraphQL service. Data API builder and the Fabric GraphQL API cover narrower cases."
        },
        "gcp": {
          "state": "absent",
          "reason": "No managed GraphQL service. GraphQL is served from Cloud Run or App Engine, or fronted by Apigee."
        },
        "oci": {
          "state": "absent",
          "reason": "No managed GraphQL service."
        }
      }
    },
    {
      "key": "managed-integration",
      "domain": "integration-messaging",
      "title": "Managed integration",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Transfer Family and Amazon MQ",
              "short_name": "Transfer Family / MQ",
              "doc_url": "https://docs.aws.amazon.com/transfer/latest/userguide/what-is-aws-transfer-family.html",
              "one_line": "Managed SFTP/FTPS/FTP/AS2 file transfer into S3/EFS; MQ runs ActiveMQ 5.x and RabbitMQ 3.13/4.2 brokers for protocol lift-and-shift.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Integration connectors & App Configuration",
              "short_name": "iPaaS extras",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-app-configuration/overview",
              "one_line": "Connector library powering Logic Apps/Power Platform plus App Configuration for centralized feature flags/settings.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Application Integration (+ Integration Connectors)",
              "short_name": "AppInt",
              "doc_url": "https://cloud.google.com/application-integration/docs/overview",
              "one_line": "Low-code iPaaS flows with 150+ managed connectors for enterprise SaaS/DB integration.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Oracle Integration 3 (OIC)",
              "short_name": "OIC",
              "doc_url": "https://docs.oracle.com/en-us/iaas/application-integration/",
              "one_line": "Enterprise iPaaS: adapters, recipes, process automation, B2B, RPA, and AI-agent connectivity (integrations exposed as MCP servers).",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "message-queue",
      "domain": "integration-messaging",
      "title": "Message queue",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon SQS",
              "short_name": "SQS",
              "doc_url": "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html",
              "one_line": "Standard queues (at-least-once, near-unlimited throughput) and FIFO queues (exactly-once processing, ordering in message groups, high-throughput mode).",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Service Bus queues (+ Storage Queues)",
              "short_name": "SB Queues",
              "doc_url": "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview",
              "one_line": "Enterprise broker queues with FIFO sessions, dead-lettering, transactions, duplicate detection.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Tasks",
              "short_name": "Tasks",
              "doc_url": "https://cloud.google.com/tasks/docs",
              "one_line": "Asynchronous task queues (push/pull) with per-queue rate/dispatch control and retries.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Queue",
              "short_name": "Queue",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/queue/overview.htm",
              "one_line": "Serverless SQS-style queue with STOMP and REST interfaces, at-least-once delivery, best-effort ordering.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "mqtt-broker",
      "domain": "integration-messaging",
      "title": "MQTT broker",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS IoT Core",
              "short_name": "IoT Core",
              "doc_url": "https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html",
              "one_line": "Managed MQTT/MQTT-over-WSS device brokering with Rules routing device data into AWS services.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure IoT Hub",
              "short_name": "IoT Hub",
              "doc_url": "https://learn.microsoft.com/en-us/azure/iot-hub/iot-concepts-and-iot-hub",
              "one_line": "Managed device broker over MQTT, AMQP, and HTTPS with per-device identity, device twins for state, and routing of device messages into other services.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "absent",
          "reason": "Cloud IoT Core was retired in 2023, so there is no first-party device broker. Google directs customers to partner platforms feeding Pub/Sub."
        },
        "oci": {
          "state": "absent",
          "reason": "No managed MQTT device broker."
        }
      }
    },
    {
      "key": "pub-sub",
      "domain": "integration-messaging",
      "title": "Pub-sub",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon SNS",
              "short_name": "SNS",
              "doc_url": "https://docs.aws.amazon.com/sns/latest/dg/welcome.html",
              "one_line": "Pub/sub fan-out to SQS, Lambda, HTTP(S), email, SMS, mobile push, Firehose, with JSON filter policies and FIFO topics.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Service Bus topics/subscriptions",
              "short_name": "Topics",
              "doc_url": "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-queues-topics-subscriptions",
              "one_line": "Brokered publish-subscribe with filtered subscriptions and SQL-style filter language.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Pub/Sub",
              "short_name": "Pub/Sub",
              "doc_url": "https://cloud.google.com/pubsub/docs/overview",
              "one_line": "Global messaging: topics/subscriptions (pull/push/BigQuery), ordering keys, exactly-once delivery, schemas.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Notifications",
              "short_name": "Notifications",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Notification/Concepts/notificationoverview.htm",
              "one_line": "Pub/sub fan-out topics delivering to Email, SMS, HTTPS webhook, Slack, PagerDuty, or Functions with confirmation and retries.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "realtime-messaging",
      "domain": "integration-messaging",
      "title": "Realtime messaging",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "API Gateway WebSocket APIs",
              "short_name": "WebSocket APIs",
              "doc_url": "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api.html",
              "one_line": "Managed two-way WebSocket connections to browsers and devices, routing inbound frames by a route key and pushing server-initiated messages back through a management API.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "SignalR Service / Web PubSub",
              "short_name": "Realtime",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-signalr/signalr-overview",
              "one_line": "Managed WebSocket pub/sub pushing realtime updates to browsers/devices at scale.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Firebase Realtime Database and Cloud Firestore listeners",
              "short_name": "Firebase listeners",
              "doc_url": "https://firebase.google.com/docs/database",
              "one_line": "Client SDKs hold an open connection and receive document or node changes as they happen, so the database itself is the fan-out path to browsers and devices.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No managed WebSocket fan-out service."
        }
      }
    },
    {
      "key": "scheduler-jobs",
      "domain": "integration-messaging",
      "title": "Scheduler jobs",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon EventBridge Scheduler",
              "short_name": "EventBridge Scheduler",
              "doc_url": "https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html",
              "one_line": "Serverless scheduler for one-time and recurring jobs, with cron and rate expressions, an explicit time zone, and an optional flexible time window.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "absent",
          "reason": "No standalone cron service since Azure Scheduler retired. Timer-triggered Functions, Logic Apps recurrence, and Automation schedules cover it."
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Scheduler",
              "short_name": "Scheduler",
              "doc_url": "https://cloud.google.com/scheduler/docs",
              "one_line": "Cron-as-a-service triggering HTTP/Pub/Sub/App Engine targets.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No general cron service. Resource Scheduler starts and stops resources on a schedule, and Functions plus Events cover the rest."
        }
      }
    },
    {
      "key": "telemetry-export-pipeline",
      "domain": "integration-messaging",
      "title": "Telemetry export pipeline",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "CloudWatch Logs subscription filters",
              "short_name": "Subscription filters",
              "doc_url": "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/SubscriptionFilters.html",
              "one_line": "Near real-time delivery of log events out of CloudWatch Logs to Data Firehose, Kinesis Data Streams, or Lambda, and on to storage, OpenSearch, or a third party.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Monitor diagnostic settings",
              "short_name": "Diagnostic settings",
              "doc_url": "https://learn.microsoft.com/en-us/azure/azure-monitor/platform/diagnostic-settings",
              "one_line": "Per-resource routing of platform logs and metrics to Log Analytics, a storage account, an event hub, or a partner destination.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Logging Log Router sinks",
              "short_name": "Log Router",
              "doc_url": "https://cloud.google.com/logging/docs/routing/overview",
              "one_line": "Routes every log entry through inclusion and exclusion filters to sinks that land it in Cloud Storage, BigQuery, Pub/Sub, another log bucket, or a third party.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Connector Hub (telemetry egress)",
              "short_name": "Connector Hub",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/connector-hub/overview.htm",
              "one_line": "Managed pipelines moving logs, metrics, queue/stream payloads between OCI services and out to Object Storage, Functions, Notifications, Log Analytics, or Streaming - the standard export path for building on telemetry.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "workflow-orchestration",
      "domain": "integration-messaging",
      "title": "Workflow orchestration",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon MWAA",
              "short_name": "MWAA",
              "doc_url": "https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html",
              "one_line": "Managed Apache Airflow running scheduler/workers as Fargate in your VPC for analytics pipeline orchestration.",
              "status": "ga"
            },
            {
              "name": "AWS Step Functions",
              "short_name": "Step Functions",
              "doc_url": "https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html",
              "one_line": "State-machine workflows in Amazon States Language: Standard (exactly-once, 1 year, per-transition) vs Express (at-least-once, 5 minutes, per-request); Map/Distributed Map, callbacks, human approval.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Logic Apps (+ Durable Functions)",
              "short_name": "Logic Apps",
              "doc_url": "https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-overview",
              "one_line": "Visual iPaaS workflows with 1000+ managed connectors; Durable Functions offers code-first orchestration.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cloud Composer (Managed Airflow)",
              "short_name": "Composer",
              "doc_url": "https://cloud.google.com/composer/docs/concepts/overview",
              "one_line": "Managed Apache Airflow 2/3 for data pipeline DAG orchestration.",
              "status": "ga"
            },
            {
              "name": "Workflows",
              "short_name": "Workflows",
              "doc_url": "https://cloud.google.com/workflows/docs/overview",
              "one_line": "YAML state orchestration calling APIs/services with retries, subworkflows, callbacks.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No generally available first-party workflow orchestrator with product documentation: OCI Workflows was announced as Limited Availability in October 2022 with a blog post as its only citation and has no docs.oracle.com documentation (all candidate paths return 404). Nearest current answers: Oracle Integration 3 process automation for integration/approval flows, and Functions + Events + Connector Hub chains for event-driven orchestration."
        }
      }
    },
    {
      "key": "agent-platform",
      "domain": "ai-ml",
      "title": "Agent platform",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Bedrock AgentCore",
              "short_name": "AgentCore",
              "doc_url": "https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html",
              "one_line": "Modular agent platform (Runtime, Gateway MCP tools, Memory, Identity, Code Interpreter, Browser, Observability) GA Oct 13 2025; Bedrock Agents Classic in maintenance mode June 30 2026.",
              "status": "ga"
            },
            {
              "name": "Amazon Q Business and Amazon Kendra",
              "short_name": "Q Business / Kendra",
              "doc_url": "https://aws.amazon.com/q/business/",
              "one_line": "Both in maintenance mode since June 30 2026 and closed to new customers July 30 2026; Kendra migrates to Bedrock Knowledge Bases, Q Business succeeds into Amazon Quick.",
              "status": "retiring"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Foundry Agent Service (+ Copilot Studio)",
              "short_name": "Agents",
              "doc_url": "https://learn.microsoft.com/en-us/azure/ai-services/agents/overview",
              "one_line": "Managed agent runtime with tools, threads, and evaluation hooks; identities governed by Entra Agent ID.",
              "status": "preview"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Agentspace / Gemini Enterprise Agent Platform",
              "short_name": "AgentPlatform",
              "doc_url": "https://cloud.google.com/agentspace/docs/overview",
              "one_line": "Agent build/run/search surface: Agent Runtime (ex-Agent Engine), Agent Search, enterprise agents UI.",
              "status": "preview"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Generative AI Agents",
              "short_name": "GenAI Agents",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/home.htm",
              "one_line": "Managed RAG/SQL/function-tool agent platform with knowledge bases over Object Storage and OpenSearch (GA March 2025).",
              "status": "ga"
            },
            {
              "name": "Digital Assistant (ODA)",
              "short_name": "ODA",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/digital-assistant/index.html",
              "one_line": "Chatbot builder with skills, channels, and prebuilt integrations, callable against GenAI Agents endpoints.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "managed-model-api",
      "domain": "ai-ml",
      "title": "Managed model API",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Bedrock",
              "short_name": "Bedrock",
              "doc_url": "https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html",
              "one_line": "Managed foundation-model APIs (Anthropic, Meta, Mistral, Amazon Nova and others) with on-demand, batch (-50%), and provisioned throughput pricing.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Microsoft Foundry Models (Azure OpenAI + model catalog)",
              "short_name": "Foundry Models",
              "doc_url": "https://learn.microsoft.com/en-us/azure/ai-foundry/openai/overview",
              "one_line": "Hosted frontier/open model inference (GPT, o-series, DeepSeek, Llama...) with PTU provisioned throughput or PAYG tokens.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Vertex AI Gemini models + Model Garden",
              "short_name": "Gemini@Vertex",
              "doc_url": "https://cloud.google.com/vertex-ai/generative-ai/docs/learn/overview",
              "one_line": "Managed frontier/open model APIs (Gemini family, 200+ Model Garden models) with tuned endpoints.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Generative AI service",
              "short_name": "GenAI",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm",
              "one_line": "Hosted foundation-model inference (Cohere, Meta Llama, Google Gemini by region) with fine-tuning (T-Few/LoRA), dedicated AI clusters, and content moderation.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "managed-rag-pipeline",
      "domain": "ai-ml",
      "title": "Managed RAG pipeline",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon Bedrock Knowledge Bases",
              "short_name": "Bedrock KBs",
              "doc_url": "https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html",
              "one_line": "Managed RAG pipelines: connectors, embedding, retrieval, cited generation; managed vector store or customer-managed OpenSearch/Aurora/Neptune options.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure AI Search integrated vectorization",
              "short_name": "Integrated vectorization",
              "doc_url": "https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization",
              "one_line": "Indexer pipeline that pulls source documents, chunks them, calls an embedding model, and writes vectors into a searchable index, then embeds the query at search time.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Vertex AI RAG Engine",
              "short_name": "RAG",
              "doc_url": "https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview",
              "one_line": "Managed retrieval-augmented generation pipeline wiring sources -> Vector Search -> model responses.",
              "status": "preview"
            }
          ]
        },
        "oci": {
          "state": "elsewhere",
          "reason": "Delivered inside Generative AI Agents, whose knowledge bases index Object Storage and OpenSearch content for grounded answers.",
          "see": "agent-platform"
        }
      }
    },
    {
      "key": "model-training-platform",
      "domain": "ai-ml",
      "title": "Model training platform",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon SageMaker AI",
              "short_name": "SageMaker AI",
              "doc_url": "https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html",
              "one_line": "Build-train-tune-deploy platform (renamed from SageMaker Dec 2024) with Unified Studio GA Mar 2025 unifying EMR/Glue/Athena/Redshift/Bedrock tooling.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Machine Learning",
              "short_name": "Azure ML",
              "doc_url": "https://learn.microsoft.com/en-us/azure/machine-learning/overview-what-is-azure-machine-learning",
              "one_line": "Training/tuning/registry/deployment studio for classical ML and fine-tuning with managed compute.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Vertex AI training/tuning/pipelines",
              "short_name": "Training",
              "doc_url": "https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform",
              "one_line": "Custom training jobs, hyperparameter tuning, pipelines (KFP), feature store, model registry, endpoints.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Data Science service (+AI Infrastructure)",
              "short_name": "Data Science",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/data-science/using/home.htm",
              "one_line": "Notebooks, Jobs, ML Pipelines, AutoML, Model Deployment endpoints on flexible/GPU shapes, plus Supercluster-class training infrastructure beneath.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "speech-vision-document-ai",
      "domain": "ai-ml",
      "title": "Speech, vision and document AI",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Applied AI services (Transcribe, Polly, Rekognition, Textract, Comprehend, Translate, Lex)",
              "short_name": "Applied AI",
              "doc_url": "https://docs.aws.amazon.com/transcribe/latest/dg/what-is-transcribe.html",
              "one_line": "Speech-to-text (streaming/batch, HIPAA eligible), text-to-speech voices, image/video analysis, document OCR/forms/tables/queries, NLP entity-sentiment-PII, translation, conversational bots.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Foundry Tools: Speech, Vision, Document Intelligence",
              "short_name": "Speech/Vision/DocAI",
              "doc_url": "https://learn.microsoft.com/en-us/azure/ai-services/",
              "one_line": "Specialist cognitive services: speech-to-text/translation, OCR/image analysis, and structured document extraction.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Speech-to-Text, Translation, Vision, Document AI",
              "short_name": "AI APIs",
              "doc_url": "https://cloud.google.com/document-ai/docs/overview",
              "one_line": "Pretrained speech transcription, translation, image analysis, and document processors/extraction APIs.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Speech (ASR/TTS)",
              "short_name": "Speech",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/speech/using/speech.htm",
              "one_line": "Transcription with diarization, Whisper model option, live transcription, and text-to-speech synthesis.",
              "status": "ga"
            },
            {
              "name": "Vision",
              "short_name": "Vision",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/vision/using/home.htm",
              "one_line": "Image classification, object/text detection (OCR), document AI extraction of tables and forms.",
              "status": "ga"
            },
            {
              "name": "Language",
              "short_name": "Language",
              "doc_url": "https://www.oracle.com/artificial-intelligence/language/",
              "one_line": "Sentiment, entity extraction, key phrases, translation, and text classification APIs.",
              "status": "ga"
            },
            {
              "name": "Document Understanding",
              "short_name": "Doc AI",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/document-understanding/using/home.htm",
              "one_line": "Key-value extraction from documents (invoices, receipts, IDs) via prebuilt models and REST/CLI.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "vector-store",
      "domain": "ai-ml",
      "title": "Vector store",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Amazon S3 Vectors",
              "short_name": "S3 Vectors",
              "doc_url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html",
              "one_line": "Vector bucket type (GA Dec 2 2025) storing/querying embeddings with strongly consistent writes, integrated into Bedrock KBs and OpenSearch tiered search.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "AI Search vectors / Cosmos DB DiskANN",
              "short_name": "Vector stores",
              "doc_url": "https://learn.microsoft.com/en-us/azure/search/vector-search-overview",
              "one_line": "Vector indexing inside AI Search indexes (hnsw/exhaustive) or Cosmos DB (DiskANN) for RAG grounding.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Vertex AI Vector Search",
              "short_name": "VectorSearch",
              "doc_url": "https://cloud.google.com/vertex-ai/docs/vector-search/overview",
              "one_line": "High-scale approximate nearest neighbor service (ScaNN lineage) for embeddings retrieval.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Autonomous Database 23ai AI Vector Search",
              "short_name": "Vectors",
              "doc_url": "https://docs.oracle.com/en/database/oracle/oracle-database/26/vecse/overview-ai-vector-search.html",
              "one_line": "VECTOR datatype, similarity operators, and in-database embeddings turning ATP/ADW into the vector store for RAG.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "backup-service",
      "domain": "resilience-migration",
      "title": "Backup service",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Backup",
              "short_name": "Backup",
              "doc_url": "https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html",
              "one_line": "Policy-driven central backup across 23+ service families with cross-region/account copies, Vault Lock WORM compliance mode, and restore testing.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Backup",
              "short_name": "Backup",
              "doc_url": "https://learn.microsoft.com/en-us/azure/backup/backup-introduction-to-azure-backup",
              "one_line": "Vault-based backups for VMs, files, SQL/HANA/SAP, blobs (operational+vaulted tiers), and AKS.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Backup and DR Service",
              "short_name": "BackupDR",
              "doc_url": "https://cloud.google.com/backup-disaster-recovery/docs/concepts/backup-dr",
              "one_line": "Centralized backup vault/plans/appliances for Compute Engine, VMware Engine, databases (SAP HANA etc.).",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Backup policies (Block Volume, Boot Volume, Database, FSS)",
              "short_name": "Backups",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Block/Tasks/schedulingvolumebackups.htm",
              "one_line": "Policy-driven scheduled backups: block/boot volume backup schedules (predefined silver/gold/bronze), database backups to Object Storage, FSS snapshots/backups.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "cross-region-replication",
      "domain": "resilience-migration",
      "title": "Cross-region replication",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "Cross-Region Replication primitives (S3 CRR, Aurora Global Database, DynamoDB Global Tables, ElastiCache Global Datastore)",
              "short_name": "XCR primitives",
              "doc_url": "https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html",
              "one_line": "Pattern summary: continuous async cross-region replication is delivered per-service rather than by one product; DR whitepaper names the set for pilot light and warmer strategies.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Storage replication & paired regions",
              "short_name": "GRS/ZRS",
              "doc_url": "https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy",
              "one_line": "Redundancy ladder: LRS/ZRS in-region, GRS/GZRS cross-region, RA- variants readable from secondary.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Cross-region replication patterns (dual-regional buckets, Spanner MR, regional PD)",
              "short_name": "XRegion",
              "doc_url": "https://cloud.google.com/storage/docs/availability-durability",
              "one_line": "Composite capability: storage dual-region+turbo, database multi-region configs, disk async replication.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Replication (Object Storage, Block replicas, FSS)",
              "short_name": "Replication",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/Object/Tasks/usingreplication.htm",
              "one_line": "Asynchronous cross-region replication: bucket replication policies, block-volume replicas, FSS replication, NoSQL global tables.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "dr-orchestration",
      "domain": "resilience-migration",
      "title": "DR orchestration",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Elastic Disaster Recovery",
              "short_name": "DRS",
              "doc_url": "https://docs.aws.amazon.com/drs/latest/userguide/what-is-drs.html",
              "one_line": "Agent-based continuous block replication to a low-cost staging subnet; crash-consistent RPO seconds, RTO minutes, non-disruptive drills, failback.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Site Recovery",
              "short_name": "ASR",
              "doc_url": "https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-overview",
              "one_line": "Replication + orchestrated failover/test-failover for VMs (Azure-to-Azure, VMware/Hyper-V/physical).",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Backup and DR Service (DR orchestration)",
              "short_name": "BackupDR-DR",
              "doc_url": "https://cloud.google.com/backup-disaster-recovery/docs/concepts/backup-dr",
              "one_line": "Failover workflows, replication targets, and recovery plans built on Backup and DR vaults.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Full Stack Disaster Recovery",
              "short_name": "Full Stack DR",
              "doc_url": "https://docs.oracle.com/en-us/iaas/disaster-recovery/index.html",
              "one_line": "DR protection groups generating automated switchover/failover/drill plans across compute, volume groups, databases, file systems, and load balancers between regions.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "migration-service",
      "domain": "resilience-migration",
      "title": "Migration service",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Transform MGN (Application Migration Service)",
              "short_name": "MGN",
              "doc_url": "https://docs.aws.amazon.com/mgn/latest/ug/what-is-application-migration-service.html",
              "one_line": "Lift-and-shift rehosting with continuous block replication, wave planning, launch/post-launch templates; agentless path for VMware vCenter.",
              "status": "ga"
            },
            {
              "name": "AWS Migration Hub and Application Discovery Service",
              "short_name": "Migration Hub / ADS",
              "doc_url": "https://docs.aws.amazon.com/migrationhub/latest/ug/whatishub.html",
              "one_line": "Status tracking across MGN/DMS plus dependency discovery (agentless collector or agents); both closed to new customers Nov 7 2025 with AWS Transform as successor.",
              "status": "retiring"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Migrate",
              "short_name": "Migrate",
              "doc_url": "https://learn.microsoft.com/en-us/azure/migrate/migrate-services-overview",
              "one_line": "Assessment + migration hub discovering servers/DBs/web apps, sizing Azure targets, and driving agentless VMware migration.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Migrate to Virtual Machines (+ Migrate to Containers)",
              "short_name": "M2VM",
              "doc_url": "https://cloud.google.com/migrate/compute-engine/docs/overview",
              "one_line": "Wave-based VM migration from AWS/Azure/vSphere/physical into Compute Engine; container variant lifts VMs to GKE.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Oracle Cloud Migrations (OCM)",
              "short_name": "OCM",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/cloud-migration/home.htm",
              "one_line": "Discovery agents, inventory/assessment dashboards, and migration waves lifting VMware/Hyper-V/KVM VMs into OCI.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "online-transfer",
      "domain": "resilience-migration",
      "title": "Online transfer",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS DataSync",
              "short_name": "DataSync",
              "doc_url": "https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html",
              "one_line": "Online NFS/SMB/HDFS/object transfer to S3/EFS/FSx with encryption, integrity validation, scheduling, VPC endpoints.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Storage Mover",
              "short_name": "Storage Mover",
              "doc_url": "https://learn.microsoft.com/en-us/azure/storage-mover/service-overview",
              "one_line": "Agent-based managed migration of file shares into Azure Files and Blob Storage, organised as projects and jobs with per-job copy logs.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Storage Transfer Service",
              "short_name": "STS",
              "doc_url": "https://cloud.google.com/storage-transfer/docs/overview",
              "one_line": "Scheduled/incremental transfers into GCS from S3/Azure/on-prem/other buckets.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "absent",
          "reason": "No managed online bulk transfer service. The Data Transfer service is the offline appliance and disk path, and online copies use the CLI, rclone, or Storage Gateway."
        }
      }
    },
    {
      "key": "region-az-model",
      "domain": "resilience-migration",
      "title": "Region and AZ model",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Global Infrastructure (Regions and AZs)",
              "short_name": "Regions / AZs",
              "doc_url": "https://aws.amazon.com/about-aws/global-infrastructure/",
              "one_line": "124 AZs across 39 regions (plus 7 AZs / 2 regions announced), minimum three AZs per region, 46 Local Zones, 33 Wavelength Zones, 750+ CloudFront POPs.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Regions and Availability Zones",
              "short_name": "Regions/AZs",
              "doc_url": "https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview",
              "one_line": "Geography > region > (usually 3+) physically separated availability zones with independent power/network.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Regions/zones/global resources model",
              "short_name": "RegionsZones",
              "doc_url": "https://cloud.google.com/compute/docs/regions-zones",
              "one_line": "Regions hold independent zones; resources declare scope global/regional/zonal; AI zones host accelerators.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Regions, Availability Domains, Fault Domains",
              "short_name": "Region model",
              "doc_url": "https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm",
              "one_line": "41 commercial regions (many single-AD); multi-AD regions have 3 ADs; EVERY AD contains exactly 3 fault domains for anti-affinity.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "resilience-assessment",
      "domain": "resilience-migration",
      "title": "Resilience assessment",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Fault Injection Service",
              "short_name": "FIS",
              "doc_url": "https://docs.aws.amazon.com/fis/latest/userguide/what-is.html",
              "one_line": "Chaos experiments defined as templates of actions + targets + CloudWatch-alarm stop conditions, runnable multi-account.",
              "status": "ga"
            },
            {
              "name": "AWS Resilience Hub",
              "short_name": "Resilience Hub",
              "doc_url": "https://docs.aws.amazon.com/resilience-hub/latest/userguide/what-is.html",
              "one_line": "Defines RTO/RPO policies, scores applications out of 100, recommends alarms/SOPs/tests, launches FIS experiments.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Business Continuity Center",
              "short_name": "ABCC",
              "doc_url": "https://learn.microsoft.com/en-us/azure/resiliency/resiliency-overview",
              "one_line": "Centralized BC/DR management surface: protection posture, readiness reporting, and onboarding of Backup/Site Recovery coverage.",
              "status": "ga"
            },
            {
              "name": "Azure Chaos Studio",
              "short_name": "Chaos",
              "doc_url": "https://learn.microsoft.com/en-us/azure/chaos-studio/chaos-studio-overview",
              "one_line": "Fault injection experiments (VM shutdown, network latency, DNS failures) with experiment guards and targets.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "absent",
          "reason": "No FIS/Chaos-Studio-equivalent first-party control plane. Note: Cloud Service Mesh does ship managed fault injection (delay/abort faults on a percentage of requests), so 'no first-party fault injection' would be false; what is absent is a standalone chaos platform. No RTO/RPO policy-scored resilience hub equivalent. Active Assist does publish tool-scored Reliability-pillar and change-risk recommendations, so DR guidance is not purely guide-led; what is absent is policy-based resilience scoring."
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "Full Stack DR drills",
              "short_name": "DR drills",
              "doc_url": "https://docs.oracle.com/en-us/iaas/disaster-recovery/doc/disaster-recovery-terminology.html",
              "one_line": "Start-drill/stop-drill plans standing up an isolated replica in the standby region to validate recovery without impacting production.",
              "status": "ga"
            }
          ]
        }
      }
    },
    {
      "key": "well-architected-framework",
      "domain": "resilience-migration",
      "title": "Well-Architected Framework",
      "cells": {
        "aws": {
          "state": "service",
          "services": [
            {
              "name": "AWS Well-Architected Framework and Tool",
              "short_name": "Well-Architected",
              "doc_url": "https://aws.amazon.com/architecture/well-architected/",
              "one_line": "Six pillars (operational excellence, security, reliability, performance efficiency, cost optimization, sustainability), free review tool, lens library.",
              "status": "ga"
            }
          ]
        },
        "azure": {
          "state": "service",
          "services": [
            {
              "name": "Azure Well-Architected Framework",
              "short_name": "WAF review",
              "doc_url": "https://learn.microsoft.com/en-us/azure/well-architected/",
              "one_line": "Five-pillar design guidance (cost, reliability, security, operational excellence, efficiency) with a self-service review tool.",
              "status": "ga"
            }
          ]
        },
        "gcp": {
          "state": "service",
          "services": [
            {
              "name": "Google Cloud Well-Architected Framework",
              "short_name": "WAF-GCP",
              "doc_url": "https://cloud.google.com/architecture/framework",
              "one_line": "Six-pillar guidance (operational excellence, security, reliability, performance, cost, sustainability) that the PCA exam explicitly weaves through objectives.",
              "status": "ga"
            }
          ]
        },
        "oci": {
          "state": "service",
          "services": [
            {
              "name": "OCI Well-Architected Framework",
              "short_name": "Well-Architected",
              "doc_url": "https://docs.oracle.com/en/solutions/oci-best-practices/index.html",
              "one_line": "Oracle's published best-practice pillars (operational excellence, security, reliability, performance, cost optimization) with mapped OCI services.",
              "status": "ga"
            }
          ]
        }
      }
    }
  ]
};
