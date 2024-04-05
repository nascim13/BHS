import pandas as pd
import numpy as np
import numpy as np
from rpy2.robjects import r
from rpy2.robjects import pandas2ri
import xgboost as xgb
from sklearn.model_selection import KFold
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import sys

#output = open ('bestParameters.txt', 'w')
output = open ('../nf2/Results/stratified_results.txt', 'w')
print ('Model', 'MAE', 'RMSE', sep = '\t', file = output)

#np.seterr(divide='ignore', invalid='ignore')

print ('Loading RDS file...')

readRDS = r['readRDS']
dataset = readRDS(sys.argv[1])
#dataset = readRDS('samp_kmer_table.rds')
dataset = pandas2ri.rpy2py_dataframe(dataset)

# Convert to numpy array
features = np.array(dataset.iloc[:, 2:-1].values)

# Labels are the values we want to predict
labels = np.array(dataset.iloc[:, 1])

#print('The shape of our features is:', features.shape)

model = xgb.model = xgb.XGBRFRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
                colsample_bytree=0.3, eta=0.5, gamma=0, gpu_id=-1,
                importance_type='gain', interaction_constraints='',
                max_delta_step=0, max_depth=6, min_child_weight=5, missing=None,
                monotone_constraints='()', n_estimators=700, n_jobs=-1,
                num_parallel_tree=700, objective='reg:squarederror',
                random_state=1, reg_alpha=0, scale_pos_weight=1, subsample=1.0,
                tree_method='exact', validate_parameters=1, verbosity=None)

# Cross validation fold split

bins = np.linspace(0, 1, 11)
y_binned = np.digitize(labels, bins)

print(bins)
print(y_binned)

#kfold = KFold(n_splits = 10, shuffle = True, random_state = 0)

#random_search = RandomizedSearchCV(model, param_distributions = params, n_iter = param_comb, n_jobs = -1, cv = 10, random_state = 0)

#print ('Finding best parameters...')

#RS = random_search.fit(features, labels)
#RS.best_estimator_

#print (RS.best_estimator_, file = output)

for i in range (0, 50):

	train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.2, shuffle = True, stratify = y_binned, random_state = i)

	#train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.2, random_state = 0)

	sets = open ('../nf2/Results/stratified_sets.txt', 'w')
	print ('Model' + str(i+1), train_labels, test_labels, file = sets)

#	print ('Training the model...')
	# Train the model on training data
	model.fit(train_features, train_labels)

#	print ('Predicting test labels...')
	# Use the forest's predict method on the test data
	predictions = model.predict(test_features)

#	print ('Calculating errors...')
	# Calculate the absolute errors
	errors = abs(predictions - test_labels)
	mae = round(np.mean(errors), 2)

	# Print out the mean absolute error (mae)
#	print('MAE:', mae)

	# Calculate root mean squared error
	rmse = np.sqrt(mean_squared_error(test_labels, predictions))
#	print ('RMSE: ', rmse)

	# Calculate mean absolute percentage error (MAPE)
	#mape = 100 * (errors / test_labels)
	#print ('Mean Absolute Percentage Error:', round(np.mean(mape), 2))

	# Calculate and display accuracy
	#accuracy = 100 - np.mean(mape)
	#print('Accuracy:', round(accuracy, 2), '%.')

	print (mae, rmse, sep = '\t')

	model.save_model('Results/Models/stratified_model_' + str(i+1) + '.model')
	#	model.dump_model('Models/model' + str(modelCount) + '.txt')

	print ('Model' + str(i+1), mae, rmse, sep = '\t', file = output)
#	sets.close()
