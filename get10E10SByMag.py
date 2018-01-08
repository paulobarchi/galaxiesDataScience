# get10E10SByMag.py
# Sort by ascending petroMag_r and get 10 early- and 10 late-type galaxies
# input: input catalog file name, early-type catalog file name, late-type catalog file name and final concatenated file name
# output: catalog with 10 early- and 10 late-type galaxies by ascending petroMag_r

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
