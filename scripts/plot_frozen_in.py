"""
Illustrate flux freezing under a spatially varying transverse flow.

"""

from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

output_dir = Path(__file__).resolve().parents[1] / 'figures'
output_dir.mkdir(exist_ok=True)

plt.rcParams.update({'text.usetex': True, 'font.family': 'serif', 'font.size': 19,
                     'text.latex.preamble': r'\usepackage{amsmath}', 'svg.fonttype': 'none'})
field_color = '#252525'
plasma_color = '#246aa6'
velocity_color = '#c53c35'

delta_t = 1.0
field_a = np.array([-0.45, 0.0, 0.45])
y = np.linspace(-1.8, 1.8, 700)
marker_y = np.array([-1.45, -0.60, 0.0, 0.60, 1.45])
flow_half_width = 1.15
# A compact, smooth profile leaves both visible ends exactly stationary.
velocity_x = 1.05 * np.maximum(1 - (y / flow_half_width) ** 2, 0) ** 3
marker_vx = 1.05 * np.maximum(1 - (marker_y / flow_half_width) ** 2, 0) ** 3

fig, axes = plt.subplots(1, 2, figsize=(10, 5.8))
fig.subplots_adjust(left=0.04, right=0.98, top=0.86, bottom=0.08, wspace=0.35)

for ax, time in zip(axes, [0.0, delta_t]):
    for a in field_a:
        ax.plot(a + time * velocity_x, y, color=field_color, linewidth=2.4, zorder=2)
        arrow_y = np.array([1.48, 1.76])
        arrow_vx = 1.05 * np.maximum(1 - (arrow_y / flow_half_width) ** 2, 0) ** 3
        arrow_x = a + time * arrow_vx
        ax.annotate('', xy=(arrow_x[1], arrow_y[1]), xytext=(arrow_x[0], arrow_y[0]),
                    arrowprops={'arrowstyle': '-|>', 'color': field_color,
                                'lw': 2.4, 'mutation_scale': 16})

        # Mark the same five material elements on every field line.
        ax.plot(a + time * marker_vx, marker_y, 'o', color=plasma_color, markersize=6, zorder=5)

    if time == 0:
        for y0, vx in zip(marker_y, marker_vx):
            if vx == 0:
                continue
            ax.annotate('', xy=(field_a[-1] + vx, y0), xytext=(field_a[-1], y0),
                        arrowprops={'arrowstyle': '-|>', 'color': velocity_color,
                                    'lw': 2.3, 'mutation_scale': 16}, zorder=4)
        ax.text(0.95, 0.16, r'$\mathbf{v}(y)$', color=velocity_color, fontsize=22)
        ax.set_title(r'$t$', fontsize=26, pad=14)
    else:
        ax.set_title(r'$t+\Delta t$', fontsize=26, pad=14)

    ax.set(xlim=(-0.80, 1.90), ylim=(-1.95, 1.95))
    ax.set_aspect('equal')
    ax.axis('off')

transition = FancyArrowPatch((0.47, 0.48), (0.58, 0.48), transform=fig.transFigure,
                             arrowstyle='-|>', mutation_scale=22,
                             linewidth=2, color='#8796a3')
fig.add_artist(transition)
fig.text(0.525, 0.53, r'$\Delta t$', ha='center', color='#596976', fontsize=22)

for extension in ['png', 'svg', 'pdf']:
    path = output_dir / f'frozen_in.{extension}'
    fig.savefig(path, dpi=240, facecolor='white')
    print(path)
plt.close(fig)
