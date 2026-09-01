# Notes

How this course teaches, and what the authoring cost.
Read `MISSION.md` first for why it exists, then `BUILDER-SPEC.md` for what differs from the house standard.

## Learner profile

A working engineer who already builds backend systems or writes basic Go, but has never been inside the internal engines of Kubernetes, Docker, etcd, or Prometheus. They think in terms of processes, sockets, memory buffers, and concurrency primitives, but they need the bridge between theoretical computer science concepts (Raft, MVCC, B-trees, DAGs, LSM-trees) and real production Go code.

## Cadence

- **Prose:** 1,000 to 1,400 prose words per lesson (never exceeding 1,800).
- **Diagrams:** Minimum 2 to 3 diagrams per lesson.
  - The first diagram is always the **orientation figure** (`.fig-cap`: `Where this sits`), placing the component within the broader system's architecture.
  - Subsequent figures illustrate concurrency flows, memory layouts, or state transition sequences.
- **Code:** Real, verbatim or cleanly extracted code snippets directly from the 17 open-source repositories, showing idiomatic Go design.
- **Quizzes:** 2 to 3 multi-choice quiz blocks per lesson, testing mechanical sympathy and failure recovery.

## Teaching preferences

- **Anatomy over API:** We do not teach how to use `docker run` or `kubectl apply`; we teach how `dockerd` calls `sys/unix` to create namespaces and cgroups, and how `kube-controller-manager` uses `DeltaFIFO` queues to reconcile desired vs actual state.
- **Mechanical sympathy:** Always explain the cost of allocations, goroutine stack growth, channel lock contention, and garbage collection pauses. Show why systems like MinIO use assembly SIMD and why CockroachDB replaced RocksDB with Pebble.

## Known gotchas

- **Mermaid semicolons:** Never use semicolons inside Mermaid flowchart or sequence nodes; use dashes or commas to prevent silent render crashes.
- **Mermaid linebreaks:** Use `&lt;br/&gt;`, never literal `<br/>`.
- **Figure captions:** Always pair `.fig-cap` with `.fig-claim` as direct children of `figure.diagram`.
- **Zero hand-crafted CSS:** Use existing tokens from `assets/hub.css`.

## Honesty notes

Where an open-source project has evolved over many years (e.g. Docker transitioning from monolith to containerd and runc), we distinguish historical design from modern architecture.
