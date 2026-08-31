# Plot - the reading order of Backend Engineering

This file records the true reading order of the course. Fill it from the interview answer about order
and the course map written in step 2 of `../new-course.md`, not from a guess.

The order rule, which holds for this course and every course in the hub: **a course's reading order is
its true order, and a tutorial or lab session that follows a lecture sits after that lecture in the
course map, never in a separate list at the bottom.**
When this file and the course `index.html` disagree, one of them is wrong, and it gets fixed before
anything new is added.

Status marks used below:

- **written** - on the site today.
- **in progress** - being written right now, not yet on this branch.
- **reserved** - the position is held; nothing else may take it; nothing is written.

## The sequence

Reading order, derived from the upstream field manual but re-sequenced so each mechanism is owned
before the next depends on it.

| # | Position | Status | Notes |
|---|---|---|---|
| 1 | Module 01 - The shape of a request (0000) | written | On-ramp: reason one request end to end before any mechanism is named. The whole map in one page. |
| 2 | Module 02 - HTTP is the language (0200-0205) | written | Methods, status, headers, caching headers, CORS. RFC 9110, RFC 9111 and RFC 9113 owned. |
| 3 | Module 03 - Routing (0300-0305) | written | The route as a pair, path against query, the prefix tree, the middleware chain, the 404/405 verdicts and prefix mounting. RFC 3986 and RFC 6570 join the canon; Go's ServeMux is the named implementation the mechanism pages read from. |
| 4 | Module 04 - Serialization and contracts (0400-0405) | written | The wire contract, JSON's six types, schema-first protobuf, boundary parsing, content negotiation, and the compatibility rules. It was written before Module 03 landed, because nothing in it depends on routing. |
| 5 | Module 05 - The layered service (0500-0505) | written | Layers as testable boundaries, controller, service, repository, request context, dependency direction. Written before Module 03 landed, because it depends on nothing routing defines. |
| 6 | Module 06 - API design (0600-0605) | written | The promise and its cost of breaking, the uniform interface, cursor pagination, RFC 9457 problem documents, the three versioning bills, and idempotency keys. Written before Modules 03 and 05 landed, because nothing in it depends on routing or on the internal layering. |
| 7 | Module 07 - Auth and security (0700-0706) | written | The two questions and their two lifetimes, sessions, self-contained tokens, OAuth with PKCE, then the threat model: injection, XSS and CSRF, each taught attack first. |
| 8 | Module 08 - Data | reserved | The relational model, transactions, indexes; then the non-relational map. |
| 9 | Module 09 - Caching (0900-0905) | written | Why a cache exists and the arithmetic of a hit rate, cache-aside against read-through, the four write patterns, key design as invalidation design, the staleness window and the stale-set race, and the four failure modes. Written while Module 08 stays reserved, because it depends on nothing that module defines. |
| 10 | Module 10 - Async work & search | reserved | Queues and background jobs; then full-text search. |
| 11 | Module 11 - Resilience & observability | reserved | Error handling, config, logging, graceful shutdown. |
| 12 | Module 12 - Inter-service communication | reserved | gRPC, message brokers / Kafka, WebSockets. |
| 13 | Module 13 - Scale, fleet and shipping (1300-1306) | written | Concurrency and shared state inside one process, statelessness and the fleet, containers and the control loop, the test budget and the deployment pipeline. Written while Modules 08 to 12 were still reserved, because it names their mechanisms and links forward to them rather than depending on them, and because it closes the course's arc. |

Reference sheets and glossaries read alongside and are recorded as such; they are not positions in the
sequence.

## Planned but unwritten

Everything the course intends but nobody has written: reserve the position now, with a status of
`reserved` and one line on when the position was claimed and by what plan.
A position reserved costs nothing; a position taken by accident is a renumbering.

Modules 08 and 10-12 above are all reserved from the first scaffold, mapped to the upstream chapters. Each
lands as a separate change so the course grows a module at a time without a trapped mega-PR.

Module 05 was written out of reading order, before Module 03 landed, because it depends on nothing routing
defines: it consumes the parsed, trusted values Module 04 produces and says only where they travel afterwards.
Its lesson numbers start at 0500, so the 03xx block stayed free for the module that owns it and nothing was
renumbered when Module 03 landed ahead of it.

Module 03 landed fifth and takes the 03xx block, for the same reason Module 02 took 02xx: each module owns a
hundred-block so a later module never renumbers an earlier one. It answers the question Module 02 leaves open - the
request has arrived and its method and target are understood, so how does it become a specific piece of code.
It lands after Modules 04 and 06 rather than before them, because neither of those depends on routing.

Module 13 landed as the closing module rather than as the next one in sequence. It names mechanisms
Modules 08 to 12 will develop - a transaction, a cache, a graceful shutdown - and links forward
to them rather than depending on them, so a reader reaches the whole-course view without needing a
module that is not yet on the site. Its name is `fleet` rather than `flight`: `index.html`,
`MISSION.md` and the roadmap row all said `fleet`, this file was the single outlier, and the rule two
paragraphs above settles a disagreement between two files in favour of the one that ships.

Module 06 landed fourth, after Module 04, because the API surface is what the serialization contract is
a surface *of*: the compatibility rules of lesson 0405 run out at a breaking change, and lesson 0604 is
where that hand-off is made. It needs neither routing nor the layered service to be readable.

Module 07 landed after Module 06, because the interface Module 06 published is the thing
this module decides who may invoke. It needs neither routing nor the layered service: the credential
arrives in a header or a cookie that Module 02 already named, and the three threats are properties of
the interpreters a handler talks to rather than of how the handler was reached. Its second half is
ordered threat before defence throughout - injection, then XSS as the same defect with the browser as
the interpreter, then CSRF as the one that needs no injected code at all - so lesson 0706 can close on
the symmetry between the last two.

Module 09 landed while Module 08 stays reserved. It needs neither the layered service nor the data
module: a cache is reasoned about from the request and the store, both of which Module 01 already names, and lesson 0204 deliberately taught the protocol
cache first so that this module could be about invalidation rather than about mechanism. Where it needs
the relational store it links Module 08 as the owner of the truth rather than restating it.

Module 02 landed second, immediately after the on-ramp and before any of modules 03 to 13, because
every later module consumes the vocabulary it defines: routing consumes the method and the target,
serialization consumes the representation fields, and auth consumes the credential fields.
Its lesson numbers start at 0200 rather than continuing from 0000, so each module owns a hundred-block
and a later module never renumbers an earlier one.

## Adding a session to this course

1. Read the course's authoring contract files first.
2. Take the next free lesson number. Never renumber anything.
3. Insert the new material at its true position in this file and in `index.html`, never appended to
   the bottom because it arrived last.
4. Re-run `python3 scripts/gen_outline.py backend-engineering-course`, commit the regenerated
   `outline.js`, run `python3 scripts/validate_site.py`, and open the changed pages in both themes
   before opening the pull request.