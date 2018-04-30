import pandas as pd
import sys
import numpy as np

def putKinFileName(filename, k):
	return filename.split('.')[0] + "_k" + str(k) + "." + filename.split('.')[-1]

# read input
inputCatalog = pd.read_csv(sys.argv[1])

print "len(inputCatalog): " + str(len(inputCatalog))

toNotProcess_kl5    = inputCatalog[(inputCatalog['areasRatio'] < 5.0)].copy()
to_process_with_k5  = inputCatalog[(inputCatalog['areasRatio'] >= 5.0)  & (inputCatalog['areasRatio'] < 10.0)].copy()
to_process_with_k10 = inputCatalog[(inputCatalog['areasRatio'] >= 10.0) & (inputCatalog['areasRatio'] < 20.0)].copy()
to_process_with_k20 = inputCatalog[(inputCatalog['areasRatio'] >= 20.0)].copy()

print "len(toNotProcess_kl5)   : " + str(len(toNotProcess_kl5))
print "len(to_process_with_k5) : " + str(len(to_process_with_k5))
print "len(to_process_with_k10): " + str(len(to_process_with_k10))
print "len(to_process_with_k20): " + str(len(to_process_with_k20))

print "SUM: " + str(len(to_process_with_k5) + len(to_process_with_k10) + len(to_process_with_k20))

# supress scientific notation
# toSupress = [id1, 'run', 'camcol', 'rerun', 'field']

kl5_fileName  = 'catalogs/IC_objects_lucas_areasRatio_kl5.csv'
k5_fileName  = putKinFileName(sys.argv[1], 5)
k10_fileName = putKinFileName(sys.argv[1], 10)
k20_fileName = putKinFileName(sys.argv[1], 20)

col = 'objID'
to_process_with_k5.loc[:,col]  = to_process_with_k5.loc[:,col].astype(np.int64)
to_process_with_k10.loc[:,col] = to_process_with_k10.loc[:,col].astype(np.int64)
to_process_with_k20.loc[:,col] = to_process_with_k20.loc[:,col].astype(np.int64)

toNotProcess_kl5.to_csv(kl5_fileName, index = False)
to_process_with_k5.to_csv(k5_fileName, index = False)
to_process_with_k10.to_csv(k10_fileName, index = False)
to_process_with_k20.to_csv(k20_fileName, index = False)