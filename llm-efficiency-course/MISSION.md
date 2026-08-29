# Mission

The record of the interview in `.claude/skills/course-authoring/new-course.md`.

## Why this course exists

The learner is an ML or platform engineer with three or more years in the job who wants frontier-class open models running on desk hardware they own: an NVIDIA DGX Spark pair, a high-memory Mac Studio, or a large-RAM workstation.

The course assumes Python, basic transformer anatomy (attention, tokens, the KV cache), and at least one encounter with a local model served through Ollama or vLLM. It does not teach transformers, and it does not teach serving infrastructure.

The cold spot is mechanism behind buzzwords. Most engineers know that quantization makes models smaller, that LoRA fine-tunes cheaply, and that speculative decoding speeds things up - as folklore. They cannot answer: why is generation limited by *memory bandwidth* and not FLOPs; what 4-bit storage actually does to a weight; why a low-rank update can steer a 320B model; and why a draft model multiplies throughput exactly on bandwidth-starved silicon. This course teaches those mechanisms by arithmetic first, then deploys them.

## The source

No single spine. The canon in `RESOURCES.md` is the source of record: the GLM-5.3-Flash model card and its vLLM serving recipe, NVIDIA's DGX Spark playbooks, and the LoRA, QLoRA, and speculative-decoding papers.

## Success looks like

The learner can:

- Compute a model's memory footprint from parameter count, quantization format, and KV-cache budget, and judge whether it fits given hardware.
- Choose a quantization format (GGUF, FP8, NVFP4) and defend the quality-size trade-off.
- Fine-tune with LoRA/QLoRA, choosing rank, target modules, and an adapter merge strategy.
- Configure speculative decoding (draft model or multi-token prediction) and predict its speedup.
- Plan a real deployment: size GLM-5.3-Flash across two DGX Sparks or one 256 GB Mac, and justify the parallelism choice.

And the failure that would still be failure with every page accurate: a recipe collection that leaves the reader unable to answer "will it fit, how fast, why is it slow" on hardware the course never mentioned.

## Structure

Thirteen lesson pages in five modules (Module 05: Apply It - the capstone worksheet and the QLoRA lab), single reading order, not routed. 900 to 1,400 prose words per page. One shape: lesson.

## The ladder

- **Foundation** (`pill easy`): `0000`, `0001` - arrive cold; every term defined here or on an earlier page.
- **Working** (`pill med`): `0002` through `0006`, `0008` - has the foundation; gets a mechanism and its trade-off directly.
- **Frontier** (`pill hard`): `0007`, `0009`, `0010`, `0011`, `0012` - has the working pages; handles live hardware case studies and a family survey.

## Constraints

- Every sizing number is derived on the page, with arithmetic shown, or linked to a fetched source. Derived figures are labelled as derivations, never presented as measurements.
- The running example hardware is desk-class: DGX Spark (128 GB unified, 273 GB/s) and Mac Studio (256 GB unified). Data-center GPUs appear only as contrast.
- GLM-5.3-Flash is the running model: 320B total, 18B active, 45 layers, 288 experts with 8 active, hybrid KDA plus sparse MLA attention, one MTP draft layer, MIT licence.

## Out of scope

- Serving infrastructure - batching, routers, observability, Kubernetes: `llm-inference-course` owns it.
- Transformer mathematics: `math-for-ml-course` and `llm-papers-course` own them.
- Cloud GPU economics and fleet capacity: `production-systems-course` owns them.
- Multi-node distributed training (DDP/FSDP): excluded entirely; this course is desk-scale.

## Siblings

- `llm-inference-course` lessons 0006 and 0007 cover speculative decoding and quantization from the serving-operator side. This course links there for serving depth and expects to be linked from there for the memory-arithmetic ground work. The honest-overlap verdict from the interview: quantization could be a chapter there, but the desk-deployment decision through-line exists nowhere in the hub.
- `llm-evolution-course` for model-lineage context; linked once, from the start-here page.

## Revisit when

- A new flagship MoE ships with a materially different active-parameter ratio.
- NVIDIA revises the Spark playbook (interconnect or memory), or the vLLM recipe adds a Spark-specific path.
- The reader gains access to the hardware: the case studies then graduate from derivations to measurements.
