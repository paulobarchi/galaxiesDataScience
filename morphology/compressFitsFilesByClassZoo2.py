import sys
import pandas as pd
import numpy as np
import tarfile

# read input
inputCat = pd.read_csv(sys.argv[1])
gType = sys.argv[2]
source_dir = sys.argv[3]

idCol = 'dr7objid'
column = 'gz2class'
inputCat.loc[:,idCol] = inputCat.loc[:,idCol].astype(np.int64)
# gType = ['Ei','Ec','Er','Sa','Sb','Sc','Sd','SBa','SBb','SBc','SBd']
# print "Total: " + str(len(inputCat))
out = tarfile.open(gType+'.tar.gz', mode='w')
# open tarfile

for index, row in inputCat.iterrows():
	if (row[column] == gType):
		# print "index: " + str(index)
		# print "file: " + str(row['Id'])+'_wout-cleaning_stamp5.fit'
		# print "gType: " + gType + "; row[class]: " + row[column]
		try:
			out.add(
				# path+file
				name = source_dir+str(row[idCol])+'_wout-cleaning_stamp5.fit',
				# (new) file name in tar file
				arcname = str(row[idCol])+'.fit')
		except Exception: 
  			pass
		# print "Done line " + str(index)

out.close()
