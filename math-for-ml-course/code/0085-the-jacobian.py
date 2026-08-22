"""Lesson 0085 - the Jacobian, the vector chain rule, and the volume factor.

Implements three named results.

1.  The vector chain rule.  For z = f(g(x)),  J_z = J_f  J_g,  so composing
    maps multiplies Jacobians. Checked against a finite-difference Jacobian of
    the composed map.

2.  The vector-Jacobian product.  v^T J is what reverse-mode autodiff actually
    computes, and it never builds J. Checked against forming J and multiplying.

3.  |det J| is the factor by which the map multiplies volume. Checked by Monte
    Carlo: push a cloud of points through the map and measure the area of the
    image against the area of the source.

The map is the one a single neural network layer applies, tanh(W x + b), so
none of this is an abstract exercise.

    python3 0085-the-jacobian.py
"""

from __future__ import annotations

import numpy as np

SEED = 20260822

# One layer: R^3 -> R^2, then a second layer R^2 -> R^2.
W1 = np.array([[0.60, -0.40, 0.25], [0.10, 0.80, -0.55]])
B1 = np.array([0.05, -0.20])
W2 = np.array([[1.20, -0.30], [0.45, 0.90]])
B2 = np.array([0.10, 0.15])


def layer1(x: np.ndarray) -> np.ndarray:
    return np.tanh(W1 @ x + B1)


def layer2(u: np.ndarray) -> np.ndarray:
    return np.tanh(W2 @ u + B2)


def composed(x: np.ndarray) -> np.ndarray:
    return layer2(layer1(x))


def jac_layer1(x: np.ndarray) -> np.ndarray:
    """d tanh(W1 x + b1) / dx. The tanh derivative is 1 - tanh^2, applied
    elementwise, which scales each ROW of W1."""
    pre = W1 @ x + B1
    return (1.0 - np.tanh(pre) ** 2)[:, None] * W1


def jac_layer2(u: np.ndarray) -> np.ndarray:
    pre = W2 @ u + B2
    return (1.0 - np.tanh(pre) ** 2)[:, None] * W2


def numeric_jacobian(fn, x: np.ndarray, h: float = 1e-6) -> np.ndarray:
    """Column j is d f / d x_j, by central difference. Shape is (outputs, inputs)."""
    base = fn(x)
    out = np.empty((len(base), len(x)))
    for j in range(len(x)):
        up, down = x.copy(), x.copy()
        up[j] += h
        down[j] -= h
        out[:, j] = (fn(up) - fn(down)) / (2.0 * h)
    return out


def vjp(v: np.ndarray, x: np.ndarray) -> np.ndarray:
    """v^T J for the composed map, computed the way backpropagation does it:
    right to left, one transposed Jacobian at a time, never forming the
    product of the two."""
    u = layer1(x)
    v = v @ jac_layer2(u)      # v now lives in the middle layer's space
    return v @ jac_layer1(x)   # and now in the input's


def main() -> None:
    rng = np.random.default_rng(SEED)
    x = np.array([0.7, -1.1, 0.4])

    print("1. the chain rule is a matrix product")
    j1 = jac_layer1(x)
    j2 = jac_layer2(layer1(x))
    analytic = j2 @ j1
    numeric = numeric_jacobian(composed, x)
    print(f"   J1 is {j1.shape[0]} x {j1.shape[1]}, J2 is {j2.shape[0]} x {j2.shape[1]}, "
          f"product is {analytic.shape[0]} x {analytic.shape[1]}")
    print(f"   largest gap against a finite-difference Jacobian: "
          f"{np.abs(analytic - numeric).max():.3e}")

    print("\n2. the vector-Jacobian product, without building the Jacobian")
    v = np.array([1.0, -2.0])
    print(f"   v^T J built and multiplied : {v @ analytic}")
    print(f"   v^T J accumulated in reverse: {vjp(v, x)}")
    print(f"   gap: {np.abs(v @ analytic - vjp(v, x)).max():.3e}")

    print("\n3. |det J| is the volume factor")
    # A square map so the determinant exists: fix the third input.
    def square_map(p: np.ndarray) -> np.ndarray:
        return composed(np.array([p[0], p[1], 0.4]))

    p0 = np.array([0.7, -1.1])
    j = numeric_jacobian(square_map, p0)
    det = float(np.linalg.det(j))
    print(f"   J at the point:\n{np.array2string(j, prefix='     ')}")
    print(f"   det J = {det:.6f},  |det J| = {abs(det):.6f}")

    # Monte Carlo. A small square around p0, pushed through the map. The image
    # area is estimated by the shoelace formula on the image of the boundary,
    # which is exact for the parallelogram the linearisation predicts.
    for side in (1e-1, 1e-2, 1e-3):
        corners = np.array([[0, 0], [side, 0], [side, side], [0, side]]) + p0 - side / 2
        image = np.array([square_map(c) for c in corners])
        shoelace = 0.0
        for i in range(4):
            a, b = image[i], image[(i + 1) % 4]
            shoelace += a[0] * b[1] - b[0] * a[1]
        measured = abs(shoelace) / 2.0
        source = side**2
        print(f"   square of side {side:.0e}: area {source:.3e} -> {measured:.3e}, "
              f"ratio {measured / source:.6f}")
    print(f"   the ratio converges on |det J| = {abs(det):.6f} as the square shrinks")


if __name__ == "__main__":
    main()
