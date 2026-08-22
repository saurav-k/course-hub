# Resources

The sources this course trusts.

**The rule that governs this file.** Every technical claim on a page carries a link to a primary source that the author of that page fetched and read while writing it. Listing a book here is not a substitute for opening it. A writer who cannot get to a source does not cite it: the claim goes under `## Gaps` below instead of into a page with a hedge.

Prefer a textbook or a primary paper over a blog summarising one.

## Status of this list

This is the **canon the scaffold inherits**, carried over from `statistical-foundations-ml-course/RESOURCES.md` for the probability and statistics half, plus the standard references for the linear algebra, calculus, optimization and information theory half that no source in this hub previously covered.

**Nothing in this list has been re-fetched by the scaffold.** It is a reading list, not a set of verified citations. Each writer verifies the specific source they cite, on the page they cite it.

## Probability and statistics

Inherited canon, prescribed by the lecture course this syllabus partly follows.

- **A First Course in Probability** - Sheldon Ross. The standard first course with a large exercise set. Combinatorics, axioms, random variables, expectation, limit theorems.
- **Probability, Random Variables and Stochastic Processes** - Papoulis and Pillai. The engineer's reference; reach for it when a result is needed rather than a course.
- **Probability with Engineering Applications** - Bruce Hajek, University of Illinois. Freely available as a PDF, which makes it the easiest of these to check a statement against.
- **Probability and Random Processes** - Grimmett and Stirzaker. More rigorous than Ross.
- **One Thousand Exercises in Probability** - Grimmett and Stirzaker. The companion problem book with solutions, and the best source of practice-problem seeds for M07 and M08.
- **Introductory Statistics** and **Probability and Statistics for Engineers and Scientists** - Ross. The applied-statistics half: estimation, intervals, testing, regression.
- **MIT OpenCourseWare RES.6-012, Introduction to Probability** - Tsitsiklis and Jaillet. Short videos, one concept each, with problem sets and solutions.
- **NIST/SEMATECH e-Handbook of Statistical Methods.** Citable, stable and government-maintained, for definitions where an authoritative wording matters more than a derivation.
- **Anscombe, "Graphs in Statistical Analysis", The American Statistician 27(1), 1973.** Four datasets, identical summary statistics, entirely different shapes. The reason M02 plots before it trusts a correlation coefficient.
- **Greenland et al., "Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations", European Journal of Epidemiology 31, 2016.** Open access. Names the specific misreadings, including the "accept the null" error M09 must teach against.
- **Wasserstein and Lazar, "The ASA Statement on p-Values", The American Statistician 70(2), 2016.** Why a 5% threshold is a convention chosen by people rather than a fact about the world.

## Linear algebra

- **Introduction to Linear Algebra** and **Linear Algebra and Learning from Data** - Gilbert Strang. The second is written for exactly this course's purpose.
- **MIT OpenCourseWare 18.06** - Strang. The lecture series, with problem sets.
- **Introduction to Applied Linear Algebra: Vectors, Matrices, and Least Squares** - Boyd and Vandenberghe. Free PDF, and the closest match to this course's data-matrix framing.
- **Matrix Computations** - Golub and Van Loan. For conditioning, stability and the numerical facts M03 and M04 state.
- **Eckart and Young, "The approximation of one matrix by another of lower rank", Psychometrika 1(3), 1936.** The primary source for the low-rank approximation result in M04.

## Calculus and optimization

- **Mathematics for Machine Learning** - Deisenroth, Faisal and Ong. Free PDF. The matrix-calculus and vector-calculus chapters are the reference for M05.
- **Convex Optimization** - Boyd and Vandenberghe. Free PDF. Convexity, duality, KKT for M06.
- **Numerical Optimization** - Nocedal and Wright. Line search, Newton, quasi-Newton.
- **Rumelhart, Hinton and Williams, "Learning representations by back-propagating errors", Nature 323, 1986.** The primary source for backpropagation as the chain rule.
- **Kingma and Ba, "Adam: A Method for Stochastic Optimization", ICLR 2015.** The primary source for M06's adaptive-learning-rate page.
- **Robbins and Monro, "A Stochastic Approximation Method", Annals of Mathematical Statistics 22(3), 1951.** The primary source for stochastic gradient descent.

## Information theory

- **Shannon, "A Mathematical Theory of Communication", Bell System Technical Journal 27, 1948.** The primary source for entropy. M10 cites this rather than a summary of it.
- **Elements of Information Theory** - Cover and Thomas. The standard text for KL divergence, mutual information and the chain rules.
- **Information Theory, Inference, and Learning Algorithms** - David MacKay. Free PDF, and the friendliest route into the same material.
- **Kullback and Leibler, "On Information and Sufficiency", Annals of Mathematical Statistics 22(1), 1951.** The primary source for the divergence.

## Where this course hands off

- **`llm-papers-course`** for every place a result gets used: the softmax in attention, cross-entropy as the training loss, low-rank adaptation, the scaling laws.
- **`llm-evolution-course`** for when and why any of it happened.
- **`production-systems-course`** for percentiles and queueing as operational tools.

## Not used, and why

- **The EPGD-AI&DS lecture notes that seeded this syllabus.** They are a fork of a third party's work carrying no licence, and several of their figures are third-party infographics. They are a **syllabus signal and a topic checklist only**: what was covered, in what order, at what depth. No prose, no figure and no table is taken from them, and nothing in them is cited. Every claim they suggested is sourced independently from the list above.
- **Course-hub sibling pages as sources.** A cross-link to another course in this hub is navigation, never a citation. If a claim needs a source, it needs a source outside this repository.

## Gaps

Claims this course wants to make and has no citable primary source for yet.
A writer who hits one adds it here rather than hedging on the page.

- **The competitor coverage survey.** Two commercially sold data science courses were surveyed while this course was planned, and the finding that shaped `reference/interview-index.html` is that between them they carry roughly 190 topics of which about 19 are mathematics, with no linear algebra, no calculus, no optimization and no information theory at all. The sources are local exports of paywalled courses: they cannot be linked, and a reader cannot check them. **The numbers are therefore recorded here and stated on no page.** If the claim is ever wanted in public, it needs a survey of syllabuses that are openly readable.
