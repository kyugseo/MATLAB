#!/usr/bin/env python
# coding: utf-8

# In[8]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from astropy.io import fits
import glob
import matplotlib.pylab as plt


linearity_directory = '/data/kma81/Croissants/Linearity/'

def readexposures(directory):
	filelist = glob.glob(directory+'/*0001*')
	nfiles = len(filelist)
	t_exp = np.empty(nfiles) # will contain the exposure times of all the exposures
	meanADU = np.empty(nfiles) # will contain the mean ADU of each exposure
	for i, f in enumerate(filelist):
		hdu = fits.open(f)
		head=hdu[0].header
		t_exp[i]= head["EXPTIME"]
		image=hdu[0].data.astype('float')
		mean = np.mean(image)
		meanADU[i]=mean
        	
	return t_exp, meanADU

def plotlinearity(t_exp,meanADU):
	plt.plot(t_exp,meanADU,'.')
	plt.xlabel('Exposure Time')
	plt.ylabel('Mean ADUs')
	plt.savefig('linearity.png')
	plt.show()

def plotresiduals(t_exp,meanADU,indices):
	fit_t_exp = t_exp[indices[0]:indices[-1]]
	fit_meanADU = meanADU[indices[0]:indices[-1]]
	params,V = np.polyfit(fit_t_exp, fit_meanADU,1,cov=True)
	residuals = fit_meanADU - np.polyval(params,fit_t_exp)
	plt.plot(fit_t_exp,residuals,'k.')
	
	residualzero=[]	# for residual plot, to make horizontal line at zero 
	for i in range(len(indices)-1):
    		residualzero.append(0)
	plt.plot(fit_t_exp,residualzero, 'k:')
	plt.xlabel('Exposure time')
	plt.ylabel('Residual')
	plt.savefig('residuals.png')
	plt.show()

#----------------------------------------------------------------------------------------------
# main commands


t_exp, meanADU = readexposures(linearity_directory)
plotlinearity(t_exp, meanADU)
indices = np.array([2,3,4,5,6])
plotresiduals(t_exp,meanADU,indices)
index = np.array([2,3,4,5,6])

print("Approximate maximum ADU of the linear regime: ",meanADU[index])



