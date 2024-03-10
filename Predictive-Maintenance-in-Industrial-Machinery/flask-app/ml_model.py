import pickle

with open('artifacts/model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('artifacts/preprocessor.pkl', 'rb') as f:
    preprocessor = pickle.load(f)

def ml_function(df):
    df1 = df[["Type", "Air temperature [K]", 
             "Process temperature [K]", "Rotational speed [rpm]", 
             "Torque [Nm]", "Tool wear [min]", "Power"]]
    scaled_df = preprocessor.transform(df1)
    predictions = model.predict(scaled_df)
    failear_df = df[predictions == 1]
    failear_df = failear_df.reset_index()
    return failear_df