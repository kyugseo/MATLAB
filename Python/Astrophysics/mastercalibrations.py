import numpy as np
from astropy.io import fits
import glob
from astropy.stats import sigma_clip

# Fill in the lines where there are 3 dots:  ...
# Each  ...  can be filled in with a single line

# Use these files and directories for this assignment
biaslist = glob.glob('/data/shared/observations/2021.02.01-BIAS-bin2/*')
darklist = glob.glob('/data/shared/observations/2021.02.01-DARK-bin2/*')

flats_directory = '/data/shared/observations/2021.01.13-18-FLATS/'


# Write a function called "readfiles" so we can use it several times without having to write it over again
def readfiles(filelist):
    ''' This function reads all the fits files in filelist and combines their data into one big 3D array.
        INPUT: 
            filelist: list of file names to be read
        OUTPUT: 
            allexposures: (nfiles, npixels_y, npixels_x) a 3D array containing all the image data for all the files
            hdu: the astropy fits object of the last file that was read
            t_exp: list of exposure times for each exposure
    '''
    
    allexposures = []  # initialize the allexposures list (this is different from a numpy array)
    t_exp = []  # initialize the t_exp list (this is different from a numpy array)
    for exposure in filelist:
        hdu = fits.open(exposure)  # open the file
        allexposures.append(hdu[0].data.astype('float'))  # append the data from hdu to the list.  Make sure to convert to floats.
        t_exp.append(hdu[0].header["EXPTIME"]) # append the exposure time to the t_exp list.

    allexposures = np.array(allexposures) # since allexposures was a list, this line converts it to a numpy array

    return allexposures,hdu,t_exp  # return the big array, and the last hdu that was read

#----------------------------------------------------------------------------------------
# Make the master bias

# Here we use the function that we wrote above to read the files in biaslist
allexposures,hdu,t_exp = readfiles(biaslist)

# Use sigma_clip and np.ma.mean to compute the data for the master bias (refer to lecture 4)
masked_exposures = sigma_clip(allexposures,sigma=3.0,axis=0)  # use sigma_clip
master_bias = np.ma.mean(masked_exposures,axis=0) # use np.ma.mean

# Turn it back to a regular array, instead of a masked array
master_bias = master_bias.data 

# Modify the hdu that was outputted from readfiles and save the file
hdu[0].data = master_bias
hdu[0].header['MSTRBIAS'] = (True,'Master Bias created from '+str(len(biaslist))+' Exposures')
hdu[0].header['BZERO'] = 0
hdu[0].header['BSCALE'] = 1.0
hdu.writeto('MasterBias.fit',overwrite=True)



#----------------------------------------------------------------------------------------
# Make the master dark

# Use readfiles to read the darklist (see how it was done for the master bias)
allexposures,hdu,t_exp = readfiles(darklist) # read the files in the dark list

# allexposures is a 3D array of shape (n_exposures, npixels_y, npixels_x).  For each exposure, subtract the master_bias 
for i in range(len(darklist)):
    allexposures[i] = allexposures[i]-master_bias  # subtract the master_bias

# Use sigma_clip and np.ma.mean to compute the data for the master dark
masked_exposures = sigma_clip(allexposures,sigma=3.0,axis=0) # use sigma_clip
master_dark = np.ma.mean(masked_exposures,axis=0) # use np.ma.mean 

# Divide the master dark by the exposure time so that the master dark is a current (per second).
# The exposure times for those files were all the same (you can check), so you can just use the first
# element of t_exp.
master_dark = master_dark/t_exp[0]

# Turn it back to a regular array, instead of a masked array
master_dark = master_dark.data  

# Modify the hdu that was outputted from readfiles and save the file
hdu[0].data = master_dark
hdu[0].header['MSTRDARK'] = (True,'Master Dark created from '+str(len(darklist))+' Exposures')
hdu[0].header['BZERO'] = 0
hdu[0].header['BSCALE'] = 1.0
hdu.writeto('MasterDark.fit',overwrite=True)



#----------------------------------------------------------------------------------------
# Make the master flat

# We have flats in 3 bands: B, V and R.  Since we have to do the same thing to all three bands,
# we're going to loop through the three bands

searches = ['*PhotB*','*PhotV*','*PhotR*']

for search in searches:
    # the *'s in the search tell glob to find all the files with 'PhotB' or 'PhotV' or 'PhotR' (depending on the search)
    flatlist = glob.glob(flats_directory+search)  

    # read the files using readfiles 
    allexposures,hdu,t_exp = readfiles(flatlist) # using the flatlist

    # loop through all the exposures and subtract the master bias and the master dark * the exposure time
    for i in range(len(flatlist)):
        allexposures[i] = allexposures[i] - master_bias  # subtract the master bias
        allexposures[i] = allexposures[i] - master_dark*t_exp[i]  # subtract the master dark * exposure time

    # Compute the means of all the exposures using np.mean and the axis keyword to sum over all pixels in a single image
    means = np.mean(allexposures,axis=(1,2)) # This is now an array of length len(flatlist)

    # Then divide each image by the mean so that each resulting image has average value of 1
    for i in range(len(flatlist)):
        allexposures[i,:,:] /= means[i]

    # Select only the good flats, ie, those whose mean counts are > 10000
    pick = np.where(means > 10000)[0] # this is numpy array containing the indices of the images that are good

    # Use sigma_clip and np.ma.mean to compute the data for the master flat,
    # but this time use allexposures[pick,:,:] as the input
    masked_exposures = sigma_clip(allexposures[pick,:,:],sigma=3.0,axis=0) # use sigma_clip, using allexposures[pick,:,:] instead of allexposures
    master_flat = np.ma.mean(masked_exposures,axis=0) # use np.ma.mean

    # Turn it back to a regular array, instead of a masked array
    master_flat = master_flat.data  

    # Modify the hdu that was outputted from readfiles and save the file
    hdu[0].data = master_flat
    hdu[0].header['MSTRFLAT'] = (True,'Master Flag created from '+str(len(flatlist))+' Exposures')
    hdu[0].header['BZERO'] = 0
    hdu[0].header['BSCALE'] = 1.0
    hdu.writeto('MasterFlat_'+search[1:-1]+'.fit',overwrite=True) 

