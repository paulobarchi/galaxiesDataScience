# DT-GS-CV_Zoo2.py
# Build Decision Tree model with Grid Search and Cross Validation.
# input: file with features and target class, target class, list of metrics separated by comma,
#		percentage of data to be used to train and validate the model, output file name and
#		file name to save the model built.
# output: best score for best estimator, best parameters found for the model, training accuracy,
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
# python DT-GS-CV_Zoo2.py inputFile.csv targetClass list,of,metrics,separated,by,comma False outputFile.txt dt-gs-cv.pkl

# read input
df = pd.read_csv(sys.argv[1])
targetClass = sys.argv[2]
features = [metric for metric in sys.argv[3].split(',')] # list of features
fullSupervision = sys.argv[4]
output_filename = sys.argv[5]

gTypes = ['Ei','Ec','Er','Sa','Sb','Sc','Sd','SBa','SBb','SBc','SBd']
gTypesNums = [0,1,2,3,4,5,6,7,8,9,10]
proportions = [0.82, 0.62, 0.78, 0.58, 0.86, 0.9, 0.66, 0.5, 0.74, 0.7, 0.54]
# Ei galaxies: 13538; prop = 0.82
# Ec galaxies: 1748; prop = 0.62
# Er galaxies: 12928; prop = 0.78
# Sa galaxies: 654; prop = 0.58
# Sb galaxies: 19219; prop = 0.86
# Sc galaxies: 28706; prop = 0.9
# Sd galaxies: 2604; prop = 0.66
# SBa galaxies: 116; prop = 0.5
# SBb galaxies: 6191; prop = 0.74
# SBc galaxies: 4928; prop = 0.7
# SBd galaxies: 346; prop = 0.54

with open(output_filename, 'w') as out_file:
	out_file.write('\n Total data before preprocessing: ' + str(len(df)))
	for gType in gTypes:
		out_file.write('\n Number of ' + gType + ' galaxies: ' + str(len(df.loc[df[targetClass] == gType])))

# remove all rows with NaN for any of the features or targetClass
print "Preprocessing..."
df = df.dropna(subset = [feature for feature in features])

df[targetClass] = df[targetClass].map({'Ei':0,'Ec':1,'Er':2,'Sa':3,'Sb':4,'Sc':5,'Sd':6,'SBa':7,'SBb':8,'SBc':9,'SBd':10})
df = df[df[targetClass].notnull()]

with open(output_filename, 'a') as out_file:
	out_file.write('\n\n Total data after preprocessing: ' + str(len(df)))
	for gTypeNum in gTypesNums:
		out_file.write('\n Number of ' + gTypes[gTypeNum] + ' galaxies: ' + str(len(df.loc[df[targetClass] == gTypeNum])))


useProps = True

if (useProps):
	# split data: proportional split by class set size
	filesList = []

	# for each gType
	for gTypeNum in gTypesNums:
		newDF = df[(df[targetClass] == gTypeNum)]
		# print str( proportions[gTypeNum] ) + " x " + str(len(newDF)) + " = " + str(int(proportions[gTypeNum]*len(newDF)))
		newDF = newDF.loc[np.random.permutation(newDF.index)[:int(proportions[gTypeNum]*len(newDF))]]
		filesList.append(newDF)

	# concatenate
	train = pd.concat(filesList)
	test = df[df['Id'].isin(train['Id']) == False]

else:
	# split data: stratified
	train, test = train_test_split(df, test_size = 0.1, stratify = df[targetClass])

with open(output_filename, 'a') as out_file:
	out_file.write('\n\n Training set size: ' + str(len(train)))
	out_file.write('\n Test set size: ' + str(len(test)))

x_train_data = train[features]
y_train_data = train[targetClass]

# set parameter of depth to decision tree
parameters = {'max_depth':range(3,20)}

# perform GridSearchCV to train/validate 
gridSearchDTclf = grid_search.GridSearchCV(tree.DecisionTreeClassifier(), parameters, n_jobs=8)

# get fit
dt_fit = gridSearchDTclf.fit(x_train_data, y_train_data)

# The mean score and the 95% confidence interval of the score estimate are hence given by:
scores = cross_val_score(gridSearchDTclf, x_train_data, y_train_data, cv=10)

# predict & get conf. matrix
if (fullSupervision != "True"):
	x_test_data = test[features]
	y_test_data = test[targetClass]
	y_true, y_pred = y_test_data, dt_fit.predict(x_test_data)
	confMatrix2print = np.matrix(confusion_matrix(y_true, y_pred))

with open(output_filename, 'a') as out_file:
	out_file.write('\n\n ### GridSearchCV - DecisionTreeClassifier ###')
	out_file.write('\n Best score for best estimator: ' + str(gridSearchDTclf.best_score_))
	out_file.write('\n Best parameters: ' + str(gridSearchDTclf.best_params_))
	out_file.write('\n Training accuracy: %0.2f (+/- %0.2f)' % (scores.mean(), scores.std() * 2))
	if (fullSupervision != "True"):
		out_file.write('\n\n Classification Report:\n ')
		out_file.write(classification_report(y_true, y_pred))
		out_file.write('\n Confusion Matrix:\n')
		# out_file.write(confMatrix2print)
		for line in confMatrix2print:
			out_file.write(' ')
			np.savetxt(out_file, line, fmt='%.2f')

# save trained model
joblib.dump(gridSearchDTclf, sys.argv[6])