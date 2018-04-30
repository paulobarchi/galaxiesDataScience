import sys
import pandas as pd
from numpy import sin, cos, arccos, nan
import numpy as np

# function to get RA and DEC
def getRaDec(filename):
	filename = ".".join(filename.split(".")[:-1])
	return filename.split("_")[-2], filename.split("_")[-1]	

# function to get distance between to galaxies
def getDistance(ra1, dec1, ra2, dec2):
	print(ra1, dec1, ra2, dec2)
	return arccos( sin(dec1) * sin(dec2) + cos(dec1) * cos(dec2) * cos(ra1 - ra2) )

# read input
dfVST = pd.read_csv(sys.argv[1])
dfZoo = pd.read_csv(sys.argv[2])

# create new columns
dfVST['minDistObjId'] = nan
dfVST['minDist'] = nan
dfVST['lessThan30sec'] = False

# for each galaxy in VST
for i, rowVST in dfVST.iterrows():

	# get RA and DEC from VST
	raVST, decVST = getRaDec(rowVST['Id'])

	# build an aux df with distances	
	auxDF = pd.DataFrame(columns = ['Id', 'distance'])

	# for each line in Zoo1
	for j, rowZoo in dfZoo.iterrows():
		# get distance (from VST galaxy to Zoo1 galaxy)	
		# UNITS alright?
		jDistance = getDistance(raVST, decVST, rowZoo['ra'], rowZoo['dec'])
		# save register 
		auxDF.set_value(j,'Id', rowZoo['dr7objid2'])
		auxDF.set_value(j,'distance', jDistance)

	# select row with min distance value (oneliner?)
	rowMinDist = auxDF.loc[auxDF['distance'].idxmax()]
	rowZooMinDist = dfZoo[dfZoo['dr7objid2'] == rowMinDist['Id']]
	# save values referent to minDist
	dfVST.set_value(i, 'minDistObjId', rowMinDist['Id'])
	dfVST.set_value(i, 'minDist', rowMinDist['distance'])
	dfVST.set_value(i, 'lessThan30sec', ( rowMinDist['distance'] < 30 ) ) # ???
	
	# print ra1 dec 1 ra2 dec2 distance
	print('raVST: ' + str(raVST) + '; decVST: ' + str (decVST))
	print('raZoo: ' + str(rowZooMinDist['ra']) + '; decZoo: ' + str(rowZooMinDist['dec']))

	exit() # test

# check how many True values for 
# print len(dfVST[dfVST['lessThan30sec'] == True])

