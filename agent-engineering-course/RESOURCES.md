# Production Agent Engineering Resources

Curated, high-trust sources behind every claim in this course.
Every URL here was fetched and read while the chapters were written.
Prefer these over blog summaries, and prefer a specification over a vendor's marketing page for the same product.

## Knowledge

### Context and protocol

- [Spec: Model Context Protocol, revision 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18)
  The authoritative protocol definition: hosts, clients, servers, JSON-RPC transport, and the resources, prompts, and tools a server may expose. Use for: building a server, the resource-versus-tool trust split, and the security section stating that tool descriptions from an untrusted server must themselves be treated as untrusted.
- [Article: "Effective context engineering for AI agents" - Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  Defines context engineering as curating and maintaining the optimal set of tokens during inference, and explains why a multi-turn agent makes prompt engineering insufficient. Use for: the displacement argument, and the vocabulary the whole course uses for the window.
- [Docs: Pydantic models](https://pydantic.dev/docs/validation/latest/concepts/models/)
  States the guarantee precisely: if validation completes without raising, the resulting instance conforms to the declared field types. Use for: typed handoffs, and for why a schema is a boundary rather than a formatting convention.
- [Docs: NVIDIA NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/latest/index.html)
  Rails declared as YAML configuration plus Colang flows, placed at five points in the request lifecycle: input, retrieval, dialog, execution, and output. Use for: guardrails-as-code as a concrete artifact shape rather than an aspiration.

### Evaluation and the data flywheel

- [Docs: Google Agent Development Kit, "Why Evaluate Agents"](https://adk.dev/evaluate/)
  Defines the trajectory as the sequence of steps including tool choice and strategy, and supplies both exact-match and rubric-judged trajectory metrics. Use for: trajectory evals, and the argument that process and outcome are complementary dimensions.
- [Article: "Dark Launching" - Martin Fowler](https://martinfowler.com/bliki/DarkLaunching.html)
  A backend change invoked for real users without the users being able to tell. Use for: shadow testing, and the distinction between measurement and exposure.
- [Chapter: "Canarying Releases" - Google SRE Workbook](https://sre.google/workbook/canarying-releases/)
  Partial, time-limited deployment evaluated against a control, with impact proportional to the traffic exposed. Use for: what a canary answers that a shadow cannot, and why metrics must be broken down by version.
- [Paper: "Hidden Technical Debt in Machine Learning Systems" - Sculley et al.](https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html)
  Names feedback loops, including direct ones where a system's outputs shape its own future data, as a principal source of hidden debt. Use for: why a flywheel needs an untouched holdout slice.
- [Chapter: "Postmortem Culture: Learning from Failure" - Google SRE Book](https://sre.google/sre-book/postmortem-culture/)
  The blameless framing and the line worth keeping: you cannot fix people, but you can fix systems and processes. Use for: the public teardown as an engineering artifact.

### State, async, and degradation

- [Docs: "Understanding Temporal"](https://docs.temporal.io/evaluate/understanding-temporal)
  Durable execution, the workflow event history as a complete durable log, and replay to recreate state after a worker crash. Use for: what durable execution gives you that a retry queue does not.
- [Docs: LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
  Checkpointers persisting thread state, enabling conversation continuity, human-in-the-loop, time travel, and fault tolerance. Use for: the framework-scoped alternative to a workflow engine, and where the boundary between them sits.
- [Spec: Google AIP-151, Long-running operations](https://google.aip.dev/151)
  Methods that take substantial time return an operation object rather than the ultimate response, comparable to a promise or future. Use for: the shape of an async tool call and the standard operations interface.
- [Spec: Standard Webhooks](https://www.standardwebhooks.com/)
  Open guidelines for sending webhooks securely and reliably, addressing server-side request forgery, spoofing, and replay. Use for: signed, timestamped, idempotent resumption of a parked agent.
- [Chapter: "Addressing Cascading Failures" - Google SRE Book](https://sre.google/sre-book/addressing-cascading-failures/)
  Separates load shedding from graceful degradation, and warns that degradation paths must be simple, monitored, and regularly exercised. Use for: the degradation chain and the reason each tier needs a scheduled test.

### Latency, cost, and local-first

- [Docs: NVIDIA LLM benchmarking metrics](https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html)
  Defines time to first token as the interval from submission to the first received token, and inter-token latency as the average time between consecutive tokens. Use for: the two clocks, and for vocabulary that matches published vendor numbers.
- [Paper: "GPTCache: An Open-Source Semantic Cache for LLM Applications" - Bang, NLP-OSS 2023](https://aclanthology.org/2023.nlposs-1.24/)
  The reference implementation of embedding-similarity caching in front of a model API. Use for: semantic caching mechanics, threshold management, and the shape of the cache key.
- [Docs: AWS Budgets, configuring budget actions](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-controls.html)
  A budget threshold that runs an action, including applying a restrictive policy, rather than only sending a notification. Use for: the difference between an alert and a kill-switch, and for the blast-radius decision.
- [Docs: MLX - Apple machine learning research](https://ml-explore.github.io/mlx/build/html/index.html)
  An array framework for Apple silicon whose arrays live in shared memory, so operations run on any supported device without data copies. Use for: on-device inference and why unified memory changes what is feasible locally.
- [Project: WebLLM - MLC AI](https://webllm.mlc.ai/)
  In-browser inference over WebGPU with no backend server and an OpenAI-compatible interface. Use for: the zero-egress, zero-marginal-cost path and its capability ceiling.

### Retrieval and isolation

- [Paper: "ColPali: Efficient Document Retrieval with Vision Language Models" - Faysse et al.](https://arxiv.org/abs/2407.01449)
  Embeds page images directly with a vision language model and retrieves by late interaction, rather than running a text-extraction pipeline first. Use for: multi-modal RAG, and the storage-against-recall trade of a multi-vector index.
- [Docs: Qdrant multitenancy guide](https://qdrant.tech/documentation/guides/multiple-partitions/)
  Recommends one collection with an indexed tenant field over a collection per tenant, plus user-defined sharding and tiered variants. Use for: multi-tenant vector design and why the filter must participate in the search.
- [Paper: "Defeating Prompt Injections by Design" - Debenedetti et al.](https://arxiv.org/abs/2503.18813)
  The CaMeL design, keeping control flow under a component that never reads untrusted content. Use for: the argument that injection is a control-flow problem rather than a filtering problem.
- [Paper: "Google's Approach for Secure AI Agents" - Diaz, Kern, and Olive](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/)
  Three principles: well-defined human controllers, carefully limited powers, and observable actions and planning, combining deterministic controls with reasoning-based defences. Use for: the vocabulary a reviewer expects, and for bounded authority as the load-bearing control.
- [Standard: OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
  The canonical threat list, with prompt injection and excessive agency both named. Use for: catalogue references in a security review. Note that this page is now maintained as a historical archive and active work has moved to the OWASP GenAI Security Project.

## Wisdom (Communities)

- [MLOps Community](https://mlops.community/)
  Practitioners running evaluation and operations in production. Use for: what evaluation practice actually looks like at teams that are not writing the papers.
- [Latent Space](https://www.latent.space/)
  Long-form practitioner interviews on production AI systems. Use for: how teams sequenced the work, which is the part papers never cover.
- [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/)
  The centre of gravity for on-device and open-weight serving. Use for: sanity-checking what actually runs on a given amount of memory before you promise a local-first feature.
- [r/MachineLearning](https://www.reddit.com/r/MachineLearning/)
  Moderated against hype. Use for: deciding whether a technique is real or marketing.

## Gaps

Where the course is honest about having no good primary source, and says so in the text rather than papering over it.

- **Semantic cache savings.** The commonly repeated claim that semantic caching removes roughly a third of an API bill has no primary source behind it. Savings are hit rate times avoided call cost, and hit rate is a property of your traffic. The course teaches the decomposition and tells the reader to measure on a replay of their own queries.
- **Trajectory eval methodology.** The strongest sources are vendor documentation for specific evaluation products. There is no widely accepted peer-reviewed methodology for grading agent trajectories, and no agreed answer to how strict a match should be. Treat the strictness guidance in Chapter 2 as reasoned practice, not as a result.
- **Data flywheel throughput.** No public source gives a defensible ratio from raw user complaints to reproducible labelled cases. The Chapter 2 exercise asks the reader to measure their own rather than quoting anyone's.
- **Cost kill-switch patterns for model gateways.** The enforcement pattern is borrowed from cloud cost management, which is well documented, but there is no comparable published reference for token-denominated per-tenant enforcement in an LLM gateway. The design in Chapter 4 is transferred, and the transfer is stated explicitly.
- **Local-first capability boundaries.** What a given on-device model can actually do at a given memory footprint changes faster than anything can be cited, and vendor claims are not independently verified. The course deliberately gives no capability figures.
- **Inter-agent injection in the wild.** The defensive literature is strong and growing, but there is little published incident data on real multi-agent injection attacks, because affected organisations do not publish. The threat model is sound; the base rate is unknown.
