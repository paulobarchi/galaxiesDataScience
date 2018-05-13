import sys
import pandas as pd
import numpy as np
import tarfile

# read input
sdss = pd.read_csv(sys.argv[1]) # k5_defined
gZoo = pd.read_csv(sys.argv[2]) # zoo1
source_dir = sys.argv[2]

id_sdss = 'dr7objid'
id_zoo1 = 'OBJID'
column = 'Zoo1class'

outE = tarfile.open('E.tar.gz', mode='w')
outS = tarfile.open('S.tar.gz', mode='w')

# merging
# print 'Merging SDSS and GZ...'
merged = pd.merge(sdss, gZoo, left_on=id_sdss,right_on=id_zoo1)

print 'Total merged: ', len(merged)
# print 'Total unique merged: ', len(pd.unique(merged[id_sdss].values))
print 'Total E: ', len(merged[merged[column] == 'E'])
print 'Total S: ', len(merged[merged[column] == 'S'])

# print list(merged)

for index, row in merged.iterrows():
	# print "file: " + str(row[id_sdss])+'.png'
	# print "row[class]: " + row[column]
	if (row[column] == 'E'):
		try:
			outE.add(
				# path+file
				name = source_dir+'E/'+str(row[id_sdss])+'.png',
				# (new) file name in tar file
				arcname = str(row[id_sdss])+'.png')
		except Exception:
  			pass
  	elif (row[column] == 'S'):
		try:
			outS.add(
				# path+file
				name = source_dir+'S/'+str(row[id_sdss])+'.png',
				# (new) file name in tar file
				arcname = str(row[id_sdss])+'.png')
		except Exception: 
  			pass
		
	print "Done %.5f %%" % ( (float(index)/float(len(merged))) * 100 )

outE.close()
outS.close()
