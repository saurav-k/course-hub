# Builder Spec - read this before writing any lesson

You are building one lesson of a 38-lesson published course on LLM research papers, for a **total beginner** who wants deep, implementation-level understanding. Match the two gold-standard lessons EXACTLY in structure, tone, CSS classes, and diagram density:

- `lessons/0000-primer-neural-nets-to-tokens.html`
- `lessons/0001-attention-is-all-you-need.html`

**Read the gold template `lessons/0001-attention-is-all-you-need.html` in full before writing.** Copy its skeleton. Only change the content.

## Hard rules
1. **No em dashes anywhere.** Use a plain `-`. (Global user rule.)
2. **Diagrams everywhere** - minimum 4 Mermaid diagrams per lesson, ideally 5-7. Use `flowchart`, `sequenceDiagram`, `stateDiagram-v2` as fits. Every diagram in a `<figure class="diagram"><div class="mermaid">...</div><figcaption>...</figcaption></figure>`. Every figcaption must explain the diagram in plain grammatical English and bold the key takeaway.
3. **Everything grammatically explainable.** Plain English BEFORE any math. Every equation goes in a `<div class="math">...<span class="gloss">plain-English reading of every symbol</span></div>`.
4. **Deep implementation.** Include at least one substantial runnable code block (PyTorch/Python/numpy) showing the paper's core mechanism. Add a `<div class="code-cap">filename.py &middot; note</div>` above each `<pre><code>`. Where relevant, show a training loop, a benchmark, or an ablation. Comment the code so a beginner can follow.
5. **Accuracy.** Ground the lesson in the ACTUAL paper. Web-search the paper (arXiv) and verify: authors, year, org, the real numbers (params, datasets, results), and the real mechanism. Do NOT invent results. If unsure of a figure, describe it qualitatively rather than fabricate.
6. Self-contained HTML. Same `<head>` as the template (link `../assets/course.css`, mermaid CDN). Same spine nav. `../assets/course.js` at end of body.

## Required section skeleton (same as gold template)
1. `.eyebrow` = `Module NN &middot; <Module Name> &middot; Lesson NN`
2. `<h1>` = lesson title. `.paper-meta` = year pill + authors + org + arXiv link.
3. `.card.tldr` = "The one-minute version", 3-5 bullets.
4. `## 1. Why this paper exists` - the problem it solves, with a diagram contrasting before/after.
5. `## 2...` mechanism, diagram-first then plain-English walkthrough. Multiple diagrams.
6. A math section using `.math` + `.gloss`.
7. Implementation section with runnable code.
8. A comparison `<table>` or ablation where it fits.
9. `## Check yourself` - a `.quiz` with 3-4 questions. **Every option in a question must be the same length** (aim for equal character count, no formatting tells). `data-answer` = correct index (0-based). Each `.q` has a `.q-fb` explanation.
10. `## How this connects` - bullet links to related lessons (use correct slugs from the map below).
11. `.teacher-note` reminding the learner to ask the agent follow-ups.
12. `#### Primary source to go deeper` - the single best paper/video/blog, real working link.
13. `.pager` with correct prev/next (slugs + titles from map).
14. `<footer>` with lesson number + glossary link.

## Quiz answer-length rule (important)
All four options in a question must be near-identical in length and grammatical shape so formatting gives no clue which is right. Rewrite options until they match.

## Tone
Warm, precise, plain. Short sentences. Explain jargon on first use (and it is in the glossary). Beginner on-ramp, then depth. Think Tufte: clean and honest.

## Full lesson map (slug, title, module)
```
00  0000-primer-neural-nets-to-tokens          Primer: From Neural Nets to Tokens             Module 00 Foundations
01  0001-attention-is-all-you-need             Attention Is All You Need                      Module 01 The Transformer Core
02  0002-bert                                  BERT                                           Module 01 The Transformer Core
03  0003-gpt-1                                 GPT-1: Generative Pre-Training                 Module 01 The Transformer Core
04  0004-gpt-2                                 GPT-2: Scaling + Zero-Shot                     Module 01 The Transformer Core
05  0005-scaling-laws                          Scaling Laws for Neural Language Models        Module 02 Scaling & Data
06  0006-gpt-3                                 GPT-3: Few-Shot Learning                       Module 02 Scaling & Data
07  0007-the-pile                              The Pile                                       Module 02 Scaling & Data
08  0008-chinchilla                            Chinchilla: Compute-Optimal Scaling            Module 02 Scaling & Data
09  0009-palm                                  PaLM                                           Module 03 Big & Open Models
10  0010-opt                                   OPT                                            Module 03 Big & Open Models
11  0011-bloom                                 BLOOM                                          Module 03 Big & Open Models
12  0012-llama                                 LLaMA                                          Module 03 Big & Open Models
13  0013-rope                                  RoPE: Rotary Position Embeddings               Module 04 Attention & Position Refinements
14  0014-alibi                                 ALiBi                                          Module 04 Attention & Position Refinements
15  0015-multi-query-attention                 Multi-Query Attention                          Module 04 Attention & Position Refinements
16  0016-grouped-query-attention               Grouped-Query Attention                        Module 04 Attention & Position Refinements
17  0017-flashattention                        FlashAttention                                 Module 05 Efficient Inference & Systems
18  0018-flashattention-2                      FlashAttention-2                               Module 05 Efficient Inference & Systems
19  0019-kv-cache-optimization                 KV Cache Compression & Optimization            Module 05 Efficient Inference & Systems
20  0020-pagedattention-vllm                   PagedAttention (vLLM)                          Module 05 Efficient Inference & Systems
21  0021-speculative-decoding                  Speculative Decoding                           Module 05 Efficient Inference & Systems
22  0022-self-instruct                         Self-Instruct                                  Module 06 Alignment & Post-Training
23  0023-instructgpt-rlhf                      InstructGPT (RLHF)                             Module 06 Alignment & Post-Training
24  0024-constitutional-ai                     Constitutional AI                              Module 06 Alignment & Post-Training
25  0025-dpo                                   Direct Preference Optimization                 Module 06 Alignment & Post-Training
26  0026-orpo                                  ORPO                                           Module 06 Alignment & Post-Training
27  0027-grpo                                  GRPO                                           Module 06 Alignment & Post-Training
28  0028-lora                                  LoRA                                           Module 07 Parameter-Efficient Fine-Tuning
29  0029-qlora                                 QLoRA                                          Module 07 Parameter-Efficient Fine-Tuning
30  0030-chain-of-thought                      Chain-of-Thought Prompting                     Module 08 Reasoning, Retrieval & Agents
31  0031-rag                                   Retrieval-Augmented Generation                 Module 08 Reasoning, Retrieval & Agents
32  0032-react                                 ReAct                                          Module 08 Reasoning, Retrieval & Agents
33  0033-tree-of-thoughts                      Tree of Thoughts                               Module 08 Reasoning, Retrieval & Agents
34  0034-test-time-scaling                     Test-Time Scaling                              Module 08 Reasoning, Retrieval & Agents
35  0035-switch-transformer-moe                Switch Transformer (MoE)                       Module 09 Mixture of Experts
36  0036-deepseekmoe                           DeepSeekMoE                                    Module 09 Mixture of Experts
37  0037-muon-optimizer                        Muon Optimizer                                 Module 10 Frontier Optimization
```

Prev/next are simply the adjacent lesson numbers in this map. Lesson 37's "next" points back to `../index.html` (Course syllabus).
