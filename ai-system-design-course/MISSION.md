# Mission

## Why this course exists

Pass system design rounds for Senior, Staff, and Principal AI/ML roles at companies like Meta, Google, Amazon, and Salesforce.

The learner is a Principal engineer with twelve years of distributed-systems experience. The gap is not system design. It is the new bottleneck set. A classic design round is bounded by databases, caches, and queues. An AI design round is bounded by tokens, context windows, retrieval quality, inference cost, hallucinations, model latency, evaluation, and user trust.

This course closes that gap. It assumes you can already reason about sharding, replication, consistency, and backpressure, and it spends its budget on what is genuinely new.

## Success looks like

At the whiteboard you can:

- Size a system in tokens and cost per query, not just QPS and storage.
- Defend a retrieval design on recall, precision, and grounding rather than "we use a vector database".
- Name the failure mode before the interviewer does, and say what degrades gracefully when it fires.
- Give an evaluation story with a golden dataset, an online signal, and an escalation path.
- Treat prompt injection and permission-aware retrieval as architecture, not as an afterthought.
- Choose between a large model, a small model, fine-tuning, and prompting, and justify it with numbers.

## Constraints

- Concept-first. The learner does not need code walkthroughs to understand a mechanism.
- Every claim carries a link to a primary source: a paper, a specification, or vendor documentation.
- Interview framing throughout. Each chapter ends with the questions an interviewer actually asks.

## Out of scope

- Training large models from scratch. This is a serving, retrieval, and operations course.
- Framework tutorials. Frameworks change; the bottlenecks do not.
- Coding rounds, behavioural rounds, and compensation strategy.

## Structure

Six chapters, one per pillar. Every topic in the pillar appears as its own section with a linked source, so the course doubles as a revision index.

1. LLM Basics
2. RAG and Retrieval
3. AI System Architecture
4. Cost and Performance
5. Evaluation and Quality
6. Reliability and Security
