# appendAndVerifyCatalogs.py
# Concatenate two result files and verify if the whole input was processed
# input: input, result1 and result2.
# output: print lengths and difference of input - output.

import pandas as pd
import sys
import os
import numpy as np

# read input
inputCat = pd.read_csv(sys.argv[1])
path = sys.argv[2]
outputFile = sys.argv[3]
extension = '.csv'

# mode can be "merge" or "missing"
mode = "merge"
if len(sys.argv) > 3: 
	mode = sys.argv[3]

id_inp = 'dr7objid2'
id_res = 'Id'

filesList = []

# for each csv file in directory
for file in os.listdir(path):
	if (not os.path.isdir(file) and file.endswith(extension) ):
		df = pd.read_csv(path+file)		
		print list(df)
		filesList.append(df)

# concatenate
print 'Concatenating ', len(filesList), ' files.'
result = pd.concat(filesList)
print list(result)

print 'Total result: ', len(result)
print 'Total unique result: ', len(pd.unique(result[id_res].values))
print 'Total input: ', len(inputCat)

# merging
print 'Merging...'
merged = pd.merge(result, inputCat, left_on=id_res,right_on=id_inp)

print 'Total merged: ', len(merged)
print 'Total unique merged: ', len(pd.unique(merged[id_res].values))

### IF there are missing galaxies... ###
if (mode == "missing"):
	# get missing galaxies data
	missing = inputCat[inputCat['dr7objid2'].isin(pd.unique(merged[id_res].values)) == False]
	missing.rename(columns={'dr7objid2':'dr7objid'}, inplace=True)

	print 'len(missing) = ',len(missing)
	# print missing.head(5)

	# supress scientific notation
	toSupress = ['dr7objid', 'run', 'camcol', 'rerun', 'field']

	for col in toSupress:
		missing.loc[:,col] = missing.loc[:,col].astype(np.int64)

	# generate file with missing galaxies data
	missing.to_csv(outputFile, index=False)
else:
	# drop duplicates
	merged = merged.drop_duplicates(subset=[id_inp])	
	print 'Total merged: ', len(merged)

	# get only desired columns
	cols = list(result)
	cols.append('gz2class')
	merged = merged[cols]
	
	merged.to_csv(outputFile, index=False)