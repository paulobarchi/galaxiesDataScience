# cutGalaxyFromFits.py
# cut desired galaxy from fits field
# input: field fits file, galaxy x center, galaxy y center, petroRad in pixels, stamp size in petroRads,
# 		output file name
# output: fits file with galaxy stamp

import sys
import astropy.io.fits as fits
import numpy as np
from math import fabs
import pyfits

# read inputs
data = pyfits.getdata(sys.argv[1], 0)
x = int(sys.argv[2])
y = int(sys.argv[3])
petroRad = float(sys.argv[4])
halfSize = float(sys.argv[5])/2.0

# calc output data dimensions
sizy = np.min(np.array([fabs(x),(halfSize)*fabs(petroRad), fabs(data.shape[0]-x)]))
sizx = np.min(np.array([fabs(y),(halfSize)*fabs(petroRad), fabs(data.shape[1]-y)]))
siz = int(np.min(np.array([sizy,sizx])))

data = data[y-siz:y+siz+1,x-siz:x+siz+1] 

if (siz < int((halfSize)*fabs(petroRad))):
	print "Warning: got stamp size smaller than desired."
	print 'siz: ' + str(siz) + '; desired: ' + str(int((halfSize)*fabs(petroRad)))

pyfits.writeto(sys.argv[6], data, clobber=True) # save fit to clean