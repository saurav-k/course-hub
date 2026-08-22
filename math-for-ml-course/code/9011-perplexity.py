"""Perplexity: three routes to one number, and why it does not survive a retokenisation.

Lesson: Perplexity.
Dataset: m10_classifier.csv (20,000 rows), read as a next-symbol predictor.

Runs on numpy and pandas and nothing else.

What it does:
  1. Computes perplexity three ways - exp of the mean negative log-likelihood,
     the reciprocal geometric mean of the assigned probabilities, and 2 raised
     to the mean bits - and asserts all three agree.
  2. Checks the two anchors: a uniform model over V symbols has perplexity
     exactly V, and a perfect model has perplexity exactly 1.
  3. Shows that perplexity is a weighted average in the wrong space: a handful
     of near-zero probabilities dominate it, while accuracy does not notice.
  4. Retokenises the same sequence by pairing adjacent symbols, so the model's
     predictions are unchanged but the token count halves, and shows that
     per-token perplexity moves while bits per symbol does not. That is the
     comparison trap, demonstrated rather than asserted.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

RAW = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/"


def load(name: str) -> pd.DataFrame:
    local = pathlib.Path(__file__).resolve().parent.parent / "datasets" / name
    return pd.read_csv(local if local.exists() else RAW + name)


def perplexity_from_nll(nll_nats: np.ndarray) -> float:
    """exp of the mean negative log-likelihood, the definition most code uses."""
    return float(np.exp(nll_nats.mean()))


def perplexity_from_geometric_mean(probabilities: np.ndarray) -> float:
    """One over the geometric mean of the probabilities the model gave.

    Computed in log space, because the product of 20,000 numbers below one
    underflows float64 long before you finish multiplying.
    """
    return float(1.0 / np.exp(np.log(probabilities).mean()))


def main() -> None:
    clf = load("m10_classifier.csv")
    n = len(clf)
    k = 5
    logits = clf[[f"logit_{j}" for j in range(k)]].to_numpy()
    truth = clf["true_class"].to_numpy()

    peak = logits.max(axis=1, keepdims=True)
    probs = np.exp(logits - peak)
    probs /= probs.sum(axis=1, keepdims=True)
    assigned = probs[np.arange(n), truth]
    nll = -np.log(assigned)

    # ---- 1. Three routes ---------------------------------------------------
    a = perplexity_from_nll(nll)
    b = perplexity_from_geometric_mean(assigned)
    c = float(2.0 ** (nll / np.log(2.0)).mean())
    assert abs(a - b) < 1e-9 and abs(a - c) < 1e-9, "the three routes disagree"

    print(f"m10_classifier.csv read as a next-symbol predictor: {n} symbols, "
          f"{k} in the alphabet")
    print(f"\n  exp(mean NLL)                       = {a:.6f}")
    print(f"  1 / geometric mean of probabilities = {b:.6f}")
    print(f"  2 ^ (mean bits per symbol)          = {c:.6f}")
    print(f"\n  mean NLL     = {nll.mean():.4f} nats = {nll.mean() / np.log(2):.4f} bits")
    print(f"  perplexity   = {a:.4f}, so on average the model is as uncertain as")
    print(f"                 someone rolling a fair {a:.2f}-sided die.")

    # ---- 2. The anchors ----------------------------------------------------
    uniform = np.full(n, 1.0 / k)
    assert abs(perplexity_from_geometric_mean(uniform) - k) < 1e-9
    print(f"\n  a uniform model over {k} symbols has perplexity "
          f"{perplexity_from_geometric_mean(uniform):.4f}, exactly the alphabet size")
    perfect = np.full(n, 1.0)
    assert abs(perplexity_from_geometric_mean(perfect) - 1.0) < 1e-12
    print(f"  a perfect model has perplexity {perplexity_from_geometric_mean(perfect):.4f}")
    print(f"  the model here sits at {a:.4f} on that scale of 1 to {k}")

    # For scale, the number a language-model reader will recognise.
    vocab = 50257
    print(f"\n  for scale: a uniform model over a {vocab}-token vocabulary has")
    print(f"  perplexity {vocab}, cross-entropy {np.log2(vocab):.4f} bits or "
          f"{np.log(vocab):.4f} nats per token")

    # ---- 3. Where the number comes from ------------------------------------
    order = np.argsort(-nll)
    for share in (0.001, 0.01, 0.05):
        worst = order[:int(share * n)]
        print(f"\n  the worst {100 * share:.1f} per cent of symbols carry "
              f"{100 * nll[worst].sum() / nll.sum():.1f} per cent of the total loss")
    kept = np.ones(n, dtype=bool)
    kept[order[:int(0.01 * n)]] = False
    print(f"\n  drop the worst 1 per cent and perplexity falls from {a:.4f} to "
          f"{perplexity_from_nll(nll[kept]):.4f}")
    print(f"  accuracy over the same rows barely moves: "
          f"{(probs.argmax(1) == truth).mean():.4f} to "
          f"{(probs.argmax(1) == truth)[kept].mean():.4f}")
    print("  Perplexity is a geometric mean, so it is dominated by the smallest")
    print("  probabilities. Accuracy is an arithmetic mean of zeros and ones and")
    print("  cannot see the difference between a near miss and a catastrophe.")

    # ---- 4. The retokenisation trap ----------------------------------------
    # Pair adjacent symbols into one bigger token. The model's beliefs about the
    # underlying sequence do not change at all: the probability of a pair is the
    # product of the two probabilities. But there are now half as many tokens, so
    # the per-token numbers move and the per-symbol numbers do not.
    pairs = n // 2
    paired_nll = nll[:2 * pairs].reshape(pairs, 2).sum(axis=1)

    fine_ppl = perplexity_from_nll(nll[:2 * pairs])
    coarse_ppl = perplexity_from_nll(paired_nll)
    fine_bits_per_symbol = nll[:2 * pairs].mean() / np.log(2)
    coarse_bits_per_symbol = paired_nll.mean() / (2 * np.log(2))

    print(f"\nretokenising: the same {2 * pairs} symbols, read as {pairs} paired tokens")
    print(f"  vocabulary                {k:>12}   {k * k:>12}")
    print(f"  tokens                    {2 * pairs:>12}   {pairs:>12}")
    print(f"  perplexity per token      {fine_ppl:>12.4f}   {coarse_ppl:>12.4f}")
    print(f"  bits per SYMBOL           {fine_bits_per_symbol:>12.4f}   "
          f"{coarse_bits_per_symbol:>12.4f}")
    assert abs(fine_bits_per_symbol - coarse_bits_per_symbol) < 1e-9
    print(f"  Perplexity per token changed by a factor of {coarse_ppl / fine_ppl:.2f}.")
    print(f"  Bits per symbol did not change at all, to nine decimal places.")
    print(f"  Nothing about the model changed. Only the unit did.")

    # The conversion The Pile uses, with its measured constant.
    tokens_per_byte = 0.29335
    for loss in (nll.mean(), 2.0, 3.0):
        print(f"\n  bits per byte for a loss of {loss:.4f} nats/token, at "
              f"{tokens_per_byte} tokens per byte:")
        print(f"    BPB = {tokens_per_byte} * {loss:.4f} / ln 2 = "
              f"{tokens_per_byte * loss / np.log(2):.4f}")


if __name__ == "__main__":
    main()
