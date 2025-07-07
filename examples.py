import h5py
import swiftsimio as sw
import numpy as np
import matplotlib.pyplot as plt
import lightcone_io as lc


#EXAMPLE 1
#I could get all M_200mean halo masses, radii and centers for the HYDRO_FIDUCIAL simulation, by doing:

path_hydro = "/net/hypernova/data2/FLAMINGO/L1000N1800/HYDRO_FIDUCIAL/SOAP-HBT/halo_properties_0077.hdf5"
with h5py.File(path_hydro, "r") as handle:
    M200m = handle["SO/200_mean/TotalMass"][:]*1e10 #mass is stored in units of 1e10 solar masses
    R200m = handle["SO/200_mean/SORadius"][:] #radii, centres and positions are in Mpc
    centre = handle["InputHalos/HaloCentre"][...]

# Find the largest M200mean halo mass in this simulation
largest_M200m = np.max(M200m)
print(f"Largest M200mean halo mass: {largest_M200m:.2e} solar masses")

# Do a histogram of np.log10(M200m) to see the mass function
plt.figure(figsize=(8, 6))
# Make sure to not divide by zero or take log of zero
M200m = M200m[M200m > 0]  # Filter out non-positive masses
plt.hist(np.log10(M200m), bins=50, color='blue', alpha=0.7)
plt.xlabel('log10(M200mean)')
plt.ylabel('Number of Halos')
plt.yscale('log')
plt.title('Halo Mass Function')
plt.grid()
plt.savefig('E1:halo_mass_function.png')