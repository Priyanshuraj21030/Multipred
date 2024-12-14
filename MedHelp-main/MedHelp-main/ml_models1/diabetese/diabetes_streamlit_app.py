
import streamlit as st
import pandas as pd
import numpy as np
from joblib import load
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the model and scaler
model = load('diabetes_model.joblib')
scaler = load('diabetes_scaler.joblib')

def main():
    st.set_page_config(page_title="Diabetes Prediction System", layout="wide")
    st.markdown("""
        <style>
            .main { background-color: #f0f0f0; }
            h1 { color: #2196F3; }
        </style>
    """, unsafe_allow_html=True)
    st.title("Diabetes Prediction System")
    
    tabs = st.tabs(["Prediction", "Model Analysis"])
    
    with tabs[0]:
        st.header("Prediction")
        # Input fields
        col1, col2, col3 = st.columns(3)
        with col1:
            pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=0)
            glucose = st.number_input("Glucose", min_value=0, max_value=200, value=120)
            blood_pressure = st.number_input("Blood Pressure", min_value=0, max_value=130, value=70)
        with col2:
            skin_thickness = st.number_input("Skin Thickness", min_value=0, max_value=100, value=20)
            insulin = st.number_input("Insulin", min_value=0, max_value=900, value=79)
            bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=32.0)
        with col3:
            dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=2.5, value=0.3725,format="%.3f")
            age = st.number_input("Age", min_value=1, max_value=120, value=29)
            st.text("")  # Empty space
            
        predict_btn = st.button("Predict")
        
        if predict_btn:
            try:
                # Collect inputs
                values = [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]
                # Scale the input
                scaled_values = scaler.transform([values])
                # Make prediction
                prediction = model.predict(scaled_values)
                probability = model.predict_proba(scaled_values)
                # Display result
                result = "Diabetic" if prediction[0] == 1 else "Non-Diabetic"
                confidence = max(probability[0]) * 100
                result_color = "red" if result == "Diabetic" else "green"
                st.markdown(f"<h2 style='color:{result_color};'>Prediction: {result}</h2>", unsafe_allow_html=True)
                st.markdown(f"<h3>Confidence: {confidence:.2f}%</h3>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    with tabs[1]:
        st.header("Model Analysis")
        if st.button("Load and Analyze Data"):
            try:
                # Load data
                df = pd.read_csv('diabetes.csv')
                X = df.drop('Outcome', axis=1)
                y = df['Outcome']
                # ...existing code...
                X_scaled = scaler.transform(X)
                predictions = model.predict(X_scaled)
                # Calculate metrics
                accuracy = accuracy_score(y, predictions)
                report = classification_report(y, predictions)
                conf_matrix = confusion_matrix(y, predictions)
                # Display analysis
                st.subheader("Overall Accuracy")
                st.write(f"{accuracy:.2%}")
                st.subheader("Classification Report")
                st.text(report)
                st.subheader("Confusion Matrix")
                st.write(conf_matrix)
            except Exception as e:
                st.error(f"An error occurred while analyzing data: {str(e)}")
    
if __name__ == '__main__':
    main()