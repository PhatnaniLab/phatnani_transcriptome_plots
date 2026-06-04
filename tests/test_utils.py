"""Unit tests for pha_plots.utils — normalize_colors and get_svg_regions."""

import numpy as np
import pytest
import matplotlib.colors as mcolors
import matplotlib.path
import matplotlib.pyplot as plt

from pha_plots.utils.colors import normalize_colors
from pha_plots.utils.svg import get_svg_regions


# ── Fixtures ──────────────────────────────────────────────────────────────────

SIMPLE_SVG = """\
<svg xmlns="http://www.w3.org/2000/svg">
  <path id="left"  d="M 0 0 L 0 10 L 10 10 L 10 0 Z" />
  <path id="right" d="M 20 0 L 20 10 L 30 10 L 30 0 Z" />
</svg>"""

DUPLICATE_ID_SVG = """\
<svg xmlns="http://www.w3.org/2000/svg">
  <path id="region" d="M 0 0 L 10 0 L 10 10 Z" />
  <path id="region" d="M 20 0 L 30 0 L 30 10 Z" />
</svg>"""

MISSING_ATTR_SVG = """\
<svg xmlns="http://www.w3.org/2000/svg">
  <path id="named"    d="M 0 0 L 10 0 L 10 10 Z" />
  <path               d="M 20 0 L 30 0 L 30 10 Z" />
  <path id="no_path"                              />
</svg>"""


# ── normalize_colors ──────────────────────────────────────────────────────────

class TestNormalizeColors:
    # ── return-type dispatch ──────────────────────────────────────────────────

    def test_none_returns_none(self):
        assert normalize_colors(None, "viridis") is None

    def test_string_returns_unchanged(self):
        assert normalize_colors("red", "viridis") == "red"

    def test_iterable_returns_list(self):
        result = normalize_colors([0.0, 0.5, 1.0], "viridis", vmin=0.0, vmax=1.0)
        assert isinstance(result, list)

    def test_iterable_list_length_matches_input(self):
        result = normalize_colors([0.0, 0.5, 1.0], "viridis", vmin=0.0, vmax=1.0)
        assert len(result) == 3

    def test_scalar_returns_four_channel_color(self):
        result = normalize_colors(0.5, "viridis")
        assert len(result) == 4

    def test_2d_array_iterates_over_rows(self):
        # A 2-D array is iterable — the function maps each row independently.
        values = np.array([[0.0, 0.5], [0.75, 1.0]])
        result = normalize_colors(values, "viridis", vmin=0.0, vmax=1.0)
        assert isinstance(result, list)
        assert len(result) == 2
        assert np.asarray(result[0]).shape == (2, 4)

    # ── RGBA element values ───────────────────────────────────────────────────

    def test_rgba_elements_in_unit_range(self):
        result = normalize_colors([0.0, 0.5, 1.0], "plasma", vmin=0.0, vmax=1.0)
        for color in result:
            assert all(0.0 <= c <= 1.0 for c in color)

    def test_alpha_channel_is_one(self):
        result = normalize_colors([0.0, 0.5, 1.0], "viridis", vmin=0.0, vmax=1.0)
        for color in result:
            assert color[3] == pytest.approx(1.0)

    def test_different_values_produce_different_colors(self):
        result = normalize_colors([0.0, 1.0], "viridis", vmin=0.0, vmax=1.0)
        assert not np.allclose(result[0], result[1])

    # ── vmin / vmax / clip ────────────────────────────────────────────────────

    def test_vmin_vmax_shifts_color_range(self):
        # [0, 1] mapped with vmin/vmax=[0, 1] should equal [5, 6] with vmin/vmax=[5, 6].
        result_a = normalize_colors([0.0, 1.0], "plasma", vmin=0.0, vmax=1.0)
        result_b = normalize_colors([5.0, 6.0], "plasma", vmin=5.0, vmax=6.0)
        np.testing.assert_array_almost_equal(result_a, result_b)

    def test_clip_true_clamps_below_vmin(self):
        at_vmin = normalize_colors([0.0], "viridis", vmin=0.0, vmax=1.0)
        below_vmin = normalize_colors([-99.0], "viridis", vmin=0.0, vmax=1.0, clip=True)
        np.testing.assert_array_almost_equal(at_vmin, below_vmin)

    def test_clip_true_clamps_above_vmax(self):
        at_vmax = normalize_colors([1.0], "viridis", vmin=0.0, vmax=1.0)
        above_vmax = normalize_colors([99.0], "viridis", vmin=0.0, vmax=1.0, clip=True)
        np.testing.assert_array_almost_equal(at_vmax, above_vmax)

    # ── colormap ──────────────────────────────────────────────────────────────

    def test_colormap_object_matches_string(self):
        cmap_obj = plt.get_cmap("plasma")
        result_str = normalize_colors([0.0, 0.5, 1.0], "plasma", vmin=0.0, vmax=1.0)
        result_obj = normalize_colors([0.0, 0.5, 1.0], cmap_obj, vmin=0.0, vmax=1.0)
        np.testing.assert_array_almost_equal(result_str, result_obj)

    # ── string pass-through in mixed iterables ────────────────────────────────

    def test_mixed_iterable_strings_pass_through(self):
        result = normalize_colors(["red", 0.5, "blue"], "viridis", vmin=0.0, vmax=1.0)
        assert result[0] == "red"
        assert result[2] == "blue"
        assert len(result[1]) == 4  # numeric element mapped to RGBA

    # ── nan_color ─────────────────────────────────────────────────────────────

    def test_nan_renders_as_default_nan_color(self):
        result = normalize_colors([float("nan"), 0.5], "viridis", vmin=0.0, vmax=1.0)
        expected = mcolors.to_rgba("lightgray")
        np.testing.assert_array_almost_equal(result[0], expected)

    def test_nan_color_custom_is_applied(self):
        result = normalize_colors([float("nan")], "viridis", vmin=0.0, vmax=1.0, nan_color="red")
        expected = mcolors.to_rgba("red")
        np.testing.assert_array_almost_equal(result[0], expected)


