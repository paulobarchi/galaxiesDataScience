import pandas as pd
import sys
import numpy

df = pd.read_csv(sys.argv[1])

index = 'CN'

df[index] = ( df[index] - min(df[index]) ) / \
	( max(df[index]) - min(df[index]) )

index = 'sA3'

df[index] = ( df[index] - min(df[index]) ) / \
	( max(df[index]) - min(df[index]) )

index = 'sS3'

df[index] = ( df[index] - min(df[index]) ) / \
	( max(df[index]) - min(df[index]) )

df.to_csv(sys.argv[2], index=False)