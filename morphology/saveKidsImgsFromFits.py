# saveImagesFromFits.py
# save images from fits
# input: csv file with list of galaxies fits, input path to fits, output path to save images
# output: images (png) saved to output path

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import pandas as pd
import astropy.io.fits as fits
import os
import numpy as np
import math
import sys

# save filtered png from stamp <objId>_<extension>.png
def saveImgFromId(fileId, image_data, output_path):
	maxX, maxY = len(image_data[0]), len(image_data)
	img2plt = image_data[int(0.2*maxX):int(0.8*maxX),int(0.2*maxY):int(0.8*maxY)]

	plt.imshow(img2plt, cmap='gray',
		# norm=colors.LogNorm(vmin=np.median(image_data),vmax=np.median(image_data)+100))
		norm=colors.LogNorm(vmin=np.median(image_data),vmax=np.percentile(image_data,98)))
	plt.tick_params(
			axis='both', 
			which='both', 
			bottom='off', 
			top='off', 
			labelbottom='off', 
			right='off', 
			left='off', 
			labelleft='off')
	plt.savefig(output_path+fileId+'.png', bbox_inches='tight')
	plt.clf()

inputPath = sys.argv[1]  # must end with "/"
outputPath = sys.argv[2] # must end with "/"

for file in os.listdir(inputPath):
	name = (os.path.join(inputPath, file))
	#try:
	image_data = fits.getdata(name)
	#print image_data
	image_data = image_data + np.fabs(image_data.min())
	#print image_data	#exit()
	saveImgFromId(file, image_data, outputPath)
	#except Exception: 
	#	pass
