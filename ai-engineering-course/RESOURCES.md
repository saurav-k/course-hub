# End-to-End AI Engineering - Resources

The sources this course trusts.
A page cites from here; anything new goes in here first, in the same pull request.

**This file is seeded, not finished.**
It carries the canon the three research reports opened, at the version each was read at, so that no module writer has to re-establish a version number.
The per-module supporting lists are filled by each module writer inside their own pull request, and the whole file is tidied by the integrator in one pass after the eight modules land, for the same reason `reference/glossary.html` is: every module would otherwise append to one alphabetical list and conflict with every sibling.

A version recorded here is the version the source was **opened** at. If you cite a source, open it again and correct the row if it has moved.

## The canon

The small set this course keeps returning to. Primary only.

### The protocols

- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/latest) - revision **`2026-07-28`**. `LATEST_PROTOCOL_VERSION` is declared in `schema.ts` at that revision. The nine changes from `2025-11-25` matter: protocol sessions and the `initialize` handshake are gone, `server/discover` is mandatory, `subscriptions/listen` replaces the GET endpoint, tasks moved to an extension, every result carries a `resultType`, and SSE resumability was removed. Leaned on by `0440`, `0540`, `0670`.
- [A2A specification](https://github.com/a2aproject/A2A) - tag **`v1.0.1`**, protocol version **`1.0`**, read in `docs/specification.md` and `specification/a2a.proto`. The Agent Card, the eleven RPCs and the `TaskState` machine. Leaned on by `0540`. A2A appears nowhere else in this hub.
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai) - **no releases and no tags**; read at commit `fee465db333bdd6a7d2faa320edab5cf3101a4f4`. Every document is **Status: Development**. The six span kinds, the retrieval span's attributes, the twelve metrics, and the `mcp.*` conventions. Leaned on by the whole observability thread and by `0670`. See the status rule in `NOTES.md`.
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) - the **2025** edition. `LLM01` prompt injection and `LLM08` vector and embedding weaknesses. Leaned on by `0280` and `0650`.

### The retrieval papers

