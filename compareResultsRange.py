import sys
import pandas as pd

# read datasets
ours = pd.read_csv(sys.argv[1])
dailers = pd.read_csv(sys.argv[2])

# get dailers results which are in ours
dailers_reduced = dailers[dailers['name'].isin(ours['Id']) == True]
print "len(dailers_reduced): " + str(len(dailers_reduced))

print "\n ### Indexes Ranges ###\n"
print " Ours"
print "C: [" + str(ours["C"].min()) + ", " + str(ours["C"].max()) + "]"
print "A: [" + str(ours["A"].min()) + ", " + str(ours["A"].max()) + "]"
print "S: [" + str(ours["S"].min()) + ", " + str(ours["S"].max()) + "]\n"

print " Dailers"
print "C: [" + str(dailers_reduced["C"].min()) + ", " + str(dailers_reduced["C"].max()) + "]"
print "A: [" + str(dailers_reduced["A"].min()) + ", " + str(dailers_reduced["A"].max()) + "]"
print "S: [" + str(dailers_reduced["S"].min()) + ", " + str(dailers_reduced["S"].max()) + "]\n"