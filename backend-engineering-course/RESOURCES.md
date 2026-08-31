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

### Module 03 - Routing

- Lesson 0300, the route as a pair: [RFC 9110 &sect;9.1](https://www.rfc-editor.org/rfc/rfc9110#section-9.1) for the
  method token as the primary source of request semantics, and
  [Go's `net/http.ServeMux`](https://pkg.go.dev/net/http#ServeMux) for a pattern grammar that states the method, the
  host and the path in one string.
- Lesson 0301, path against query: [RFC 3986 &sect;3.3](https://www.rfc-editor.org/rfc/rfc3986#section-3.3) and
  [&sect;3.4](https://www.rfc-editor.org/rfc/rfc3986#section-3.4), which define both components as identifying the
  resource and separate them by hierarchy alone; [RFC 6570 &sect;3.2.6](https://www.rfc-editor.org/rfc/rfc6570#section-3.2.6)
  and [&sect;3.2.8](https://www.rfc-editor.org/rfc/rfc6570#section-3.2.8) for the two template operators; and
  [RFC 9111 &sect;2](https://www.rfc-editor.org/rfc/rfc9111#section-2) for the cache key being method plus target URI.
  The filter counts on that page are derived on the page and are not quoted from any source.
- Lesson 0302, the routing tree: [Go's `net/http/routing_tree.go`](https://cs.opensource.google/go/go/+/refs/tags/go1.24.0:src/net/http/routing_tree.go)
  for the level order and the backtracking case, and the Precedence section of the
  [ServeMux documentation](https://pkg.go.dev/net/http#ServeMux) for the strict-subset rule and the conflict panic.
  The comparison counts on that page are derived from the two costs stated there.
- Lesson 0303, the middleware chain: [PEP 3333, middleware components](https://peps.python.org/pep-3333/#middleware-components-that-play-both-sides)
  for the two roles that make wrapping the shape, [Express's writing-middleware guide](https://expressjs.com/en/guide/writing-middleware.html)
  for the loading-order rule and the `next()` obligation, and Go's
  [`http.ResponseWriter`](https://pkg.go.dev/net/http#ResponseWriter) for the header map having no effect after a write.
- Lesson 0304, the routing verdicts: [RFC 9110 &sect;15.5.5](https://www.rfc-editor.org/rfc/rfc9110#section-15.5.5),
  [&sect;15.5.6](https://www.rfc-editor.org/rfc/rfc9110#section-15.5.6),
  [&sect;15.6.2](https://www.rfc-editor.org/rfc/rfc9110#section-15.6.2) and
  [&sect;10.2.1](https://www.rfc-editor.org/rfc/rfc9110#section-10.2.1) for 404, 405, 501 and the `Allow` field.
- Lesson 0305, mounting: [PEP 3333's environment variables](https://peps.python.org/pep-3333/#environ-variables) for
  `SCRIPT_NAME` and `PATH_INFO`, [Go's `http.StripPrefix`](https://pkg.go.dev/net/http#StripPrefix), and
  [Express's request reference](https://expressjs.com/en/5x/api/request/) for `req.baseUrl` and `req.originalUrl`.
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

### Module 08 - Data

- Lesson 0800, the relational model and constraints: [PostgreSQL - Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
  for the five constraint kinds, the statement that a foreign key maintains referential integrity between two tables, and the
  rule that a check constraint is satisfied when its expression evaluates to true **or to null**, and
  [PostgreSQL - Concepts](https://www.postgresql.org/docs/current/tutorial-concepts.html) for relation as the mathematical term
  for table and for the statement that SQL guarantees no order among the rows of a table.
- Lesson 0801, transactions and the log: [PostgreSQL - Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
  for the bank-transfer example, the definition of atomic, the invisibility of an open transaction's updates until commit, and
  savepoints, and [PostgreSQL - Write-Ahead Logging](https://www.postgresql.org/docs/current/wal-intro.html) for the ordering
  rule, roll-forward recovery and the statement that one flush of the log may suffice to commit many small concurrent transactions.
- Lesson 0802, isolation: [PostgreSQL - Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
  for the four phenomena, Table 13.1, the note that PostgreSQL implements three distinct levels and that its Repeatable Read
  does not allow phantom reads, the Read Committed re-evaluation rule with the `website.hits` example, and both serialization
  failure messages with the instruction that applications must be prepared to retry. The MVCC claim that reading never blocks
  writing is [PostgreSQL - Introduction to MVCC](https://www.postgresql.org/docs/current/mvcc-intro.html).
- Lesson 0803, locking: [PostgreSQL - Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html) for the
  four row-lock modes, the statement that row-level locks are released at transaction end, automatic deadlock detection by
  aborting one transaction, and the advice that the best defence is acquiring locks in a consistent order.
  [PostgreSQL - Lock Management](https://www.postgresql.org/docs/current/runtime-config-locks.html) for `deadlock_timeout`
  defaulting to 1s and why the check is deliberately lazy.
- Lesson 0804, indexes: [PostgreSQL - Indexes](https://www.postgresql.org/docs/current/indexes-intro.html) for the sequential
  scan against a few levels of a search tree, the synchronisation overhead on data manipulation, and the instruction to remove
  seldom-used indexes, and [PostgreSQL - Index Types](https://www.postgresql.org/docs/current/indexes-types.html) for what a
  B-tree can serve, including `IS NULL`, sorted retrieval and the anchored-pattern rule, and for hash, GiST, SP-GiST, GIN and BRIN.
- Lesson 0805, composite order and the planner: [PostgreSQL - Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
  for the exact leading-column rule, the 32-column limit and the advice to use them sparingly,
  [Index-Only Scans and Covering Indexes](https://www.postgresql.org/docs/current/indexes-index-only-scans.html) for the two
  conditions, the visibility map and the `INCLUDE` caveats,
  [Statistics Used by the Planner](https://www.postgresql.org/docs/current/planner-stats.html) for `pg_statistic`, the default
  of 100 entries and the weakness of single-column statistics, and
  [Row Estimation Examples](https://www.postgresql.org/docs/current/row-estimation-examples.html) for the worked histogram
  arithmetic that yields 0.100697 and `rows=1007`.
- Lesson 0806, the non-relational map: [AWS - NoSQL design for DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-general-nosql-design.html)
  for the access-pattern-first method, the few-tables advice and the statement that queries outside the designed set are
  expensive and slow, [AWS - DynamoDB read consistency](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html)
  for eventually consistent being the default and strongly consistent reads being unavailable on a global secondary index,
  [MongoDB - Data modeling](https://www.mongodb.com/docs/manual/data-modeling/) for the flexible schema and the principle that
  data accessed together is stored together, [MongoDB - Limits](https://www.mongodb.com/docs/manual/reference/limits/) for the
  16 MiB document ceiling and the 100-level nesting cap, [Redis - Data types](https://redis.io/docs/latest/develop/data-types/)
  for the data structure server framing and the structures it offers, and
  [Neo4j - Graph database concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/) for nodes, labels, and
  directed relationships carrying properties.

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

- A concrete B-tree fanout for a given key width and page size. Lesson 0804 derives its depth arithmetic from an assumed
  fanout of 200 and labels the assumption on the figure rather than quoting a figure the documentation does not state.
- Codd's 1970 paper, *A Relational Model of Data for Large Shared Data Banks*, is the origin of the model Module 08 teaches
  and is behind a paywall that refused every fetch attempted while the module was written. Lesson 0800 therefore grounds the
  model on the PostgreSQL documentation, which states the same properties, rather than citing a paper nobody opened.
