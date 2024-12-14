import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
data = pd.read_csv('breast.csv')

# Encode the target variable
le = LabelEncoder()
data['diagnosis'] = le.fit_transform(data['diagnosis'])

# Prepare features and target variable
X = data.drop(columns=['id', 'diagnosis'])
y = data['diagnosis']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize variables
best_accuracy = 0
best_model = None

# Iterate to improve the model
stop_training = False
for n_estimators in range(100, 1001, 100):
    if stop_training:
        break
    for learning_rate in [0.1, 0.05, 0.01]:
        if stop_training:
            break
        for max_depth in [3, 4, 5]:
            model = GradientBoostingClassifier(
                n_estimators=n_estimators,
                learning_rate=learning_rate,
                max_depth=max_depth,
                random_state=42
            )
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_model = model
                print(f"New best accuracy: {best_accuracy:.5f}")
            if best_accuracy >= 0.96:
                stop_training = True
                break

# Save the most accurate model
if best_model:
    joblib.dump(best_model, 'breast_cancer_model.pkl')
    print(f"Model saved with accuracy: {best_accuracy:.2f}")
else:
    print("Desired accuracy not achieved.")