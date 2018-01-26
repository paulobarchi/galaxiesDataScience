# getIndexesDomain.py
# get indexes domain from result file.
# input: result file and list of metrics (separated by comma).
# output: indexes domain.

import sys
import pandas as pd

# read datasets
ds = pd.read_csv(sys.argv[1])
metrics = [metric for metric in sys.argv[2].split(',')]

print "\n ### Indexes Ranges ###\n"

for metric in metrics:
	print metric + ": [" + str(ds[metric].min()) + ", " + str(ds[metric].max()) + "]"

print ""
