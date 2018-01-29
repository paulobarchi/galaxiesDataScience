# getDesiredTypes.py
# Merge SDSS catalog (CyMorph input) with Galaxy Zoo 2 catalog and 
# get files for each desired galaxy type cataloged by GZ2.
# input: SDSS catalog, Galaxy Zoo 2 catalog(, desired galaxyZoo2 classes -- commented) and output path.
# output: csv files with merged result and one file for each galaxy type.

import pandas as pd
import sys

# read input
sdssCatalog = pd.read_csv(sys.argv[1])
gz2catalog = pd.read_csv(sys.argv[2])
outputPath = sys.argv[3]
# gTypes = [gType for gType in sys.argv[4].split(',')]
gTypes = ['Ei','Ec','Er','Sa','Sb','Sc','Sd','SBa','SBb','SBc','SBd']

# avoid duplicated columns
cols2merge = gz2catalog.columns.difference(sdssCatalog.columns)

# merge data
merged = pd.merge(sdssCatalog, gz2catalog[cols2merge], left_on='dr7objid',right_on='dr7objid2')

# mantain only columns of interest
desiredCols = sdssCatalog.columns.values.tolist()
desiredCols.append('gz2class')
merged = merged[desiredCols]

for gType in gTypes:
	# define dataframe mask to desired galaxy type
	mask = merged['gz2class'].str.startswith(gType)
	# copy register to new data frame, with desired class prefix	
	newDF = merged[mask].copy()
	# change 'old' gzclass to NEW
	mask = newDF['gz2class'].str.startswith(gType)
	newDF.loc[mask, 'gz2class'] = gType
	print 'len(' + gType + ') =', len(newDF)
	newDF.to_csv(outputPath + gType + '.csv', index=False)
