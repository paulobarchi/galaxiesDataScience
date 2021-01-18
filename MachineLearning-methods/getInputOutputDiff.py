# getInputOutputDiff.py
# verify if all fits in given directory have results
# input: results csv file and directory with fits files
# output: print number of input files, results length and difference

import os
import sys
import pandas as pd

outputData = pd.read_csv(sys.argv[1])
path = sys.argv[2]

extension = '.fits'

outputLen = len(outputData)

inputLen = 0

for file in os.listdir(path):	
	if file.endswith(extension):
		inputLen += 1

print 'inputLen = '+str(inputLen)

print 'outputLen = '+str(outputLen)

print 'Diff = '+str(inputLen-outputLen)