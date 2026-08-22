# Builder spec - Mathematics for Machine Learning and Data Science

The **course delta**: what is true of this course and not of the hub.

`.claude/skills/course-authoring/SKILL.md` is the house standard and it wins wherever this file appears to contradict it.
`MISSION.md` is canonical for scope, ladder and constraints.
Read both before this one.

Nine writing crews work from this file in parallel, so everything here is a rule that stops nine people making nine different reasonable choices.

## 1. Notation, fixed for the whole course

A reader who meets `x` as a vector on one page and a scalar on the next has been taught nothing.
`reference/notation.html` is the reader-facing version of this table; it and this table must agree.

| Object | Written | Example |
|---|---|---|
| Scalar | lower case italic | *x*, *n*, &lambda; |
| Vector | lower case **bold**, always a **column** | **x**, **w** |
| Matrix | upper case **bold** | **A**, **X**, **S** |
| Set | upper case script or a named word | the set of outcomes, &Omega; |
| Random variable | upper case italic | *X* |
| A value it took | lower case italic | *x* |
| Estimate of a parameter | a hat | &theta;-hat, written `&theta;&#770;` or as `theta-hat` in plain text |
| True parameter | the bare Greek letter | &theta;, &mu;, &sigma; |
| Index over samples | *i*, running 1 to *n* | |
| Index over features | *j*, running 1 to *d* | |
| Transpose | superscript T | **A**<sup>T</sup> |
| Estimated from data | over the sample | x-bar, *s*<sup>2</sup> |
| Log | natural log unless stated | log = ln. Any other base is written explicitly, `log2`. |

**The data matrix is `X` with `n` rows and `d` columns: one row per sample, one column per feature.**
This is the single most common source of transposed confusion in a maths-for-ML course and it is settled here.
A page that genuinely needs the transpose writes `X` transpose and says why in words.

Vectors are columns, so `Xw` is the vector of predictions and `w` transpose `x` is one prediction.
Never quietly switch to row vectors to make an expression look tidier.

## 2. One meaning, one colour

The chart palette is a closed set declared in `assets/hub.css`, and in this course each colour carries one meaning on page 1 and the same meaning on page 133.

| Colour | Means, everywhere in this course |
|---|---|
| `prob` | a probability, a density, a distribution |
| `stat` | an estimate computed from data |
| `signal` | the true or target quantity |
| `noise` | error, residual, variance |
| `alarm` | the thing that bites: a tail, a divergence, a failure case |
| `gold` | a special direction or a special value: an eigenvector, an optimum, a threshold |
| `plum`, `sky` | a second and third series where the meanings above do not apply |
| `ink` | axes, grids, construction lines |

Used through the prefixes in `widgets.md`: `m-` a filled mark, `s-` a stroked line, `f-` a translucent region, `t-` coloured text, `sw-` a legend swatch.
**Never a literal hex.** It looks right in one theme, vanishes in the other, and cannot follow the print stylesheet.

## 3. Figures

The house floor is 3 diagrams and 2 kinds. This course adds one bar and it is the one that makes it a mathematics course:

**At least one hand-authored `svg.chart` on every content page.** `check_pages.py` fails the page without it.

Mermaid cannot draw a distribution, a density, a vector, a unit ball, a contour or a scatter plot, and those are the figures this subject is made of.
A page whose only figures are flowcharts has drawn the filing system rather than the mathematics.

Pick the kind by what the reader is confused about:

| Confusion | Widget |
|---|---|
| What it *looks like*: vectors, projections, unit balls, eigenvectors, contours | inline `svg.chart` |
| Distribution shape: PMF, PDF, CDF, a tail, a band, a sampling distribution | inline `svg.chart` |
| The algebra itself | `.math` + `.gloss`, then `ol.worked`. Not a diagram. |
| What feeds what in a derivation | `flowchart` |
| What happens in what order: forward then backward, propose-accept-reject | `sequenceDiagram` |
| What state a thing is in. **A Markov chain is this.** | `stateDiagram-v2` |
| Two-axis comparison: bias against variance | `quadrantChart`, labels under 26 characters |
| How the field is organised | `mindmap` |
| When things happened | `timeline`, at most six columns |

