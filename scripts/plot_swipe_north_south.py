"""
Compare northern and southern SWIPE potential and convection maps.
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

v_sw = 400.
b_y  = 5.
b_z  = 0.
tilt = 0.
f107 = 100.

swipe = SWIPE(v_sw, b_y, b_z, tilt, f107, minlat=60., height=110.)
vlat, vmlt = [coordinate.ravel() for coordinate in swipe.vectorgrid]
slat, smlt = [coordinate.ravel() for coordinate in swipe.scalargrid]
potential = swipe.get_potential().ravel()

# Fix the geographic mapping time and IGRF epoch for reproducibility.
reference_date = datetime(2020, 3, 20, 12)
reference_times = np.full(vlat.size, np.datetime64(reference_date))
v_e1, v_e2 = swipe.get_convection_vel_MA(times=reference_times, apex_refdate=reference_date)

limit = np.ceil(np.nanmax(np.abs(potential)) / 5) * 5
levels = np.linspace(-limit, limit, 21)
fig, axes = plt.subplots(1, 2, figsize=(14, 7))
fig.subplots_adjust(left=0.04, right=0.96, bottom=0.12, top=0.88, wspace=0.15)

quiver_scale = 5000  # Shared fixed scale for both hemispheres.

for axis, sign, title in zip(axes, [1, -1], ['Northern hemisphere', 'Southern hemisphere']):
    vectors = sign * vlat > 0
    scalars = sign * slat > 0
    polar = Polarplot(axis, minlat=60, plotgrid=False)
    polar.plotgrid(labels=False, color='0.65', linestyle=':')
    polar.writeLTlabels(size=13)
    polar.writeLATlabels(size=11)
    # Both hemispheres are viewed with the pole at the centre and noon at the top.
    filled = polar.contourf(np.abs(slat[scalars]), smlt[scalars], potential[scalars],
                            levels=levels, cmap='RdBu_r', extend='both', zorder=-2)
    # e2 is equatorward in either hemisphere: negate it for plot-poleward arrows.
    velocity_arrows = polar.quiver(np.abs(vlat[vectors]), vmlt[vectors], -v_e2[vectors], v_e1[vectors],
                 color='black', scale=quiver_scale, angles='xy', scale_units='xy', width=0.003)
    axis.set_title(title, fontsize=18, pad=24)

axes[-1].quiverkey(velocity_arrows, X=0.47, Y=0.045, U=500, label='500 m/s',
                  coordinates='figure', labelpos='E')

for extension in ['png', 'pdf', 'svg']:
    fig.savefig(output_directory / f'swipe_north_south_By5.{extension}', dpi=200, facecolor='white')
plt.show()
