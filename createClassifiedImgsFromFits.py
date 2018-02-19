# createClassifiedImgsFromFits.py
# Create images (pngs) from galaxy fit(s).
# input: input csv file with classification, number of galaxies from each type, 
#		input path, extension of files and output path for each class.
# output: galaxy images (pngs).

import sys
import pandas as pd
import os
from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

def getFileNameAndExtension(file):
	return file.split(".")[0], file.split(".")[1]

# save filtered png from stamp <objId>_<extension>.png
def saveImgFromId(galId, extension, input_path, output_path):
	file = str(galId) + '.' + extension
	image_data = fits.getdata(input_path+file)
	plt.imshow(image_data, cmap='gray', 
		# norm=colors.LogNorm(vmin=np.median(image_data),vmax=np.median(image_data)+100))
		# norm=colors.LogNorm(vmin=np.median(image_data)+100,vmax=np.percentile(image_data,99)))
		norm=colors.LogNorm())
	filename, extension = getFileNameAndExtension(file)	

	plt.tick_params(
			axis='both', 
			which='both', 
			bottom='off', 
			top='off', 
			labelbottom='off', 
			right='off', 
			left='off', 
			labelleft='off')
	plt.savefig(output_path+filename)
	plt.clf()

# read csv file
df = pd.read_csv(sys.argv[1])
# read number of galaxies from each type
numberOfGal = int(sys.argv[2])
input_path = sys.argv[3] # must be with "/" after
extension = sys.argv[4] # must be with "." before
output_path_E = sys.argv[5] # must be with "/" after
output_path_S = sys.argv[6] # must be with "/" after

i = 0 # controls S
j = 0 # controls E

for index, row in df.iterrows():
	if (i == numberOfGal and j == numberOfGal):
		break;

	if (i == numberOfGal and row['class'] == 'S'):
		continue
	elif (j == numberOfGal and row['class'] == 'E'):
		continue
	
	if (row['class'] == 'S'):
		output_path = output_path_S
		i += 1
	else:
		output_path = output_path_E
		j += 1

	# create image
	saveImgFromId(row['Id'], extension, input_path, output_path)

# saveImgFromId('401000007', extension, input_path, output_path_S)		
