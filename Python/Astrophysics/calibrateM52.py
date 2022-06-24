import numpy as np
from astropy.io import fits
import glob

# Fill in the lines where there are 3 dots:  ...
# Each  ...  can be filled in with a single line

# In the two lines below, you may have called "mydata" something else in Assignment 1
calibrated_dir =  '../mydata/M52_calibrated/'
raw_dir =  '../mydata/2020.08.25-M52/'


# Read the master bias and master dark frames that you created earlier:
hdu = fits.open('../assignment4/MasterBias.fit') # open the master bias file
MasterBias = hdu[0].data.astype('float') # take the data, convert to floats, and assign it to MasterBias
hdu = fits.open('../assignment4/MasterDark.fit') # open the master dark file
MasterDark = hdu[0].data.astype('float') # take the data, convert to floats, and assign it to MasterDark


# The master flat we use must correspond to the same band that the raw image was taken in.
# Therefore, let's loop through the three bands
bands = ['PhotB','PhotV','PhotR']

for band in bands:
    FlatFileName = '../mydata/2020.08.24-FLAT-MASTERS-bin2/MasterFlat_'+band+'.fit'
    hdu = fits.open(FlatFileName) # open FlatFileName
    MasterFlat = hdu[0].data.astype('float') # take the data, convert to floats, and assign it to MasterFlat

    # get the list of all the files that were exposed in the current band
    filelist = glob.glob(raw_dir+'*'+band+'*') # the stars mean to search for any file name with 'PhotB', or 'PhotV', or 'PhotR' in it
    
    # loop over all the files in the filelist and calibrate them
    for f in filelist:
        hdu = fits.open(f) # open the file f
        rawdata = hdu[0].data.astype('float') # get the data, convert to float, and assign to rawdata
        texp = hdu[0].header["EXPTIME"] # get the exposure time

        # Use the equation in lecture 4 to calibrate the data
        calibrated_data = (rawdata-texp*MasterDark-MasterBias)/MasterFlat

        # modify the hdu file, but save it in the calibrated directory
        hdu[0].data = calibrated_data
        hdu[0].header['CLBRATED'] = (True,'Calibrated from file '+f)
        hdu[0].header['BZERO'] = 0
        hdu[0].header['BSCALE'] = 1.0

        filename = f[f.rfind('/')+1:] # strip the file name of the leading directorys in the full path
        hdu.writeto(calibrated_dir+ filename,overwrite=True)

        

    