**Every page's orientation figure is that page's own slice of the course prerequisite graph**: three to five nodes, what it needs, this page, what it enables.
That satisfies the house orientation bar by construction and nobody has to invent one.

### Chart archetypes

Reuse these rather than inventing shapes. The first thirteen are proven in the hub already; the rest are this course's own.

Venn of overlapping sets. Bell curve with a shaded band. Horizontal confidence-interval bars. Balance beam for the mean as centre of mass. PMF bars with a shaded tail. Bar chart with reference lines. Number line magnified twice. Density with the area split. Density with a shaded tail beside a limit. A curve falling and flattening. Paired scatter plots. A diverging scale with markers. A four-stage funnel.

New here: arrows from an origin on a 2-D grid; a grid deformed by a matrix, before and after; a dropped perpendicular for a projection; nested unit balls for L1, L2 and L-infinity; contour ellipses with a descent path; a tangent line then a tangent parabola; a small-multiples row of three or four panels inside one `<figure>` for the CLT; contour ellipses with eigenvector axes drawn on; a curve with the area under it swept.

## 4. The worked example, in eight parts

Every content page owes at least one, and it has all eight:

1. **A concrete named setting with small numbers.** A 2x2 or 3x3 matrix, at most ten data points, two or three outcomes. Small enough that the reader can check it by hand; an example they cannot verify is a demonstration.
2. **The symbolic statement first**, in `<div class="math">` with a `<span class="gloss">` naming **every** symbol in words. No exceptions.
3. **The picture before the algebra.** No formula appears before a figure that shows what it means.
4. **`<ol class="worked">`, one arithmetic step per `<li>`,** each opening with a bolded imperative, running numbers shown and never skipped.
5. **`<span class="keynum">` only for a number quoted from a source.** A number derived here is plain, with its arithmetic visible.
6. **A sanity check**, one sentence: what the answer should roughly be and why.
7. **A "what changes if" line.** One perturbation of the input and its effect.
8. **The interpretation in words.** What the number means in the machine learning setting it came from.

## 5. Proofs

**Every named theorem gets a stated proof.** Naming a theorem and asserting its result is an incomplete page.

The proof is written to be read, not to be rigorous for its own sake:

- Name what is assumed, in words, before any symbol.
- Give the shape of the argument in two or three sentences before the steps.
- **Mark the step that does the real work.** Most proofs have one; the rest is bookkeeping. Say which is which.
- Where a full proof is genuinely beyond this course - the CLT in full generality, the spectral theorem for the infinite-dimensional case - **say so plainly, prove the case the course needs, and name what the general case adds.** An honest boundary teaches more than a hand-wave.
- A proof goes after the mental model and the picture, never before.

## 6. Code and datasets

**Every theorem or named result ships with a runnable program.**

### Layout

```
math-for-ml-course/
  code/NNNN-slug.py            one program per lesson, same stem as the lesson
  datasets/<name>.csv          the generated data, committed
  datasets/generate/make_<name>.py   the seeded generator
  datasets/README.md           repository-facing, never linked from a page
  reference/datasets.html      reader-facing index, this is what pages link
```

`lessons/0042-the-spectral-theorem.html` pairs with `code/0042-the-spectral-theorem.py`.
Same number, same stem, no exceptions: a reader who has the lesson number can guess the file.

### What a program must be

- **Self-contained plain Python needing only `numpy` and `pandas`.** No scikit-learn, no scipy, no plotting. The point is that the reader sees the arithmetic, not a library call that hides it.
- **Runs unchanged in a codebase, in Jupyter, and in Google Colab.** It loads its dataset by a relative path with a URL fallback, so pasting it into Colab works:

  ```python
  LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "sessions.csv"
  URL = "https://<hub>/math-for-ml-course/datasets/sessions.csv"
  frame = pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)
  ```

