# getImgsFromK5.py
# select images to save from K5 images
# input: csv file with list of galaxies, input path to imgs, output path to save images
# output: images (png) saved to output path

import pandas as pd
import os
import sys

inputFile = pd.read_csv(sys.argv[1])
idCol = sys.argv[2]
classCol = sys.argv[3]
inputPath = sys.argv[4]  # must end with "/"
outputPath = sys.argv[5] # must end with "/"
desiredClass = sys.argv[6]

classCount = 0
imgAlreadyDone = 0

for index, row in inputFile.iterrows():
	if (row[classCol] == desiredClass):
		classCount = classCount + 1
		# generate file path and name, and search
		fname = inputPath+str(row[idCol])+'.png'
		if (os.path.isfile(fname)):
			imgAlreadyDone = imgAlreadyDone + 1
			dest = fname.replace(inputPath.split('/')[0], outputPath.split('/')[0])
			# print 'fname: ' + fname
			# print 'dest: ' + dest
			cmd = "cp "+fname+" "+dest
			# print 'cmd: '+cmd
			# exit()
			process = os.popen(cmd)
			process.read()
	# print "Done %.5f %%" % ( (float(index)/float(len(inputFile))) * 100)

print 'outputPath: '+outputPath
print 'len(gz2class == desiredClass): ' + str(len(inputFile[inputFile[classCol] == desiredClass]))
print 'classCount: ' + str(classCount)
print 'imgAlreadyDone: ' + str(imgAlreadyDone)