import pandas as pd
import sys

# use example:
# python getIds.py <inputFile> <IdColumn> <outputFile>

df = pd.read_csv(sys.argv[1])

columns = [sys.argv[2]]

df[columns].to_csv(sys.argv[3], index=False)