import sys
import pandas as pd
import tarfile

# read input
sdss = pd.read_csv(sys.argv[1]) # k5_defined
gZoo = pd.read_csv(sys.argv[2]) # zoo1

source_dir = sys.argv[3]

outE = "E.tar.gz" # sys.argv[4]
outS = "S.tar.gz" # sys.argv[5]

id_sdss = 'dr7objid'
id_zoo1 = 'OBJID'

# merging
print 'Merging SDSS and GZ...'
merged = pd.merge(sdss, gZoo, left_on=id_sdss,right_on=id_zoo1)

# print 'Total merged: ', len(merged)
# print 'Total unique merged: ', len(pd.unique(merged[id_sdss].values))
print 'Total E: ', len(merged[merged['Zoo1class'] == 'E'])
print 'Total S: ', len(merged[merged['Zoo1class'] == 'S'])

fits_E = []
fits_S = []

for index, row in merged.iterrows():
	if (row['Zoo1class'] == 'E'):
		fits_E.append(str(row['dr7objid']))
	elif (row['Zoo1class'] == 'S'):
		fits_S.append(str(row['dr7objid']))


print 'fits_E: ' + str(len(fits_E))
print 'fits_S: ' + str(len(fits_S))

with tarfile.open(outE, "w:gz") as tar:
	for item in fits_E:
		tar.add(source_dir, item+'_wout-cleaning_stamp5.fit')

with tarfile.open(outS, "w:gz") as tar:
	for item in fits_S:
		tar.add(source_dir, item+'_wout-cleaning_stamp5.fit')