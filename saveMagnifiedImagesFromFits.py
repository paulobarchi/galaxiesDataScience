# saveMagnifiedImagesFromFits.py
# save magnified images (with good visualization) from fits
# input: csv file with list of galaxies fits, input path to fits, output path to save images
# output: magnified images (png) saved to output path

import matplotlib.pyplot as plt
import pandas as pd
import astropy.io.fits as fits
import os
import numpy
import math
import sys

def readFITSIMG(string):
	process = os.popen("stiff "+string)
	process.read()
	return plt.imread("stiff.tif")

# save filtered png from stamp <objId>_<extension>.png
def saveImgFromId(fileId, image_data, output_path):
	maxX, maxY = len(image_data[0]), len(image_data)
	img2plt = image_data[int(0.35*maxX):int(0.65*maxX),int(0.35*maxY):int(0.65*maxY)]

	plt.imshow(img2plt, cmap=plt.cm.inferno)
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
inputPath = sys.argv[2]
outputPath = sys.argv[3]
extension = '.fits'

for f in inputFile["Id"]:
	print "File: " + inputPath + str(f) + extension
	image_data = readFITSIMG(inputPath+str(f)+extension)
	saveImgFromId(str(f), image_data, outputPath)
	cmd = "rm stiff.tif stiff.xml"
	process = os.popen(cmd)
	process.read()
	exit()
