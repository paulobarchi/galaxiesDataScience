import sys
import pandas as pd
import numpy as np
import tarfile

# read input
inputCat = pd.read_csv(sys.argv[1])
gType = sys.argv[2]
source_dir = sys.argv[3]
outPath = sys.argv[4]

idCol = 'dr7objid'
column = 'gz2class'
inputCat.loc[:,idCol] = inputCat.loc[:,idCol].astype(np.int64)

out = tarfile.open(outPath+gType+'.tar.gz', mode='w')

for index, row in inputCat.iterrows():
	if (row[column] == gType):
		try:
			outE.add(
				# path+file
				name = source_dir+gType+'/'+str(row[id_sdss])+'.png',
				# (new) file name in tar file
				arcname = str(row[id_sdss])+'.png')
		except Exception:
  			pass
  			
	print "Done %.5f %%" % ( (float(index)/float(len(inputCat))) * 100 )

out.close()
