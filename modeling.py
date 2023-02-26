"""
This file will test multiple models for demand prediction.

Reminder that this is a regression problem, and we need to choose
our model based on RMSE & MAE.

Our base model will be the average demand of the training set.

"""
# Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from catboost import CatBoostRegressor, Pool

# Getting the dataset
dataset = pd.read_csv('data/final_prepared_dataset.csv')

# Splitting the data into features & target
features = dataset.drop(['Total Demand'],axis=1)
target = dataset['Total Demand']

# Splitting the dataset into training and testing
features_train, features_test, target_train, target_test = train_test_split(features,target,test_size=0.2,random_state=42,shuffle=True)

# Creating a validation set 
features_train, features_valid, target_train, target_valid = train_test_split(features_train,target_train,test_size=0.2,random_state=42,shuffle=True)

# Creating a table to monitor performance
performance_table = {'Model':[],'Training RMSE':[],'Validation RMSE':[]}

# Checking how the baseline model performs 
baseline_model = np.mean(target_train)
baseline_training_rmse = np.sqrt(mean_squared_error(target_train,np.full(shape=len(features_train),fill_value=baseline_model)))
baseline_validation_rmse = np.sqrt(mean_squared_error(target_valid,np.full(shape=len(features_valid),fill_value=baseline_model)))

# Adding results to the table
temp = performance_table['Model']
temp.append('Base Line')
performance_table['Model'] = temp
temp = performance_table['Training RMSE']
temp.append(baseline_training_rmse)
performance_table['Training RMSE'] = temp
temp = performance_table['Validation RMSE']
temp.append(baseline_validation_rmse)
performance_table['Validation RMSE'] = temp

# Building a Decision Tree Regressor
decision_tree = DecisionTreeRegressor(criterion='squared_error',max_features=None,random_state=42)
decision_tree.fit(features_train,target_train)
training_predictions_tree = decision_tree.predict(features_train)
validation_predictions_tree = decision_tree.predict(features_valid)
training_rmse_tree = np.sqrt(mean_squared_error(target_train,training_predictions_tree))
validation_rmse_tree = np.sqrt(mean_squared_error(target_valid,validation_predictions_tree))

# Adding results to the table
temp = performance_table['Model']
temp.append('Decision Tree')
performance_table['Model'] = temp
temp = performance_table['Training RMSE']
temp.append(training_rmse_tree)
performance_table['Training RMSE'] = temp
temp = performance_table['Validation RMSE']
temp.append(validation_rmse_tree)
performance_table['Validation RMSE'] = temp

# Building a Random Forest Regressor
random_forest = RandomForestRegressor(criterion='squared_error',bootstrap=True,max_samples=0.8,n_jobs=-1)
random_forest.fit(features_train,target_train)
training_predictions_forest = random_forest.predict(features_train)
validation_predictions_forest = random_forest.predict(features_valid)
training_rmse_forest = np.sqrt(mean_squared_error(target_train,training_predictions_forest))
validation_rmse_forest = np.sqrt(mean_squared_error(target_valid,validation_predictions_forest))

# Adding results to the table
temp = performance_table['Model']
temp.append('Random Forest')
performance_table['Model'] = temp
temp = performance_table['Training RMSE']
temp.append(training_rmse_forest)
performance_table['Training RMSE'] = temp
temp = performance_table['Validation RMSE']
temp.append(validation_rmse_forest)
performance_table['Validation RMSE'] = temp

# Building a Linear Regression Regressor
linear_regressor = LinearRegression(n_jobs=-1)
linear_regressor.fit(features_train,target_train)
training_predictions_linear = linear_regressor.predict(features_train)
validation_predictions_linear = linear_regressor.predict(features_valid)
training_rmse_linear = np.sqrt(mean_squared_error(target_train,training_predictions_linear))
validation_rmse_linear = np.sqrt(mean_squared_error(target_valid,validation_predictions_linear))

# Adding results to the table
temp = performance_table['Model']
temp.append('Linear Regression')
performance_table['Model'] = temp
temp = performance_table['Training RMSE']
temp.append(training_rmse_linear)
performance_table['Training RMSE'] = temp
temp = performance_table['Validation RMSE']
temp.append(validation_rmse_linear)
performance_table['Validation RMSE'] = temp

# Catboost Regressor 
catboost_regressor = CatBoostRegressor(iterations=1000,learning_rate=0.03,loss_function='RMSE')
catboost_regressor.fit(X=features_train,y=target_train,eval_set=(features_valid,target_valid),early_stopping_rounds=5,
                        use_best_model=True)
training_predictions = catboost_regressor.predict(features_train)
valid_predictions = catboost_regressor.predict(features_valid)

training_rmse = np.sqrt(mean_squared_error(target_train,training_predictions))
validation_rmse = np.sqrt(mean_squared_error(target_valid,valid_predictions))

# Adding results to the table
temp = performance_table['Model']
temp.append('CatBoost')
performance_table['Model'] = temp
temp = performance_table['Training RMSE']
temp.append(training_rmse)
performance_table['Training RMSE'] = temp
temp = performance_table['Validation RMSE']
temp.append(validation_rmse)
performance_table['Validation RMSE'] = temp


# Showing the performance table as a dataframe for easier viewing
performance_table_df = pd.DataFrame(performance_table)
print(performance_table_df)

# Getting the predictions for the whole dataset
predictions = catboost_regressor.predict(features)

# Appending the predictions to the preliminary dataset
final_data = pd.read_csv('data/transformed_preliminary_data.csv')
final_data = pd.concat((final_data,pd.Series(predictions)),axis=1)
final_data.to_csv('final_predictions.csv',index=False)