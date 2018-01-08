# seqMorph.py
# Sequentially run CyMorph for stamps in a path
# input: path to stamps, file extension, output file name and boolean to save (or not) intermediary images
# output: CyMorph output (non-parametric morphology parameters)

import ConfigParser
import os
import sys
import csv

# run example:
# python seqMorph.py <path_to_stamps> <extension> <output_file_name> <saveFigBoolean>

def removeExtension(fileName):
	return fileName.split('.')[0]

path = sys.argv[1] # must end with "/"
extension = sys.argv[2]
resultFile = sys.argv[3]
saveFig = sys.argv[4]

# TODO: desired morph indexes as arguments???

# make first changes in config.ini
configFileName = 'config.ini'
configParser = ConfigParser.ConfigParser()
configParser.read(configFileName)
configParser.set('File_Configuration', 'Path', path)

if (saveFig == 'True'):
	configParser.set('Output_Configuration', 'SaveFigure', 'True')
else:
	configParser.set('Output_Configuration', 'SaveFigure', 'False')

# command to run CyMorph
cmd = "python main.py config.ini"
singleResultFile = "Result.csv"
i = 0

for file in os.listdir(path):	
	if file.endswith(extension):
		objId = removeExtension(file)
		
		# change config.ini for current file
		configParser.set('File_Configuration', 'Filename', file)

		# before running CyMorph, save config.ini
		with open(configFileName, 'wb') as configFile:
			configParser.write(configFile)

		# run CyMorph for this galaxy
		print("\n Running CyMorph for galaxy: " + objId)
		pr = os.popen(cmd)
		pr.read()
		
		# get Result
		reader = csv.reader(open(singleResultFile))
		lines = [l for l in reader]
		lines[1][0] = objId
		
		# if first result	
		if (i == 0):
			# save header and result to file
			with open(path+resultFile, 'wb') as csv_file:
				writer = csv.writer(csv_file)
				for line in lines:
					writer.writerows([line])
		else:
			# save only result
			with open(path+resultFile, 'ab') as csv_file:
				writer = csv.writer(csv_file)
				writer.writerows([lines[1]])
		
		pr = os.popen("rm "+singleResultFile)
		pr.read()

		# backup saveFig content
		if (saveFig == 'True'):
			pr = os.popen("mkdir "+path+objId)
			pr.read()
			pr = os.popen("mv imgs/* "+path+objId+"/")
			pr.read()

		print(" " + objId + " done.")
		i = i + 1
