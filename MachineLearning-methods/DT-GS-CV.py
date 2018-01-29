import sys
import timing
import numpy as np
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn import grid_search
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

### -- PRINT TO FILE
orig_stdout = sys.stdout
# open file to write and go to the beginning
output_file = open("DT-GS-CV-k20_sS3_balanced50-50_21-03-2017.txt", 'w')
output_file.seek(0)	
# prints to file (because of 'timing' and 'svm')
sys.stdout = output_file

# read all data
df = pd.read_csv('merged_21-03-2017.csv')
print "Total data before preprocessing: " + str(len(df)) # total data = 51756 rows
# preprocessing: removing objects with NaN values
dt = df[df["CN"].notnull()]
dt = dt[dt["CN"].notnull()]
dt = dt[dt["sA3"].notnull()]
dt = dt[dt["sS3"].notnull()]
dt = dt[dt["sH"].notnull()]
dt = dt[dt["sGa"].notnull()]

### -- BALACING DATASET -- ###
# balanced_dataset = dt.loc[dt['Zoo1'] == 'E'] # create dataset with this galaxies
# E_number = len(balanced_dataset) # get number of elliptical
# all_spiral = dt.loc[dt['Zoo1'] == 'S'] # get all spiral galaxies 
# # get E_number spiral galaxies randomly
# balanced_spiral = all_spiral.ix[random.sample(all_spiral.index, E_number)]
#  # add spiral galaxies to balanced_dataset
# balanced_dataset = balanced_dataset.append(balanced_spiral, ignore_index=True)
# dt = balanced_dataset

dt_len = len(dt)
print "Total data after balancing: " + str(dt_len) 

# print "Total data after preprocessing: " + str(dt_len) 
print "Number of spiral galaxies: " + str(len(dt.loc[dt['Zoo1'] == 'S']))
print "Number of elliptical galaxies: " + str(len(dt.loc[dt['Zoo1'] == 'E']))

# specify which features and target class
# from solo best to all
#features = ["sGa"]
#features = ["sH", "sGa"]
#features = ["sA3", "sH", "sGa"]
#features = ["CN", "sA3", "sH", "sGa"]
features = ["CN", "sA3", "sS3", "sH", "sGa"]

# from solo worst to all
#features = ["sS3"]
#features = ["CN", "sS3"]
#features = ["CN", "sA3","sS3"]
#features = ["CN", "sA3","sS3", "sH"]
#features = ["CN", "sA3","sS3", "sH", "sGa"]

dt['class'] = dt['Zoo1'].map({'S':0,'E':1})

# split data: 4/5 for trainning, 1/5 for testing
train, test = train_test_split(dt, test_size = 0.5)

x_train_data = train[features]
y_train_data = train['class']
x_test_data = test[features]
y_test_data = test['class']

# # set parameter of depth to decision tree
parameters = {'max_depth':range(3,20)}

# perform GridSearchCV to train/validate 
print "GridSearchCV - DecisionTreeClassifier"
gridSearchDTclf = grid_search.GridSearchCV(tree.DecisionTreeClassifier(), parameters, n_jobs=4)
# get fit
dt_fit = gridSearchDTclf.fit(x_train_data, y_train_data)

# print "Best score for best estimator: " + str(gridSearchDTclf.best_score_)
# print "Best parameters: " + str(gridSearchDTclf.best_params_)

# # The mean score and the 95% confidence interval of the score estimate are hence given by:
# scores = cross_val_score(gridSearchDTclf, x_train_data, y_train_data, cv=20)
# print ("Trainning accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

# # predict & get conf. matrix
y_true, y_pred = y_test_data, dt_fit.predict(x_test_data)
# print(classification_report(y_true, y_pred, digits=3))

# print("Confusion Matrix:")
# print(confusion_matrix(y_true, y_pred))

# create output dataframe 
output_df = pd.DataFrame(columns = ["ObjId", "DTree_class"])
output_df["ObjId"] = test["Id"]
output_df["DTree_class"] = y_pred

output_df.to_csv('DTree_classification.csv', index=False)

# return to default stdout
sys.stdout = orig_stdout
output_file.close()