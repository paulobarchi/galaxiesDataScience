# fits2img.py
# Get visualizable pngs from fit(s) file.
# input: input path with fits, extension (.fit or .fits) and output path
# output: filtered image files (.png)

import sys
import os
from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

def getFileNameAndExtension(file):
	return file.split(".")[0], file.split(".")[1]

input_path = sys.argv[1]
extension = sys.argv[2]
output_path = sys.argv[3]

for file in os.listdir(input_path):
	if file.endswith(extension):
		image_data = fits.getdata(input_path+file)
		plt.imshow(image_data, cmap='gray', 
			norm=colors.LogNorm(vmin=np.median(image_data),vmax=np.median(image_data)+100))
			# norm=colors.LogNorm(vmin=np.median(image_data),vmax=np.percentile(image_data,90)))
		filename, extension = getFileNameAndExtension(file)
		plt.savefig(output_path + filename + "_" + extension + ".png")