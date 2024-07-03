from joblib import load
from sklearn.preprocessing import StandardScaler
import numpy as np

# Load your trained model
model = load('D:\Study Material\Projects\MEDHELP\MEDHELP\ml_models\diabetes_model.joblib')

# Create a StandardScaler instance
scaler = StandardScaler()

input_data = (8, 283, 23.3, 85)

# Changing to a numpy array
input_numpyarray = np.asarray(input_data)

# Reshaping
input_reshaped = input_numpyarray.reshape(1, -1)

# Fit the scaler on your training data (if available)
# You should replace X_train with your actual training data
# scaler.fit(X_train)

# Standardize the input data
inp = scaler.fit_transform(input_reshaped)

y_pred = model.predict(inp)

if y_pred[0] == 1:
    print('Diabetic')
else:
    print('Not Diabetic')
