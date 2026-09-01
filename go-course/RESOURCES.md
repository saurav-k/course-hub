# Resources - Systems Engineering in Go

The primary sources and open-source repositories this course trusts and dissects.

## The canon (The 17 Open-Source Systems)

1. [moby/moby](https://github.com/moby/moby) - Docker container engine, daemon, and libnetwork.
2. [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) - Container orchestration, controller-manager, client-go, and API machinery.
3. [containerd/containerd](https://github.com/containerd/containerd) - Core container runtime, runtime v2 shim, event bus, and snapshotters.
4. [helm/helm](https://github.com/helm/helm) - Kubernetes package manager, engine template rendering, and storage drivers.
5. [hashicorp/terraform](https://github.com/hashicorp/terraform) - Infrastructure as code, DAG construction, graph walk, and provider RPC.
6. [hashicorp/vault](https://github.com/hashicorp/vault) - Secret management, envelope barrier encryption, Shamir secret sharing, and lease engine.
7. [hashicorp/consul](https://github.com/hashicorp/consul) - Service mesh and discovery, SWIM gossip (memberlist), and Raft consensus.
8. [hashicorp/nomad](https://github.com/hashicorp/nomad) - Workload orchestrator, optimistic evaluation broker, and scheduling algorithms.
9. [prometheus/prometheus](https://github.com/prometheus/prometheus) - Time-series monitoring, TSDB inverted index, Gorilla compression, and PromQL.
10. [grafana/grafana](https://github.com/grafana/grafana) - Observability platform, Go backend service architecture, and live streaming channels.
11. [etcd-io/etcd](https://github.com/etcd-io/etcd) - Distributed key-value store, Raft consensus engine, and bbolt storage.
12. [coredns/coredns](https://github.com/coredns/coredns) - Fast DNS server with plugin chain architecture and zero-allocation packet handling.
13. [traefik/traefik](https://github.com/traefik/traefik) - Cloud-native reverse proxy, atomic configuration reload, and reactive providers.
14. [caddyserver/caddy](https://github.com/caddyserver/caddy) - Extensible web server, module registry, and automated ACME TLS (certmagic).
15. [gohugoio/hugo](https://github.com/gohugoio/hugo) - High-throughput static site generator with parallel rendering pipelines.
16. [minio/minio](https://github.com/minio/minio) - S3-compatible object storage, SIMD-accelerated Reed-Solomon erasure coding, and bitrot protection.
17. [cockroachdb/cockroach](https://github.com/cockroachdb/cockroach) - Distributed SQL database, Multi-Raft consensus, and pure-Go Pebble LSM-tree engine.

## Supporting specifications & design documents

- [The Go Memory Model](https://go.dev/ref/mem)
- [OCI Runtime Specification](https://github.com/opencontainers/runtime-spec)
- [In Search of an Understandable Consensus Algorithm (Ongaro & Ousterhout)](https://raft.github.io/raft.pdf)
- [SWIM: Weakly-Consistent Infection-Style Process Group Membership Protocol (Das, Gupta, Motivala)](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/SWIM.pdf)
- [Gorilla: A Fast, Scalable, In-Memory Time Series Database (Pelkonen et al.)](https://www.vldb.org/pvldb/vol8/p1816-teller.pdf)
