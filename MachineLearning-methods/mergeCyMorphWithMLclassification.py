import sys
import pandas as pd
import numpy as np

### READ INPUTS ###
df1 = pd.read_csv(sys.argv[1])
df2 = pd.read_csv(sys.argv[2])

Id1 = sys.argv[3]
Id2 = sys.argv[4]

### MERGE ###
# merge and put all results from CyMorph even those without class
merged = pd.merge(df1, df2, how='left', left_on=Id1, right_on=Id2)

# desiredColumns = ['Id','sGa', 'sH', 'CN', 'sA3', 'sS3', 'class', 'Error']
desiredColumns = ['Id','sGa', 'sH', 'sA3', 'sS3', 'class', 'Error']
merged = merged[desiredColumns]
# columnsRenamed = ['Id','G2', 'H', 'C', 'A', 'S', 'class', 'Error']
columnsRenamed = ['Id','G2', 'H', 'A', 'S', 'class', 'Error']
merged.columns = columnsRenamed

### ASSING 9999.99 TO ALL FAILED METRICS ###
# metrics = ['G2', 'H', 'C', 'A', 'S']
metrics = ['G2', 'H', 'A', 'S']
for metric in metrics:
	merged.loc[(merged[metric] == 0.0) | (merged[metric].isnull()), metric] = 9999.99

### REMAPPING ERROR ###
precedentErrorsCondition =  (merged['Error'] != 1) & (merged['Error'] != 2)
merged.loc[precedentErrorsCondition, 'Error'] = 0

# if G2 is null and Error = 0, Error = 3
merged.loc[(merged['G2'] == 9999.99) & (precedentErrorsCondition), 'Error'] = 3

# if H is null and Error = 0, Error = 4
merged.loc[(merged['H'] == 9999.99) & (precedentErrorsCondition), 'Error'] = 4

# if A is null and Error = 0, Error = 6
merged.loc[(merged['A'] == 9999.99) & (precedentErrorsCondition), 'Error'] = 6

# if S is null and Error = 0, Error = 7
merged.loc[(merged['S'] == 9999.99) & (precedentErrorsCondition), 'Error'] = 7

# if C is null and Error = 0, Error = 5
# merged.loc[(merged['C'] == 9999.99) & (precedentErrorsCondition), 'Error'] = 5

# if has any problem, class = 'U'
problems = ( (merged['G2'] == 9999.99) | (merged['H'] == 9999.99) | \
	(merged['A'] == 9999.99) | (merged['S'] == 9999.99) )

# merged.loc[merged['Error'] != 0, 'class'] = 'U'
merged.loc[problems, 'class'] = 'U'

### SAVE CSV ###
merged.to_csv(sys.argv[5], index = False)