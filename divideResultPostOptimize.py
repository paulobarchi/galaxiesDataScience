# divideResultPostOptimize.py
# Divide CyMorph output by metric (for later, easily get the geometric histogram separation between distributions).
# input: CyMorph output and desired metric.
# output: csv files with results for different metric configurations.

import pandas as pd
import sys
import os

inputFile = sys.argv[1]
metric = sys.argv[2]

# read csv file into dataframe
df = pd.read_csv(inputFile)
# group by desired metric
gp = df.groupby(metric)
# create directory 'metric'
os.makedirs(metric)

for g in gp.groups:
	newFile = metric + '/' + str(g) + '.csv'
	gp.get_group(g).to_csv(newFile, index=False)
