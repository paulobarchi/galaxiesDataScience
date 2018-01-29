import sys
import timing
import numpy as np
import pandas as pd
from sklearn import tree
from sklearn import grid_search
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import confusion_matrix

### -- PRINT TO FILE
orig_stdout = sys.stdout
# open file to write and go to the beginning
output_file = open("tree-cv15-gridsearch-output.txt", 'w')
output_file.seek(0)	
# prints to file (because of 'timing' and 'svm')
sys.stdout = output_file

# read all data
#df = pd.read_csv('merged.csv',header=None,names=features)
df = pd.read_csv('merged.csv')
#print np.argwhere(df.isnull().any())
print "Total data before preprocessing: " + str(len(df)) # total data = 51756 rows

#dt = df[~np.isnan(df)]
dt = df[df["CN"].notnull()]
dt_len = len(dt)
print "Total data after preprocessing: " + str(dt_len) 
print "Number of eliptical galaxies: " + str(len(dt.loc[dt['Zoo1'] == 'S']))
print "Number of spiral galaxies: " + str(len(dt.loc[dt['Zoo1'] == 'E']))

# header = 
# [Id,CN,sA3,sS3,sH,sGa,Error,dr7objid,ra,dec,z,petroR50_r,deVAB_r,seeing_r,run,camcol,rerun,field,Zoo1,image]

# specify which features
features = ["CN","sA3","sS3","sH","sGa"]
x = dt[features]
# x = np.array(x).reshape((len(x)), 5)
# np.argwhere(np.isnan(x))

# # map and specify target class
dt['class'] = dt['Zoo1'].map({'S':0,'E':1})

y = dt['class']
#y = np.array(y).reshape((len(y)), 1)

# #---
# ## GET DIFFERENT K-FOLD CROSS-VALIDATION TO BUILD TOTAL CONFUSION MATRIX -- ###

dt_classifier = tree.DecisionTreeClassifier()

# # build cross-validation (folds)
cv = cross_validation.KFold(dt_len, n_folds=20,shuffle=True,random_state=None)
for train_index, test_index in cv:
	x_train, x_test = x[train_index], x[test_index]
   	y_train, y_test = y[train_index], y[test_index]

   	# model = specific tree FALTA ISSO
   	dt_fit = dt_classifier.fit(x_train, y_train) # fit model

   	# predict & get conf. matrix
   	current_confusion_matrix = confusion_matrix(y_test, dt_fit.predict(x_test)) 

   	print(current_confusion_matrix)
   	total_cv_conf_matrix = total_cv_conf_matrix + current_confusion_matrix

print "Resulting conf matrix (all matrices summed up):"
print total_cv_conf_matrix
# return to default stdout
sys.stdout = orig_stdout
output_file.close()