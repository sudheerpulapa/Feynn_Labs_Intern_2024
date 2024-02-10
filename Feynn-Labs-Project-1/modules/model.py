import pandas as pd
import pickle

# Load the 'is_failure' model
with open('models/is_failure.pkl', 'rb') as f:
    model = pickle.load(f)

# Function to predict whether there is a failure or not
def is_failure(x):
    x = x[['Type', 'Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']]
    df1 = pd.get_dummies(x, columns=['Type'])
    df1[['Type_H', 'Type_L', 'Type_M']] = df1[['Type_H', 'Type_L', 'Type_M']].astype(int)
    return model.predict(df1)

# Load the 'failure_type' model and its inverse encoding
with open('models/failure_type.pkl', 'rb') as f:
    model2 = pickle.load(f)

with open('models/encoding.pkl', 'rb') as f:
    inverse = pickle.load(f)

# Function to predict failure type
def failure_type(x):
    x = x[['Type', 'Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']]
    df1 = pd.get_dummies(x, columns=['Type'])
    df1[['Type_H', 'Type_L', 'Type_M']] = df1[['Type_H', 'Type_L', 'Type_M']].astype(int)
    prediction = model2.predict(df1)
    return pd.Series(prediction).map(inverse)

# Function to load and transform data
def data():
    df = pd.read_csv('predictive_maintenance.csv')
    return df[['Type', 'Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']]
