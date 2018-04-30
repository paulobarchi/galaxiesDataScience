# classifyUnlabeledDataWithModel.py
# Classify unlabeled data with already built decision tree model
# input: csv file with result from CyMorph, Id column name, list,of,features,separated,by,comma
#		pkl file with already built model and keyword to contitute the output file
# output: csv file with Ids and classifications

# example to run: 
# python classifyUnlabeledDataWithModel.py resultFromCyMorph.csv Id CN,sA3,sS3,sH,sGa model.pkl Shapley

import pandas as pd
import sys
from sklearn.externals import joblib
import datetime

def intToClass(i):
	if i == 0:
		return 'S' # spiral
	elif i == 1:
		return 'E' # elliptical
	else:
		return 'U' # undefined

# read dataset
inputDF = pd.read_csv(sys.argv[1])

# tr column to build output file with classification
idColumn = sys.argv[2]
classCol = 'class'

# list of features
features = [metric for metric in sys.argv[3].split(',')] 

# load DT model
clf = joblib.load(sys.argv[4]) 

# output file with classification
output_keyword = sys.argv[5]

print '\n Total data before preprocessing: ' + str(len(inputDF))

# remove all rows with NaN for any of the features
inputDF = inputDF.dropna(subset = [feature for feature in features])

print ' Total data after preprocessing: ' + str(len(inputDF))

# classify
predictions = clf.predict(inputDF[features])

# build output dataframe
outputDF = pd.DataFrame(columns=(idColumn, classCol))
outputDF[idColumn] = inputDF[idColumn]
outputDF[classCol] = list(map(intToClass, predictions))

print '\n Number of spiral galaxies: ' + str(len(outputDF.loc[outputDF[classCol] == 'S']))
print ' Number of elliptical galaxies: ' + str(len(outputDF.loc[outputDF[classCol] == 'E']))
# print '\n Number of undefined galaxies: ' + str(len(outputDF.loc[outputDF[classCol] == 'U']))

# build classification file name
dateString = datetime.date.today().strftime("%b-%d-%y")
classiFile = 'DT-classification_' + output_keyword + '_' + dateString + '.csv'

# save classification
outputDF.to_csv(classiFile, index=False)