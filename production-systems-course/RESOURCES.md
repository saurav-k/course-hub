# Production Systems Resources

188 citations across eleven chapters. Every URL was fetched and read before it was cited. This file lists the sources worth returning to, not all of them - the chapters carry the rest inline.

## Knowledge

### Standards and specifications

- [RFC 9110 - HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), [RFC 9111 - HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html), [RFC 9113 - HTTP/2](https://www.rfc-editor.org/rfc/rfc9113.html), [RFC 9114 - HTTP/3](https://www.rfc-editor.org/rfc/rfc9114.html), [RFC 9000 - QUIC](https://www.rfc-editor.org/rfc/rfc9000.html)
  The transport and caching layer, stated normatively. Use for: anything where "how does HTTP actually behave" is the question.
- [RFC 6455 - WebSocket](https://www.rfc-editor.org/rfc/rfc6455.html), [RFC 6202 - Long Polling](https://www.rfc-editor.org/rfc/rfc6202.html), [WHATWG HTML - Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html)
  The three real-time options, from their own definitions. Use for: choosing a push transport.
- [RFC 8446 - TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446), [RFC 6749 - OAuth 2.0](https://www.rfc-editor.org/rfc/rfc6749), [RFC 7636 - PKCE](https://www.rfc-editor.org/rfc/rfc7636), [RFC 9700 - OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700), [RFC 7519 - JWT](https://www.rfc-editor.org/rfc/rfc7519), [RFC 7009 - Token Revocation](https://www.rfc-editor.org/rfc/rfc7009)
  Use for: the security chapter's whole argument. RFC 9700 is the one most engineers have not read and should.
- [RFC 5905 - NTP](https://www.rfc-editor.org/rfc/rfc5905), [RFC 1035 - DNS](https://www.rfc-editor.org/rfc/rfc1035), [RFC 2181 - DNS Clarifications](https://www.rfc-editor.org/rfc/rfc2181)
  Use for: clock skew and the DNS failover arithmetic.

### Papers

- [The Tail at Scale - Dean and Barroso](https://research.google/pubs/the-tail-at-scale/)
  Why fan-out turns a rare slow response into a common one. The single most useful paper in this course.
- [Dynamo - DeCandia et al., SOSP 2007](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
  Quorums, eventual consistency, and the operational reasoning behind them.
- [Spanner - Corbett et al., OSDI 2012](https://research.google/pubs/spanner-googles-globally-distributed-database/)
  TrueTime, and what bounding clock uncertainty actually buys.
- [CAP: Gilbert and Lynch 2002](https://users.ece.cmu.edu/~adrian/731-sp04/readings/GL-cap.pdf) with [Brewer, "CAP Twelve Years Later" (2012)](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/)
  Read both or neither. The second is where Brewer says the two-of-three framing "was always misleading".
- [The Network is Reliable - Bailis and Kingsbury](https://bailis.org/papers/partitions-queue2014.pdf)
  Partitions are not hypothetical. Use for: arguing that the partition branch of CAP is a real operating condition.
- [Raft - Ongaro and Ousterhout](https://raft.github.io/raft.pdf), [Chubby - Burrows, OSDI 2006](https://www.usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows_html/)
  Leader election and the lock service that popularised it.
- [Maglev - Eisenbud et al., NSDI 2016](https://research.google/pubs/maglev-a-fast-and-reliable-software-network-load-balancer/), [Scaling Memcache at Facebook](https://research.facebook.com/publications/scaling-memcache-at-facebook/), [An Analysis of Facebook Photo Caching](https://research.facebook.com/publications/an-analysis-of-facebook-photo-caching/)
  Load balancing and caching at a scale where the arithmetic is published.

### Operations

- [Google SRE Book](https://sre.google/sre-book/table-of-contents/) - especially [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/), [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/), [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/), and [Handling Overload](https://sre.google/sre-book/handling-overload/)
  Free, and the primary source for most of chapters 2 and 10. Cite the chapter, not the book.
- [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)
  Use for: tracing and metric attribute names that will still make sense to the next team.
- [Principles of Chaos Engineering](https://principlesofchaos.org/)
  Use for: the discipline, not the tooling.

### First-party documentation worth trusting

PostgreSQL (indexes, planner, EXPLAIN, hot standby, PITR), Kubernetes (deployments, probes, CronJob), Envoy (load balancing, circuit breaking), Kafka, RabbitMQ, AWS (DynamoDB partition keys, IAM policy evaluation, IMDS, KMS), Cloudflare engineering blog, Stripe API (idempotency, webhooks), OWASP cheat sheets.

## Wisdom (Communities)

- [r/ExperiencedDevs](https://www.reddit.com/r/ExperiencedDevs/) - senior-level discussion, moderated against career-advice noise.
- [USENIX SREcon](https://www.usenix.org/srecon) - talks and papers from people running these systems, most freely available afterwards.
- [Papers We Love](https://paperswelove.org/) - reading groups for the papers above, if reading alone is not working.

## Gaps

Recorded honestly, because these shaped what the chapters could claim.

- **Several AWS Builders' Library pages now redirect to an empty shell.** Two chapters wanted them for retry and backlog guidance and could not read them, so that arithmetic is derived from stated assumptions instead of borrowed.
- **ACM and USENIX PDFs frequently return 403 to automated fetching.** Where an author-hosted copy of the same paper existed it was used; where none existed the paper was dropped rather than cited unread.
- **The original Sagas paper (1987) and the Raft PDF could not be text-extracted on this machine.** They are cited as origin works and no factual claim in the course rests on their body text; the mechanics are grounded in sources that could be read.
- **Vendor numbers on living pages will drift.** Cloudflare purge limits, Envoy's build and lookup comparisons, and AWS retry defaults - which AWS currently marks as requiring an opt-in flag - are all current-at-time-of-writing rather than stable.
- **Derived numbers are labelled as derived.** Region latency floors assume a fibre group index of 1.47 and great-circle paths; cache offload percentages are arithmetic on published traffic shares rather than published figures. Every one of these is marked in the text.
- **One architectural claim remains reasoning rather than a documented case**: that long-lived game sessions pinned to fixed addresses belong behind a relay tier. It is marked as such in chapter 1.
- **No public source gives a defensible cost-per-request figure for a named company.** Cost arithmetic in chapter 8 is built from stated unit assumptions, and the reader is told to substitute their own.
- **EC2 on-demand prices in chapter 8 are stated without a link.** AWS renders that price table via JavaScript, so it could not be fetched; the figures were read from the JSON price feed backing the page, which is too fragile a URL to cite. Treat them as list prices at time of writing and substitute your own contract rates.
- **The log storage price in chapter 10 is a placeholder**, labelled as such in the text, because no vendor figure was verified. Replace it with your own contract price before using that arithmetic.
