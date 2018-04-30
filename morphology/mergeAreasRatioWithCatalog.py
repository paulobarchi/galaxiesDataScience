import pandas as pd
import sys

# read input
classifs = pd.read_csv(sys.argv[1])
withArea = pd.read_csv(sys.argv[2])

print "len(classifs): " + str(len(classifs))
print "len(withArea): " + str(len(withArea))

# print "len(areasRatio < 20): " + str(len(withArea[withArea['areasRatio'] < 20]))
# print withArea[withArea['areasRatio'] < 20]

id1 = 'Id'
id2 = 'dr7objid'

# merging
print 'Merging...'
merged = pd.merge(classifs, withArea, left_on=id1, right_on=id2)
print "len(merged): " + str(len(merged))

allCols = list(merged)

for c in allCols:
	if c.endswith('_x'):
		newC = c[:-2]
		merged.rename(columns={c:newC}, inplace=True)

desiredColumns = list(classifs)
desiredColumns.append('areasRatio')

# print desiredColumns
# print list(classifs)

merged = merged[desiredColumns]
# print list(merged)

# supress scientific notation
# toSupress = [id1, 'run', 'camcol', 'rerun', 'field']

# for col in toSupress:
# 	toProcess.loc[:,col] = toProcess.loc[:,col].astype(np.int64)

merged.to_csv(sys.argv[3], index = False)
