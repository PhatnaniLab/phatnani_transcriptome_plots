"""Color normalization utilities for mapping numeric values to matplotlib colors."""

from __future__ import annotations

import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import ArrayLike


def normalize_colors(
    x: ArrayLike,
    cmap: str | matplotlib.colors.Colormap,
    vmin: float | None = None,
    vmax: float | None = None,
    clip: bool = True,
) -> np.ndarray | tuple[float, float, float, float]:
    """
    Map numeric values to RGBA colors using a matplotlib colormap.

    :param x: Numeric value or array of values to map.
    :type x: ArrayLike
    :param cmap: Colormap name or object used for mapping.
    :type cmap: str or matplotlib.colors.Colormap
    :param vmin: Lower bound for normalization. Defaults to the data minimum.
    :type vmin: float or None
    :param vmax: Upper bound for normalization. Defaults to the data maximum.
    :type vmax: float or None
    :param clip: If True, clip values outside [vmin, vmax] to the boundary colors.
    :type clip: bool

    :returns: RGBA colors. Returns an ndarray of shape ``(..., 4)`` for
        array-like input, or a ``(r, g, b, a)`` tuple for scalar input.
    :rtype: numpy.ndarray or tuple[float, float, float, float]
    """
    _norm = matplotlib.colors.Normalize(
        vmin=vmin,
        vmax=vmax,
        clip=clip
    )

    return plt.get_cmap(cmap)(_norm(x))
