# unify11classesTo3classesZoo2.py
# Given the file with CyMorph results and gz2class (for each galaxy, 1 class out of 11),
# 	generates a similar file, but, for each galaxy, 1 class out of 3.
# input: file with CyMorph results and gz2class; and an output file name.
# output: csv file with CyMorph result and "new" galaxy type (unified from 11 to 3 classes).

import pandas as pd
import sys

# read input
df = pd.read_csv(sys.argv[1])
outputFileName = sys.argv[2]

# E = [Ei, Ec, Er]

for i, row in df.iterrows():
	ifor_val = 'U'
	if row['gz2class'].startswith('E'):
		ifor_val = 'E'
		df.set_value(i,'gz2class', ifor_val)
	# elif row['gz2class'].startswith('SB'):
	# 	ifor_val = 'SB_'
	# elif row['gz2class'].startswith('S'):
	# 	ifor_val = 'S_'
	# df.set_value(i,'gz2class', ifor_val)
	

# shuffle and get a sample to visually verify
# print df.sample(frac=1).head(n=100) 

df.sample(frac=1).to_csv(outputFileName, index = False)