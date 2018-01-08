import numpy
import csv
import sys
import os

gal = list(csv.reader(open(sys.argv[1], "rb"), delimiter=','))
ndata = len(gal)
header = numpy.array(gal[0])
# gal[1:] = sorted(gal[1:],key=lambda l:l[numpy.where(header == "image")[0][0]])
path = "../Field/"

#myiterMin,myiterMax = int(ndata*float(rank-1)/float(size)+ ndata/float(size)),int(ndata*float(rank)/float(size)+ ndata/float(size))

count = 0

for line in range(1,ndata):
	# imgIndex = numpy.where(header == "image")[0][0]
	ra = gal[line][numpy.where(header == "ra")[0][0]]
	dec = gal[line][numpy.where(header == "dec")[0][0]]
	run = gal[line][numpy.where(header == "run")[0][0]]
	rerun = gal[line][numpy.where(header == "rerun")[0][0]]
	camcol = gal[line][numpy.where(header == "camcol")[0][0]]
	field = gal[line][numpy.where(header == "field")[0][0]]
	dr7id = gal[line][numpy.where(header == "dr7objid")[0][0]]
	band = 'r'
	fileName = 'fpC-%06d-%c%d-%04d.fit' % (int(run),band,int(camcol),int(field))
	if (os.path.isfile(path + fileName)):
		os.remove(path + fileName)
	# else:
	# 	count = count + 1
	print("Downloading ", line)

	cmd = "wget --inet4-only -r -nd --directory-prefix=../Field http://das.sdss.org/raw/"
	cmd += str(run) + "/"
	cmd += str(rerun) + "/corr/"
	cmd += str(camcol) + "/"
	cmd += fileName + ".gz"
	pr = os.popen(cmd)
	print(cmd)
	pr.read()
	# unzip the image
	cmd = "gzip -d " + path + fileName + ".gz"
	pr = os.popen(cmd)
	pr.read()
	#else:
	#	print("Found",line,rank)
# print("Done: ", count)
# comm.Barrier()
