import sys
import pandas as pd
from shutil import copyfile

k10catalog = pd.read_csv(sys.argv[1])
catal_670k = pd.read_csv(sys.argv[2])
part = sys.argv[3]

inputPath  = '/data/barchi/out_imgs/'+part+'/'
outputPath = '/data/barchi/out_imgs/k10_3classes/'

for index, row in k10catalog.iterrows():
	if (row['dr7objid'] in set(catal_670k['dr7objid'])):
		# copy file
		filename = str(row['dr7objid']) + '.png'
		src = inputPath  + filename
		dst = outputPath + row['gz2class'] + '/' + filename
		copyfile(src, dst)
