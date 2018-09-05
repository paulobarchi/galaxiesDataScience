import sys
import random

# get input
inputPath = sys.argv[1]
files = [inputPath+'train.txt',inputPath+'val.txt',inputPath+'test.txt']

for file in files:
	# read whole input file
	with open(file) as f:
		originalSample = [line for line in f]

	SB_examples = [line for line in originalSample if '/SB_/' in line]
	S_examples = [line for line in originalSample if '/S_/' in line]
	E_examples = [line for line in originalSample if '/E/' in line]

	smoteSample = []

	# get how many examples there are in minority class
	if (2*len(SB_examples) < len(E_examples)):
		smoteSample = random.sample(E_examples, 2*len(SB_examples)) + \
			SB_examples + SB_examples + random.sample(S_examples, 2*len(SB_examples))
	else:
		SB_examples = SB_examples + SB_examples
		smoteSample = E_examples + random.sample(SB_examples, len(E_examples)) + \
			random.sample(S_examples, len(E_examples))

	print len(smoteSample)

	with open(file, 'w') as f:
		for example in smoteSample:
	  		print >> f, example.replace("\n", "")
