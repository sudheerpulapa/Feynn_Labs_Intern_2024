import os
import pickle
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier

# Read the dataset from a CSV file
df = pd.read_csv('predictive_maintenance.csv')

# Perform one-hot encoding for the 'Type' column
df1 = pd.get_dummies(df, columns=['Type'])
df1[['Type_H', 'Type_L', 'Type_M']] = df1[['Type_H', 'Type_L', 'Type_M']].astype(int)

# Define features (X) and target variable (y)
X = df1[['Air temperature [K]', 'Process temperature [K]',
       'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]',
       'Type_H', 'Type_L', 'Type_M']]
y = df1.Target

# Apply SMOTE for handling imbalanced classes in the target variable
smote = SMOTE()
X_smote, y_smote = smote.fit_resample(X, y)

# Create a RandomForestClassifier model with specified parameters
best_model = RandomForestClassifier(n_estimators=300, verbose=2)
best_model.fit(X_smote, y_smote)

# Create necessary directories if they don't exist
if not os.path.exists('models'):
    os.mkdir('models')

if not os.path.exists('uploaded'):
    os.mkdir('uploaded')

# Save the trained model for predicting 'is_failure'
with open('models/is_failure.pkl', 'wb') as f:
    pickle.dump(best_model, f)

# Prepare data for predicting 'Failure Type'
X = df1[['Air temperature [K]', 'Process temperature [K]',
       'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]',
       'Type_H', 'Type_L', 'Type_M']]
y = df1['Failure Type']

# Encode the 'Failure Type' column and create an inverse mapping
labelEncoding = {j: i for i, j in enumerate(y.unique())}
inverse = {j: i for i, j in labelEncoding.items()}
y = y.map(labelEncoding)

# Apply SMOTE for handling imbalanced classes in the encoded 'Failure Type'
X_smote, y_smote = smote.fit_resample(X, y)

# Create a new RandomForestClassifier model for predicting 'Failure Type'
best_model = RandomForestClassifier(n_estimators=300, verbose=2)
best_model.fit(X_smote, y_smote)

# Save the trained model for predicting 'Failure Type'
with open('models/failure_type.pkl', 'wb') as f:
    pickle.dump(best_model, f)

# Save the inverse mapping for 'Failure Type' encoding
with open('models/encoding.pkl', 'wb') as f:
    pickle.dump(inverse, f)
