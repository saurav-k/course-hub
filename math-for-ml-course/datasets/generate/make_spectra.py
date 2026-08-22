"""Generate spectra.csv - a wide measurement matrix with a designed-in rank.

Why this dataset exists
-----------------------
M04 needs a matrix whose *own* low-rank structure is the point, not the low-rank
structure of its covariance. sensors.csv is tabular and built for the covariance
story (standardise or regret it). This one is a wide measurement matrix: 8,000
samples by 24 channels, built as four latent components plus small noise, so the
matrix itself is very nearly rank 4 and the SVD can be watched finding that out.

What is designed in, and therefore what a page may claim
--------------------------------------------------------
- Four latent components, so the centred matrix has four large singular values
  and then a cliff into a noise floor. The scree elbow at four is built, not
  discovered, and any page using it must say so.
- The components have overlapping, non-orthogonal spectral profiles, because
  orthogonal profiles would make the SVD's job trivial and would teach the wrong
  lesson: the SVD recovers an orthogonal basis for the *span*, not the original
  components. That distinction is the misconception quiz on the SVD page.
- Concentrations are non-negative and skewed, so the reader cannot assume the
  latent scores are Gaussian.
- Channels share a unit (absorbance), so this dataset does *not* punish skipping
  standardisation. That is sensors.csv's job, deliberately, and the two datasets
  are complementary rather than interchangeable.

Reproducibility contract
------------------------
    python3 make_spectra.py && git diff --exit-code

Re-running must leave the working tree clean. A diff means an unseeded source of
randomness crept in, which is a bug and not a new dataset. Every float is written
with a fixed six-decimal format so the file is byte-identical across platforms.
"""

from __future__ import annotations

import pathlib

import numpy as np

SEED = 20260822
N_SAMPLES = 8000
N_CHANNELS = 24
N_COMPONENTS = 4
NOISE_SD = 0.02

OUT = pathlib.Path(__file__).resolve().parent.parent / "spectra.csv"


def component_profiles() -> np.ndarray:
    """Four overlapping Gaussian bumps across the 24 channels, each unit norm.

    Overlapping on purpose: the profiles are linearly independent but not
    orthogonal, so the right singular vectors the SVD returns are not the
    profiles themselves. They span the same 4-dimensional subspace.
    """
    channels = np.arange(N_CHANNELS, dtype=float)
    centres = np.array([4.0, 9.5, 14.0, 19.0])
    widths = np.array([3.0, 2.5, 3.5, 2.0])
    profiles = np.exp(-0.5 * ((channels[None, :] - centres[:, None]) / widths[:, None]) ** 2)
    return profiles / np.linalg.norm(profiles, axis=1, keepdims=True)


def concentrations(rng: np.random.Generator) -> np.ndarray:
    """Non-negative, skewed, and on deliberately different scales.

    Different scales are what make the four singular values clearly ordered
    rather than a near-tie, so `sigma_k > sigma_{k+1}` holds strictly and the
    best rank-k approximation is unique at every k the pages use.
    """
    scales = np.array([1.00, 0.60, 0.35, 0.18])
    raw = rng.lognormal(mean=0.0, sigma=0.45, size=(N_SAMPLES, N_COMPONENTS))
    return raw * scales


def build() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(SEED)
    profiles = component_profiles()
    scores = concentrations(rng)
    signal = scores @ profiles
    noise = rng.normal(0.0, NOISE_SD, size=signal.shape)
    return signal + noise, scores


def write_csv(absorbance: np.ndarray) -> None:
    header = "sample_id," + ",".join(f"ch{i + 1:02d}" for i in range(N_CHANNELS))
    lines = [header]
    for i, row in enumerate(absorbance):
        cells = ",".join(f"{v:.6f}" for v in row)
        lines.append(f"{i + 1},{cells}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def report(absorbance: np.ndarray) -> None:
    """Print the properties a page is allowed to quote, so they are checkable."""
    centred = absorbance - absorbance.mean(axis=0)
    singular = np.linalg.svd(centred, compute_uv=False)
    total = (singular ** 2).sum()
    print(f"rows {absorbance.shape[0]}  channels {absorbance.shape[1]}")
    print(f"file {OUT.name}  {OUT.stat().st_size / 1e6:.2f} MB")
    print("singular values of the centred matrix, first 8:")
    print("  " + "  ".join(f"{s:.4f}" for s in singular[:8]))
    kept = np.cumsum(singular ** 2) / total
    for k in (1, 2, 3, 4, 5, 6):
        print(f"  k={k}  energy kept {kept[k - 1] * 100:7.4f}%   sigma_{k + 1}={singular[k]:.4f}")


if __name__ == "__main__":
    absorbance, _ = build()
    write_csv(absorbance)
    report(absorbance)
