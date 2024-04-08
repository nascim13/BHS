# Import necessary libraries
import pandas as pd
import numpy as np
from rpy2.robjects import r, pandas2ri
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import sys

# Open output file to log model performance metrics
output = open('Results/stratified_results.txt', 'w')
print('Model', 'MAE', 'RMSE', sep='\t', file=output)

# Load dataset from RDS file specified as command line argument
print('Loading RDS file...')
readRDS = r['readRDS']
dataset = readRDS(sys.argv[1])
dataset = pandas2ri.rpy2py_dataframe(dataset)

# Prepare feature and label arrays
features = np.array(dataset.iloc[:, 2:-1].values)
labels = np.array(dataset.iloc[:, 1])

# Initialize the XGBoost regressor with predefined hyperparameters
model = xgb.XGBRFRegressor(
    base_score=0.5, booster='gbtree', colsample_bylevel=1,
    colsample_bytree=0.3, eta=0.5, gamma=0, gpu_id=-1,
    importance_type='gain', interaction_constraints='',
    max_delta_step=0, max_depth=6, min_child_weight=5, missing=None,
    monotone_constraints='()', n_estimators=700, n_jobs=-1,
    num_parallel_tree=700, objective='reg:squarederror',
    random_state=1, reg_alpha=0, scale_pos_weight=1, subsample=1.0,
    tree_method='exact', validate_parameters=1, verbosity=None)

# Stratify labels for train-test splitting
bins = np.linspace(0, 1, 11)
y_binned = np.digitize(labels, bins)

# Perform stratified sampling and model evaluation 50 times
for i in range(0, 50):
    train_features, test_features, train_labels, test_labels = train_test_split(
        features, labels, test_size=0.2, shuffle=True, stratify=y_binned, random_state=i)

    # Log the train-test split for each model
    sets = open('../nf2/Results/stratified_sets.txt', 'w')
    print('Model' + str(i+1), train_labels, test_labels, file=sets)

    # Train the model and make predictions
    model.fit(train_features, train_labels)
    predictions = model.predict(test_features)

    # Evaluate and log the model performance
    errors = abs(predictions - test_labels)
    mae = round(np.mean(errors), 2)
    rmse = np.sqrt(mean_squared_error(test_labels, predictions))

    print(mae, rmse, sep='\t')
    model.save_model('Results/Models/stratified_model_' + str(i+1) + '.model')
    print('Model' + str(i+1), mae, rmse, sep='\t', file=output)

# Close the output file
output.close()
