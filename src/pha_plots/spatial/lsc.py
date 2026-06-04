"""Spinal cord drawing function using an embedded SVG template."""

from __future__ import annotations

from typing import Any, Mapping

import matplotlib.colors
from matplotlib.axes import Axes
from matplotlib.patches import (
    PathPatch,
    Patch
)

from pha_plots.utils import get_svg_regions, normalize_colors

SPINAL_SVG = """
<ns0:svg xmlns:ns0="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 154.18 118.84">
  <ns0:defs>
    <ns0:style>
      .cls-1 {
        fill: #ce5d5d;
      }

      .cls-2 {
        fill: #718191;
      }

      .cls-3 {
        fill: #a0532b;
      }

      .cls-4 {
        fill: #609e9f;
      }

      .cls-5 {
        fill: #314f50;
      }

      .cls-6 {
        fill: #f47e53;
      }

      .cls-7 {
        fill: #bb8d8e;
      }

      .cls-8 {
        fill: #cd863c;
      }

      .cls-9 {
        fill: #fed9b9;
      }

      .cls-10 {
        fill: #8a191b;
      }

      .cls-11 {
        fill: #f3a461;
      }
    </ns0:style>
  </ns0:defs>

  <ns0:g>
    <ns0:g id="Layer_1">
      <ns0:g>
        <ns0:path class="cls-8" d="M52.56,27.85c5.28-2.41,10.83-5.27,16.56-6.43,10.59-1.57,22.36-.45,31.95,4.39,4.57,2.44,8.63,5.69,13.23,8.61l2.18-2.16c-4.62-3.11-8.81-6.46-13.46-9.03-10.4-5.41-23.16-6.66-34.65-4.91-6.21,1.3-12.23,4.49-17.96,7.19-3.62,1.78-7.24,3.74-10.71,5.95l2.19,2.19c3.43-2.18,7.06-4.08,10.67-5.8Z" id="Dors_Edge" />
        <ns0:path class="cls-3" d="M114.52,34.57c2.88,1.88,5.86,3.63,8.54,5.82l.15.12c12.52,9.66,13.87,24.9,5.74,36.93l5.08,2.28c7.94-13.25,6.17-29.58-6.99-40.05l-.16-.13c-2.91-2.44-6.14-4.4-9.27-6.5-.22-.14-.44-.29-.66-.44-.16-.11-.32-.22-.48-.33l-2.18,2.16c.08.05.15.1.23.15Z" id="Lat_Edge" />
        <ns0:path class="cls-3" d="M22.41,67.66c-1.15-5.4.62-11.16,2.88-16.08,3.51-7.88,9.64-13.5,16.59-17.93l-2.19-2.19c-.62.39-1.24.78-1.84,1.19-7.13,4.84-13.37,10.96-17.02,19.39-2.45,5.51-4.37,11.95-3.12,17.98.81,3.97,3.24,7.88,6.3,11.44l5.3-2.39c-3.32-3.5-6.05-7.42-6.89-11.42Z" id="Lat_Edge" />
        <ns0:path class="cls-6" d="M128.95,77.44c-1.24,1.83-2.68,3.59-4.35,5.24-4.93,5.6-11.58,8.68-18.45,10.83-2.38.96-4.97,1.94-7.61,2.65-5.83,1.56-11.91,1.77-16.55-2.51-2.36-2.7-2.24-9.3-3.38-13.1-.39-1.23-.78-.39-.98.44-.61,2.03-.85,7.06-2.57,10.3-3.3,6.64-9.77,6.73-15.89,5-2.31-.65-4.57-1.56-6.59-2.47-4.75-2.04-9.41-3.48-13.85-6.58-2.98-2.2-6.44-5.01-9.43-8.16l-5.3,2.39c.44.52.9,1.03,1.37,1.53,3.2,3.44,6.87,6.51,10.04,8.92,4.81,3.47,9.87,5.08,15.02,7.36,1.84.85,3.86,1.7,5.94,2.38.93.3,1.88.57,2.84.8,6.27,1.47,12.94.94,16.21-5.9,1.89-3.96,2.27-8.05,2.45-10.44.03-1.01.51-1.94.58-.55.2,4.43.64,10.46,3.2,13.47,4.58,4.36,11.1,4.58,16.94,3.27.21-.05.42-.09.63-.14,3.23-.79,6.42-2.02,9.33-3.23,7.45-2.4,14.67-5.85,20.01-12.11,1.51-1.54,2.84-3.16,4.03-4.84.52-.74,1-1.49,1.46-2.26l-5.08-2.28Z" id="Vent_Edge" />
        <ns0:path class="cls-9" d="M45.2,34.24c2.27-.47,6.18,2.7,8.34,4.82,2.23,2.19,4.35,4.59,6.35,7.06,2.34,2.9,4.54,5.96,7.43,8.11l.39-.03-.39.03c1.4,1.04,2.97,1.87,4.8,2.35,4.27,1.17,9.09,1.25,13.33-.15,2.14-.7,3.93-1.97,5.53-3.52l-.57-.1.57.1c2.96-2.87,5.27-6.7,7.95-9.69,3.1-3.2,7.95-10.12,12.85-8.99.61.21,1.13.63,1.52,1.18l1.01-1c-4.6-2.92-8.67-6.17-13.23-8.61-9.59-4.84-21.36-5.96-31.95-4.39-5.72,1.16-11.28,4.02-16.56,6.43-3.62,1.72-7.24,3.62-10.67,5.8l1.61,1.61c.36-.51.9-.88,1.7-1.02Z" id="Dors_Med_White" />
        <ns0:path class="cls-11" d="M42.95,65.96c1.33-2.6,4.56-4.17,6.99-6.17l-.14-.05.14.05c1.27-1.04,2.33-2.19,2.79-3.66.06-.32.09-.64.09-.95h-.1s.1,0,.1,0c.07-5.1-7.36-9.52-8.99-14.08-.81-1.65-1.39-4.34-.35-5.84l-1.61-1.61c-6.95,4.42-13.08,10.04-16.59,17.93-2.26,4.93-4.03,10.68-2.88,16.08.84,4,3.58,7.92,6.89,11.42l13.47-6.08c-1.03-2.07-1.16-4.44.17-7.03Z" id="Med_Lat_White" />
        <ns0:path class="cls-7" d="M56.8,81.45c-4.87-.68-11.71-3.81-14.03-8.46l-13.47,6.08c2.99,3.15,6.45,5.96,9.43,8.16,4.44,3.1,9.1,4.54,13.85,6.58,2.02.91,4.28,1.82,6.59,2.47l-.07-14.96c-.72.15-1.48.21-2.3.13Z" id="Vent_Lat_White" />
        <ns0:path class="cls-7" d="M101.53,81.6c-1.02.25-2.05.31-3.06.23l.07,14.32c2.64-.7,5.23-1.68,7.61-2.65,6.87-2.15,13.52-5.23,18.45-10.83,1.67-1.65,3.12-3.41,4.35-5.24l-14.87-6.68c-.61,5.48-6.87,9.69-12.55,10.85Z" id="Vent_Lat_White" />
        <ns0:path class="cls-1" d="M93.03,79.44c-4.07-3.99-5.52-9.1-9.92-11.5l-.26.09.26-.09c-1.25-.68-2.71-1.15-4.56-1.31-1.94-.16-3.57.34-5.03,1.23l.13.05-.13-.05c-5.41,3.32-8.32,12.16-14.42,13.46l.07,14.96c6.12,1.72,12.59,1.64,15.89-5,1.71-3.24,1.96-8.27,2.57-10.3.2-.83.6-1.67.98-.44,1.14,3.8,1.02,10.4,3.38,13.1,4.64,4.28,10.72,4.07,16.55,2.51l-.07-14.32c-1.99-.17-3.9-.96-5.44-2.38Z" id="Vent_Med_White" />
        <ns0:path class="cls-11" d="M123.21,40.51l-.15-.12c-2.68-2.18-5.66-3.94-8.54-5.82-.08-.05-.15-.1-.23-.15l-1.01,1c.63.91.91,2.2.67,3.63-.37,2.56-2.52,5.09-4.53,7.55-2.94,3.39-4.22,6.32-4.17,8.92l.51.09-.51-.09c.03,1.56.53,3,1.44,4.35l.3-.1-.3.1c1.26,1.86,3.29,3.55,5.9,5.13l.13.14c1.18,1.97,1.56,3.86,1.36,5.62l14.87,6.68c8.13-12.03,6.78-27.27-5.74-36.93Z" id="Med_Lat_White" />
        <ns0:path class="cls-2" d="M59.88,46.12c-2.01-2.47-4.12-4.87-6.35-7.06-2.15-2.12-6.06-5.3-8.34-4.82-.8.14-1.34.51-1.7,1.02l.28.28-.28-.28c-1.04,1.49-.46,4.19.35,5.84,1.62,4.56,9.05,8.98,8.99,14.08l14.49-.95c-2.89-2.15-5.09-5.21-7.43-8.11Z" id="Dors_Horn" />
        <ns0:path class="cls-5" d="M93.03,79.44c1.54,1.42,3.45,2.21,5.44,2.38v-.04s0,.04,0,.04c1.01.09,2.04.02,3.06-.23,5.69-1.16,11.94-5.36,12.55-10.85l-.18-.08.18.08c.2-1.76-.19-3.65-1.36-5.62l-.13-.14c-2.61-1.58-4.64-3.26-5.9-5.13l-23.58,8.07c4.41,2.4,5.85,7.51,9.92,11.5Z" id="Vent_Horn" />
        <ns0:path class="cls-5" d="M42.95,65.96c-1.34,2.59-1.2,4.96-.17,7.03l.07-.03-.07.03c2.31,4.66,9.16,7.78,14.03,8.46.82.08,1.58.02,2.3-.13v-.11s0,.11,0,.11c6.1-1.3,9-10.13,14.42-13.46l-23.57-8.07c-2.44,1.99-5.66,3.57-6.99,6.17Z" id="Vent_Horn" />
        <ns0:path class="cls-4" d="M85.44,56.43c-4.24,1.4-9.06,1.31-13.33.15-1.83-.48-3.39-1.31-4.8-2.35l-14.49.95c0,.31-.03.63-.09.95-.46,1.47-1.52,2.62-2.79,3.66l23.57,8.07c1.46-.9,3.1-1.4,5.03-1.23,1.85.16,3.31.63,4.56,1.31l23.58-8.07c-.91-1.35-1.41-2.79-1.44-4.35l-14.28-2.61c-1.6,1.55-3.38,2.82-5.53,3.52ZM78.05,63.36c-3.08,0-5.57-.67-5.57-1.5s2.5-1.5,5.57-1.5,5.57.67,5.57,1.5-2.5,1.5-5.57,1.5Z" id="Med_Grey" />
        <ns0:path class="cls-2" d="M111.77,34.24c-4.9-1.13-9.75,5.79-12.85,8.99-2.68,2.99-4.99,6.82-7.95,9.69l14.28,2.61c-.05-2.6,1.23-5.53,4.17-8.92,2.02-2.46,4.17-4.99,4.53-7.55.24-1.43-.04-2.72-.67-3.63l-.18.17.18-.17c-.39-.56-.91-.97-1.52-1.18Z" id="Dors_Horn" />
        <ns0:path class="cls-10" d="M78.05,60.36c-3.08,0-5.57.67-5.57,1.5s2.5,1.5,5.57,1.5,5.57-.67,5.57-1.5-2.5-1.5-5.57-1.5Z" id="Cent_Can" />
      </ns0:g>
    </ns0:g>
  </ns0:g>
</ns0:svg>
"""

