# Mission

## Why this course exists

To be the reference an engineer actually reaches for when designing or operating a production system: 111 topics, each answered the same way, so the answers are comparable.

The learner is a Principal engineer with twelve years of experience. They know most of these words. What this course adds is the part that is usually missing: what each technique costs, what it looks like in a named real system, and how the decision changes as load grows.

## The organising idea

**Every topic is answered at three scale tiers: 100, 1,000, and 10,000 requests per second.**

That spine is the whole point. Most engineering writing describes a technique as though it were always correct. In practice, a decision that is over-engineering at 100 requests per second is table stakes at 10,000, and something that quietly works at 100 collapses at 1,000. Naming the tier at which a technique starts to matter is more useful than the technique itself.

## Success looks like

- You can size a component from a requirement, showing the arithmetic, rather than reaching for a familiar shape.
- You can name the scale at which a decision flips, and defend the flip.
- You can give a real system that uses each technique and say what would break without it.
- You can state the failure mode of anything you propose, not only its benefit.

## Constraints

- Concept-first. No framework tutorials; frameworks change and the bottlenecks do not.
- Every claim carries a linked primary source: an RFC, a specification, a paper, or first-party documentation.
- Arithmetic is shown, not asserted. Derived numbers are welcome; borrowed numbers must be in the source.
- Heavy on diagrams. A block diagram or a sequence diagram beats three paragraphs.

## Out of scope

- Language-specific implementation and framework APIs.
- Vendor comparison and procurement advice.
- Front-end concerns beyond the transport and security boundary.

## Structure

Eleven chapters, 111 topics.

1. Edge and Traffic Management
2. Resilience Patterns
3. Asynchronous and Event-Driven Systems
4. Protocols and Real-Time Transport
5. Database Performance
6. Distributing Data
7. Concurrency and Runtime
8. Scale, Latency and Cost
9. Delivery and Deployment
10. Observability and Operations
11. Security

## Siblings

This is the third course in a set. `ai-system-design-course` is the interview track for AI systems, `agent-engineering-course` is the build track for agents. This one is the substrate both of them assume.
