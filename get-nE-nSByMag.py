# get10E10SByMag.py
# Sort by ascending petroMag_r and get n early- and n late-type galaxies
# input: input catalog file name, early-type catalog file name, late-type catalog file name and final concatenated file name
# output: catalog with n early- and n late-type galaxies by ascending petroMag_r

import pandas as pd
import sys

catalog = pd.read_csv(sys.argv[1])
n = int(sys.argv[1])
# sort by ascending magnitude
catalog = catalog.sort_values('petroMag_r', ascending=True)

# get n first E
catalogE = catalog[(catalog['Zoo1class'] == 'E')].head(n)
# print catalogE
catalogE.to_csv(sys.argv[3], index=False)

# get n first S
catalogS = catalog[(catalog['Zoo1class'] == 'S')].head(n)
# print catalogS
catalogS.to_csv(sys.argv[4], index=False)

# concatenate and save
catalogs = [catalogE, catalogS]
final = pd.concat(catalogs)
final.to_csv(sys.argv[5], index=False)