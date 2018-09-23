import pandas as pd
import sys

# read input
kids_cat = pd.read_csv(sys.argv[1], sep='\s+', header=None)
# header should be:
# sdssId	gz2class	filename	kidsId	matchRadius	kidsFlag1	kidsFlag2	kidsFOV
outputFile  = sys.argv[2]

print 'len(kids_cat) = ',len(kids_cat)

newDF = kids_cat.copy()

gTypes = ['E','S_','SB_']

for index, row in newDF.iterrows():
	if (row[1].startswith('E')):
		newDF.iloc[index, newDF.columns.get_loc(1)] = 'E'
	elif (row[1].startswith('SB')):
		newDF.iloc[index, newDF.columns.get_loc(1)] = 'SB_'
	elif (row[1].startswith('S')):
		newDF.iloc[index, newDF.columns.get_loc(1)] = 'S_'

for gType in gTypes:
	print 'len(' + gType + ') =', len(newDF[newDF[1] == gType])
	newDF[newDF[1] == gType].to_csv(outputFile.split('.')[0]+'_'+gType+'.csv', index=False)

# save merged data
print 'after gTypes processing'
print 'len(newDF) = ',len(newDF)

# drop rows with gz2class not in gTypes
newDF = newDF[newDF[1].isin(gTypes)]
print 'after selecting K>=10 and gz2class in gTypes'
print 'len(newDF) = ',len(newDF)

newDF.to_csv(outputFile, index=False, header=False)