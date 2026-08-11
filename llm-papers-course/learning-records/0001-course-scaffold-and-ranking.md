# 0001 - Course scaffold and paper ranking

**Date:** 2026-07-29
**Status:** active

## Decision
Built a 38-lesson course (1 primer + 37 papers) as a publishable static HTML site under `/Users/saurav.kumar/workdir/llm-papers-course`.

## Learner profile (from Q&A)
- Total beginner to LLM internals -> Lesson 0 primer added.
- Wants DEEP implementation (runnable code, training loops, benchmarks/ablations).
- Wanted all lessons built up front (publishable), not one-at-a-time.
- Diagrams everywhere; everything grammatically explainable.

## Ranking (easiest -> hardest), grouped into 10 modules
00 Foundations (primer) | 01 Transformer Core (Attention, BERT, GPT-1, GPT-2) | 02 Scaling & Data (Scaling Laws, GPT-3, Pile, Chinchilla) | 03 Big & Open Models (PaLM, OPT, BLOOM, LLaMA) | 04 Attention & Position (RoPE, ALiBi, MQA, GQA) | 05 Efficient Inference (FlashAttn, FlashAttn-2, KV cache, PagedAttention, Speculative) | 06 Alignment (Self-Instruct, InstructGPT, Constitutional AI, DPO, ORPO, GRPO) | 07 PEFT (LoRA, QLoRA) | 08 Reasoning/Agents (CoT, RAG, ReAct, ToT, Test-Time Scaling) | 09 MoE (Switch, DeepSeekMoE) | 10 Frontier Opt (Muon).

Rationale: order follows dependency + conceptual load, not chronology. Position/attention refinements and systems papers deliberately placed AFTER the base models that motivate them. Alignment before PEFT since RLHF concepts frame why cheap fine-tuning matters. MoE and Muon last as most specialized.

## Architecture
- Shared design system `assets/course.css` + runtime `assets/course.js` (mermaid, quiz, theme, copy).
- `index.html` = ranked syllabus. `reference/glossary.html` = canonical vocab.
- Gold-standard lessons 0000 (primer) + 0001 (attention) authored by hand as the template.
- Lessons 02-37 fan-out-built by 8 parallel subagents, each cloning the gold template via `BUILDER-SPEC.md`, grounded on real arXiv facts + told to web-verify.

## Status: COMPLETE (papers course)
- All 38 lessons built and validated: 38 files, 0 em dashes, 0 HTML double-escape bugs, all close </html>, every lesson >=4 mermaid diagrams + 4 quizzes (primer 3).
- Spend-limit hit mid-build killed 7 of 8 first-wave builders; relaunched after cap cleared. Hand-built 0008/0012/0015 in-loop during the outage, then topped up their (and 0022's) diagram counts to meet the >=4 bar.

## Second course spun up: llm-inference-course/
- User asked (mid-turn) for a hands-on inference-optimization course from an 18-bullet list. Built as a sibling site: 16 lab lessons, own index/spec/glossary, shared design system + lab.css add-ons. Gold lesson 0000 by hand; 01-15 fan-out-built.

## Open follow-ups / to verify after build
- Validate inference course same way (files, em dashes, mermaid, quiz, chain).
- Final prev/next chain sweep both courses; cross-links between the two.
- Optional: a "lineage map" diagram on papers index; print/PDF pass; publish as Artifacts or host.
