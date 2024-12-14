import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np

def test_model():
    # Load the model
    model = joblib.load('breast_cancer_model.pkl')
    
    # Load and prepare the data
    data = pd.read_csv('breast.csv')
    
    # Convert M/B to 1/0
    diagnosis_map = {'M': 1, 'B': 0}
    actual_labels = data['diagnosis'].map(diagnosis_map)
    
    # Prepare features (drop id and diagnosis)
    features = data.drop(columns=['id', 'diagnosis'])
    
    # Make predictions
    predictions = model.predict(features)
    probabilities = model.predict_proba(features)
    
    # Calculate accuracy
    accuracy = accuracy_score(actual_labels, predictions)
    
    # Get number of correct predictions
    correct_predictions = np.sum(predictions == actual_labels)
    total_samples = len(actual_labels)
    
    # Print results
    print("\n=== Model Performance Report ===")
    print(f"Total samples tested: {total_samples}")
    print(f"Correct predictions: {correct_predictions}")
    print(f"Overall accuracy: {accuracy:.2%}")
    
    # Print detailed classification report
    print("\n=== Detailed Classification Report ===")
    print(classification_report(actual_labels, predictions, target_names=['Benign', 'Malignant']))
    
    # Print confusion matrix
    conf_matrix = confusion_matrix(actual_labels, predictions)
    print("\n=== Confusion Matrix ===")
    print("                  Predicted Benign    Predicted Malignant")
    print(f"Actual Benign          {conf_matrix[0][0]}                {conf_matrix[0][1]}")
    print(f"Actual Malignant       {conf_matrix[1][0]}                {conf_matrix[1][1]}")

if __name__ == "__main__":
    test_model()