def draw_spinal_cord(
    ax: Axes,
    values: dict[str, Any] | None,
    cmap: str | matplotlib.colors.Colormap,
    vmin: float | None = None,
    vmax: float | None = None,
    scale: float = 1.0,
    offset: tuple[float, float] | None = None,
    patch_kwargs: dict[str, Any] | None = None,
    nan_color: str = 'lightgray'
) -> dict[str, Patch]:
    """
    Draw the spinal cord SVG on the given axis with optional per-region coloring.

    Regions with no entry in *values* are rendered in light gray.

    :param ax: Matplotlib axis on which to draw the patches.
    :type ax: matplotlib.axes.Axes
    :param values: Mapping of SVG region id to a numeric value (or array of values)
        that is normalized and mapped to a color. Pass ``None`` to render all
        regions in light gray.
    :type values: dict[str, Any] or None
    :param cmap: Colormap name or object used to map *values* to RGBA colors.
    :type cmap: str or matplotlib.colors.Colormap
    :param vmin: Lower bound for color normalization. Defaults to the data minimum.
    :type vmin: float or None
    :param vmax: Upper bound for color normalization. Defaults to the data maximum.
    :type vmax: float or None
    :param scale: Uniform scale factor applied to all path vertices.
    :type scale: float
    :param offset: (x_offset, y_offset) translation applied to all path vertices
        after scaling.
    :type offset: tuple[float, float] or None

    :returns: Dict of Matplotlib patch objects added to *ax*
    :rtype: dict of matplotlib.patches.Polygon
    """

    if values is not None:
        colors = {
            k: normalize_colors(v, cmap, vmin, vmax)
            for k, v in values.items()
        }
    else:
        colors = None


    _patch_refs = {}
    _patch_kwargs = {
        'edgecolor': 'black',
        'linewidth': 0.5
    }

    if patch_kwargs is not None:
        _patch_kwargs.update(patch_kwargs)

    for region_id, paths in get_svg_regions(SPINAL_SVG).items():
        color = colors.get(region_id, nan_color) if colors else nan_color

        for path in paths:
            if scale is not None:
                path.vertices *= scale

            if offset is not None:
                path.vertices[:, 0] += offset[0]
                path.vertices[:, 1] += offset[1]

            _patch_refs[region_id] = ax.add_patch(
                PathPatch(path, facecolor=color, **_patch_kwargs)
            )

    return _patch_refs
