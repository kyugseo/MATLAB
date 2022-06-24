import numpy as np
from astropy.io import fits
import glob
from astropy.stats import sigma_clip
from reproject.mosaicking import find_optimal_celestial_wcs
from reproject import reproject_interp

# Fill in the lines where there are 3 dots:  ...
# Each  ...  can be filled in with a single line

# In the line below, you may have called "mydata" something else in Assignment 1
calibrated_dir = '../mydata/ContactBinary_calibrated/'

# Use glob to create file list that includes images from *all* bands
filelist = filelist = glob.glob(calibrated_dir+'*')

# Find the optimal shape of the canvas that will fit all the images, as well as the optimal wcs coordinates
wcs_out, shape_out = find_optimal_celestial_wcs(filelist,auto_rotate=True)
print('Dimensions of new canvas:',shape_out) # Should be bigger than the original 2048x2048 images we started with.

bands = ['PhotB','PhotV','PhotR']  # This is the list of the three filter names

for band in bands # Loop through the three bands (TIP: when testing your code, just go through one band; but don't forget
         # to change this back to 3 bands when you're done testing and ready to run the whole thing)
         
    # Get the list of all the files that were exposed in the current band
    filelist = glob.glob(calibrated_dir+'*'+band+'*') # Remember to use *'s as wild cards in the file names
    
    allexposures = [] # Declare an empty list.  Each item of the list will hold the data array of each file in filelist.
    airmass = [] # Declare an empty list.  Will hold the airmass of each file in filelist.
    texp = [] # Declare an empty list.  Will hold the exposure times.
    
    for f in filelist # Loop through the files in filelist  (TIP: when testing your code, just go through the first 3 files;
            # don't forget to change this to back to the full filelist when you're done testing)
        hdu = fits.open(f) # Open the current file
        texp.append(hdu[0].header['EXPTIME']) # get the exposure time
        airmass.append(hdu[0].header['AIRMASS']) # get the air mass 

        # This line runs reproject_interp to map the pixels of the image to the pixels of the canvas we created above
        # new_image_data below has the same dimensions as the larger canvas.
        new_image_data = reproject_interp(f, wcs_out,shape_out=shape_out,return_footprint=False) 
        allexposures.append(new_image_data)

    # Turn the list of arrays into a 3D array
    allexposures = np.array(allexposures)

    # We have now aligned all the exposures onto the same pixels.  Combine them into a single image using sigma_clip and taking the mean.
    images_masked = sigma_clip(allexposures,sigma=3.0)  # Use sigma_clip to mask pixels more than 3 sigma from the mean of the exposures
    combined_image = np.ma.mean(images_masked) # Take the mean of the masked array images_masked using np.ma.mean()

    # np.ma.mean() sets pixels to 0 if there were no good pixels to take a mean.  The following lines set them to NaN instead.
    # NaN means "not a number" - easier to mask later on.
    mask = combined_image.mask
    combined_image = combined_image.data
    combined_image[mask] = np.nan

    # We want to save this new data into a new fits file.  But we need to save it with most of the same header information as the original
    # files.  Get the header of the first file in filelist:
    hdu = fits.open(filelist[0])
    oldheader = hdu[0].header
    newheader = oldheader.copy()  # Copy all the header "cards" into "newheader"
    # The rest of the "cards" we'll get from the wcs_out.  This changes the cards that have to do with the WCS 
    for card in wcs_out.to_header().cards: newheader[card[0]] = card[1:]

    # Change the exposure time
    newheader['EXPTIME'] = np.sum(texp) # Put here the sum of all the exposure times in the list texp
    # Add the average airmass, max and min
    newheader['AVGAIRMS'] = np.mean(airmass) # Put here the mean of all the airmasses in the airmass list
    newheader['MAXAIRMS'] = np.max(airmass) # The maximum value of the airmass list 
    newheader['MINAIRMS'] = np.min(airmass) # The minimum value of the airmass list

    # Now save the file 
    fits.writeto('WUMA_'+band+'.fit', combined_image, newheader,overwrite=True)

