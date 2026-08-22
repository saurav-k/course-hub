# 0009 - Sequences, limits, and how to read a Big-O claim

| | |
|---|---|
| Module | M01 Foundations |
| Rung | foundation (`pill easy`) |
| Partition | **depth** - the one M01 page a reader can skip and still read the course |
| Prose budget | 1,400 to 1,600 words |
| Prerequisites | `0006` (the growth ladder needs logs and exponentials), `0008` (factorials) |
| Needed by | M05 (the derivative as a limit), M06 (schedules), M08 (convergence in probability) |
| Code | `code/0009-limits-and-reading-big-o.py` |
| Dataset | `datasets/tickets.csv` |
| Named theorems | **the p-series test**, **`(1 - 1/n)^n -> 1/e`**, and **Knuth's `O`, `Omega`, `Theta` definitions**. Proved or stated with an explicit boundary (D4). |

## Boundary

M05 owns the derivative as a limit. M08 owns convergence in probability, the law of large numbers and the CLT.
This page owns the intuition and the notation, and says so where the two nearly touch.

## The one idea

A limit says where a sequence is heading and an asymptotic bound says how fast a cost grows, and neither is a statement about any particular `n`.

## Beats, in order

1. A sequence, and convergence stated informally and honestly: the tail gets close and **stays** close. No epsilon-delta on a foundation page; say the formal version exists and where it lives.
2. Two sequences the reader already has: the loss curve, and the learning-rate schedule.
3. A series is the running total of a sequence. **The p-series test**, stated and proved. Show the partial sums as computed numbers so "diverges" is something the reader has seen rather than been told.
4. Why stochastic gradient descent needs one of each. Deep Learning Book equations 8.12 and 8.13: the steps must sum to infinity so you can still reach anywhere, and their squares must sum to something finite so the sampling noise dies. Check four schedules against the pair.
5. **`e` as a limit**: `(1 - 1/n)^n -> 1/e`, proved, which is the bootstrap's out-of-bag fraction. Breiman states "about 37%"; the `0.3679` is this course's own derivation and is labelled so.
6. Asymptotics in Knuth's own words: `O` is "order at most", `Omega` "order at least", `Theta` "order exactly".
7. The two habits that letter buys. Never use `O` for a lower bound, which is the misuse Knuth wrote to stop. And read `=` as "is in", because `O(f(n))` denotes a **set** of functions and "the equal sign here really means set inclusion". Point back at `0002`: a set statement wearing an equals sign.
8. The growth ladder, drawn: `1, log n, n, n log n, n^2, 2^n, n!`.
9. Close on what everyone gets wrong: an asymptotic bound never settles a race by itself, because it hides constants and hides which variable is growing. Self-attention is `O(n^2 d)`, a recurrent layer `O(n d^2)`, and the transformer paper says self-attention wins only "when the sequence length n is smaller than the representation dimensionality d".

## The proofs (D4)

**The p-series test.** `Sum_{k>=1} 1/k^p` converges when `p > 1` and diverges when `p <= 1`.
*Proof by grouping, for the two cases the course needs.* For `p = 1`, group the terms in blocks of length 1, 2, 4, 8 and so on. The block starting at `1/(2^m + 1)` has `2^m` terms, each at least `1/2^(m+1)`, so the block sums to at least `1/2`. Infinitely many blocks each contributing at least `1/2` cannot have a finite total, so the harmonic series diverges. For `p <= 1` every term is at least the corresponding harmonic term, so those diverge too.
For `p > 1`, group the same way from above: the block starting at `1/(2^m)^p` has `2^m` terms, each at most `1/(2^m)^p`, so the block sums to at most `2^m / 2^(mp) = (2^(1-p))^m`. Since `p > 1`, the ratio `2^(1-p)` is below 1, and a geometric series with ratio below 1 has a finite total.
**The step that does the real work** is the grouping itself: it replaces a sum nobody can evaluate with a geometric series everybody can.

**`(1 - 1/n)^n -> 1/e`.**
*Proof.* Take logarithms, which is legal because the base is positive for `n >= 2`: `ln((1 - 1/n)^n) = n ln(1 - 1/n)` by the power rule of `0006`. Write `h = 1/n`, so the right side is `ln(1 - h) / h`, and `h -> 0` as `n -> infinity`. The series `ln(1 - h) = -h - h^2/2 - h^3/3 - ...` gives `ln(1-h)/h = -1 - h/2 - h^2/3 - ...`, which tends to `-1`. So the logarithm of the expression tends to `-1`, and because `exp` is continuous the expression itself tends to `e^-1`.
**The step that does the real work** is taking the logarithm first, which turns an exponent that is itself changing into an ordinary product. That move is `0006` paying for itself.

**Knuth's definitions**, quoted rather than proved, because they are definitions: `O(f(n))` is the set of `g` for which there are positive `C` and `n0` with `abs(g(n)) <= C f(n)` for all `n >= n0`; `Omega` reverses the inequality; `Theta` is bounded on both sides. Verbally, "order at most", "order at least", "order exactly".

**Honest boundary, stated on the page.** The grouping proof is the engineering version; the integral test is the general one and needs M05. And the `e` proof leans on a series expansion of `ln(1 - h)` that this course states rather than derives. Say both plainly, so the reader knows what was shown and what was borrowed.

## Figures (5, at least one `svg.chart`)

