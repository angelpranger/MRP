import numpy as np
import h5py
import healpy as hp
import matplotlib.pyplot as plt
import unyt as u
import lightcone_io.healpix_maps as hm

# Lightcone base directory
basedir = "/net/hypernova/data2/FLAMINGO/"

# Simulation
simulation = "L1000N1800/HYDRO_FIDUCIAL/lightcones_downsampled_4096"

# Lightcone base name
basename = "lightcone0"

# Open the lightcone map set
shells = hm.ShellArray(basedir + simulation, basename)

z = 0.1  # Redshift for the shell

def Last_shell(z):
    """
    Function to get the last shell number for a given redshift z.
    The function assumes that shells are spaced at 0.05 redshift intervals up to z=3,
    and at 0.25 intervals from z=3 to z=5.
    """
    if (0.05 <= z <= 3):
        return int(z / 0.05 - 1) # As shells are spaced at 0.05 redshift intervals
    elif (3 < z <= 5):
        # After z=3, shells are spaced at 0.25 intervals
        return int(60 + (z - 3) / 0.25 - 1) # After z=3, shells are spaced at 0.25 intervals
    else:
        raise ValueError("Redshift out of range. Valid range is 0.05 <= z <= 5.")
    
# Get the last shell number for the given redshift
last_shell = Last_shell(z)

# print(shells[0:3].comoving_inner_radius) werkt niet, moet een enkele shell kiezen voordat je de comoving radii kunt opvragen

print(z, last_shell)

#total_map = np.zeros_like(shells[0]["DM"][...]).to(u.pc/u.cm**3) # Initialize the total map in pc cm^-3
total_map = shells[0]["DM"][...] * 3e-19 
for shell_nr in range(0, last_shell + 1):
    #map = shells[shell_nr]["DM"][...].to(u.pc/u.cm**3) # Convert the map to pc cm^-3
    map = shells[shell_nr]["DM"][...] *3e-19
    # TODO: Randomly rotate the map
    # Add the map to the total map
    print(map)
    total_map += map

print(total_map)
print(type(total_map))

# Plot the total map

# TODO segmentation fault??? komt door unyts

hp.mollview(total_map, norm="log")
plt.title(f"Total Lightcone Map: DM (Redshift 0 - {z})")
plt.savefig(f"total_lightcone_map_{z}.png")

tot_pixels = len(total_map)

num_draws = 1000
# Randomly draw pixels from the total map
random_indices = np.random.choice(tot_pixels, num_draws, replace=True)
random_sightlines = total_map[random_indices]
sightlines_normalized = random_sightlines / np.mean(random_sightlines) #/ (u.pc/u.cm**3)

def compute_F(sightlines_normalized, z):
    """    
    Function to compute the F statistic from a set of sightlines coming from a certain redshift z.
    """
    F = np.std(sightlines_normalized) * z**(0.5) # TODO is deze std correct?
    return F

# Compute the F statistic for the random sightlines
F = compute_F(random_sightlines, z)

# TODO: error on F (through bootstrapping?)
# TODO: test for convergence of the F statistic w.r.t. the number of sightlines, resolution, box size, etc.
# TODO: also test for effects of smoothing of the lightcone maps and downsampling of the lightcone maps
# TODO: test redshift dependence of the F statistic

fig, ax = plt.subplots()
ax.hist(sightlines_normalized, bins=50, density=True, alpha=0.7, color='blue')
ax.axvline(np.mean(sightlines_normalized), color='red', linestyle='dashed', linewidth=1, label='Mean')
# ax.axvline(np.mean(sightlines_normalized) + F, color='green', linestyle='dashed', linewidth=1, label='F Statistic = {:.2f}'.format(F))
# ax.axvline(np.mean(sightlines_normalized) - F, color='green', linestyle='dashed', linewidth=1)
ax.set_xlabel('DM / <DM>')
ax.set_ylabel('Number')
ax.set_title(f'DM distribution at z = {z}')
ax.legend()
plt.tight_layout()
fig.savefig(f"sightlines_normalized_histogram_{z}.png")

# TODO de DM/<DM> is niet normaal verdeeld??