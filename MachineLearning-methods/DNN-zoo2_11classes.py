from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.utils import shuffle

# ARG PARSER
parser = argparse.ArgumentParser()
parser.add_argument('--input_dataset', default='merged_CyMorph-SDSSk10_Zoo2_11classes.csv', 
    type=str, help='input dataset')
parser.add_argument('--features', default='CN,sA3,sS3,sGa,sH', 
    type=str, help='features')
parser.add_argument('--batch_size', default=100, type=int, help='batch size')
parser.add_argument('--train_steps', default=1000, type=int,
                    help='number of training steps')

# TARGET CLASS
LABEL = 'gz2class'
gTypes = ['Ei','Ec','Er','Sa','Sb','Sc','Sd','SBa','SBb','SBc','SBd']
gTypesNums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
galMap = dict(zip(gTypes, gTypesNums))
proportions = [0.82, 0.62, 0.78, 0.58, 0.86, 0.9, 0.66, 0.5, 0.74, 0.7, 0.54]

# TRAIN TEST FUNCTION
"""Returns the dataset as (train_x, train_y), (test_x, test_y)."""
def get_train_test(df, features):
    filesList = []
    for gTypeNum in gTypesNums:
        # Here, type(gTypeNum) is 'int'
        newDF = df[(df[LABEL] == gTypeNum)]
        newDF = newDF.loc[np.random.permutation(newDF.index)[:int(proportions[gTypeNum]*len(newDF))]]
        filesList.append(newDF)
    # concatenate
    train = pd.concat(filesList)
    test  = df[~df['Id'].isin(train['Id'])]
    return train, test


# INPUT FUNCTIONS
def train_input_fn(data_set, features, num_epochs=None, shuffle=True):
    return tf.estimator.inputs.pandas_input_fn(
        x = pd.DataFrame({k: data_set[k].values for k in features}),
        y = pd.Series(data_set[LABEL].values),
        num_epochs = num_epochs,
        shuffle = shuffle)

def test_input_fn(data_set, features, num_epochs=1, shuffle=False):
    return tf.estimator.inputs.pandas_input_fn(
        x = pd.DataFrame({k: data_set[k].values for k in features}),
        y = pd.Series(data_set[LABEL].values),
        num_epochs = num_epochs,
        shuffle = shuffle)

# MAIN FUNCTION
def main(argv):
    # Read arguments
    args = parser.parse_args(argv[1:])
    features_string = args.features
    dataset = args.input_dataset
    steps = args.train_steps
    batch_size = args.batch_size

    # features
    features = [metric for metric in features_string.split(',')] # list of features
    feature_cols = [tf.feature_column.numeric_column(k) for k in features]

    print("Reading and preprocessing input data...")

    # Read input dataset and preprocess
    df = pd.read_csv(dataset)
    df = df.dropna(subset = [feature for feature in features])    
    df = df[df[LABEL].isin(gTypes)]
    df[LABEL] = df[LABEL].map(galMap).astype(int)
    
    # split data: proportional split by class set size
    print("Splitting data into training and testing sets...")
    train, test = get_train_test(df, features)

    print("Building classifier...")
    # Build 2 hidden layer DNN with 10, 10 units respectively.
    classifier = tf.estimator.DNNClassifier(        
        feature_columns=feature_cols,
        # each <number> is a hidden layer with <number> nodes.
        hidden_units=[10, 10],
        optimizer = tf.train.RMSPropOptimizer(#1e-3
            learning_rate = 0.1
            # ,
            # global_step=0
            # ,
            # l1_regularization_strength = 0.001
        ),#.minimize(loss_tensor,global_step=tf.train.create_global_step()),
        # The model must choose among 11 classes.
        n_classes=11)

    print("Training classifier...")
    # Train the Model.
    classifier.train(input_fn = train_input_fn(train, features), steps=steps)

    print("Evaluating classifier...")
    # Evaluate the model.
    eval_result = classifier.evaluate(input_fn = test_input_fn(test, features))

    print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)
