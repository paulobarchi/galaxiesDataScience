import pandas as pd
import sys
import numpy as np

### TO SLICE CYMORPH RESULT FROM SDSS QUERY ###

# read input
cyMo = pd.read_csv(sys.argv[1])
sdss = pd.read_csv(sys.argv[2])
outC = sys.argv[3]

print "len(cyMo): " + str(len(cyMo))
print "len(sdss): " + str(len(sdss))

id1 = 'dr7objid'
id2 = 'Id'

# merging
print 'Merging...'
merged = pd.merge(sdss, cyMo, left_on=id1, right_on=id2)

print "len(merged): " + str(len(merged))

merged = merged[list(cyMo)]

# supress scientific notation
# toSupress = [id1, 'run', 'camcol', 'rerun', 'field']
# for col in toSupress:
# 	merged.loc[:,col] = merged.loc[:,col].astype(np.int64)
merged.loc[:,id2] = merged.loc[:,id2].astype(np.int64)

# generate file with merged galaxies data
merged.to_csv(outC, index=False)