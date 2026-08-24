# Mission

## Why this course exists

The hub can explain why paged attention and speculative decoding work; it could not show you how to run them.
This course is the hands-on counterpart to [`llm-papers-course`](../llm-papers-course/index.html): that course is the theory, this one is the practice of serving large language models fast and cheap at scale.

Every lesson is a lab with a goal you can measure: stand up a serving engine, tune batching, quantize deliberately, route by cost, load test to the knee, and read the unit economics that decide whether a product survives its inference bill.

## Who it is for

An engineer comfortable with a terminal, Docker, Python, and basic cloud.
No prior inference experience is assumed - Lesson 0 builds the prefill/decode mental model everything else rests on - but this is not a spectator course; most labs want either a laptop or a single cloud GPU.

## Success looks like

After working through the labs you can:

- Explain prefill against decode, TTFT against TPOT, and memory-bound against compute-bound, and say which one your workload is hitting.
- Serve a model with vLLM or SGLang, and say when each beats the other.
- Tune continuous batching and admission control for a latency-versus-throughput target.
- Quantize weights, KV cache, or activations deliberately rather than by copy-paste.
- Route requests across models by cost, latency, and quality, and cap tokens per request and per user.
- Load test past a thousand concurrent requests, find the knee, and read the curve honestly.
- Compute cost per token, per request, and per user, and say where the margin dies.
- Benchmark an optimisation honestly and publish the numbers.

## Constraints

- **Hands-on.** Every lesson carries a lab you actually run: commands, code, a benchmark, and a checklist. A lesson with nothing to measure does not belong here.
- **Mechanism before the lab.** The diagram explains why the lab shows what it shows.
- **Numbers are measured, not asserted**, and they are labelled as hardware-dependent. A benchmark result from one machine is an example, not a law.
- Every lesson ends with a primary source to go deeper.

## Out of scope

- Training and fine-tuning models. This course starts where training ends.
- Paper-level derivations. [`llm-papers-course`](../llm-papers-course/index.html) owns the maths behind every mechanism used here.
- Managed-vendor marketing. Comparing serving engines is in scope; comparing procurement contracts is not.
- Front-end work beyond calling the served API.

## Structure

Sixteen lessons in seven modules, read top to bottom:

| Module | Lessons | What it covers |
|---|---|---|
| 00 Inference Foundations | 0000-0001 | The mental model, then local testing with Ollama, LM Studio, LiteLLM |
| 01 High-Throughput Serving Engines | 0002-0006 | vLLM, SGLang, continuous batching, KV eviction, speculative decoding |
| 02 Quantization | 0007 | INT4/FP8/AWQ/GPTQ trade-offs |
| 03 Routing and Budgeting | 0008-0009 | Model routers, token budgets per request |
| 04 Edge and Deployment Targets | 0010 | TensorRT-LLM, ONNX Runtime, WebLLM |
| 05 Scale and Operations | 0011-0013 | Kubernetes, observability, load testing |
| 06 Economics and Craft | 0014-0015 | Unit economics, then the capstone benchmark |

[`PLOT.md`](PLOT.md) records the reading order and the state of every position.

There is no `BUILDER-SPEC.md` here by decision: the house standard plus the hub design system carry everything this course needs. If this course ever grows rules of its own, write the spec then rather than guessing at one now.
