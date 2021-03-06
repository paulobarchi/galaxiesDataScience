# mergeAndSeparateClasses.py
# Merge CyMorph output with Galaxy Zoo 1 catalog and create result files for early- and late-type galaxies.
# input: CyMorph output, merged result file name, results for early- and late-type galaxies filenames.
# output: csv files with merged result, results for early- and late-type galaxies.

import pandas as pd
import sys
import numpy

# use example:
# python mergeAndSeparateClasses.py result.csv result_merged.csv resultE.csv resultS.csv

### MERGE WITH GALAXYZOO ###
result = pd.read_csv(sys.argv[1])
galZoo = pd.read_csv('galaxyZoo1Classification.csv')

merged = pd.merge(result, galZoo, left_on='Id',right_on='OBJID')
merged = merged.drop('OBJID',1)
merged.to_csv(sys.argv[2],index=False)

### SEPARATE CLASSES ###
print 'len(merged) = ',len(merged)

resultE = merged[(merged['Zoo1class'] == 'E')]
print 'len(resultE) = ',len(resultE)
resultE.to_csv(sys.argv[3], index=False)

resultS = merged[(merged['Zoo1class'] == 'S')]
print 'len(resultS) = ',len(resultS)
resultS.to_csv(sys.argv[4], index=False)
