"""
Shared plotting configuration for NumPyro book sites.

Supports two modes:

  Script pipeline (build.py --py):
      setup_plotting("ch01")          # sets chapter prefix for save_fig
      save_fig("posterior_update")    # saves to PLOT_OUTPUT_DIR/ch01_posterior_update.png
      get_data_path("data.csv")      # returns DATA_DIR/data.csv

  Notebook pipeline (build.py --nb):
      setup_plotting()               # no prefix needed; plots display inline
      plt.show()                     # inline output in notebook
"""
import os
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# ── Script-pipeline state (chapter prefix + figure counter) ──────────────────
_chapter_prefix = ""
_fig_counter = 0


# ── Page-layout constants ────────────────────────────────────────────────────
# These tie the matplotlib figure size to the mkdocs-material page width so
# that matplotlib font sizes roughly match the rendered site font, and figures
# fill an appropriate fraction of the content area.
#
#   content_px  = PAGE_WIDTH_REM * 16           (= 1104 px)
#   figure_px   = content_px * FIGURE_FRAC      (= ~938 px)
#   figsize_w   = figure_px / DPI               (= ~9.4 in at 100 DPI)
#   font_pt     = SITE_FONT_PX * 72 / DPI       (= ~9.4 pt at 100 DPI)
#
# At 100 DPI with 10 pt font, rendered text is 10*100/72 ≈ 13.9 px — a good
# match for the ~13 px site body font (Inter @ 0.8 rem).

PAGE_WIDTH_REM = 69         # max-width set in custom.css
FIGURE_FRAC = 0.85          # fraction of content area for default figures
DPI = 100                   # screen-resolution DPI (sharp without bloat)
SITE_FONT_PX = 13           # approximate rendered site body font size

_content_px = PAGE_WIDTH_REM * 16
_figure_px = _content_px * FIGURE_FRAC         # ~938 px
_figsize_w = round(_figure_px / DPI, 1)        # ~9.4 in → 9.4
_figsize_h = round(_figsize_w * 0.55, 1)       # ~5.2 → golden-ish ratio
_font_pt = round(SITE_FONT_PX * 72 / DPI, 1)  # ~9.4 → use 10 for readability

FIGSIZE_DEFAULT = (_figsize_w, _figsize_h)      # (9.4, 5.2) — standard
FIGSIZE_WIDE = (round(_content_px * 0.98 / DPI, 1), 4.0)  # (~10.8, 4) — multi-panel side-by-side
FIGSIZE_TALL = (_figsize_w, round(_figsize_w * 0.75, 1))   # (9.4, 7.1)
FIGSIZE_SQUARE = (6.5, 6.5)
# Two-panel stacked (2 rows × 1 col): each subplot gets full content width so
# font sizes match single-axis FIGSIZE_DEFAULT plots exactly.
FIGSIZE_2PANEL = (_figsize_w, round(_figsize_h * 1.85, 1))  # (9.4, 9.6)
FONT_SIZE = 10              # slightly above calculated 9.4 for readability


# ── Color palette ───────────────────────────────────────────────────────────
# Dark mode colors (brighter for contrast on dark background) — the default
COLORS = {
    "purple": "#BB86FC",
    "orange": "#FFB347",
    "blue": "#64B5F6",
    "green": "#81C784",
    "red": "#EF5350",
    "pink": "#F48FB1",
    "light_orange": "#FFE0B2",
    "light_blue": "#BBDEFB",
    "light_green": "#C8E6C9",
    "light_purple": "#E1BEE7",
    "grey": "#BDBDBD",
}

PALETTE = list(COLORS.values())

# Convenient shorthand
C = COLORS


