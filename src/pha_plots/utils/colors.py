"""Color normalization utilities for mapping numeric values to matplotlib colors."""

import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import ArrayLike


def normalize_colors(
    x: ArrayLike | float | str | None,
    cmap: str | matplotlib.colors.Colormap,
    vmin: float | None = None,
    vmax: float | None = None,
    clip: bool = True,
    nan_color: str = 'lightgray'
) -> np.ndarray | tuple[float, float, float, float] | None:
    """
    Map numeric values to RGBA colors via *cmap*, with optional pass-through
    for pre-specified color strings.

    Dispatch by input type:

    * ``None`` → returns ``None`` immediately (no-op).
    * ``str`` → returned unchanged (treated as a pre-specified matplotlib color).
    * iterable → each element is mapped through *cmap* if numeric, or kept
      as-is if it is already a string.  Returns a list.
    * scalar number → mapped to a single RGBA color; returns a tuple or ndarray.

    NaN entries in numeric arrays render as *nan_color* via
    :meth:`~matplotlib.colors.Colormap.set_bad`.

    :param x: Value(s) to map.  ``None`` is a no-op; strings are passed through
        unchanged; iterables may mix numeric values and pre-specified color strings.
    :type x: ArrayLike, float, str, or None
    :param cmap: Colormap name or object used for the numeric → RGBA mapping.
    :type cmap: str or matplotlib.colors.Colormap
    :param vmin: Lower bound for normalization. Defaults to the data minimum.
    :type vmin: float or None
    :param vmax: Upper bound for normalization. Defaults to the data maximum.
    :type vmax: float or None
    :param clip: If ``True``, numeric values outside ``[vmin, vmax]`` are clamped
        to the boundary colors rather than the colormap's ``under``/``over`` colors.
    :type clip: bool
    :param nan_color: Color used to render ``NaN`` entries in numeric arrays.
    :type nan_color: str

    :returns: ``None`` if *x* is ``None``; the original string if *x* is a string;
        a mixed list of RGBA colors and/or pass-through strings if *x* is iterable;
        or an RGBA ndarray/tuple for a scalar numeric input.
    :rtype: None, str, list, tuple[float, float, float, float], or numpy.ndarray
    """

    if x is None:
        return None
    elif isinstance(x, str):
        return x

    _norm = matplotlib.colors.Normalize(
        vmin=vmin,
        vmax=vmax,
        clip=clip
    )

    _cmap = plt.get_cmap(cmap).copy()
    _cmap.set_bad(nan_color)

    try:
        return [
            _cmap(_norm(v)) if not isinstance(v, str) else v
            for v in x
        ]
    except TypeError:
        return _cmap(_norm(x))
