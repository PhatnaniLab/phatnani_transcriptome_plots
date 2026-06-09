"""Colorbar drawing utilities."""

from typing import Any

import matplotlib.colors
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import Colorbar


def draw_colorbar(
    ax: Axes,
    xy: tuple[float, float, float, float],
    cmap: str | matplotlib.colors.Colormap,
    vmin: float,
    vmax: float,
    orientation: str = 'vertical',
    label: str = '',
    xycoords: str = 'data',
    **kwargs: Any,
) -> tuple[Colorbar, Axes]:
    """
    Draw a colorbar as an inset axis positioned using *xycoords*.

    Creates an inset axis inside *ax* at the rectangle defined by *xy*, then
    renders a colorbar there using a :class:`~matplotlib.cm.ScalarMappable` built
    from *cmap*, *vmin*, and *vmax*.

    :param ax: Parent axis on which the colorbar inset is placed.
    :type ax: matplotlib.axes.Axes
    :param xy: Bounding box ``(x0, y0, width, height)`` of the colorbar.
        ``(x0, y0)`` is the bottom-left corner.
    :type xy: tuple[float, float, float, float]
    :param cmap: Colormap name or object used to build the colorbar gradient.
    :type cmap: str or matplotlib.colors.Colormap
    :param vmin: Lower bound of the colorbar data range.
    :type vmin: float
    :param vmax: Upper bound of the colorbar data range.
    :type vmax: float
    :param orientation: ``'vertical'`` (default) or ``'horizontal'``.
    :type orientation: str
    :param label: Text label placed along the colorbar axis.
    :type label: str
    :param xycoords: Coordinate system for *xy*. ``'data'`` (default) places the
        colorbar in data coordinates; ``'axes fraction'`` places it in axes
        fraction coordinates (0–1 relative to the axes bounding box).
    :type xycoords: str
    :param kwargs: Additional keyword arguments forwarded to
        :meth:`~matplotlib.figure.Figure.colorbar`, e.g. ``ticks``,
        ``ticklocation``, ``format``, ``extend``.

    :returns: A ``(cbar, cax)`` tuple where *cbar* is the
        :class:`~matplotlib.colorbar.Colorbar` instance and *cax* is the
        :class:`~matplotlib.axes.Axes` inset on which it was drawn.
    :rtype: tuple[matplotlib.colorbar.Colorbar, matplotlib.axes.Axes]
    """
    _transforms = {
        'data': ax.transData,
        'axes fraction': ax.transAxes,
    }
    if xycoords not in _transforms:
        raise ValueError(f"xycoords must be 'data' or 'axes fraction', got {xycoords!r}")
    cax = ax.inset_axes(list(xy), transform=_transforms[xycoords])

    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    sm = ScalarMappable(cmap=cmap, norm=norm)
    # set_array is required so the ScalarMappable reports itself as initialised;
    # without it some matplotlib versions skip drawing the colorbar gradient.
    sm.set_array([])

    fig = ax.get_figure()
    cbar = fig.colorbar(
        sm,
        cax=cax,
        orientation=orientation,
        label=label,
        **kwargs,
    )

    cax.set_yticks(
        *format_ticks([vmin, vmax]),
        size=6
    )

    return cbar, cax

def format_ticks(ticks):
    return [
        int(t/1000) * 1000 if t > 1000 else t for t in ticks
    ], [
        f'{int(t/1000)}k' if t > 1000 else str(t) for t in ticks
    ]
