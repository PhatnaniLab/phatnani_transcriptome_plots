import matplotlib.pyplot as plt
import matplotlib.colors


def normalize_colors(x, cmap, vmin=None, vmax=None, clip=True):
    _norm = matplotlib.colors.Normalize(
        vmin=vmin,
        vmax=vmax,
        clip=clip
    )

    return plt.get_cmap(cmap)(_norm(x))
