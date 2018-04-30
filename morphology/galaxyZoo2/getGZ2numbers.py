import sys
import pandas as pd
import numpy as np

# read input data
df = pd.read_csv(sys.argv[1])
# targetClass = sys.argv[2]
targetClass = 'gz2class'

print 'Total: ', len(df)
print 'Total Undefined: ', len(df[df[targetClass] == 'U'])
print 'Total defined: ', len(df[df[targetClass] != 'U'])

# if E-united
gTypes = ['E','Sa','Sb','Sc','Sd','SBa','SBb','SBc','SBd']
gTypesNums = [0,1,2,3,4,5,6,7,8]
# proportion increments in 0.05

# if E-united; and (Sd and SBd) removed
gTypes = ['E','Sa','Sb','Sc','SBa','SBb','SBc']
gTypesNums = [0,1,2,3,4,5,6]

# for each gType
for gTypeNum in gTypesNums:
	print ' Total of ' + gTypes[gTypeNum] + ' galaxies: ' + str(len(df[df[targetClass] == gTypes[gTypeNum]]))