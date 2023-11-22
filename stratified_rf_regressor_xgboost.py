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
from sklearn.metrics import mean_squared_error

# Open output file for recording performance metrics

output = open ('stratified_results.txt', 'w')
print ('MAE', 'RMSE', sep = '\t', file = output)

# Load RDS file with pandas for model training later on
print ('Loading RDS file...')

readRDS = r['readRDS']
dataset = readRDS('../clusterPhenotypesKmers.rds')
dataset = pandas2ri.rpy2py_dataframe(dataset)

# Convert data to a numpy array
# Features: binary matrix of presence and absence of unique kmer genome-wide
features = np.array(dataset.iloc[:, 2:-1].values)

# Labels: plant weight phenotypes as a proxy to virulence; the lower the value, the strogest the pathogen
labels = np.array(dataset.iloc[:, 1])

print('The shape of our features is:', features.shape)

# Define the model. Parameters have been pre-determined by Scikit-learn's find_best_parameters function

model = xgb.XGBRFRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
                colsample_bytree=0.3, eta=0.5, gamma=0, gpu_id=-1,
                importance_type='gain', interaction_constraints='',
                max_delta_step=0, max_depth=6, min_child_weight=5, missing=None,
                monotone_constraints='()', n_estimators=700, n_jobs=-1,
                num_parallel_tree=700, objective='reg:squarederror',
                random_state=1, reg_alpha=0, scale_pos_weight=1, subsample=1.0,
                tree_method='exact', validate_parameters=1, verbosity=None)

# Cross validation fold split. This step is necessary to avoid overfitting during model training. It splits samples into 10 phenotype groups based on their plant weight values

bins = np.linspace(0, 1, 11)
y_binned = np.digitize(labels, bins)

print(bins)
print(y_binned)

modelCount = 0

# Specify training and testing sizes, and enforce stratification during model training

for i in range (0, 50):
	train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.2, shuffle = True, stratify = y_binned, random_state = i)

	modelCount += 1

# Save stratified group composition for validation

	sets = open ('stratified_sets.txt', 'w')
	print (train_labels, test_labels, file = sets)

# Train model
	print ('Training the model...')
	model.fit(train_features, train_labels)

# Predict labels for the testing group for comparison

	print ('Predicting test labels...')
	predictions = model.predict(test_features)

# Calculate and print mean absolute errors

	print ('Calculating errors...')
	errors = abs(predictions - test_labels)
	mae = round(np.mean(errors), 2)
	print('MAE:', mae)


# Calculate and print root mean squared errors
	rmse = np.sqrt(mean_squared_error(test_labels, predictions))
	print ('RMSE: ', rmse)

# Print performance matrics

	print (mae, rmse, sep = '\t')

# Save model

	model.save_model('stratified_model.model')

# Save performance metrics

print (mae, rmse, sep = '\t', file = output)
sets.close()
