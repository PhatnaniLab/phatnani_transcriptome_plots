"""pha_plots — transcriptome visualisation utilities for PhatnaniLab."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__: str = version("pha-plots")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0.dev0"

__all__ = [
    "__version__",
    "draw_frontal_cortex",
    "draw_motor_cortex",
    "draw_spinal_cord"
]

from .spatial import (
    draw_frontal_cortex,
    draw_motor_cortex,
    draw_spinal_cord
)