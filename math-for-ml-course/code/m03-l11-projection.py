"""M03 L11 - Orthogonality and projection: the closest point you can reach.

    python3 m03-l11-projection.py

Three results, each checked twice.

1. The orthogonality principle. The projection of b onto the span of the columns of
   A leaves a residual orthogonal to every column. Checked by taking the dot
   products, and again by confirming no other point in the span is closer.
2. The projection matrix P = A (A^T A)^-1 A^T satisfies P = P^T and P P = P.
3. An orthogonal matrix preserves every length and every angle, and its transpose
   is its inverse. Checked on 10,000 real points at once.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "points2d.csv"


def project(A: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """The point in the span of A's columns closest to b, and the residual."""
    coefficients = np.linalg.solve(A.T @ A, A.T @ b)
    projection = A @ coefficients
    return projection, b - projection


def main() -> None:
    a1 = np.array([2.0, 3.0, 1.0])
    a2 = np.array([1.0, 4.0, 2.0])
    A = np.column_stack([a1, a2])
    b = np.array([1.0, 1.0, 1.0])

    projection, residual = project(A, b)
    coefficients = np.linalg.solve(A.T @ A, A.T @ b)
    print("projecting b = (1, 1, 1) onto the plane spanned by a1 and a2")
    print(f"  coefficients : {np.round(coefficients, 6)}")
    print(f"  projection   : {np.round(projection, 6)}")
    print(f"  residual     : {np.round(residual, 6)}")
    print(f"  a1 . residual = {a1 @ residual:.3e}")
    print(f"  a2 . residual = {a2 @ residual:.3e}")
    assert abs(a1 @ residual) < 1e-12 and abs(a2 @ residual) < 1e-12

    print("\n  and no other point in the plane is closer:")
    best = np.linalg.norm(residual)
    rng = np.random.default_rng(21)
    worst_improvement = 0.0
    for _ in range(20_000):
        trial = A @ (coefficients + rng.normal(0.0, 0.35, size=2))
        worst_improvement = max(worst_improvement, best - float(np.linalg.norm(b - trial)))
    print(f"    best random challenger over 20,000 tries beat it by {worst_improvement:.3e}")
    print(f"    (a negative or zero number means nothing beat it)")
    assert worst_improvement <= 1e-12
    print("checked twice: the residual is orthogonal, and nothing in the span is nearer")

    print("\n-- the projection matrix --")
    P = A @ np.linalg.solve(A.T @ A, A.T)
    print(f"  max |P - P^T|  = {np.abs(P - P.T).max():.3e}   (symmetric)")
    print(f"  max |P P - P|  = {np.abs(P @ P - P).max():.3e}   (idempotent: projecting twice changes nothing)")
    print(f"  trace(P)       = {np.trace(P):.6f}, which equals the dimension it projects onto")
    assert np.allclose(P, P.T) and np.allclose(P @ P, P)
    assert abs(np.trace(P) - 2.0) < 1e-9
    print(f"  P @ b = {np.round(P @ b, 6)}, the same projection as above")
    assert np.allclose(P @ b, projection)

    print("\n-- orthogonal, orthonormal, orthogonal matrix --")
    q1 = a1 / np.linalg.norm(a1)
    w = a2 - (a2 @ q1) * q1          # Gram-Schmidt, one step
    q2 = w / np.linalg.norm(w)
    q3 = np.cross(q1, q2)
    Q = np.column_stack([q1, q2, q3])
    print(f"  ||q1|| = {np.linalg.norm(q1):.6f}, ||q2|| = {np.linalg.norm(q2):.6f}, q1 . q2 = {q1 @ q2:.3e}")
    print(f"  max |Q^T Q - I| = {np.abs(Q.T @ Q - np.eye(3)).max():.3e}")
    print(f"  max |Q Q^T - I| = {np.abs(Q @ Q.T - np.eye(3)).max():.3e}")
    print(f"  max |Q^-1 - Q^T| = {np.abs(np.linalg.inv(Q) - Q.T).max():.3e}")
    assert np.allclose(Q.T @ Q, np.eye(3)) and np.allclose(np.linalg.inv(Q), Q.T)
    print("checked twice: both products give the identity, so the transpose is the inverse")

    print("\n  a matrix with orthogonal but NOT orthonormal columns is not an orthogonal matrix:")
    scaled = np.column_stack([q1 * 3.0, q2 * 3.0, q3 * 3.0])
    print(f"    columns still mutually orthogonal: max off-diagonal of M^T M ="
          f" {np.abs(scaled.T @ scaled - np.diag(np.diag(scaled.T @ scaled))).max():.3e}")
    print(f"    but max |M^T M - I| = {np.abs(scaled.T @ scaled - np.eye(3)).max():.3f}, so M^-1 is not M^T")

    print("\n-- an orthogonal map on 10,000 real points --")
    points = pd.read_csv(DATA)[["x", "y"]].to_numpy(dtype=float)
    theta = np.pi / 6
    R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    rotated = points @ R.T
    before = np.linalg.norm(points, axis=1)
    after = np.linalg.norm(rotated, axis=1)
    print(f"  max |length before - length after| over {len(points):,} points: {np.abs(before - after).max():.3e}")
    pairs = np.random.default_rng(31).integers(0, len(points), size=(2_000, 2))
    cos_before = np.einsum("ij,ij->i", points[pairs[:, 0]], points[pairs[:, 1]])
    cos_after = np.einsum("ij,ij->i", rotated[pairs[:, 0]], rotated[pairs[:, 1]])
    print(f"  max |dot before - dot after| over 2,000 pairs: {np.abs(cos_before - cos_after).max():.3e}")
    assert np.abs(before - after).max() < 1e-12
    print("checked twice: lengths and inner products both survive a rotation unchanged")


if __name__ == "__main__":
    main()
