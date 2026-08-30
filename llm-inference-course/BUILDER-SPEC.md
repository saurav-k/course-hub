# Builder Spec - Inference Optimization course

You are building one hands-on LAB lesson of a 16-lesson published course on production LLM inference/serving, for an engineer who knows Python + a terminal but is new to serving at scale. Match the gold template EXACTLY in structure, CSS classes, and diagram density:

- Gold template: `lessons/0000-inference-101.html` (READ IT FULLY FIRST, copy the skeleton).

This course links TWO stylesheets, in this order: the shared design system `../../assets/hub.css`, then the course-local `../assets/course-extras.css`. Use the lab components, all of which live in the extras file: `.lab` (with `.goal` label + `<h3 class="h-label">` title), `.term` (terminal blocks with `.p` prompt / `.c` comment / `.o` output spans), `.metric-grid`/`.metric` (k/v/u), `.checklist`. Everything else, `.pill` included, comes from `hub.css`.

## Hard rules
1. No em dashes anywhere. Use `-`.
2. Diagrams everywhere - min 4 Mermaid diagrams per lesson (flowchart, sequenceDiagram, stateDiagram, architecture). Each in `<figure class="diagram"><div class="fig-cap">...</div><div class="fig-claim">...</div><div class="mermaid">...</div><figcaption>...</figcaption></figure>`; the caption pair goes above the drawing, `.fig-cap` naming the subject in 2 to 5 words and `.fig-claim` stating in one sentence what the drawing proves, and the figcaption below explains it in plain English and bolds the takeaway.
3. This is a LAB course: every lesson must include at least one `.lab` box with a concrete goal, the real commands (`.term` blocks) and/or runnable code (`<pre><code>` with `.code-cap`) to run it, and a measurable outcome. Prefer real tool invocations (docker run, vllm serve, pip install, kubectl, etc.) that actually work.
4. Everything grammatically explainable. Plain English before commands/code. Any formula in `.math` + `.gloss`.
5. Accuracy: web-verify current tool usage/flags (vLLM, SGLang, TensorRT-LLM, LiteLLM, etc.) so commands are real, not invented. Note version-sensitivity where relevant.
6. End each lesson with a `.checklist` (ul.checklist) of what the learner should now be able to do.
7. Self-contained HTML: same head as gold, in this exact order, and nothing at the end of `<body>`:

   ```html
   <link rel="stylesheet" href="../../assets/hub.css">
   <link rel="stylesheet" href="../assets/course-extras.css">
   <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
   <script src="../../assets/hub.js"></script>
   <script src="../outline.js"></script>
   ```

   `hub.js` takes no `defer` and no `async`; that is what stops the flash of the wrong colours. It mounts the rail, the Appearance panel and the copy buttons at runtime, so the spine needs no theme button of its own.
8. Write a Mermaid line break as `&lt;br/&gt;` and any bold inside a label as `&lt;b&gt;`, never as a literal tag. A literal tag is parsed into a real element, and `hub.js` re-reads the graph source with `textContent` on every palette or mode change, so the break vanishes and the two halves join with no space. The page looks right until the reader touches the appearance controls. A semicolon inside a label is a statement separator; use a dash.
9. Never write a literal colour. Use the semantic tokens from `hub.css`, or a `color-mix()` of them, so all six palettes and both modes follow for free. The attribute is `data-mode`; `data-theme` is dead and fails silently.

## Section skeleton (match gold)
1. `.eyebrow` = `Module NN &middot; <Module Name> &middot; Lesson NN`
2. `<h1>` title + a `.paper-meta` one-liner describing the lab's focus (no arXiv needed; link official docs).
3. `.card.tldr` "The one-minute version", 3-5 bullets.
4. `## 1. Why this matters` with a before/after or architecture diagram.
5. Mechanism sections, diagram-first, plain English. Multiple diagrams.
6. At least one `.lab` with commands/code + expected metrics (use `.metric-grid` where numbers help).
7. A comparison `<table>` (tools/tradeoffs) where it fits.
8. `## Check yourself` `.quiz` with 3-4 questions, EQUAL-LENGTH options, `data-answer` index, `.q-fb`.
9. `## Your checklist` `ul.checklist`.
10. `.teacher-note`, then `#### Primary source` (official docs / high-quality blog, real links).
11. `.pager` prev/next (map below). `<footer>`.

## Quiz answer-length rule
All options in a question near-identical length and shape. No formatting tells.

## Lesson map (slug, title, module) - prev/next are adjacent
```
00  0000-inference-101                              Inference 101: Prefill, Decode, and the Metrics That Matter   Module 00 Inference Foundations
01  0001-local-testing-ollama-lmstudio-litellm      Local Testing: Ollama, LM Studio, LiteLLM                     Module 00 Inference Foundations
02  0002-vllm-paged-attention-serving               vLLM and PagedAttention Serving                               Module 01 High-Throughput Serving Engines
03  0003-sglang-radixattention                      SGLang and RadixAttention                                     Module 01 High-Throughput Serving Engines
04  0004-continuous-batching-queueing               Continuous Batching and Request Queue Management              Module 01 High-Throughput Serving Engines
05  0005-kv-cache-eviction-long-context             KV Cache Eviction for Long Contexts                           Module 01 High-Throughput Serving Engines
06  0006-speculative-decoding-draft-handoff         Speculative Decoding and Draft Model Handoffs                 Module 01 High-Throughput Serving Engines
07  0007-quantization-int4-fp8-awq-gptq             Quantization Tradeoffs: INT4, FP8, AWQ, GPTQ                  Module 02 Quantization
08  0008-model-router-cost-latency-quality          Build a Model Router by Cost, Latency, Quality                Module 03 Routing and Budgeting
09  0009-token-budgeting-per-request                A Token Budgeting System per User Request                     Module 03 Routing and Budgeting
10  0010-edge-onnx-tensorrt-webllm                  Edge Deployment: ONNX, TensorRT, WebLLM                       Module 04 Edge and Deployment Targets
11  0011-kubernetes-for-ai-workloads                Kubernetes for AI Workloads: HPA and Autoscaling              Module 05 Scale and Operations
12  0012-observability-latency-tokens-cost          Observability: Latency, Tokens, Errors, Costs                 Module 05 Scale and Operations
13  0013-load-testing-1000-concurrent               Load Testing 1000+ Concurrent Requests                        Module 05 Scale and Operations
14  0014-inference-unit-economics                   How Inference Costs Break Unit Economics                      Module 06 Economics and Craft
15  0015-capstone-benchmark-publicly                Capstone: Build, Benchmark, and Share an Optimized Service    Module 06 Economics and Craft
```
Lesson 15's next -> `../index.html` "Course syllabus".

## Tone
Practical, direct, senior-engineer-to-junior. Show the command, explain what it does, show the number to expect. Honest about tradeoffs and version drift.
