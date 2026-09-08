"""
xrd_plot.py

XRD pattern plot (2-theta vs normalized intensity), styled to match a
reference figure (bold title, light gridlines on both axes, legend box)
while keeping the same font/line-weight conventions used in the other
scaffold plots (nature_style.py).

Requirements:
    pip install numpy pandas matplotlib
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# ----------------------------------------------------------------------
# 1. Load data
# ----------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_xrd(filename):
    path = os.path.join(SCRIPT_DIR, filename)
    df = pd.read_csv(path)
    df.columns = ['two_theta', 'intensity']
    return df['two_theta'].to_numpy(), df['intensity'].to_numpy()

two_theta, intensity = load_xrd('xrd_data.txt')

# Normalize intensity to 0-1 (as in the reference figure)
intensity_norm = intensity / intensity.max()

# ----------------------------------------------------------------------
# 2. Style
# ----------------------------------------------------------------------
mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 16,
    'axes.linewidth': 1.5,
})

fig, ax = plt.subplots(figsize=(7.5, 5.0), dpi=300)  # wider so the x-axis (2-theta) isn't squished

ax.plot(two_theta, intensity_norm, color='#3B6FB6', linewidth=1.3,
        label='Ball Milled Scaffold')

ax.set_xlim(20, 70)
ax.set_ylim(0, 1.05)
ax.set_xlabel(r'2$\theta$ ($\degree$)', fontsize=18)
ax.set_ylabel('Intensity (a.u.)', fontsize=18)
ax.set_title('Ball Milled Scaffold', fontsize=20, fontweight='bold')

# Light gridlines on both axes, box border, ticks inward-facing like reference
ax.grid(True, which='major', linestyle='-', linewidth=0.6, color='0.85')
ax.set_axisbelow(True)
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1.5)
ax.tick_params(direction='out', length=5, labelsize=16)

ax.legend(loc='upper right', frameon=True, fontsize=14)

plt.tight_layout()
fig.savefig(os.path.join(SCRIPT_DIR, 'xrd_plot.png'), dpi=300, bbox_inches='tight')
fig.savefig(os.path.join(SCRIPT_DIR, 'xrd_plot.pdf'), bbox_inches='tight')

plt.show()