# ── Colormap management ──────────────────────────────────────────────────────
def get_cmap(name: str = "viridis"):
    """
    Get a dark-mode-friendly colormap.

    Maps commonly dark-unfriendly cmaps to better alternatives:
      - Sequential (Blues, Greens, Reds) → plasma/inferno
      - Diverging (RdBu, coolwarm) → RdYlGn
      - Default: viridis → plasma
    """
    dark_alternatives = {
        "viridis": "plasma",
        "Blues": "plasma",
        "Greens": "inferno",
        "Reds": "inferno",
        "Purples": "plasma",
        "Oranges": "inferno",
        "RdBu": "RdYlGn",
        "RdBu_r": "RdYlGn_r",
        "coolwarm": "RdYlGn",
        "bwr": "RdYlGn",
        "bone": "plasma",
        "gray": "plasma",
    }
    return dark_alternatives.get(name, name)


# ── Setup ────────────────────────────────────────────────────────────────────
def setup_plotting(chapter_prefix_or_style: str = "dark_background"):
    """
    Initialize matplotlib with dark mode web-optimized defaults.

    Accepts either:
      - A chapter prefix like "ch01" (script pipeline) — sets up save_fig state
      - A matplotlib style name like "dark_background" (notebook pipeline)

    If the argument looks like a chapter prefix (starts with "ch" followed by
    digits), it is treated as a prefix and dark_background is used as the style.
    """
    global _chapter_prefix, _fig_counter

    # Detect whether this is a chapter prefix or a style name
    arg = chapter_prefix_or_style
    if arg and len(arg) >= 4 and arg[:2] == "ch" and arg[2:4].isdigit():
        # Script-pipeline mode: "ch01", "ch14", etc.
        _chapter_prefix = arg
        _fig_counter = 0
        style = "dark_background"
    else:
        # Notebook-pipeline mode: use arg as style directly
        _chapter_prefix = ""
        _fig_counter = 0
        style = arg

    plt.style.use(style)

    bg_color = "#1e1e1e"
    text_color = "#e0e0e0"

    custom = {
        # ── Figure size / layout ──
        # Calculated from page width: figures fill ~85% of 69 rem content area
        # at 100 DPI so that 10 pt matplotlib font ≈ 13–14 px ≈ site body font.
        "figure.figsize": FIGSIZE_DEFAULT,
        "figure.dpi": DPI,
        "figure.facecolor": bg_color,
        "figure.autolayout": True,           # apply tight_layout automatically
        "savefig.dpi": DPI,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.15,
        "savefig.facecolor": bg_color,

        # ── Font (sized to match site body text when rendered) ──
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
        "font.size": FONT_SIZE,
        "axes.titlesize": FONT_SIZE + 2,
        "axes.titleweight": "bold",
        "axes.labelsize": FONT_SIZE,
        "xtick.labelsize": FONT_SIZE - 1,
        "ytick.labelsize": FONT_SIZE - 1,
        "legend.fontsize": FONT_SIZE - 1,

        # ── Colors ──
        "axes.prop_cycle": mpl.cycler(color=PALETTE),
        "text.color": text_color,
        "axes.labelcolor": text_color,
        "xtick.color": text_color,
        "ytick.color": text_color,

        # ── Grid ──
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linewidth": 0.5,
        "grid.linestyle": "--",

        # ── Lines / markers ──
        "lines.linewidth": 2.0,
        "lines.marker": "",                  # no markers by default (use '-')
        "lines.markersize": 5,               # if markers are added, keep small

        # ── Axes ──
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 1.0,
        "axes.facecolor": bg_color,

        # ── Legend ──
        "legend.framealpha": 0.9,
        "legend.edgecolor": "0.3",
        "legend.borderpad": 0.4,
        "legend.facecolor": bg_color,

        # ── Colormap ──
        "image.cmap": "plasma",
    }
    mpl.rcParams.update(custom)


# ── Figsize helpers ──────────────────────────────────────────────────────────
def figsize_wide():
    """Wider figsize for multi-panel plots (e.g., 1×2 or 1×3 subplots)."""
    return FIGSIZE_WIDE


def figsize_tall():
    """Taller figsize for vertically-stacked plots."""
    return FIGSIZE_TALL


def figsize_square():
    """Square figsize for scatter plots, heatmaps, etc."""
    return FIGSIZE_SQUARE


