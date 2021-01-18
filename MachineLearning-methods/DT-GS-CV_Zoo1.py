# DT-GS-CV.py
# Build Decision Tree model with Grid Search and Cross Validation.
# input: file with features and target class, target class, list of metrics separated by comma,
#		percentage of data to be used to train and validate the model, output file name and
#		file name to save the model built.
# output: best score for best estimator, best parameters found for the model, trainning accuracy,
#		classification report, confusion matrix and decision tree model saved to a file.

import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn import grid_search
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.externals import joblib
import numpy as np
import datetime

# use example:
# python DT-GS-CV.py inputFile.csv targetClass list,of,metrics,separated,by,comma 0.1 outputFile.txt dt-gs-cv.pkl

testSize = float(sys.argv[4]) # 0.1
output_filename = sys.argv[5]

# read all data
df = pd.read_csv(sys.argv[1])

with open(output_filename, 'w') as out_file:
	out_file.write('\n Total data before preprocessing: ' + str(len(df)))

# list of features
features = [metric for metric in sys.argv[3].split(',')] 

# remove all rows with NaN for any of the features
df = df.dropna(subset = [feature for feature in features])

targetClass = sys.argv[2]

with open(output_filename, 'a') as out_file:
	out_file.write('\n Total data after preprocessing: ' + str(len(df)))
	out_file.write('\n Number of spiral galaxies: ' + str(len(df.loc[df[targetClass] == 'S'])))
	out_file.write('\n Number of elliptical galaxies: ' + str(len(df.loc[df[targetClass] == 'E'])))

df[targetClass] = df[targetClass].map({'S':0,'E':1})

# split data: (1 - <testSize>) for trainning, <testSize> for testing
train, test = train_test_split(df, test_size = testSize)

x_train_data = train[features]
y_train_data = train[targetClass]

# set parameter of depth to decision tree
parameters = {'max_depth':range(3,20)}

# perform GridSearchCV to train/validate 
gridSearchDTclf = grid_search.GridSearchCV(tree.DecisionTreeClassifier(), parameters, n_jobs=4)

# get fit
dt_fit = gridSearchDTclf.fit(x_train_data, y_train_data)

# The mean score and the 95% confidence interval of the score estimate are hence given by:
scores = cross_val_score(gridSearchDTclf, x_train_data, y_train_data, cv=20)

# predict & get conf. matrix
if (testSize > 0.0):
	x_test_data = test[features]
	y_test_data = test[targetClass]
	y_true, y_pred = y_test_data, dt_fit.predict(x_test_data)
	confMatrix2print = np.matrix(confusion_matrix(y_true, y_pred))

with open(output_filename, 'a') as out_file:
	out_file.write('\n\n ### GridSearchCV - DecisionTreeClassifier ###')
	out_file.write('\n Best score for best estimator: ' + str(gridSearchDTclf.best_score_))
	out_file.write('\n Best parameters: ' + str(gridSearchDTclf.best_params_))
	out_file.write('\n Trainning accuracy: %0.2f (+/- %0.2f)' % (scores.mean(), scores.std() * 2))
	if (testSize > 0.0):
		out_file.write('\n\n Classification Report:\n ')
		out_file.write(classification_report(y_true, y_pred))
		out_file.write('\n Confusion Matrix:\n')
		# out_file.write(confMatrix2print)
		for line in confMatrix2print:
			out_file.write(' ')
			np.savetxt(out_file, line, fmt='%.2f')

# save trained model
joblib.dump(gridSearchDTclf, sys.argv[6])