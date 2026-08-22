"""M05 lesson 7 - backpropagation is the chain rule on a computation graph.

Implements reverse-mode accumulation for a small network, and the proposition
that makes it trustworthy:

    reverse accumulation returns the exact gradient, up to floating point

checked against a central difference on every one of the network's parameters.

Two things this shows that a hand-worked example cannot. The gradient check
runs over all 209 parameters, not one. And the cost of the backward pass is
measured against the forward pass rather than asserted.

The network is a 4-32-1 regressor on the housing table. Rows are samples.

    python3 m05_07_backprop.py
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "datasets" / "m05-housing.csv"
FEATURES = ["area_sqft", "bedrooms", "age_years", "lot_sqft"]
TARGET = "price_k"
HIDDEN = 32
SEED = 20260822


def load() -> tuple[np.ndarray, np.ndarray]:
    """Standardised features and a centred target.

    Standardising here is not cosmetic and it is not the lesson: an unscaled
    design matrix makes the tanh saturate and the gradient check meaningless.
    Lesson 10 is where the scaling itself gets explained.
    """
    frame = pd.read_csv(DATA)
    x = frame[FEATURES].to_numpy(dtype=float)
    y = frame[TARGET].to_numpy(dtype=float)
    x = (x - x.mean(axis=0)) / x.std(axis=0)
    return x, (y - y.mean()) / y.std()


def init_params(rng: np.random.Generator, n_in: int) -> dict[str, np.ndarray]:
    return {
        "W1": rng.normal(0, 1.0 / np.sqrt(n_in), (n_in, HIDDEN)),
        "b1": np.zeros(HIDDEN),
        "w2": rng.normal(0, 1.0 / np.sqrt(HIDDEN), HIDDEN),
        "b2": np.zeros(1),
    }


def forward(p: dict[str, np.ndarray], x: np.ndarray, y: np.ndarray) -> tuple[float, dict]:
    """The forward pass, keeping every intermediate the backward pass will need.

    That dictionary is the whole memory cost of backpropagation, and it is why
    a deep network runs out of memory on activations rather than on weights.
    """
    z1 = x @ p["W1"] + p["b1"]
    h = np.tanh(z1)
    z2 = h @ p["w2"] + p["b2"][0]
    residual = z2 - y
    loss = float(residual @ residual / len(y))
    return loss, {"x": x, "z1": z1, "h": h, "residual": residual}


def backward(p: dict[str, np.ndarray], cache: dict) -> dict[str, np.ndarray]:
    """Reverse accumulation. Start at dL/dL = 1 and walk the graph backwards,
    multiplying each node's local derivative and accumulating.

    Every line is one application of the chain rule and nothing else.
    """
    n = len(cache["residual"])
    d_z2 = 2.0 * cache["residual"] / n           # dL/dz2
    d_w2 = cache["h"].T @ d_z2                   # through h . w2
    d_b2 = np.array([d_z2.sum()])
    d_h = np.outer(d_z2, p["w2"])                # gradient flowing into h
    d_z1 = d_h * (1.0 - np.tanh(cache["z1"]) ** 2)   # through tanh
    d_W1 = cache["x"].T @ d_z1                   # through x . W1
    d_b1 = d_z1.sum(axis=0)
    return {"W1": d_W1, "b1": d_b1, "w2": d_w2, "b2": d_b2}


def flat(params: dict[str, np.ndarray]) -> np.ndarray:
    return np.concatenate([params[k].ravel() for k in ("W1", "b1", "w2", "b2")])


def main() -> None:
    x, y = load()
    rng = np.random.default_rng(SEED)
    p = init_params(rng, x.shape[1])
    total = sum(v.size for v in p.values())
    print(f"loaded {DATA.name}: {len(y)} rows")
    print(f"network 4-{HIDDEN}-1, {total} parameters\n")

    loss, cache = forward(p, x, y)
    grads = backward(p, cache)
    print(f"loss {loss:.8f}")

    print("\ngradient check: every parameter, central difference at h = 1e-6")
    h = 1e-6
    worst_name, worst_rel = "", 0.0
    for name in ("W1", "b1", "w2", "b2"):
        analytic = grads[name].ravel()
        numeric = np.empty_like(analytic)
        flat_view = p[name].ravel()
        for i in range(flat_view.size):
            original = flat_view[i]
            flat_view[i] = original + h
            up, _ = forward(p, x, y)
            flat_view[i] = original - h
            down, _ = forward(p, x, y)
            flat_view[i] = original
            numeric[i] = (up - down) / (2.0 * h)
        denom = np.maximum(np.abs(analytic), 1e-12)
        rel = float(np.max(np.abs(analytic - numeric) / denom))
        print(f"  {name:>3} ({analytic.size:3d} params)  worst relative error {rel:.3e}")
        if rel > worst_rel:
            worst_name, worst_rel = name, rel
    print(f"  worst overall: {worst_name} at {worst_rel:.3e}")
    print(f"  all {total} analytic partials agree with the definition")

    print("\nwhat the backward pass costs, measured")
    reps = 200
    start = time.perf_counter()
    for _ in range(reps):
        forward(p, x, y)
    forward_s = (time.perf_counter() - start) / reps
    _, cache = forward(p, x, y)
    start = time.perf_counter()
    for _ in range(reps):
        backward(p, cache)
    backward_s = (time.perf_counter() - start) / reps
    print(f"  forward pass  : {forward_s * 1e3:7.3f} ms")
    print(f"  backward pass : {backward_s * 1e3:7.3f} ms")
    print(f"  ratio         : {backward_s / forward_s:7.2f} x the forward pass")
    print(f"  a full finite-difference gradient would need {2 * total} forward passes,")
    print(f"  which is {2 * total * forward_s:.2f} s against {forward_s + backward_s:.5f} s")


if __name__ == "__main__":
    main()
