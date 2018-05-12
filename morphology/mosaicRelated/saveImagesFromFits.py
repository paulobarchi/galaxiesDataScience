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
	img2plt = image_data[int(0.3*maxX):int(0.7*maxX),int(0.3*maxY):int(0.7*maxY)]

	plt.imshow(img2plt, cmap='gray',
		norm=colors.LogNorm(vmin=np.median(image_data),vmax=np.median(image_data)+100))
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

inputFile = pd.read_csv(sys.argv[1])
idCol = sys.argv[2]
classCol = sys.argv[3]
inputPath = sys.argv[4]  # must end with "/"
outputPath = sys.argv[5] # must end with "/"
desiredClass = sys.argv[6]

for index, row in inputFile.iterrows():
	if (row[classCol] == desiredClass):
		name = inputPath+str(row[idCol])+'_wout-cleaning_stamp5.fit'
		print "Done %.5f %%" % ( (float(index)/float(len(inputFile))) * 100)
		try:
			image_data = fits.getdata(name)			
			saveImgFromId(str(row[idCol]), image_data, outputPath)
		except Exception: 
		 	pass
