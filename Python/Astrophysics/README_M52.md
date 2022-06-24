# Image of M52

## Calibrate images of M52

By using following [code](https://github.com/kyugseo/Programming/blob/3cca06b0b293cc41eecc39548923f3ba6013a893/Python/Astrophysics/calibrateM52.py), calibrate the M52 datas, 

```
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

```


## Align the dithered images of M52
[code](https://github.com/kyugseo/Programming/blob/c5ccf14be456ee4e1f7860a0be98742d7d529271/Python/Astrophysics/align.py)


```
conda install python=3.7
conda install -c conda-forge reproject shapely six
```


```
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
    
```

## Subtract the Sky from the Combined Images
[code](https://github.com/kyugseo/Programming/blob/3cca06b0b293cc41eecc39548923f3ba6013a893/Python/Astrophysics/sky_subtract_M52.py)

```
import numpy as np
from astropy.io import fits
import sep
from astropy.visualization import ZScaleInterval,ImageNormalize
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt

# Fill in the lines where there are 3 dots:  ...
# Each  ...  can be filled in with a single line

plt.ion() # This turns on automatic display of the plots ("plt.show()" is no longer necessary)

def readImageData(f): # The argument f is a string that contains the file name to be read
    hdu = fits.open(f) # Open the file 
    image_data = hdu[0].data # get the data, and assign to image_data (after calibration they're already floats)
    image_data = image_data.byteswap(inplace=True).newbyteorder() # This line is need for SEP; otherwise it produces an error

    return hdu, image_data

def subtractSky(image_data, band, filter_size=3, box_size=64):
    # Determine the sky level as a function of position 
    sky = sep.Background(image_data,fw=filter_size,fh=filter_size,bh=box_size,bw=box_size) # use SEP to determine the background sky level
    sky_data = sky.back() # This is the 2D array containing the sky level in each pixel (ADUs)

    image_data_nosky = image_data - sky_data # Subtract the sky data from the image data and assign the result to image_data_sub

    makeplots(image_data,sky_data,image_data_nosky,band) # Call the function makeplots defined below

    return sky_data,image_data_nosky, sky.globalrms

def makeplots(image_data,sky_data,image_data_nosky,band):
    # This function is complete.  No need to edit.
    # Plot the 3 images side by side to compare them (the original image, the sky image, and the image minus the sky)
    fig, ax = plt.subplots(1,3,figsize=[12,4])
    
    norm = ImageNormalize(image_data,interval=ZScaleInterval()) # scales the image by same 'zscale' algorithm as ds9
    im0 = ax[0].imshow(image_data,origin='lower',cmap='gray',norm=norm)
    ax[0].set_title('Original')

    im1 = ax[1].imshow(sky_data,origin='lower',cmap='gray') # linear.  no need for zscale
    ax[1].set_title('Sky')

    norm = ImageNormalize(image_data_nosky,interval=ZScaleInterval()) # scales the image by same 'zscale' algorithm as ds9
    im2 = ax[2].imshow(image_data_nosky,origin='lower',cmap='gray',norm=norm)
    ax[2].set_title('After sky subtraction')

    # Remove the ticks and tick labels
    for a in ax:
        a.xaxis.set_visible(False)
        a.yaxis.set_visible(False)

    # Add colour bars to all three panels (not as simple when using subplots; calls function below)
    colourbar(im0,ax[0])
    colourbar(im1,ax[1])
    colourbar(im2,ax[2])
    fig.tight_layout()
    fig.savefig('test_sky_subtraction_'+band+'.png')

def colourbar(sc,ax):
    # This function is complete.  No need to edit.
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size="5%", pad=0.05)
    cbar = plt.colorbar(sc, cax=cax, orientation='vertical')


#--------------------------------------------------------------------
# If using the ipython interpreter, copy-paste all the above lines at once. 
# Then go through the following line-by-line.

bands = ['PhotV','PhotB','PhotR']
for band in bands: # If using the ipython interpreter, type band='PhotV' instead of this line. Change to the band you want 
    # Call the function to read the file
    hdu, image_data = readImageData('M52_'+band+'.fit')

    # Use the ipython interpreter to keep adjusting this line (filter_size and box_size)
    # until you get a relatively smooth sky and sky subtraction.
    # TIP: use the up-arrow key to get your previous commands in the ipython interpreter
    sky_data,image_data_nosky,skyrms = subtractSky(image_data, band, filter_size=10, box_size=64)

    # Once you're happy with the sky subtraction, save the sky data and sky-subtracted image into new files
    hdu[0].header['GLOBLRMS'] = skyrms
    hdu[0].data = sky_data # Re-use the header information from the old hdu, but overwrite the data with the sky data
    hdu.writeto('sky_'+band+'.fit',overwrite=True) # save the hdu as new file

    hdu[0].data = image_data_nosky # Re-use the header information from the old hdu, but overwrite the data with the sky-subtracted image
    hdu.writeto('M52_nosky_'+band+'.fit',overwrite=True) # save the hdu as new file
```
### PhotB
![](https://github.com/kyugseo/Programming/blob/3cca06b0b293cc41eecc39548923f3ba6013a893/Python/Astrophysics/test_sky_subtraction_PhotB.png)
### PhotV
![](https://github.com/kyugseo/Programming/blob/3cca06b0b293cc41eecc39548923f3ba6013a893/Python/Astrophysics/test_sky_subtraction_PhotV.png)
### PhotR
![](https://github.com/kyugseo/Programming/blob/3cca06b0b293cc41eecc39548923f3ba6013a893/Python/Astrophysics/test_sky_subtraction_PhotR.png)
    
