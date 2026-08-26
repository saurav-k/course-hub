# Probability You Build - Resources

The sources this course trusts.
Everything below was opened and verified by the design reports this course was commissioned
from (`pai-w12`, `pai-w34`, `pai-w56`, August 2026); the note beside each source says what
it established. Add anything new here before citing it, and prefer a paper or vendor page
over a blog summarising one.

## The programme

- **[Probability for AI (PAI1), Stanford](https://pai.stanford.edu/)** - Chris Piech and Mehran Sahami.
  The spine: the six-week You Learn / You Build table, "comfort with algebra is all you need",
  "a public portfolio of your work", Code-in-Place teaching model. The `/team` page names the instructors.
  **Do not assert internal PAI1 specifics**: `pai.stanford.edu/apply/pai1/student/aboutCourse` is behind a sign-in wall and was never read.
- **[CS109, Stanford](https://web.stanford.edu/class/cs109/)** (and the [Winter 2025 archive](https://web.stanford.edu/class/archive/cs/cs109/cs109.1254/)).
  PAI1's ancestor; used for concept-inventory shape and problem style. Its PSet 3 includes "make your own art!", the ancestor of Week 2's garden.
- **[Probability for Computer Scientists](https://chrispiech.github.io/probabilityForComputerScientists/en/)** - Chris Piech.
  Open textbook. The [random variables chapter](https://chrispiech.github.io/probabilityForComputerScientists/en/part2/rvs/), the
  [algorithmic art example](https://chrispiech.github.io/probabilityForComputerScientists/en/examples/algorithmic_art/)
  (Pareto circles via inverse transform in JavaScript - Week 2's direct ancestor),
  the [parameter estimation](https://chrispiech.github.io/probabilityForComputerScientists/en/part5/parameter_estimation/) and
  [MLE](https://chrispiech.github.io/probabilityForComputerScientists/en/part5/mle) chapters (Bernoulli p-hat = k/n, likelihood wording),
  and the [logistic regression chapter](https://chrispiech.github.io/probabilityForComputerScientists/en/part5/log_regression)
  (assumption, log-likelihood, gradient, ascent update). Weeks 2-4 lean on these heavily.

## Weeks 1-2: decisions under uncertainty, and random variables

- **[Self-Consistency, Wang et al., arXiv:2203.11171](https://arxiv.org/abs/2203.11171)** (ICLR 2023).
  Sampling n reasoning paths and marginalising beats greedy decoding: +17.9% GSM8K over CoT baselines. Week 1's n-sample lever.
- **[FrugalGPT, Chen, Zaharia and Zou, arXiv:2305.05176](https://arxiv.org/abs/2305.05176)**.
  LLM cascades cut cost at equal quality (up to 98% cost reduction claimed); API fees differ by two orders of magnitude. Week 1's cascade lever.
- **[Snell et al., arXiv:2408.03314](https://arxiv.org/abs/2408.03314)** (2024).
  Compute-optimal test-time allocation beats uniform best-of-N (>4x efficiency claimed); effectiveness depends on prompt difficulty - which is the correlated-failure lesson wearing everyday clothes.
- **[RouteLLM, Ong et al., arXiv:2406.18665](https://arxiv.org/abs/2406.18665)**.
  Learned strong-vs-weak routing, >2x cost reduction without quality loss claimed. Week 1's routing lever.
- **[OpenAI pricing](https://platform.openai.com/docs/pricing)** and **[Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing)**.
  Sources of the frozen per-token price snapshot (dated 2026-08-26) behind the Spend Planner's catalogue. Snapshot only: label it historical, never claim current truth.
- **[Artificial Analysis model leaderboard](https://artificialanalysis.ai/models)**.
  Source of the frozen latency snapshot (TTFT and output-speed spread), same date, same labelling rule.

## Week 3: maximum likelihood instruments

- **[Morishima et al., "Discovery of a big void in Khufu's Pyramid by observation of cosmic-ray muons", Nature 552, 2017](https://www.nature.com/articles/nature24647)** ([free version, arXiv:1711.01576](https://arxiv.org/abs/1711.01576)).
  The real discovery behind Build 1: three detector technologies, counted muons, excess located by fitting against simulations with and without structures; void of minimum length 30 m. The simulation uses teaching constants for fluxes, not this paper's values.
- **[Sercombe et al., 2023 North Face Corridor paper, Nature Communications 14](https://www.nature.com/articles/s41467-023-36351-0)**.
  The clean one-sentence framing: measuring muon flux in a given direction estimates mean density along that path.
- **[Muon tomography](https://en.wikipedia.org/wiki/Muon_tomography)** - background only: sea-level flux scale (~10^4 muons/m^2/min) and transmission-radiography framing.
- **[Log-distance path loss model](https://en.wikipedia.org/wiki/Log-distance_path_loss_model)** - the phone tracker's sensor model:
  received power falls logarithmically with distance, shadowing is Gaussian in dB. Canonical textbook treatment in Rappaport, *Wireless Communications: Principles and Practice*.
- MLE localization with Gaussian ranging errors reducing to weighted least squares: standard result in the localization literature (e.g. [IEEE survey record 10599696](https://ieeexplore.ieee.org/document/10599696)).

## Week 4: logistic regression

- **[CS109 Lecture 24, Logistic Regression (archived PDF)](https://web.stanford.edu/class/archive/cs/cs109/cs109.1222/lectures/24-LogisticRegression/24-LogisticRegression.pdf)**
  and the [CS109 schedule](https://web.stanford.edu/class/cs109/schedule.html) - lecture/pset structure the week's shape follows.

## Week 5: neural networks

- **[Rumelhart, Hinton and Williams, "Learning representations by back-propagating errors", Nature 323, 1986](https://doi.org/10.1038/323533a0)**. The origin of backpropagation.
- **[Nielsen, Neural Networks and Deep Learning, chapter 2](http://neuralnetworksanddeeplearning.com/chap2.html)**. The slow-read backpropagation walkthrough; the companion to the learner's own coded backward pass.
- **[CS231n notes](https://cs231n.github.io/neural-networks-case-study/)** - softmax, numerical stability, and the code-first case-study teaching pattern.
- **[Karpathy, micrograd](https://karpathy.ai/micrograd.html)** - precedent for building autograd from scratch with zero dependencies.
- **[Hugging Face generation strategies](https://huggingface.co/docs/transformers/generation_strategies)** - temperature as the knob real stacks expose.

## Week 6: calibration and fairness

- **[Kleinberg, Mullainathan and Raghavan, arXiv:1609.05807](https://arxiv.org/abs/1609.05807)** - the impossibility trade-off, optimisation view.
  **Citation warning:** arXiv 1609.07536 is an LPV control paper, not this. Never cite 07536.
- **[Chouldechova, arXiv:1703.00056](https://arxiv.org/abs/1703.00056)** (Big Data 5(2):153-163, DOI 10.1089/big.2016.0047) - the same trade-off, statistics view.
- **[Guo, Pleiss, Sun and Weinberger, "On Calibration of Modern Neural Networks", ICML 2017, arXiv:1706.04599](https://arxiv.org/abs/1706.04599)** -
  modern nets are confidently wrong; temperature scaling fixes probabilities without moving accuracy.
- **[Hardt, Price and Srebro, "Equality of Opportunity", NeurIPS 2016, arXiv:1610.02413](https://arxiv.org/abs/1610.02413)** - equalised odds and opportunity.
- **[Pleiss et al., "On Fairness and Calibration", NeurIPS 2017, arXiv:1709.02012](https://arxiv.org/abs/1709.02012)** - calibration and within-group error rates cannot coexist.
- **[Brier 1950, Monthly Weather Review 78:1-3](https://doi.org/10.1175/1520-0493(1950)078%3C0001:VOFEIT%3E2.0.CO;2)** - the Brier score's origin.
- **[Murphy 1973, J. Applied Meteorology 12:595-600](https://doi.org/10.1175/1520-0450(1973)012%3C0595:ANVPOT%3E2.0.CO;2)** - the reliability/resolution decomposition of the Brier score.
- **DeGroot and Fienberg 1983, The Statistician 32:12-22** - calibration foundations (article paywalled; cited via the citation record).
- **Gneiting and Raftery 2007, JASA 102(477):359-378** - strictly proper scoring rules.
- **[Barocas, Hardt and Narayanan, fairmlbook.org](https://fairmlbook.org/)** - the free rigorous fairness textbook.
- **[ProPublica, "Machine Bias"](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing)** (Angwin et al., 2016) and the
  **[compas-analysis repository](https://github.com/propublica/compas-analysis)** - the primary journalism and the data behind the capstone's re-audit proposal.
- **[UCI Adult dataset](https://archive.ics.uci.edu/dataset/2/adult)** - the standard two-group evaluation set.

## Capstone

- **[UCI SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)**, Enron corpus, **[Open-Meteo](https://open-meteo.com/)** free tier,
  NOAA CSVs - the licence-friendly proposal data sources. ProPublica COMPAS above for the high-ambition audit proposal.

## Not used, and why

- **`chrishaikelly.com/probabilityforcomputerscientists`** - unreachable when the design reports were written (empty response). The live textbook lives at chrispiech.github.io, listed above.
- **Real phone-tracking datasets** - nothing public and licensable fits a 360 m teaching map; the tracker generates its own measurements from the cited path-loss model.
- **Live API calls anywhere in the builds** - rejected by mission: needs keys and money, breaks silently, and a merged pull request is a live deployment here.

## Gaps

- Platt scaling's primary chapter was never fetched; cite it by bibliographic record (title/year/venue) until someone fetches the PDF.
- PAI1's internal per-week detail is locked behind sign-in; everything attributed to PAI1 comes from the public pages only.
- The muon paper's emulsion exposure durations and count totals were never machine-read from the PDF; lessons must not state them.
- The cos-squared angular law for sea-level muons is standard folklore; cite it as a standard approximation rather than to a derivation.
