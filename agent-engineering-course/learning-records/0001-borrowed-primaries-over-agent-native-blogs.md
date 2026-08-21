# 0001 - Borrowed primaries over agent-native blogs

**Date:** 2026-08-21
**Status:** Accepted

## Context

Four of this course's eighteen topics have no agent-specific primary source, and it is not close.

- **Shadow testing.** Every agent-flavoured write-up of "route 5 percent of traffic to a new prompt" is a blog post restating a delivery practice that predates language models by a decade.
- **Async tool execution.** There is no specification for "an agent tool that takes four minutes". There is a mature specification for an API method that takes a long time.
- **Graceful degradation chains.** The ladder from a frontier model down to a cache is new; the discipline of shedding quality before capacity is not.
- **Cost kill-switches.** No published reference describes token-denominated per-tenant enforcement inside a model gateway. Cloud cost management documents the enforcement pattern thoroughly.

The repository's authoring rule is that every topic carries a linked primary source and never a blog summarising one.
Applied literally to these four topics, that rule has no satisfying answer, because the well-written agent-specific material *is* the blog layer and the primary layer sits one field over.

## Decision

Cite the **general software-engineering primary source** and make the transfer explicit in the prose, rather than citing an agent-specific secondary source that would look more topical.

In practice: Fowler on dark launching and the SRE Workbook on canarying for shadow testing, Google AIP-151 plus the Standard Webhooks specification for async tools, the SRE book chapter on cascading failures for degradation chains, and AWS Budgets actions for kill-switches.
Where the transfer is not exact, the text says which part transfers and which part does not, rather than letting the citation imply more coverage than it has.

## Why

- The rule's purpose is that the reader can check the claim against something authoritative. A blog post restating Fowler fails that test in a way that citing Fowler does not, even though the blog post would mention agents and Fowler does not.
- The transfer is the actual teaching content for this audience. A Principal engineer already knows dark launching. What they need is the sentence explaining that a shadow agent inheriting write credentials will send a duplicate email for every mirrored request, which is the part that is genuinely new.
- It keeps the course honest about its own novelty. Most of production agent engineering is existing operational discipline applied to a component with unusual cost and trust properties. Citing agent-native sources for everything would have implied the whole field is new, which would be flattering and wrong.
- The alternative, leaving those topics uncited, would have been worse: four of eighteen topics with no source at all is a visible hole in a course whose entire promise is a linked source per topic.

## Cost of this decision

The citations look less topical than a reader might expect.
Someone scanning Chapter 2's sources for shadow testing finds a 2020 Martin Fowler post rather than anything about agents, and could reasonably wonder whether the author found the current material.

Mitigation in place: every borrowed source is annotated in `RESOURCES.md` with what it is being used for, and the prose that cites it states the agent-specific consequence in the same paragraph.
`RESOURCES.md` also carries a `## Gaps` section that names each place where the agent-specific literature is genuinely thin, so the absence is documented rather than hidden behind a confident-looking link.

## Revisit when

An agent-specific primary source appears for any of these four topics.
The likeliest candidates are a specification for asynchronous tool results in a protocol such as MCP, which would replace AIP-151 for that topic directly, and peer-reviewed work on cost enforcement for agent systems.
When one lands, swap the citation and delete the corresponding entry from `## Gaps` in the same commit, so the two never drift apart.
