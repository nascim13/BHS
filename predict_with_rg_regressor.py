# Load required libraries

import pandas as pd
import numpy as np
from rpy2.robjects import r
from rpy2.robjects import pandas2ri
import xgboost as xgb
from sklearn.model_selection import KFold
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split

# Open output file to save predictions
output = open ('Model_7_predictions.txt', 'w')
print ('Isolate', 'Value', 'Def', sep = '\t', file = output)

# Load RDS file with pandas for model prediction
print ('Loading RDS file...')

readRDS = r['readRDS']
dataset = readRDS('clusterPhenotypesKmers.rds')
dataset = pandas2ri.rpy2py_dataframe(dataset)
ids = np.array(dataset.iloc[:, 0])

# Convert data to a numpy array
# Features: binary matrix of presence and absence of unique kmer genome-wide
features = np.array(dataset.iloc[:, 1:-1].values)

data_dmatrix = xgb.DMatrix(data = features, label = labels)

# Load model
model = xgb.Booster({'nthread': -1})
model.load_model('Models/model7.model')

# Make predictions
predictions = model.predict(data_dmatrix)

# Print real and predicted values for each sample
for i in range (0, len(ids)):
	print (ids[i], predictions[i], 'Prediction', sep = '\t', file = output)
