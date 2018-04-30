# checkMissingGalaxies.py
# Check for missing galaxies in CyMorph output.
# input: input catalog for CyMorph, CyMorph output and desired file name to store missing galaxies catalog.
# output: csv file with missing galaxies catalog.

import pandas as pd
import sys
import numpy

# read arguments
df1  = pd.read_csv(sys.argv[1])
print 'len(df1)  = ',len(df1)
df2 = pd.read_csv(sys.argv[2])
print 'len(df2) = ',len(df2)

print 'numerical diff = ',int(len(df1)-len(df2))

# get missing galaxies data
# missing = df1[df1['dr7objid'].isin(df2['Id']) == False]
missing = df1[~df1.index.isin(df2.index)]
print 'len(missing) = ',len(missing)
# generate file with missing galaxies data
missing.to_csv(sys.argv[3], index=False)
