import sys
import pandas as pd
import numpy as np

# read input data
dr7 = pd.read_csv(sys.argv[1])
zoo = pd.read_csv(sys.argv[2])

id_dr7 = sys.argv[3]
id_zoo = sys.argv[4]

# merging
print 'Merging SDSS and GZ...'
merged = pd.merge(dr7, zoo, left_on=id_dr7,right_on=id_zoo)

print 'Total merged: ', len(merged)
print 'Total unique merged: ', len(pd.unique(merged[id_dr7].values))
print 'Total Undefined: ', len(merged[merged['Zoo1class'] == 'U'])
print 'Total merged and defined: ', len(merged[merged['Zoo1class'] != 'U'])
print 'Total E: ', len(merged[merged['Zoo1class'] == 'E'])
print 'Total S: ', len(merged[merged['Zoo1class'] == 'S'])

# print 'Is it right? ', (len(merged[merged['Zoo1class'] == 'U']) + 
#	len(merged[merged['Zoo1class'] != 'U']))

# only defined galaxies
merged = merged[merged['Zoo1class'] != 'U']
# drop class column
merged = merged.drop('Zoo1class', 1)
# correct names of columns
allCols = list(merged)
for c in allCols:
	if c.endswith('_x'):
		newC = c[:-2]
		merged.rename(columns={c:newC}, inplace=True)

merged = merged[list(dr7)]

# suppress scientific notation
toSupress = [id_dr7, 'run', 'camcol', 'rerun', 'field']

for col in toSupress:
	merged.loc[:,col] = merged.loc[:,col].astype(np.int64)

merged.to_csv(sys.argv[5])


