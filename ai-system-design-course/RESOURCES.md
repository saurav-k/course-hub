# AI System Design Resources

Curated, high-trust sources behind every claim in this course. Prefer these over blog summaries.

## Knowledge

### Model behaviour and interfaces

- [Paper: "The Curious Case of Neural Text Degeneration" - Holtzman et al.](https://arxiv.org/abs/1904.09751)
  Introduces nucleus (top-p) sampling and shows why pure likelihood maximisation produces degenerate text. Use for: temperature, top-p, and why greedy decoding is not "the safe default".
- [Paper: "Lost in the Middle: How Language Models Use Long Contexts" - Liu et al.](https://arxiv.org/abs/2307.03172)
  Evidence that accuracy drops when the relevant passage sits mid-context. Use for: context window sizing, context packing order, and why a bigger window is not a retrieval strategy.
- [Paper: "Training language models to follow instructions with human feedback" - Ouyang et al.](https://arxiv.org/abs/2203.02155)
  The InstructGPT paper. Use for: why instruction-tuned models behave differently from base models, and what alignment buys you.
- [Paper: "Siren's Song in the AI Ocean: A Survey on Hallucination" - Zhang et al.](https://arxiv.org/abs/2311.05232)
  Taxonomy of hallucination types and mitigations. Use for: naming the specific failure rather than saying "it hallucinates".
- [Docs: OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
  Constrained decoding against a JSON Schema. Use for: JSON mode, structured outputs, and the difference between "asked nicely" and "guaranteed".
- [Docs: OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
  Use for: function calling mechanics and the tool-choice contract.
- [Docs: Anthropic Tool Use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview)
  Use for: tool calling, the tool-result loop, and multi-tool orchestration.
- [Article: "Building Effective Agents" - Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
  Distinguishes workflows from agents and argues for the simplest structure that works. Use for: agents, memory, and when not to build one.
- [Paper: "LoRA: Low-Rank Adaptation of Large Language Models" - Hu et al.](https://arxiv.org/abs/2106.09685)
  Use for: fine-tuning economics and the prompting-versus-tuning decision.

### Retrieval

- [Paper: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" - Lewis et al.](https://arxiv.org/abs/2005.11401)
  The original RAG paper. Use for: the core architecture and why parametric memory alone is insufficient.
- [Paper: "Sentence-BERT" - Reimers & Gurevych](https://arxiv.org/abs/1908.10084)
  Use for: what an embedding is and why bi-encoders make search tractable.
- [Paper: "Efficient and robust approximate nearest neighbor search using HNSW" - Malkov & Yashunin](https://arxiv.org/abs/1603.09320)
  The index behind most vector databases. Use for: vector search internals and the recall-versus-latency knob.
- [Paper: "Billion-scale similarity search with GPUs" - Johnson et al. (FAISS)](https://arxiv.org/abs/1702.08734)
  Use for: quantised indexes and the memory-versus-recall trade-off at scale.
- [Paper: "ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction" - Khattab & Zaharia](https://arxiv.org/abs/2004.12832)
  Use for: reranking and late interaction as a middle ground between bi-encoders and cross-encoders.
- [Paper: "The Probabilistic Relevance Framework: BM25 and Beyond" - Robertson & Zaragoza](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf)
  Use for: keyword search, why BM25 still wins on rare terms, and what hybrid search is hybridising.
- [Paper: "Reciprocal Rank Fusion outperforms Condorcet" - Cormack et al.](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
  Use for: combining keyword and semantic result lists without tuning score scales.
- [Paper: "Precise Zero-Shot Dense Retrieval without Relevance Labels" - Gao et al. (HyDE)](https://arxiv.org/abs/2212.10496)
  Use for: query rewriting and the hypothetical-document trick.
- [Paper: "Self-RAG" - Asai et al.](https://arxiv.org/abs/2310.11511)
  Use for: retrieve-on-demand, self-critique, and missing-information detection.
- [Article: "Introducing Contextual Retrieval" - Anthropic](https://www.anthropic.com/news/contextual-retrieval)
  Use for: chunking, chunk context loss, and combining embeddings with BM25 and reranking.

### Serving, cost, and performance

- [Paper: "Efficient Memory Management for Large Language Model Serving with PagedAttention" - Kwon et al. (vLLM)](https://arxiv.org/abs/2309.06180)
  Use for: KV cache management, memory fragmentation, and why throughput collapses without it.
- [Paper: "Orca: A Distributed Serving System for Transformer-Based Generative Models" - Yu et al.](https://www.usenix.org/conference/osdi22/presentation/yu)
  Introduces continuous (iteration-level) batching. Use for: batching, queueing, and tail latency in inference.
- [Paper: "Fast Inference from Transformers via Speculative Decoding" - Leviathan et al.](https://arxiv.org/abs/2211.17192)
  Use for: draft-and-verify decoding and latency reduction without quality loss.
- [Paper: "FlashAttention" - Dao et al.](https://arxiv.org/abs/2205.14135)
  Use for: why attention is memory-bandwidth bound, and what GPU utilisation really measures.
- [Paper: "GPTQ" - Frantar et al.](https://arxiv.org/abs/2210.17323) and [Paper: "AWQ" - Lin et al.](https://arxiv.org/abs/2306.00978)
  Use for: post-training quantisation and the quality cliff.
- [Paper: "Distilling the Knowledge in a Neural Network" - Hinton et al.](https://arxiv.org/abs/1503.02531)
  Use for: distillation as a cost lever and the small-versus-large model decision.
- [Docs: Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
  Use for: prompt caching mechanics, cache hit economics, and prefix design.
- [Docs: OpenAI Batch API](https://platform.openai.com/docs/guides/batch)
  Use for: batch inference and the latency-for-cost trade.

### Evaluation

- [Paper: "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" - Zheng et al.](https://arxiv.org/abs/2306.05685)
  Use for: LLM-as-judge, its position and verbosity biases, and when human review is unavoidable.
- [Paper: "Holistic Evaluation of Language Models (HELM)" - Liang et al.](https://arxiv.org/abs/2211.09110)
  Use for: multi-metric evaluation and why a single leaderboard number misleads.
- [Paper: "RAGAS: Automated Evaluation of Retrieval Augmented Generation" - Es et al.](https://arxiv.org/abs/2309.15217)
  Use for: faithfulness, answer relevance, and context precision as measurable quantities.
- [Paper: "TruthfulQA" - Lin et al.](https://arxiv.org/abs/2109.07958)
  Use for: factual accuracy benchmarking and why scale alone does not fix truthfulness.
- [Paper: "Hidden Technical Debt in Machine Learning Systems" - Sculley et al.](https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html)
  Use for: feedback loops, drift, and why the model is the small part of the system.

### Reliability and security

- [Standard: OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
  The canonical threat list. Use for: prompt injection, data leakage, and supply-chain risk in an interview answer.
- [Paper: "Not what you've signed up for: Indirect Prompt Injection" - Greshake et al.](https://arxiv.org/abs/2302.12173)
  Use for: why retrieved content is untrusted input and how injection crosses trust boundaries.
- [Paper: "Universal and Transferable Adversarial Attacks on Aligned Language Models" - Zou et al.](https://arxiv.org/abs/2307.15043)
  Use for: jailbreak defence and why filtering alone is not a control.
- [Book: Google SRE Book](https://sre.google/sre-book/table-of-contents/)
  Use for: error budgets, handling overload, load shedding, and graceful degradation. The chapters on [Embracing Risk](https://sre.google/sre-book/embracing-risk/) and [Handling Overload](https://sre.google/sre-book/handling-overload/) transfer directly.
- [Article: "Circuit Breaker" - Martin Fowler](https://martinfowler.com/bliki/CircuitBreaker.html)
  Use for: the canonical statement of the pattern you will be asked to apply to model providers.
- [Spec: OpenTelemetry Semantic Conventions for GenAI](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
  Use for: tracing, prompt logs, and token metrics with standard attribute names.
- [Framework: NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
  Use for: governance, compliance, and audit vocabulary that senior interviewers respond to.

## Wisdom (Communities)

- [r/MachineLearning](https://www.reddit.com/r/MachineLearning/)
  Moderated against hype. Use for: sanity-checking whether a technique is real or marketing.
- [Latent Space](https://www.latent.space/)
  Practitioner interviews on production AI systems. Use for: how teams actually operate these systems.
- [MLOps Community](https://mlops.community/)
  Use for: evaluation and operations practice from people running this in production.

## Gaps

- Public, citable numbers for cost per query at a named company are rare. Treat any specific dollar figure in an interview as an assumption you state aloud, not a fact you assert.
- Permission-aware retrieval has strong vendor documentation but little peer-reviewed work. The design is sound; the literature is thin.
