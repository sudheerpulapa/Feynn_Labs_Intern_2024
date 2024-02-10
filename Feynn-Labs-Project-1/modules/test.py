# Import required functions from the 'model' module
from model import is_failure, failure_type

# Import necessary libraries
import pandas as pd
from sklearn.metrics import accuracy_score

# Read the predictive maintenance dataset into a DataFrame
df = pd.read_csv('predictive_maintenance.csv')

# Calculate accuracy scores for is_failure and failure_type predictions
is_failure_score = accuracy_score(is_failure(df), df.Target)
failure_type_score = accuracy_score(failure_type(df), df['Failure Type'])

# Display the accuracy scores
print(f'{is_failure_score = }')
print(f'{failure_type_score = }')
