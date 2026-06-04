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
