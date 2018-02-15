# mergeAndMaintainColumn.py
# merge 2 dataframes and, besides keeping the whole first dataframe, adds a specific column.
# input: first dataframe, second dataframe, Id from first datafarme, Id from second dataframe, 
#		column to be maintained and output file name for merged dataframe
# output: csv file with merged dataframe

import pandas as pd
import sys
import numpy

df1 = pd.read_csv(sys.argv[1])
df2 = pd.read_csv(sys.argv[2])

firstId = sys.argv[3]
secondId = sys.argv[4]

maintainColumn = sys.argv[5]

col_list = list(df1)
col_list.append(maintainColumn) # append returns None; can't assign

merged = pd.merge(df1, df2, left_on=firstId, right_on=secondId)

merged = merged[col_list]

merged.to_csv(sys.argv[6], index=False)