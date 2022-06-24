import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table

# Using Table.read, read the masterTable.fits file that you created in Assignment 7
mastertable = Table.read("../assignment7/masterTable.fits")

# Select only those stars for which there was a Bmag measured. In Assignment 7, we matched the V-band detected
# stars with the B-band detected stars.  Any stars that appeared in the V-band image but not in the B-band images
# were given a B instrumental magnitude of NaN.
mask = np.isfinite(mastertable['mag_inst_PhotB'])  # An array of booleans where True means that the instrumental B mags are finite
mastertable = mastertable[mask]  # select only those stars with finite instrumental Bmag.

# Write the pixel coordinates of the reference star HIP 115521 in your fits images
xstar, ystar = 1332, 1329

# Find the pixel distance of all the objects in mastertable from the x,y coordinates of the star
dist = np.sqrt((mastertable['x'] - xstar)**2 + (mastertable['y'] - ystar)**2)

# Use np.argmin to find the index of the dist array that gives you the minimum distanace.
# This also corresponds to the index of mastertable that gives you all your measurements for that star
idx = np.argmin(dist)

# The offset between the actual B mag of the reference star and your instrumental magnitude
Bmag_offset = mastertable['mag_inst_PhotB'][idx] - 11.18

# The offset between the actual V mag of the reference star and your instrumental magnitude
Vmag_offset = mastertable['mag_inst_PhotV'][idx] - 10.55

# Compute the apparent magnitudes of all the objects in the mastertable given the magnitude offsets and the
# instrumental magnitudes
magB = mastertable["mag_inst_PhotB"] - Bmag_offset
magV = mastertable["mag_inst_PhotV"] - Vmag_offset


# Add new columns in mastertable with your
mastertable['magB'] = magB
mastertable['magV'] = magV

# Since the magnitudes were only offset by a constant, the errors on the magnitudes are the same
mastertable['magB_err'] = mastertable['mag_inst_err_PhotB']
mastertable['magV_err'] = mastertable['mag_inst_err_PhotV']


# ------------------------------------------------------------------------------------------------
# Lastly, select only those stars that are likely to be members of the cluster.
xcluster, ycluster = 1036, 1152
rcluster = np.sqrt((1332 - xcluster)**2 + (1162 - ycluster)**2)

# Compute the distance of each star from centre of the cluster
dist = np.sqrt((mastertable['x'] - xcluster)**2 + (mastertable['y'] - ycluster)**2)

# Create a mask (a boolean array) that selects only those stars within rcluster of the cluster centre
maskCluster = (dist < rcluster)

# Save this flag mask as another column in mastertable
mastertable['maskCluster'] = maskCluster


# ------------------------------------------------------------------------------------------------
# Save the new master table into your current directory with the filename "masterTable_calib.fits".
# Look up the documentation on astropy tables in order to do this.
mastertable.write('masterTable_calib.fits', overwrite=True)
