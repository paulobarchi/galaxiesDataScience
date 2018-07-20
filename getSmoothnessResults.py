import sys
import pandas as pd

df = pd.read_csv(sys.argv[1])
# Id,segMaskAndCleanTime,RpTime,sC003,sC03,Error,Zoo1class
df = df.drop('sC003', axis=1)
df = df.rename(columns={'sC03':'SmoothnessConselice'})

df.to_csv(sys.argv[2], index=False)