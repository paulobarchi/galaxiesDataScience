import pandas as pd
import sys
import os
from shutil import copyfile

# read input
kids_cat = pd.read_csv(sys.argv[1], header=None)
# header should be:
# sdssId	gz2class	filename	kidsId	matchRadius	kidsFlag1	kidsFlag2	kidsFOV
inputDir = sys.argv[2] # must end with "/"

print 'len(kids_cat) = ',len(kids_cat)

# for file in os.listdir(path):
for index, row in kids_cat.iterrows():
	src = inputDir + row[2]
	dst = ''
	if (row[1] == 'E'):
		dst = dst + 'E/' + row[2]
	elif (row[1] == 'S_'):
		dst = dst + 'S_/' + row[2]
	elif (row[1] == 'SB_'):
		dst = dst + 'SB_/' + row[2]
	copyfile(src, dst)	
