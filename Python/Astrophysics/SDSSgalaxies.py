import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from astropy.cosmology import FlatLambdaCDM
from astropy.table import Table
import SciServer.CasJobs as CasJobs # query with CasJobs, the primary database for the SDSS
import SciServer.SkyServer as SkyServer # show individual objects through SkyServer

#----------------------------------------------------------------------------------------------
# Do not modify the following function
def getDistance(z):
    # This function converts a redshift z into a distance in kpc ("luminosity distance" to be exact).
    # To convert redshift z to a distance, you need to to know some cosmology (PHYS 390). 
    cosmo = FlatLambdaCDM(name='Concordance',H0=67.4,Om0=0.315,Tcmb0=2.726, Neff=2.99, Ob0=0.0493)
    comd = cosmo.comoving_distance(z).value*1.0e3 # Comoving distance in kpc
    dist = (1.0+z)*comd # This is the "luminosity distance" in kpc
    return dist # kpc

#----------------------------------------------------------------------------------------------


# Write an SQL query that selects the objID, ra, dec, the ugriz magnitudes and redshifts from the 
# Galaxy and SpecObj tables.  Select only those galaxies whose redshifts are between 0.05 and 0.1,
# and whose r-band and g-band magnitudes are between 14 and 17.  These limits will keep the counts 
# to below 100000, so there's no need to use the "TOP"
# export HTTPS_PROXY=http://bby-nsx-proxy.its.sfu.ca:8080
query= """
SELECT p.objID,p.ra,p.dec,p.u,p.g,p.r,p.i,p.z,s.z as redshift
    FROM Galaxy As p
    JOIN SpecObj As s ON s.bestObjID = p.objID
WHERE s.z BETWEEN 0.05 AND 0.1
    AND p.r BETWEEN 14 and 17
    AND p.g BETWEEN 14 and 17
"""

# send query to CasJobs
galaxyTable = CasJobs.executeQuery(query,'dr16')
galaxyTable = Table.from_pandas(galaxyTable) # Convert to astropy table

# Define a few variables 
gal_col = galaxyTable["g"] - galaxyTable["r"]# The g-r colour index
z = galaxyTable["redshift"] # The redshift
dist = getDistance(z) *1000 # The distance in pc (use the function I wrote for you above)

gal_mag = galaxyTable['r']-2.5*np.log10((dist/10)**2) # The absolute magnitude in the r-band


# Let's plot the CMD of galaxies with dots and see how crowded it is. 
# (colour on the y-axis, absolute magnitude on the x-axis)
# Make sure the magnitude axis is plotted such that brightness increases along that axis.
# Don't forget to label the axes. (Hint: to use subscripts, surround your label with $-signs and 
# use underscore before the subscript.  Eg. '$X_y$' is X with a y subscript)
plt.scatter(gal_mag,gal_col)

# Use the magnifying glas and your mouse to zoom in on the region of the plot where the bulk of 
# the points are.  Note that the sharp diagonal "cut" on the *dim* end of the plot is artificial, 
# and is due to our dim limit of 17 in both the r and g bands.  Zoom in so that your plot 
# *excludes* that cut.  So your dimmest r-band absolute magnitude will be about -21.
# Write down the approximate axis limits.  
plt.ylabel("g-r Colour Index")
plt.xlabel("Absolute Magnitude, $M_r$")
plt.ylim(0.2,1.2)
plt.xlim(-21,-24)
plt.savefig('CMD_dots.png')
plt.show()
plt.close()

 
# As you can see, the plot is pretty crowded.  Therefore, let's make a "2D histogram" which is 
# the same plot colour-coded by the number of galaxies in that region of the plot.  
# 1. Use plt.hist2d().  Look up the documentation on plt.hist2d() to understand how to use it.
# 2. Use the keyword "range" such that the range corresponds to the axis limits you wrote down earlier.
# 3. Use the keyword "cmap" to change the colour map such that 0 points corresponds to a white colour.  
#    Google "matplotlib colour maps" to get a list of available colour maps
# 4. The default is to divide the plot into 10x10 bins (pixels) to colour-code the mapt.  
#    Use the "bins" keyword to adjust the number of bins to get finer detail.  
# 5. Add a color bar and label it "Number of galaxies" (keyword label).
# 6. Don't forget to label the axes and make sure brightness increases along the magnitude axis.

plt.hist2d(gal_mag,gal_col,bins=50,range=[[0.2,1.2],[-23.0,-21.0]],cmap='Purples')
ax = plt.colorbar()
ax.set_label('Number of galaxies')
plt.ylabel("g-r Colour Index")
plt.xlabel("Absolute Magnitude, $M_r$")
plt.ylim(0.2,1.2)
plt.xlim(-21,-24)
plt.close()
# It's hard to see the galaxy bimodality when using linear counts as the colour scale.  Let's change 
# the colour scale to map logarithmic counts. a
# 1. Copy the lines you wrote to make the last plot.  
# 2. Then in the plt.hist2d() line, add the "norm" keyword to use the LogNorm() function we imported at 
#    the beginning.
# 3. Change the savefig line to save the file as 'CMD_logcounts.png'  

plt.hist2d(gal_mag,gal_col,bins=50,range=[[-24,-21],[0.2,1.2]],norm=LogNorm(),cmap='Purples')
ax = plt.colorbar()
ax.set_label('Number of galaxies')
plt.ylabel("g-r Colour Index")
plt.xlabel("Absolute Magnitude, $M_r$")
plt.ylim(0.2,1.2)
plt.xlim(-21,-24)
plt.savefig('CMD_logcounts.png')
plt.close()

