# Statistical Foundations of Machine Learning - Resources

The sources this course trusts.
The first section is the canon the lecture course itself prescribes, taken verbatim from slide 21 of Lecture 1.
Everything after that is a supporting source this course adds and cites from a page.

Prefer a textbook or a primary paper over a blog summarising one.

## The course canon (slide 21 of Lecture 1)

### Books

- **A First Course in Probability** - Sheldon Ross.
  The standard first course, and the one the lecture course names first. Combinatorics, axioms, random variables, expectation, limit theorems, all with a large exercise set.
  Use for: the binomial calculation on page 0003, expectation on page 0003, and the exponential distribution on page 0004. Chapter 1 covers the counting rules and the four sampling cases that Lecture 4 builds and Lecture 5 applies; chapter 4 develops the binomial and the hypergeometric as named distributions, which is where pages 0062 to 0068 point a reader who wants the next step.

- **Probability, Random Variables and Stochastic Processes** - Athanasios Papoulis and S. Unnikrishna Pillai.
  The engineer's reference. Denser than Ross, and the book to reach for when a result is needed rather than a course.
  Use for: densities, transformations, and the second-order statistics behind correlation.

- **[Probability with Engineering Applications](https://courses.grainger.illinois.edu/ece313/fa2020/probabilityAug21.pdf)** - Bruce Hajek, University of Illinois.
  Freely available as a PDF, which makes it the easiest of the four to check a statement against right now. Written for engineers, worked examples throughout.
  Use for: the Central Limit Theorem on page 0005, the law of large numbers behind page 0006, and confidence intervals.

- **Probability and Random Processes** - Geoffrey Grimmett and David Stirzaker.
  More rigorous than Ross. The book to graduate to once the first pass has landed.
  Use for: precise statements when an informal one starts to feel unsafe.

- **One Thousand Exercises in Probability** - Geoffrey Grimmett and David Stirzaker.
  The companion problem book. Exercises with solutions, which is what actually moves probability from recognised to owned.
  Use for: practice after each lecture. Reading probability does not work; solving it does.

### Online courses

- **[MIT OpenCourseWare RES.6-012, Introduction to Probability](https://ocw.mit.edu/resources/res-6-012-introduction-to-probability-spring-2018/index.htm)** - John Tsitsiklis and Patrick Jaillet, Spring 2018.
  Short videos, one concept each, with problem sets and solutions. The closest thing to this course's own teaching style in video form.
  Use for: a second explanation of anything on these pages that did not land the first time.

- **[NPTEL Probability Foundations](https://nptel.ac.in/syllabus/108106083/)** - Krishna Jagannathan, IIT Madras.
  A full Indian-syllabus probability course, aligned with what the IIT Bombay lectures assume.
  Use for: following the same syllabus at the same depth, in the same order.

## Supporting sources cited by these pages

- **[NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/)** - National Institute of Standards and Technology.
  A citable, stable, government-maintained reference for definitions of the mean, the median, the standard error, and Pearson's correlation coefficient.
  Use for: definitions where an authoritative wording matters more than a derivation.

- **[NIST e-Handbook 1.3.5.2, Confidence Limits for the Mean](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm)**.
  Use for: what a confidence interval does and does not claim, on page 0005.

- **[NIST e-Handbook 1.3.5.16, Pearson's Correlation Coefficient](https://www.itl.nist.gov/div898/handbook/eda/section3/eda35d.htm)**.
  Use for: the definition and the bounds of `r` on page 0007.

- **[Anscombe, "Graphs in Statistical Analysis", The American Statistician 27(1), 1973](https://www.sci.utah.edu/~kpotter/Library/Papers/anscombe:1973:GSA/index.html)**.
  The four datasets with identical summary statistics and entirely different shapes. The reason page 0007 insists on plotting before trusting a correlation coefficient.
  Use for: why a single number never replaces a scatter plot.

- **[Greenland et al., "Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations", European Journal of Epidemiology 31, 2016](https://link.springer.com/article/10.1007/s10654-016-0149-3)**.
  Open access. Names the specific misreadings of a confidence interval, including the overlap fallacy that page 0005 flags.
  Use for: the honest note about comparing two intervals by eye.

- **[Wasserstein and Lazar, "The ASA Statement on p-Values: Context, Process, and Purpose", The American Statistician 70(2), 2016](https://www.tandfonline.com/doi/full/10.1080/00031305.2016.1154108)**.
  The American Statistical Association's own statement. Open access.
  Use for: why a threshold like 5 percent is a convention chosen by people, not a fact about the world.

- **[Bertsekas and Tsitsiklis, "Introduction to Probability", 2nd edition, full text as a PDF](https://web.jfet.org/6.041-text/Probability.pdf)**.
  The textbook behind the MIT OCW RES.6-012 course already listed in the canon. Freely available from the authors' course materials.
  Use for: the set-theory chapter and the probability-axioms section of Lecture 2 (parts 0010 to 0015), and in particular the Section 1.2 footnote on why uncountable sample spaces cannot put a probability on every subset.

- **[NIST e-Handbook 1.3.6.2, Related Distributions - the cumulative distribution function](https://www.itl.nist.gov/div898/handbook/eda/section3/eda362.htm)**.
  The CDF stated as `Pr[X <= x]`, in both its discrete summed form and its continuous integral form, together with the survival function `S(x) = 1 - F(x)`.
  Use for: the CDF definition on Lecture 7 parts 0097 and 0101, and the survival identity the board corrected live on part 0101.

- **[NIST e-Handbook 1.3.6.6.18, The Binomial Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366i.htm)**.
  Use for: the binomial's cumulative form on Lecture 7 parts 0097 and 0098, where the poll's error probability is a binomial CDF.

- **[NIST e-Handbook 1.3.6.6.1, 1.3.6.6.2 and 1.3.6.6.7, the normal, uniform and exponential distributions](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366.htm)**.
  Use for: the three continuous densities and their CDFs on Lecture 7 parts 0105, 0106 and 0108, including the handbook's own statement that the normal CDF integral has no simple closed form and is computed numerically, and that the maximum likelihood estimator of the exponential's scale parameter is the sample mean.

- **[Wolfram MathWorld, "Multinomial Distribution"](https://mathworld.wolfram.com/MultinomialDistribution.html)**.
  A reference entry rather than a primary source, and cited for one sentence only: the multinomial is the binomial extended from two outcomes to several. Lecture 7 part 0099 names it because a student asked what happens with more than two candidates, and the lecture names it without developing it. Nothing further is built on it.

- **[MIT 6.436J Lecture 1, "Probabilistic Models and Probability Measures", Fall 2018](https://ocw.mit.edu/courses/6-436j-fundamentals-of-probability-fall-2018/c37dc8b61cdf6bde689a627bfa5b4942_MIT6_436JF18_lec01.pdf)** - Yury Polyanskiy, MIT OpenCourseWare.
  Graduate-level lecture notes, linked from Lecture 2 only to show the precise three-axiom sigma-field definition the course paraphrases.
  Use for: Definition 2, the sigma-field axioms with countable unions stated outright, on part 0013. Not a reading recommendation for this course's audience.

## Not used, and why

- **The GeeksforGeeks probability-and-statistics illustration** that slide 4 adapts.
  This course draws its own Venn diagram instead. The lecture credits the source, which is correct for a lecture; a published course reproducing a third party's figure is a licensing question this course does not need to have. The idea is not the illustration.

## Gaps

- The lecture's three case studies (the new-to-credit limit, the button A/B test, the leading-indicator search) are teaching constructions. The data is invented to make a point. Nothing in them should be cited as evidence about real fintech behaviour, and the pages say so.
- Lecture 5's two source documents are the lecturer's own: a typeset examples handout and five pages of handwritten class notes, both watermarked for personal use. Neither is reproduced anywhere on the site and neither is linkable, so pages 0058 to 0068 cite them by description rather than by link. Two marks on the handwritten notes could not be read, and both are named on the pages that would otherwise have used them.
- The correlation slide's normalising constants do not reproduce from the table printed on the slide immediately before it. Page 0007 quotes the deck and then shows the arithmetic the table itself gives. There is no source that resolves the difference, so the page names it rather than picking a side.
- Lecture 7's two source documents are six pages of class notes taken during the session and the full recording of that session. Neither is public, neither is reproduced anywhere on the site, and neither is linkable, so pages 0096 to 0109 cite them by description. Two of the three error probabilities the session quotes belong to a neighbouring sample size rather than the one written beside them; page 0098 carries both the quoted figure and this course's recomputation rather than choosing between them.
- **The lecture ties ordinary least squares to the Gaussian noise assumption and does not derive it.** The claim, made at the end of Lecture 7, is that modelling the regression error as `N(0, sigma^2)` is what the usual least-squares fit "comes naturally from". It is asserted with no derivation in the session, and no source in this canon was found that states it in a form these pages could cite: the NIST process-modelling chapter develops least squares without ever tying it to normal errors. Page 0108 carries it as the lecture's own claim, marked as asserted rather than shown. **The maximum-likelihood argument that closes the gap is not in these pages and should be added with a citation when a suitable source is read**, rather than reconstructed from memory.
