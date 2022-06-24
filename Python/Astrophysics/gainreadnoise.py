#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from astropy.io import fits
import glob
import matplotlib.pylab as plt

bias_directory = '/data/kma81/Croissants/Bias/'
linearity_directory = '/data/kma81/Croissants/Linearity/'

# Choose 2 bias files in the bias directory and write their names in a list:
biasfiles = ['BIAS-0010.fit','BIAS-0009.fit']

# Choose 2 dome files in the linearity directory that have the ***same exposure time***.
# (This is where the suffixes on the file names will come in handy).'
# Refer to your linearity.png plot that you made in Part 2 and choose an exposure time that
# gives a mean ADU in the 40000-range. Write their names in a list.
domefiles = ['DOME-0001_24s.fit','DOME-0002_24s.fit']

# Extract the data from the bias images into the arrays bias1 and bias2.
# Make sure they are converted to float arrays.
hdu1 = fits.open('/data/kma81/Croissants/Bias/BIAS-0010.fit')
hdu2 = fits.open('/data/kma81/Croissants/Bias/BIAS-0009.fit')
bias1 = hdu1[0].data.astype('float')
bias2 = hdu2[0].data.astype('float')
B1= np.mean(bias1)
B2= np.mean(bias2)


# Extract the data from the dome images into the arrays dome1 and dome2.
# Make sure they are converted to float arrays.
hdu3 = fits.open('/data/kma81/Croissants/Linearity/DOME-0001_24s.fit')
hdu4 = fits.open('/data/kma81/Croissants/Linearity/DOME-0002_24s.fit')
dome1 = hdu3[0].data.astype('float')
dome2 = hdu4[0].data.astype('float')
F1= np.mean(dome1)
F2= np.mean(dome2)

# Use the equations in Lecture 3 to derive the gain of the CCD:
# (dome1 and dome2 can be used instead of flats - they don't have to be flat)
# (B1-B2 and F1-F2)

diff_B = bias1 -bias2
sigmaB = np.var(diff_B)
diff_F=dome1-dome2
sigmaF= np.var(diff_F)

print (F1+F2)
print(B1+B2)

gain = (F1+F2-B1-B2)/(sigmaF**2-sigmaB**2)

print('The CCD gain is: ',gain)

# Now compute the read noise in electrons
readnoise = (gain*np.sqrt(sigmaB/2))
print('The CCD read noise is ',readnoise,' electrons')

