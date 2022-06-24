import numpy as np
from astropy.io import fits
import sep
import matplotlib.pyplot as plt
from astropy.table import Table
import warnings
warnings.filterwarnings('ignore')
from matplotlib.patches import Ellipse
from astropy.visualization import ZScaleInterval,ImageNormalize
import matplotlib as mpl
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["b", "g", "r"]) # For plotting the bands in the right colours
#hdu = fits.open('../mydata/2021.01.18-NGC1907/NGC1907-0001_PhotR.fit')
pixscale = 0.8142039473684209# Use the plate scale (arsec/pixel) that you found in Assignment 2 (note that is for binned pixels
of 2x2)
#---------------------------------------------------------------------------------------------------------------
# From assignment7/photometry.py:
# copy readImageData(), readSkyData() and computeNoise(). These can stay unmodified.
def readImageData(f):
    # This function receives the filename f and reads the image data.
    # Along with the image data, from the header, read the exposure time and the average air mass (fits header card
    "AVGAIRMS")
    hdu = fits.open(f) # Open the file
    image_data = hdu[0].data # get the data, and assign to image_data (after calibration they're already floats)
    texp=hdu[0].header["EXPTIME"]
    airmass=hdu[0].header["AVGAIRMS"]
    # You may or may not need the following line.
    image_data = image_data.byteswap(inplace=True).newbyteorder()
    return hdu, image_data, texp, airmass # outputs the hdu, the image data, the exposure time and the average air mass
def readSkyData(f):
    # This function receives the filename f and reads the sky data.
    # From the header, read the background rms value that we saved (card "GLOBLRMS") when we measured the sky in
    Assignment 6
    hdu = fits.open(f)
    skyrms = hdu[0].header['GLOBLRMS']
    sky_data = hdu[0].data.astype("float")
    return sky_data, skyrms # outputs the sky data and the global rms of the background

def computeNoise(image_data_nosky,sky_data,texp):
    # This function computes the total noise in units of ADUs. Asside from the image data and sky data, you will also need:
    #- gain
    #- read noise
    #- dark current # -> use the master dark file you created in Assignment 4
    # The total noise is the sum (in quadrature) of 4 sources of noise: the read noise, the dark noise, the sky noise and the data noise
    # 1. Declare the gain and read noise (in electrons)
    gain = 1.5
    noise_read = 19
    # 2. Read the master dark data from Assignment 4 and compute the Poision noise (in electrons)
    hdu = fits.open('../assignment4/MasterDark.fit') # Open the master dark file from assignment 4
    MasterDark = hdu[0].data.astype('float') # Assign the dark data to MasterDark
    noise_dark = np.mean(np.sqrt(gain*np.abs(MasterDark))) # Compute the Poisson noise due to the dark current (in electrons); take the absolute value first since some pixels are negative
    # 3. Compute the Poisson noise of the sky in electrons
    noise_sky = np.sqrt(gain*np.abs(sky_data))
    # 4. Compute the Poisson noise of the sky-subtracted image in electrons
    noise_nosky = np.sqrt(gain*np.abs(image_data_nosky))# 5. Total noise: add the image noise, sky noise, dark noise and read noise in quadrature. Note that the dark noise defined above
    # is the dark noise per second. Make sure to scale it up by the exposure time.
    noise = np.sqrt(noise_nosky**2 + noise_sky**2 + texp*noise_dark**2 + noise_read**2)
    # 6. Turn the noise back into units of ADU
    noise = noise/gain
    return noise # Return the noise in units of ADU
