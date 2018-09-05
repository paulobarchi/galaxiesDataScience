import sys
import random

# get input
inputPath = sys.argv[1]
files = [inputPath+'train.txt',inputPath+'val.txt',inputPath+'test.txt']

for file in files:
	# read whole input file
	with open(file) as f:
		originalSample = [line for line in f]

	# get how many examples there are in minority class
	SB_examples = [line for line in originalSample if '/SB_/' in line]
	S_examples = [line for line in originalSample if '/S_/' in line]
	E_examples = [line for line in originalSample if '/E/' in line]

	undersampling = random.sample(E_examples, len(SB_examples)) + \
			SB_examples + random.sample(S_examples, len(SB_examples))

	# print len(undersampling)

	with open(file, 'w') as f:
		for example in undersampling:
	  		print >> f, example.replace("\n", "")
