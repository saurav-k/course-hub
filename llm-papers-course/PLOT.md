# Plot - the reading order of this course

This file records the true reading order of the course: where every lesson sits, and everything planned but unwritten.

The order rule, which holds for this course and every course in the hub: **a course's reading order is its true order, and a tutorial or lab session that follows a lecture sits after that lecture in the course map, never in a separate list at the bottom.**
When this file and the course `index.html` disagree, one of them is wrong, and it gets fixed before anything new is added.

Status marks used below:

- **written** - on the site today.
- **in progress** - being written right now, not yet on this branch.
- **reserved** - the position is held; nothing else may take it; nothing is written.

## The sequence

The true order here is the **difficulty rank**: primer first, then the 37 papers easiest to hardest, grouped into ten modules.
That ordering is the course's whole point, and one consequence is deliberate and worth knowing: difficulty rank is not chronology. The 2021 RoPE lesson sits in module 04 while the 2019 Multi-Query Attention lesson sits beside it, and the 2017 Transformer opens because everything else stands on it, not because it came first historically.
[`../llm-evolution-course/`](../llm-evolution-course/index.html) is the chronological telling; this course is the mechanism ladder.

| # | Position | Status | Notes |
|---|---|---|---|
| 0 | Module 00 - Foundations: `0000` Primer | written | Tokens to gradient descent. Everything later assumes it. |
| 1 | Module 01 - The Transformer Core: `0001` Attention Is All You Need through `0004` GPT-2 | written | |
| 2 | Module 02 - Scaling and Data: `0005` Scaling Laws through `0008` Chinchilla | written | |
| 3 | Module 03 - Big and Open Models: `0009` PaLM through `0012` LLaMA | written | |
| 4 | Module 04 - Attention and Position Refinements: `0013` RoPE through `0016` Grouped-Query Attention | written | |
| 5 | Module 05 - Efficient Inference and Systems: `0017` FlashAttention through `0021` Speculative Decoding | written | |
| 6 | Module 06 - Alignment and Post-Training: `0022` Self-Instruct through `0027` GRPO | written | |
| 7 | Module 07 - Parameter-Efficient Fine-Tuning: `0028` LoRA, `0029` QLoRA | written | |
| 8 | Module 08 - Reasoning, Retrieval and Agents: `0030` Chain-of-Thought through `0034` Test-Time Scaling | written | |
| 9 | Module 09 - Mixture of Experts: `0035` Switch Transformer, `0036` DeepSeekMoE | written | |
| 10 | Module 10 - Frontier Optimization: `0037` Muon Optimizer | written | |
| 11 | Module 11 - Vision, Multimodal & Generative: `0038` ViT through `0045` GraphRAG | written | Ordered by dependency, not by difficulty rank. See the note below. |

All 46 lessons are written. There are no reserved positions.

## Module 11 orders by dependency, and says so

Modules 00 to 10 are ranked easiest to hardest, and that rank is the course's whole point.
Module 11 is appended at the end of that sequence and is ordered differently inside itself: by **dependency**, not by difficulty and not by date.

The reading order is ViT, CLIP, VAE, GAN, Diffusion, Latent Diffusion, BLIP-2 and LLaVA, GraphRAG.
The dates run the other way for the first five: the VAE is from 2013 and the GAN from 2014, six and seven years before ViT, and the original diffusion paper is from 2015 while DDPM predates ViT by four months.
Nothing in the generative line depends on anything in the vision-transformer line.

The module reads the other way round for one reason.
Lesson 43, Latent Diffusion, is the payoff: one checkpoint containing a VAE, the adversarial loss that trained its decoder, a CLIP text encoder, a diffusion model and a ViT backbone.
Its conditioning cannot be explained without CLIP, and CLIP cannot be explained without ViT.
Teaching the generative line first would mean either explaining that checkpoint twice or leaving its text encoder unexplained.

Lesson 43 states this difference on the page as well, with the real dependency graph drawn beside it, so a reader is never left thinking the reading order is a causal claim.
GraphRAG sits last as a retrieval coda that depends only on lesson 0031, not on the rest of the module.

A new paper does not go at the bottom just for arriving last: it takes the next free number - numbers are identity, rank is order - and enters the map at its rank position inside the module whose material it belongs to.

## Planned but unwritten

- **A possible math refresher card in Module 0** (linear algebra, softmax), held until the primer proves too dense for readers in practice. See the open follow-up in `NOTES.md`. It would sit between the primer and Lesson 01 if built.
- Nothing else is reserved or planned.

## Adding a session to this course

1. Read `NOTES.md` for the nine-part template, then an existing lesson from the target module.
2. Take the next free lesson number. Never renumber anything.
3. Insert it at its rank position in this table, in `index.html`, and in the owning module.
4. Re-run `python3 scripts/gen_outline.py llm-papers-course`, commit the regenerated `outline.js`, run `python3 scripts/validate_site.py`, and click the pager links on both neighbours before opening the pull request.
