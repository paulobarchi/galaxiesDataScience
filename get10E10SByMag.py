import pandas as pd
import sys

catalog = pd.read_csv(sys.argv[1])
# sort by ascending magnitude
catalog = catalog.sort_values('petroMag_r', ascending=True)

# get 10 first E
catalogE = catalog[(catalog['Zoo1class'] == 'E')].head(10)
# print catalogE
catalogE.to_csv(sys.argv[2], index=False)

# get 10 first S
catalogS = catalog[(catalog['Zoo1class'] == 'S')].head(10)
# print catalogS
catalogS.to_csv(sys.argv[3], index=False)

# concatenate and save
catalogs = [catalogE, catalogS]
final = pd.concat(catalogs)
final.to_csv(sys.argv[4], index=False)