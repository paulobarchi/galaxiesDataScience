import pandas as pd
import sys
import numpy as np

def putKinFileName(filename, k):
	return filename.split('.')[0] + "_k" + str(k) + "." + filename.split('.')[-1]

# read input
sdss = pd.read_csv(sys.argv[1])
cyMo = pd.read_csv(sys.argv[2])

print "len(sdss): " + str(len(sdss))
print "len(cyMo): " + str(len(cyMo))

id1 = 'objID'
id2 = 'Id'

# merging
print 'Merging...'
merged = pd.merge(sdss, cyMo, left_on=id1, right_on=id2)
print "len(merged): " + str(len(merged))

toNotProcess_kl5    = merged[(merged['areasRatio'] < 5.0)].copy()
to_process_with_k5  = merged[(merged['areasRatio'] >= 5.0)  & (merged['areasRatio'] < 10.0)].copy()
to_process_with_k10 = merged[(merged['areasRatio'] >= 10.0) & (merged['areasRatio'] < 20.0)].copy()
to_process_with_k20 = merged[(merged['areasRatio'] >= 20.0)].copy()

print "len(toNotProcess_kl5)   : " + str(len(toNotProcess_kl5))
print "len(to_process_with_k5) : " + str(len(to_process_with_k5))
print "len(to_process_with_k10): " + str(len(to_process_with_k10))
print "len(to_process_with_k20): " + str(len(to_process_with_k20))

print "SUM: " + str(len(to_process_with_k5) + len(to_process_with_k10) + len(to_process_with_k20))

# supress scientific notation
# toSupress = [id1, 'run', 'camcol', 'rerun', 'field']

desiredColumns = list(cyMo)
desiredColumns.append('areasRatio')

kl5_fileName  = sys.argv[3]
k5_fileName  = putKinFileName(sys.argv[2], 5)
k10_fileName = putKinFileName(sys.argv[2], 10)
k20_fileName = putKinFileName(sys.argv[2], 20)

to_process_with_k5.loc[:,id2]  = to_process_with_k5.loc[:,id2].astype(np.int64)
to_process_with_k10.loc[:,id2] = to_process_with_k10.loc[:,id2].astype(np.int64)
to_process_with_k20.loc[:,id2] = to_process_with_k20.loc[:,id2].astype(np.int64)

toNotProcess_kl5.to_csv(kl5_fileName, index = False)
to_process_with_k5.to_csv(k5_fileName, index = False)
to_process_with_k10.to_csv(k10_fileName, index = False)
to_process_with_k20.to_csv(k20_fileName, index = False)