import numpy as np
from astropy.io import fits
import glob
import sep
#from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from astropy.stats import sigma_clip

# Fill in the lines where there are 3 dots:  ...
# Each  ...  can be filled in with a single line

# In the two lines below, you may have called "mydata" something else in Assignment 1

calibrated_dir = '../mydata/ContactBinary_calibrated/'
raw_dir = '../mydata/ContactBinary/'
filelist = glob.glob(raw_dir+'*')

exptimes = []
# Information for computing the noise
gain = 1.5
noise_read = 19. # in electrons; value that fits for 2048x2048 images


def Master(): 
# Read the master bias and master dark frames that you created earlier:
    hdu = fits.open('../mydata/2021.03.17-BIAS-DARK-MASTERS-bin1/MasterBias.fit') # open the master bias file
    MasterBias = hdu[0].data.astype('float') # take the data, convert to floats, and assign it to MasterBias
    hdu = fits.open('../mydata/2021.03.17-BIAS-DARK-MASTERS-bin1/MasterDark.fit') # open the master dark file
    MasterDark = hdu[0].data.astype('float') # take the data, convert to floats, and assign it to MasterDark
    hdu = fits.open('../mydata/2021.03.15-FLAT-MASTERS-bin1/MasterFlat_PhotV.fit') # open FlatFileName
    MasterFlat = hdu[0].data.astype('float')
    
    return MasterBias, MasterDark, MasterFlat


MasterBias, MasterDark, MasterFlat = Master()
noise_dark = np.sqrt(gain*np.abs(MasterDark))


bands = ['PhotV']
airmass = []
mags = []
mag_errors = []
sn = [] 
mags_ref=[]
mag_errors_ref=[]
magV=[]
times=[]

