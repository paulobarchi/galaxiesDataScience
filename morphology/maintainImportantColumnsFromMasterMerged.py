import pandas as pd
import sys

# read input
classifs = pd.read_csv(sys.argv[1])
masterDF = pd.read_csv(sys.argv[2])

print "len(classifs): " + str(len(classifs))
print "len(masterDF): " + str(len(masterDF))

id1 = 'Id'
id2 = 'ObjID_DR7'

desiredColumns = list(classifs)
desiredColumns.extend(
	['sigma', 'metL_MILES', 'ageL_MILES', 'logMass_MILES', 'z', 'zErr', 'absMag_r', 'eClass'])

print desiredColumns

masterDF = masterDF[desiredColumns]

masterDF.to_csv(sys.argv[3], index = False)
