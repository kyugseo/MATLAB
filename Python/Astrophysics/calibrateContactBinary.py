import numpy as np
from astropy.io import fits
import glob

calibrated_dir = '../mydata/ContactBinary_calibrated/'
raw_dir = '../mydata/ContactBinary/'


# Read the master bias and master dark frames that you created earlier:
hdu = fits.open('../data/shared/calibrations/2021.03.17-BIAS-DARK-MASTERS-bin1/MasterBias.fit') 
MasterBias = hdu[0].data.astype('float') 
hdu = fits.open('..//data/shared/calibrations/2021.03.17-BIAS-DARK-MASTERS-bin1/MasterDark.fit') 
MasterDark = hdu[0].data.astype('float')


bands = ['PhotV']

for band in bands:
    FlatFileName = '../data/shared/calibrations/2021.03.15-FLAT-MASTERS-bin1/MasterFlat_'+band+'.fit'
    hdu = fits.open(FlatFileName)
    MasterFlat = hdu[0].data.astype('float') 

    # get the list of all the files that were exposed in the current band
    filelist = glob.glob(raw_dir+'*'+band+'*')
    
    # loop over all the files in the filelist and calibrate them
    for f in filelist:
        hdu = fits.open(f) # open the file f
        rawdata = hdu[0].data.astype('float') 
        texp = hdu[0].header["EXPTIME"] 

        # Use the equation in lecture 4 to calibrate the data
        calibrated_data = (rawdata-texp*MasterDark-MasterBias)/MasterFlat

        # modify the hdu file, but save it in the calibrated directory
        hdu[0].data = calibrated_data
        hdu[0].header['CLBRATED'] = (True,'Calibrated from file '+f)
        hdu[0].header['BZERO'] = 0
        hdu[0].header['BSCALE'] = 1.0

        filename = f[f.rfind('/')+1:] # strip the file name of the leading directorys in the full path
        hdu.writeto(calibrated_dir+ filename,overwrite=True)

        

    
