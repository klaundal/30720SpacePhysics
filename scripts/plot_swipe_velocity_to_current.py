"""
Using SWIPE and AMPS, illustrate the v -> E (and Sigma) -> J -> dB at THL logic
"""

from datetime import datetime
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from apexpy import Apex
from polplot import Polarplot
from pyswipe import SWIPE

output_directory = Path(__file__).resolve().parents[1] / 'figures'
output_directory.mkdir(exist_ok=True)
plt.rcParams.update({'font.sans-serif': ['DejaVu Sans'], 'font.size': 12, 'svg.fonttype': 'none', 'text.usetex': False})

v_sw, by, bz, tilt, f107 = 400., 0., -5., 0., 100.
reference_date = datetime(2020, 3, 20, 12)
swipe = SWIPE(v_sw, by, bz, tilt, f107, minlat=60., height=110.)
vlat, vmlt = [coordinate.ravel() for coordinate in swipe.vectorgrid]
slat, smlt = [coordinate.ravel() for coordinate in swipe.scalargrid]
north, north_scalar = vlat > 0, slat > 0

ve1, ve2 = swipe.get_convection_vel_MA(times=np.full(vlat.size, np.datetime64(reference_date)), apex_refdate=reference_date)
E_east, E_north = [np.asarray(value).ravel() for value in swipe.get_efield_MA(return_emphi_emlambda=True)]
J_east, J_north = [np.asarray(value).ravel() for value in swipe.get_AMPS_current()]  # A/m
K_east, K_north = [np.asarray(value).ravel() / 1000 for value in swipe.amps.get_divergence_free_current(vlat, vmlt)]
_, sigma_p, inconsistent = swipe.get_conductances(slat, smlt)
sigma_p = np.ma.masked_where(np.asarray(inconsistent).ravel() | ~np.isfinite(np.asarray(sigma_p).ravel()), np.asarray(sigma_p).ravel())

# Circle at THL's QD latitude; arrows are QD horizontal ground perturbations.
apex = Apex(date=reference_date)
thl_lat, _ = apex.geo2qd(77.47, 290.773, 0.)
circle_mlt = np.linspace(0, 24, 241)
field_mlt  = np.arange(0, 24, 2.)
field_lat  = np.full(field_mlt.size, thl_lat)
B_east, B_north = swipe.amps.get_ground_perturbation(field_lat, field_mlt, height=0.)

fig, axes = plt.subplots(2, 2, figsize=(13, 12))
fig.subplots_adjust(left=0.04, right=0.94, bottom=0.07, top=0.94, hspace=0.24, wspace=0.18)
axes = axes.ravel()
polar_axes = [Polarplot(axis, minlat=60, plotgrid=False) for axis in axes]
for polar in polar_axes:
    polar.plotgrid(labels=False, color='0.65', linestyle=':')
    polar.writeLTlabels(size=12)
    polar.writeLATlabels(size=10)

# Common current scale in the last two panels.
vector_pairs = [(ve1, -ve2), (E_east, E_north), (J_east, J_north), (K_east, K_north)]
scales       = [5000, 300, 2, 2]
key_values   = [500, 20, 0.1, 0.1]
key_labels   = ['500 m/s', '20 mV/m', '0.1 A/m', '0.1 A/m']
for polar, (east, poleward), scale, key, label in zip(polar_axes, vector_pairs, scales, key_values, key_labels):
    polar.quiver(vlat[north], vmlt[north], poleward[north], east[north], color='black',
                 scale=scale, angles='xy', scale_units='xy', width=0.003,
                 qkeyproperties={'X': 0.15, 'Y': 0.0, 'U': key, 'label': label})

conductance = polar_axes[1].contourf(slat[north_scalar], smlt[north_scalar], sigma_p[north_scalar],
                                    levels=np.arange(0, 21, 2), cmap='YlOrRd', extend='max', zorder=-2)
colorbar_axis = axes[1].inset_axes([1.03, 0.27, 0.025, 0.46])
fig.colorbar(conductance, cax=colorbar_axis, ticks=[0, 10, 20], label=r'$\Sigma_P$ [S]')

polar_axes[3].plot(np.full(circle_mlt.size, thl_lat), circle_mlt, color='#7b3294', linewidth=1.4)
polar_axes[3].quiver(field_lat, field_mlt, B_north, B_east, color='#7b3294',
                     scale=250, angles='xy', scale_units='xy', width=0.005, zorder=5,
                     qkeyproperties={'X': 0.75, 'Y': 0.0, 'U': 50, 'label': '50 nT', 'labelcolor': '#7b3294'})

for axis, title in zip(axes, ['Convection velocity', 'Electric field and Pedersen conductance', 'Total current', 'Equivalent current']):
    axis.set_title(title, fontsize=16, pad=23)

for extension in ['png', 'pdf', 'svg']:
    fig.savefig(output_directory / f'swipe_velocity_to_current.{extension}', dpi=200, facecolor='white')
print(f'THL QD latitude: {thl_lat:.2f} degrees; maximum horizontal ground field: {np.max(np.hypot(B_east, B_north)):.1f} nT')
plt.show()
