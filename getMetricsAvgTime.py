import pandas as pd
import sys

catalog = pd.read_csv(sys.argv[1])

# print catalog.columns.values

avgCN = catalog["CNTime"].mean() + catalog["RpTime"].mean()# + catalog["maskTime"].mean()
avgA = catalog["sA3Time"].mean() + catalog["maskTime"].mean()
avgS = catalog["sS3Time"].mean() + catalog["maskTime"].mean() + catalog["smoothTime"].mean() 
avgH = catalog["sHTime"].mean() + catalog["maskTime"].mean()
avgG1 = catalog["G1Time"].mean() + catalog["maskTime"].mean()
avgG2 = catalog["sGaTime"].mean() + catalog["maskTime"].mean()

print "maskTime = " + str(catalog["maskTime"].mean()) + " milliseconds"
print "RpTime = " + str(catalog["RpTime"].mean()) + " milliseconds"
print "smoothTime = " + str(catalog["smoothTime"].mean()) + " milliseconds"

print ""

print " ### Average Time for Metrics ###"
print "CN time = " + str(avgCN) + " milliseconds"
print "sA3 time = " + str(avgA) + " milliseconds"
print "sS3 time = " + str(avgS) + " milliseconds"
print "sH time = " + str(avgH) + " milliseconds"
print "G1 time = " + str(avgG1) + " milliseconds"
print "sGa time = " + str(avgG2) + " milliseconds"