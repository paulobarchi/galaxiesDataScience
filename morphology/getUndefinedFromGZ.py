# .py
# 
# 	
# input: 
# output: 

import pandas as pd
import sys
import numpy as np

# read input
sdss = pd.read_csv(sys.argv[1])
# cyMo = pd.read_csv(sys.argv[2])
gZoo = pd.read_csv(sys.argv[2])

outC = sys.argv[3]

# Ids ???
# id_cymo = 'Id'
id_sdss = 'dr7objid'
id_zoo1 = 'OBJID'

# merging
print 'Merging SDSS and GZ1...'
merged1 = pd.merge(sdss, gZoo, left_on=id_sdss,right_on=id_zoo1)

# print 'Total merged1: ', len(merged1)
# print 'Total unique merged1: ', len(pd.unique(merged1[id_sdss].values))
print 'Total Undefined1: ', len(merged1[merged1['Zoo1class'] == 'U'])

undefined1 = merged1[merged1['Zoo1class'] == 'U']

# merging
# print 'Merging CyMorph and GZ1...'
# merged2 = pd.merge(cyMo, gZoo, left_on=id_cymo,right_on=id_zoo1)

# print 'Total merged2: ', len(merged2)
# print 'Total unique merged2: ', len(pd.unique(merged2[id_cymo].values))
# print 'Total Undefined2: ', len(merged2[merged2['Zoo1class'] == 'U'])

# undefined2 = merged2[merged2['Zoo1class'] == 'U']

# toProcess = undefined1 - undefined2
# toProcess = undefined1[undefined1[id_sdss].isin(pd.unique(undefined2[id_cymo].values)) == False]
# toProcess.rename(columns={'dr7objid2':'dr7objid'}, inplace=True)

undefined1.rename(columns={'dr7objid2':'dr7objid'}, inplace=True)
toProcess = undefined1.copy()

# processed = undefined2[undefined2[id_cymo].isin(pd.unique(undefined1[id_sdss].values)) == True]

# print 'len(toProcess) = ',len(toProcess)
# print 'len(processed) = ',len(processed)

allCols = list(toProcess)
# allCols = list(processed)

for c in allCols:
	if c.endswith('_x'):
		newC = c[:-2]
		toProcess.rename(columns={c:newC}, inplace=True)
		# processed.rename(columns={c:newC}, inplace=True)

toProcess = toProcess[list(sdss)]
# processed = processed[list(cyMo)]

print 'len(toProcess) = ',len(toProcess)
# print 'len(processed) = ',len(processed)

# supress scientific notation
toSupress = [id_sdss, 'run', 'camcol', 'rerun', 'field']

for col in toSupress:
	toProcess.loc[:,col] = toProcess.loc[:,col].astype(np.int64)
# 	processed.loc[:,col] = processed.loc[:,col].astype(np.int64)

# generate file with toProcess galaxies data
toProcess.to_csv(outC, index=False)
# processed.to_csv(outC, index=False)