# ── get_svg_regions ───────────────────────────────────────────────────────────

class TestGetSvgRegions:
    def test_returns_expected_region_ids(self):
        regions = get_svg_regions(SIMPLE_SVG)
        assert set(regions.keys()) == {"left", "right"}

    def test_each_region_contains_one_path(self):
        regions = get_svg_regions(SIMPLE_SVG)
        assert len(regions["left"]) == 1
        assert len(regions["right"]) == 1

    def test_x_coords_normalized_to_unit_interval(self):
        regions = get_svg_regions(SIMPLE_SVG)
        all_x = np.concatenate([
            p.vertices[:, 0]
            for paths in regions.values()
            for p in paths
        ])
        assert pytest.approx(all_x.min(), abs=1e-6) == 0.0
        assert pytest.approx(all_x.max(), abs=1e-6) == 1.0

    def test_duplicate_ids_collected_into_same_list(self):
        regions = get_svg_regions(DUPLICATE_ID_SVG)
        assert "region" in regions
        assert len(regions["region"]) == 2

    def test_path_without_id_is_skipped(self):
        regions = get_svg_regions(MISSING_ATTR_SVG)
        assert "named" in regions
        assert len(regions) == 1

    def test_path_without_d_attribute_is_skipped(self):
        regions = get_svg_regions(MISSING_ATTR_SVG)
        assert "no_path" not in regions

    def test_returns_matplotlib_path_objects(self):
        regions = get_svg_regions(SIMPLE_SVG)
        for paths in regions.values():
            for path in paths:
                assert isinstance(path, matplotlib.path.Path)

    def test_flip_y_true_differs_from_flip_y_false(self):
        regions_flip = get_svg_regions(SIMPLE_SVG, flip_y=True)
        regions_no_flip = get_svg_regions(SIMPLE_SVG, flip_y=False)
        y_flip = regions_flip["left"][0].vertices[:, 1]
        y_no_flip = regions_no_flip["left"][0].vertices[:, 1]
        assert not np.allclose(y_flip, y_no_flip)

    def test_flip_y_false_preserves_positive_y_ordering(self):
        # With flip_y=False and a rectangle above y=0, normalized y should be >= 0
        regions = get_svg_regions(SIMPLE_SVG, flip_y=False)
        all_y = np.concatenate([
            p.vertices[:, 1]
            for paths in regions.values()
            for p in paths
        ])
        assert np.all(all_y >= 0.0)

    def test_vertices_are_finite(self):
        regions = get_svg_regions(SIMPLE_SVG)
        for paths in regions.values():
            for path in paths:
                assert np.all(np.isfinite(path.vertices))