#------------------------------------------------------------------
# Now copy sourceExtraction() also from assignment7/photometry.py.
# We will make some modifications:
'''
1. We have been using sep.extract() to output the objects list only. Check the documentation to
find out to *also* output the segmentation map. So, your sep.extract line should read something
like this:
objects, seg = sep.extract(...)
If you don't remember what the segmentation map is, please review Tuesday's lecture.
2. The segmentation map is a list of IDs for each object, mapped onto pixels.
We need to create the array seg_id which contains the IDs, corresponding to each object in the
objects list. Do this by adding this line after your sep.extrac() line:
seg_id = np.arange(1, len(objects)+1, dtype=np.int32)
3. seg_id is a list that corresponds to the objects list. Therefore, just as you masked out the
objects list to excluded the stars near the edges, do the same to seg_id.
4. Convert the objects list structured array into an astropy Table.
5. Make sure to return objects, seg and seg_id as output from the function
'''
def sourceExtraction(image_data_nosky,skyrms):
    # In this function each "..." is a single line
    # Use sep.extract to find all the objects in image_data_nosky that are 2-sigma above the background,
    # where sigma (err) is the skyrms (follow the example in the slides)
    objects,seg = sep.extract(image_data_nosky, 2, err=skyrms,segmentation_map=True)
    seg_id = np.arange(1, len(objects)+1, dtype=np.int32)
    # Get the dimensions of image_data_nosky
    ny,nx = np.shape(image_data_nosky)
    # We are going to keep only those objects whose light-weighted centres are more than 30 pixels
    # away from the edge of the image. objects['x'] and objects['y'] are the pixel coordinates of
    # the light-weighted centres. The following illustrates how masks are used to select a subset
    # of an array or table.
    mask = (objects['x'] > 30) & (objects['x'] < nx-30) & (objects['y'] > 30) & (objects['y'] < ny-30)
    seg_id = seg_id[mask]
    objects = objects[mask] # Here we've overwritten "objects" with a subset that fulfill the above criteria
    objects = Table(objects)
    return objects,seg, seg_id# Return the structured array of objects
#------------------------------------------------------------------
# Now copy getMags() also from assignment7/photometry.py.
# We will make some modifications:
'''
1. Instead of putting a bunch of things in the return line, let's save the important arrays
into new columns of the objects Table. We want to save:
flux/texp into the column "flux"fluxerr/texp into the column "fluxerr"
mag into the column 'mag_inst' (ie, the instrumental magnitude)
mag_err into the column 'mag_err'
kronrad into the column 'kronrad' (this is the Kron radius. 2.5*kronrad will include pretty much all of the light in that object)
2. Delete the return line.
'''
def getMags(image_data_nosky,objects,noise, texp, ext_coeff, airmass):
    # This function first computes the kron radius and then finds the flux within the 2.5*kron_radius.
    # Follow the examples in the slides to fill this out.
    kronrad, krflag = sep.kron_radius(image_data_nosky, objects['x'], objects['y'], objects['a'], objects['b'],
    objects['theta'], 6.0)
    flux, fluxerr, flag = sep.sum_ellipse(image_data_nosky, objects['x'], objects['y'], objects['a'],
    objects['b'], objects['theta'], 2.5*kronrad, subpix=1, err=noise)
    # Compute the S/N as the flux divided by the error on the flux
    sn = flux/fluxerr
    # Now compute the magnitudes and magnitude error
    mag = -2.5*np.log10(flux/texp)
    mag_err = 2.5*fluxerr/flux/np.log(10)
    # Correct the magnitudes for atmospheric extinction
    mag -= ext_coeff*airmass
    objects['flux'] = flux/texp
    objects['fluxerr'] = fluxerr/texp
    objects['mag_inst'] = mag
    objects['mag_err'] = mag_err
    objects['kronrad'] = kronrad
    #return mag, mag_err, sn, flag # Return the magnitudes, magnitude errors, S/N and the flag
#------------------------------------------------------------------
# This is a new function where we will calibrate our magnitudes just like we did in
# assignment8/findApparentMag.py. Note that in this function, the refmag is given
# as an argument.
def calibrateRefStar(objects,refmag): # refmag is the true magnitude of the reference star
    xstar,ystar = 1076,1271 # Coordinates of reference star
    dist = np.sqrt((objects['x']-xstar)**2+(objects['y']-ystar)**2)
    idx = np.argmin(dist)
    mag_offset = objects['mag_inst'][idx]-refmag
    # Note that mag_offset helps to convert our instrumental magnitudes to
    # standard magnitudes. However, we will need to convert the instrumental fluxes
    # to standard fluxes. Find this conversion factor.
    flux_conversion_factor = 10**(-mag_offset/2.5)
    return flux_conversion_factor
