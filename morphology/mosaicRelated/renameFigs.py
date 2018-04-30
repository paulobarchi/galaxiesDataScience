import sys
import os

path = sys.argv[1]
extension = '.png'

def getNewName(filename):
	return filename.split("_")[-1]

# for each png file in directory
for file in os.listdir(path):
	if (not os.path.isdir(file) and file.endswith(extension) ):
		cmd = "mv " + path + file + " " + path + getNewName(file)
		process = os.popen(cmd)
		process.read()