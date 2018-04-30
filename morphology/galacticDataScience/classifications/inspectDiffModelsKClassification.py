import sys
import pandas as pd
import numpy as np

### READ INPUTS ###
df = pd.read_csv(sys.argv[1], low_memory=False)
classk05 = 'class-k5Model'
classk10 = 'class-k10Model'
classk20 = 'class-k20Model'
# print "len(sdssDR7): " + str(len(sdssDR7))
# print "len(mergedk5): " + str(len(mergedk5))
# print "len(classk10): " + str(len(classk10))
# print "len(classk20): " + str(len(classk20))

print '\nTotal: ' + str(len(df))
print '\nTotal undefined & unclassified: ' + str( len( df[(df[classk05] == 'U') & \
	( (df[classk10] == 'U') | (df[classk10] == '--') ) & \
	( (df[classk20] == 'U') | (df[classk20] == '--') ) ] ) )
print '\nTotal classified (E or S) by k5: ' + \
	str(len(df[(df[classk05] == 'E')]) + len(df[(df[classk05] == 'S')]))
print 'E: ' + str(len(df[(df[classk05] == 'E')]))
print 'S: ' + str(len(df[(df[classk05] == 'S')]))
print 'U: ' + str(len(df[(df[classk05] == 'U')]))

print '\nTotal classified (E or S) by k10: ' + \
        str(len(df[(df[classk10] == 'E')]) + len(df[(df[classk10] == 'S')]))
print 'E: ' + str(len(df[(df[classk10] == 'E')]))
print 'S: ' + str(len(df[(df[classk10] == 'S')]))
print 'U: ' + str(len(df[(df[classk10] == 'U')]))

print '\nTotal classified (E or S) by k20: ' + \
        str(len(df[(df[classk20] == 'E')]) + len(df[(df[classk20] == 'S')]))
print 'E: ' + str(len(df[(df[classk20] == 'E')]))
print 'S: ' + str(len(df[(df[classk20] == 'S')]))
print 'U: ' + str(len(df[(df[classk20] == 'U')]))

