import sys
import random

# get input
inputPath = sys.argv[1]
files = [inputPath+'train.txt',inputPath+'val.txt',inputPath+'test.txt']

for file in files:
	# read whole input file
	with open(file) as f:
		originalSample = [line for line in f]

	SB_orig = [line for line in originalSample if '/SB_/' in line]
	S_orig = [line for line in originalSample if '/S_/' in line]
	E_orig = [line for line in originalSample if '/E/' in line]

	overSample = []	
	SB_examples = SB_orig
	S_examples = S_orig
	E_examples = E_orig

	while (len(SB_examples) < len(S_examples)):
		SB_examples = SB_examples + SB_orig
	SB_examples = SB_examples[:len(S_examples)]

	while (len(E_examples) < len(S_examples)):
		E_examples = E_examples + E_orig
	E_examples = E_examples[:len(S_examples)]

	overSample = E_examples + SB_examples + S_examples

	# print 'originalSample: ', len(originalSample)
	# print 'S_examples: ', len(S_examples)
	# print 'E_examples: ', len(E_examples)
	# print 'SB_examples: ', len(SB_examples)
	# print 'overSample: ', len(overSample)
	# exit()

	with open(file, 'w') as f:
		for example in overSample:
	  		print >> f, example.replace("\n", "")
