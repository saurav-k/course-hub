# Resources

High-trust sources grounding this course. Each lesson also links its own primary source.

## Meta / reading guides
- Sebastian Raschka, "Understanding Large Language Models" and his paper reading lists - https://magazine.sebastianraschka.com/
- Jay Alammar, "The Illustrated Transformer" - https://jalammar.github.io/illustrated-transformer/
- Andrej Karpathy, "Neural Networks: Zero to Hero" (micrograd, makemore, GPT) - https://karpathy.ai/zero-to-hero.html
- Lil'Log (Lilian Weng) - deep explainers on attention, RLHF, agents - https://lilianweng.github.io/

## Primary papers (arXiv), by lesson
- 01 Transformer - https://arxiv.org/abs/1706.03762
- 02 BERT - https://arxiv.org/abs/1810.04805
- 03 GPT-1 - OpenAI "Improving Language Understanding by Generative Pre-Training" (2018)
- 04 GPT-2 - "Language Models are Unsupervised Multitask Learners" (2019)
- 04 GPT-2 release repository (corrects the paper's parameter counts to 124M / 355M / 774M / 1558M) - https://github.com/openai/gpt-2
- 05 Scaling Laws - https://arxiv.org/abs/2001.08361
- 06 GPT-3 - https://arxiv.org/abs/2005.14165
- 07 The Pile - https://arxiv.org/abs/2101.00027
- 08 Chinchilla - https://arxiv.org/abs/2203.15556
- 09 PaLM - https://arxiv.org/abs/2204.02311
- 10 OPT - https://arxiv.org/abs/2205.01068
- 11 BLOOM - https://arxiv.org/abs/2211.05100
- 12 LLaMA - https://arxiv.org/abs/2302.13971
- 13 RoPE - https://arxiv.org/abs/2104.09864
- 14 ALiBi - https://arxiv.org/abs/2108.12409
- 15 MQA - https://arxiv.org/abs/1911.02150
- 16 GQA - https://arxiv.org/abs/2305.13245
- 17 FlashAttention - https://arxiv.org/abs/2205.14135
- 18 FlashAttention-2 - https://arxiv.org/abs/2307.08691
- 19 KV cache: H2O https://arxiv.org/abs/2306.14048 ; StreamingLLM https://arxiv.org/abs/2309.17453 ; MLA in DeepSeek-V2 https://arxiv.org/abs/2405.04434
- 20 PagedAttention / vLLM - https://arxiv.org/abs/2309.06180
- 21 Speculative Decoding - https://arxiv.org/abs/2211.17192
- 22 Self-Instruct - https://arxiv.org/abs/2212.10560
- 23 InstructGPT - https://arxiv.org/abs/2203.02155
- 24 Constitutional AI - https://arxiv.org/abs/2212.08073
- 25 DPO - https://arxiv.org/abs/2305.18290
- 26 ORPO - https://arxiv.org/abs/2403.07691
- 27 GRPO / DeepSeekMath - https://arxiv.org/abs/2402.03300
- 28 LoRA - https://arxiv.org/abs/2106.09685
- 29 QLoRA - https://arxiv.org/abs/2305.14314
- 30 Chain-of-Thought - https://arxiv.org/abs/2201.11903
- 31 RAG - https://arxiv.org/abs/2005.11401
- 32 ReAct - https://arxiv.org/abs/2210.03629
- 33 Tree of Thoughts - https://arxiv.org/abs/2305.10601
- 34 Test-Time Scaling - https://arxiv.org/abs/2408.03314
- 35 Switch Transformer - https://arxiv.org/abs/2101.03961
- 36 DeepSeekMoE - https://arxiv.org/abs/2401.06066
- 37 Muon - Keller Jordan writeup (2024): https://kellerjordan.github.io/posts/muon/
- 38 ViT - https://arxiv.org/abs/2010.11929
- 39 CLIP - https://arxiv.org/abs/2103.00020
- 39 ARO, the bag-of-words finding - https://arxiv.org/abs/2210.01936
- 39 SigLIP - https://arxiv.org/abs/2303.15343 ; SigLIP 2 - https://arxiv.org/abs/2502.14786
- 40 VAE - https://arxiv.org/abs/1312.6114 ; VQ-VAE - https://arxiv.org/abs/1711.00937
- 41 GAN - https://arxiv.org/abs/1406.2661
- 41 Diffusion Models Beat GANs (where GANs lost) - https://arxiv.org/abs/2105.05233
- 41 Adversarial Diffusion Distillation - https://arxiv.org/abs/2311.17042 ; HiFi-GAN - https://arxiv.org/abs/2010.05646
- 42 DDPM - https://arxiv.org/abs/2006.11239 ; the 2015 original - https://arxiv.org/abs/1503.03585
- 42 Classifier-Free Guidance - https://arxiv.org/abs/2207.12598
- 42 DiT - https://arxiv.org/abs/2212.09748 ; SD3 rectified flow - https://arxiv.org/abs/2403.03206
- 43 Latent Diffusion - https://arxiv.org/abs/2112.10752 (read section 3.1, not only the abstract)
- 44 BLIP - https://arxiv.org/abs/2201.12086 ; BLIP-2 - https://arxiv.org/abs/2301.12597
- 44 LLaVA - https://arxiv.org/abs/2304.08485 ; LLaVA-1.5 - https://arxiv.org/abs/2310.03744
- 45 GraphRAG - https://arxiv.org/abs/2404.16130
- 45 GraphRAG-Bench, the independent evaluation - https://arxiv.org/abs/2506.05690
- 45 LightRAG - https://arxiv.org/abs/2410.05779
- 45 Microsoft GraphRAG documentation and repository - https://microsoft.github.io/graphrag/ and https://github.com/microsoft/graphrag
- 45 LazyGraphRAG (vendor claims about its own system) - https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/

## Gaps

Named absences in Module 11, recorded so a later refresh chases only what is missing rather than re-deriving the whole module.

- **Diffusion language model throughput.** The figures in circulation, around one to two thousand tokens per second, are all vendor-reported. No independent benchmark was found, so Lesson 42 states the direction and marks the numbers as claims.
- **A dollar cost for indexing a GraphRAG corpus.** A widely repeated figure traces only to a blog post with no primary citation. Lesson 45 leaves it out and carries the measured token counts instead.
- **A named company publishing that GraphRAG runs its production retrieval.** Not found. Lesson 45 says so rather than implying adoption.
- **Whether current vision encoders still show the bag-of-words failure.** The ARO finding stands as published; whether the newest encoders still fail that way is a separate question this course has not tested.
- **Whether GAN vocoders are still a default in text-to-speech.** The HiFi-GAN speed figures are the paper's own. The claim that it remains standard is flagged in Lesson 41 as a judgement to check, not a fact established here.

## Communities (for wisdom / testing understanding)
- r/MachineLearning and r/LocalLLaMA (Reddit)
- EleutherAI Discord (research-grade discussion)
- Hugging Face forums - https://discuss.huggingface.co/
- Papers with Code - https://paperswithcode.com/
