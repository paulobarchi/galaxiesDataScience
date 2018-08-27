import sys
import pandas as pd

def oneColClassificationByK(x):
	if x['areasRatio'] < 5.0: return '--'
	if x['areasRatio'] >= 5.0 and x['areasRatio'] < 10: return x['DT_k5_class']
	if x['areasRatio'] >= 10.0 and x['areasRatio'] < 20: return x['DT_k10_class']
	if x['areasRatio'] >= 20.0: return x['DT_k20_class']

# input
DL_2018_cat = pd.read_csv(sys.argv[1]).drop_duplicates(subset=['dr7objid'])
CyMorphInp  = pd.read_csv(sys.argv[2]).drop_duplicates(subset=['dr7objid'])
CyMorphInp  = CyMorphInp.rename(columns={'dr7objid':'Id'})
CyMorphOut  = pd.read_csv(sys.argv[3]).drop_duplicates(subset=['Id'])
DT_k5_clas  = pd.read_csv(sys.argv[4]).drop_duplicates(subset=['Id'])
DT_k10_clas = pd.read_csv(sys.argv[5]).drop_duplicates(subset=['Id'])
DT_k20_clas = pd.read_csv(sys.argv[6]).drop_duplicates(subset=['Id'])

#print len(DL_2018_cat)

# only specific columns
CyMorphInp = CyMorphInp[list(['Id','areasRatio'])]
CyMorphOut = CyMorphOut[list(['Id','CN','sA3','sS3','sGa','sH'])]

# merges, drops and renames

#print 'merge1'
merge1 = DL_2018_cat.merge(CyMorphInp, left_on='dr7objid', right_on='Id', how='left')
#print len(merge1)
merge1 = merge1.drop('Id', axis=1) # drop extra id
#print len(merge1)
#print 'merge2'
merge2 = merge1.merge(CyMorphOut, left_on='dr7objid', right_on='Id', how='left')
#print len(merge2)
merge2 = merge2.drop('Id', axis=1) # drop extra id
#print len(merge2)
#print 'merge3'
merge3 = merge2.merge(DT_k5_clas, left_on='dr7objid', right_on='Id', how='left')
#print len(merge3)
merge3 = merge3.rename(columns={'class':'DT_k5_class'})
#print len(merge3)
merge3 = merge3.drop('Id', axis=1) # drop extra id
#print len(merge3)
#print 'merge4'
merge4 = merge3.merge(DT_k10_clas, left_on='dr7objid', right_on='Id', how='left')
#print len(merge4)
merge4 = merge4.rename(columns={'class':'DT_k10_class'})
#print len(merge4)
merge4 = merge4.drop('Id', axis=1) # drop extra id
#print len(merge4)
#print 'merge5'
merge5 = merge4.merge(DT_k20_clas, left_on='dr7objid', right_on='Id', how='left')
#print len(merge5)
merge5 = merge5.rename(columns={'class':'DT_k20_class'})
#print len(merge5)
merge5 = merge5.drop('Id', axis=1) # drop extra id
#print len(merge5)
#print merge5.columns.tolist()


# determining ML classification
merge5['ML_2classes'] = merge5.apply(oneColClassificationByK, axis=1)
# fill NaN values with -9999.999999
merge5[list(['CN','sA3','sS3','sGa','sH'])] = \
	merge5[list(['CN','sA3','sS3','sGa','sH'])].fillna(-9999.999999)
# where there's no classification, assign 'U' ('Undefined')
merge5['ML_2classes'] = merge5['ML_2classes'].fillna('U')
# drop columns with classification for specific k
merge5.drop(['DT_k5_class','DT_k10_class','DT_k20_class'],axis=1,inplace=True)
merge5 = merge5.rename(columns={'CN':'C','sA3':'A','sS3':'S','sGa':'G2','sH':'H'})

# verify if it's alright
#print len(merge5)
#print merge5.columns.tolist()
#print merge5.head(n=20)

merge5.to_csv(sys.argv[7], index=False)
