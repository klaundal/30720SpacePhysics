"""
Illustrate IMF clock angle in the GSM y-z plane.
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch

output_directory = Path(__file__).resolve().parents[1] / 'figures'
output_directory.mkdir(exist_ok=True)

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14, 'svg.fonttype': 'none'})

clock_angle = 135.0  # degrees, measured from +Bz towards +By
length      = 1.05
by          = length * np.sin(np.deg2rad(clock_angle))
bz          = length * np.cos(np.deg2rad(clock_angle))
field_color = '#186787'
angle_color = '#bc591c'

fig, axis = plt.subplots(figsize=(8, 8), facecolor='white')
axis.set_aspect('equal')
axis.set_xlim(-1.38, 1.55)
axis.set_ylim(-1.48, 1.48)
axis.axis('off')

# Coordinate axes and reference directions.
axis.add_patch(FancyArrowPatch((-1.16, 0), (1.22, 0), arrowstyle='-|>', mutation_scale=15, color='0.3', linewidth=1.3))
axis.add_patch(FancyArrowPatch((0, -1.16), (0, 1.22), arrowstyle='-|>', mutation_scale=15, color='0.3', linewidth=1.3))
axis.text(1.26, 0.05, r'$+B_y$', ha='left', va='bottom')
axis.text(0.07, 1.22, r'$+B_z$', ha='left', va='center')
axis.text(-0.08, 1.04, '0°', ha='right', va='center', color='0.4')
axis.text(1.05, -0.08, '90°', ha='center', va='top', color='0.4')
axis.text(-0.08, -1.08, '180°', ha='right', va='center', color='0.4')
axis.text(-1.04, 0.08, '270°', ha='center', va='bottom', color='0.4')

# A projected IMF vector with positive By and negative Bz.
axis.plot([by, by], [0, bz], linestyle='--', color=field_color, alpha=0.45, linewidth=1.2)
axis.plot([0, by], [bz, bz], linestyle='--', color=field_color, alpha=0.45, linewidth=1.2)
axis.add_patch(FancyArrowPatch((0, 0), (by, bz), arrowstyle='-|>', mutation_scale=24, color=field_color, linewidth=3))
axis.text(by + 0.07, bz - 0.02, r'$\mathbf{B}_{\perp x}$', color=field_color, ha='left', va='center', fontsize=21)
axis.text(by / 2, bz - 0.08, r'$B_y > 0$', color=field_color, ha='center', va='top', fontsize=13)
axis.text(by + 0.06, bz / 2, r'$B_z < 0$', color=field_color, ha='left', va='center', fontsize=13)

# Clockwise angle from the positive vertical axis to the projected field.
radius = 0.48
axis.add_patch(Arc((0, 0), 2 * radius, 2 * radius, theta1=90 - clock_angle, theta2=90,
                   color=angle_color, linewidth=2))
end_angle = np.deg2rad(90 - clock_angle)
end       = radius * np.array([np.cos(end_angle), np.sin(end_angle)])
tangent   = np.array([np.sin(end_angle), -np.cos(end_angle)])
axis.add_patch(FancyArrowPatch(end - 0.045 * tangent, end, arrowstyle='->',
                              mutation_scale=16, color=angle_color, linewidth=2))
axis.text(0.55, 0.30, r'$\theta_c = 135^\circ$', color=angle_color, fontsize=19, ha='left')
axis.plot(0, 0, 'o', color='0.25', markersize=4)

axis.set_title('IMF clock angle\nGSM yz plane, seen from the Sun', fontsize=24)
axis.text(0.5, -0.025, r'$\theta_c = \operatorname{atan2}(B_y,\,B_z)$',
          transform=axis.transAxes, ha='center', va='top', fontsize=18)

fig.subplots_adjust(left=0.04, right=0.96, top=0.87, bottom=0.17)
for extension in ['png', 'pdf', 'svg']:
    fig.savefig(output_directory / f'imf_clock_angle.{extension}', dpi=220, facecolor='white')
plt.show()
