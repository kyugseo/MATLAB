import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from ezpadova import parsec
from mpfit import mpfit
from scipy.spatial.distance import cdist
from astropy.stats import sigma_clip

# ----------------------------------------------------------------------------
# Get the magnitudes of the stars in M52

# Read the table you just created in findApparentMag.py
mastertable = Table.read("./masterTable_calib.fits")

# Get the B-V and V-mag information from the mastertable
magV_M52 = mastertable["magV"]  # Get the apparent V-band magnitude (not the instrumental magnitude)
bv_M52 = mastertable["magB"] - mastertable["magV"]  # Get the B-V of the stars given the information in mastertable

maskCluster = mastertable["maskCluster"]  # From mastertable get the mask that selects cluster stars


# -----------------------------------------------------------------------------
# Download the Padova isochrones (use intervals of 0.1 in logAge)
iso = parsec.get_t_isochrones(6.0, 10.0, 0.1, 0.019)

# Get rid of the post-AGB stars
mask = (iso['label'] != 9)
iso = iso[mask]

# Get the B-V and V mag values from the iso table
bv_isochrone = iso["Bmag"] - iso["Vmag"]
v_isochrone = iso["Vmag"]

# Get the log of the ages from the iso table
logAge_isochrone = np.log10(iso["Age"])  # All the values in the iso table
logAge_isochrone_unique = np.unique(logAge_isochrone)  # Only the unique values


# -----------------------------------------------------------------------------
# Some functions to plot things
def plotCMD():
    # Plot the stars on a colour-magnitude diagram
    plt.scatter(bv_M52, magV_M52, color="lightgrey", label="Non-cluster stars")  # First plot all the stars as "lightgrey" dots. Use the "label" keyword to call these "Non-cluster stars"
    plt.scatter(bv_M52[maskCluster], magV_M52[maskCluster], color="blue", label="Cluster stars")  # Then plot only the cluster stars as blue dots. Use the "label" keyword to call these "Cluster stars"
    # The labels will later appear in a legend.
    plt.ylim([18, 8])
    plt.xlim([0.1, 3.4])
    # Label the axes
    plt.ylabel("magnitude")
    plt.xlabel("B-V")


def plotIsochrone(logAge, DM, EBV):
    # This function plots a single isochone with a given logAge, E(B-V), and distance modulus

    # Find the value in logAge_isochrone_unique that is the closest to logAge:
    closest_idx = np.argmin(np.abs(logAge_isochrone_unique - logAge))
    closestLogAge = logAge_isochrone_unique[closest_idx]

    # Create the mask that selects only those items in logAge_isochrone that correspond to that closestLogAge
    mask = (logAge_isochrone == closestLogAge)

    # Compute what the isochrone would like after the distance modulus and reddening are applied
    # http://voyages.sdss.org/expeditions/expedition-to-the-milky-way/star-clusters/distance-modulus/
    Av = 3.1 * EBV  # The attenuation in V
    bv_apparent = bv_isochrone[mask] + EBV
    v_apparent = v_isochrone[mask] + Av + DM

    # Plot the isochrone as a red curve and give it a label that will appear in the legend
    label = f'log Age: {logAge:.2f}\nDistance Modulus: {DM:.2f}\nE(B-V): {EBV:.2f}'
    pltiso, = plt.plot(bv_apparent, v_apparent, c='red', label=label)
    return pltiso


# ------------------------------------------------------------------------------
# STOP! copy the above lines into the ipython interpreter  (use the command "ipython --pylab" in the HPC terminal)
plotCMD()  # Then plot the CMD

# Run this a few times with different values in the arguments until you get a good fit by eye.
# Note: you can remove the last isochrone with the command pltiso.remove()
# Also: up-arrow works in the ipython interpreter just as it does on the command line
# https://webda.physics.muni.cz/cgi-bin/ocl_page.cgi?dirname=ngc7654
params = [7.76, 5 * np.log10(1421/10), 0.7]  # Write the values of three parameters that you found when fitting by eye.
pltiso = plotIsochrone(params[0], params[1], params[2])

