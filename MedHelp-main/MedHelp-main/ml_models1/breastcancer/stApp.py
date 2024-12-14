# app.py
import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the trained model
model = joblib.load('breast_cancer_model.pkl')

def predict_cancer(features):
    prediction = model.predict([features])
    probability = model.predict_proba([features])
    return prediction[0], probability[0]

def main():
    st.set_page_config(page_title="Breast Cancer Predictor", layout="wide")
    
    # Header
    st.title("🎗️ Breast Cancer Prediction System")
    st.markdown("---")

    # Create three columns
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.subheader("Patient Measurements")
        
        # Create input fields in organized groups
        with st.expander("Mean Values", expanded=True):
            radius_mean = st.number_input("Radius Mean", 0.0, 100.0, 14.0)
            texture_mean = st.number_input("Texture Mean", 0.0, 100.0, 19.0)
            perimeter_mean = st.number_input("Perimeter Mean", 0.0, 200.0, 92.0)
            area_mean = st.number_input("Area Mean", 0.0, 3000.0, 654.0)
            smoothness_mean = st.number_input("Smoothness Mean", 0.0, 1.0, 0.1)
            compactness_mean = st.number_input("Compactness Mean", 0.0, 1.0, 0.1)
            concavity_mean = st.number_input("Concavity Mean", 0.0, 1.0, 0.1)
            concave_points_mean = st.number_input("Concave Points Mean", 0.0, 1.0, 0.05)
            symmetry_mean = st.number_input("Symmetry Mean", 0.0, 1.0, 0.2)
            fractal_dimension_mean = st.number_input("Fractal Dimension Mean", 0.0, 1.0, 0.06)

        with st.expander("Standard Error Values"):
            radius_se = st.number_input("Radius SE", 0.0, 10.0, 0.4)
            texture_se = st.number_input("Texture SE", 0.0, 10.0, 1.2)
            perimeter_se = st.number_input("Perimeter SE", 0.0, 10.0, 2.8)
            area_se = st.number_input("Area SE", 0.0, 100.0, 40.0)
            smoothness_se = st.number_input("Smoothness SE", 0.0, 0.1, 0.007)
            compactness_se = st.number_input("Compactness SE", 0.0, 0.1, 0.025)
            concavity_se = st.number_input("Concavity SE", 0.0, 0.1, 0.03)
            concave_points_se = st.number_input("Concave Points SE", 0.0, 0.1, 0.01)
            symmetry_se = st.number_input("Symmetry SE", 0.0, 0.1, 0.02)
            fractal_dimension_se = st.number_input("Fractal Dimension SE", 0.0, 0.1, 0.003)

        with st.expander("Worst Values"):
            radius_worst = st.number_input("Radius Worst", 0.0, 100.0, 17.0)
            texture_worst = st.number_input("Texture Worst", 0.0, 100.0, 28.0)
            perimeter_worst = st.number_input("Perimeter Worst", 0.0, 300.0, 120.0)
            area_worst = st.number_input("Area Worst", 0.0, 4000.0, 900.0)
            smoothness_worst = st.number_input("Smoothness Worst", 0.0, 1.0, 0.13)
            compactness_worst = st.number_input("Compactness Worst", 0.0, 1.0, 0.25)
            concavity_worst = st.number_input("Concavity Worst", 0.0, 1.0, 0.23)
            concave_points_worst = st.number_input("Concave Points Worst", 0.0, 1.0, 0.12)
            symmetry_worst = st.number_input("Symmetry Worst", 0.0, 1.0, 0.29)
            fractal_dimension_worst = st.number_input("Fractal Dimension Worst", 0.0, 1.0, 0.08)

        # Create feature array
        features = [
            radius_mean, texture_mean, perimeter_mean, area_mean, smoothness_mean,
            compactness_mean, concavity_mean, concave_points_mean, symmetry_mean,
            fractal_dimension_mean, radius_se, texture_se, perimeter_se, area_se,
            smoothness_se, compactness_se, concavity_se, concave_points_se,
            symmetry_se, fractal_dimension_se, radius_worst, texture_worst,
            perimeter_worst, area_worst, smoothness_worst, compactness_worst,
            concavity_worst, concave_points_worst, symmetry_worst, fractal_dimension_worst
        ]

        if st.button("Predict", type="primary"):
            prediction, probability = predict_cancer(features)
            
            st.markdown("---")
            st.subheader("Prediction Results")
            
            # Display prediction
            if prediction == 1:
                st.error("⚠️ Malignant (Cancerous)")
                prob = probability[1] * 100
            else:
                st.success("✅ Benign (Non-cancerous)")
                prob = probability[0] * 100
                
            st.metric("Confidence", f"{prob:.2f}%")
            
            # Display warning
            st.warning("""
            **Disclaimer:** This prediction is based on a machine learning model and should not be used as the sole basis for medical decisions. 
            Please consult with a healthcare professional for proper diagnosis and treatment.
            """)

if __name__ == "__main__":
    main()