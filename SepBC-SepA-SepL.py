import numpy
import pandas as pd
from math import sqrt
import sys

def distanceMetric(data1, data2, metrics, outFile):
	columns = ['metric', 'SepBCA', 'SepBCL', 'SepBC']

	numpy.savetxt(outFile, numpy.array([columns]), delimiter=',', fmt="%s")

	for metric in metrics:
		hist1, bins1 = numpy.histogram(data1[metric])
		hist2, bins2 = numpy.histogram(data2[metric])
		both = numpy.concatenate((bins1,bins2))
		# n is the number of bins (average between the number of both bins)
		n = len(both)/2
		rnge = (numpy.min(both),numpy.max(both))
		hist1, bins1 = numpy.histogram(ell[metric],bins=n,range=rnge,normed=True)
		hist2, bins2 = numpy.histogram(sp[metric],bins=n,range=rnge,normed=True)

		# since both histograms have same bins, dy is the inteserction
		dx = (rnge[1]-rnge[0])/n
		dy = numpy.minimum(hist1,hist2)

		# ao is the relative area
		ao = numpy.sum(dy*dx)

		a_height = numpy.max(hist1)
		b_height = numpy.max(hist2)
		c_height = numpy.max(dy)

		separation_BCL = (a_height + b_height - 2.0 * c_height) / (a_height + b_height)
		separation_BCA = 1 - (ao) / (2.0 - ao)

		final_separation = ( sqrt(separation_BCA) + separation_BCL ) / 2.0

		results = [metric, separation_BCA, separation_BCL, final_separation]

		with open(outFile,'a') as f_handle:
			numpy.savetxt(f_handle, numpy.array([results]), delimiter=',', fmt="%s")		

		# print 'Separation BCA: ', separation_BCA
		# # print 'a height:', a_height
		# # print 'b height:', b_height
		# # print 'c height:', c_height	
		# print 'Separation_BCL: ', separation_BCL
		# print 'Separation (final): ', final_separation
		# return final_separation	

if __name__ == "__main__":
	ell = pd.read_csv(sys.argv[1]).dropna()
	sp = pd.read_csv(sys.argv[2]).dropna()
	outFile = sys.argv[3]
	# distanceMetric(ell[metrica], sp[metrica])
	metrics = ['C', 'A', 'S']
	distanceMetric(ell, sp, metrics, outFile)
