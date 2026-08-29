# llm-efficiency-course - Resources

The sources this course trusts. A page cites from here; anything new goes in here first, in the same pull request.

## The canon

- [GLM-5.3-Flash model card (zai-org)](https://huggingface.co/zai-org/GLM-5.3-Flash) - the running model's architecture: 320B total / 18B active, 45 layers, 288 experts with 8 active, hybrid KDA + sparse MLA, MTP draft layer, MIT licence. Lean on it from `0002` onward.
- [GLM-5.3-Flash vLLM recipe](https://recipes.vllm.ai/zai-org/GLM-5.3-Flash) - serving parameters: FP8 checkpoint ~306 GiB, MTP speculative config, tool/reasoning parsers, context and concurrency figures. Leans on `0004`, `0008`, `0009`.
- [Connect Two Sparks (NVIDIA DGX Spark playbook)](https://build.nvidia.com/spark/connect-two-sparks) - the 200 GbE QSFP direct link, netplan and SSH setup. Leans on `0009`.
- [LoRA: Low-Rank Adaptation of Large Language Models (Hu et al., 2021)](https://arxiv.org/abs/2106.09685) - the low-rank update mechanism and rank arithmetic. Leans on `0005`, `0007`.
- [QLoRA: Efficient Finetuning of Quantized LLMs (Dettmers et al., 2023)](https://arxiv.org/abs/2305.14314) - NF4, double quantization, paged optimizers. Leans on `0006`.
- [Fast Inference from Transformers via Speculative Decoding (Leviathan et al., 2022)](https://arxiv.org/abs/2211.17192) - the draft-and-verify framework and the expected-tokens-per-step formula. Leans on `0008`.

## Supporting sources

### Hardware

- [NVIDIA DGX Spark](https://www.nvidia.com/en-us/products/workstations/dgx-spark/) - GB10 Grace Blackwell superchip, 128 GB unified memory, ConnectX-7. Cited by `0001`, `0009`, `0010`.
- [Serve LLMs with vLLM (DGX Spark playbook)](https://build.nvidia.com/spark/serve-llms-with-vllm) - serving stack on Spark. Cited by `0009`.
- [NCCL for Multiple Sparks (DGX Spark playbook)](https://build.nvidia.com/spark/nccl-for-multiple-sparks) - multi-node collective validation. Cited by `0009`.

### Formats and runtimes

- [llama.cpp](https://github.com/ggml-org/llama.cpp) and the GGUF format - the CPU/desktop path and its quantization catalogue. Cited by `0004`, `0010`.
- [MLX](https://github.com/ml-explore/mlx) - Apple unified-memory model framework. Cited by `0010`.

### Community quantizations

- [unsloth/GLM-5.3-Flash-GGUF](https://huggingface.co/unsloth/GLM-5.3-Flash-GGUF) and community NVFP4 checkpoints on the Hugging Face model tree - evidence that day-two quant support existed; cited by `0004` as release-velocity context, not as quality evidence.

## Wisdom

- [llama.cpp discussions](https://github.com/ggml-org/llama.cpp/discussions) - where desktop quantization quality is argued with perplexity numbers, not vibes.
- [vLLM issue tracker](https://github.com/vllm-project/vllm/issues) - where the gap between recipe and reality on new hardware surfaces first.

## Not used, and why

- Blog-perplexity shootouts of GLM-5.3-Flash quants: the model is two days old as of authoring; no benchmark has enough runs to trust. Perceived quality claims stay qualitative on the page.
- AWS/GCP serving docs: out of scope per `MISSION.md`.

## Gaps

- Measured tokens/second for GLM-5.3-Flash NVFP4 on GB10 (two Sparks or Mac Studio): no public benchmark existed at authoring time. The course derives rates from bandwidth arithmetic and labels them as derivations. What would settle it: a published `vllm bench serve` run at concurrency 6 on the hardware.
- Quality delta between FP8 and NVFP4 checkpoints of this model: no perplexity or eval suite published yet. What would settle it: an open-llm-leaderboard-style eval of both checkpoints.