for band in bands:
    # Get the list of all the files that were exposed in the current band
    filelist = glob.glob(calibrated_dir+'*'+band+'*')
    
    # Loop over all the files in the filelist and calibrate them

    for f in filelist:
        hdu = fits.open(f) # Open the file f
        image_data =  hdu[0].data # get the data, and assign to image_data (after calibration they're already floats)
        texp = hdu[0].header['EXPTIME'] # get the exposure time
        am = hdu[0].header['AIRMASS'] # get the air mass from the header
        time=hdu[0].header['TIME']
        times.append(time) # append am to the airmass 
        
        image_data = image_data.byteswap(inplace=True).newbyteorder() # This line is needed for SEP; otherwise it produces an error
        
        # determine the sky level as a function of position 
        sky = sep.Background(image_data,fw=30,fh=30,bh=120,bw=120) # use SEP to determine the background sky level
        sky_data = sky.back() # This is the 2D array containing the sky level in each pixel (ADUs)
        
        noise_sky = np.sqrt(gain*np.abs(sky_data)) # Compute the Poisson noise of the sky in *electrons*
        
        image_data_sub = image_data-sky_data # Subtract the sky data from the image data and assign the result to image_data_sub
        noise_data = np.sqrt(gain*np.abs(image_data_sub)) # Compute the noise of the image data in *electrons*; some of the data will be negative, so take the absolute value first

        # Total noise: add the image noise, sky noise, dark noise and read noisein quadrature
        noise = (noise_data ** 2 + noise_sky ** 2 + (noise_dark) ** 2 * texp + noise_read ** 2) ** 0.5  # This is in electrons
        noise /= gain  # Turn the noise back into units of ADU


        #-------------------------------------------------------------------------------
        # Lines that have to do with SEP and they are already completed for you (we will learn more about these functions
        # another time).  
        
        # This line extracts all light sources at least 1.5 sigma from the background (sky.globalrms) and assigns the result
        # to the variable called "objects"
        objects = sep.extract(image_data_sub, 1.5, err=sky.globalrms)

        # This line computes the Kron radius of each object (in units of objects['a'] and objects['b'])
        kronrad, krflag = sep.kron_radius(image_data_sub, objects['x'], objects['y'], objects['a'], objects['b'], objects['theta'], 6.0)
        flux_radius = 2.5*kronrad*objects['b']

        # This line measures the flux within 2.5*Kron radius
        flux, fluxerr, flag = sep.sum_ellipse(image_data_sub, objects['x'], objects['y'], objects['a'], objects['b'], objects['theta'],
                                              2.5*kronrad,subpix=1,err=noise)

        #-------------------------------------------------------------------------------
        # The following lines (already completed for you) attempt to select a particular star out of the many objects detected
        # by SEP.  The brightest star is saturated, so we can't use that.  We want the 2nd brightest star near the centre.  There's another 
        # star in the corner of the image that is the brightest object after the galaxy, but it sometimes appears or disappears because
        # the camera shifts around by a few pixels after every exposure - a process called dithering).  The strategy here will be to
        # sort the objects by flux, and then select the 2nd brightest object that isn't in the corner.
        
        # Get the indices of the object list that sorts the flux into decreasing order (brightest first)
        indsort = np.flip(np.argsort(flux))  #  np.argsort() sorts in increasing order.  np.flip() reverses the order
        
        # After sorting, select only those objects whose x-coordinate is between 500 and 1500 (ie not in the corner)
        indcentre = np.where( (objects['x'][indsort] > 1700) & (objects['x'][indsort] < 2200) &
                              (objects['y'][indsort] > 1700) & (objects['y'][indsort] < 2200) &
                             (flux_radius[indsort] < 20.0) ) # We also want the radius to be small so as not to select the galaxy

        # Pick the brightest object
        idx = indsort[indcentre][0] # this gives a single index of that brightest 

        # Plot ellipse around star to make sure it's the one we wanted
        #plotcircle(image_data_sub,idx,objects,f,band)
        
        # The flux of the object we picked
        flux_pick = flux[idx]
        fluxerr_pick = fluxerr[idx]
        sn.append(flux_pick/fluxerr_pick) # Append the S/N of this star in the sn list
        
        #---------------------------------------------------------------------------------
        # Determine the instrumental magnitude from flux_pick; This is the Pogson equation with C=0 (Lecture 2) 
        mag_instrument = -2.5*np.log10(flux_pick/texp) # instrumental magnitude
        mag_error = -2.5*(1/flux_pick)*(1/np.log(10)) # determine the error on the magnitude using error propagation through a function

        # Append mag_instrument to the mags list
        mags.append(mag_instrument)

        # Append mag_err to the mag_errors list
        mag_errors.append(mag_error)

        #------------------------------------------------------------------------

        # Get the indices of reference star (brightest first)
        indsort = np.flip(np.argsort(flux))  #  np.argsort() sorts in increasing order.  np.flip() reverses the order
        
        # After sorting, select only those objects whose x-coordinate is between 500 and 1500 (ie not in the corner)
        indcentre = np.where( (objects['x'][indsort] > 1700) & (objects['x'][indsort] < 2200) &
                              (objects['y'][indsort] > 1700) & (objects['y'][indsort] < 2200) &
                             (flux_radius[indsort] < 20.0) ) # We also want the radius to be small so as not to select the galaxy

        # Pick the 2ndd brightest object
        idx = indsort[indcentre][1] # this gives a single index of that 2nd-brightest 

        # Plot ellipse around star to make sure it's the one we wanted
        #plotcircle(image_data_sub,idx,objects,f,band)
        
        # The flux of the object we picked
        flux_pick = flux[idx]
        fluxerr_pick = fluxerr[idx]
        sn.append(flux_pick/fluxerr_pick) # Append the S/N of this star in the sn list
        
        #----------------------------------------------------------------------------------
        # Determine the instrumental magnitude from flux_pick; This is the Pogson equation with C=0 (Lecture 2) 
        mag_instrument_ref = -2.5*np.log10(flux_pick/texp) # instrumental magnitude
        mag_error_ref= -2.5*(1/flux_pick)*(1/np.log(10)) # determine the error on the magnitude using error propagation through a function

        # Append mag_instrument to the mags list
        mags_ref.append(mag_instrument_ref)

        # Append mag_err to the mag_errors list
        mag_errors_ref.append(mag_error_ref)
        # Now that we've read through all the files, we can make our plot
        # First, convert airmass, mags, mag_errors to numpy arrays
        
        Vmag_offset = 11.46 - mag_instrument
        magV = -2.5*np.log10(Vmag_offset/11.46)
        
        magV.apped(magV)
        
    mags = np.array(magV)
    mag_errors = np.array(mag_errors)
    airmass = np.array(airmass)
    sn = np.array(sn)

    # Plot the instrumental magnitudes against the airmass
    plt.errorbar(times,magV,yerr=mag_errors,fmt='ko') # Plot errorbars on top of filled circles (the errorbars will be pretty small - you may not see them)
    plt.xlabel('Airmass') # label the x-axis
    plt.ylabel('Instrumental Magnitude') # label the y-axis
    plt.gca().invert_yaxis() # invert the axis
    plt.title(band) # Put a title at the top that is simply the band

    # If you look at the plot, you'll see that there are some points that do not belong to the main relation
    # (either because of clouds or we didn't get the right star every time).  However the vast majority are
    # on the relation.  We'll need to use sigma_clip to remove those points when we fit a line
        
    # Create a masked array for mags using sigma_clip;
    # this time you don't need the "axis" keyword because mags is a 1D array
    mags_masked = sigma_clip(mags, sigma=3.0)

    # Use np.ma.polyfit and mags_masked to fit only the good points
    slope,intercept = np.ma.polyfit(airmass, mags_masked, 1)




    # Plot the fit line onto the graph
    def model(x,m,b):
        return m*x+b
    plt.plot(airmass,model(airmass,slope,intercept),'r-')

    # Label the graph with the slope and intercept
    label = "y = {0:.2f}x + {1:.2f}".format(*[slope,intercept]) # Create the label
    plt.text(0.1,0.1,label,transform = plt.gca().transAxes) # Write the label at the bottom left corner 

    # Write the highest S/N
    label = "Highest S/N: +{0:.2f}".format(*[np.max(sn)])
    plt.text(0.1,0.07,label,transform = plt.gca().transAxes) # Write the label at the bottom left corner 
    
    #plt.show()
    plt.savefig('extinction_plot_'+band+'.pdf') # Save the figure
