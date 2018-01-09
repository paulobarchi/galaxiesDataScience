# createImgsFromFits.py
# Create images (pngs) from galaxy and masks fit(s).
# input: input path, extension of files and output path.
# output: galaxy and masks images (pngs).

import sys
import os
from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

def getFileNameAndExtension(file):
	return file.split(".")[0], file.split(".")[1]

def saveAndClearPlot(filename):
	plt.tick_params(
			axis='both', 
			which='both', 
			bottom='off', 
			top='off', 
			labelbottom='off', 
			right='off', 
			left='off', 
			labelleft='off')
	plt.savefig(filename)
	plt.clf()

input_path = sys.argv[1] # must be with "/" after
extension = sys.argv[2] # must be with "." before
output_path = sys.argv[3] # must be with "/" after

# for each fit file in directory
for file in os.listdir(input_path):
	if file.endswith(extension):
		# save filtered png from stamp <objId>_<extension>.png
		image_data = fits.getdata(input_path+file)
		plt.imshow(image_data, cmap='gray', 
			# norm=colors.LogNorm(vmin=np.median(image_data),vmax=np.median(image_data)+100))
			norm=colors.LogNorm(vmin=np.median(image_data),vmax=np.percentile(image_data,90)))
		filename, extension = getFileNameAndExtension(file)
		saveAndClearPlot(output_path + filename + "_" + extension + ".png")		

		# save png of old mask <objId>_oldMask.png --> same, without filter
		oldMask_data = fits.getdata(input_path+"old--beforeBugFix/"+filename+"/mask.fit")
		plt.imshow(oldMask_data, cmap='gray')
		saveAndClearPlot(output_path + filename + "_oldMask.png")

		# save png of new mask <objId>_newMask.png --> same, without filter
		newMask_data = fits.getdata(input_path+"new--afterBugFix/"+filename+"/mask.fit")
		plt.imshow(newMask_data, cmap='gray')		
		saveAndClearPlot(output_path + filename + "_newMask.png")
		
