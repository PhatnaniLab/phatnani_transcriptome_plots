"""SVG region parsing utilities for extracting matplotlib Path objects by region ID."""

from __future__ import annotations

from collections import defaultdict
from xml.etree import ElementTree as ET

import numpy as np
from matplotlib.path import Path
from svgpath2mpl import parse_path


def get_svg_regions(
    svg_string: str,
    flip_y: bool = True
) -> dict[str, list[Path]]:
    """
    Load regions from an SVG where each <path> has a unique 'id' attribute.

    Handles duplicate ids (e.g., regions on left and right). All paths are
    normalized so that the x-axis spans [0, 1] after parsing.

    :param svg_string: Raw SVG XML string to parse.
    :type svg_string: str
    :param flip_y: If True, negate the y-coordinates of every path vertex to
        convert from SVG (top-down) to matplotlib (bottom-up) coordinates.
    :type flip_y: bool

    :returns: Mapping of region_id to a list of parsed matplotlib Path objects.
    :rtype: dict[str, list[matplotlib.path.Path]]
    """
    root = ET.fromstring(svg_string)
    ns = {'svg': 'http://www.w3.org/2000/svg'}

    paths = root.findall(".//svg:path", ns)

    region_paths: defaultdict[str, list[Path]] = defaultdict(list)

    for path_el in paths:
        region_id: str | None = path_el.attrib.get('id')
        d: str | None = path_el.attrib.get('d')

        if region_id and d:
            path: Path = parse_path(d)

            if flip_y:
                path.vertices[:, 1] = path.vertices[:, 1] * -1

            region_paths[region_id].append(path)

    vertices_arr: np.ndarray = np.vstack([
        path.vertices
        for paths in region_paths.values()
        for path in paths
    ])

    min_vert: np.ndarray = vertices_arr.min(axis=0)
    max_vert: np.ndarray = vertices_arr.max(axis=0)
    scale: float = 1 / (max_vert[0] - min_vert[0])

    for paths in region_paths.values():
        for path in paths:
            path.vertices = (path.vertices - min_vert[None, :]) * scale

    return region_paths
