import sys
import pandas as pd

df = pd.read_csv(sys.argv[1])
spirals = df[(df['TType'] > 2)]

#print len(spirals)
sample = spirals.sample(1000)
#print len(sample)
sample_ids = sample[['dr7objid']].copy()
sample_ids['dr7objid'] = sample_ids['dr7objid'].astype(str) + '.png'
#print len(sample_ids)
sample_ids.to_csv(sys.argv[2], index=False, header=False)