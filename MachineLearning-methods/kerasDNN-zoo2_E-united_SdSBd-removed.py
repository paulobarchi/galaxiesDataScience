import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

# fix random seed for reproducibility
seed = 3
np.random.seed(seed)

# features
features_string = 'CN,sA3,sS3,sGa,sH'
features = [metric for metric in features_string.split(',')] # list of features

# target class
LABEL = 'gz2class'
gTypes = ['E','Sa','Sb','Sc','SBa','SBb','SBc']
gTypesNums = [0, 1, 2, 3, 4, 5, 6]
galMap = dict(zip(gTypes, gTypesNums))
proportions = [0.832, 0.566, 0.766, 0.9, 0.5, 0.7, 0.632]

# load dataset and preprocess
df = pd.read_csv("merged_CyMorph-SDSSk10_Zoo2_E-united.csv", low_memory=False)
df = df.dropna(subset = [feature for feature in features])
df = df[df[LABEL].isin(gTypes)]
# df[LABEL] = df[LABEL].map(galMap).astype(int)
# dataset = df.values

# defining x and y
X = np.array( pd.DataFrame({k: df[k].values for k in features}) )
Y = np.array( pd.Series(df[LABEL].values) )

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)

# define baseline model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(16, input_dim=5, activation='relu'))
	model.add(Dense(7, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

estimator = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5, verbose=0)

kfold = KFold(n_splits=10, shuffle=True, random_state=seed)

results = cross_val_score(estimator, X, dummy_y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
