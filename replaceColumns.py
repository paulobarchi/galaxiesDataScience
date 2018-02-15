# replaceColumns.py
# Replace desired dataframe columns 
# input: dataframe with columns to be replaced, dataframe with desired replacing columns, list of columns,
#		output file name for resulting dataframe
# output: csv file with resulting dataframe

import pandas as pd
import sys

df1 = pd.read_csv(sys.argv[1])
df2 = pd.read_csv(sys.argv[2])

columns = [column for column in sys.argv[3].split(',')] # list of columns to replace

for column in columns:
	df1[column] = df2[column]

df1.to_csv(sys.argv[4], index=False)