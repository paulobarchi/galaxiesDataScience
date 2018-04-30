import pandas as pd
import sys

# read input
df1 = pd.read_csv(sys.argv[1])
df2 = pd.read_csv(sys.argv[2])
col = sys.argv[3]

df2 = df2.drop(col, 1)
# where 1 is the axis number 
# (0 for rows and 1 for columns.)

frames = [df1, df2]

result = pd.concat(frames)

print result.head(5)

result.to_csv(sys.argv[4], index = False)