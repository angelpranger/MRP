import matplotlib.pyplot as plt
import healpy as hp
import numpy as np
import h5py

import lightcone_io.healpix_maps as hm

# Lightcone base directory
basedir = "/net/hypernova/data2/FLAMINGO/L1000N1800/HYDRO_FIDUCIAL/lightcones_downsampled"

# Lightcone base name
basename = "lightcone0"

with h5py.File("/net/hypernova/data2/FLAMINGO/L1000N1800/HYDRO_FIDUCIAL/lightcones_downsampled/lightcone0_shells/shell_0/lightcone0.shell_0.0.hdf5","r") as lightcone:
    print(lightcone["DM"].attrs.keys())

# Which shell to plot
shell_nr = 0

# Which map to plot
map_name = "DM"

# Open the lightcone map set
shell = hm.ShellArray(basedir, basename)
# print(len(shell))
# print(list(shell[shell_nr]))

for shell_nr in range(10):
    print("Comoving inner radius = ", shell[shell_nr].comoving_inner_radius)
    print("Comoving outer radius = ", shell[shell_nr].comoving_outer_radius)

# Read the map
map = shell[shell_nr][map_name]
map_data = map[...]
# print(len(map_data))
# print(map_data)
# print(map.units)

# Plot the map
hp.mollview(map_data, norm="log")
plt.title(f"Lightcone Map: {map_name} (Shell {shell_nr})")
plt.savefig(f"lightcone_map_{shell_nr}.png")