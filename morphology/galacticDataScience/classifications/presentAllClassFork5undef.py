import sys
import pandas as pd
import numpy as np

### READ INPUTS ###
sdssDR7 = pd.read_csv(sys.argv[1]) # to get astroph. data
mergedk5 = pd.read_csv(sys.argv[2])
classk10 = pd.read_csv(sys.argv[3])
classk20 = pd.read_csv(sys.argv[4])
# print "len(sdssDR7): " + str(len(sdssDR7))
# print "len(mergedk5): " + str(len(mergedk5))
# print "len(classk10): " + str(len(classk10))
# print "len(classk20): " + str(len(classk20))

print '\nTotal: ' + str(len(mergedk5))
print '\nTotal classified (E or S) by k5: ' + \
	str(len(mergedk5[(mergedk5['class'] == 'E')]) + len(mergedk5[(mergedk5['class'] == 'S')]))
print 'E: ' + str(len(mergedk5[(mergedk5['class'] == 'E')]))
print 'S: ' + str(len(mergedk5[(mergedk5['class'] == 'S')]))
print 'U: ' + str(len(mergedk5[(mergedk5['class'] == 'U')]))

print '\nTotal: ' + str(len(classk10))
print '\nTotal classified (E or S) by k10: ' + \
	str(len(classk10[(classk10['class'] == 'E')]) + len(classk10[(classk10['class'] == 'S')]))
print 'E: ' + str(len(classk10[(classk10['class'] == 'E')]))
print 'S: ' + str(len(classk10[(classk10['class'] == 'S')]))
print 'U: ' + str(len(classk10[(classk10['class'] == 'U')]))

print '\nTotal: ' + str(len(classk20))
print '\nTotal classified (E or S) by k20: ' + \
	str(len(classk20[(classk20['class'] == 'E')]) + len(classk20[(classk20['class'] == 'S')]))
print 'E: ' + str(len(classk20[(classk20['class'] == 'E')]))
print 'S: ' + str(len(classk20[(classk20['class'] == 'S')]))
print 'U: ' + str(len(classk20[(classk20['class'] == 'U')]))

sdssId = 'dr7objid'
mergId = 'Id'
includeAstroData = sys.argv[5]

### MERGE ###
# merge and put all results from CyMorph even those without class
mergePt1 = pd.merge(sdssDR7, mergedk5, how='left', left_on=sdssId, right_on=mergId)
# print ""
# print list(mergePt1)
# print "len(mergePt1): " + str(len(mergePt1))
mergePt2 = pd.merge(mergePt1, classk10, how='left', left_on=sdssId, right_on=mergId)
# print list(mergePt2)
# print "len(mergePt2): " + str(len(mergePt2))
mergeFin = pd.merge(mergePt2, classk20, how='left', left_on=sdssId, right_on=mergId)
# mergeFin = pd.merge(mergedk5, classk20, how='left', left_on=mergId, right_on=mergId)
# print list(mergeFin)
# print "len(mergeFin): " + str(len(mergeFin))

## MAP DESIRED COLUMNS ### 
if (includeAstroData.lower() == 'y' or includeAstroData.lower() == 'yes'):
	desiredColumns = ['dr7objid','G2_x', 'H_x', 'C_x', 'A_x', 'S_x', 'petroR50_r', 'petroMag_r', 
		'class_x', 'class_y', 'class', 'Error_x']
	columnsRenamed = ['Id','G2', 'H', 'C', 'A', 'S', 'petroR50_r', 'petroMag_r', 
		'class-k5Model', 'class-k10Model',	'class-k20Model', 'Error']
	# desiredColumns = ['Id','G2_x', 'H_x', 'C_x', 'A_x', 'S_x', 'class_x', 'class_y', 'Error_x']
	# columnsRenamed = ['Id','G2', 'H', 'C', 'A', 'S', 'class-k5Model', 'class-k20Model', 'Error']
