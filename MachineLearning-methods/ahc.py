import sys
import timing
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

### -- PRINT TO FILE
orig_stdout = sys.stdout
# open file to write and go to the beginning
output_file = open("DT-GS-CV-20_dataset80-20_output.txt", 'w')
output_file.seek(0)	
# prints to file (because of 'timing' and 'svm')
sys.stdout = output_file

# read all data
df = pd.read_csv('merged.csv')
print "Total data before preprocessing: " + str(len(df)) # total data = 51756 rows

dt = df[df["CN"].notnull()]
dt_len = len(dt)

print "Total data after preprocessing: " + str(dt_len) 
print "Number of spiral galaxies: " + str(len(dt.loc[dt['Zoo1'] == 'S']))
print "Number of elliptical galaxies: " + str(len(dt.loc[dt['Zoo1'] == 'E']))

# specify which features and target class
features = ["CN","sA3","sS3","sH","sGa"]
dt['class'] = dt['Zoo1'].map({'S':0,'E':1})

x_data = dt[features]
y_data = dt['class']

clustering_output = AgglomerativeClustering(n_clusters=2, linkage='ward').fit(x_data)
y_ahc = clustering_output.labels_

print(classification_report(y_data, y_ahc))

print("Confusion Matrix:")
print(confusion_matrix(y_data, y_ahc))