#--------------------------------------------------------------------------------------------------
# Function to measure flux within ellipses of varying radius centred on the galaxy
def galaxyProfile(image_data_nosky,noise,objects,seg,seg_id,band):
    # Recall that sep.extract() above produced a table called objects, containing columns "a" and "b"
    # which are the semi-major and semi-minor axes in units pixels, of the ellipses that contain the objects.
    # The column 'theta' is the CCW angle between the ellipse and the horizontal.# The Kron radii which we computed above are in units of "a" and "b". It has been shown that 2.5 times
    # the Kron radius contains ~90% of the object's light. Compute this radius (in pixels) that contains 90% of the
    # light. Note that we have to compute this radius twice: one for the major axis, one for the minor axis
    r_a= objects['a']*objects['kronrad'] *2.5 # Semi-major axis that contains 90% of the light
    r_b= objects['b']*objects['kronrad'] *2.5 # Semi-minor axis that conatins 90% of the light
    # The objects Table contains information about all the stars in the image. However, we only care about
    # the galaxy that's in this image. The galaxy will have the biggest semi-major axis in the whole image.
    # Find the index of objects that corresponds to the galaxy.
    idx_galaxy = np.argmax(r_a)
    # Now let's define our ellipse parameters for the galaxy alone:
    a = r_a[idx_galaxy]# Semi-major axis that contains 90% of the light of the galaxy
    b = r_b[idx_galaxy]# Semi-minor axis that contains 90% of the light of the galaxy
    xgal = objects['x'][idx_galaxy] # x-position of the galaxy (get this from objects)
    ygal = objects['y'][idx_galaxy] # y-position of the galaxy (get this from objects)
    theta = objects['theta'][idx_galaxy] # Angle of the ellipse (get this from objects)
    # Get the ID of the segmentation map that corresponds to the galaxy
    sid = seg_id[idx_galaxy]
    # Plot the galaxy along with an ellipse that contains 90% of the light
    showEllipses(image_data_nosky,xgal,ygal,a,b,theta,1.0,newplot=True)
    # Define ellipses of varying r_a and r_b and draw them on the above plot
    rfractions = np.arange(0.01,0.9,0.05) # Define the fractions of r_a and r_b that will define smaller ellipses to measure the flux in.
    for r in rfractions: showEllipses(image_data_nosky,xgal,ygal,a,b,theta,r) # Draw these ellipses on the same plot
    plt.savefig('annulli_'+band+'.png') # Save this plot.
    plt.close() # Close this plot.
    # Measure flux within ellipses of varying radius from the centre:
    flux_ellipses, fluxerr, flag =
    sep.sum_ellipse(image_data_nosky,xgal,ygal,a,b,theta,r=rfractions,subpix=5,err=noise,segmap=seg,seg_id=sid)
    # We eventually want the surface brightness, not the flux, so compute the area of the ellipses in units of pixels
    area_ellipses =np.pi*(a*b*rfractions*rfractions)
    # We actually want the flux and area of the annuli between the ellipses. Compute this by subtracting the flux and area
    # of the adjacent smaller ellipse from the bigger ellipse.
    flux_annuli = 0.0*flux_ellipses
    fluxerr_annuli = 0.0*flux_ellipses
    area_annuli = 0*area_ellipses
    for i in range(1,rfractions.size):
        flux_annuli[i] = flux_ellipses[i] - flux_ellipses[i-1] # Subtract the smaller ellipse from the bigger ellipse
        fluxerr_annuli[i] = np.sqrt(fluxerr[i]**2 + fluxerr[i-1]**2 )# Error propagtation for subtraction
        area_annuli[i] = area_ellipses[i] - area_ellipses[i-1] # Subtract the smaller ellipse from the bigger ellipse
        # Create data table to store galaxy profile values
    tab = Table()
    tab['semi-major axis'] = rfractions * a # in pixels
    tab['flux_annuli'] = flux_annuli
    tab['fluxerr_annuli'] = fluxerr_annuli
    tab['area_annuli'] = area_annuli
    return tab


