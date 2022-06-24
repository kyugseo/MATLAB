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
