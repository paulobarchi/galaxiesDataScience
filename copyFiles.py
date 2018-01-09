# copyFiles.py
# script to copy desired files (in catalog) to destination.
# input: catalog with filenames and destination
# output: none.

import pandas as pd
import sys
import os
import shutil

catalog = pd.read_csv(sys.argv[1])
dest = sys.argv[2]
src = '../cutted/'

# for each instance in catalog
for index, row in catalog.iterrows():
	# get file name
	file_name = str(row['dr7objid']) + '.fit'
	full_file_name = os.path.join(src,file_name)
	# copy to desired directory
	shutil.copy(full_file_name, dest)
