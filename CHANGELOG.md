# Changelog

All notable changes to this project will be documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-08

### Added

**Drawing functions**

- `draw_frontal_cortex` — draws a stylised 7-layer frontal cortex cross-section
  (layers I–VI with layer IV split) as a stack of quarter-circle arc polygons.
  Accepts per-layer numeric values mapped to colors via a colormap.
- `draw_motor_cortex` — draws a 6-layer agranular motor cortex cross-section
  (layers I–III, V–VI; no layer IV). Same interface as `draw_frontal_cortex`
  with geometry tuned for motor cortex.
- `draw_spinal_cord` — draws a spinal cord cross-section from a bundled SVG
  template. Accepts a `dict` mapping anatomical region IDs to numeric values.
  Bilateral regions (e.g. dorsal/ventral horns) are keyed by a single ID and
  rendered symmetrically.
- `draw_colorbar` — places a `matplotlib` colorbar as an inset axis at a
  user-specified bounding box in data coordinates `(x0, y0, width, height)`.
  Returns both the `Colorbar` and the inset `Axes` for further customisation.

All four functions are importable from the top-level `pha_plots` namespace.

**Significance annotations**

- All drawing functions accept `is_sig` to mark statistically significant
  layers or regions with an annotation character (default `*`).
- `sig_annotation_char` and `sig_annotation_kwargs` allow the character and
  text style to be customised per call.
- `SPINAL_SIG_LOCS` provides default annotation anchor points (in normalised
  SVG coordinates) for each named spinal cord region; callers can override or
  extend them via the `sig_locations` parameter of `draw_spinal_cord`.

**Color utilities (`pha_plots.utils`)**

- `normalize_colors` — maps numeric values to RGBA colors via a matplotlib
  colormap and `Normalize`. Handles `None` (returns `None`), bare color strings
  (pass-through), mixed iterables of numbers and strings, and NaN values
  (rendered as `nan_color`, default `'lightgray'`).
- `get_svg_regions` — parses an SVG string and returns a `dict` mapping each
  `id` attribute to a list of `matplotlib.path.Path` objects. Applies optional
  y-axis flip and normalises all paths so the x-axis spans `[0, 1]`.

**Package**

- Python 3.9–3.12 support.
- CI via GitHub Actions: linting (ruff), type-checking (mypy strict), and tests
  (pytest with coverage) on every push and pull request.
- Automated PyPI publishing via GitHub Actions trusted publishing (no API
  tokens required).
- Full type annotations and REST-format docstrings on all public symbols.
- Unit tests for `normalize_colors` and `get_svg_regions`.

[Unreleased]: https://github.com/PhatnaniLab/phatnani_transcriptome_plots/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/PhatnaniLab/phatnani_transcriptome_plots/releases/tag/v0.1.0
