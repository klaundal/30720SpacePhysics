"""
Illustration of magnetic forces
"""

from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

output_dir = Path(__file__).resolve().parents[1] / 'figures'
output_dir.mkdir(exist_ok=True)

plt.rcParams.update({'text.usetex': True, 'font.family': 'serif', 'font.size': 15,
                     'text.latex.preamble': r'\usepackage{amsmath}', 'svg.fonttype': 'none'})
field_color = '#252525'
force_color = '#c53c35'
tangent_color = '#246aa6'
fig, axes = plt.subplots(2, 1, figsize=(8, 10))
fig.subplots_adjust(left=0.06, right=0.94, top=0.94, bottom=0.01, hspace=0.21)

# Circular, equally spaced field lines: constant B, with inward curvature.
ax = axes[0]
theta = np.linspace(-1.05, 1.05, 400)
radii = [2.65, 3.05, 3.45]
for radius in radii:
    ax.plot(radius * np.cos(theta), radius * np.sin(theta), color=field_color, lw=2)
    angle0, angle1 = 0.63, 0.74
    ax.annotate('', xy=(radius * np.cos(angle1), radius * np.sin(angle1)),
                xytext=(radius * np.cos(angle0), radius * np.sin(angle0)),
                arrowprops={'arrowstyle': '-|>', 'color': field_color, 'lw': 2, 'mutation_scale': 15})

radius = radii[1]
ax.plot([0, radius], [0, 0], color='0.65', lw=1.2, ls=(0, (4, 4)), zorder=0)
ax.plot(0, 0, 'o', color='0.45', ms=4)
ax.text(0, -0.25, 'Centre of\ncurvature', ha='center', va='top', fontsize=12, color='0.35')
ax.text(0.95, 0.08, r'$R_c$', color='0.4', fontsize=19)
ax.plot(radius, 0, 'o', color=field_color, ms=6, zorder=5)
ax.annotate('', xy=(radius, 1.22), xytext=(radius, 0),
            arrowprops={'arrowstyle': '-|>', 'color': tangent_color, 'lw': 2.8, 'mutation_scale': 19})
ax.text(radius + 0.58, 0.88, r'$\hat{\mathbf{b}}$', color=tangent_color, fontsize=24)
ax.annotate('', xy=(1.45, 0), xytext=(radius, 0),
            arrowprops={'arrowstyle': '-|>', 'color': force_color, 'lw': 3.2, 'mutation_scale': 21})
ax.text(2.18, 0.2, r'$\boldsymbol{\kappa}$', ha='center', color=force_color, fontsize=25)
ax.text(2.25, -3.45, 'Tension pulls toward the inside of the bend', ha='center', fontsize=13)
ax.set(xlim=(-0.65, 4.3), ylim=(-3.7, 3.2))
ax.set_title('Magnetic tension / curvature force', fontsize=18, pad=16)
ax.set_aspect('equal')
ax.axis('off')

# Straight field with B increasing to the right. Equal-flux line spacing
# decreases to the right; B_y(x) has zero divergence and zero curvature.
ax = axes[1]
flux_coordinates = np.linspace(0, 1, 9)
x_positions = np.log1p(3.0 * flux_coordinates) / np.log(4.0) * 4.0
for x in x_positions:
    ax.plot([x, x], [-2.4, 2.4], color=field_color, lw=2)
    ax.annotate('', xy=(x, 1.65), xytext=(x, 1.25),
                arrowprops={'arrowstyle': '-|>', 'color': field_color, 'lw': 2, 'mutation_scale': 15})
ax.annotate('', xy=(0.4, 0), xytext=(2.6, 0),
            arrowprops={'arrowstyle': '-|>', 'color': force_color, 'lw': 3.2, 'mutation_scale': 21}, zorder=5)
ax.text(1.45, 0.3, 'Pressure force', ha='center', color=force_color, fontsize=15,
        bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 3})
ax.text(0, 2.65, 'Weaker B', ha='left', fontsize=12)
ax.text(4, 2.65, 'Stronger B', ha='right', fontsize=12)
ax.text(2, -3.45, 'Pressure pushes from stronger to weaker field', ha='center', fontsize=13)
ax.set(xlim=(-0.45, 4.45), ylim=(-3.7, 3.2))
ax.set_title('Magnetic pressure force', fontsize=18, pad=16)
ax.set_aspect('equal')
ax.axis('off')

for extension in ['png', 'svg', 'pdf']:
    path = output_dir / f'magnetic_forces.{extension}'
    fig.savefig(path, dpi=240, facecolor='white')
    print(path)
plt.close(fig)
