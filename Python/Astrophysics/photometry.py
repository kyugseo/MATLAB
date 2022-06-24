import numpy as np
from astropy.io import fits
import sep
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.wcs import WCS
import warnings
warnings.filterwarnings('ignore')

#plt.ion()

def readImageData(f):
    # This function receives the filename f and reads the image data.  
    # Along with the image data, from the header, read the exposure time and the average air mass (fits header card "AVGAIRMS")
    hdu = fits.open(f) # Open the file 
    image_data =  hdu[0].data # get the data, and assign to image_data (after calibration they're already floats)
    texp=hdu[0].header["EXPTIME"]
    airmass=hdu[0].header["AVGAIRMS"]
    # You may or may not need the following line.  
    image_data = image_data.byteswap(inplace=True).newbyteorder() 
    return hdu, image_data, texp, airmass # outputs the hdu, the image data, the exposure time and the average air mass

def readSkyData(f):
    # This function receives the filename f and reads the sky data.  
    # From the header, read the background rms value that we saved (card "GLOBLRMS") when we measured the sky in Assignment 6
    hdu = fits.open(f)
    skyrms = hdu[0].header['GLOBLRMS']
    sky_data = hdu[0].data.astype("float")

    return sky_data, skyrms # outputs the sky data and the global rms of the background

def computeNoise(image_data_nosky,sky_data,texp):
    # This function computes the total noise in units of ADUs.  Asside from the image data and sky data, you will also need:
    #- gain
    #- read noise
    #- dark current # -> use the master dark file you created in Assignment 4
    # The total noise is the sum (in quadrature) of 4 sources of noise: the read noise, the dark noise, the sky noise and the data noise
    
    # 1. Declare the gain and read noise (in electrons)
    gain = 1.5
    noise_read = 19 
    
    # 2. Read the master dark data from Assignment 4 and compute the Poision noise (in electrons)
    hdu =  fits.open('../assignment4/MasterDark.fit') # Open the master dark file from assignment 4
    MasterDark = hdu[0].data.astype('float') # Assign the dark data to MasterDark
    noise_dark = np.mean(np.sqrt(gain*np.abs(MasterDark))) # Compute the Poisson noise due to the dark current (in electrons); take the absolute value first since some pixels are negative

    # 3. Compute the Poisson noise of the sky in electrons
    noise_sky = np.sqrt(gain*np.abs(sky_data))
    # 4. Compute the Poisson noise of the sky-subtracted image in electrons
    noise_nosky = np.sqrt(gain*np.abs(image_data_nosky)) 

    # 5. Total noise: add the image noise, sky noise, dark noise and read noise in quadrature.  Note that the dark noise defined above
    # is the dark noise per second.  Make sure to scale it up by the exposure time.
    noise = np.sqrt(noise_nosky**2 + noise_sky**2 + texp*noise_dark**2 + noise_read**2)

    # 6. Turn the noise back into units of ADU
    noise = noise/gain
    return noise # Return the noise in units of ADU

def sourceExtraction(image_data_nosky,skyrms):
    # In this function each "..." is a single line
    # Use sep.extract to find all the objects in image_data_nosky that are 2-sigma above the background,
    # where sigma (err) is the skyrms (follow the example in the slides)
    objects = sep.extract(image_data_nosky, 2, err=skyrms)
    
    # Get the dimensions of image_data_nosky
    ny,nx = np.shape(image_data_nosky)

    # We are going to keep only those objects whose light-weighted centres are more than 30 pixels
    # away from the edge of the image.  objects['x'] and objects['y'] are the pixel coordinates of
    # the light-weighted centres.  The following illustrates how masks are used to select a subset
    # of an array or table.
    mask = (objects['x'] > 30) & (objects['x'] < nx-30) & (objects['y'] > 30) & (objects['y'] < ny-30)
    objects = objects[mask] # Here we've overwritten "objects" with a subset that fulfill the above criteria

    return objects # Return the structured array of objects

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
    mag -=  ext_coeff*airmass
    
    return mag, mag_err, sn, flag # Return the magnitudes, magnitude errors, S/N and the flag


def constructDataTable(hdu,objects,mag,mag_err,sn,flag):
    # This function constructs an astropy table using the numpy structured array "objects" and adds the magnitudes and
    # RA and DEC as extra columns.  It then removes bad stars from the table.
    
    # get WCS of each object (see slide 17 of Lecture 6)
    w = WCS(hdu[0].header)
    coords = w.pixel_to_world(objects['x'], objects['y'])

    # Create the Table 
    tab = Table(objects) # inherits all the columns of objects
    
    # Add extra columns like this:
    tab['ra'] = coords.ra
    tab['dec'] = coords.dec
    tab['mag_inst'] = mag 
    tab['mag_inst_err'] = mag_err

    # Remove bad stars
    print("Number of saturated stars: ",np.sum(objects['peak'] > 55000)) 
    # Keep only those stars with S/N > 5, flag < 8, unsaturated stars and stars that are circular (not elongated):
    mask = (sn > 5) & (flag < 8) & (objects['peak'] < 55000) & (objects['b']/objects['a'] > 0.5)
    tab = tab[mask]

    return tab

