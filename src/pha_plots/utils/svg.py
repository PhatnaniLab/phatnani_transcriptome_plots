import numpy as np
from xml.etree import ElementTree as ET
from svgpath2mpl import parse_path
from collections import defaultdict


def get_svg_regions(svg_string, flip_y=True):
    """
    Load regions from an SVG where each <path> has a unique 'id' attribute.
    Handles duplicate ids (e.g., regions on left and right).

    Returns:
        dict: Mapping of region_id -> list of parsed paths (matplotlib Path objects)
    """
    root = ET.fromstring(svg_string)
    ns = {'svg': 'http://www.w3.org/2000/svg'}

    paths = root.findall(".//svg:path", ns)

    region_paths = defaultdict(list)

    vertices = []
    for path_el in paths:
        region_id = path_el.attrib.get('id')
        d = path_el.attrib.get('d')

        if region_id and d:
            path = parse_path(d)
            if flip_y:
                path.vertices[:, 1] *= -1
            region_paths[region_id].append(path)
            vertices.append(path.vertices)

    vertices = np.vstack(vertices)
    min_vert, max_vert = vertices.min(axis=0), vertices.max(axis=0)
    scale = 1 / (max_vert[0] - min_vert[0])

    for paths in region_paths.values():
        for path in paths:
            path.vertices = (path.vertices - min_vert[None, :]) * scale

    return region_paths
