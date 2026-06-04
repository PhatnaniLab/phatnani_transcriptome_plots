"""Colorbar drawing utilities for placing colorbars at data coordinates."""

from typing import Any

import matplotlib.colors
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import Colorbar


def draw_colorbar(
    ax: Axes,
    xycoords: tuple[float, float, float, float],
    cmap: str | matplotlib.colors.Colormap,
    vmin: float,
    vmax: float,
    orientation: str = 'vertical',
    label: str = '',
    **kwargs: Any,
) -> tuple[Colorbar, Axes]:
    """
    Draw a colorbar as an inset axis positioned at *xycoords* in data coordinates.

    Creates an inset axis inside *ax* at the rectangle defined by *xycoords*, then
    renders a colorbar there using a :class:`~matplotlib.cm.ScalarMappable` built
    from *cmap*, *vmin*, and *vmax*. The inset is placed in the same coordinate
    space as the data, so its position scales and pans with the axes.

    :param ax: Parent axis on which the colorbar inset is placed.
    :type ax: matplotlib.axes.Axes
    :param xycoords: Bounding box ``(x0, y0, width, height)`` of the colorbar in
        the data coordinate system of *ax*. ``(x0, y0)`` is the bottom-left corner.
    :type xycoords: tuple[float, float, float, float]
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
    :param kwargs: Additional keyword arguments forwarded to
        :meth:`~matplotlib.figure.Figure.colorbar`, e.g. ``ticks``,
        ``ticklocation``, ``format``, ``extend``.

    :returns: A ``(cbar, cax)`` tuple where *cbar* is the
        :class:`~matplotlib.colorbar.Colorbar` instance and *cax* is the
        :class:`~matplotlib.axes.Axes` inset on which it was drawn.
    :rtype: tuple[matplotlib.colorbar.Colorbar, matplotlib.axes.Axes]
    """
    # Create an inset axis at the requested data-coordinate rectangle.
    cax = ax.inset_axes(list(xycoords), transform=ax.transData)

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