#--------------------------------------------------------------------------------------------------
def matchTables(listofTables,bands):
    # A handy package in astropy will match stars in different catalogues based on their RA and DEC
    # This function requires some tricky use of masks, indices and astropy Tables.
    # Therefore I have written it for you and you do not need to modify it.

    refTable = listofTables[0] # the reference table against which the other tables will be matched
    masterTable = refTable['ra','dec','x','y'] # select only the coordinate information from the first table

    # Get the sky coordinates of all the objects in the reference table
    coords = SkyCoord(ra=refTable['ra'], dec=refTable['dec'])

    # Initialize the magnitude and error columns
    for band in bands: 
        masterTable['mag_inst_'+band] = np.repeat(np.nan,len(refTable))
        masterTable['mag_inst_err_'+band] = np.repeat(np.nan,len(refTable))

    # Use astropy Skycoord to match the objects by RA/DEC
    for band,table in zip(bands,listofTables):
        coords_other = SkyCoord(ra=table['ra'], dec=table['dec'])
        indmatch, d2d, d3d = coords.match_to_catalog_sky(coords_other) # d2d is the separation in degrees
        mask = d2d.value*3600.0 < 2.0 # use only those that match within less than 2 arcsec
        masterTable['mag_inst_'+band][mask] = table['mag_inst'][indmatch[mask]]
        masterTable['mag_inst_err_'+band][mask] = table['mag_inst_err'][indmatch[mask]]

    return masterTable



#===============================================================================
# This function calls all the functions you wrote above (but not matchTables)
def getDataTable(band,ext_coeff):
    tab = 0
    # Uncomment these lines one by one as you finish each function above.
    hdu, image_data_nosky, texp, airmass = readImageData('../assignment6/M52_nosky_'+band+'.fit')
    sky_data,skyrms = readSkyData('../assignment6/sky_'+band+'.fit')
    noise = computeNoise(image_data_nosky,sky_data,texp)
    objects = sourceExtraction(image_data_nosky,skyrms)
    mag, mag_err, sn, flag = getMags(image_data_nosky,objects,noise,texp,ext_coeff,airmass)
    tab = constructDataTable(hdu,objects,mag,mag_err,sn,flag)

    return tab

# Get the data table for all three bands
# Use the extinction coefficents measured in assignment 5, but in principle they vary from night to night!
VTable = getDataTable('PhotV',ext_coeff=0.54)
BTable = getDataTable('PhotB',ext_coeff=0.76)
RTable = getDataTable('PhotR',ext_coeff=0.41)

# When you're done editing the functions above, COMMENT THE FOLLOWING LINE to make the colour-magnitude diagram of the cluster
#exit('Success!  Edit the next function') # This line tells python to stop running the rest of the code, and outputs a message.

#------------------------------------------------------------------------------------
# Since the images in the different bands have different detection limits, the tables VTable, BTable and RTable
# have different numbers of detected stars in them.  
# In order to make a colour-magnitude diagram, we will have to match the objects to each other.
print("Number of objects detected in the V band image:", len(VTable))
print("Number of objects detected in the B band image:", len(BTable))
print("Number of objects detected in the R band image:", len(RTable))

listofTables = [VTable,BTable,RTable] # put the three tables in a list
bands = ['PhotV','PhotB','PhotR'] # bands in the same order as the listofTables

# Call matchTables which I wrote for you above
masterTable = matchTables(listofTables,bands)

# Save the masterTable into a fits file.  Yes, fits files hold data tables too, not just images!
masterTable.write('masterTable.fits',overwrite=True)

#------------------------------------------------------------------------------------
# Now plot the V instrumental magnitude vs instrumental B-V colour:
bminusv = masterTable['mag_inst_PhotB'] - masterTable['mag_inst_PhotV']
vmag_inst = masterTable['mag_inst_PhotV']
plt.plot(bminusv,vmag_inst,'.')
plt.xlabel('b-v instrumental colour')
plt.ylabel('v instrumental magnitude')
plt.gca().invert_yaxis() # invert the y-axis because we want "bright" to be at the top
plt.title('Instrumental Colour-Magnitude Diagram of M52')
plt.savefig('cmd_instrumental.png')
