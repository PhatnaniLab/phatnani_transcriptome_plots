# pha-plots

Transcriptome visualisation utilities for PhatnaniLab.

[![CI](https://github.com/PhatnaniLab/phatnani_transcriptome_plots/actions/workflows/ci.yml/badge.svg)](https://github.com/PhatnaniLab/phatnani_transcriptome_plots/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/pha-plots.svg)](https://pypi.org/project/pha-plots/)
[![Python versions](https://img.shields.io/pypi/pyversions/pha-plots.svg)](https://pypi.org/project/pha-plots/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Installation

```bash
pip install pha-plots
```

Install with optional development dependencies:

```bash
pip install "pha-plots[dev]"
```

## Usage

### Cortical slices

`draw_frontal_cortex` and `draw_motor_cortex` each accept a list of per-layer
numeric values (outermost layer first), a colormap, and optional normalization
bounds.  Frontal cortex uses 7 layers (I–VI with layer IV split); motor cortex
uses 6 (agranular — no layer IV).

```python
import matplotlib.pyplot as plt
from pha_plots import draw_frontal_cortex, draw_motor_cortex

fig, (ax_f, ax_m) = plt.subplots(1, 2, figsize=(4, 3))

draw_frontal_cortex(
    ax_f,
    values=[0.1, 0.4, 0.8, 0.3, 0.6, 0.9, 0.5],  # 7 layers
    cmap="viridis",
    vmin=0, vmax=1,
)

draw_motor_cortex(
    ax_m,
    values=[0.2, 0.5, 0.7, 0.4, 0.8, 0.6],  # 6 layers
    cmap="viridis",
    vmin=0, vmax=1,
)

for ax in (ax_f, ax_m):
    ax.set_aspect("equal")
    ax.autoscale()
    ax.axis("off")
```

Pass `is_sig` (a list of booleans, one per layer) to mark significant layers
with an annotation character:

```python
draw_frontal_cortex(
    ax, values, "viridis", vmin=0, vmax=1,
    is_sig=[False, False, True, False, True, False, False],
    sig_annotation_char="*",
)
```

### Spinal cord cross-section

`draw_spinal_cord` accepts a dictionary mapping anatomical region IDs to
values.  Any region absent from the dictionary is filled with `nan_color`
(default `'lightgray'`).

Recognized region IDs (matching the embedded SVG):

| ID | Anatomy |
|----|---------|
| `Dors_Edge` | Dorsal edge |
| `Lat_Edge` | Lateral edge (bilateral) |
| `Vent_Edge` | Ventral edge |
| `Dors_Med_White` | Dorsal median white matter |
| `Med_Lat_White` | Medial–lateral white matter (bilateral) |
| `Vent_Lat_White` | Ventral lateral white matter (bilateral) |
| `Vent_Med_White` | Ventral median white matter |
| `Dors_Horn` | Dorsal horn (bilateral) |
| `Vent_Horn` | Ventral horn (bilateral) |
| `Med_Grey` | Medial grey matter |
| `Cent_Can` | Central canal |

```python
from pha_plots import draw_spinal_cord

fig, ax = plt.subplots(figsize=(3, 3))

draw_spinal_cord(
    ax,
    values={
        "Dors_Horn":      0.9,
        "Vent_Horn":      0.7,
        "Med_Grey":       0.4,
        "Dors_Med_White": 0.2,
        "Vent_Med_White": 0.3,
    },
    cmap="plasma",
    vmin=0, vmax=1,
)

ax.set_aspect("equal")
ax.autoscale()
ax.axis("off")
```

Significance annotations use the same `is_sig` / `sig_annotation_char`
pattern, but `is_sig` is a `dict[str, bool]` keyed by region ID:

```python
draw_spinal_cord(
    ax, values, "plasma", vmin=0, vmax=1,
    is_sig={"Dors_Horn": True, "Vent_Horn": False},
)
```

### Colorbar

`draw_colorbar` creates a colorbar inset directly inside an existing axis at a
bounding box given in data coordinates `(x0, y0, width, height)`, so it moves
and scales with the plot.

```python
from pha_plots.utils import draw_colorbar

cbar, cax = draw_colorbar(
    ax,
    xycoords=(x_max + 0.02, y_min, 0.04, y_max - y_min),
    cmap="viridis",
    vmin=0, vmax=1,
    orientation="vertical",
    label="Expression (normalised)",
)
```

`cbar` is the `matplotlib.colorbar.Colorbar` instance; `cax` is the inset
`Axes` on which it was drawn.  Both are returned so tick positions, labels, and
other properties can be adjusted after the call:

```python
cbar.set_ticks([0, 0.5, 1])
cax.yaxis.set_tick_params(labelsize=6)
```

### Combining all four

```python
import matplotlib.pyplot as plt
from pha_plots import draw_frontal_cortex, draw_motor_cortex, draw_spinal_cord
from pha_plots.utils import draw_colorbar

CMAP, VMIN, VMAX = "viridis", 0.0, 1.0

fig, axes = plt.subplots(1, 3, figsize=(8, 3))

draw_frontal_cortex(
    axes[0],
    values=[0.1, 0.4, 0.8, 0.3, 0.6, 0.9, 0.5],
    cmap=CMAP, vmin=VMIN, vmax=VMAX,
)
draw_motor_cortex(
    axes[1],
    values=[0.2, 0.5, 0.7, 0.4, 0.8, 0.6],
    cmap=CMAP, vmin=VMIN, vmax=VMAX,
)
draw_spinal_cord(
    axes[2],
    values={"Dors_Horn": 0.9, "Vent_Horn": 0.7, "Med_Grey": 0.4},
    cmap=CMAP, vmin=VMIN, vmax=VMAX,
)

for ax in axes:
    ax.set_aspect("equal")
    ax.autoscale()
    ax.axis("off")

# Add a shared colorbar just outside the spinal cord panel.
x0, x1 = axes[2].get_xlim()
y0, y1 = axes[2].get_ylim()
draw_colorbar(
    axes[2],
    xycoords=(x1 + 0.02 * (x1 - x0), y0, 0.04 * (x1 - x0), y1 - y0),
    cmap=CMAP, vmin=VMIN, vmax=VMAX,
    label="Expression",
)

plt.tight_layout()
plt.savefig("expression_figure.pdf", bbox_inches="tight")
```

## Development setup

```bash
git clone https://github.com/PhatnaniLab/phatnani_transcriptome_plots.git
cd phatnani_transcriptome_plots
pip install -e ".[dev]"
pytest
```

## Releasing

1. Create and push a git tag matching `v*` (e.g. `v0.1.0`).
2. Draft a GitHub Release from that tag.
3. The [publish workflow](.github/workflows/publish.yml) builds the
   distribution, pushes to TestPyPI, then promotes to PyPI automatically.

> **Trusted publishing** — configure an OIDC publisher for `pha-plots` on
> PyPI/TestPyPI (no API tokens needed). See the
> [PyPA guide](https://docs.pypi.org/trusted-publishers/).

## License

MIT — see [LICENSE](LICENSE).
