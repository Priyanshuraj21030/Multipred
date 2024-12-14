
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
import pandas as pd
import numpy as np
from joblib import load
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class DiabetesPredictor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diabetes Prediction System")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("QMainWindow {background-color: #f0f0f0;}")

        # Load the model and scaler
        self.model = load('diabetes_model.joblib')
        self.scaler = load('diabetes_scaler.joblib')

        self.init_ui()

    def init_ui(self):
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create tabs
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { border: 2px solid #c2c2c2; }
            QTabBar::tab { 
                background-color: #e1e1e1; 
                padding: 10px 20px;
                margin: 2px;
            }
            QTabBar::tab:selected { 
                background-color: #ffffff;
                border-bottom: 2px solid #2196F3;
            }
        """)

        # Add prediction tab
        prediction_tab = self.create_prediction_tab()
        tabs.addTab(prediction_tab, "Prediction")

        # Add analysis tab
        analysis_tab = self.create_analysis_tab()
        tabs.addTab(analysis_tab, "Model Analysis")

        layout.addWidget(tabs)

    def create_prediction_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Input form
        form_layout = QFormLayout()
        self.inputs = {}
        
        fields = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        
        for field in fields:
            self.inputs[field] = QLineEdit()
            self.inputs[field].setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 2px solid #ddd;
                    border-radius: 5px;
                }
                QLineEdit:focus {
                    border-color: #2196F3;
                }
            """)
            form_layout.addRow(field + ":", self.inputs[field])

        # Predict button
        predict_btn = QPushButton("Predict")
        predict_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        predict_btn.clicked.connect(self.predict)

        # Result label
        self.result_label = QLabel()
        self.result_label.setStyleSheet("""
            QLabel {
                padding: 20px;
                font-size: 18px;
                border-radius: 5px;
            }
        """)
        self.result_label.setAlignment(Qt.AlignCenter)

        # Add to layout
        layout.addLayout(form_layout)
        layout.addWidget(predict_btn)
        layout.addWidget(self.result_label)
        tab.setLayout(layout)
        return tab

    def create_analysis_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Add load data button
        load_btn = QPushButton("Load and Analyze Data")
        load_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        load_btn.clicked.connect(self.analyze_data)

        # Results text area
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-family: monospace;
            }
        """)

        layout.addWidget(load_btn)
        layout.addWidget(self.analysis_text)
        tab.setLayout(layout)
        return tab

    def predict(self):
        try:
            # Get values from inputs
            values = []
            for field in self.inputs:
                value = float(self.inputs[field].text())
                values.append(value)

            # Scale the input
            scaled_values = self.scaler.transform([values])
            
            # Make prediction
            prediction = self.model.predict(scaled_values)
            probability = self.model.predict_proba(scaled_values)
            
            # Format result
            result = "Diabetic" if prediction[0] == 1 else "Non-Diabetic"
            confidence = max(probability[0]) * 100
            
            # Update result label with styled text
            result_color = "#f44336" if result == "Diabetic" else "#4CAF50"
            self.result_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {result_color};
                    color: white;
                    padding: 20px;
                    font-size: 18px;
                    border-radius: 5px;
                }}
            """)
            self.result_label.setText(f"Prediction: {result}\nConfidence: {confidence:.2f}%")
            
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid numeric values for all fields.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def analyze_data(self):
        try:
            # Load the data
            df = pd.read_csv('diabetes.csv')
            X = df.drop('Outcome', axis=1)
            y = df['Outcome']
            
            # Scale and predict
            X_scaled = self.scaler.transform(X)
            predictions = self.model.predict(X_scaled)
            
            # Calculate metrics
            accuracy = accuracy_score(y, predictions)
            report = classification_report(y, predictions)
            conf_matrix = confusion_matrix(y, predictions)
            
            # Format results
            analysis_text = f"""
Model Performance Analysis
========================

Overall Accuracy: {accuracy:.2%}

Classification Report:
{report}

Confusion Matrix:
----------------
True Negative:  {conf_matrix[0][0]}
False Positive: {conf_matrix[0][1]}
False Negative: {conf_matrix[1][0]}
True Positive:  {conf_matrix[1][1]}
"""
            self.analysis_text.setText(analysis_text)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while analyzing data: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern looking style
    window = DiabetesPredictor()
    window.show()
    sys.exit(app.exec_())