# Let's create masks to select a small rectangular region of the plot inside the red sequence (RS), 
# and a small rectangular region of the plot inside the blue cloud (BC).  We will use these masks to 
# grab some cutout images of those galaxies to see what typical RS and BC galaxies look like. 
# Use conditions on the absolute r magnitude and on the colour index to create these masks.
# Tip: don't pick from the dimmest ones.  They won't look impressive in the images.
maskRSbox = []
maskRSleft = gal_mag < -22.3
maskRSright = gal_mag < -22.0
maskRStop = gal_col < 0.9
maskRSbottom = gal_col < 0.86
for i in range(len(maskRSleft)):
    if maskRSleft[i] == True and maskRSright[i] == True and maskRStop[i] == True and maskRSbottom[i]==True:
        maskRSbox.append(True)
    else:
        maskRSbox.append(False)
maskRSbox =np.array(maskRSbox)
        
maskBCbox = []
maskBCleft = gal_mag < -22.2
maskBCright = gal_mag < -21.8
maskBCtop = gal_col < 0.64
maskBCbottom = gal_col < 0.6


for i in range(len(maskBCleft)):
    if maskBCleft[i] == True and maskBCright[i] == True and maskBCtop[i] == True and maskBCbottom[i]==True:
        maskBCbox.append(True)
    else:
        maskBCbox.append(False)
maskBCbox =np.array(maskBCbox)

# Save the masks into new columns of galaxyTable
galaxyTable['maskRSbox'] = maskRSbox
galaxyTable['maskBCbox'] = maskBCbox

# Save the galaxyTable for future use
galaxyTable.write('SDSS_galaxies.fits',overwrite=True)

# Use Rectangle (imported above) to plot your regions on your graph.  Rectangle wants the lower
# x and y coordinates (xstart and ystart), and then the width and height of the rectangle to draw.

# Rectangle parameters for the RS:
xstart,ystart = [-22.0,0.86]
width,height = [0.03,0.04]
plt.gca().add_patch(Rectangle((xstart,ystart),width,height,fill=False,edgecolor='red'))

# Rectangle parameters for the BC: 
xstart,ystart = [-21.8,0.6]
width,height = [0.03,0.04]
plt.gca().add_patch(Rectangle((xstart,ystart),width,height,fill=False,edgecolor='blue'))
plt.ylim(0.2,1.2)
plt.xlim(-21,-24)
plt.savefig('CMD_logcounts_boxes.png')
plt.close()

        
# Now let's grab a random 16 galaxies from the boxes we drew above.  Since we're doing this twice,
# let's write a function and then call it twice.
def plotImages(mask,galaxyTable):
    # This function downloads a random 16 images from the SDSS.  galaxyTable should contain ra and dec,
    # and mask is the subset of galaxyTable that you want to draw the 16 galaxies from.  (We will call this 
    # function once using maskRSbox, and once using maskBCbox.)
    
    # Set up a plot of 4x4 subplots (look up the documentation for plt.subplots).  The size of the canvas
    # should be 10x10 (keyword figsize).
    fig,ax = plt.subplots(4,4,figsize = (10,10))   # There should be 4x4 subplots
    
    # The "ax" output from plt.subplots() is a 4x4 array reprepsenting the 16 subplots.  We'll need
    # to flatten the array in order to use it easily in the loop below.
    ax = ax.flatten()

    # Find all the indices of the mask where mask is True.  (Use np.where)
    ind_all = np.where(mask==True) # This is the array of indices where mask is True
    ind_all = ind_all[0] # np.where() returns a tuple containing the array of indices.  The [0] just selects
                         # the array of indices so that ind_all becomes the array instead of the tuple containing
                         # the array.
    
    # Select 16 random galaxies from mask using np.random.choice().  Use the keyword replace=False.
    indpick = np.random.choice(ind_all,16,replace=False) # These are 16 random indices selected from ind_all
    
    
    for i,a in zip(indpick,ax): # i runs through the indices in indpick, and a runs through the subplots in ax
        #print('Getting image '+str(i)+' of 16 ...')
        
        # Download the image 
        ra = galaxyTable['ra'][i] # get the ra value of the current index
        dec =galaxyTable['dec'][i]# get the dec value of the current index
        img= SkyServer.getJpegImgCutout(ra=ra, dec=dec, width=100, height=100) # width, height in pixels
        
        # Plot using imshow
        a.imshow(img)# Plot the downloaded image using imshow in the ***current subplot***
        a.axis('off') # Turn off the ticks and labels

        # Set the title to be the objID of the current galaxy, using fontsize=10
        objID = galaxyTable[i]['objID'] # objID of the current galaxy
        a.set_title(objID,fontsize=10) # use the set_title method to set the title of the subplot with fontsize=10

        fig.tight_layout()
    return fig  # Output the fig object so that we can save the figure


# Now call the function you just wrote.
plotImages(maskRSbox,galaxyTable) # Call plotImages using maskRSbox
plt.savefig("RS_Galaxies.png") # Save the figure as "RS_Galaxies.png"

plotImages(maskBCbox,galaxyTable)  # Call plotImages using maskBCbox
plt.savefig("BC_Galaxies.png") # Save the figure as "BC_Galaxies.png"
