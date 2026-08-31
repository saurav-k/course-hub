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
- HTTP caching, freshness and validation: [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111) - the
  companion to RFC 9110 that owns the cache model Module 02 teaches.
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

### Module 02 - HTTP is the language

- Lesson 0200, the request frame: [RFC 9110 &sect;7.1, Determining the Target Resource](https://www.rfc-editor.org/rfc/rfc9110#section-7.1)
  and [RFC 9113 &sect;8.3.1, Request Pseudo-Header Fields](https://www.rfc-editor.org/rfc/rfc9113#section-8.3.1)
  for the same components carried under HTTP/2.
- Lesson 0201, method properties: [RFC 9110 &sect;9.2](https://www.rfc-editor.org/rfc/rfc9110#section-9.2)
  for safe, idempotent and cacheable, including the note that most cache implementations support only
  GET and HEAD, and the prohibition on a proxy retrying a non-idempotent request.
- Lesson 0202, status codes: [RFC 9110 &sect;15](https://www.rfc-editor.org/rfc/rfc9110#section-15)
  for the extensibility rule and the five class definitions.
- Lesson 0203, header fields: [RFC 9110 &sect;12](https://www.rfc-editor.org/rfc/rfc9110#section-12)
  for content negotiation and [&sect;13](https://www.rfc-editor.org/rfc/rfc9110#section-13) for
  conditional requests and the precondition fields.
- Lesson 0204, caching: [RFC 9111 &sect;4.2](https://www.rfc-editor.org/rfc/rfc9111#section-4.2) for
  freshness and the ordered lifetime rules, [&sect;4.3](https://www.rfc-editor.org/rfc/rfc9111#section-4.3)
  for validation, and [MDN's HTTP caching guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching)
  as the readable companion.
- Lesson 0205, CORS: [MDN's CORS guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)
  for the safelisted fields, the preflight and the credentialed-request rules, over the normative
  [Fetch standard](https://fetch.spec.whatwg.org/) that specifies the browser behaviour itself.

### Module 04 - Serialization and contracts

- Lesson 0400, the wire contract: [RFC 8259 &sect;6](https://www.rfc-editor.org/rfc/rfc8259#section-6) for
  what the number grammar deliberately leaves unsettled, [&sect;4](https://www.rfc-editor.org/rfc/rfc8259#section-4)
  for the duplicate-name situation, and [Go encoding/json](https://pkg.go.dev/encoding/json) for the
  documented default that unmatched object keys are ignored.
- Lesson 0401, JSON's type system: [RFC 8259 &sect;3](https://www.rfc-editor.org/rfc/rfc8259#section-3)
  for the six values, [&sect;6](https://www.rfc-editor.org/rfc/rfc8259#section-6) for the interoperable
  integer range, and the [ProtoJSON mapping](https://protobuf.dev/programming-guides/json/) for the
  worked decision to carry int64 as a decimal string.
- Lesson 0402, schema-first: [Protocol Buffers language guide (proto3)](https://protobuf.dev/programming-guides/proto3/)
  for field numbers, the reserved range and unknown-field retention, and
  [Do's and Don'ts](https://protobuf.dev/programming-guides/dos-donts/) for the reuse prohibition.
- Lesson 0403, boundary validation: [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
  for allow-list validation and the explicit statement that it is not the primary defence against
  injection, [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
  for the mechanism at the sink, [RFC 9110 &sect;15.5.21](https://www.rfc-editor.org/rfc/rfc9110#section-15.5.21)
  for 422, and [encoding/json](https://pkg.go.dev/encoding/json#Decoder.DisallowUnknownFields) for the
  strict decoder option.
- Lesson 0404, content negotiation: [RFC 9110 &sect;12.1](https://www.rfc-editor.org/rfc/rfc9110#section-12.1)
  for proactive negotiation and its stated disadvantages, [&sect;12.5.1](https://www.rfc-editor.org/rfc/rfc9110#section-12.5.1)
  for the Accept grammar and weights, [&sect;8.3](https://www.rfc-editor.org/rfc/rfc9110#section-8.3) for
  Content-Type and the sniffing warning, [&sect;15.5.7](https://www.rfc-editor.org/rfc/rfc9110#section-15.5.7)
  and [&sect;15.5.16](https://www.rfc-editor.org/rfc/rfc9110#section-15.5.16) for 406 and 415, and
  [MDN's content negotiation guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Content_negotiation)
  as the readable companion on the cache's role.
- Lesson 0405, compatibility: [Updating a Message Type](https://protobuf.dev/programming-guides/proto3/#updating)
  for the safe, unsafe and lossy edits including the truncation behaviour, and the
  [ProtoJSON mapping](https://protobuf.dev/programming-guides/json/) for the name-keyed rules and the
  unknown-field default that inverts the binary one.

### Module 06 - API design

- Lesson 0600, the promise: [Stripe - API upgrades](https://docs.stripe.com/upgrades) for the published
  list of backward-compatible changes, including the reserved right to change opaque identifier formats,
  and [GitHub - API Versions](https://docs.github.com/en/rest/about-the-rest-api/api-versions) for the
  mirror-image list of changes that force a new version.
- Lesson 0601, the uniform interface: [RFC 9110 &sect;3.1](https://www.rfc-editor.org/rfc/rfc9110#section-3.1)
  for the stated design goal of separating resource identification from request semantics,
  [Fielding, *Architectural Styles and the Design of Network-based Software Architectures*, chapter 5](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
  for the four uniform-interface constraints and the efficiency they cost, and
  [AIP-136](https://google.aip.dev/136) for the custom-method colon form and the rule that standard
  methods are preferred.
- Lesson 0602, pagination: [PostgreSQL - LIMIT and OFFSET](https://www.postgresql.org/docs/current/queries-limit.html)
  for the skipped-row cost and the inconsistent-results warning, [AIP-158](https://google.aip.dev/158)
  for opaque page tokens and the matching-parameters rule, [RFC 8288](https://www.rfc-editor.org/rfc/rfc8288)
  for what a link relation is, and
  [GitHub - Using pagination in the REST API](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api)
  for the `link` header with `next`, `prev`, `first` and `last` and the advice to follow those URLs
  rather than construct them.
- Lesson 0603, error bodies: [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) for the
  problem-details object, its five members, the `about:blank` default, extension members (&sect;3.2), and
  the security considerations (&sect;5) that bound what `detail` may say.
- Lesson 0604, versioning: [GitHub - API Versions](https://docs.github.com/en/rest/about-the-rest-api/api-versions)
  for the `X-GitHub-Api-Version` header, the `2022-11-28` default, the 24-month support window and the
  410, [Stripe - Versioning](https://docs.stripe.com/api/versioning) for the account-pinned variant,
  [RFC 9745](https://www.rfc-editor.org/rfc/rfc9745.html) for the `Deprecation` header and
  [RFC 8594](https://www.rfc-editor.org/rfc/rfc8594.html) for `Sunset`.
- Lesson 0605, idempotency: [RFC 9110 &sect;9.2.2](https://www.rfc-editor.org/rfc/rfc9110#section-9.2.2)
  for the definition and the conditional permission to auto-retry,
  [Stripe - Idempotent requests](https://docs.stripe.com/api/idempotent_requests) for the stored
  status-and-body behaviour, the 24-hour pruning and the parameter comparison, and
  [draft-ietf-httpapi-idempotency-key-header](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header)
  for the 400 / 409 / 422 refusals. **That draft expired in April 2026 rather than shipping**, which is
  why lesson 0605 treats the header as a convention and cites Stripe for the practice.

### Module 13 - Scale, fleet and shipping

- Lesson 1300, concurrency: [Effective Go - Concurrency](https://go.dev/doc/effective_go) for the
  goroutine as a function "executing concurrently with other goroutines in the same address space",
  costing "little more than the allocation of stack space", and multiplexed onto OS threads so that
  others continue to run when one blocks on I/O;
  [asyncio - Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html) for
  cooperative scheduling and the statement that an event loop "runs one Task at a time"; and the
  [Python glossary](https://docs.python.org/3/glossary.html#term-global-interpreter-lock) for the
  interpreter lock, including the sentence that is usually dropped, "the GIL is always released when
  doing I/O", and the 3.13 build option specified in [PEP 703](https://peps.python.org/pep-0703/).
  The pool ceiling is derived on the page from arrival rate times hold time, with both assumptions
  stated in the figcaption rather than attributed to a source.
- Lesson 1301, shared state: [The Go Memory Model](https://go.dev/ref/mem) for the mechanical
  definition of a data race, the DRF-SC guarantee, the permission to terminate a racy program, and
  the requirement that concurrent access be serialized;
  [pkg.go.dev/sync](https://pkg.go.dev/sync) for the mutex contract and the stated preference for
  channels over the primitives; [Effective Go](https://go.dev/doc/effective_go) for the sharing
  slogan; the [Python glossary](https://docs.python.org/3/glossary.html#term-global-interpreter-lock)
  for the precise scope of what the interpreter lock protects, which is the object model rather than
  a program's invariants; and [the race detector article](https://go.dev/doc/articles/race_detector)
  for the runtime-only limit and the 5 to 10 times memory and 2 to 20 times execution cost.
- Lesson 1302, statelessness: [Fielding, chapter 5](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
  for the stateless constraint, its three benefits and its two costs;
  [the twelve-factor app, factor VI](https://12factor.net/processes) for share-nothing processes and
  the statement that sticky sessions "should never be used or relied upon"; and
  [nginx - load balancing](https://nginx.org/en/docs/http/load_balancing.html) for round-robin,
  least-connected, ip-hash with its "except when this server is unavailable" clause, weights, and
  the passive health checks governed by `max_fails` and `fail_timeout`.
- Lesson 1303, containers: [namespaces(7)](https://man7.org/linux/man-pages/man7/namespaces.7.html)
  for the definition and the eight kinds;
  [cgroups(7)](https://man7.org/linux/man-pages/man7/cgroups.7.html) for hierarchical resource
  limiting and the rule that a descendant cannot exceed an ancestor's limit;
  [pid_namespaces(7)](https://man7.org/linux/man-pages/man7/pid_namespaces.7.html) for the init
  signal semantics, which is why a process with no SIGTERM handler ignores a polite stop;
  the [OCI image specification](https://github.com/opencontainers/image-spec/blob/main/spec.md) for
  the manifest, the index, layers as changesets and content-addressable identity;
  [Docker - build cache](https://docs.docker.com/build/cache/) for the downstream invalidation rule;
  and [multi-stage builds](https://docs.docker.com/build/building/multi-stage/) for leaving the
  toolchain behind.
- Lesson 1304, orchestration: [Kubernetes - Controllers](https://kubernetes.io/docs/concepts/architecture/controller/)
  for the control loop, the thermostat and the statement that a controller more commonly writes to
  the API server than acts directly;
  [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) for the
  ReplicaSet rollout and revision history;
  [the Deployment API reference](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/deployment-v1/)
  for `maxSurge` and `maxUnavailable`, both defaulting to 25%, rounded up and down respectively;
  [the three probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
  for the restart-against-remove-from-endpoints distinction;
  [Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/) for the
  termination sequence and the 30-second default grace period; and
  [horizontal pod autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
  for the ratio algorithm, the 15-second sync period and the 0.1 tolerance.
- Lesson 1305, testing: [Fowler - TestPyramid](https://martinfowler.com/bliki/TestPyramid.html) for
  the two assertions, the cost of end-to-end tests and the ice-cream cone; and
  [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) for
  the layer definitions and consumer-driven contract tests, which is the mechanism lesson 0600's
  closing warning asked for and could not name. [pkg.go.dev/testing](https://pkg.go.dev/testing) for
  `t.Run` and `t.Parallel`.
- Lesson 1306, the pipeline: [the twelve-factor app, factor V](https://12factor.net/build-release-run)
  for the three separated stages, the unique release identifier and the append-only ledger;
  [Fowler - ContinuousDelivery](https://martinfowler.com/bliki/ContinuousDelivery.html) for the
  definition, the four tests and the one-directional relation to continuous deployment; and
  [DORA - the four keys](https://dora.dev/guides/dora-metrics-four-keys/) for the metric definitions
  and the finding that "speed and stability are not tradeoffs". **That programme is observational
  research across many organisations**, which is why the page states what it establishes as the two
  moving together in practice rather than as causation in any one team.

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