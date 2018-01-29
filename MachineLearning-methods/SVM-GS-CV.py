import sys
import timing
import numpy as np
import pandas as pd
import random
#from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

### -- PRINT TO FILE
orig_stdout = sys.stdout
# open file to write and go to the beginning
output_file = open("SVM-GS-CV-k20_sS3_balanced-50-50_21-03-2017.txt", 'w')
output_file.seek(0)	
# prints to file (because of 'timing' and 'svm')
sys.stdout = output_file

# read all data
df = pd.read_csv('merged_21-03-2017.csv')
print "Total data before preprocessing: " + str(len(df)) # total data = 51756 rows
# preprocessing: removing objects with NaN values
dt = df[df["CN"].notnull()]
dt = dt[dt["sA3"].notnull()]
dt = dt[dt["sS3"].notnull()]
dt = dt[dt["sH"].notnull()]
dt = dt[dt["sGa"].notnull()]

### -- BALACING DATASET -- ###
balanced_dataset = dt.loc[dt['Zoo1'] == 'E'] # create dataset with this galaxies
E_number = len(balanced_dataset) # get number of elliptical
all_spiral = dt.loc[dt['Zoo1'] == 'S'] # get all spiral galaxies 
# get E_number spiral galaxies randomly
balanced_spiral = all_spiral.ix[random.sample(all_spiral.index, E_number)]
 # add spiral galaxies to balanced_dataset
balanced_dataset = balanced_dataset.append(balanced_spiral, ignore_index=True)
dt = balanced_dataset

dt_len = len(dt)
print "Total data after balancing: " + str(dt_len) 

# print "Total data after preprocessing: " + str(dt_len) 
print "Number of spiral galaxies: " + str(len(dt.loc[dt['Zoo1'] == 'S']))
print "Number of elliptical galaxies: " + str(len(dt.loc[dt['Zoo1'] == 'E']))

# ### -- NORMALIZE DATA -- ###
#dt_norm = (dt - dt.min()) / (dt.max() - dt.min())
#dt = dt_norm

# features = ["CN", "sA3", "sS3", "sH", "sGa"]

# norm_dt = dt.copy()
# for feature_name in features:
# 	max_value = dt[feature_name].max()
# 	min_value = dt[feature_name].min()
# 	norm_dt[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)

# dt = norm_dt

# values = df.values #returns a numpy array
# min_max_scaler = preprocessing.MinMaxScaler()
# scaled_values = min_max_scaler.fit_transform(values)
# dt = pandas.DataFrame(scaled_values)

# specify which features and target class
# from solo best to all
#features = ["sGa"]
#features = ["sH", "sGa"]
#features = ["sA3", "sH", "sGa"]
#features = ["CN", "sA3", "sH", "sGa"]
#features = ["CN", "sA3", "sS3", "sH", "sGa"]

# from solo worst to all
features = ["sS3"]
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

# Set the parameters by cross-validation
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

#scores = ['precision', 'recall']

#for score in scores:
    #print("# Tuning hyper-parameters for %s" % score)
    #print()

clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=20)#,
                   #scoring='%s_macro' % score)
clf.fit(x_train_data, y_train_data)

print("Best parameters set found on development set:")
print()
print(clf.best_params_)
print()
print("Grid scores on development set:")
print()
means = clf.cv_results_['mean_test_score']
stds = clf.cv_results_['std_test_score']
for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    print("%0.3f (+/-%0.03f) for %r"
          % (mean, std * 2, params))
print()

print("Detailed classification report:")
print()
print("The model is trained on the full development set.")
print("The scores are computed on the full evaluation set.")
print()
y_true, y_pred = y_test_data, clf.predict(x_test_data)
print(classification_report(y_true, y_pred, digits=3))

print("Confusion Matrix:")
print(confusion_matrix(y_true, y_pred))

# return to default stdout
sys.stdout = orig_stdout
output_file.close()