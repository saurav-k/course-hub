# 0209 - Information gain

**Module** M10 - lesson 10  **Rung** working  **Class** depth

## The single tight idea

The split a decision tree chooses is the one with the highest mutual information with the label,
and that criterion has a bias you can see with one column.

## Prerequisites

0200 (entropy), 0203 (mutual information, and the plug-in bias sweep this page pays off).

## Beats, in order

1. **One-minute version.** Entropy before the split, weighted entropy after, the difference is the
   gain - and the gain **is** the mutual information between the attribute and the class.
2. **Orientation figure.** 0203's mutual information as an abstract quantity into "this page: the
   same quantity as a greedy algorithm" into ID3, C4.5, CART and every gradient-boosted tree.
3. **Mental model: twenty questions.** Each split is a question and you want the one that narrows
   things most on average. Draw the tree with the entropy written at each node before any formula.
4. **Mechanism in Quinlan's own notation, on his own data.** The fourteen-row table from Table 1 of
   the 1986 paper, worked in full below.
5. **The identity, key callout, from Quinlan's footnote 3 verbatim:** "maximizing the gain is
   equivalent to minimizing `E(A)`, which is the mutual information of the attribute `A` and the
   class." The reader has now met the same number three times: as a KL in 0203, as a
   conditional-entropy reduction in 0203, and as a tree split here. **Named theorem, see proof.**
6. **The trade-off, same section, and it is a proof rather than an anecdote.** Splitting one
   attribute value into two can only increase the gain. So gain systematically prefers attributes
   with more values, and an attribute with a distinct random value per row attains the maximum gain
   with no predictive content. **Named theorem, see proof.**
7. **The fix Quinlan proposes, and how far it gets.** Split information `IV(A)` and gain ratio
   `gain(A) / IV(A)`, applied only among attributes with above-average gain. **Measured on the
   committed data it narrows the gap from 10.0x to 1.13x and still selects the identifier.** Say
   that. A course that reports the fix without measuring it teaches a false sense of safety.
8. **Gini, in one honest paragraph.** `sklearn`'s default is Gini, `1 - sum p^2`, not entropy. It
   needs no logarithm, which is why it is the default. On the committed columns the two criteria
   give the same ranking and different units. **Do not claim a general benchmark result**: this
   page has measured three columns, not the literature.

**Do not do here:** pruning, ensembles, boosting, continuous splits beyond one sentence.

## The stated proofs (D4)

**Theorem (gain is mutual information).** For an attribute `A` and a class `Y`,
`gain(A) = H(Y) - E(A) = I(A; Y)`.

*Proof, in full.* Quinlan's `E(A)` is the weighted average of the label entropy inside each branch:

```
E(A) = sum_a  P(A = a) * H(Y | A = a)
```

That is precisely the definition of the conditional entropy `H(Y | A)`. So
`gain(A) = H(Y) - H(Y | A)`, and page 0203 proved that this equals `I(A; Y)`.

**The step that does the real work** is recognising that Quinlan's branch weights `(p_i + n_i)/(p + n)`
are the empirical `P(A = a)`. Once you see that, `E(A)` is not a tree-specific quantity at all: it
is conditional entropy, and the whole splitting criterion is an information-theoretic object that
happened to be invented independently. The code file checks this to twelve decimal places on all
four of Quinlan's columns.

**Theorem (the many-valued bias).** Let `A'` be formed from `A` by splitting one of its values into
two. Then `gain(A') >= gain(A)`, with equality only when the class proportions are the same in both
halves of the split value.

*Proof, in full.* Both gains subtract from the same `H(Y)`, so the claim is `H(Y|A') <= H(Y|A)`.
Every branch of `A` is a branch of `A'` except the value `v` that was split into `v1` and `v2`. So
the two conditional entropies differ only in that one term:

```
H(Y|A)  contributes   P(v)  H(Y | A = v)
H(Y|A') contributes   P(v1) H(Y | A' = v1)  +  P(v2) H(Y | A' = v2)
```

