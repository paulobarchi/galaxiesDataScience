import pandas as pd
import sys
import os

metric = sys.argv[2]
inputFile = sys.argv[1]

# read csv file into dataframe
df = pd.read_csv(inputFile)
# group by desired metric
gp = df.groupby(metric)
# create directory 'metric'
os.makedirs(metric)

for g in gp.groups:
	newFile = metric + '/' + str(g) + '.csv'
	gp.get_group(g).to_csv(newFile, index=False)
