# Plot - the reading order of llm-efficiency-course

This file records the true reading order of the course. When this file and the course `index.html` disagree, one of them is wrong, and it gets fixed before anything new is added.

## The sequence

| # | Position | Status | Notes |
|---|---|---|---|
| 1 | `lessons/0000-start-here.html` - Start Here | written | On-ramp: who the course is for, the hardware and model it follows, the map. |
| 2 | `lessons/0001-generation-is-a-bandwidth-problem.html` - Generation Is a Bandwidth Problem | written | The physics everything else leans on. |
| 3 | `lessons/0002-moe-total-versus-active-parameters.html` - A 320B MoE Reads Like an 18B Model | written | Active vs total parameters; why MoE changes the fit math. |
| 4 | `lessons/0003-quantization-shrinks-weights-by-spending-error.html` - Quantization Spends Rounding Error to Shrink Memory | written | The arithmetic of low-precision weights. |
| 5 | `lessons/0004-pick-the-format-gguf-fp8-nvfp4.html` - The Format Decides Where the Model Runs | written | GGUF, FP8, NVFP4 in practice; hardware gating. |
| 6 | `lessons/0005-lora-steers-a-frozen-model-with-two-small-matrices.html` - LoRA Steers a Frozen Model with Two Small Matrices | written | Low-rank adaptation mechanism and rank arithmetic. |
| 7 | `lessons/0006-qlora-fine-tunes-in-4-bit.html` - QLoRA Fine-Tunes a Model That Does Not Fit Unfrozen | written | NF4, double quantization, paged optimizers. |
| 8 | `lessons/0007-the-wider-peft-family.html` - LoRA Is One Point in a Family of Cheap Adapters | written | DoRA, IA3, prompt and prefix tuning, merging. |
| 9 | `lessons/0008-speculative-decoding-buys-bandwidth-with-compute.html` - Speculative Decoding Trades Spare Compute for Bandwidth | written | Draft-and-verify, acceptance rates, MTP. |
| 10 | `lessons/0009-case-study-glm-on-two-dgx-sparks.html` - Two DGX Sparks Run a 320B MoE at NVFP4 | written | The worked deployment: fit math, pipeline parallelism, expected rates. |
| 11 | `lessons/0010-case-study-mac-studio-256gb.html` - One 256 GB Mac Runs the Same Model Alone | written | The unified-memory route and the cluster-vs-desk verdict. |

Reference sheets read alongside and are not positions: `reference/glossary.html`.

## Planned but unwritten

All originally planned positions are now written. The course reserves open slots after 0012 for any future session; nothing is currently planned or in progress.

## Adding a session to this course

1. Read the course's authoring contract files first.
2. Take the next free lesson number. Never renumber anything.
3. Insert the new material at its true position in this file and in `index.html`, never appended to the bottom because it arrived last.
4. Re-run `python3 scripts/gen_outline.py llm-efficiency-course`, commit the regenerated `outline.js`, run `python3 scripts/validate_site.py`, and open the changed pages in both themes before opening the pull request.