- **It computes the result twice**: once from the definition, spelled out in arithmetic, and once with the NumPy one-liner, then asserts they agree. That assertion is the teaching. A reader who only sees `np.linalg.eig` has learned an API.
- **It prints numbers a reader can compare against the page.** The page quotes what the program prints.
- **It scales.** Point it at ten times the data and it still runs. No loop over rows where a vectorised expression exists, except where the loop *is* the lesson, and then it says so in a comment.
- **A docstring saying what it demonstrates and which lesson it belongs to.**

### On the page

The program appears in the existing code widget and as a download:

```html
<div class="code-cap">code/0042-the-spectral-theorem.py &middot; NumPy and Pandas only &middot;
  <a href="../code/0042-the-spectral-theorem.py">download</a></div>
<pre><code>...</code></pre>
```

The site executes nothing. No build step, no bundler, no runtime.
If the program is longer than about forty lines, the page shows the part that carries the idea and the download carries the whole thing, and the caption says so.

### Datasets

Two exist and they are meant to serve the whole course: `sessions.csv` and `sensors.csv`.
Their teaching properties are documented in `datasets/README.md`.
**Reuse before you add.** A reader who already knows the columns can concentrate on the mathematics instead of re-reading a schema.

A new dataset is generated, seeded, byte-reproducible, under about 2 MB, and its generator's docstring says what was designed into it and why.

## 7. Quizzes and practice

House bars apply: two quizzes minimum, exactly four options, 12-character spread, `.q-fb` explaining why each wrong option is wrong.
Four additions:

1. **At least one of the two quizzes tests a misconception, not a definition.** The strongest distractor is a true statement answering a different question, and `.q-fb` says which question it answered.
2. **Never make the numerically largest or the most precise option the answer.** In a mathematics quiz that is the leak the character count does not catch.
3. **The answer index is assigned by the module owner at integration, not by the page author.** The house cap is 40% at any one index across a course. Nine authors each picking what feels right produced 56% at index 0 in the predecessor course. Page authors write the four options in any order and mark which is correct in a comment; the module owner sets `data-answer` and records the running distribution.
4. **At least one practice problem per page**, with `details.hint` before `details.solution`, and a `.p-check` sanity line closing every solution. The markup is in `widgets.md`, the floors in `pedagogy.md`.

Practice text and quiz text are not prose and do not count against the 1,800-word ceiling. `check_pages.py` excludes both.

## 8. The five ways a page breaks silently

Inherited from the hub and repeated because this course writes more diagrams than any other.
Every one of these ships green, renders wrong, and reaches no console.

1. **`<div class="mermaid">`, never `<pre class="mermaid">`.** `hub.js` appends a copy button to every `<pre>`, so a `pre` diagram gains the word `copy` as a final line of graph source and renders as a syntax error.
2. **A line break inside a Mermaid label is `&lt;br/&gt;`, never `<br/>`.** A literal `<br/>` becomes a real `BR` element, which `textContent` drops, so the first paint is right and every repaint after a mode or palette change joins the halves with no space.
3. **No semicolon in Mermaid text. Use a dash.** In a `sequenceDiagram` the free text after a colon is parsed as a statement and a semicolon there is a red error box.
4. **Always wrap Mermaid node labels in double quotes.** `A["P(X > 2000)"]` parses; `A[P(X > 2000)]` does not. Parentheses, commas and mathematics all break the parser bare, and this course is made of them.
5. **Check every page in both render states.** Defects of kind 1 are wrong on first paint; defects of kind 2 are wrong only after a repaint. Toggle mode or palette. **Counting SVGs proves nothing** - a Mermaid error box is itself an `<svg>`. Look at the figures, and match `.error-icon` when checking by machine.

A sixth, specific to `.math`: a `<br/>` inside a `.math` block is an ordinary line break and is correct there. The entity rule applies only inside `.mermaid`.

## 9. Sources

Every technical claim carries a link to a primary source fetched and read while writing the page.
The canon is in `RESOURCES.md`.

The lecture notes that seeded this course's syllabus are a **topic checklist only**: no prose, no figure and no table is lifted from them, and nothing in them is citable. Where they are the only place a claim appears, it goes in `RESOURCES.md` under `## Gaps` rather than into a page with a hedge.

A number derived here shows its arithmetic and names its assumptions, so a reader can tell a derivation from a measurement.
