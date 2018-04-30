import pandas as pd
import sys

# read input
classifs = pd.read_csv(sys.argv[1])
masterDF = pd.read_csv(sys.argv[2], sep=' ')

print "len(classifs): " + str(len(classifs))
print "len(masterDF): " + str(len(masterDF))

id1 = 'Id'
id2 = 'ObjID_DR7'

# merging
print 'Merging...'
merged = pd.merge(classifs, masterDF, left_on=id1, right_on=id2)
print "len(merged): " + str(len(merged))

desiredColumns = list(classifs)
desiredColumns.extend(
	['sigma', 'metL_MILES', 'ageL_MILES', 'logMass_MILES', 'z', 'zErr', 'absMag_r', 'eClass'])

print desiredColumns

merged = merged[desiredColumns]

merged.to_csv(sys.argv[3], index = False)
