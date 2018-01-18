import sys
import pandas as pd

classic = pd.read_csv(sys.argv[1])
CyMorph = pd.read_csv(sys.argv[2])
errorFlag = sys.argv[3]

print "CyMorph: " + str(len(CyMorph))
print "classic: " + str(len(classic))
print "difference: " + str(len(CyMorph) - len(classic))

# Filter CyMorph result by errorFlag
# if 0, considering only results with errorFlag == 0
if int(errorFlag) == 0:
	new_CyMorph = CyMorph[CyMorph['Error'] == 0]
# else, exclude errorFlag specified
else:
	new_CyMorph = CyMorph[CyMorph['Error'] != errorFlag]

print "new_CyMorph: " + str(len(new_CyMorph))

# filter both results
new_classic = classic[classic['Id'].isin(new_CyMorph['Id'])]
print "new_classic: " + str(len(new_classic))

new_CyMorph = new_CyMorph[new_CyMorph['Id'].isin(new_classic['Id'])]
print "new_CyMorph: " + str(len(new_CyMorph))

# save result
new_classic.to_csv(sys.argv[4], index=False)
new_CyMorph.to_csv(sys.argv[5], index=False)
