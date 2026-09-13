import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import ppigrf
from datetime import datetime

# Grid
lon  =  np.linspace(-180, 180, 361)
lat  =  np.linspace(-89.5, 89.5, 180)
lon, lat  =  np.meshgrid(lon, lat)

theta  = 90 - lat
date  = datetime(2025, 1, 1)

# Radii [km]
RE = 6371.2
r_geo = 42164.0

# IGRF radial field [nT]
Br_surface = ppigrf.igrf_gc(RE, theta, lon, date)[0][0]
Br_geo     = ppigrf.igrf_gc(r_geo, theta, lon, date)[0][0]

# Plot
fig, axes = plt.subplots(2, 1, figsize = (12, 12), subplot_kw = {'projection': ccrs.Robinson()} )

levels_surface = np.linspace(-70000, 70000, 15)
levels_geo     = np.linspace(-220, 220, 23)

for ax, Br, levels, title in zip(axes, [Br_surface, Br_geo], [levels_surface, levels_geo], [r'Earth surface ($r  =  1\,R_E$)', r'Geostationary orbit ($r  =  6.62\,R_E$), projected to Earth']):
    im = ax.contourf(lon, lat, Br, levels = levels, cmap = 'bwr', extend = 'both', transform = ccrs.PlateCarree())
    ax.coastlines(linewidth = 0.7)
    ax.set_global()
    ax.set_title(title)

    cb = fig.colorbar(im, ax = ax, orientation = 'horizontal', pad = 0.05, shrink = 0.9, aspect = 45, ) 
    cb.set_label(r'$B_r$ [nT]')

fig.suptitle(r'IGRF-14 (2025.0): radial magnetic field $B_r$', fontsize = 16)

plt.tight_layout()
plt.show()