# Once you've found a good fit, run these lines:
plt.legend()
plt.title('Fit By Eye')  # I eyeballed it
plt.savefig('fitByEye.png')

plt.close()


# Now you can continue:
# ---------------------------------------------------------------------------------------
# Numerical isochrone fitting
def isochroneDistance(bv, v, lage, dm, ebv):

    # logAge_isochrone_unique is sorted.  lage is a value that is between two values in logAge_isochrone_unique.
    # idx is the index for the value below lage, and idx+1 is the index of the value above lage.
    idx = np.searchsorted(logAge_isochrone_unique, lage) - 1

    # The linear interpolation factor to be used a few lines down
    factor = (lage - logAge_isochrone_unique[idx])/(logAge_isochrone_unique[idx+1]-logAge_isochrone_unique[idx])

    # What is the attenuation in v?
    Av = 3.1 * ebv

    # This line creates a 2D array with v and bv values, which are the coordinates of the stars on the CMD.
    # Needs to be transposed in order to input to cdist.
    star_coords = np.array([v, bv]).T

    # Initialize a 2D array of distances on the CMD
    twodists = np.empty([v.size, 2])
    for i in range(2):  # loops through the two isochrones that are closest in age to the given lage
        mask = (logAge_isochrone == logAge_isochrone_unique[idx+i])  # select the lines in iso table that correspond to the age we want
        v_iso = (v_isochrone[mask] + dm) + Av  # Find what the apparent magnitude of the isochrone would be given the distance modulus and Av
        bv_iso = bv_isochrone[mask] + ebv  # Find what the B-V of the isochrone would be given the E(B-V)

        iso_coords = np.array([v_iso, bv_iso]).T  # These are the coordinates of the isochrone points on the CMD

        # cdist computes the distances of each star to the each isochrone point, creating a big 2D array.
        # np.nanmin finds the minimum distance for each star (along one axis of the 2D array).
        twodists[:, i] = np.nanmin(cdist(iso_coords, star_coords), axis=0)

    dist = (twodists[:, 1] - twodists[:, 0])*factor + twodists[:, 0]  # Interpolate between the minimum distances to the 2 isochrones we looped through
    dist_masked = sigma_clip(dist, 3.0)  # Use sigma_clip to keep only the stars within a distance of 3 sigma from the isochones
    dist[dist_masked.mask] = 0.0  # Assign the clipped stars a value of 0

    return dist


# This is the function that is called by mpfit
def fitfunction(params, x=None, y=None, err=None, fjac=None):
    lage, dm, ebv = params
    bv = x
    vmag = y

    dist = isochroneDistance(bv, vmag, lage, dm, ebv)
    status = 0

    return status, dist  # dist is the value that will be minimized by mpfit


# params are the starting values that will be input to mpfit
kw = {'y': magV_M52[maskCluster], 'x': bv_M52[maskCluster]}
parinfo = [{'parname': 'logAge (yr)',     'value': params[0], 'fixed': False, 'limited': [True, True], 'limits': [6, 10]},
           {'parname': 'Distance Modulus', 'value': params[1], 'fixed': False, 'limited': [True, False], 'limits': [0, 0]},
           {'parname': 'E(B-V)',          'value': params[2], 'fixed': False, 'limited': [True, False], 'limits': [0, 0]}]
# (in the above parinfo, 'limited' tells mpfit whether the parameters should be limited to certain lower and upper values,
# and 'limits' gives what those limits are)

# Call mpfit
m = mpfit(fitfunction, functkw=kw, parinfo=parinfo)


# ---------------------------------------------------------------------------------------
# Plot the result
lage, dm, ebv = m.params

plotCMD()
plotIsochrone(lage, dm, ebv)
plt.legend()
plt.title('Numerical Fit')
plt.savefig('numericalfit.png')
