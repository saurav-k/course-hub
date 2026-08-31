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

### Module 05 - The layered service

- Lesson 0500, the seam: [The Go specification, Interface types](https://go.dev/ref/spec#Interface_types) for an
  interface as a type set, and [Implementing an interface](https://go.dev/ref/spec#Implementing_an_interface) for the
  rule that implementation is membership rather than a declaration, which is what lets a consumer own the contract.
- Lesson 0501, mapping an outcome onto a status: [RFC 9110 &sect;15](https://www.rfc-editor.org/rfc/rfc9110#section-15),
  and in particular [400](https://www.rfc-editor.org/rfc/rfc9110#name-400-bad-request) against
  [422](https://www.rfc-editor.org/rfc/rfc9110#name-422-unprocessable-content) for the syntax-against-semantics split,
  [409](https://www.rfc-editor.org/rfc/rfc9110#name-409-conflict) for a conflict with current state, and
  [500](https://www.rfc-editor.org/rfc/rfc9110#name-500-internal-server-error) for an unexpected condition.
  [NestJS on controllers](https://docs.nestjs.com/controllers) for the framework statement of the responsibility.
- Lesson 0502, the service layer: [NestJS on providers](https://docs.nestjs.com/providers) for a service as an ordinary
  class whose collaborators are supplied, and
  [Spring's dependency injection reference](https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html)
  for the constructor-injection argument, including components never handed back half-initialised.
- Lesson 0503, the repository: [Spring Data repository core concepts](https://docs.spring.io/spring-data/jpa/reference/repositories/core-concepts.html)
  for the store-agnostic interface extended by technology-specific ones, and [Go's database/sql](https://pkg.go.dev/database/sql)
  as the counter-example whose generic interface is generic over drivers rather than over stores.
- Lesson 0504, request context: [Go's context package](https://pkg.go.dev/context) for what a context carries, the
  first-parameter and never-in-a-struct conventions, and the restriction of values to request-scoped data that transits
  processes and APIs. [W3C Trace Context](https://www.w3.org/TR/trace-context/) for the four fields of `traceparent`,
  the invalid all-zero values, and `tracestate`. [Python contextvars](https://docs.python.org/3/library/contextvars.html)
  and [asyncio tasks](https://docs.python.org/3/library/asyncio-task.html) for the copied-context and timeout behaviour.
- Lesson 0505, dependency direction: the Spring and NestJS references above for the inversion itself, and the Go
  specification for what changes when interface satisfaction needs no declaration.

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

### Module 07 - Auth and security

- Lesson 0700, the two questions: [RFC 9110 &sect;11](https://www.rfc-editor.org/rfc/rfc9110#section-11)
  for the challenge-response framework, &sect;11.5 for the protection space and the automatic
  re-presentation of credentials inside it, [&sect;15.5.2](https://www.rfc-editor.org/rfc/rfc9110#section-15.5.2)
  and [&sect;15.5.4](https://www.rfc-editor.org/rfc/rfc9110#section-15.5.4) for the exact 401 and 403
  wording including the permission to answer 404 instead;
  [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
  for deny-by-default and validating permission on every request;
  [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
  for the Argon2id parameters that make authentication deliberately slow; and the
  [OWASP Top 10:2021](https://owasp.org/Top10/2021/A00_2021_Introduction/) factors tables for the
  occurrence chart, with the methodology note that eight of the ten categories were ranked from data
  and two from a practitioner survey.
- Lesson 0701, sessions: [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
  for the 64-bit entropy floor, the requirement to regenerate the id after any privilege change, the
  idle and absolute timeouts and the both-sides invalidation rule;
  [RFC 6265 &sect;4.1.2](https://www.rfc-editor.org/rfc/rfc6265#section-4.1.2) for the attributes,
  [&sect;8.5](https://www.rfc-editor.org/rfc/rfc6265#section-8.5) for the absence of isolation by port
  or scheme and [&sect;8.6](https://www.rfc-editor.org/rfc/rfc6265#section-8.6) for the absence of
  integrity across sibling domains; and [MDN Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie)
  for what `HttpOnly` does and does not stop.
- Lesson 0702, self-contained tokens: [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519) &sect;3 for the
  three-part serialisation, &sect;4.1 for the registered claims and &sect;11.1 for the statement that
  contents cannot be relied upon unless cryptographically secured;
  [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) &sect;2.1 for the `alg: none` and RS256-to-HS256
  substitutions and &sect;3.1, &sect;3.9 and &sect;3.12 for the requirements that close them;
  [RFC 7009 &sect;3](https://www.rfc-editor.org/rfc/rfc7009#section-3) for the self-contained against
  handle fork, the short-lived-token compromise and the sentence that the cost of revocation follows
  from the desired security properties; and
  [RFC 9700 &sect;2.2.1](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.2.1) for
  sender-constrained tokens.
- Lesson 0703, OAuth: [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) &sect;1 for the five failures
  of password sharing, &sect;1.1 for the four roles, &sect;1.4 and &sect;1.5 for access and refresh
  tokens; [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) &sect;1 for the code-interception attack
  on a registered custom scheme and &sect;4.2 for `S256` being mandatory to implement;
  [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html) &sect;2.1 for exact redirect-URI matching,
  &sect;2.1.1 for PKCE as a requirement, &sect;2.1.2 against the implicit grant and &sect;2.4 for the
  resource owner password credentials grant that MUST NOT be used; and
  [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html) for the identity
  layer and the ID token's required claims.
- Lesson 0704, injection: [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
  for the ordered primary defences, the statement that a parameterised query makes the database always
  distinguish between code and data, the rule that identifiers and sort order need validation or query
  redesign rather than binding, and the warning that escaping is fragile and cannot be guaranteed; and
  [A03:2021 - Injection](https://owasp.org/Top10/2021/A03_2021-Injection/) for the general case across
  interpreters.
- Lesson 0705, XSS: [OWASP Cross Site Scripting Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
  for the five output contexts and the warning about using the wrong encoding, the safe and dangerous
  sink lists, DOMPurify for genuine user-authored HTML, and the framework escape hatches by name; and
  [MDN's CSP guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP) for the
  nonce-per-response requirement, why allow-list policies fail, what `strict-dynamic` costs, and the
  statement that a policy is not an alternative to sanitising input.
- Lesson 0706, CSRF: [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
  for the definition, the synchroniser token including the rule that it is not stored in a cookie, the
  naive double-submit pattern being bypassable by an attacker who can write cookies on the target
  domain, custom headers being subject to the same-origin policy, and the statement that `SameSite` is
  defence in depth rather than a replacement; and
  [MDN Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie) for
  the precise `Strict`, `Lax` and `None` definitions that leave a state-changing GET forgeable.

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

### Module 09 - Caching

- Lesson 0900, why a cache exists: [Atikoglu et al., *Workload Analysis of a Large-Scale Key-Value Store*, SIGMETRICS 2012](https://s4plus.ustc.edu.cn/_upload/article/files/7a/5b/5c9fd1264e30b6881ecd7f7733f2/3ef2e159-9fd8-47a6-903c-cf9bfa836a28.pdf)
  for the 284-billion-request trace, the per-pool GET hit rates in Table 2 (98.7%, 98.2%, 93.7%, 92.9%,
  81.4%), the 30:1 GET/SET ratio, and the key-popularity tail behind the ETC miss rate;
  [Redis benchmark](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/benchmarks/)
  for the measured sub-millisecond loopback latency the page anchors its planning figure on; and
  [AWS - Caching strategies](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html)
  for the three-trip cache miss penalty. **The 20 ms origin cost in the worked arithmetic is a stated
  assumption, not a measurement**, and the page says so.
- Lesson 0901, read patterns: [Azure Architecture Center - Cache-Aside pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)
  for the pattern, the read-through comparison and the problems-and-considerations list;
  [AWS - Caching strategies](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html)
  for lazy loading with its advantages and disadvantages stated; and &sect;2 of
  [Nishtala et al., *Scaling Memcache at Facebook*, NSDI 2013](https://users.cs.utah.edu/~stutsman/cs6963/public/papers/memcached.pdf)
  ([paper home](https://research.facebook.com/publications/scaling-memcache-at-facebook/)) for the
  demand-filled look-aside shape.
- Lesson 0902, write patterns: [AWS - Caching strategies](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html)
  for write-through, its two-trip cost and the missing-data and cache-churn disadvantages;
  [*Scaling Memcache at Facebook*](https://users.cs.utah.edu/~stutsman/cs6963/public/papers/memcached.pdf) &sect;2
  for deleting rather than updating because deletes are idempotent;
  [Azure - Cache-Aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside) for the
  ordering rule and the refill window it leaves open; and
  [Redis - Key eviction](https://redis.io/docs/latest/develop/reference/eviction/) for `allkeys-lru`
  evicting any key, which is what makes an unflushed write-back entry losable.
- Lesson 0903, keys: [RFC 9111 &sect;4.1](https://www.rfc-editor.org/rfc/rfc9111#section-4.1) for the primary
  and secondary cache key and the fragmentation `Vary` costs;
  [Fastly - Working with surrogate keys](https://www.fastly.com/documentation/guides/full-site-delivery/purging/working-with-surrogate-keys/)
  for tag-based purge, the many-to-many mapping and the 1,024-byte key and 16,384-byte header limits; and
  [*Scaling Memcache at Facebook*](https://users.cs.utah.edu/~stutsman/cs6963/public/papers/memcached.pdf) &sect;4.1
  for SQL statements amended with the keys to invalidate, and the measured 4% of deletes that removed anything.
- Lesson 0904, invalidation: [*Scaling Memcache at Facebook*](https://users.cs.utah.edu/~stutsman/cs6963/public/papers/memcached.pdf)
  &sect;3.2.1 for the stale-set definition and the 64-bit lease token, and &sect;4.1 for the commit-log
  invalidation pipeline, the 18x batching improvement and the read-after-write local invalidation;
  [AWS - Caching strategies](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html) for
  a TTL keeping data from getting too stale without guaranteeing freshness; and
  [Redis EXPIRE](https://redis.io/docs/latest/commands/expire/) for passive and active expiry and the
  synthesized DEL on the replication link. **The `p` and `d` figures in the staleness arithmetic are
  illustrative**, and the page labels them as such.
- Lesson 0905, failure modes: [*Scaling Memcache at Facebook*](https://users.cs.utah.edu/~stutsman/cs6963/public/papers/memcached.pdf)
  &sect;3.2.1 for the 17K/s to 1.3K/s peak database rate under leases, &sect;3.3 for Gutter at about 1% of
  servers reducing client-visible failures by 99%, and &sect;4.3 for Cold Cluster Warmup and its two-second
  hold-off; [Redis - Key eviction](https://redis.io/docs/latest/develop/reference/eviction/) for `maxmemory`,
  the policy list, the volatile policies behaving like `noeviction` with no expirations set, approximated
  LRU with `maxmemory-samples`, and LFU's Morris counters;
  [Vattani, Chierichetti and Lowenstein, *Optimal Probabilistic Cache Stampede Prevention*, VLDB 2015](https://cseweb.ucsd.edu/~avattani/papers/cache_stampede.pdf)
  for the XFetch rule and the proof that the exponential distribution is the right one; and
  [golang.org/x/sync/singleflight](https://pkg.go.dev/golang.org/x/sync/singleflight) for duplicate call
  suppression and its documented per-process scope.

### Module 10 - Async work and search

- Lesson 1000, the deferred request: [RFC 9110 &sect;15.3.3](https://www.rfc-editor.org/rfc/rfc9110#section-15.3.3)
  for 202 Accepted, its deliberate noncommittal framing, the status-monitor recommendation and the
  sentence the whole module rests on - there is no facility in HTTP for re-sending a status code from an
  asynchronous operation. [Sidekiq - Best Practices](https://github.com/sidekiq/sidekiq/wiki/Best-Practices)
  for the rule that a job payload carries identifiers rather than state, and
  [Amazon SQS - standard queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues.html)
  for redundant storage before the send is acknowledged.
- Lesson 1001, delivery semantics: [Amazon SQS - visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)
  for the lease, the 30-second default, the 12-hour ceiling measured from first receipt, the heartbeat
  advice and the in-flight quota; [RabbitMQ - Consumer Acknowledgements and Publisher Confirms](https://www.rabbitmq.com/docs/confirms)
  for automatic against manual acknowledgement and the requeue on channel or connection close;
  [Celery - Tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html) for `acks_late` stated as the
  explicit choice between the two guarantees; and
  [Sidekiq - Best Practices](https://github.com/sidekiq/sidekiq/wiki/Best-Practices) for the flat refusal
  of an exactly-once guarantee.
- Lesson 1002, retries: [AWS Architecture Blog - Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
  for the clustering that backoff alone leaves behind and the reported halving of the call count at 100
  contending clients, with the four strategies read from its published
  [simulator](https://github.com/aws-samples/aws-arch-backoff-simulator) rather than from the post's
  images; [Google SRE Book - Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)
  for retry amplification as a product across layers and the server-wide retry budget; and
  [Amazon SQS - dead-letter queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)
  for `maxReceiveCount` and the standard-queue retention clock that does not reset on the move.
- Lesson 1003, idempotent consumers: [Amazon SQS - exactly-once processing](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-exactly-once-processing.html)
  for the five-minute deduplication interval and the fact that it covers the `SendMessage` action rather
  than delivery, read beside the visibility-timeout page's statement that there is still no absolute
  guarantee against a second delivery. [Sidekiq - Best Practices](https://github.com/sidekiq/sidekiq/wiki/Best-Practices)
  and [Celery - Tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html) for idempotence stated as
  the job author's obligation.
- Lesson 1004, the dual write: [microservices.io - Transactional outbox](https://microservices.io/patterns/data/transactional-outbox.html)
  for the problem, the solution and - unusually for a pattern page - the residual weakness, which is that
  the message relay might publish a message more than once.
- Lesson 1005, the inverted index: [PostgreSQL - Introduction to Full Text Search](https://www.postgresql.org/docs/current/textsearch-intro.html)
  for the three failings of pattern matching, the token-to-lexeme vocabulary and the `tsvector` /
  `tsquery` pair; [PostgreSQL - GiST and GIN Index Types](https://www.postgresql.org/docs/current/textsearch-indexes.html)
  for the inverted index as an entry per lexeme with a compressed location list, GIN as the preferred
  type and GiST's lossiness; and [Elasticsearch - Near real-time search](https://www.elastic.co/docs/manage-data/data-store/near-real-time-search)
  for the refresh that puts about a second between a write and a searchable document.
- Lesson 1006, relevance: [Lucene - `BM25Similarity`](https://lucene.apache.org/core/9_11_1/core/org/apache/lucene/search/similarities/BM25Similarity.html)
  for what `k1` and `b` control, their 1.2 and 0.75 defaults and the Okapi at TREC-3 origin;
  [Elasticsearch - Similarity settings](https://www.elastic.co/docs/reference/elasticsearch/index-settings/similarity)
  for the same two descriptions and defaults on the engine most readers meet BM25 in; and
  [PostgreSQL - Controlling Text Search](https://www.postgresql.org/docs/current/textsearch-controls.html)
  for `ts_rank`, `ts_rank_cd`, the `{0.1, 0.2, 0.4, 1.0}` weights, the normalisation bit flags and the
  statement that ranking requires consulting the `tsvector` of each matching document. Robertson and
  Zaragoza, *The Probabilistic Relevance Framework: BM25 and Beyond*, Foundations and Trends in
  Information Retrieval 3(4), 2009, is named as the standard derivation; the module cites the
  implementations for every number it states.

### Module 12 - Inter-service communication

- Lesson 1200, the three couplings: [Apache Kafka - Introduction](https://kafka.apache.org/intro) for
  the statement that events "are not deleted after consumption" and that retention is a per-topic
  setting, [RFC 6455 &sect;1.1](https://www.rfc-editor.org/rfc/rfc6455#section-1.1) for why HTTP polling
  was worth replacing, and [RabbitMQ - Consumer acknowledgements](https://www.rabbitmq.com/docs/confirms)
  for the at-least-once consequence. The chain-availability arithmetic on that page is derived here from
  a stated 99.9% per-service assumption, not quoted from a source.
- Lesson 1201, gRPC on the wire: [gRPC over HTTP/2](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md)
  for the one-RPC-one-stream mapping, the request header set including `te: trailers`, the
  length-prefixed message framing, and the rule that status is sent in trailers even when it is OK;
  [gRPC core concepts](https://grpc.io/docs/what-is-grpc/core-concepts/) for the four call shapes; and
  [gRPC custom load balancing](https://grpc.io/docs/guides/custom-load-balancing/) for `pick_first`
  doing no load balancing at all; and
  [the gRPC-Web protocol](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-WEB.md) for the browser
  limitation, the status moved into the response body, and the proxy-translation deployment model.
- Lesson 1202, deadlines: [gRPC - Deadlines](https://grpc.io/docs/guides/deadlines/) for the
  deadline-against-timeout distinction, the absence of a default, the propagation rule that deducts
  elapsed time so clocks need not agree, and the guidance on choosing a value;
  [gRPC core concepts](https://grpc.io/docs/what-is-grpc/core-concepts/) for the independent local
  determinations of success and for changes before a cancellation not being rolled back; and
  [gRPC status codes](https://grpc.io/docs/guides/status-codes/) for DEADLINE_EXCEEDED being possible
  on a successful operation and for the UNAVAILABLE retry advice with its non-idempotent caveat. The
  retry-amplification figure is derived here from a stated three-attempts-per-hop assumption.
- Lesson 1203, queues: [RabbitMQ - Consumer acknowledgements and publisher confirms](https://www.rabbitmq.com/docs/confirms)
  for automatic acknowledgement being unsafe, automatic requeue on channel or connection close, the
  `redeliver` flag and the idempotence requirement;
  [AMQP 0-9-1 concepts](https://www.rabbitmq.com/tutorials/amqp-concepts) for exchanges, bindings and
  the four exchange types including fanout ignoring the routing key;
  [RabbitMQ - Dead letter exchanges](https://www.rabbitmq.com/docs/dlx) for the four dead-lettering
  conditions and the `x-death` header; and
  [Transactional outbox](https://microservices.io/patterns/data/transactional-outbox.html) for the
  dual-write problem and the relay's own at-least-once residue.
- Lesson 1204, the log: [Apache Kafka - Introduction](https://kafka.apache.org/intro) for retention,
  partitioning and the same-key-same-partition ordering guarantee, and
  [Apache Kafka - Design](https://kafka.apache.org/40/design/design/) for the three delivery semantics,
  the offset-commit ordering that selects between at-most-once and at-least-once, the idempotent
  producer and transactions, the advice to store the consumer offset alongside its output, and the rule
  that a partition is read by exactly one consumer in a group. Head-of-line blocking on a partition is
  derived on the page from those rules rather than quoted.
- Lesson 1205, WebSockets: [RFC 6455](https://www.rfc-editor.org/rfc/rfc6455), &sect;1.1 and &sect;1.3, for the polling
  background, the `Upgrade` handshake with `Sec-WebSocket-Key` and `Sec-WebSocket-Accept`, the 101
  response, the independent two-way channel and the closing handshake;
  [MDN - Writing WebSocket client applications](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_client_applications)
  for the error event closing the connection and the absence of automatic reconnection; and
  [MDN - Using server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
  for the one-way constraint, the automatic restart with `retry` and `id`, and the six-connection
  HTTP/1.1 limit against HTTP/2's negotiated streams defaulting to 100.
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

- A concrete B-tree fanout for a given key width and page size. Lesson 0804 derives its depth arithmetic from an assumed
  fanout of 200 and labels the assumption on the figure rather than quoting a figure the documentation does not state.
- Codd's 1970 paper, *A Relational Model of Data for Large Shared Data Banks*, is the origin of the model Module 08 teaches
  and is behind a paywall that refused every fetch attempted while the module was written. Lesson 0800 therefore grounds the
  model on the PostgreSQL documentation, which states the same properties, rather than citing a paper nobody opened.
