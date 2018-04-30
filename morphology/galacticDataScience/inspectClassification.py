import pandas as pd
import sys

df = pd.read_csv(sys.argv[1])

print ''

errors = [1, 2, 3, 4, 5, 6, 7]

for error in errors:
	print 'Error' + str(error) + ': ' + str(len(df[(df['Error'] == error)]))

print '\nTotal errors: ' + str(len(df[(df['Error'] != 0)]))
print 'Total U: ' + str(len(df[(df['class'] == 'U')]))

# mask: rows ok with all metrics except Concentration
# CProblemOnly = ( (df['C'] == 9999.99) & (df['G2'] != 9999.99) & \
# 	(df['H'] != 9999.99) & (df['A'] != 9999.99) & (df['S'] != 9999.99) )

# dfCProblemOnly = df[CProblemOnly]

# print '\nGalaxies with C problem only: ' + str(len(dfCProblemOnly))

#######################################################
# dfWoutCProblemOnly = df.merge(dfCProblemOnly, indicator=True, how='outer')
# dfWoutCProblemOnly = dfWoutCProblemOnly[dfWoutCProblemOnly['_merge'] == 'left_only']

# print '\n ## Total: ' + str(len(dfWoutCProblemOnly))
# print ' Does it totals? ' + str(len(dfWoutCProblemOnly) + len(dfCProblemOnly))

# print '\nErrors for dfWoutCProblemOnly'
# for error in errors:
# 	print 'Error' + str(error) + ': ' + str(len(dfWoutCProblemOnly[(dfWoutCProblemOnly['Error'] == error)]))

print '\nTotal: ' + str(len(df))
print 'Total classified (E or S): ' + str(len(df[(df['class'] == 'E')]) + len(df[(df['class'] == 'S')]))
print 'E: ' + str(len(df[(df['class'] == 'E')]))
print 'S: ' + str(len(df[(df['class'] == 'S')]))
print 'U: ' + str(len(df[(df['class'] == 'U')]))

print ''

# print 'SUM: ' + str( len(df[(df['class'] == 'E')]) + len(df[(df['class'] == 'S')]) + len(df[(df['class'] == 'U')]))
# print df[(df['class'] != 'E') & (df['class'] != 'S') & (df['class'] != 'U')]
# print df[(df['Error'] != 0) & (df['Error'] != 1) & (df['Error'] != 2) & (df['Error'] != 3) & (df['Error'] != 4) & (df['Error'] != 5) & (df['Error'] != 6) & (df['Error'] != 7)]