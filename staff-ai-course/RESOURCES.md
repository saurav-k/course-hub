# The Staff AI Engineer - Resources

The sources this course trusts.
A page cites from here; anything new goes in here first, in the same pull request.

Every entry carries the date the source claims for itself and the date the research behind this course read it, because a claim with no date is unrefreshable and this field moves monthly.
**Read on** below means the date a research scout fetched and read the page.
The staleness column says what a future refresh should chase first.

## The canon

The small set this course keeps returning to.

| Source | Publisher, date | Read on | What rests on it | Staleness |
|---|---|---|---|---|
| [Adding Error Bars to Evals](https://arxiv.org/abs/2411.00640) | Evan Miller, arXiv:2411.00640, submitted 2024-11-01; the work was published by Anthropic | 2026-08-28 | The whole statistical half of chapter 0004: the five recommendations, n=164 giving about 3.2% standard error, clustered errors up to 3x, paired differences cutting variance about a third at r=0.5, the resampling ladder, power analysis | Very slow. Statistics does not move |
| [The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) | Simon Willison, 2025-06-16 | 2026-08-28 | Chapter 0006's organising idea: private data, untrusted content, external communication, and why any two are safe. **Practitioner writing under his own name, not peer review; attributed as such on the page** | Slow on the concept, growing on the incident list |
| [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Anthropic, Erik Schluntz and Barry Zhang, 2024-12-19 | 2026-08-28 | Chapter 0002's workflow-against-agent test and the framework warning; chapter 0001's "find the simplest solution possible" | Slow |
| [What We've Learned From A Year of Building with LLMs](https://applied-llms.org/) | Yan, Bischof, Frye, Husain, Liu and Shankar, O'Reilly Radar, 2024-06-08 | 2026-08-28 | Chapter 0001's build-against-buy rule, the pre-PMF gate and the self-hosting gate; chapter 0004's daily-data habit and the two skews; chapter 0008's team composition | Medium. The cost-halving claim is the fastest-ageing part |
| [Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml) | Martin Zinkevich, Google | 2026-08-28 | Chapter 0001's default: rules first, and the trigger for adopting a model is that your heuristic became harder to maintain than a model would be. **Predates LLMs entirely, which is why it is not selling anything** | Very slow |
| [Anthropic model deprecations](https://platform.claude.com/docs/en/docs/about-claude/model-deprecations) | Anthropic, live page | 2026-08-28 | Chapter 0007: at least 60 days' notice; the Opus 4.1 deprecate-then-retire pair; the sampling parameters that became a 400 error | **Very fast. Re-fetch on every use** |
| [OpenAI deprecations](https://developers.openai.com/api/docs/deprecations) | OpenAI, live page | 2026-08-28 | Chapter 0007: the three notice tiers, and the 2026-06-03 announcement retiring the Evals platform, Agent Builder and the reusable Prompts API on 2026-11-30 | **Very fast. Re-fetch on every use** |
| [Don't trust the number, trust the methodology](https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/) | UC Berkeley RDI - Wang, Mang, Cheung, Sen and Song, April 2026 | 2026-08-28 | Chapter 0000: eight agent benchmarks driven to near-perfect scores without solving a task, and the named exploits | Medium |
| [We have Mythos at home](https://semgrep.dev/blog/2026/we-have-mythos-at-home-glm-52-beats-claude-in-our-cyber-benchmarks/) | Semgrep - Paxton-Fear, Jaksik, Noblitt and Buchanan, 2026-06-22 | 2026-08-28 | Chapter 0000's worked example of a headline dismantled by its own author; chapter 0005's cost-per-finding figure | Fast |
| [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) | Hamel Husain, 2024-03-29 | 2026-08-28 | Chapter 0004's three levels, "remove all friction from the process of looking at data", and "don't buy fancy LLM tools" - which chapter 0007 then pairs with OpenAI retiring its own eval platform | Slow |

## Supporting sources

Cited once or twice, by chapter.

### 0000 - Reading the Claim

- [The Leaderboard Illusion](https://arxiv.org/abs/2504.20879) - Singh, Nan, Wang, D'Souza, Kapoor, Üstün, Koyejo, Deng, Longpre, Smith, Ermis, Fadaee and Hooker, arXiv:2504.20879, submitted 2025-04-29, revised 2025-05-12. Read 2026-08-28. The arena data shares, the 27 private Meta variants, and the up-to-112% relative gain. **Fast on the numbers, slow on the argument.**
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) - METR, 2025-07-10. Read 2026-08-28. **Superseded in part; never cite without the row below.**
- [An update on our uplift experiments](https://metr.org/blog/2026-02-24-uplift-update/) - METR, 2026-02-24. Read 2026-08-28. The redesign, the selection effects, the participant quote, and METR's own "our data is only very weak evidence for the size of this increase".

### 0001 - Should This Be an AI System at All

- [Musings on building a Generative AI product](https://www.linkedin.com/blog/engineering/generative-ai/musings-on-building-a-generative-ai-product) - LinkedIn, Juan Pablo Bottaro and Karthik R., 2024-04-25. Read 2026-08-28. 80% in one month and 95% in five; YAML errors from about 10% to about 0.01%; 500 conversations a day assessed by linguists; 2s of latency per 200 reasoning tokens.
- [Accelerating Large-Scale Test Migration with LLMs](https://airbnb.tech/infrastructure/accelerating-large-scale-test-migration-with-llms/) - Airbnb, Charles Covey-Brandt, 2025. Read 2026-08-28. **The page carries no machine-readable date**; the work is 2025 and the exact date should be confirmed before it is quoted anywhere new.
- [All the Hard Stuff Nobody Talks About when Building Products with LLMs](https://www.honeycomb.io/blog/hard-stuff-nobody-talks-about-llm) - Honeycomb, Phillip Carter, published 2023-05-26, modified 2024-08-26. Read 2026-08-28. The three refusals, the chained-call arithmetic, and the non-technical gates on the critical path.
- [Developing rapidly with Generative AI](https://discord.com/blog/developing-rapidly-with-generative-ai) - Discord, Shannon Phu, 2024-04-12. Read 2026-08-28. The pre-prototype requirement checklist.
- [Staff Software Engineer, Labs: Applied AI](https://job-boards.greenhouse.io/anthropic/jobs/5304425008) - Anthropic job board, live in August 2026. Read 2026-08-28. **A job posting is pulled when it is filled**; this course quotes it as a posting live in August 2026 and never as a standing fact.

### 0002 - The Shape of the System

- [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) - OpenAI, PDF, undated in the file. Read 2026-08-28. The three qualifying conditions, the gate before committing, start-expensive-then-descend, and single agent before multi-agent.
- [Agents](https://huyenchip.com/2025/01/07/agents.html) - Chip Huyen, 2025-01-07. Read 2026-08-28. The compounding-error arithmetic over ten and one hundred steps.
- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) - HumanLayer, Dex Horthy. No version date on the README. Read 2026-08-28. The 70-to-80% ceiling arc, and "own your control flow".
- [When AI Agents Go Rogue: Agent Session Smuggling in A2A Systems](https://unit42.paloaltonetworks.com/agent-session-smuggling-in-agent2agent-systems/) - Unit 42, Palo Alto Networks, Royce Lu and Jay Chen, 2025-10-31. Read 2026-08-28. Out-of-band confirmation for sensitive actions as a mitigation.

### 0003 - Where the Knowledge Comes From

- [Optimizing model accuracy](https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy) - OpenAI documentation, the written form of the DevDay talk of 2023-11-06. Read 2026-08-28. The two-axis diagnosis and the Icelandic table in which adding retrieval to a fine-tuned model **lowered** the score.
- [T2-RAGBench](https://arxiv.org/html/2604.01733v1) - Akarsu, Karaman and Mierbach, arXiv:2604.01733, April 2026. Read 2026-08-28. 23,088 questions over 7,318 mixed text-and-table financial documents; BM25 beating a strong dense model; reranking as the largest single lever.
- [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) - Anthropic, 2024-09-19. Read 2026-08-28. The 5.7% to 1.9% retrieval-failure ladder, measured as one minus recall@20. **A vendor publishing a technique that sells its own model**, flagged on the page; the baseline and the method are stated.
- [When to use Graphs in RAG (GraphRAG-Bench)](https://arxiv.org/abs/2506.05690) - Xiang, Wu, Zhang, Chen, Hong, Huang and Su, ICLR 2026, v1 2025-06-06, v3 2026-02-22. Read 2026-08-28. Basic RAG winning fact retrieval, graph methods winning complex reasoning and summarisation, and the per-query token gap.
- [Is Semantic Chunking Worth the Computational Cost?](https://aclanthology.org/2025.findings-naacl.114/) - Qu, Tu and Bao, Findings of NAACL 2025. Read 2026-08-28. A peer-reviewed negative result against a near-universal practice.
- [Do We Need Domain-Specific Embedding Models?](https://arxiv.org/abs/2409.18511) - Tang and Yang, arXiv:2409.18511, submitted 2024-09-27, revised 2025-02-18. Read 2026-08-28. MTEB rank not correlated with FinMTEB rank.
- [pgvector](https://github.com/pgvector/pgvector) - v0.8.6, live. Read 2026-08-28. The capability surface a Postgres-only answer actually has.
- [pgvector vs Qdrant](https://www.tigerdata.com/blog/pgvector-vs-qdrant) - Tiger Data (formerly Timescale), Sewrathan, Arye and Smitty, 2025-04-29. Read 2026-08-28. **A vendor benchmarking its own extension against a competitor**, taught as exactly that, including the columns the vendor loses.
- [An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929) - Dosovitskiy et al., arXiv:2010.11929, v1 2020-10-22. Read 2026-08-28. Patch-as-token, which is what makes an image a token budget. The per-image counts on the page are arithmetic on the patch grid, not figures either paper states.
- [Improved Baselines with Visual Instruction Tuning (LLaVA-1.5)](https://arxiv.org/abs/2310.03744) - Liu, Li, Li and Lee, arXiv:2310.03744, 2023-10-05. Read 2026-08-28. The 336-pixel encoder the 576-token figure is computed from.
- [SigLIP 2](https://arxiv.org/abs/2502.14786) - Tschannen et al., arXiv:2502.14786, 2025-02-20. Read 2026-08-28. The four model sizes. **"The current default vision tower" is the research's own reading and a claim with a shelf life**, flagged as such on the page.
- [How Ramp built an industry classification system](https://engineering.ramp.com/post/industry_classification) - Ramp engineering, 2025-01-15 from page metadata, **no author name on the page**. Read 2026-08-28. The build counter-case. Publishes relative gains and **no absolute accuracy**.

### 0004 - Proving It Works

- [Who Validates the Validators?](https://arxiv.org/abs/2404.12272) - Shankar, Zamfirescu-Pereira, Hartmann, Parameswaran and Arawjo, arXiv:2404.12272, submitted 2024-04-18, UIST. Read 2026-08-28. Criteria drift, and the finding that some criteria depend on outputs observed rather than being definable in advance.
- [Task-Specific LLM Evals that Do and Don't Work](https://eugeneyan.com/writing/evals/) - Eugene Yan, March 2024. Read 2026-08-28. Off-the-shelf metrics barely correlating with application performance; the 5 to 10% factual inconsistency floor after grounding; Voiceflow's 10-point drop on a version upgrade.
- [The AI Engineering Field Guide](https://hamel.dev/blog/posts/field-guide/) - Hamel Husain, 2025-03-24. Read 2026-08-28. The tools trap, "generic metrics are worse than useless", and error analysis as the highest-return activity.
- [Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge](https://arxiv.org/abs/2410.02736) - Ye et al., arXiv:2410.02736, submitted 2024-10-03. Read 2026-08-28. The CALM twelve biases and the robustness-rate table across six judges.
- [Reliability without Validity](https://arxiv.org/abs/2606.19544) - Norman, Rivera and Hughes, arXiv:2606.19544, 2026. Read 2026-08-28. Judges internally consistent and not correlated with human judgement. **Only the qualitative finding is used; the numeric detail was not extractable from the PDF.**
- [QueryGPT](https://www.uber.com/en-US/blog/query-gpt/) - Uber, Khune, Busch, Johnson, Chakka, Chintapalli, Nagesh, Paul and Carroll, 2024-09-19. Read 2026-08-28. Vanilla against decoupled evaluation, and non-determinism inside the eval itself.
- [AI Evals for Engineers and PMs](https://maven.com/parlance-labs/evals) - Hamel Husain and Shreya Shankar, Maven, 4,200 USD, cohorts listed for September and October 2026. Read 2026-08-28. Named as the place to go deeper rather than imitated. **Price and cohort dates go stale fast.**
- [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing) - Anthropic documentation, live. Read 2026-08-28. 50% cost reduction, most batches finishing in under an hour.

### 0005 - What It Costs

- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) - Anthropic documentation, live. Read 2026-08-28. Cache write and read multipliers, the per-model minimum cacheable length, the fact that a below-minimum prompt returns **no error**, and the usage fields that prove caching happened. **Multipliers and minimums change per model generation.**
- [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing) - live. Read 2026-08-28. The output-to-input ratio, the newer tokenizer producing about 30% more tokens for the same text, and the costs that are not tokens. **The page itself documents an introductory price becoming standard on 2026-08-31, which is how fast this row rots.**
- [OpenAI pricing](https://developers.openai.com/api/docs/pricing) and [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) - live. Read 2026-08-28. The output-to-input ratios across three vendors, and Google's context caching charged per token **and per hour of storage**.
- [NVIDIA H100 rental prices](https://getdeploying.com/gpus/nvidia-h100) - GetDeploying, an aggregator rather than a vendor, data date 2026-08-28. Read 2026-08-28. Median on-demand $3.39 per GPU-hour across 54 providers, and a 21x spread on identical silicon.

### 0006 - The Blast Radius

- [CVE-2025-32711](https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2025-32711) - NIST NVD JSON API, published 2025-06-11, modified 2026-06-17. Read 2026-08-28. CVSS 3.1 base 9.3 CRITICAL and the full vector. **The NVD web page is JavaScript-rendered and returns the homepage shell; use the REST API.**
- [Adaptive Attacks Break Defenses Against Indirect Prompt Injection Attacks on LLM Agents](https://arxiv.org/abs/2503.00061) - Zhan, Fang, Panchal and Kang, arXiv:2503.00061, 2025-02-27. Read 2026-08-28. Eight defences, all bypassed, consistently above 50% attack success.
- [Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813) - Debenedetti, Shumailov, Fan, Hayes, Carlini et al., arXiv:2503.18813, submitted 2025-03-24, revised 2025-06-24. Read 2026-08-28. CaMeL: 77% of AgentDojo tasks with provable security against 84% with no defence.
- [MCPTox](https://arxiv.org/abs/2508.14925) - arXiv:2508.14925, 2025. Read 2026-08-28. 45 real MCP servers, 353 tools, 1,312 malicious cases, 20 agents; 72.8% attack success on one model; the highest refusal rate under 3%.
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices) - Model Context Protocol, draft specification, live. Read 2026-08-28. The only normative document in the security material. **It is a draft; re-check the revision before quoting a MUST.**
- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/) - OWASP Gen AI Security Project, 2025-03-12. Read 2026-08-28. The shared risk vocabulary.
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) - OWASP Gen AI Security Project, published 2025-12-09, more than 100 industry experts. Read 2026-08-28. **The publisher page carries the date and the expert count but does not list the ten risks; the ASI titles come from two agreeing secondary write-ups and are flagged on the page.**
- [Moffatt v. Air Canada, 2024 BCCRT 149](https://decisions.civilresolutionbc.ca/crt/crtd/en/item/525448/index.do) - BC Civil Resolution Tribunal, Member Christopher C. Rivers, February 2024. Read 2026-08-28. Paragraphs 27 and 28, and the $812.02 award. **The outer page is JavaScript-rendered; the tribunal's `?iframe=true` endpoint returns the text.**
- [AI Overviews: About last week](https://blog.google/products/search/ai-overviews-update-may-2024/) - Elizabeth Reid, VP of Search, Google, 2024-05-30. Read 2026-08-28. Data voids, and the fact that every published fix is a decision about when not to answer.
- [Cursor AI's own support bot hallucinated its usage policy](https://www.theregister.com/2025/04/18/cursor_ai_support_bot_lies/) - The Register, 2025-04-18. Read 2026-08-28. **Secondary**: the co-founder's words are quoted through The Register because no first-party statement could be reached.
- [Zillow Group Q3 2021 results and the Zillow Offers wind-down](https://www.sec.gov/Archives/edgar/data/1617640/000161764021000085/q32021991.htm) - Form 8-K exhibit 99.1, SEC EDGAR, 2021-11-02. Read 2026-08-28. The $304 million write-down and Rich Barton's own explanation. **Not an LLM incident, and included deliberately as the clearest published case of its risk class.**
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai) - live. Read 2026-08-28. The span taxonomy, every span marked Development, and the README's schema-URL section reading TODO.
- [Exfiltration attacks](https://simonwillison.net/tags/exfiltration-attacks/) - Simon Willison, live archive. Read 2026-08-28. The list of products fixed at the rendering layer, and "a filter that catches 99% of attacks is effectively worthless".

### 0007 - Model Supply Is a Dependency

- [How is ChatGPT's behavior changing over time?](https://arxiv.org/abs/2307.09009) - Chen, Zaharia and Zou, arXiv:2307.09009, submitted 2023-07-18, revised 2023-10-31. Read 2026-08-28. **Cite only with the methodological caveat**: the paper drew criticism the research could not adjudicate, and the operational claim leans on the corroborating Voiceflow observation instead.
- [Linux Foundation announces the Agentic AI Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) - Linux Foundation, 2025-12-09. Read 2026-08-28. MCP from Anthropic, goose from Block, AGENTS.md from OpenAI.
- [A2A Protocol Surpasses 150 Organizations](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year) - Linux Foundation, 2026-04-09. Read 2026-08-28. v1.0, 150+ organisations, five SDK languages, named cloud integrations. **And the negative finding the page carries by omission: it names no company running it in production.**
- [A2A and MCP](https://a2a-protocol.org/latest/topics/a2a-and-mcp/) - A2A Protocol, v1.0.0, living. Read 2026-08-28. "A2A is about agents partnering on tasks, while MCP is more about agents using capabilities."
- [Model Context Protocol specification, revision 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18) - read 2026-08-28. Tool descriptions to be considered untrusted unless obtained from a trusted server. **Revision-dated; check for a newer one before quoting.**

### 0008 - Carrying the Organisation

- [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/) - Malte Ubl, 2020-07-06. Read 2026-08-28. The six functions, and the test for when writing the program beats writing the document.
- [Scaling engineering teams via writing things down: RFCs](https://blog.pragmaticengineer.com/scaling-engineering-teams-via-writing-things-down-rfcs/) - Gergely Orosz, 2018-10-03, updated 2022-09-21. Read 2026-08-28. The broadcast RFC, and that it scaled from tens of engineers to the low thousands.
- [Writing an engineering strategy](https://lethain.com/eng-strategies/) - Will Larson, 2023-02-13. Read 2026-08-28. Rumelt's diagnosis, guiding policies and coherent actions; the five-design-documents procedure; 1:1s with dissenters; the two-month impact review.
- [2016 Letter to Shareholders](https://www.sec.gov/Archives/edgar/data/1018724/000119312517120198/d373368dex991.htm) - Amazon, Form 8-K exhibit 99.1, SEC EDGAR, letter dated 2016, filed April 2017. Read 2026-08-28. Two-way doors, 70% of the information, disagree and commit including upward, and exhaustion as the default dispute-resolution mechanism.
- [Being Glue](https://noidea.dog/glue) - Tanya Reilly. **The page carries no date**; the talk was given at Lead Developer and Write/Speak/Code. Read 2026-08-28. The definition of glue work and the promotion-committee scene.
- [Staff Archetypes](https://staffeng.com/guides/staff-archetypes/) - Will Larson, StaffEng. **No date shown on the page.** Read 2026-08-28. Tech Lead, Architect, Solver and Right Hand, and "not just a role".
- [Dropbox Engineering Career Framework](https://dropbox.github.io/dbx-career-framework/ic5_staff_software_engineer.html) - Dropbox, undated. Read 2026-08-28. "Decisions optimized for the wider org" and "I design software components that are difficult to misuse". The [IC5 Staff Machine Learning Engineer](https://dropbox.github.io/dbx-career-framework/ic5_staff_machine_learning_engineer.html) page carries the quality-strategy and experiment-soundness rows.
- [Etsy Engineering Career Ladder](https://etsy.github.io/Etsy-Engineering-Career-Ladder/) - Etsy, undated. Read 2026-08-28. Loosely scoped against unscoped.
- [The Rise of the AI Engineer](https://www.latent.space/p/ai-engineer) - Shawn Wang (swyx), Latent Space, 2023-06-30. Read 2026-08-28. The naming of the role and the five-year prediction whose deadline is 2028.

## Wisdom

Where the practitioners argue, for a reader who wants to test their understanding against people who do this.

- [Simon Willison's weblog](https://simonwillison.net/) - the running record of what actually broke this month, written by someone who publishes his own corrections.
- [applied-llms.org](https://applied-llms.org/) - six named practitioners writing from their own production work. The closest thing the field has to a staff-level consensus document.
- [Hamel Husain's blog](https://hamel.dev/) - the evaluation material the rest of the field summarises.

## Not used, and why

- **Vendor comparison tables of eval, observability and vector platforms.** Almost every such comparison on the open web is published by one of the platforms being compared. The course teaches that structural bias as an exercise in chapter 0004 rather than adding one more table.
- **Role and salary data for 2026.** Two targeted searches returned only recruiter and lead-generation pages with unstated methodology. All were discarded, and the course carries no such number.
- **The $33,000 GraphRAG indexing figure** that circulates widely. It traces only to a Medium post. The primary cost evidence used instead is Microsoft's own comparison and GraphRAG-Bench's token tables.
- **`marginlab.ai`'s model degradation tracker.** Returned HTTP 403 and its method is unverified. Its Hacker News reception is evidence that this audience tracks drift; its data is not cited anywhere.
- **Published self-hosting break-even token volumes.** Every source found for them is a marketing blog with unstated assumptions. Chapter 0005 teaches the reader to derive their own from two published price tables instead.
- **Gartner's agentic inference cost prediction.** The press release returned HTTP 403 and could not be read. The 5-to-30x range is second-hand and is not asserted on any page.
- **The Hugging Face unsafe-serialization counts.** The paper's abstract confirms the study exists but does not carry the figures; those came from a search summary of a PDF that would not extract. Recorded under Gaps rather than taught.
- **RAG vs Fine-tuning: a Case Study on Agriculture (arXiv:2401.08406).** Read during the research and deliberately left out: its additive finding is a genuine counterweight to the Icelandic result in chapter 0003, and the research could not adjudicate between them within the session.

## Gaps

Claims this course would like to make and cannot source.
A gap recorded here is a gap the course does not assert on a page.

- **A named company that removed an LLM from production and replaced it with a classical model or rules.** A targeted search returned no named account. The absence is itself taught in chapter 0001: the field publishes its adoptions and not its retreats, which is a reason to weight the restraint cases that do exist more heavily than their number suggests. What would settle it: one published engineering write-up with a company name on it.
- **A survey measuring what senior engineers want from AI learning material.** None found. Everything this course assumes about its own reader is inferred from what that audience published, amplified and paid for.
- **A published engineering career ladder with AI-specific staff-level rows**, beyond Dropbox's ML ladder. None found as of the research date. That absence is a finding in chapter 0008: the discipline is being practised faster than it is being written down.
- **What it costs to retire an AI feature your own users have built habits on.** No source. A chapter was considered for it and deliberately not reserved in `PLOT.md`.
- **The decision layer for generative modalities beyond the token bill.** When a diffusion model is the right answer for a product, and what it costs to serve, is not covered here: the research behind this course reached those papers at mechanism depth only. Chapter 0003 carries the token arithmetic and the step-count framing and stops there, linking into `llm-papers-course` for everything else.
- **The exact publication date of the Airbnb test-migration post.** The page carries no machine-readable date. What would settle it: a dated first-party copy.
- **Whether AgentDojo has saturated.** One 2026 source reports near-zero attack success on the newest frontier models with no defence at all. It could not be confirmed against a primary source, so chapter 0006 states the caution rather than the claim.
- **The date and version of the OpenTelemetry GenAI conventions move.** Two secondary write-ups name 2026-06-12 and v1.42.0; no primary release note was reached. What is confirmed directly is the redirect notice, the Development status on every span, and the TODO schema URL - which is the whole teaching point anyway.
