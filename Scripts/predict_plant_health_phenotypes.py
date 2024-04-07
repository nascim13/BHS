import pandas as pd
import numpy as np
from rpy2.robjects import r, pandas2ri
import xgboost as xgb
import sys

# Load dataset
print('Loading RDS file...')
readRDS = r['readRDS']
dataset = readRDS(sys.argv[1])
dataset = pandas2ri.rpy2py_dataframe(dataset)

# Prepare data
ids = np.array(dataset.iloc[:, 0])
features = np.array(dataset.iloc[:, 2:-1].values)
labels = np.array(dataset.iloc[:, 1])
data_dmatrix = xgb.DMatrix(data=features, label=labels)

# Initialize predictions array
all_predictions = np.zeros((len(labels), 50))

# Load and predict with each of the 50 models
for i in range(1, 51):
    model_path = f'Models/model{i}.model'
    model = xgb.Booster({'nthread': -1})
    model.load_model(model_path)
    predictions = model.predict(data_dmatrix)
    all_predictions[:, i-1] = predictions

# Calculate average predictions
avg_predictions = np.mean(all_predictions, axis=1)

# Calculate errors and accuracy
errors = abs(avg_predictions - labels)
mape = 100 * (errors / labels)
accuracy = 100 - np.mean(mape)

# Output results
output = open('predictions.txt', 'w')
print('Isolate', 'Value', 'Def', sep='\t', file=output)

for i in range(len(ids)):
    print(ids[i], labels[i], 'Label', sep='\t', file=output)
    print(ids[i], avg_predictions[i], 'Prediction', sep='\t', file=output)

# Optionally print accuracy and MAPE
#print(round(accuracy, 2), '%.', round(np.mean(errors), 2), 'MAPE:', np.mean(mape), sep='\t')

output.close()