- **F1 orientation, `flowchart LR`.** "Logs (0006), factorials (0008)" to "THIS PAGE: where a sequence heads and how fast a cost grows" to "the derivative as a limit (M05), the CLT (M08)".
- **F2 inline `svg.chart`.** Partial sums of `Sum 1/k` and `Sum 1/k^2` on shared axes with a `ref` line at `pi^2/6 = 1.6449`. One curve flattens onto the line, the other keeps climbing. Kills: "the terms go to zero, so it converges".
- **F3 inline `svg.chart`.** The growth ladder on a log-y axis.
- **F4 inline `svg.chart`.** Self-attention `n^2 d` and recurrent `n d^2` against sequence length `n` with `d` pinned at 512, crossing at `n = 512`, the crossing annotated. Kills: "`O(n^2)` is worse than `O(n)`".
- **F5 `flowchart LR`.** `Theta(f)` drawn inside `O(f)` and inside `Omega(f)` as nested boxes of functions, with the `=` on an edge labelled "read this as *is in*". Pays `0002` back.

## Worked example (eight parts)

**(a) Which learning-rate schedules can converge?** Against equations 8.12 and 8.13:

| Schedule | `Sum eps_k` | `Sum eps_k^2` | Verdict |
|---|---|---|---|
| `1/k` | diverges | converges to `pi^2/6` | both hold |
| `1/sqrt(k)` | diverges | diverges | fails the second: the noise never dies |
| `1/k^2` | converges | converges | fails the first: the steps run out before you arrive |
| constant | diverges | diverges | fails the second |

**(b) How much does a bootstrap sample leave out?** `(1 - 1/n)^n` is `0.3487` at `n = 10`, `0.3660` at 100, `0.3677` at 1,000 and `0.3679` at 10,000, against the limit `1/e = 0.36788`. Breiman's "about 37%" is a limit that has already arrived by `n = 100`.

**(c) When is `O(n^2 d)` cheaper than `O(n d^2)`?** They are equal when `n = d`. The transformer's base model has `d_model = 512`, so below 512 tokens self-attention is the cheaper of the two and above it is not; at `n = 1024` it costs exactly twice as much.

- **Sanity check.** `(1 - 1/n)^n` must stay below `1/e` and rise towards it, which the table shows.
- **What changes if** the schedule is `1/k^2`: the squares still converge but now the steps do too, so the run stalls short of the optimum.

## Code

`code/0009-limits-and-reading-big-o.py`.
Three checks against `tickets.csv` and pure arithmetic.
It computes partial sums for `p = 0, 0.5, 0.75, 1, 2` and **classifies each schedule against both conditions**, reporting that both hold exactly when `0.5 < p <= 1`.
It draws 200 bootstrap resamples of the 9,000 tickets and reports the mean left-out fraction against `1/e`, which is the limit checked by simulation rather than asserted.
And it evaluates `n^2 d` against `n d^2` across a range of `n` with `d = 512`, asserting the crossover is exactly at `n = 512`.

## Quizzes

- **Q1** (misconception): a reviewer rejects a sort "because its running time is `O(n^2)`". What is wrong with the sentence?
  `O gives an upper bound, not a lower` / `O(n^2) is faster than O(n log n)` / `O should have been written Theta` / `Sorting cannot be worse than O(n)`
  Feedback: option 3 is closer than it looks and still wrong, since `Theta` would make the sentence valid but is not what was written, and the defect is the **direction** of the bound rather than its tightness; options 2 and 4 are false. This is the exact sentence Knuth wrote his 1976 letter to stop.
- **Q2** (misconception): both `1/k` and `1/k^2` have terms going to zero. Which sum converges?
  `Both, since the terms vanish` / `Neither, both keep on growing` / `Only the sum of 1/k squared` / `Only the sum of 1/k itself`
  Feedback: option 1 is the misconception, and terms going to zero is necessary and nowhere near sufficient; option 2 is false, one of them settles at `pi^2/6`; option 4 has it backwards, and the harmonic series is the standard counterexample.

## Practice

(a) For `eps_k = C / k^p`, for which `p` do both of the Deep Learning Book's conditions hold? Check `p = 0, 0.5, 0.75, 1`.
(b) A brute-force nearest-neighbour search is `O[D N^2]` and a tree is `O[D N log N]`. With `N = 1,000,000`, roughly how many times fewer distance calculations? Does the base of the log change your answer?
(c) At what sequence length does a self-attention layer cost four times a recurrent layer, with `d = 512`?

- **Hint.** For (a), apply the p-series test twice: once to `eps_k` and once to `eps_k^2`, whose exponent is `2p`.
- **Solution.** (a) `Sum 1/k^p` diverges exactly when `p <= 1`, and `Sum 1/k^(2p)` converges exactly when `2p > 1`. Both hold precisely when `0.5 < p <= 1`, so `p = 0.75` and `p = 1` pass while a constant rate and `1/sqrt(k)` fail the second. (b) the ratio is `N / log N`, about `7.2e4` with natural logs and `5.0e4` with base 2. The base changes the number and not the **class**, because `log_b N = ln N / ln b` differs by a constant factor and a constant factor is exactly what `O` discards, which is `0006`'s change-of-base rule reappearing here. Note the honest caveat: scikit-learn reports the tree "becomes inefficient as D grows very large". (c) `n^2 d = 4 n d^2` gives `n = 4d = 2,048`.
- **`.p-check`.** In (a), the two conditions must pull in opposite directions: if your answer admits a constant learning rate, you have only checked one of them.

## Primary sources to go deeper

Knuth, *Big Omicron and Big Omega and Big Theta*, SIGACT News, April-June 1976.
Vaswani et al., *Attention Is All You Need*, Table 1 and section 4.
