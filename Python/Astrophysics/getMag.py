

import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
import glob
import sep
from astropy.wcs import WCS
from astropy.io import fits
from astropy.coordinates import SkyCoord

nosky_dir= '../mydata/ContactBinary_nosky/'
calibrated_dir = '../mydata/ContactBinary_calibrated/'
filelist = glob.glob(nosky_dir+'*')
magV=[]
magV_err=[]
times=[]

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

def computeNoise(image_data_nosky,sky_data,texp):
    # This function computes the total noise in units of ADUs.  Asside from the image data and sky data, you will also need:
    #- gain
    #- read noise
    #- dark current # -> use the master dark file you created in Assignment 4
    # The total noise is the sum (in quadrature) of 4 sources of noise: the read noise, the dark noise, the sky noise and the data noise
    
    # 1. Declare the gain and read noise (in electrons)
    gain = 1.5
    noise_read = 19 
    
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
    return noise

def readImageData(f):
    # This function receives the filename f and reads the image data.  
    # Along with the image data, from the header, read the exposure time and the average air mass (fits header card "AVGAIRMS")
    hdu = fits.open(f) # Open the file 
    image_data =  hdu[0].data # get the data, and assign to image_data (after calibration they're already floats)
    texp=hdu[0].header["EXPTIME"]
    airmass=hdu[0].header["AIRMASS"]
    JD=hdu[0].header["JD"]
    
    # You may or may not need the following line.  
    image_data = image_data.byteswap(inplace=True).newbyteorder() 
    return hdu, image_data, texp, airmass, JD


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

    return objects

def readSkyData(f):
    # This function receives the filename f and reads the sky data.  
    # From the header, read the background rms value that we saved (card "GLOBLRMS") when we measured the sky in Assignment 6
    hdu = fits.open(f)
    skyrms = hdu[0].header['GLOBLRMS']
    sky_data = hdu[0].data.astype("float")

    return sky_data, skyrms # outputs the sky data and the global rms of the background
def constructDataTable(hdu,objects,mag,mag_err,sn,flag):
    # This function constructs an astropy table using the numpy structured array "objects" and adds the magnitudes and
    # RA and DEC as extra columns.  It then removes bad stars from the table.
    
    # get WCS of each object (see slide 17 of Lecture 6)
    w = WCS(hdu[0].header)
    coords = w.pixel_to_world(objects['x'], objects['y'])

    # Create the Table 
    tab = Table(objects) # inherits all the columns of objects
    
    # Add extra columns like this:

    tab['magV'] = magV
    tab['mag_inst_err'] = mag_err

    # Remove bad stars
    print("Number of saturated stars: ",np.sum(objects['pea'] > 55000)) 
    # Keep only those stars with S/N > 5, flag < 8, unsaturated stars and stars that are circular (not elongated):
    mask = (sn > 5) & (flag < 8) & (objects['peak'] < 55000) & (objects['b']/objects['a'] > 0.5)
    tab = tab[mask]

    return tab

def matchTables(listofTables):
    # A handy package in astropy will match stars in different catalogues based on their RA and DEC
    # This function requires some tricky use of masks, indices and astropy Tables.
    # Therefore I have written it for you and you do not need to modify it.

    refTable = listofTables[0] # the reference table against which the other tables will be matched
    masterTable = refTable['ra','dec','x','y'] # select only the coordinate information from the first table

    # Get the sky coordinates of all the objects in the reference table
    coords = SkyCoord(ra=refTable['ra'], dec=refTable['dec'])

    # Initialize the magnitude and error columns

    masterTable['magV'] = np.repeat(np.nan,len(refTable))
    masterTable['mag_inst_err'] = np.repeat(np.nan,len(refTable))

    # Use astropy Skycoord to match the objects by RA/DEC
    for table in (listofTables):
        coords_other = SkyCoord(ra=table['ra'], dec=table['dec'])
        indmatch, d2d, d3d = coords.match_to_catalog_sky(coords_other) # d2d is the separation in degrees
        mask = d2d.value*3600.0 < 2.0 # use only those that match within less than 2 arcsec
        masterTable['magV'][mask] = table['magV'][indmatch[mask]]
        masterTable['mag_inst_err'][mask] = table['mag_inst_err'][indmatch[mask]]

    return masterTable

def getMags(image_data_nosky,objects,noise, texp, ext_coeff, airmass):
    
    kronrad, krflag = sep.kron_radius(image_data_nosky, objects['x'], objects['y'], objects['a'], objects['b'],
                                      objects['theta'], 6.0)
    
    flux, fluxerr, flag= sep.sum_ellipse(image_data_nosky, objects['x'], objects['y'], objects['a'], 
                                    objects['b'], objects['theta'], 2.5*kronrad, subpix=1, err=noise)
    if texp ==0:
        mag=0
    else:
        mag = -2.5*np.log10(flux/texp)
    mag_err = 2.5*fluxerr/flux/np.log(10)
    sn = flux/fluxerr
    
    return mag, mag_err, sn, flag 

filelist = glob.glob(calibrated_dir+'*')

ext_coeff=0.54 
for f in filelist:
    filename = f[f.rfind('/')+1:] 
    hdu, image_data_nosky, texp, airmass, JD = readImageData('../mydata/ContactBinary_nosky/nosky_'+filename)
    sky_data,skyrms = readSkyData('../mydata/ContactBinary_sky/sky_'+filename)
    objects = sourceExtraction(image_data_nosky,skyrms)
    noise = computeNoise(image_data_nosky,sky_data,texp)
    mag, mag_err, sn, flag = getMags(image_data_nosky,objects,noise, texp, ext_coeff, airmass)
    
    times.append(JD)
    

    print(magV)
    exit()



def getDataTable(ext_coeff):
    tab=0
    # Uncomment these lines one by one as you finish each function above.
    for f in filelist:
        filename = f[f.rfind('/')+1:] 
        hdu, image_data_nosky, texp, airmass,JD = readImageData('../mydata/ContactBinary_nosky/nosky_'+filename)
        sky_data,skyrms = readSkyData('../mydata/ContactBinary_sky/sky_'+filename)
        noise = computeNoise(image_data_nosky,sky_data,texp)
        objects = sourceExtraction(image_data_nosky,skyrms)
        mag, mag_err, sn, flag = getMags(image_data_nosky,objects,noise,texp,ext_coeff,airmass)
        times.append(JD)    
        Vmag_offset = 11.46 - mag
        magV = -2.5*np.log10(Vmag_offset/11.46)
        tab = constructDataTable(hdu,objects,magV,mag_err,sn,flag)
    return tab

VTable = getDataTable(ext_coeff=0.54)

listofTables = [VTable] # put the three tables in a list
bands = ['PhotV'] # bands in the same order as the listofTables

# Call matchTables which I wrote for you above
masterTable = matchTables(listofTables)

# Save the masterTable into a fits file.  Yes, fits files hold data tables too, not just images!
masterTable.write('masterTable.fits',overwrite=True)

#------------------------------------------------------------------------------------
# Now plot the V instrumental magnitude vs instrumental B-V colour:

vmag_inst = masterTable['mag_inst_PhotV']
