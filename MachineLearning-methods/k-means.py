import sys
import timing
import numpy as np
import pandas as pd
import random
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

### -- PRINT TO FILE
orig_stdout = sys.stdout
# open file to write and go to the beginning
output_file = open("k-means_CN-sA3-sS3-sH-sGa_unbalanced_22-03-2017.txt", 'w')
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

# ### -- BALACING DATASET -- ###
# balanced_dataset = dt.loc[dt['Zoo1'] == 'E'] # create dataset with this galaxies
# E_number = len(balanced_dataset) # get number of elliptical
# all_spiral = dt.loc[dt['Zoo1'] == 'S'] # get all spiral galaxies 
# # get E_number spiral galaxies randomly
# balanced_spiral = all_spiral.ix[random.sample(all_spiral.index, E_number)]
#  # add spiral galaxies to balanced_dataset
# balanced_dataset = balanced_dataset.append(balanced_spiral, ignore_index=True)
# dt = balanced_dataset

dt_len = len(dt)
# print "Total data after balancing: " + str(dt_len) 

print "Total data after preprocessing: " + str(dt_len) 
print "Number of spiral galaxies: " + str(len(dt.loc[dt['Zoo1'] == 'S']))
print "Number of elliptical galaxies: " + str(len(dt.loc[dt['Zoo1'] == 'E']))

# specify which features and target class
# from solo best to all
#features = ["sGa"]
#features = ["sH", "sGa"]
#features = ["sA3", "sH", "sGa"]
#features = ["CN", "sA3", "sH", "sGa"]
#features = ["CN", "sA3", "sS3", "sH", "sGa"]

# from solo worst to all
# features = ["sS3"]
#features = ["CN", "sS3"]
#features = ["CN", "sA3","sS3"]
#features = ["CN", "sA3","sS3", "sH"]
features = ["CN", "sA3","sS3", "sH", "sGa"]

dt['class'] = dt['Zoo1'].map({'S':0,'E':1})

x_data = dt[features]
y_data = dt['class']

clustering_output = KMeans(init='random', n_clusters=2, n_init=10).fit(x_data)
y_kmeans = clustering_output.labels_

print(classification_report(y_data, y_kmeans, digits=3))

print("Confusion Matrix:")
print(confusion_matrix(y_data, y_kmeans))