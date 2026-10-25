"""
Northern SWIPE potential and convection for northward IMF and contrasting By.
"""

from datetime import datetime
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from polplot import Polarplot
from pyswipe import SWIPE

output_directory = Path(__file__).resolve().parents[1] / 'figures'
output_directory.mkdir(exist_ok=True)
plt.rcParams.update({'font.sans-serif': ['DejaVu Sans'], 'font.size': 12, 'svg.fonttype': 'none'})

v_sw     = 400.
b_y_cases = [-5., 0., 5.]
b_z      = 5.
tilt     = 0.
f107     = 100.
quiver_scale = 5000  # Fixed and identical in all three panels.
reference_date = datetime(2020, 3, 20, 12)

# Calculate every case before choosing a common potential colour scale.
cases = []
for b_y in b_y_cases:
    swipe = SWIPE(v_sw, b_y, b_z, tilt, f107, minlat=60., height=110.)
    vlat, vmlt = [coordinate.ravel() for coordinate in swipe.vectorgrid]
    slat, smlt = [coordinate.ravel() for coordinate in swipe.scalargrid]
    potential = swipe.get_potential().ravel()
    reference_times = np.full(vlat.size, np.datetime64(reference_date))
    v_e1, v_e2 = swipe.get_convection_vel_MA(times=reference_times, apex_refdate=reference_date)
    north, north_scalar = vlat > 0, slat > 0
    cases.append({'By': b_y, 'vlat': vlat[north], 'vmlt': vmlt[north],
                  'slat': slat[north_scalar], 'smlt': smlt[north_scalar],
                  'potential': potential[north_scalar], 'v_e': v_e1[north], 'v_poleward': -v_e2[north]})

limit = max(5., np.ceil(max(np.nanmax(np.abs(case['potential'])) for case in cases) / 5) * 5)
levels = np.linspace(-limit, limit, 21)
fig, axes = plt.subplots(1, 3, figsize=(19, 6.8))
fig.subplots_adjust(left=0.03, right=0.97, bottom=0.13, top=0.85, wspace=0.17)

for axis, case in zip(axes, cases):
    polar = Polarplot(axis, minlat=60, plotgrid=False)
    polar.plotgrid(labels=False, color='0.65', linestyle=':')
    polar.writeLTlabels(size=13)
    polar.writeLATlabels(size=11)
    polar.contourf(case['slat'], case['smlt'], case['potential'], levels=levels,
                   cmap='RdBu_r', extend='both', zorder=-2)
    velocity_arrows = polar.quiver(case['vlat'], case['vmlt'], case['v_poleward'], case['v_e'],
                                   color='black', scale=quiver_scale, angles='xy', scale_units='xy', width=0.003)
    axis.set_title(rf"$B_y={case['By']:+g}$ nT, $B_z=+{b_z:g}$ nT", fontsize=18, pad=24)

axes[-1].quiverkey(velocity_arrows, X=0.47, Y=0.055, U=500, label='500 m/s',
                  coordinates='figure', labelpos='E')
for extension in ['png', 'pdf', 'svg']:
    fig.savefig(output_directory / f'swipe_northward_imf.{extension}', dpi=200, facecolor='white')
plt.show()
