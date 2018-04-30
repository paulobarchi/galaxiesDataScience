import pandas as pd
import sys

# read input
df1 = pd.read_csv(sys.argv[1])
df2 = pd.read_csv(sys.argv[2])

print "len(df1): " + str(len(df1))
print "len(df2): " + str(len(df2))

id1 = 'dr7objid'
id2 = 'dr7objid'

# merging
print 'Merging...'
merged = pd.merge(df1, df2, left_on=id1, right_on=id2)

print "len(merged): " + str(len(merged))