def plotSBProfile(tab,flux_conversion_factor,texp,band,ax):
    # This function plots the surface brightness profile of the galaxy
    # Convert the instrumental flux within the annuli to standard fluxes. (Notice the arguments in this function.)
    correctedFlux = tab['flux_annuli'] * flux_conversion_factor
    correctedFluxErr = tab['fluxerr_annuli'] * flux_conversion_factor
    # Compute the surface brightness in mag/arcsec^2. (Hint: notice the arguments of this function.)
    mu = 2.5*np.log10(tab['area_annuli']*pixscale**2) - 2.5*np.log10(correctedFlux/texp) # surface brightness in mag/arcsec^2mu_err = np.abs((-2.5/correctedFlux)/np.log(10)*correctedFluxErr) # The errors using standard error propagation.
    # Compute the semi-major axis in arcsec.
    r_arcsec = tab['semi-major axis'] * pixscale
    # Use ax.errorbar() to plot the profile. Label the plot with the band argument.
    ax.errorbar(r_arcsec, mu, yerr= mu_err, label=band)
#----------------------------------------------------------------------------------------
# Function to plot galaxy showing ellipse of radius r. No need to modify this function.
def showEllipses(image_data_nosky,x,y,a,b,theta,r,newplot=False):
    if newplot:
    fig, ax = plt.subplots()
    norm = ImageNormalize(image_data_nosky,interval=ZScaleInterval()) # scales the image by same 'zscale' algorithm as
    ds9
    ax.imshow(image_data_nosky, cmap='gray',origin='lower',norm=norm)
    ax.set_xlim([700,1400])
    ax.set_ylim([700,1400])
    else: ax = plt.gca()
    # plot an ellipse for object with index idx
    e = Ellipse(xy=(x,y),
    width=r*a,
    height=r*b,
    angle=theta * 180. / np.pi)
    e.set_facecolor('none')
    e.set_edgecolor('red')
    ax.add_artist(e)
    #fig.savefig('detectedObjects_'+band+'.png')
    #plt.close()
    #return fig,ax
#===============================================================================
# This function calls all the functions you wrote above. It is very similar to
# assignment7/photometry.py. However, note that some of the functions have different outputs.
def getDataTable(band,ax,ext_coeff,refmag): # Note the arguments.
    tab = 0
    # These functions were unchanged from asssignment7/photometry.py
    hdu, image_data_nosky, texp, airmass = readImageData('NGC2841_nosky_'+band+'.fit')
    sky_data,skyrms = readSkyData('sky_'+band+'.fit')
    noise = computeNoise(image_data_nosky,sky_data,texp)
    # Debug by filling in these lines and commenting/uncommeting one by one as you finish each function
    objects,seg, seg_id = sourceExtraction(image_data_nosky,skyrms) # call sourceExtraction()
    getMags(image_data_nosky,objects,noise, texp, ext_coeff, airmass) # call getMags()
    flux_conversion_factor = calibrateRefStar(objects,refmag) # call calibrateRefStar()
    tab = galaxyProfile(image_data_nosky,noise,objects,seg,seg_id,band) # call galaxyProfile()
    plotSBProfile(tab,flux_conversion_factor,texp,band,ax) # call plotSBProfile()
    # Save the SB tables
    tab.write('SBtables_'+band+'.fits',overwrite=True)
    return tab
# Now run everything for each band. Note that plotSBProfile() plots the surface brightness
# profile for each band individually. We want them on the same plot. Therefore, create the
# plot and axis objects before calling getDataTable().
fig,ax = plt.subplots()# Notice that I have put in the extinction coefficients and magnitudes of the reference stars here.
BTable = getDataTable('PhotB',ax,ext_coeff=0.76,refmag=11.58)
VTable = getDataTable('PhotV',ax,ext_coeff=0.54,refmag=11.22)
RTable = getDataTable('PhotR',ax,ext_coeff=0.41,refmag=10.6)
# After all the profiles are plotted, finish up the plot
ax.set_ylabel('$\mu$ (mag/arcsec$^2$)')
ax.set_xlabel('r (arcsec)')
ax.set_title('Surface Brightness Profiles of NGC2841')
ax.invert_yaxis()
ax.legend()
fig.savefig('SBprofiles.png')