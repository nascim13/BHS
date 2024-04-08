import pandas as pd
import numpy as np
from rpy2.robjects import r, pandas2ri  # For R to Python object conversion
import xgboost as xgb
import sys  # For accessing command-line arguments

# Load dataset from an RDS file specified as a command-line argument
print('Loading RDS file...')
readRDS = r['readRDS']  # R function for reading RDS files
dataset = readRDS(sys.argv[1])  # Load RDS file specified in command-line
dataset = pandas2ri.rpy2py_dataframe(dataset)  # Convert R dataframe to Pandas dataframe

# Prepare data for model
ids = np.array(dataset.iloc[:, 0])  # Extract IDs
features = np.array(dataset.iloc[:, 2:-1].values)  # Extract features
labels = np.array(dataset.iloc[:, 1])  # Extract labels
data_dmatrix = xgb.DMatrix(data=features, label=labels)  # Create DMatrix for XGBoost

# Initialize an array to store predictions from each of the 50 models
all_predictions = np.zeros((len(labels), 50))

# Load and predict with each of the 50 XGBoost models
for i in range(1, 51):
    model_path = f'Models/model{i}.model'  # Model file path
    model = xgb.Booster({'nthread': -1})  # Initialize model
    model.load_model(model_path)  # Load model from file
    predictions = model.predict(data_dmatrix)  # Make predictions
    all_predictions[:, i-1] = predictions  # Store predictions

# Calculate the average of predictions from all models
avg_predictions = np.mean(all_predictions, axis=1)

# Calculate errors and accuracy metrics
errors = abs(avg_predictions - labels)  # Absolute errors
mape = 100 * (errors / labels)  # Mean Absolute Percentage Error (MAPE)
accuracy = 100 - np.mean(mape)  # Accuracy

# Output results to a text file
output = open('predictions.txt', 'w')
print('Isolate', 'Value', 'Def', sep='\t', file=output)  # Print header

# Print each ID with its label and prediction
for i in range(len(ids)):
    print(ids[i], labels[i], 'Label', sep='\t', file=output)
    print(ids[i], avg_predictions[i], 'Prediction', sep='\t', file=output)

# Close the output file
output.close()