else:
	desiredColumns = ['dr7objid','G2_x', 'H_x', 'C_x', 'A_x', 'S_x', 'class_x', 'class_y', 
		'class', 'Error_x']
	columnsRenamed = ['Id','G2', 'H', 'C', 'A', 'S', 'class-k5Model', 'class-k10Model',
		'class-k20Model', 'Error']

mergeFin = mergeFin[desiredColumns]
mergeFin.columns = columnsRenamed

mergeFin[mergId] = mergeFin[mergId].astype(np.int64)

# mergeFin.loc[(mergeFin['class-k5Model'].isnull()), 'class-k5Model']   = '--'
mergeFin.loc[(mergeFin['class-k10Model'].isnull()), 'class-k10Model'] = '--'
mergeFin.loc[(mergeFin['class-k20Model'].isnull()), 'class-k20Model'] = '--'

print '\nTotal: ' + str(len(mergeFin))
print '\n Total - Input file for k5 classification: ' + str(len(mergedk5))
print 'Total (U+E+S): ' + str(len(mergeFin[(mergeFin['class-k5Model'] == 'U')]) + \
	len(mergeFin[(mergeFin['class-k5Model'] == 'E')]) + len(mergeFin[(mergeFin['class-k5Model'] == 'S')]))
print 'Total classified (E or S) by k5: ' + \
	str(len(mergeFin[(mergeFin['class-k5Model'] == 'E')]) + len(mergeFin[(mergeFin['class-k5Model'] == 'S')]))
print 'E: ' + str(len(mergeFin[(mergeFin['class-k5Model'] == 'E')]))
print 'S: ' + str(len(mergeFin[(mergeFin['class-k5Model'] == 'S')]))
print 'U: ' + str(len(mergeFin[(mergeFin['class-k5Model'] == 'U')]))
print '--: ' + str(len(mergeFin[(mergeFin['class-k5Model'] == '--')]))


print '\n Total - Input file for k10 classification: ' + str(len(classk10))
print 'Total (U+E+S): ' + str(len(mergeFin[(mergeFin['class-k10Model'] == 'U')]) + \
	len(mergeFin[(mergeFin['class-k10Model'] == 'E')]) + len(mergeFin[(mergeFin['class-k10Model'] == 'S')]))
print 'Total classified (E or S) by k10: ' + \
	str(len(mergeFin[(mergeFin['class-k10Model'] == 'E')]) + len(mergeFin[(mergeFin['class-k10Model'] == 'S')]))
print 'E: ' + str(len(mergeFin[(mergeFin['class-k10Model'] == 'E')]))
print 'S: ' + str(len(mergeFin[(mergeFin['class-k10Model'] == 'S')]))
print 'U: ' + str(len(mergeFin[(mergeFin['class-k10Model'] == 'U')]))
print '--: ' + str(len(mergeFin[(mergeFin['class-k10Model'] == '--')]))

print '\n Total - Input file for k20 classification: ' + str(len(classk20))
print 'Total (U+E+S): ' + str(len(mergeFin[(mergeFin['class-k20Model'] == 'U')]) + \
	len(mergeFin[(mergeFin['class-k20Model'] == 'E')]) + len(mergeFin[(mergeFin['class-k20Model'] == 'S')]))
print 'Total classified (E or S) by k20: ' + \
	str(len(mergeFin[(mergeFin['class-k20Model'] == 'E')]) + len(mergeFin[(mergeFin['class-k20Model'] == 'S')]))
print 'E: ' + str(len(mergeFin[(mergeFin['class-k20Model'] == 'E')]))
print 'S: ' + str(len(mergeFin[(mergeFin['class-k20Model'] == 'S')]))
print 'U: ' + str(len(mergeFin[(mergeFin['class-k20Model'] == 'U')]))
print '--: ' + str(len(mergeFin[(mergeFin['class-k20Model'] == '--')]))

mergeFin.to_csv(sys.argv[6], index = False)