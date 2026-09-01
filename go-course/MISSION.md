# Mission

The record of the interview in `.claude/skills/course-authoring/new-course.md`.
This file is canonical: when a later authoring decision is argued, it is settled by re-reading this, not by re-deciding.

## Why this course exists

The modern cloud substrate is built on Go. Docker, Kubernetes, containerd, Helm, Terraform, Vault, Consul, Nomad, Prometheus, Grafana, etcd, CoreDNS, Traefik, Caddy, Hugo, MinIO, and CockroachDB are all written in Go. Yet most engineers learn Go through syntax primers, web-framework tutorials, or simple concurrency toys. They never see how world-class systems engineers architect real distributed consensus engines, write-ahead logs, container shims, pluggable schedulers, LSM-tree storage engines, or zero-allocation network pipelines.

This course exists to teach systems engineering in Go by disassembling 17 landmark open-source projects at their source code.

- **The learner:** A software engineer with 2 to 7 years of backend or systems experience (in Go, Python, Java, C++, or TypeScript) who wants to write production-grade, highly concurrent, and mechanically sympathetic systems in Go.
- **Assumed baseline:** Core programming concepts, basic data structures, Linux operating system concepts (threads, processes, virtual memory, file descriptors, network sockets), and git. They do not need Go syntax 101 re-explained.
- **The specific cold spot:** The architectural leap from writing basic Go services to engineering resilient distributed systems:
  1. How the Go runtime actually interacts with the Linux kernel (namespaces, cgroups, syscalls, non-blocking I/O).
  2. How real systems structure concurrency without deadlocks, goroutine leaks, or lock contention.
  3. How consensus protocols (Raft, SWIM gossip), storage engines (LSM-trees, B+trees, TSDB), and state machines are implemented in pure Go.
  4. How modularity, dynamic extensibility, and IPC are achieved (gRPC plugins, in-process module registries, `net/http` hijacking, file descriptor handovers).

## The source

The course derives directly from the authoritative source repositories of 17 open-source projects:
1. **Docker / Moby** (`moby/moby`)
2. **Kubernetes** (`kubernetes/kubernetes`)
3. **containerd** (`containerd/containerd`)
4. **Helm** (`helm/helm`)
5. **Terraform** (`hashicorp/terraform`)
6. **Vault** (`hashicorp/vault`)
7. **Consul** (`hashicorp/consul`)
8. **Nomad** (`hashicorp/nomad`)
9. **Prometheus** (`prometheus/prometheus`)
10. **Grafana** (`grafana/grafana`)
11. **etcd** (`etcd-io/etcd`)
12. **CoreDNS** (`coredns/coredns`)
13. **Traefik** (`traefik/traefik`)
14. **Caddy** (`caddyserver/caddy`)
15. **Hugo** (`gohugoio/hugo`)
16. **MinIO** (`minio/minio`)
17. **CockroachDB** (`cockroachdb/cockroach`)

Every mechanism, package layout, and pattern taught in this course points directly to concrete files, interfaces, and algorithms within these codebases.

## Success looks like

The learner can:

1. **Trace container isolation to kernel primitives:** Explain how Docker and containerd configure Linux namespaces, cgroups, and rootfs mounts through Go's `os/exec` and `syscall` packages, and how containerd's shim architecture keeps containers alive across daemon restarts.
2. **Implement distributed consensus and state machines:** Dissect how etcd, Consul, and CockroachDB implement Raft and Multi-Raft in Go, including the zero-I/O `Ready` pattern, write-ahead logs, and storage engines (bbolt and Pebble).
3. **Architect declarative control loops and schedulers:** Apply Kubernetes' Informer-Lister-Workqueue reconciliation pattern and Nomad's plan/eval scheduling pipeline to design custom operators and resource managers.
4. **Design extensible plug-in systems and zero-downtime servers:** Implement out-of-process gRPC plugins (Terraform/Vault/Nomad `go-plugin`), compile-time plugin chains (CoreDNS, Caddy), and seamless socket handovers for zero-downtime configuration reloads (Caddy/Traefik).
5. **Engineer high-throughput storage and telemetry engines:** Apply TSDB chunking and memory-mapped inverted indexes (Prometheus), SIMD-accelerated Reed-Solomon erasure coding (MinIO), and parallel pipeline worker pools (Hugo).

**The failure mode:** If the course reads like an API listing, promotional documentation, or generic Go syntax primer without showing real code anatomy, architectural diagrams, concurrency mechanics, and failure modes.

## Structure

- **Page shape:** A lesson shape (conforming to `references/page-contracts.md`). Each lesson tackles one tight idea with an orientation diagram, real source code dissection, and check questions.
- **Grain:** 900 to 1,400 prose words per lesson (strict ceiling of 1,800), with 2+ diagrams per page.
- **Organization:** 8 sequential modules grouping the 17 open-source systems into coherent architectural themes, plus a synthesis module on cross-cutting production patterns.

## The ladder

- **Foundation (`pill easy`):** The substrate. OS kernel primitives in Go, container isolation (`moby`, `containerd`), and single-node service composition (`coredns`, `caddy`).
- **Working (`pill med`):** Distributed systems mechanics. State synchronization, consensus engines (`etcd`, `consul`), control loops (`kubernetes`), workload scheduling (`nomad`), and infrastructure graph execution (`terraform`).
- **Frontier (`pill hard`):** Extreme scale, storage internals, and high-performance engineering. Multi-Raft and distributed transactions (`cockroachdb`), TSDB chunking and memory mapping (`prometheus`), hardware SIMD erasure coding (`minio`), and barrier encryption envelopes (`vault`).

## Constraints

1. **No toy implementations:** Every pattern shown must map to how the real open-source system implements it.
2. **Every technical claim links to a primary source:** Links point to exact files or functions in the respective open-source repositories or official architecture specs.
3. **Diagram before code:** Every architectural component, state machine, or concurrency flow must have an orientation diagram before discussing the implementation.
4. **No hand-rolled styles:** All markup follows the Course Hub design system (`assets/hub.css` and `assets/hub.js`) with zero custom CSS files.

## Out of scope

- **General Go syntax 101:** Assumed knowledge; basic types, syntax, and package setup are not re-taught.
- **Cloud provider specific APIs:** Owned by `aws-course`, `gcp-course`, and `azure-course`.
- **General backend API concepts:** High-level REST vs GraphQL vs gRPC comparison is owned by `backend-engineering-course`.
- **Production systems capacity math:** Sizing clusters at 10k rps is owned by `production-systems-course`.

## Siblings

- **`backend-engineering-course`:** Covers request pipelines, HTTP, and gRPC theoretically; `go-course` shows how Traefik, Caddy, and CoreDNS implement them at wire speed in Go.
- **`production-systems-course`:** Covers failure modes and scale math; `go-course` shows the exact code in Kubernetes, etcd, and Prometheus that handles those failures.
- **`herdr-course`:** Covers agent process management; `go-course` shows how containerd and Docker isolate and monitor host processes.
