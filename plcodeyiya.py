
'''-----------------------------------------------------------------------'''
"""
pl_spectrum_plot.py

Photoluminescence spectrum plot (Wavelength vs Intensity), styled to
match a reference figure: dotted vertical gridlines at each x-axis
tick (with tick labels), NO tick marks or numbers on the y-axis,
full box border, and a legend box naming the sample.

Requirements:
    pip install numpy matplotlib pandas
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# ----------------------------------------------------------------------
# 1. Load data
# ----------------------------------------------------------------------
# Build the path relative to this script's own location, so it works
# regardless of the folder you run the script from.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, 'pl_spectrum_data.txt')

df = pd.read_csv(DATA_PATH, sep='\t')
df.columns = ['nm', 'intensity']

# Restrict to the display range shown in the reference figure.
# (Saturated detector readings, flagged as 9999.9, only occur outside
# this window -- ~389-405 nm and ~787-800 nm -- so no masking needed here.)
mask = (df['nm'] >= 500) & (df['nm'] <= 750)
wl = df.loc[mask, 'nm'].to_numpy()
intensity = df.loc[mask, 'intensity'].to_numpy()

# ----------------------------------------------------------------------
# 2. Style
# ----------------------------------------------------------------------
mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 18,          # 2x the original 9
    'axes.linewidth': 2.0,    # thicker border
})

fig, ax = plt.subplots(figsize=(6, 4.5), dpi=150)  # smaller so it renders reasonably in an IDE/notebook

ax.plot(wl, intensity, color='black', linewidth=2.0, label='HAp:Eu Scaffold')

# X-axis: ticks + labels + dotted vertical gridlines
ax.set_xlim(500, 750)
ax.set_xticks(np.arange(500, 751, 50))
ax.xaxis.grid(True, linestyle=':', color='black', linewidth=1.2, alpha=0.8)
ax.tick_params(axis='x', which='both', direction='out', length=6, width=2.0, labelsize=18)

# Y-axis: no tick marks, no tick labels, no horizontal gridlines
ax.set_yticks([])
ax.tick_params(axis='y', which='both', left=False, right=False)

# Full box border (all four spines visible)
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(2.0)

ax.set_xlabel('Wavelength (nm)', fontsize=18)
ax.set_ylabel('Intensity', fontsize=18)

ax.legend(loc='upper right', frameon=True, fontsize=18)

plt.tight_layout()
fig.savefig('pl_spectrum.png', dpi=200, bbox_inches='tight')
fig.savefig('pl_spectrum.pdf', bbox_inches='tight')

plt.show()