# getDataframesDiff.py
# Get rows in df1 which are not in df2
# input: df1, df2 output file name.
# output: csv file with desired output.

import pandas as pd
import sys
import numpy as np

# read input
df1 = pd.read_csv(sys.argv[1])
df2 = pd.read_csv(sys.argv[2])
outputFile = sys.argv[3]

diff = df1[~df1.isin(df2)].dropna()

print 'len(df1) = ',len(df1)
print 'len(df2) = ',len(df2)
print 'len(diff) = ',len(diff)

# supress scientific notation
toSupress = ['dr7objid', 'run', 'camcol', 'rerun', 'field']

for col in toSupress:
	diff[col] = diff[col].astype(np.int64)

# print diff.head(2)

# diff.to_csv(outputFile, index=False, float_format='{:f}'.format, encoding='utf-8')
diff.to_csv(outputFile, index=False, encoding='utf-8')