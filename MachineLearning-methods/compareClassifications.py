import pandas as pd
import sys

df1 = pd.read_csv(sys.argv[1])
df2 = pd.read_csv(sys.argv[2])

print ''
print '##### df1 #####'
print 'Total: ' + str(len(df1))
print 'E: ' + str(len(df1[(df1['class'] == 'E')]))
print 'S: ' + str(len(df1[(df1['class'] == 'S')]))
print 'U: ' + str(len(df1[(df1['class'] == 'U')]))
print ''
print '##### df2 #####'
print 'Total: ' + str(len(df2))
print 'E: ' + str(len(df2[(df2['class'] == 'E')]))
print 'S: ' + str(len(df2[(df2['class'] == 'S')]))
print 'U: ' + str(len(df2[(df2['class'] == 'U')]))

# print 'Total classified (E or S): ' + str(len(df2[(df2['class'] == 'E')]) + len(df2[(df2['class'] == 'S')]))

df1 = df1[(df1['class'] != 'U')]
df2 = df2[(df2['class'] != 'U')]

# merging classifications
merged = pd.merge(df1, df2, how='right', left_on='Id', right_on='Id')

desiredColumns = ['Id', 'class_x', 'class_y', 'Error_x']
merged = merged[desiredColumns]

columnsRenamed = ['Id', 'class_df1', 'class_df2', 'Error']
merged.columns = columnsRenamed

print '\nequals? ' + str( len(merged[(merged['class_df1'] == merged['class_df2'])]) )
print 'differs? ' + str( len(merged[(merged['class_df1'] != merged['class_df2'])]) )
# print 'summ?' + str( len(merged[(merged['class_df1'] == merged['class_df2'])]) + len(merged[(merged['class_df1'] != merged['class_df2'])]) )