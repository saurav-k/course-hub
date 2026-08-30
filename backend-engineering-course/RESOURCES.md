# Backend Engineering - Resources

The sources this course trusts. A page cites from here; anything new goes in here first, in the same
pull request.

## The attribution contract

This course is **derived** from the open field-manual series
[Backend from First Principles](https://github.com/DsThakurRawat/Backend-from-first-Principle) by
@DsThakurRawat (24 chapters: HTTP, routing, serialization, auth, databases, caching, queues, search,
error handling, gRPC, config, observability, graceful shutdown, security, scaling, concurrency,
containerization, testing, Kafka, WebSockets). Same subjects and arc, same commitment to mechanism.

The prose and diagrams here are re-authored from first principles and from the canonical primary
sources this series cites. Nothing on these pages is a transcription of the source text or a copy of
its figures. The source is credited because this course follows its arc; every page still links the
primary source for its own subject.

## The canon

The small set this course keeps returning to. Primary only.

- HTTP semantics, headers, methods, caching: [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) - the
  HTTP/1.1 field semantics, used throughout the Web Fundamentals module.
- HTTP/2 and the connection model: [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113).
- The browser same-origin policy and CORS: [Fetch standard](https://fetch.spec.whatwg.org/) - what the
  browser enforces and why.
- Relational model and SQL semantics: [PostgreSQL documentation](https://www.postgresql.org/docs/current/).
- Redis, the in-memory data store, its persistence and eviction model:
  [Redis documentation](https://redis.io/docs/latest/).
- Apache Kafka and the log as a storage primitive:
  [Kafka documentation](https://kafka.apache.org/documentation/) and
  [The Log: What every software engineer should know](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying) (Kreps).
- gRPC and protobuf: [Protocol Buffers](https://protobuf.dev/) and
  [gRPC documentation](https://grpc.io/docs/).
- Go concurrency: [The Go Programming Language / concurrency](https://go.dev/doc/effective_go) and
  [Go by Example](https://gobyexample.com/).
- Python concurrency: [asyncio documentation](https://docs.python.org/3/library/asyncio.html).
- Graceful shutdown, signals, and process lifecycle: POSIX signal semantics, linked per page.
- Containerisation and orchestration: [Docker documentation](https://docs.docker.com/), [Kubernetes documentation](https://kubernetes.io/docs/).
- Simplifying test taxonomy: [TestPyramid / Martin Fowler](https://martinfowler.com/bliki/TestPyramid.html).

## Supporting sources

Cited once or twice, by page. Filled in as modules land; the canon above is the default for anything
the canon already owns.

### Module 01 - The shape of a request

TBD as lessons landing.

## Wisdom

Where the practitioners argue, for a reader who wants to test their understanding against people who do this.

- [Timelines / "How To Do Distributed Locking" or equivalent per-topic posts] - linked as lessons land.
- [Systems Design and other practitioner blogs] - the field keeps arguing about polyglot persistence,
  sharding, and event sourcing; frontier questions in the late modules link these.

## Not used, and why

Sources a reader would expect to see here, and the reason they are not.

- The source series' own chapter files are **crediting the arc, not copyable text**. Its notes are the
  spine, but every page's primary source is the canonical web source the chapter cites.

## Gaps

Claims this course would like to make and cannot source.

A gap recorded here is a gap the course does not assert on a page.

- -