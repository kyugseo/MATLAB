import matplotlib.pyplot as plt
from astroML.datasets import fetch_sdss_spectrum
from scipy.optimize import curve_fit
import scipy.constants as constants
import numpy as np

# An example galaxy whose spectrum you're going to fit
plate,mjd,fiber = 1725,54266,527 

# Fetch the spectrum
spec = fetch_sdss_spectrum(plate=plate,mjd=mjd,fiber=fiber)
wavelength = spec.wavelength()
spectrum = spec.spectrum
error = spec.error

# Plot the spectrum as dots with error bars, with no line going through the points. 
# Label it "Data" (we'll use the label later in a legend)
plt.errorbar(wavelength, spectrum, yerr=error,marker='o',linestyle="None", label="Data")

# Label the axes, showing the appropriate units.  Look up 'SDSS spectrum units' to find the flux units.
plt.xlabel("Wavelength $(\AA)$")
plt.ylabel("Flux $(10^{-17} $erg cm$^{-2}$ s$^{-1}$ $\AA^{-1}$)")

# Zoom into the NII-Ha region of the plot so that you only show those lines.  
# Change the axis limits to this region.
plt.xlim([7100,7170])

# Rest-frame wavelengths of the 3 lines of the NII-Ha region in Angstroms
lam_NII_B = 6549.86  # the "_B" means the NII line on the blue side
lam_Ha = 6564.61 
lam_NII_R = 6585.27  # the "_R" means the NII line on the red side

# This part of the spectrum is a function f(lambda) that is the sum of:
#    1. An approximately horizontal stellar continuum (1 parameter: the continuum level)
#    2. A gaussian for the NII 6550 line (3 paramters: the amplitude, the centre and the width sigma)
#    3. A gaussian for the Ha line (3 paramters: the amplitude, the centre and the width sigma)
#    4. A guassian for the NII 6585 line (3 paramters: the amplitude, the centre and the width sigma)
# At first this looks like a function with 10 parameters, however we know the rest-frame centres of each 
# of the gaussians (the wavelengths defined above).  What we don't know is the redshift of these centres.
# Therefore our f(lambda) has 8 parameters (continuum level, 3 amplitudes, 3 sigmas and the redshift)
# We're going to fit this function f(lambda) with 8 parameters to the data using curve_fit.  

# But before we define it, notice that we have to create a gaussian three times.  
# Therefore let's define the gaussian function first.
def gaussian(wavelength,amplitude,wave_centre,sigma):
    f = amplitude*np.exp(-0.5*((wavelength-wave_centre)/sigma)**2)
    return f

# Now let's define our fitting function (our f(lambda)).  The arguments of this function should
# include the wavelength as the first argument, and then the 8 parameters described above.
def fitfunction(wavelength, cont_level, amp1, amp2, amp3, sig1, sig2, sig3, redshift):
    
    # Find the redshifted centres of the three lines
    lam_NII_B_redshifted = lam_NII_B*(redshift + 1)
    lam_Ha_redshifted = lam_Ha*(redshift + 1)
    lam_NII_R_redshifted = lam_NII_R*(redshift + 1)
    
    # Add the four parts of the spectrum (continuum + 3 gaussians)
    spec = cont_level*np.ones(len(wavelength)) # Approximate the continuum as a constant array of the same size as the wavelength array
    spec += gaussian(wavelength,amp1,lam_NII_B_redshifted,sig1) # Add the 3 gaussians
    spec += gaussian(wavelength,amp2,lam_Ha_redshifted,sig2)
    spec += gaussian(wavelength,amp3,lam_NII_R_redshifted,sig3)
    return spec

# We don't want to fit the whole spectrum, just the range that contains the 3 lines.  Use the
# plot limits that you used above to create a mask on the spectrum data
maskfit = (wavelength>=7100) & (wavelength <= 7170) # the mask on the spectrum data
x = wavelength[maskfit]
y = spectrum[maskfit]
err = error[maskfit]

# Look at your plot to estimate starting values for the continuum and the redshift.  The starting 
# values of the other parameters are not very important.
continuum_start = 25
redshift_start = (7125-lam_Ha)/lam_Ha

# List of 8 starting values (use 1 for the amplitudes and sigmas).  The order will depend on how you 
# ordered them in the arguments to fitfunction.
p0 = [continuum_start, 1, 1, 1, 1, 1, 1, redshift_start] # List of 8 starting values

# Run curve_fit using the fit function, x, y, err and the list of starting values
popt, pcov = curve_fit(fitfunction, x, y, p0, err) # popt is the array of best-fit parameters

# Plot the model as a line plot and label it "Model"
modelspace = np.linspace(x[0], x[-1], 1000)
plt.plot(modelspace, fitfunction(modelspace, *popt), '-', label="Model")

# Create the legend.
plt.legend()

# Now we're going to label the plot with the best-fit parameters

# Grab these best-fit parameters from popt (this will depend on what order you put the parameters
# in the arguments of fitfunction)
continuumLevel,z = popt[0], popt[-1] # The continuum level and redshift
amp_NII_B,amp_Ha,amp_NII_R = popt[1], popt[2], popt[3] # The amplitudes of the 3 gaussians
sig_NII_B,sig_Ha,sig_NII_R = popt[4], popt[5], popt[6] # The sigmas of the 3 gaussians

# Determine the recession velocity of this galaxy in km/s
vel_recession = constants.c*z/1e3

# Determine the total flux in the Ha line using the best-fit parameters
Ha_flux = amp_Ha*sig_Ha*np.sqrt(2*np.pi)

# Determine the sum of the flux in the two NII lines using the best-fit parameters
NII_flux =  (amp_NII_B*sig_NII_B+amp_NII_R*sig_NII_R)*np.sqrt(2*np.pi)

# Determine the ratio of the NII to Ha flux
NII_Ha_ratio = NII_flux/Ha_flux

# Create the label containing the quantities you just computed
label = r'Redshift: '+str(np.round(z,5))
label += '\n' # new line
label += r'Recession velocity: '+str(int(vel_recession))+ ' km/s'
label += '\n' # new line
label += r'[NII]/H$\alpha$ flux ratio: '+str(np.round(NII_Ha_ratio,2))

# This line puts the label as text at the position that corresponds to 2% of the x-axis length 
# and 80% of the y-axis length.
plt.text(0.02,0.8,label,transform=plt.gca().transAxes) 

plt.savefig('SpectrumFit.png')