# ── Helper functions ─────────────────────────────────────────────────────────
def plot_posterior(samples, param_name="θ", ax=None, color=None, hdi_prob=0.89,
                   show_mean=True, show_hdi=True, title=None):
    """
    Plot a posterior distribution with HDI shading.

    Args:
        samples: 1-D array of posterior samples
        param_name: label for the parameter
        ax: matplotlib axes (creates new if None)
        color: line/fill color
        hdi_prob: HDI probability mass (default 0.89)
        show_mean: whether to show vertical mean line
        show_hdi: whether to shade the HDI region
        title: optional title override
    """
    import arviz as az

    if ax is None:
        fig, ax = plt.subplots()
    if color is None:
        color = C["purple"]

    samples = np.asarray(samples).flatten()

    az.plot_kde(samples, ax=ax, plot_kwargs={"color": color, "linewidth": 2.5})

    if show_hdi:
        hdi = az.hdi(samples, hdi_prob=hdi_prob)
        ymax = ax.get_ylim()[1]
        ax.fill_between(
            np.linspace(hdi[0], hdi[1], 100),
            0, ymax * 0.05,
            alpha=0.4, color=color,
            label=f"{int(hdi_prob*100)}% HDI [{hdi[0]:.2f}, {hdi[1]:.2f}]"
        )

    if show_mean:
        mean_val = np.mean(samples)
        ax.axvline(mean_val, color=color, linestyle="--", alpha=0.6,
                   label=f"Mean = {mean_val:.3f}")

    ax.set_xlabel(param_name)
    ax.set_ylabel("Density")
    ax.set_title(title or f"Posterior: {param_name}")
    ax.legend()
    return ax


def plot_trace(samples, param_names=None, figsize=None):
    """
    Plot trace plots for MCMC samples.

    Args:
        samples: dict of {param_name: array} or arviz InferenceData
        param_names: subset of parameters to plot
        figsize: override figure size
    """
    import arviz as az

    if isinstance(samples, dict):
        data = az.from_dict(posterior={k: np.atleast_2d(v) for k, v in samples.items()})
    else:
        data = samples

    if param_names:
        az.plot_trace(data, var_names=param_names, figsize=figsize or figsize_wide())
    else:
        az.plot_trace(data, figsize=figsize or figsize_wide())

    return plt.gcf()


def annotate_point(ax, x, y, text, color=None, fontsize=None):
    """Add an annotated point with an arrow."""
    if color is None:
        color = C["red"]
    if fontsize is None:
        fontsize = FONT_SIZE
    ax.annotate(
        text, (x, y),
        textcoords="offset points", xytext=(15, 15),
        fontsize=fontsize, color=color,
        arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
    )


# ── Script-pipeline functions ────────────────────────────────────────────────
# These are used by the old build.py → scripts pipeline.
# Notebooks don't need them (plots display inline via plt.show()).

def save_fig(name: str):
    """
    Save the current figure to PLOT_OUTPUT_DIR/{prefix}_{name}.png.

    Only meaningful in the script pipeline where PLOT_OUTPUT_DIR is set.
    In notebooks this is a no-op (prints a note instead).
    """
    global _fig_counter
    _fig_counter += 1

    plot_dir = os.environ.get("PLOT_OUTPUT_DIR")
    if not plot_dir:
        # Notebook mode or no output dir set — skip silently
        return

    out = Path(plot_dir)
    out.mkdir(parents=True, exist_ok=True)

    if _chapter_prefix:
        filename = f"{_chapter_prefix}_{name}.png"
    else:
        filename = f"{name}.png"

    filepath = out / filename
    plt.savefig(filepath)
    plt.close()
    print(f"  Saved: {filename}")


def get_data_path(filename: str) -> str:
    """
    Return the full path to a data file.

    Uses DATA_DIR env var if set (both pipelines set it),
    otherwise falls back to a relative path.
    """
    data_dir = os.environ.get("DATA_DIR")
    if data_dir:
        return str(Path(data_dir) / filename)
    # Fallback: try relative to this file
    return str(Path(__file__).parent.parent / "data" / filename)
