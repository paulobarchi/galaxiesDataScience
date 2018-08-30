import sys
import pandas as pd

# input
CASG2H = pd.read_csv(sys.argv[1])
CACons = pd.read_csv(sys.argv[2])
SmCons = pd.read_csv(sys.argv[3])
SDSS   = pd.read_csv(sys.argv[4])
SDSS   = SDSS.drop_duplicates(subset=['dr7objid'])
GalZo2 = pd.read_csv(sys.argv[5])

# only specific columns
CASG2H = CASG2H[list(['Id','Zoo1class','CN','sA3','sS3','sGa','sH'])]
# merges
merge1 = CASG2H.merge(CACons[list(['Id','C','A'])], left_on='Id', right_on='Id', how='left')
merge2 = merge1.merge(SmCons[list(['Id','SmoothnessConselice'])], left_on='Id', right_on='Id', how='left')
merge3 = merge2.merge(SDSS[list(['dr7objid','ra','dec'])], left_on='Id', right_on='dr7objid', how='left')
merge3 = merge3.drop('dr7objid', axis=1) # drop extra id
merge4 = merge3.merge(GalZo2[list(['dr7objid2','gz2class'])], left_on='Id', right_on='dr7objid2', how='left')
merge4 = merge4.drop('dr7objid2', axis=1) # drop extra id

# rename columns
merge4 = merge4.rename(columns={'Id':'dr7objid','ra':'RA','dec':'DEC','Zoo1class':'GZ1_class',
	'gz2class':'GZ2_class','CN':'C','sA3':'A','sS3':'S','sGa':'G2','sH':'H','C':'C_Cons',
	'A':'A_Cons','SmoothnessConselice':'S_Cons'})
# reorder columns
cols   = merge4.columns.tolist()
cols   = cols[0:1] + cols[-3:-1] + cols[1:2] + cols[-1:] + cols[2:-3]
merge4 = merge4[cols]
# fill NaN values with -9999.999999
merge4 = merge4.fillna(-9999.999999)
# save table
merge4.to_csv(sys.argv[6], index=False)