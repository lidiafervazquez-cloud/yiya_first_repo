r"""
nature_style.py

Reusable matplotlib styling + plotting helpers for Nature-journal-style
figures: clean sans-serif font, thin closed-box axes with inward ticks,
muted pastel color palette, and bar charts with capped error bars.

Usage
-----
    from nature_style import apply_nature_style, NATURE_COLORS, bar_with_error, save_figure

    apply_nature_style()
    fig, ax = plt.subplots(figsize=(3.3, 2.3), dpi=300)
    bar_with_error(ax, labels, means, sds)
    ax.set_xlabel('Scaffolds')
    ax.set_ylabel(r'Pore Size ($\mu$m)')
    save_figure(fig, 'pore_size_bar_chart')

Requirements:
    pip install numpy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ----------------------------------------------------------------------
# Palette
# ----------------------------------------------------------------------
NATURE_COLORS = ['#9BB3D4', '#F2A2A2', '#A8D5BA', '#C9AEDC', '#A0CFCF']


# ----------------------------------------------------------------------
# Style
# ----------------------------------------------------------------------
def apply_nature_style():
    """Apply Nature-journal-style rcParams globally. Call once, before plotting."""
    mpl.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'font.size': 8,
        'axes.linewidth': 0.8,
        'axes.labelsize': 9,
        'axes.titlesize': 9,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'xtick.major.width': 0.8,
        'ytick.major.width': 0.8,
        'xtick.major.size': 3,
        'ytick.major.size': 3,
        'legend.fontsize': 8,
        'svg.fonttype': 'none',   # keep text editable if exported as SVG
        'pdf.fonttype': 42,       # embed fonts as text, not curves
    })


def style_axes(ax):
    """Apply closed-box spines + inward ticks to a single Axes object."""
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.8)
    ax.tick_params(direction='in', top=False, right=False)


# ----------------------------------------------------------------------
# Stats helper
# ----------------------------------------------------------------------
def group_stats(groups: dict):
    """
    groups: dict mapping label -> list/array of raw values.
    Returns (labels, means, sds) as lists, in the dict's insertion order.
    """
    labels = list(groups.keys())
    means = [np.mean(groups[k]) for k in labels]
    sds = [np.std(groups[k], ddof=1) for k in labels]
    return labels, means, sds


# ----------------------------------------------------------------------
# Core plotting function
# ----------------------------------------------------------------------
def bar_with_error(ax, labels, means, sds, colors=None, width=0.6,
                    ylim_pad=1.15, ylim_zero=True):
    """
    Draw a Nature-style bar chart with SD error bars (capped) on `ax`.

    Parameters
    ----------
    ax : matplotlib Axes
    labels : list of str        - x tick labels (group names)
    means : list of float       - bar heights
    sds : list of float          - error bar sizes
    colors : list of str, optional - defaults to NATURE_COLORS, cycled if needed
    width : float                - bar width
    ylim_pad : float             - multiplier applied to (max mean+sd) for headroom
    ylim_zero : bool             - if True, y-axis starts at 0

    Returns
    -------
    bars : the BarContainer returned by ax.bar
    """
    x = np.arange(len(labels))
    if colors is None:
        colors = [NATURE_COLORS[i % len(NATURE_COLORS)] for i in range(len(labels))]

    bars = ax.bar(
        x, means,
        yerr=sds,
        capsize=3,
        color=colors,
        width=width,
        error_kw={'elinewidth': 0.8, 'capthick': 0.8}
    )

    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    style_axes(ax)

    top = max(m + s for m, s in zip(means, sds)) * ylim_pad
    ax.set_ylim(0 if ylim_zero else None, top)

    return bars


# ----------------------------------------------------------------------
# Save helper
# ----------------------------------------------------------------------
def save_figure(fig, basename, png_dpi=600, formats=('png', 'pdf')):
    """
    Save a figure as PNG (high-res, for viewing/slides) and/or PDF
    (vector, for journal submission). basename should have no extension.
    """
    if 'png' in formats:
        fig.savefig(f'{basename}.png', dpi=png_dpi, bbox_inches='tight')
    if 'pdf' in formats:
        fig.savefig(f'{basename}.pdf', bbox_inches='tight')


# ----------------------------------------------------------------------
# Example usage (runs only if this file is executed directly)
# ----------------------------------------------------------------------
if __name__ == '__main__':
    apply_nature_style()

    # --- toy data, replace with your own groups dict ---
    rng = np.random.default_rng(0)
    groups = {
        'N1': rng.normal(18, 3, 300),
        'N4': rng.normal(19, 2, 300),
        'N5': rng.normal(16, 4, 300),
    }

    labels, means, sds = group_stats(groups)

    fig, ax = plt.subplots(figsize=(3.3, 2.3), dpi=300)
    bar_with_error(ax, labels, means, sds)
    ax.set_xlabel('Scaffolds')
    ax.set_ylabel(r'Pore Size ($\mu$m)')
    plt.tight_layout()

    save_figure(fig, 'example_bar_chart')
    plt.show()
    