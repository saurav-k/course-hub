# AGENTS.md - Systems Engineering in Go

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

A deep-dive systems engineering course exploring how 17 landmark open-source projects (Docker, Kubernetes, containerd, Helm, Terraform, Vault, Consul, Nomad, Prometheus, Grafana, etcd, CoreDNS, Traefik, Caddy, Hugo, MinIO, CockroachDB) are architected and built in Go. It teaches runtime mechanics, consensus algorithms, scheduling, storage engines, and zero-allocation networking.

## Read before you write

In this order:

1. [`MISSION.md`](MISSION.md) - why the course exists and what is out of scope.
2. [`NOTES.md`](NOTES.md) - how this course teaches: cadence, diagram policy, known gotchas.
3. [`BUILDER-SPEC.md`](BUILDER-SPEC.md) - the markup contract for a page.
4. [`RESOURCES.md`](RESOURCES.md) - the primary open-source repositories this course trusts.
5. [`PLOT.md`](PLOT.md) - the true reading order and everything planned but unwritten.
6. Two neighbouring lessons, to match voice, depth, and structure.

## The rules that bite hardest here

1. **Every page opens with an orientation figure:** Labelled `.fig-cap`: `Where this sits`, depicting the architectural context before the first body section.
2. **Never use unescaped semicolons in Mermaid:** In `sequenceDiagram` and flowchart free text, replace semicolons with dashes or commas to avoid silent rendering breaks.
3. **No syntax 101:** Never re-explain how a basic `for` loop or `if` statement works; focus on memory layouts, goroutine dispatch, mutex contention, and runtime syscalls.

## Out of scope here

Generic programming 101, cloud provider managed API tutorials, and high-level REST vs GraphQL trade-offs. See [`MISSION.md`](MISSION.md).
