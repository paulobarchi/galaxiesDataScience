# mergeSDSSandGZ2.py
# Merge SDSS catalog (CyMorph input) with Galaxy Zoo 2 catalog
# input: SDSS catalog, Galaxy Zoo 2 catalog and output file name.
# output: csv file with merged result.

# run example: 
# python mergeSDSSandGZ2.py catalogs/SDSS_DR7_k10.csv catalogs/zoo2MainSpecz.csv 
#	catalogs/Paulo_10k_Zoo2_desiredClasses.csv 

import pandas as pd
import sys

# read input
sdssCatalog = pd.read_csv(sys.argv[1])
gz2catalog = pd.read_csv(sys.argv[2])
outputFile = sys.argv[3]

print 'len(sdssCatalog) = ',len(sdssCatalog)
print 'len(gz2catalog) = ',len(gz2catalog)

# merge data
merged = pd.merge(sdssCatalog, gz2catalog[list(['dr7objid2','gz2class'])], left_on='dr7objid',right_on='dr7objid2')
merged = merged.drop('dr7objid2',1)
print 'len(merged) = ',len(merged)
# copy registers to new data frame
newDF = merged.copy()

# desired galaxy types
gTypes = ['Ei','Ec','Er','Sa','Sb','Sc','Sd','SBa','SBb','SBc','SBd']

for gType in gTypes:
	# define dataframe mask to desired galaxy type
	mask = newDF['gz2class'].str.startswith(gType)
	newDF.loc[mask, 'gz2class'] = gType
	print 'len(' + gType + ') =', len(newDF[mask])

# save merged data
print 'len(newDF) = ',len(newDF)
newDF.to_csv(outputFile, index=False)