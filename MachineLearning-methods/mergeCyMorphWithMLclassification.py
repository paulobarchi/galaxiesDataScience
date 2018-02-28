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

desiredColumns = ['Id','sGa', 'sH', 'CN', 'sA3', 'sS3', 'class', 'Error']
merged = merged[desiredColumns]
columnsRenamed = ['Id','G2', 'H', 'C', 'A', 'S', 'class', 'Error']
merged.columns = columnsRenamed

### ASSING 9999.99 TO ALL FAILED METRICS ###
metrics = ['G2', 'H', 'C', 'A', 'S']
for metric in metrics:
	merged.loc[(merged[metric] == 0.0) | (merged[metric].isnull()), metric] = 9999.99

### REMAPPING ERROR ###
precedentErrorsCondition =  (merged['Error'] != 1) & (merged['Error'] != 2)
merged.loc[precedentErrorsCondition, 'Error'] = 0

errors = [1, 2, 3, 4, 5, 6, 7]

# for error in errors:
# 	print 'Error' + str(error) + ': ' + str(len(merged[(merged['Error'] == error)]))

# if G2 is null and Error = 0, Error = 3
merged.loc[(merged['G2'] == 9999.99) & (precedentErrorsCondition), 'Error'] = 3

# if H is null and Error = 0, Error = 4
merged.loc[(merged['H'] == 9999.99) & (precedentErrorsCondition), 'Error'] = 4

# if A is null and Error = 0, Error = 6
merged.loc[(merged['A'] == 9999.99) & (precedentErrorsCondition), 'Error'] = 6

# if S is null and Error = 0, Error = 7
merged.loc[(merged['S'] == 9999.99) & (precedentErrorsCondition), 'Error'] = 7

# if C is null and Error = 0, Error = 5
merged.loc[(merged['C'] == 9999.99) & (precedentErrorsCondition), 'Error'] = 5

# if has any error, class = 'U'
merged.loc[merged['Error'] != 0, 'class'] = 'U'

### VERIFY RESULT AND SAVE CSV ###

# print '\n\n'

for error in errors:
	print 'Error' + str(error) + ': ' + str(len(merged[(merged['Error'] == error)]))

# print merged[(merged['Error'] == 3)]

print 'Total errors: ' + str(len(merged[(merged['Error'] != 0)]))
print 'Total U: ' + str(len(merged[(merged['class'] == 'U')]))

print 'Total: ' + str(len(merged))
print 'E: ' + str(len(merged[(merged['class'] == 'E')]))
print 'S: ' + str(len(merged[(merged['class'] == 'S')]))
print 'U: ' + str(len(merged[(merged['class'] == 'U')]))
# print 'SUM: ' + str( len(merged[(merged['class'] == 'E')]) + len(merged[(merged['class'] == 'S')]) + len(merged[(merged['class'] == 'U')]))

# print merged[(merged['class'] != 'E') & (merged['class'] != 'S') & (merged['class'] != 'U')]

# print merged[(merged['Error'] != 0) & (merged['Error'] != 1) & (merged['Error'] != 2) & (merged['Error'] != 3) & (merged['Error'] != 4) & (merged['Error'] != 5) & (merged['Error'] != 6) & (merged['Error'] != 7)]

merged.to_csv(sys.argv[5], index = False)