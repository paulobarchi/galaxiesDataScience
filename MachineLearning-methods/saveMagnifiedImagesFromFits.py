# saveMagnifiedImagesFromFits.py
# save magnified images (with good visualization) from fits
# requisites: need to have stiff installed!
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
	img2plt = image_data[int(0.3*maxX):int(0.7*maxX),int(0.3*maxY):int(0.7*maxY)]

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
classCol = sys.argv[2]
inputPath = sys.argv[3]  # must end with "/"
outputPath = sys.argv[4] # must end with "/"
howMany = int(sys.argv[5])
desiredClass = sys.argv[6]
extension = '.fits'

i = 0

print howMany

for index, row in inputFile.iterrows():
	if (row[classCol] == desiredClass):
		if (i < howMany):
			print "File: " + inputPath + str(row["Id"]) + extension
			image_data = readFITSIMG(inputPath+str(row["Id"])+extension)
			saveImgFromId(str(row["Id"]), image_data, outputPath)
			cmd = "rm stiff.tif stiff.xml"
			process = os.popen(cmd)
			process.read()
			i += 1
		else:
			exit()
