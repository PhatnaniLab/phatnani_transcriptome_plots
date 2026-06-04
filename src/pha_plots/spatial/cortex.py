"""Cortical slice drawing functions for frontal and motor cortex regions."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import matplotlib.colors
import numpy as np
from matplotlib.axes import Axes
from matplotlib.patches import Polygon
from numpy.typing import ArrayLike

from pha_plots.utils import normalize_colors


def _draw_cortex_slice(
    ax: Axes,
    colors: np.ndarray | list[np.ndarray],
    offset: list[float] | None = None,
    scale: float = 1.0,
    y_int: float = 0.06,
    x_int: float = 0.3,
    side_slope: float = 1.6,
    layer_widths: list[float] = [1, 2, 4, 1, 4, 3, 3],
    layer_torque: list[float] = [1, 1.05, 1.1, 1.25, 1.25, 1.5, 1.9],
    slice_torque: float = 1.2,
    add_lines: bool = True,
    is_sig: list[Any] | None = None,
) -> list[Polygon]:
    """
    Draw a stylized cortical slice as a stack of concentric quarter-circle arc polygons.

    Each layer is a filled polygon bounded by a distorted quarter-circle arc on the
    outside and the next-inner arc on the inside. The right edge of every arc is
    clipped by a straight side line, giving the slice its wedge-like appearance.
    An outer border arc at radius 1 is always drawn.

    :param ax: Matplotlib axis on which to draw the patches.
    :type ax: matplotlib.axes.Axes
    :param colors: Fill color for each layer, ordered from outermost to innermost.
        Accepts any color specification understood by Matplotlib.
    :type colors: numpy.ndarray
    :param offset: (x, y) translation applied to every polygon vertex after scaling.
        Defaults to [0, 0].
    :type offset: list or None
    :param scale: Uniform scale factor applied to all coordinates before the offset.
    :type scale: float
    :param y_int: Minimum y-value (bottom intercept) of the slice boundary. Controls
        how far below the arc the slice extends on the y-axis.
    :type y_int: float
    :param x_int: x-intercept of the straight side line that clips each arc on the right.
    :type x_int: float
    :param side_slope: Slope of the side-clipping line ``y = side_slope * (x - x_int)``.
        Larger values make the right edge steeper.
    :type side_slope: float
    :param layer_widths: Relative thickness of each cortical layer, from outermost to
        innermost. These are converted internally to fractional arc radii.
    :type layer_widths: list of float
    :param layer_torque: Per-layer x-scale multiplier applied before ``slice_torque``.
        Values > 1 compress the arc horizontally, producing the curved appearance of
        deeper layers.
    :type layer_torque: list of float
    :param slice_torque: Global x-scale multiplier applied to every arc in addition to
        the per-layer ``layer_torque``.
    :type slice_torque: float
    :param add_lines: If True, draw a thin black boundary line along the outer edge of
        each layer arc.
    :type add_lines: bool
    :param is_sig: Per-layer significance flag. Truthy values cause an asterisk
        annotation to be placed at the left edge of that layer. Defaults to all None
        (no annotations).
    :type is_sig: list or None

    :returns: List of Matplotlib patch objects added to *ax* (border patch first,
        then one patch per layer).
    :rtype: list of matplotlib.patches.Polygon
    """
    if offset is None:
        offset = [0, 0]

    if is_sig is None:
        is_sig = [None] * len(layer_widths)

    # Prepend 0 so cumsum gives the outer radius of each layer (outermost = sum of all widths).
    layer_widths = np.concatenate(([0], np.asanyarray(layer_widths)))
    # Convert cumulative widths to fractional radii, then rescale into [y_int, 1-y_int²].
    layer_heights = (np.sum(layer_widths) - np.cumsum(layer_widths[:-1])) / np.sum(layer_widths)
    layer_heights = (layer_heights + y_int) * (1 - y_int)

    def _sideline(x: float) -> float:
        # Linear right-edge clip: arcs are kept only where y >= this line.
        return side_slope * (x - x_int)

    def curve(
        arclen: float,
        side_func: Callable[[float], float] = _sideline,
        xscale: float = 1.0,
    ) -> np.ndarray:
        # Combined x-compression: per-layer torque * global torque.
        xscale = xscale * slice_torque

        # Sample a quarter-circle arc (x=cos, y=sin) at the given radius.
        polar = np.linspace(0, np.pi / 2, 200).reshape(-1, 1)
        curves = np.concatenate((np.cos(polar), np.sin(polar)), axis=1) * arclen
        # Squish x-axis to create the characteristic bent shape of deeper layers.
        curves[:, 0] *= xscale

        # Keep only the arc segment above the side line, then close the polygon
        # with the top-left corner, the bottom of the side line, and the x-intercept.
        plot_curve = np.vstack((
            curves[curves[:, 1] >= side_func(curves[:, 0]), :],
            np.array([[0, arclen], [0, y_int]]),
            np.array([[x_int, 0.0]]),
        )) * scale

        plot_curve[:, 0] += offset[0]
        plot_curve[:, 1] += offset[1]

        return plot_curve

    # Outer border drawn at radius 1 (the full unit arc), on top of all layers.
    _patch_refs = [
        ax.add_patch(Polygon(
            curve(1),
            facecolor='None',
            edgecolor='black',
            lw=0.5,
            zorder=100
        ))
    ]

    for layer, (height, color, xs, sig) in enumerate(zip(
        layer_heights,
        colors,
        layer_torque,
        is_sig
    )):
        # Each layer is a filled polygon clipped to its outer arc radius.
        # zorder=layer means outer layers are drawn on top of inner ones.
        _patch_refs.append(
            ax.add_patch(Polygon(
                curve(height, xscale=xs),
                facecolor=color,
                zorder=layer
            ))
        )

        if add_lines:
            # Thin boundary line along the outer edge of this layer.
            _line_curve = curve(height, xscale=xs)
            ax.plot(_line_curve[:, 0], _line_curve[:, 1], color='black', lw=0.25, zorder=100)

        if sig:
            # Place the asterisk vertically centered within this layer.
            try:
                yloc = (layer_heights[layer] + layer_heights[layer + 1]) / 2
            except IndexError:
                # Innermost layer has no layer[layer+1]; use y_int as the inner bound.
                yloc = (layer_heights[layer] + y_int) / 2

            ax.annotate(
                "*",
                (
                    offset[0] - (0.1 * scale),
                    offset[1] + ((yloc - (y_int / 2)) * scale)
                ),
                size=6,
                ha='center',
                va='center'
            )

    return _patch_refs


def draw_frontal_cortex(
    ax: Axes,
    values: ArrayLike,
    cmap: str | matplotlib.colors.Colormap,
    vmin: float | None = None,
    vmax: float | None = None,
    offset: list[float] | None = None,
    scale: float = 1.0,
    add_lines: bool = True,
    is_sig: list[Any] | None = None,
) -> list[Polygon]:
    """
    Draw a stylized frontal cortex slice with per-layer colors derived from *values*.

    Delegates to :func:`_draw_cortex_slice` using default frontal cortex geometry.

    :param ax: Matplotlib axis on which to draw the patches.
    :type ax: matplotlib.axes.Axes
    :param values: Per-layer numeric values that are mapped to colors via *cmap*.
    :type values: ArrayLike
    :param cmap: Colormap name or object used to map *values* to RGBA colors.
    :type cmap: str or matplotlib.colors.Colormap
    :param vmin: Lower bound for color normalization. Defaults to the data minimum.
    :type vmin: float or None
    :param vmax: Upper bound for color normalization. Defaults to the data maximum.
    :type vmax: float or None
    :param offset: (x, y) translation applied to every polygon vertex after scaling.
        Defaults to [0, 0].
    :type offset: list or None
    :param scale: Uniform scale factor applied to all coordinates.
    :type scale: float
    :param add_lines: If True, draw a thin black boundary line along each layer arc.
    :type add_lines: bool
    :param is_sig: Per-layer significance flag. Truthy values place an asterisk
        annotation at the left edge of that layer.
    :type is_sig: list or None

    :returns: List of Matplotlib patch objects added to *ax*.
    :rtype: list of matplotlib.patches.Polygon
    """
    return _draw_cortex_slice(
        ax,
        normalize_colors(values, cmap, vmin, vmax),
        offset,
        scale=scale,
        add_lines=add_lines,
        is_sig=is_sig
    )


def draw_motor_cortex(
    ax: Axes,
    values: ArrayLike,
    cmap: str | matplotlib.colors.Colormap,
    vmin: float | None = None,
    vmax: float | None = None,
    offset: list[float] | None = None,
    scale: float = 1.0,
    add_lines: bool = True,
    is_sig: list[Any] | None = None,
) -> list[Polygon]:
    """
    Draw a stylized motor cortex slice with per-layer colors derived from *values*.

    Delegates to :func:`_draw_cortex_slice` using default motor cortex geometry.

    :param ax: Matplotlib axis on which to draw the patches.
    :type ax: matplotlib.axes.Axes
    :param values: Per-layer numeric values that are mapped to colors via *cmap*.
    :type values: ArrayLike
    :param cmap: Colormap name or object used to map *values* to RGBA colors.
    :type cmap: str or matplotlib.colors.Colormap
    :param vmin: Lower bound for color normalization. Defaults to the data minimum.
    :type vmin: float or None
    :param vmax: Upper bound for color normalization. Defaults to the data maximum.
    :type vmax: float or None
    :param offset: (x, y) translation applied to every polygon vertex after scaling.
        Defaults to [0, 0].
    :type offset: list or None
    :param scale: Uniform scale factor applied to all coordinates.
    :type scale: float
    :param add_lines: If True, draw a thin black boundary line along each layer arc.
    :type add_lines: bool
    :param is_sig: Per-layer significance flag. Truthy values place an asterisk
        annotation at the left edge of that layer.
    :type is_sig: list or None

    :returns: List of Matplotlib patch objects added to *ax*.
    :rtype: list of matplotlib.patches.Polygon
    """
    return _draw_cortex_slice(
        ax,
        normalize_colors(values, cmap, vmin, vmax),
        offset,
        scale=scale,
        add_lines=add_lines,
        is_sig=is_sig
    )
