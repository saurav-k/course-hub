/* The capability matrix data for Comparing the Four Clouds.

   One file is the single source of truth for both the rendered matrix and the
   validation gate:

     - clouds   the four columns, in column order
     - domains  the twenty-four capability areas of the shared taxonomy, each
                carrying the capability keys that belong to it
     - rows     one row per capability key, one cell per cloud

   A cell is exactly one of three states:

     {"state": "unfilled"}
         Nobody has filled this cell in yet. Rendered as a dashed, quiet box;
         it means "not written yet", never "this cloud has nothing here".
     {"state": "absent", "reason": "..."}
         A finding: this cloud genuinely ships no equivalent for the
         capability, and the reason says what is nearest and how it differs.
     {"state": "service", "services": [{"name": ..., "short_name": ...,
                                         "doc_url": ..., "one_line": ...}]}
         One or more services answering the capability, each linking that
         vendor's own documentation.

   scripts/validate_site.py enforces all of this: every row resolves to a key
   in the taxonomy and appears once, every row carries all four clouds, every
   cell is one of the three states, and every doc_url is well formed. The
   cells shipped here are deliberately all unfilled: this frame slice carries
   no cloud facts. Later slices fill them only from verified inventories. */
window.CLOUD_CAPABILITY_MATRIX = {
  "version": 1,
  "note": "One row per capability key; one column per cloud. A cell is a service (with a link to that vendor's own documentation), a declared absence with a reason, or unfilled until verified research fills it.",
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
        "vm-instances",
        "vm-images",
        "bare-metal",
        "gpu-compute",
        "spot-capacity"
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
        "managed-kubernetes",
        "serverless-containers",
        "container-registry",
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
        "object-storage",
        "block-storage",
        "file-storage",
        "archive-storage",
        "bulk-transfer-appliance"
      ]
    },
    {
      "slug": "databases",
      "name": "Databases",
      "covers": "relational, NoSQL, key-value, document, in-memory, graph, time-series, ledger, migration services",
      "keys": [
        "relational-managed",
        "relational-serverless",
        "nosql-keyvalue",
        "nosql-document",
        "in-memory-cache",
        "graph-database",
        "timeseries-database"
      ]
    },
    {
      "slug": "analytics",
      "name": "Analytics",
      "covers": "data warehouse, lakehouse, ETL/ELT, streaming, managed Spark/Flink, search, BI, data catalog",
      "keys": [
        "data-warehouse",
        "data-lake",
        "etl-service",
        "stream-ingest",
        "managed-spark",
        "managed-search",
        "bi-dashboards",
        "data-catalog"
      ]
    },
    {
      "slug": "networking-core",
      "name": "Networking core",
      "covers": "virtual networks, subnets, routing, NAT, private endpoints/service links, peering, IP address management, network interfaces",
      "keys": [
        "virtual-network",
        "subnet",
        "route-table",
        "nat-gateway",
        "private-endpoint",
        "network-peering",
        "transit-hub",
        "network-interface"
      ]
    },
    {
      "slug": "networking-lb-edge",
      "name": "Load balancing and edge",
      "covers": "L4 and L7 load balancers, global anycast front doors, CDN, DDoS-scrubbing edge, traffic managers",
      "keys": [
        "l4-load-balancer",
        "l7-load-balancer",
        "global-front-door",
        "cdn",
        "ddos-protection"
      ]
    },
    {
      "slug": "dns-domains",
      "name": "DNS and domains",
      "covers": "authoritative DNS, private DNS zones, domain registrar, health-checked and geo/latency routing policies",
      "keys": [
        "authoritative-dns",
        "private-dns",
        "domain-registrar",
        "dns-routing-policies"
      ]
    },
    {
      "slug": "hybrid-connectivity",
      "name": "Hybrid connectivity",
      "covers": "site-to-site and client VPN, dedicated private circuits, on-prem/edge racks and stacks, SD-WAN partners",
      "keys": [
        "site-to-site-vpn",
        "client-vpn",
        "dedicated-interconnect",
        "on-prem-extension"
      ]
    },
    {
      "slug": "identity-workforce",
      "name": "Identity - workforce",
      "covers": "the cloud's own IAM: users, groups, roles, policy language, permission boundaries, SSO/workforce federation, privileged access",
      "keys": [
        "iam-principals",
        "iam-policy-language",
        "iam-roles",
        "permission-boundary",
        "workforce-sso",
        "privileged-access"
      ]
    },
    {
      "slug": "identity-workload",
      "name": "Identity - machine",
      "covers": "machine identity: instance/pod/function identity, workload identity federation, cross-account and cross-tenant role assumption, short-lived credential issuance",
      "keys": [
        "workload-identity",
        "cross-account-assumption",
        "workload-identity-federation",
        "short-lived-credentials"
      ]
    },
    {
      "slug": "identity-customer",
      "name": "Identity - customer (CIAM)",
      "covers": "CIAM for the apps you build: user pools/directories, social and enterprise federation, MFA, token issuance, B2C tenants",
      "keys": [
        "ciam-user-directory",
        "ciam-social-federation",
        "ciam-mfa"
      ]
    },
    {
      "slug": "secrets-keys",
      "name": "Secrets and keys",
      "covers": "key management, HSM, secrets stores, certificate issuance and lifecycle, envelope encryption, BYOK/HYOK",
      "keys": [
        "key-management",
        "hsm",
        "secrets-store",
        "certificate-manager"
      ]
    },
    {
      "slug": "org-tenancy",
      "name": "Organisation and tenancy",
      "covers": "the account/subscription/project/compartment hierarchy, org policy and guardrails, landing zones, quotas, tagging, billing and cost management",
      "keys": [
        "org-hierarchy",
        "org-guardrail-policy",
        "landing-zone",
        "quota-management",
        "resource-tagging",
        "cost-management"
      ]
    },
    {
      "slug": "governance-policy",
      "name": "Governance and policy",
      "covers": "policy-as-code, configuration/drift assessment, compliance packs and attestation, resource graph/inventory query",
      "keys": [
        "policy-as-code",
        "config-drift-assessment",
        "compliance-pack",
        "resource-graph-query",
        "well-architected-framework"
      ]
    },
    {
      "slug": "observability",
      "name": "Observability",
      "covers": "metrics, logs, traces, dashboards, alerting, synthetic monitoring, profilers, the query language",
      "keys": [
        "metrics-store",
        "log-store",
        "distributed-tracing",
        "dashboards",
        "alerting",
        "synthetic-monitoring",
        "profiler"
      ]
    },
    {
      "slug": "audit-telemetry",
      "name": "Audit and telemetry",
      "covers": "the SPECIFIC telemetry streams the platform emits - control-plane audit, data-plane access, network flow logs, service-specific logs - see section D2",
      "keys": [
        "control-plane-audit-log",
        "data-plane-access-log",
        "network-flow-log",
        "load-balancer-access-log",
        "dns-query-log",
        "service-specific-log"
      ]
    },
    {
      "slug": "security-services",
      "name": "Security services",
      "covers": "WAF, firewall, threat detection, posture management, vulnerability scanning, data classification, incident response tooling",
      "keys": [
        "waf",
        "cloud-firewall",
        "threat-detection",
        "posture-management",
        "vulnerability-scanning",
        "data-classification"
      ]
    },
    {
      "slug": "iac-deployment",
      "name": "IaC and deployment",
      "covers": "native templates, Terraform/OpenTofu providers, imperative-in-code SDKs, config management, pipeline/CI-CD services, progressive delivery",
      "keys": [
        "native-iac-template",
        "terraform-provider",
        "iac-in-code-sdk",
        "config-management",
        "cicd-pipeline",
        "artifact-registry",
        "progressive-delivery"
      ]
    },
    {
      "slug": "integration-messaging",
      "name": "Integration and messaging",
      "covers": "queues, pub/sub, event buses, workflow orchestration, API gateways, managed integration/iPaaS",
      "keys": [
        "message-queue",
        "pub-sub",
        "event-bus",
        "workflow-orchestration",
        "api-gateway",
        "managed-integration"
      ]
    },
    {
      "slug": "ai-ml",
      "name": "AI and ML",
      "covers": "managed model APIs, training and tuning platforms, vector stores, agent platforms, speech/vision/document extraction",
      "keys": [
        "managed-model-api",
        "model-training-platform",
        "vector-store",
        "agent-platform",
        "speech-vision-document-ai"
      ]
    },
    {
      "slug": "resilience-migration",
      "name": "Resilience and migration",
      "covers": "backup, DR orchestration, replication, migration services and assessment tooling, chaos/resilience testing, region/AZ model",
      "keys": [
        "backup-service",
        "dr-orchestration",
        "cross-region-replication",
        "migration-service",
        "resilience-assessment",
        "region-az-model"
      ]
    }
  ],
  "rows": [
    {
      "key": "vm-instances",
      "domain": "compute-iaas",
      "title": "VM instances",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "vm-images",
      "domain": "compute-iaas",
      "title": "VM images",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "bare-metal",
      "domain": "compute-iaas",
      "title": "Bare metal",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "gpu-compute",
      "domain": "compute-iaas",
      "title": "GPU compute",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "spot-capacity",
      "domain": "compute-iaas",
      "title": "Spot capacity",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "autoscaling-group",
      "domain": "compute-scaling",
      "title": "Autoscaling group",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "instance-template",
      "domain": "compute-scaling",
      "title": "Instance template",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "managed-kubernetes",
      "domain": "containers",
      "title": "Managed Kubernetes",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "serverless-containers",
      "domain": "containers",
      "title": "Serverless containers",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "container-registry",
      "domain": "containers",
      "title": "Container registry",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "service-mesh",
      "domain": "containers",
      "title": "Service mesh",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "functions-faas",
      "domain": "serverless-app",
      "title": "Functions (FaaS)",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "paas-web-runtime",
      "domain": "serverless-app",
      "title": "PaaS web runtime",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "static-site-hosting",
      "domain": "serverless-app",
      "title": "Static site hosting",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "object-storage",
      "domain": "storage",
      "title": "Object storage",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "block-storage",
      "domain": "storage",
      "title": "Block storage",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "file-storage",
      "domain": "storage",
      "title": "File storage",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "archive-storage",
      "domain": "storage",
      "title": "Archive storage",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "bulk-transfer-appliance",
      "domain": "storage",
      "title": "Bulk transfer appliance",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "relational-managed",
      "domain": "databases",
      "title": "Relational (managed)",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "relational-serverless",
      "domain": "databases",
      "title": "Relational (serverless)",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "nosql-keyvalue",
      "domain": "databases",
      "title": "NoSQL key-value",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "nosql-document",
      "domain": "databases",
      "title": "NoSQL document",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "in-memory-cache",
      "domain": "databases",
      "title": "In-memory cache",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "graph-database",
      "domain": "databases",
      "title": "Graph database",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "timeseries-database",
      "domain": "databases",
      "title": "Time-series database",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "data-warehouse",
      "domain": "analytics",
      "title": "Data warehouse",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "data-lake",
      "domain": "analytics",
      "title": "Data lake",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "etl-service",
      "domain": "analytics",
      "title": "ETL service",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "stream-ingest",
      "domain": "analytics",
      "title": "Stream ingest",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "managed-spark",
      "domain": "analytics",
      "title": "Managed Spark",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "managed-search",
      "domain": "analytics",
      "title": "Managed search",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "bi-dashboards",
      "domain": "analytics",
      "title": "BI dashboards",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "data-catalog",
      "domain": "analytics",
      "title": "Data catalog",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "virtual-network",
      "domain": "networking-core",
      "title": "Virtual network",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "subnet",
      "domain": "networking-core",
      "title": "Subnet",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "route-table",
      "domain": "networking-core",
      "title": "Route table",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "nat-gateway",
      "domain": "networking-core",
      "title": "NAT gateway",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "private-endpoint",
      "domain": "networking-core",
      "title": "Private endpoint",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "network-peering",
      "domain": "networking-core",
      "title": "Network peering",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "transit-hub",
      "domain": "networking-core",
      "title": "Transit hub",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "network-interface",
      "domain": "networking-core",
      "title": "Network interface",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "l4-load-balancer",
      "domain": "networking-lb-edge",
      "title": "L4 load balancer",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "l7-load-balancer",
      "domain": "networking-lb-edge",
      "title": "L7 load balancer",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "global-front-door",
      "domain": "networking-lb-edge",
      "title": "Global front door",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "cdn",
      "domain": "networking-lb-edge",
      "title": "CDN",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "ddos-protection",
      "domain": "networking-lb-edge",
      "title": "DDoS protection",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "authoritative-dns",
      "domain": "dns-domains",
      "title": "Authoritative DNS",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "private-dns",
      "domain": "dns-domains",
      "title": "Private DNS",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "domain-registrar",
      "domain": "dns-domains",
      "title": "Domain registrar",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "dns-routing-policies",
      "domain": "dns-domains",
      "title": "DNS routing policies",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "site-to-site-vpn",
      "domain": "hybrid-connectivity",
      "title": "Site-to-site VPN",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "client-vpn",
      "domain": "hybrid-connectivity",
      "title": "Client VPN",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "dedicated-interconnect",
      "domain": "hybrid-connectivity",
      "title": "Dedicated interconnect",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "on-prem-extension",
      "domain": "hybrid-connectivity",
      "title": "On-prem extension",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "iam-principals",
      "domain": "identity-workforce",
      "title": "IAM principals",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "iam-policy-language",
      "domain": "identity-workforce",
      "title": "IAM policy language",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "iam-roles",
      "domain": "identity-workforce",
      "title": "IAM roles",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "permission-boundary",
      "domain": "identity-workforce",
      "title": "Permission boundary",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "workforce-sso",
      "domain": "identity-workforce",
      "title": "Workforce SSO",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "privileged-access",
      "domain": "identity-workforce",
      "title": "Privileged access",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "workload-identity",
      "domain": "identity-workload",
      "title": "Workload identity",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "cross-account-assumption",
      "domain": "identity-workload",
      "title": "Cross-account assumption",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "workload-identity-federation",
      "domain": "identity-workload",
      "title": "Workload identity federation",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "short-lived-credentials",
      "domain": "identity-workload",
      "title": "Short-lived credentials",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "ciam-user-directory",
      "domain": "identity-customer",
      "title": "CIAM user directory",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "ciam-social-federation",
      "domain": "identity-customer",
      "title": "CIAM social federation",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "ciam-mfa",
      "domain": "identity-customer",
      "title": "CIAM MFA",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "key-management",
      "domain": "secrets-keys",
      "title": "Key management",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "hsm",
      "domain": "secrets-keys",
      "title": "HSM",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "secrets-store",
      "domain": "secrets-keys",
      "title": "Secrets store",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "certificate-manager",
      "domain": "secrets-keys",
      "title": "Certificate manager",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "org-hierarchy",
      "domain": "org-tenancy",
      "title": "Org hierarchy",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "org-guardrail-policy",
      "domain": "org-tenancy",
      "title": "Org guardrail policy",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "landing-zone",
      "domain": "org-tenancy",
      "title": "Landing zone",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "quota-management",
      "domain": "org-tenancy",
      "title": "Quota management",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "resource-tagging",
      "domain": "org-tenancy",
      "title": "Resource tagging",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "cost-management",
      "domain": "org-tenancy",
      "title": "Cost management",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "policy-as-code",
      "domain": "governance-policy",
      "title": "Policy as code",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "config-drift-assessment",
      "domain": "governance-policy",
      "title": "Config drift assessment",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "compliance-pack",
      "domain": "governance-policy",
      "title": "Compliance pack",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "resource-graph-query",
      "domain": "governance-policy",
      "title": "Resource graph query",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "well-architected-framework",
      "domain": "governance-policy",
      "title": "Well-Architected Framework",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "metrics-store",
      "domain": "observability",
      "title": "Metrics store",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "log-store",
      "domain": "observability",
      "title": "Log store",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "distributed-tracing",
      "domain": "observability",
      "title": "Distributed tracing",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "dashboards",
      "domain": "observability",
      "title": "Dashboards",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "alerting",
      "domain": "observability",
      "title": "Alerting",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "synthetic-monitoring",
      "domain": "observability",
      "title": "Synthetic monitoring",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "profiler",
      "domain": "observability",
      "title": "Profiler",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "control-plane-audit-log",
      "domain": "audit-telemetry",
      "title": "Control-plane audit log",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "data-plane-access-log",
      "domain": "audit-telemetry",
      "title": "Data-plane access log",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "network-flow-log",
      "domain": "audit-telemetry",
      "title": "Network flow log",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "load-balancer-access-log",
      "domain": "audit-telemetry",
      "title": "Load-balancer access log",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "dns-query-log",
      "domain": "audit-telemetry",
      "title": "DNS query log",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "service-specific-log",
      "domain": "audit-telemetry",
      "title": "Service-specific log",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "waf",
      "domain": "security-services",
      "title": "WAF",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "cloud-firewall",
      "domain": "security-services",
      "title": "Cloud firewall",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "threat-detection",
      "domain": "security-services",
      "title": "Threat detection",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "posture-management",
      "domain": "security-services",
      "title": "Posture management",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "vulnerability-scanning",
      "domain": "security-services",
      "title": "Vulnerability scanning",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "data-classification",
      "domain": "security-services",
      "title": "Data classification",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "native-iac-template",
      "domain": "iac-deployment",
      "title": "Native IaC template",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "terraform-provider",
      "domain": "iac-deployment",
      "title": "Terraform provider",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "iac-in-code-sdk",
      "domain": "iac-deployment",
      "title": "IaC-in-code SDK",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "config-management",
      "domain": "iac-deployment",
      "title": "Config management",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "cicd-pipeline",
      "domain": "iac-deployment",
      "title": "CI/CD pipeline",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "artifact-registry",
      "domain": "iac-deployment",
      "title": "Artifact registry",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "progressive-delivery",
      "domain": "iac-deployment",
      "title": "Progressive delivery",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "message-queue",
      "domain": "integration-messaging",
      "title": "Message queue",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "pub-sub",
      "domain": "integration-messaging",
      "title": "Pub-sub",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "event-bus",
      "domain": "integration-messaging",
      "title": "Event bus",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "workflow-orchestration",
      "domain": "integration-messaging",
      "title": "Workflow orchestration",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "api-gateway",
      "domain": "integration-messaging",
      "title": "API gateway",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "managed-integration",
      "domain": "integration-messaging",
      "title": "Managed integration",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "managed-model-api",
      "domain": "ai-ml",
      "title": "Managed model API",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "model-training-platform",
      "domain": "ai-ml",
      "title": "Model training platform",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "vector-store",
      "domain": "ai-ml",
      "title": "Vector store",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "agent-platform",
      "domain": "ai-ml",
      "title": "Agent platform",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "speech-vision-document-ai",
      "domain": "ai-ml",
      "title": "Speech, vision and document AI",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "backup-service",
      "domain": "resilience-migration",
      "title": "Backup service",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "dr-orchestration",
      "domain": "resilience-migration",
      "title": "DR orchestration",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "cross-region-replication",
      "domain": "resilience-migration",
      "title": "Cross-region replication",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "migration-service",
      "domain": "resilience-migration",
      "title": "Migration service",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "resilience-assessment",
      "domain": "resilience-migration",
      "title": "Resilience assessment",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    },
    {
      "key": "region-az-model",
      "domain": "resilience-migration",
      "title": "Region and AZ model",
      "cells": {
        "aws": {
          "state": "unfilled"
        },
        "azure": {
          "state": "unfilled"
        },
        "gcp": {
          "state": "unfilled"
        },
        "oci": {
          "state": "unfilled"
        }
      }
    }
  ]
};
