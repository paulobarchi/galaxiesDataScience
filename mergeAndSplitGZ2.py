# mergeAndSplitGZ2.py
# Merge SDSS catalog (CyMorph input) with Galaxy Zoo 2 catalog and 
# create files for each galaxy type cataloged by GZ2.
# input: SDSS catalog, Galaxy Zoo 2 catalog, merged file name and output path.
# output: csv files with merged result and one file for each galaxy type.

import pandas as pd
import sys

# read input
sdssCatalog = pd.read_csv(sys.argv[1])
gz2catalog = pd.read_csv(sys.argv[2])
mergedFile = sys.argv[3]
outputPath = sys.argv[4]

print 'len(sdssCatalog) = ',len(sdssCatalog)
print 'len(gz2catalog) = ',len(gz2catalog)

# merge data
merged = pd.merge(sdssCatalog, gz2catalog, left_on='dr7objid',right_on='dr7objid2')
merged = merged.drop('dr7objid2',1)

# mantain only columns of interest
col_list = ['dr7objid', 'gz2class']
merged = merged[col_list]

# save merged data
print 'len(merged) = ',len(merged)
merged.to_csv(mergedFile, index=False)

# get len and save file for each galaxy type
galaxyTypes = merged['gz2class'].unique()

for galaxyType in galaxyTypes:
	df = merged[(merged['gz2class'] == galaxyType)]
	print galaxyType + ' =', len(df)
	df.to_csv(outputPath + galaxyType + '.csv', index=False)
