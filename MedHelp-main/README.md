# Multipred: Empowering Healthcare Access in the Digital Age

Multipred is an innovative online platform designed to provide accessible healthcare information and predictive tools. Our mission is to empower individuals with knowledge and resources to make informed decisions about their health.

## Key Features

1. **Disease Predictions**
   - Diabetes Prediction Model (Accuracy: 70.13%)
   - Breast Cancer Prediction Model (Accuracy: 90.35%)

2. **BMI Calculator**
   - Helps users assess their body composition and weight status

3. **Health Information**
   - Comprehensive resources on various health topics

## Tech Stack

- **Backend**: Django
- **API**: FastAPI
- **Frontend**: Bootstrap
- **Machine Learning**: Support Vector Machine (SVM) for classification tasks

## Machine Learning Models

### Diabetes Prediction Model
- **Algorithm**: Support Vector Machine (SVM)
- **Accuracy**: 70.13%
- **Purpose**: Estimates the likelihood of having or developing diabetes based on user-input data and symptoms

### Breast Cancer Prediction Model
- **Algorithm**: Support Vector Machine (SVM)
- **Accuracy**: 90.35%
- **Purpose**: Predicts the likelihood of breast cancer based on relevant input features

## BMI Calculator

Our BMI (Body Mass Index) calculator allows users to:
- Input their height and weight
- Calculate their BMI
- Determine if they fall within a healthy weight range

## Project Structure

This project has two main branches:
- `main`: ML models are stored directly on the website server
- `main_api`: ML models are deployed as FastAPIs, with results fetched by the website server on request

## How to Run the Project

Follow these steps to run the Multipred project on your local system:

1. **Clone the repository**
   ```
   git clone https://github.com/your-username/Multipred.git
   cd Multipred
   ```

2. **Set up a virtual environment** (optional but recommended)
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```
   python manage.py migrate
   ```

5. **Create a superuser** (optional)
   ```
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```
   python manage.py runserver
   ```

7. **Access the application**
   Open your web browser and go to `http://127.0.0.1:8000/`

Note: If you're using the `main_api` branch, you'll need to run the FastAPI server separately. Refer to the branch-specific instructions for more details.

## Important Note

While Multipred provides valuable tools and information, it is not a substitute for professional medical advice. Users should always consult with healthcare professionals for accurate diagnoses and personalized treatment plans.

## Future Development

Multipred is continuously evolving. We are committed to expanding our offerings to become a comprehensive medical assistance portal, providing even more tools and services to support our users' health journeys.

## Contributing

We welcome contributions to improve Multipred. If you're interested in contributing, please [contact us](mailto:your-email@example.com) or check our [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).
