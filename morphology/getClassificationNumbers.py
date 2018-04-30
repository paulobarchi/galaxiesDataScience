import sys
import pandas as pd

# read input data
df = pd.read_csv(sys.argv[1])

k5, k10, k20 = 'class-k5Model' ,'class-k10Model' ,'class-k20Model'

print 'Total: ', len(df)

print '#### Classified by k >= 5 model ####'
print 'Total E: ', len(df[df[k5] == 'E'])
print 'Total S: ', len(df[df[k5] == 'S'])
print 'Total U: ', len(df[df[k5] == 'U'])
print ''
print '#### Classified by k >= 10 model ####'
print 'Total E: ', len(df[df[k10] == 'E'])
print 'Total S: ', len(df[df[k10] == 'S'])
print 'Total U: ', len(df[df[k10] == 'U'])
print ''
print '#### Classified by k >= 20 model ####'
print 'Total E: ', len(df[df[k20] == 'E'])
print 'Total S: ', len(df[df[k20] == 'S'])
print 'Total U: ', len(df[df[k20] == 'U'])
