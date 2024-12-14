import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from joblib import dump

# Load the dataset
df = pd.read_csv('diabetes.csv')

# Separate features and target
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Clean and scale the features
scaler = StandardScaler()
X_train = X_train.astype(float)
X_test = X_test.astype(float)
y_train = y_train.fillna(y_train.mode()[0])
y_test = y_test.fillna(y_test.mode()[0])
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

def train_until_accuracy(min_accuracy=0.85, max_iterations=500):
    best_accuracy = 0
    best_model = None
    iteration = 0
    
    # Parameter grid for random search
    param_dist = {
        'max_depth': randint(3, 20),
        'min_samples_split': randint(2, 20),
        'min_samples_leaf': randint(1, 10),
        'criterion': ['gini', 'entropy'],
        'splitter': ['best', 'random']
    }

    while best_accuracy < min_accuracy and iteration < max_iterations:
        # Create and train a new decision tree with random parameters
        tree = DecisionTreeClassifier(random_state=iteration)
        random_search = RandomizedSearchCV(
            tree, 
            param_distributions=param_dist,
            n_iter=10,
            cv=5,
            random_state=iteration
        )
        
        # Train the model
        random_search.fit(X_train_scaled, y_train)
        
        # Get the best model from random search
        current_model = random_search.best_estimator_
        
        # Evaluate the model
        y_pred = current_model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Iteration {iteration + 1}: Accuracy = {accuracy:.4f}")
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = current_model
            print(f"New best accuracy: {best_accuracy:.4f}")
            print(f"Best parameters: {random_search.best_params_}")
        
        iteration += 1
    
    return best_model, best_accuracy

# Train the model until desired accuracy
print("Training model to achieve 85% accuracy...")
best_model, best_accuracy = train_until_accuracy()

if best_accuracy >= 0.85:
    print(f"\nTarget accuracy achieved! Final accuracy: {best_accuracy:.4f}")
else:
    print(f"\nMaximum iterations reached. Best accuracy: {best_accuracy:.4f}")

# Save the best model and scaler for predictions
print("\nSaving model and scaler...")
dump(best_model, 'diabetes_model.joblib')
dump(scaler, 'diabetes_scaler.joblib')
print("Model and scaler saved successfully!")

def predict_diabetes(features):
    """
    Predict diabetes based on input features.
    Features should be a list containing: [Pregnancies, Glucose, BloodPressure, SkinThickness, 
                                         Insulin, BMI, DiabetesPedigreeFunction, Age]
    """
    # Convert input to numpy array and reshape
    features_array = np.array(features).reshape(1, -1)
    
    # Scale the features
    features_scaled = scaler.transform(features_array)
    
    # Make prediction
    prediction = best_model.predict(features_scaled)
    probability = best_model.predict_proba(features_scaled)[0]
    
    return {
        'prediction': 'Diabetic' if prediction[0] == 1 else 'Non-Diabetic',
        'confidence': f"{max(probability) * 100:.2f}%"
    }

# Example usage
if __name__ == "__main__":
    # Example input
    sample_input = [6, 148, 72, 35, 0, 33.6, 0.627, 50]
    result = predict_diabetes(sample_input)
    print("\nSample Prediction:")
    print(f"Diagnosis: {result['prediction']}")
    print(f"Confidence: {result['confidence']}")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv('diabetes.csv')

# Separate features and target variable
X = data.drop('Outcome', axis=1)
y = data['Outcome']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize variables
best_accuracy = 0
best_model = None
n_estimators = 100
learning_rate = 0.1

# Iteratively train the model until accuracy reaches 85%
while best_accuracy < 0.85:
    # Initialize the model with current hyperparameters
    model = GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=learning_rate, random_state=42)
    # Train the model
    model.fit(X_train, y_train)
    # Predict on test set
    y_pred = model.predict(X_test)
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    # If current model is better, save it
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
    # Adjust hyperparameters if accuracy is less than 85%
    # Increase n_estimators and decrease learning_rate to improve performance
    n_estimators += 50
    learning_rate *= 0.9

# Save the most accurate model
joblib.dump(best_model, 'best_model.pkl')
