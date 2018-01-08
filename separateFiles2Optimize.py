import pandas as pd
import os
import sys

# open file with all galaxies
# file = pd.read_csv('../../../CyMorph_master/57000_20k_Zoo1_EeS.csv')
file = pd.read_csv(sys.argv[1])
total = len(file)
print("Total: " + str(total))

elliptical = file[file["Zoo1class"] == 'E']
print(" Elliptical len : " + str(len(elliptical)))

spiral = file[file["Zoo1class"] == 'S']
print(" Spiral len : " + str(len(spiral)))

# 1 csv file for each class
elliptical.head(n=1000).to_csv(sys.argv[2], index=False)
spiral.head(n=1000).to_csv(sys.argv[3], index=False)