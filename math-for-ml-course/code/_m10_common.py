"""Shared dataset loading for the M10 programs.

Every M10 program is self-contained and needs only numpy and pandas. This file
exists so the loading paragraph is written once; each program also carries its
own copy of `load()` inline, so a reader who downloads one `.py` on its own can
still run it. Keep the two in step.
"""

from __future__ import annotations

import pathlib

import pandas as pd

RAW = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/"


def load(name: str) -> pd.DataFrame:
    """Read a committed M10 dataset from disk, falling back to the raw URL.

    The relative path works in a clone. The URL fallback is what makes the file
    paste-and-run in Colab or a bare Jupyter kernel.
    """
    local = pathlib.Path(__file__).resolve().parent.parent / "datasets" / name
    if local.exists():
        return pd.read_csv(local)
    return pd.read_csv(RAW + name)