- [Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*](https://arxiv.org/abs/2005.11401) - `v4`. What RAG named: parametric against non-parametric memory. `0000`, `0120`.
- [Thakur et al., *BEIR*](https://arxiv.org/abs/2104.08663) - `v4`. Eighteen datasets, nDCG@10 as the standard measure, and BM25 as a robust baseline. `0160`, `0260`.
- [Muennighoff et al., *MTEB*](https://arxiv.org/abs/2210.07316) - `v3`. No embedding method dominates across tasks, which is what kills "pick the top of the leaderboard". `0130`.
- [Malkov & Yashunin, *HNSW*](https://arxiv.org/abs/1603.09320) - `v4`. The layered proximity graph and its logarithmic scaling. `0140`.
- [Nogueira & Cho, *Passage Re-ranking with BERT*](https://arxiv.org/abs/1901.04085) - `v5`. The cross-encoder second pass. `0270`.
- [Cormack, Clarke & Buettcher, *Reciprocal Rank Fusion*](https://dl.acm.org/doi/10.1145/1571941.1572114) - SIGIR'09. The formula and `k = 60`. `0260`.
- [Robertson & Zaragoza, *The Probabilistic Relevance Framework: BM25 and Beyond*](https://doi.org/10.1561/1500000019) - 2009. BM25, and its own statement that the model gives no guidance on setting `b` and `k1`. `0260`.
- [Liu et al., *Lost in the Middle*](https://arxiv.org/abs/2307.03172) - `v3`. Position sensitivity in long contexts. `0240`.
- [Qu, Tu & Bao, *Is Semantic Chunking Worth the Computational Cost?*](https://arxiv.org/abs/2410.13070) - `v1`. `0220`.
- [Guenther et al., *Late Chunking*](https://arxiv.org/abs/2409.04701) - `v3`. `0230`.
- [Gao et al., *HyDE*](https://arxiv.org/abs/2212.10496) - `v1`. `0130`.
- [Es et al., *Ragas*](https://arxiv.org/abs/2309.15217) - `v2`. Reference-free RAG evaluation. `0170`.
- [Zheng et al., *Judging LLM-as-a-Judge*](https://arxiv.org/abs/2306.05685) - `v4`. Over 80% agreement with humans, and the position, verbosity and self-enhancement biases. `0170`.
- [Asai et al., *Self-RAG*](https://arxiv.org/abs/2310.11511) - `v1`, and [Yan et al., *Corrective RAG*](https://arxiv.org/abs/2401.15884) - `v3`. Retrieve on demand, and a retrieval evaluator with a confidence degree. `0400`, `0410`.
- [Greshake et al., *Not what you've signed up for*](https://arxiv.org/abs/2302.12173) - `v2`. Indirect prompt injection through retrieved data. `0280`.

### The agent papers

- [Yao et al., *ReAct*](https://arxiv.org/abs/2210.03629) - `v3`. Interleaved reasoning and acting. `0300`.
- [Shinn et al., *Reflexion*](https://arxiv.org/abs/2303.11366) - `v4`, and [Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*](https://arxiv.org/abs/2310.01798) - `v2`. **These two disagree and `0360` is written on the disagreement**, which is that the signal has to come from outside.
- [Madaan et al., *Self-Refine*](https://arxiv.org/abs/2303.17651) - `v2`. `0360`.
- [Park et al., *Generative Agents*](https://arxiv.org/abs/2304.03442) - `v2`, and [Packer et al., *MemGPT*](https://arxiv.org/abs/2310.08560) - `v2`. Memory as a stream, and memory as tiers. `0340`, `0350`.
- [Fourney et al., *Magentic-One*](https://arxiv.org/abs/2411.04468) - `v1`. The outer task ledger and the inner progress ledger. `0520`.
- [Yao et al., *tau-bench*](https://arxiv.org/abs/2406.12045) - `v1`. Database-state grading and the `pass^k` reliability metric. `0370`.
- [Cemri et al., *Why Do Multi-Agent LLM Systems Fail?* (MAST)](https://arxiv.org/abs/2503.13657) - `v3`. Fourteen failure modes in three categories, over 1,600 annotated traces. `0310`, `0550`.

### The operations papers

- [Beurer-Kellner et al., *Design Patterns for Securing LLM Agents against Prompt Injections*](https://arxiv.org/abs/2506.08837) - `v3`. Six named patterns: Action-Selector, Plan-Then-Execute, LLM Map-Reduce, Dual LLM, Code-Then-Execute, Context-Minimization. **The paper's central claim is a negative one** and `0650` may not soften it into a menu of hardening tips.
- [Debenedetti et al., *Defeating Prompt Injections by Design* (CaMeL)](https://arxiv.org/abs/2503.18813) - `v2`. 77% of AgentDojo tasks with provable security, against 84% undefended. `0650`.
- [Bang & Feng, *GPTCache*](https://aclanthology.org/2023.nlposs-1.24/) - NLP-OSS 2023. The only primary source that measured a semantic cache's **false-hit** rate as well as its hit rate. `0640`.
- [Sculley et al., *Hidden Technical Debt in Machine Learning Systems*](https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) - NIPS 2015, and [Amershi et al., *Software Engineering for Machine Learning*](https://www.microsoft.com/en-us/research/publication/software-engineering-for-machine-learning-a-case-study/) - ICSE 2019. `0100`. See `## Gaps`.
- [Mitchell et al., *Model Cards for Model Reporting*](https://arxiv.org/abs/1810.03993) - `v2`. `0810`. See `## Gaps`.

### First-party engineering writing

Primary for what that organisation did, and never a third-party benchmark. Every number from these carries its measurer in the sentence that quotes it.

- [Anthropic, *Introducing Contextual Retrieval*](https://www.anthropic.com/engineering/contextual-retrieval) - the failure-rate ladder measured on Anthropic's own corpora, the per-million-token cost of generating context, and the 200,000-token rule for a corpus small enough to need no retrieval at all. `0000`, `0120`, `0230`.
- [Anthropic, *Effective context engineering for AI agents*](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - the attention budget, context rot, and the three long-horizon techniques. `0240`.
- [Anthropic, *Building effective agents*](https://www.anthropic.com/engineering/building-effective-agents) - the workflow-against-agent definition and the five workflow patterns. `0300`.
- [Anthropic, *How we built our multi-agent research system*](https://www.anthropic.com/engineering/multi-agent-research-system) - the token multipliers and the internal-eval result. `0450`, `0500`, `0700`.
- [Cognition, *Don't Build Multi-Agents*](https://cognition.ai/blog/dont-build-multi-agents) - the counter-position to the post above, and `0500` is written on both. 
- [LinkedIn Engineering, *Musings on building a Generative AI product*](https://www.linkedin.com/blog/engineering/generative-ai/musings-on-building-a-generative-ai-product) - the routing/retrieval/generation split, the structured-output failure rate and its fix, and the honest shape of the quality curve. `0620`, `0660`, `0710`.
- [Uber Engineering, *QueryGPT*](https://www.uber.com/en-US/blog/query-gpt/) - the four-agent decomposition and the adoption numbers. `0710`.

### First-party vendor documentation

- [Claude tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) - a tool is a name, a description and an `input_schema`; the published per-model token cost of the tool-use system prompt. `0210`, `0320`.
- [Claude prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) - the write and read multipliers, the breakpoint limit, the lookback, the per-model minimums, and the `tools` to `system` to `messages` invalidation cascade. `0630`.
- [Claude Message Batches API](https://platform.claude.com/docs/en/build-with-claude/batch-processing) - the discount and the batch limits. `0600`.
- [Claude memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) - six commands, client-side execution, and the path-traversal responsibility that lands on the implementer. `0350`.
- [Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output) - a documented subset of JSON Schema. `0210`.
- [Gemini context caching](https://ai.google.dev/gemini-api/docs/caching) - the implicit/explicit split and the minimums. `0630`. See `## Gaps`.
- [pgvector](https://github.com/pgvector/pgvector) - tag `v0.8.6`. HNSW and IVFFlat, the four knobs, and the filtering behaviour that returns four rows when a condition matches 10% of them. `0140`.
- [Pydantic](https://docs.pydantic.dev/) - `2.13.x`. Schema generation, strict and lax modes. `0210`.
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) - `1.2.x`. The checkpointed pause, and the caveat that the runtime restarts the whole node rather than resuming at the line. `0420`.
- [Ragas metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/) - `0.4.x`. The metric **names** are the canon here; the 0.x API is not. `0170`.
- [uv](https://docs.astral.sh/uv/) - `0.12.x`. `0110`.
- [FastAPI](https://fastapi.tiangolo.com/async/) - `0.141.x`, still pre-1.0. `0600`.
- [Kubernetes probes and HPA](https://kubernetes.io/docs/) - `v1.37`. `0610`, `0670`.
- [OpenSSF Scorecard](https://github.com/ossf/scorecard) - `v5.5.0`, nineteen named checks, and [Diataxis](https://diataxis.fr/). `0810`. See `## Gaps`.

## Supporting sources

Cited once or twice, by page. **Each module writer adds their own rows here, inside their own pull request.**

### Module 01 - Foundations

### Module 02 - Retrieval quality and context engineering

### Module 03 - Agents and agentic systems

### Module 04 - From basic to agentic RAG

### Module 05 - Multi-agent systems

### Module 06 - Deployment, optimization and reliability

### Module 07 - Agentic AI system design

### Module 08 - Final delivery

## Wisdom

Where the practitioners argue, for a reader who wants to test their understanding against people who do this.

- The two published positions on multi-agent systems, held by two companies that both ship them, are the best argument in the course: Anthropic's orchestrator-worker post against Cognition's *Don't Build Multi-Agents*. Read both before writing `0500`.

## Not used, and why

- **`openai.com` is unreachable to the tooling that built this course.** The OpenAI Agents SDK is cited from its GitHub repository and from PyPI metadata only, and nothing about OpenAI's own caching, batching or pricing rests on this research. Do not write such a claim from memory.
- **AutoGen** is named by the syllabus and its `autogen-agentchat` package had gone eleven months without a release when the research was done. It is evidence for a historical framing and is not a fixture in any lesson.
- **Vendor pages for semantic caching.** Every one of them quotes a hit rate and none quotes a false-hit rate, which is why `0640` is written from the one primary source that measured both.

## Gaps

Claims this course would like to make and cannot source.
**A gap recorded here is a gap the course does not assert on a page.** An unsourceable claim goes here, not into a lesson wearing a hedge.

- **"Only a small fraction of a real ML system is ML code."** This is Sculley et al.'s Figure 1 and it is not on the abstract page. Do not use the figure or a percentage until somebody opens the PDF. The debt list itself is from the abstract and is safe.
- **The nine stage names of Amershi et al.'s ML workflow.** The publication page states there is a nine-stage workflow and does not enumerate it. `0100` describes the workflow without claiming the names, or somebody opens the paper.
- **Corrective RAG's three confidence labels.** The abstract describes a confidence degree that triggers different retrieval actions and does not name the actions. `0410` says "three outcomes" until somebody reads the paper body.
- **The original nDCG definition.** Jarvelin & Kekalainen, TOIS 2002, was not opened. `0160` cites BEIR's use of nDCG@10 as the standard practice, which is a source that was opened. A writer who wants the formula opens the original.
- **A recommended chunk size from Anthropic's contextual-retrieval post.** The post says chunks are "usually no more than a few hundred tokens" and gives no number. Do not print one.
- **The task list behind the format-restriction result.** The abstract says "various common tasks" and names none.
- **Model card section names.** arXiv:1810.03993v2's abstract was read and the PDF was not. `0810` may cite the paper for the idea and may not list its sections.
- **Diataxis authorship and licence.** The four modes and the two axes are on the page. The colophon was not read, and this hub requires a named licence before quoting an artefact. Cite the framework by URL and quote nothing until somebody reads it.
- **MITRE ATLAS tactic names.** The release and the technique count were confirmed; the tactics file fetch failed. The count is safe to state and a tactic list is not.
- **Gemini context-cache pricing and TTL.** The documentation carries the minimums and the implicit/explicit split and neither the storage price nor the TTL. State the minimums; do not state a Gemini discount figure.
- **vLLM automatic prefix caching internals.** Not read. `0630` links `llm-inference-course` rather than describing block hashing from memory.
- **promptfoo's version.** The CI documentation carries the commands and no version. `0660` either pins from a commit or teaches the gate generically with promptfoo as one instance.
- **A measured recovery rate for error visibility.** `0330`'s central claim - that an error the model cannot see is an error it cannot correct - is stated by the MCP specification and, at the time of research, had no measurement behind it that could be opened. The page argues it qualitatively or somebody finds the number.
