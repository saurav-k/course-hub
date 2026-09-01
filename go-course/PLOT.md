# Plot - the reading order of Systems Engineering in Go

This file records the true reading order of the course: where every module, lesson, and reference sheet sits, and everything planned but unwritten.
Fill it from the interview answer about order and the course map written in step 2 of `../new-course.md`, not from a guess.

The order rule, which holds for this course and every course in the hub: **a course's reading order is its true order, and a tutorial or lab session that follows a lecture sits after that lecture in the course map, never in a separate list at the bottom.**
When this file and the course `index.html` disagree, one of them is wrong, and it gets fixed before anything new is added.

Status marks used below:

- **written** - on the site today.
- **in progress** - being written right now, not yet on this branch.
- **reserved** - the position is held; nothing else may take it; nothing is written.

## The sequence

| # | Position | Status | Notes |
|---|---|---|---|
| 1 | `lessons/0100-how-go-talks-to-the-linux-kernel.html` | written | Namespaces, cgroups, syscalls, `os/exec`, `sys/unix` |
| 2 | `lessons/0101-the-anatomy-of-a-zero-allocation-network-loop.html` | written | epoll, network poller, buffer reuse, `sync.Pool` |
| 3 | `lessons/0200-moby-container-lifecycle-and-daemon-architecture.html` | written | Docker/Moby daemon, client-server engine, TTY hijacking |
| 4 | `lessons/0201-containerd-the-shim-pattern-and-event-bus.html` | written | containerd v2 shim, decoupling container lifetimes, topic event bus |
| 5 | `lessons/0202-content-addressable-storage-and-snapshotters.html` | written | CAS, OCI image layers, diffing, overlayfs snapshotters in Go |
| 6 | `lessons/0300-etcd-the-zero-io-raft-engine.html` | written | etcd `raft.Ready` pattern, decoupling state machine from disk/network |
| 7 | `lessons/0301-etcd-write-ahead-log-and-mvcc-bbolt.html` | written | WAL, CRC validation, revisions, bbolt B+tree storage engine |
| 8 | `lessons/0302-consul-swim-gossip-with-memberlist.html` | written | Memberlist, SWIM protocol, failure detection, state sync |
| 9 | `lessons/0303-cockroachdb-multi-raft-and-pebble-lsm.html` | written | Multi-Raft ranges, range leases, Pebble LSM-tree engine replacing CGo RocksDB |
| 10 | `lessons/0400-kubernetes-the-declarative-reconciliation-loop.html` | written | Controller-manager, Informers, Lister, DeltaFIFO, Workqueue rate limiting |
| 11 | `lessons/0401-kubernetes-api-machinery-and-type-schemes.html` | written | runtime.Object, dynamic typing, Scheme registration, field selectors |
| 12 | `lessons/0402-nomad-optimistic-concurrency-and-eval-brokers.html` | written | Nomad plan/eval scheduling pipeline, task runner drivers |
| 13 | `lessons/0403-helm-chart-rendering-and-kubernetes-storage-drivers.html` | written | Go `text/template` sandboxing, release state in K8s Secrets, 3-way merge |
| 14 | `lessons/0500-terraform-dag-construction-and-graph-walking.html` | written | Directed Acyclic Graph, topological sort, concurrent worker evaluation |
| 15 | `lessons/0501-terraform-and-vault-the-go-plugin-subsystem.html` | written | HashiCorp `go-plugin`, net/rpc and gRPC IPC, handshake verification, process supervision |
| 16 | `lessons/0502-vault-barrier-encryption-and-shamir-secret-sharing.html` | written | AES-GCM envelope barrier encryption, Shamir GF(2^8) math, dynamic lease revocation |
| 17 | `lessons/0600-coredns-zero-allocation-dns-pipeline.html` | written | Plugin chain pattern, `plugin.Handler`, `miekg/dns` wire packet parsing |
| 18 | `lessons/0601-traefik-dynamic-configuration-and-reactive-providers.html` | written | Atomic configuration swapping, provider event listeners, middleware chains |
| 19 | `lessons/0602-caddy-modular-architecture-and-zero-downtime-reloads.html` | written | Caddy module lifecycle, `certmagic` automated ACME TLS, socket file descriptor handovers |
| 20 | `lessons/0700-prometheus-tsdb-architecture-and-chunk-compression.html` | reserved | Head block, inverted index posting lists, Gorilla float64 XOR encoding, mmap |
| 21 | `lessons/0701-prometheus-concurrent-scraping-and-promql-engine.html` | reserved | Scrape loop jitter, atomic append, PromQL AST and vectorized execution |
| 22 | `lessons/0702-grafana-backend-routing-and-streaming-channels.html` | reserved | Go backend architecture, service registry, WebSocket/SSE live channels |
| 23 | `lessons/0800-minio-simd-erasure-coding-and-bitrot-protection.html` | reserved | Reed-Solomon erasure coding in assembly/Go, HighwayHash bitrot detection, disk I/O quorum |
| 24 | `lessons/0801-hugo-high-throughput-parallel-pipelines.html` | reserved | Worker pools, `sync.Pool` byte buffer reuse, deduplicated asset caches |
| 25 | `lessons/0900-concurrency-patterns-across-17-codebases.html` | reserved | Channel idioms, cancellation contexts, worker pools, graceful shutdown trees |
| 26 | `lessons/0901-memory-management-and-mechanical-sympathy.html` | reserved | Zero-copy design, escape analysis, `GOMEMLIMIT` tuning, eliminating lock contention |

Reference sheets and glossaries read alongside and are recorded as such; they are not positions in the sequence.

## Planned but unwritten

All reserved positions above form the complete master curriculum for the 17 open-source systems. Position 1 is authored as the gold standard lesson.

## Adding a session to this course

1. Read the course's authoring contract files first (`AGENTS.md`, `MISSION.md`, `NOTES.md`).
2. Take the next free lesson number. Never renumber anything.
3. Insert the new material at its true position in this file and in `index.html`, never appended to the bottom because it arrived last.
4. Re-run `python3 scripts/gen_outline.py go-course`, commit the regenerated `outline.js`, run `python3 scripts/validate_site.py`, and open the changed pages in both themes before opening the pull request.