Now `P(v) = P(v1) + P(v2)`, and the distribution of `Y` given `A = v` is the mixture of the two
child distributions with weights `P(v1)/P(v)` and `P(v2)/P(v)`. Entropy is **concave** in the
distribution, so the entropy of a mixture is at least the mixture of the entropies:

```
H(Y | A = v)  >=  (P(v1)/P(v)) H(Y|v1)  +  (P(v2)/P(v)) H(Y|v2)
```

Multiply through by `P(v)` and the right-hand side is exactly `A'`'s contribution. So
`H(Y|A') <= H(Y|A)` and `gain(A') >= gain(A)`.

**The step that does the real work** is the concavity of entropy, and it is worth telling the
reader what concavity is doing here in plain words: **splitting a group can never make you more
uncertain on average, so a criterion that rewards reduced uncertainty always rewards splitting
more finely.** The equality case is where the two children have the same class mix as the parent,
because then the mixture is not a mixture of anything different.

**The reductio, which is the practical form of the theorem.** Take the splitting to its limit: an
attribute whose value is unique to each row puts one row in each branch, every branch is pure,
`H(Y|A) = 0`, and `gain(A) = H(Y)`, the largest value any attribute can attain. The column is an
account number. It knows nothing. **Measured on the committed data:** `account_ref` has 7,559
distinct values over 12,000 rows and scores 0.5686 bits against `plan`'s 0.0568, ten times as much,
while `H(churned)` is only 0.8902.

## Planned figures

1. **Orientation, `flowchart LR`,** as beat 2.
2. **`flowchart TB`, Quinlan's tree with the entropy at every node.** Root: 14 rows, `I = 0.940`
   bits. Three children for sunny, overcast, rain at 0.971, 0.000, 0.971. Weighted average 0.694
   printed on the join. Kills "gain is the entropy of the children".
3. **`svg.chart`, the four gains as a bar chart.** outlook 0.2467, humidity 0.1518, windy 0.0481,
   temperature 0.0292, winner in `signal`.
4. **`svg.chart`, the bias.** Measured gain against the number of distinct values for a column
   independent of the label by construction, using 0203's sweep, with the honest columns marked as
   points. The identifier towers over everything real.
5. **`svg.chart`, gain against gain ratio**, four real columns as paired bars, so the reader sees
   both that the ratio helps and that it does not finish the job.

## The worked example, with its numbers

Quinlan's fourteen Saturday mornings, in full. Quoted throughout except where marked. Eight parts.

1. Fourteen days, nine of class P and five of class N.
   `I(9,5) = -(9/14)log2(9/14) - (5/14)log2(5/14) = 0.9403` bits. **The paper prints 0.940.**
2. Split on `outlook`. Sunny: 2 P, 3 N, `I = 0.971`. Overcast: 4 P, 0 N, `I = 0`. Rain: 3 P, 2 N,
   `I = 0.971`.
3. `E(outlook) = (5/14)(0.971) + (4/14)(0) + (5/14)(0.971) = 0.6935`. **The paper prints 0.694.**
4. `gain(outlook) = 0.9403 - 0.6935 = 0.2467`. **The paper prints 0.246.**
5. The other three, quoted: `humidity` 0.151, `windy` 0.048, `temperature` 0.029. ID3 picks
   `outlook`.
6. `IV(outlook) = -2(5/14)log2(5/14) - (4/14)log2(4/14) = 1.5774` bits; `IV(humidity) = 1` bit.
7. `gain ratio(outlook) = 0.2467/1.5774 = 0.1564` against `gain ratio(humidity) = 0.1518`. The
   margin collapses from 63 per cent to **3 per cent**.
8. **Sanity check.** Every gain must be non-negative and at most `I(9,5) = 0.9403`, because a split
   cannot remove more uncertainty than there was. All four clear it.

