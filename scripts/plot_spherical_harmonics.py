""" Plot the real cosine spherical harmonics through degree 4 """

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from ppigrf.ppigrf import get_legendre

repository_directory = Path(__file__).resolve().parent.parent
default_output       = repository_directory / 'figures' / 'spherical_harmonics_n1_n4.png'

degrees_orders = [(degree, order) for degree in range(1, 5) for order in range(degree + 1)]

longitude_degrees = np.linspace(-180, 180, 721)
latitude_degrees  = np.linspace(-90 ,  90, 361)
colatitude_degrees = 90 - latitude_degrees

longitude = np.radians(longitude_degrees)
latitude  = np.radians(latitude_degrees)

P, _ = get_legendre(colatitude_degrees, degrees_orders)

figure = plt.figure(figsize=(13, 9), layout='constrained')
grid   = figure.add_gridspec(5, 6, width_ratios=(0.22, 1, 1, 1, 1, 1), height_ratios=(1, 1, 1, 1, 0.16))
axes   = []

for order in range(5):
    label_axis = figure.add_subplot(grid[4, order + 1])
    label_axis.axis('off')
    label_axis.text(0.5, 0.65, rf'$m={order}$', ha = 'center', va = 'center', fontsize = 15)

for degree in range(1, 5):
    label_axis = figure.add_subplot(grid[degree - 1, 0])
    label_axis.axis('off')
    label_axis.text(0.5, 0.5, rf'$n={degree}$', ha = 'center', va = 'center', rotation = 90, fontsize = 15)

for column, (degree, order) in enumerate(degrees_orders):
    axis = figure.add_subplot(grid[degree - 1, order + 1], projection = 'mollweide')
    
    legendre_function = P[:, column, np.newaxis]
    longitude_function = np.cos(order * longitude)[np.newaxis, :]
    spherical_harmonic = legendre_function * longitude_function

    image = axis.pcolormesh(longitude, latitude, spherical_harmonic, cmap = 'RdBu_r', vmin = -1, vmax = 1, shading = 'auto', rasterized = True)

    axis.grid(color = '0.45', linewidth = 0.35, alpha = 0.55)
    axis.set_xticklabels([])
    axis.set_yticklabels([])
    axes.append(axis)

figure.suptitle(r'Schmidt semi-normalized cosine spherical harmonics ' r'$P_n^m(\cos\theta)\cos(m\phi)$', fontsize=20)

colorbar_grid = grid[0:2, 4:6].subgridspec(1, 3, width_ratios = (1.2, 0.12, 0.35))
colorbar_axis = figure.add_subplot(colorbar_grid[0, 1])
colorbar      = figure.colorbar(image, cax=colorbar_axis, orientation = 'vertical')
colorbar.set_label('Harmonic amplitude', fontsize=12)

plt.show()
