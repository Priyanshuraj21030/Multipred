import pandas as pd
import numpy as np
from joblib import load
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the saved model and scaler
model = load('diabetes_model.joblib')
scaler = load('diabetes_scaler.joblib')

# Load the entire dataset
df = pd.read_csv('diabetes.csv')

# Separate features and target
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Scale the features
X_scaled = scaler.transform(X)

# Make predictions
predictions = model.predict(X_scaled)
probabilities = model.predict_proba(X_scaled)

# Calculate accuracy
accuracy = accuracy_score(y, predictions)
total_samples = len(df)
correct_predictions = (predictions == y).sum()

# Print results
print("\nModel Performance on Entire Dataset")
print("=" * 40)
print(f"Total samples tested: {total_samples}")
print(f"Correct predictions: {correct_predictions}")
print(f"Overall accuracy: {accuracy:.2%}")

# Print detailed classification report
print("\nDetailed Classification Report:")
print("=" * 40)
print(classification_report(y, predictions))

# Create confusion matrix
conf_matrix = confusion_matrix(y, predictions)
print("\nConfusion Matrix:")
print("=" * 40)
print("True Negative:", conf_matrix[0][0])
print("False Positive:", conf_matrix[0][1])
print("False Negative:", conf_matrix[1][0])
print("True Positive:", conf_matrix[1][1])

# Show some example predictions
print("\nSample Predictions (first 10 rows):")
print("=" * 40)
random_indices = np.random.choice(len(df), 10, replace=False)
for i in random_indices:
    
    actual = "Diabetic" if y.iloc[i] == 1 else "Non-Diabetic"
    predicted = "Diabetic" if predictions[i] == 1 else "Non-Diabetic"
    confidence = max(probabilities[i]) * 100
    print(f"\nRow {i+1}:")
    print(f"Actual: {actual}")
    print(f"Predicted: {predicted}")
    print(f"Confidence: {confidence:.2f}%")