**Two places where full precision and the printed figure part company, and the page must own both.**
`gain(outlook)` computes to 0.2467 where the paper prints 0.246, because the paper subtracts its own
rounded intermediates: `0.940 - 0.694 = 0.246`. And `IV(outlook)` computes to 1.5774 where the paper
prints 1.578, which rounds the wrong way in the third decimal. Neither changes a decision the
algorithm makes. Both are worth showing once, because **a number you derived and a number you quoted
are different objects** and this course marks them differently.

**What changes if** you add an account-number column? Measured on `m10_signals.csv`: gain jumps to
0.5686 bits and the tree roots on a column that means nothing.

## Quiz seeds

- **Q1 (misconception, M7).** You add a customer-ID column to a training set and information gain
  selects it as the root. Why? **Answer: gain rises whenever an attribute is split more finely, and
  a unique-per-row attribute is the extreme case, so it attains the maximum with no predictive
  content.** Distractors: the ID leaks the label; the tree is overfitting; the entropy calculation
  is wrong.
- **Q2.** On Quinlan's table `gain(outlook) = 0.246` and `gain(temperature) = 0.029`. What does the
  difference mean? **Answer: splitting on outlook removes 0.246 bits of label uncertainty on
  average, temperature removes 0.029.** Distractors: outlook is 8.5 times more accurate; outlook
  explains 24.6 per cent of the labels; temperature is uninformative.

## Practice seed

**Stem.** Twelve rows, six of class P and six of class N. Attribute `A` is binary and splits them
`(4P,2N)` and `(2P,4N)`. Attribute `B` has six values and splits them into six pairs, each `(1P,1N)`.
(a) Compute `I(6,6)`, `gain(A)` and `gain(B)`. (b) Compute `IV(A)`, `IV(B)` and both gain ratios.
(c) Say which attribute a tree should use, and why raw gain gets this case wrong in the *opposite*
direction to the usual warning.

**Hint.** Work out `I` inside one of `B`'s branches before you compute anything else.

**Solution.** (a) `I(6,6) = 1` bit. `A`: each child has
`-(4/6)log2(4/6) - (2/6)log2(2/6) = 0.9183`, both weighted 1/2, so `E(A) = 0.9183` and
`gain(A) = 0.0817` bits. `B`: every child is `(1P,1N)` so `I = 1`, `E(B) = 1`, and
`gain(B) = 0` bits. (b) `IV(A) = 1` bit; `IV(B) = log2 6 = 2.5850` bits; gain ratios 0.0817 and 0.
(c) `A`, on both criteria. The teaching point is the shape of the counterexample: the many-valued
bias is a **tendency, not a law**. A many-valued attribute that genuinely carries no signal scores
zero on both criteria, because its branches are as impure as the parent. A student who has memorised
"gain always prefers many values" gets this wrong, which is why it is worth setting.

**`.p-check`.** `gain(B)` must be exactly 0, not merely small. If you got a positive number, check
that each of `B`'s six branches really is one P and one N: a single branch of `(2P,0N)` would make
it positive and would be a different problem.

## Code and dataset plan

`code/0209-information-gain.py`, carrying Quinlan's fourteen rows inline and loading
`m10_signals.csv` for the scale-up. Asserts every one of the paper's four gains to within 1.5e-3
and `E(outlook)` and `IV(outlook)` to their computed values; **asserts gain equals mutual
information to 1e-12 on all four columns**, which is footnote 3 verified; measures the identifier
bias at 10.0x on gain and 1.13x on gain ratio; and compares entropy with Gini on the same splits.

## Sources, primary only

- Quinlan, *Induction of Decision Trees*, Machine Learning 1 (1986): Table 1, section 4, footnote 3,
  section 7 and the `IV(A)` worked figures on page 102.
  https://link.springer.com/content/pdf/10.1007/BF00116251.pdf
- Shannon 1948 section 6, property 4, for the concavity the bias proof leans on.

## Primary source to go deeper

Quinlan 1986, sections 4 and 7. Twenty-six pages, and section 7 is the honest account of the
criterion's own weakness written by the person who proposed it.
